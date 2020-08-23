from database_handler import DatabaseHandler, Articles, SourceArticleRelationships, TickerArticleRelationships, Sources
from datetime import datetime


class ArticleHandler(DatabaseHandler):
    def __init__(self):
        super().__init__()

    def insert_article(self, title, url, sentiment, published_datetime, source, tickers):
        article = Articles()
        article.title = title
        article.url = url
        article.sentiment = sentiment
        article.published_datetime = published_datetime
        self.session.add(article)
        self.session.commit()
        article_id = [x.article_id for x in self.session.query(Articles).filter_by(url=url).all()][0]
        sar = SourceArticleRelationships()
        source_id = self.session.query(Sources).filter_by(source_name=source).all()[0].source_id
        sar.source_id = source_id
        sar.article_id = article_id
        for ticker in tickers:
            tar = TickerArticleRelationships()
            tar.article_id = article_id
            tar.symbol = ticker
            self.session.add(tar)
        self.session.add(sar)
        self.session.commit()


if __name__ == '__main__':
    article_handler = ArticleHandler()
    article_handler.insert_article("Facebook Bankrupt", "marketwatch.com/id=adgaf4n", -.999, datetime.utcnow(),
                                   "MarketWatch", ["FB", "GOOG", "NFLX"])
