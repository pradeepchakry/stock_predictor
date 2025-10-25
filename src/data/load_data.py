import yfinance as yf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_stock_data(ticker="AAPL", start="2020-01-01", end="2025-01-01"):
    print(f"📥 Downloading data for {ticker} from {start} to {end}...")
    data = yf.download(ticker, start=start, end=end)

    if data.empty:
        raise ValueError(f"No data returned for {ticker}. Check date range or symbol.")

    # Use only Close price for training
    close_data = data[['Close']].dropna()

    # Scale only the Close column
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_data)

    print(f"✅ Loaded {len(close_data)} rows for {ticker}")
    return scaled_data, scaler, close_data
