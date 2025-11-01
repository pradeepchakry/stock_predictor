import time
import random
from nsepython import equity_history
from datetime import date, datetime
import pandas as pd
import requests
from tqdm import tqdm
import nsepython


class StockCollector:
    def __init__(self, symbol: str, max_retries: int = 3):
        self.symbol = symbol
        self.max_retries = max_retries
    
    def __init__(self, symbol: str, max_retries: int = 3):
        self.symbol = symbol
        self.max_retries = max_retries

    def _parse_date(self, d):
        """Ensure date is a datetime.date object."""
        if isinstance(d, date):
            return d
        if isinstance(d, str):
            # Try parsing formats like '2023-01-01' or '01-01-2023'
            for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
                try:
                    return datetime.strptime(d, fmt).date()
                except ValueError:
                    continue
        raise ValueError(f"Invalid date format: {d}")
    
    def fetch_stock_data(self, symbol, start_date, end_date):
        df = equity_history(
            symbol=symbol,
            series="EQ",
            start_date=start_date.strftime("%d-%m-%Y"),
            end_date=end_date.strftime("%d-%m-%Y")
        )

        # # Normalize column names for clarity and consistency
        # df = df.rename(columns={
        #     "mTIMESTAMP": "DATE",
        #     "CH_OPENING_PRICE": "OPEN_PRICE",
        #     "CH_TRADE_HIGH_PRICE": "HIGH_PRICE",
        #     "CH_TRADE_LOW_PRICE": "LOW_PRICE",
        #     "CH_CLOSING_PRICE": "CLOSE_PRICE",
        #     "CH_TOT_TRADED_QTY": "VOLUME"
        # })

        return df

    # def fetch_stock_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    #     """Fetch stock data with retry logic and safe date conversion."""
    #     start_date = self._parse_date(start_date)
    #     end_date = self._parse_date(end_date)

    #     retries = 0
    #     last_exception = None

    #     while retries < self.max_retries:
    #         try:
    #             print(f"Fetching stock data for {self.symbol}... Attempt {retries+1}/{self.max_retries}")
    #             print("symbol =", self.symbol, type(self.symbol))
    #             print("start_date =", start_date, type(start_date))
    #             print("end_date =", end_date, type(end_date))

    #             nsepython.headers = {
    #                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    #                 "Accept-Encoding": "gzip, deflate, br",
    #                 "Accept": "*/*",
    #                 "Connection": "keep-alive"
    #             }

    #             df = equity_history(
    #                 symbol=self.symbol,
    #                 series='EQ',
    #                 start_date=start_date.strftime("%d-%m-%Y"),
    #                 end_date=end_date.strftime("%d-%m-%Y")
    #             )

    #             if df is None or df.empty:
    #                 raise ValueError("Received empty DataFrame from NSE.")

    #             print(f"✅ Successfully fetched {len(df)} rows for {self.symbol}")
    #             return df

    #         except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
    #             print(f"⚠️ Network issue: {e}. Retrying in a few seconds...")
    #             last_exception = e
    #             retries += 1
    #             time.sleep(random.uniform(3, 8))

    #         except Exception as e:
    #             print(f"❌ Unexpected error fetching data: {e}")
    #             raise

    #     raise RuntimeError(f"Failed to fetch data for {self.symbol} after {self.max_retries} attempts") from last_exception
    
    def collect_and_store(self, symbols, start_date, end_date):
        for sym in tqdm(symbols):
            df = self.fetch_stock_data(sym, start_date, end_date)
            if not df.empty:
                self.db.insert_dataframe(df, "stock_history")
