from src.ingestion.stock_data_fetcher import StockDataFetcher
from src.ingestion.news_scraper import NewsScraper

class IngestionPipeline:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def run(self):
        print(f"🚀 Running pipeline for {self.symbol}")

        # Step 1: Stock Data
        stock_df = StockDataFetcher(self.symbol).fetch()
        StockDataFetcher(self.symbol).save(stock_df)

        # Step 2: News/Sentiment
        news_df = NewsScraper(self.symbol).fetch()
        NewsScraper(self.symbol).save(news_df)

        print(f"🏁 Completed ingestion for {self.symbol}")
