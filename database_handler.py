from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()


class StockData(Base):
    __tablename__ = 'stock_data'
    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    open = Column(Integer)
    close = Column(Integer)
    date = Column(DateTime)
    material_id = Column(Boolean)
    material_source = Column(String)
    material_sentiment = Column(Integer)

    def __repr__(self):
        return self.ticker, str(self.date), str(self.open)


class MaterialData(Base):
    __tablename__ = 'material_data'
    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    date = Column(DateTime)
    material_source = Column(String)
    material_sentiment = Column(Integer)
    keyword_matches = Column(Integer)

    def __repr__(self):
        return self.ticker, str(self.date), str(self.material_source), str(self.material_sentiment)


class DatabaseHandler:
    def __init__(self):
        self.connection = ""
        self.database = ""

    def query_sql(self):
        pass

    def commit_sql(self):
        pass

    def __exit__(self):
        self.connection.close()
