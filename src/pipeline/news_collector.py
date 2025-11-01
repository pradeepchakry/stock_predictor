from newsplease import NewsPlease
import pandas as pd
from tqdm import tqdm

class NewsCollector:
    def __init__(self, db_manager):
        self.db = db_manager

    def fetch_articles(self, urls):
        articles_data = []
        for url in tqdm(urls, desc="Crawling news sites"):
            try:
                article = NewsPlease.from_url(url)
                if article and article.title and article.text:
                    print(article.title)
                    articles_data.append({
                        "source": article.source_domain or "unknown",
                        "title": article.title,
                        "published_date": article.date_publish,
                        "url": article.url,
                        "content": article.text
                    })
            except Exception as e:
                print(f"⚠️ Failed to parse {url}: {e}")
        return pd.DataFrame(articles_data)

    def collect_and_store(self, urls):
        print("📰 Fetching financial news...")
        df = self.fetch_articles(urls)
        if not df.empty:
            self.db.insert_dataframe(df, "news_articles")
