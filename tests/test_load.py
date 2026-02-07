import sqlite3
import pandas as pd
import sys
import os 
    
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from ETL_pipeline import load


def test_load_inserts_data():
    conn = sqlite3.connect(":memory:")

    conn.execute("""
        CREATE TABLE exchange_rates (
            currency TEXT,
            rate REAL,
            base_currency TEXT,
            date TEXT,
            ingested_at TEXT
        )
    """)

    df = pd.DataFrame({
        "currency": ["INR"],
        "rate": [83.0],
        "base_currency": ["USD"],
        "date": ["2026-02-07"],
        "ingested_at": ["2026-02-07T10:00:00"]
    })

    load(df, conn)

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM exchange_rates")
    count = cursor.fetchone()[0]

    assert count == 1
    conn.close()
