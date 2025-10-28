from nsepython import nsefetch
import pandas as pd
from src.db.db_connector import engine

class StockDataFetcher:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def fetch(self):
        """Fetch historical data from NSE via nsepython."""
        url = f"https://www.nseindia.com/api/historical/cm/equity?symbol={self.symbol}"
        try:
            data = nsefetch(url)
            df = pd.DataFrame(data['data'])
            df = df.rename(columns={
                'CH_TIMESTAMP': 'date',
                'CH_OPENING_PRICE': 'open',
                'CH_TRADE_HIGH_PRICE': 'high',
                'CH_TRADE_LOW_PRICE': 'low',
                'CH_CLOSING_PRICE': 'close',
                'CH_TOTAL_TRADED_QUANTITY': 'volume'
            })
            df['symbol'] = self.symbol
            df['date'] = pd.to_datetime(df['date'])
            return df[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']]
        except Exception as e:
            print(f"❌ Error fetching data for {self.symbol}: {e}")
            return pd.DataFrame()

    def save(self, df: pd.DataFrame):
        if not df.empty:
            df.to_sql("stocks", con=engine, if_exists="append", index=False)
            print(f"✅ Saved {len(df)} rows for {self.symbol}")
