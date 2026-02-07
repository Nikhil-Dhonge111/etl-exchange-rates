import requests
import pandas as pd
import sqlite3
import logging
import json
from pathlib import Path
from datetime import datetime

DB_NAME = "exchange_rates.db"
TABLE_NAME = "exchange_rates"
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# Logging
logging.basicConfig(
    filename="etl.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def get_last_loaded_date(conn):
    cursor = conn.cursor()
    cursor.execute(f"SELECT MAX(date) FROM {TABLE_NAME}")
    result = cursor.fetchone()
    logging.info(f"Last loaded date: {result[0]}")
    return result[0]


def extract():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    logging.info("API response received")
    return response.json()


def save_raw_data(data):
    raw_dir = Path("raw_data")
    raw_dir.mkdir(exist_ok=True)

    file_path = raw_dir / f"exchange_rates_{data['date']}.json"
    with open(file_path, "w") as f:
        json.dump(data, f)

    logging.info(f"Raw data saved: {file_path}")


def transform(data):
    df = pd.DataFrame(
        data["rates"].items(),
        columns=["currency", "rate"]
    )

    df["base_currency"] = data["base"]
    df["date"] = data["date"]
    df["ingested_at"] = datetime.utcnow().isoformat()

    # Data quality checks
    if df.isnull().any().any():
        raise ValueError("Null values found in data")

    if (df["rate"] <= 0).any():
        raise ValueError("Invalid exchange rate")

    logging.info("Data transformation completed")
    return df


def load(df, conn):
    try:
        df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
        logging.info("Data loaded into database")
    except sqlite3.IntegrityError:
        logging.warning("Duplicate records detected. Load skipped.")


def main():
    logging.info("ETL job started")

    conn = sqlite3.connect(DB_NAME)

    # Create table
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            currency TEXT,
            rate REAL,
            base_currency TEXT,
            date TEXT,
            ingested_at TEXT
        )
        """
    )

    # Enforce idempotency
    conn.execute(
        f"""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_currency_date
        ON {TABLE_NAME}(currency, date)
        """
    )

    last_date = get_last_loaded_date(conn)

    data = extract()
    save_raw_data(data)

    if data["date"] == last_date:
        logging.info("No new data. ETL skipped.")
        conn.close()
        return

    df = transform(data)
    load(df, conn)

    conn.commit()
    conn.close()

    logging.info("ETL job completed successfully")


if __name__ == "__main__":
    main()
