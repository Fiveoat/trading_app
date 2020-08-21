from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Tickers(Base):
    __tablename__ = 'tickers'
    symbol = Column(String, primary_key=True)
    exchange = Column(String)


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


class DatabaseHandler:
    def __init__(self):
        self.engine = create_engine('sqlite:///Files/data.sqlite', echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def query(self, sql_statement):
        return [x for x in self.engine.execute(sql_statement)]

    def commit(self, sql_statement):
        try:
            self.engine.execute(sql_statement)
            self.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def insert_article(self, title, url, sentiment, published_datetime, source, tickers):
        article = Articles()
        article.title = title
        article.url = url
        article.sentiment = sentiment
        article.published_datetime = published_datetime
        sar = SourceArticleRelationships()
        sar.source_id = source  # GET PROPER SOURCE ID ( LOOKUP )
        sar.article_id = article.article_id  # NEEDS INSERTED & ARTICLE ID LOOKED UP
        for ticker in tickers:
            tar = TickerArticleRelationships()
            tar.article_id = article.article_id  # NEEDS INSERTED & ARTICLE ID LOOKED UP
            tar.symbol = ticker  # GET PROPER SYMBOL ( LOOKUP )
            self.session.add(tar)
        self.session.add(sar)
        self.session.add(article)
        self.session.commit()

    def _create_database(self):
        Base.metadata.create_all(bind=self.engine)

    def __exit__(self):
        self.session.close()


if __name__ == '__main__':
    database_handler = DatabaseHandler()
    database_handler.insert_article("MITT Skyrockets With Google Merger Talks", "marketwatch.com/yh34ubbali4", .89,
                                    datetime.now(), "MarketWatch", ["MITT", "GOOG"])
