import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
import datetime

# Mock yfinance before importing app to avoid network calls during module load
import yfinance as yf

# Function to create mock data
def create_mock_yf_data(*args, **kwargs):
    dates = pd.date_range("2023-01-01", "2023-01-10")
    # Create simple data with slight variations to ensure std() > 0
    close_prices = [100.0, 101.0, 102.0, 101.5, 103.0, 102.5, 104.0, 103.5, 105.0, 106.0]
    df = pd.DataFrame({"Close": close_prices}, index=dates)
    df.index.name = "Date"
    return df

@pytest.fixture(autouse=True)
def mock_yfinance():
    with patch("yfinance.download", side_effect=create_mock_yf_data) as _mock_yf:
        yield _mock_yf

def test_load_data():
    from app import load_data
    
    # Call the function
    data = load_data("INFY.NS", datetime.date(2023, 1, 1), datetime.date(2023, 1, 10))
    
    # Assertions
    assert not data.empty
    assert "simple_return" in data.columns
    assert "log_return" in data.columns
    
    # Since we have 10 data points, dropna() removes the first one
    assert len(data) == 9
    
    # Check if simple_return is correctly calculated
    # For day 2 (index 1), price went from 100 to 101, which is a 1% return.
    assert np.isclose(data["simple_return"].iloc[0], 0.01)
    
    # Check log return
    assert np.isclose(data["log_return"].iloc[0], np.log(101.0 / 100.0))

def test_load_market():
    from app import load_market
    
    market = load_market(datetime.date(2023, 1, 1), datetime.date(2023, 1, 10))
    
    assert not market.empty
    assert "market_return" in market.columns
    assert len(market) == 9
    assert np.isclose(market["market_return"].iloc[0], np.log(101.0 / 100.0))

from streamlit.testing.v1 import AppTest

def test_streamlit_app_renders():
    """Test that the Streamlit app runs without exceptions."""
    # Use Streamlit's testing framework
    at = AppTest.from_file("app.py", default_timeout=30)
    
    # Run the app
    at.run()
    
    # Check that there are no exceptions
    assert not at.exception
    
    # Check title
    assert "Indian Equities Analytics Dashboard" in at.title[0].value
    
    # Check metrics
    metrics = at.metric
    assert len(metrics) == 5
    assert metrics[0].label == "Annual Return"
    assert metrics[1].label == "Annual Volatility"
    assert metrics[2].label == "Sharpe Ratio"
    assert metrics[3].label == "Beta (vs NIFTY)"
    assert metrics[4].label == "95% VaR (Daily)"

