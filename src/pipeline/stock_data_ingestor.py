from nsepython import equity_history
from datetime import date
from src.pipeline.db_manager import DBManager

class StockDataIngestor:
    def __init__(self, db: DBManager):
        self.db = db

    def fetch_stock_data(self, symbol, start_date, end_date):
        df = equity_history(
            symbol=symbol,
            series="EQ",
            start_date=start_date.strftime("%d-%m-%Y"),
            end_date=end_date.strftime("%d-%m-%Y")
        )

        # Normalize column names for clarity and consistency
        df = df.rename(columns={
            "mTIMESTAMP": "DATE",
            "CH_OPENING_PRICE": "OPEN_PRICE",
            "CH_TRADE_HIGH_PRICE": "HIGH_PRICE",
            "CH_TRADE_LOW_PRICE": "LOW_PRICE",
            "CH_CLOSING_PRICE": "CLOSE_PRICE",
            "CH_TOT_TRADED_QTY": "VOLUME"
        })

        return df

    def save_to_db(self, symbol, df):
        # Some rows may have missing data, drop them
        df = df.dropna(subset=["DATE", "OPEN_PRICE", "HIGH_PRICE", "LOW_PRICE", "CLOSE_PRICE", "VOLUME"])

        data = [
            (
                symbol,
                row["DATE"],
                float(row["OPEN_PRICE"]),
                float(row["HIGH_PRICE"]),
                float(row["LOW_PRICE"]),
                float(row["CLOSE_PRICE"]),
                int(row["VOLUME"])
            )
            for _, row in df.iterrows()
        ]

        self.db.insert_many(
            "stock_history",
            ["symbol", "date", "open", "high", "low", "close", "volume"],
            data
        )
