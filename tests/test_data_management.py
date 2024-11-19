import pytest
from datetime import datetime, timedelta
from moonedge.data_management.market_data import fetch_historical_data, clean_market_data
from moonedge.data_management.lunar_data import calculate_lunar_phases

def test_fetch_historical_data():
    try:
        # Default start date (5 years ago)
        data = fetch_historical_data("AAPL")
        assert not data.empty
        assert "Open" in data.columns

        # Custom start date (e.g., 1 year ago)
        start_date = datetime.now() - timedelta(days=365)
        data_custom = fetch_historical_data("AAPL", start_date=start_date)
        assert not data_custom.empty
        assert "Open" in data_custom.columns
    except RuntimeError as e:
        pytest.fail(f"Fetching historical data failed: {e}")

def test_calculate_lunar_phases():
    try:
        # Default start date (5 years ago)
        phases = calculate_lunar_phases()
        assert not phases.empty
        assert "phase" in phases.columns

        # Custom start date (e.g., 1 year ago)
        start_date = datetime.now() - timedelta(days=365)
        phases_custom = calculate_lunar_phases(start_date=start_date)
        assert not phases_custom.empty
        assert "phase" in phases_custom.columns
    except RuntimeError as e:
        pytest.fail(f"Calculating lunar phases failed: {e}")

def test_clean_market_data():
    try:
        data = fetch_historical_data("AAPL")
        cleaned_data = clean_market_data(data)
        assert not cleaned_data.isnull().values.any()
    except RuntimeError as e:
        pytest.fail(f"Cleaning market data failed: {e}")

def test_fetch_historical_data_cache():
    """Test if the cache system is working properly."""
    try:
        data_first = fetch_historical_data("AAPL")
        data_cached = fetch_historical_data("AAPL")
        assert data_first.equals(data_cached)
    except RuntimeError as e:
        pytest.fail(f"Caching test failed: {e}")
