# from src.pipeline.db_manager import DBManager
# from src.pipeline.stock_data_ingestor import StockDataIngestor
# from src.pipeline.news_data_ingestor import NewsDataIngestor
# from datetime import date

# def main():
#     db = DBManager()

#     stock_ingestor = StockDataIngestor(db)
#     news_ingestor = NewsDataIngestor(db)

#     symbol = "RELIANCE"
#     start_date = date(2023, 1, 1)
#     end_date = date(2023, 12, 31)

#     print(f"Fetching stock data for {symbol}...")
#     df = stock_ingestor.fetch_stock_data(symbol, start_date, end_date)
#     stock_ingestor.save_to_db(symbol, df)

#     print(f"Fetching news data for {symbol}...")
#     news_entries = news_ingestor.fetch_news(symbol)
#     news_ingestor.save_to_db(symbol, news_entries)

#     db.close()

# if __name__ == "__main__":
#     main()

from datetime import date
from src.pipeline.db_manager import DBManager
from src.pipeline.stock_data_ingestor import StockDataIngestor
from src.pipeline.news_data_ingestor import NewsDataIngestor

def main():
    db = DBManager("postgresql+psycopg2://postgres:yourpassword@localhost:5432/stockdb")
    ingestor = StockDataIngestor(db)
    news_ingestor = NewsDataIngestor(db)


    symbol = "RELIANCE"
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)

    # print(f"Fetching stock data for {symbol}...")
    # df = ingestor.fetch_stock_data(symbol, start_date, end_date)
    # print(df.head())

    # print(f"Saving {symbol} data to PostgreSQL...")
    # ingestor.save_to_db(symbol, df)

    print(f"Fetching news data for {symbol}...")
    news_entries = news_ingestor.fetch_news(symbol)

    print(f"Saving {symbol} data to PostgreSQL...")
    news_ingestor.save_to_db(symbol, news_entries)


if __name__ == "__main__":
    main()
