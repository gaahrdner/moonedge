import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_historical_data(ticker: str, start_date: datetime = None) -> pd.DataFrame:
    """Fetch historical market data for the given ticker.

    Args:
        ticker (str): Stock ticker symbol.
        start_date (datetime, optional): Start date for fetching historical data. Defaults to 5 years ago.

    Returns:
        pd.DataFrame: A dataframe containing historical market data.
    """
    end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=5*365)
    directory = "src/moonedge/data"
    filename = f"{directory}/{ticker}_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.csv"

    try:
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Check if data already exists on disk
        if os.path.exists(filename):
            return pd.read_csv(filename, index_col='Date', parse_dates=True)

        # Fetch data from Yahoo Finance
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

        # Save data to disk for caching
        data.to_csv(filename)

        return data

    except Exception as e:
        raise RuntimeError(f"Error fetching historical data for {ticker}: {e}")

def clean_market_data(data: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess market data.

    Args:
        data (pd.DataFrame): Raw market data.

    Returns:
        pd.DataFrame: Cleaned market data.
    """
    try:
        # Handle missing values by dropping rows with NaNs
        data = data.dropna()
        return data

    except Exception as e:
        raise RuntimeError(f"Error cleaning market data: {e}")