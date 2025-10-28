from sqlalchemy import Column, Integer, String, Date, Numeric, BigInteger, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20))
    date = Column(Date)
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    close = Column(Numeric)
    volume = Column(BigInteger)

class NewsEvent(Base):
    __tablename__ = "news_events"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20))
    published_at = Column(TIMESTAMP)
    title = Column(Text)
    description = Column(Text)
    sentiment = Column(Numeric)
    source = Column(String(255))
    link = Column(String(500))
