import sqlite3
import sys
import os 
    
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from ETL_pipeline import get_last_loaded_date

def test_get_last_loaded_date():
    conn = sqlite3.connect(":memory:")

    conn.execute("""
        CREATE TABLE exchange_rates (
            date TEXT
        )
    """)

    conn.execute("INSERT INTO exchange_rates VALUES ('2026-02-06')")
    conn.execute("INSERT INTO exchange_rates VALUES ('2026-02-07')")
    conn.commit()

    last_date = get_last_loaded_date(conn)
    assert last_date == "2026-02-07"

    conn.close()
