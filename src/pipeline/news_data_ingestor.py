import feedparser
from textblob import TextBlob
from datetime import datetime
from src.pipeline.db_manager import DBManager

class NewsDataIngestor:
    def __init__(self, db: DBManager):
        self.db = db

    def fetch_news(self, query):
        rss_url = f"https://news.google.com/rss/search?q={query}+stock+India"
        feed = feedparser.parse(rss_url)
        print(feed)
        return feed.entries

    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        score = analysis.sentiment.polarity
        label = "positive" if score > 0 else "negative" if score < 0 else "neutral"
        return score, label

    def save_to_db(self, symbol, entries):
        data = []
        for entry in entries:
            score, label = self.analyze_sentiment(entry.title)
            data.append((
                symbol,
                datetime(*entry.published_parsed[:6]),
                entry.title,
                entry.link,
                score,
                label
            ))
        self.db.insert_many(
            "news_sentiment",
            ["symbol", "news_date", "title", "source", "sentiment_score", "sentiment_label", "link", "summary", "created_at"],
            data
        )
