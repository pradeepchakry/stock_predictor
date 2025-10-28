CREATE TABLE IF NOT EXISTS stock_history (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    date DATE,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT
);

CREATE TABLE IF NOT EXISTS news_sentiment (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    news_date TIMESTAMP,
    title TEXT,
    source TEXT,
    sentiment_score NUMERIC,
    sentiment_label VARCHAR(10)
);
