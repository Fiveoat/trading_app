from database_handler import DatabaseHandler, Articles, SourceArticleRelationships, TickerArticleRelationships
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


if __name__ == '__main__':
    article_handler = ArticleHandler()
    article_handler.insert_article("Apple Acquires Google", "marketwatch.com/id=adjfklanien", .999, datetime.utcnow())
