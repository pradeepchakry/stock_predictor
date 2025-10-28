import feedparser
import pandas as pd
from datetime import datetime
from src.db.db_connector import engine
from src.transformation.sentiment_analyzer import SentimentAnalyzer

class NewsScraper:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.feeds = [
            "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
            "https://www.moneycontrol.com/rss/MCtopnews.xml",
            "https://www.business-standard.com/rss/markets-106.rss"
        ]

    def fetch(self):
        analyzer = SentimentAnalyzer()
        news_records = []

        for feed_url in self.feeds:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.title
                summary = entry.get("summary", "")
                published = entry.get("published_parsed", None)
                published_date = datetime(*published[:6]) if published else datetime.now()
                sentiment = analyzer.get_sentiment(title + " " + summary)

                if self.symbol.lower() in title.lower() or self.symbol.lower() in summary.lower():
                    news_records.append({
                        "symbol": self.symbol,
                        "published_at": published_date,
                        "title": title,
                        "description": summary,
                        "sentiment": sentiment,
                        "source": feed_url,
                        "link": entry.link
                    })

        return pd.DataFrame(news_records)

    def save(self, df: pd.DataFrame):
        if not df.empty:
            df.to_sql("news_events", con=engine, if_exists="append", index=False)
            print(f"✅ Saved {len(df)} news records for {self.symbol}")
