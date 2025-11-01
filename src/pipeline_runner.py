from src.pipeline.db_manager import DBManager
from src.pipeline.stock_collector import StockCollector
from src.pipeline.news_collector import NewsCollector
from src.pipeline.stock_data_ingestor import StockDataIngestor
from src.pipeline.news_data_ingestor import NewsDataIngestor
from datetime import date

if __name__ == "__main__":
    db = DBManager("postgresql+psycopg2://postgres:yourpassword@localhost:5432/stockdb")
    stockIngestor = StockDataIngestor(db)
    # db.init_tables()

    # --- Fetch stock data ---
    symbol = "RELIANCE"
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)

    print(f"Fetching stock data for {symbol}...")
    df = stockIngestor.fetch_stock_data(symbol, start_date, end_date)
    print(df.head())

    print(f"Saving {symbol} data to PostgreSQL...")
    StockDataIngestor.save_to_db(symbol, df)

    # --- Fetch news data ---
    urls = [
        "https://economictimes.indiatimes.com/",
        "https://www.moneycontrol.com/",
        "https://www.business-standard.com/"
    ]
    news_collector = NewsCollector(db)
    news_collector.collect_and_store(urls)
