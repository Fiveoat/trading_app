from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///Files/data.sqlite')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


class Tickers(Base):
    __tablename__ = 'tickers'
    symbol = Column(String, primary_key=True)
    company_name = Column(String)
    exchange = Column(String)
    sector = Column(String)
    industry = Column(String)
    market_cap = Column(String)


class Sources(Base):
    __tablename__ = 'sources'
    source_id = Column(Integer, primary_key=True)
    source_name = Column(String)


class Articles(Base):
    __tablename__ = 'articles'
    article_id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    sentiment = Column(Integer)
    published_datetime = Column(DateTime)
    created_datetime = datetime.utcnow()


class TickerArticleRelationships(Base):
    __tablename__ = 'ticker_article_relationships'
    symbol_article_id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.article_id'))
    symbol = Column(Integer, ForeignKey('tickers.symbol'))
    created_datetime = datetime.utcnow()


class SourceArticleRelationships(Base):
    __tablename__ = 'source_article_relationships'
    source_article_id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('sources.source_id'))
    article_id = Column(Integer, ForeignKey('articles.article_id'))
    created_datetime = datetime.utcnow()


class PaperTrades(Base):
    __tablename__ = 'paper_trades'
    trade_id = Column(Integer, primary_key=True)
    ticker = Column(String)
    purchase_price = Column(Integer)
    trade_datetime = Column(DateTime)
    quantity = Column(Integer)
    active = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.user_id"))


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    first = Column(String)
    last = Column(String)
    email = Column(String)


class PaperTradeTickerRelationships(Base):
    __tablename__ = 'paper_trade_ticker_relationships'
    trade_ticker_relationship_id = Column(Integer, primary_key=True)
    ticker = Column(String, ForeignKey('tickers.symbol'))
    trade_id = Column(Integer, ForeignKey('paper_trades.trade_id'))


class DatabaseHandler:
    def __init__(self):
        self.engine = create_engine('sqlite:///Files/data.sqlite')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def query(self, sql_statement):
        return [x for x in self.engine.execute(sql_statement)]

    def commit(self, sql_statement):
        try:
            self.engine.execute(sql_statement)
            self.session.commit()
            return True
        except Exception:
            return False

    def _create_database(self):
        Base.metadata.create_all(bind=self.engine)

    def wipe_tables(self):
        tables = ["articles", "paper_trade_ticker_relationships", "paper_trades", "source_article_relationships",
                  "ticker_article_relationships", "users"]
        [self.commit(f"DELETE FROM {table}") for table in tables]

    def __exit__(self):
        self.session.close()


if __name__ == '__main__':
    db_handler = DatabaseHandler()
    db_handler.wipe_tables()
