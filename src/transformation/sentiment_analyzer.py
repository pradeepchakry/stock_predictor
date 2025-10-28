from textblob import TextBlob

class SentimentAnalyzer:
    def get_sentiment(self, text: str):
        if not text:
            return 0.0
        try:
            polarity = TextBlob(text).sentiment.polarity
            return round(polarity, 3)
        except Exception:
            return 0.0
