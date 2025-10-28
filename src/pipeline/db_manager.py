from sqlalchemy import create_engine, text

class DBManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self._init_tables()

    def _init_tables(self):
        """Create tables if they don't already exist."""
        with self.engine.connect() as conn:
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS stock_history (
                id SERIAL PRIMARY KEY,
                symbol VARCHAR(20) NOT NULL,
                date DATE NOT NULL,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume BIGINT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """))
            
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS news_sentiment (
                id SERIAL PRIMARY KEY,
                symbol VARCHAR(20),
                date DATE,
                headline TEXT,
                sentiment NUMERIC,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """))

            conn.commit()

    def insert_many(self, table_name, columns, values):
        """Insert multiple rows into a table."""
        if not values:
            return

        cols = ",".join(columns)
        placeholders = ",".join(["%s"] * len(columns))
        query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

        conn = self.engine.raw_connection()
        try:
            cur = conn.cursor()
            cur.executemany(query, values)
            conn.commit()
            cur.close()
        finally:
            conn.close()

