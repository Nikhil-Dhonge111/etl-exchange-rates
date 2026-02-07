import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from ETL_pipeline import extract


def test_extract_returns_json(mocker):
    mock_response = {
        "base": "USD",
        "date": "2026-02-07",
        "rates": {"INR": 83.0}
    }

    mocker.patch(
        "ETL_pipeline.requests.get",
        return_value=mocker.Mock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=lambda: None
        )
    )

    data = extract()
    assert data["base"] == "USD"
    assert "rates" in data
