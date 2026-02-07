import pandas as pd
import pytest
import sys
import os 

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from ETL_pipeline import transform

def sample_api_data():
    return {
        "base": "USD",
        "date": "2026-02-07",
        "rates": {
            "INR": 83.1,
            "EUR": 0.92
        }
    }


def test_transform_success():
    data = sample_api_data()
    df = transform(data)

    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2
    assert set(df.columns) == {
        "currency",
        "rate",
        "base_currency",
        "date",
        "ingested_at"
    }


def test_transform_negative_rate():
    data = sample_api_data()
    data["rates"]["INR"] = -10

    with pytest.raises(ValueError):
        transform(data)
