import requests
import pandas as pd
import sqlite3
import logging
import json
from pathlib import Path
from datetime import datetime
# used for the automated run ad email alerts
import os
import smtplib
from email.message import EmailMessage
import traceback

# os → read GitHub Secrets
# smtplib → send email
# EmailMessage → clean email formatting
# traceback → useful error details in failure emai

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


def send_email(subject: str, body: str):
    print("send_email() called")
    required_vars = ["EMAIL_USER", "EMAIL_PASS", "EMAIL_TO"]

    # Skip email if env vars not set (local run)
    if not all(var in os.environ for var in required_vars):
        print("Email credentials not found. Skipping email notification.")
        return

    msg = EmailMessage()
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = os.environ["EMAIL_TO"]
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            os.environ["EMAIL_USER"],
            os.environ["EMAIL_PASS"]
        )
        smtp.send_message(msg)


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
    try:
        main()

        send_email(
            subject="✅ ETL Pipeline Success",
            body="Exchange Rates ETL pipeline completed successfully."
        )

    except Exception:
        error_details = traceback.format_exc()

        send_email(
            subject="❌ ETL Pipeline Failed",
            body=f"ETL pipeline failed:\n\n{error_details}"
        )

        raise
