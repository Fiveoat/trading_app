from bs4 import BeautifulSoup
from sentiment_evaluator import SentimentEvaluator
import datetime
import requests
import re


class DataScraper:
    # TODO: MANY THINGS
    def __init__(self):
        self.sentiment_evaluator = SentimentEvaluator()
        self.keywords = ["coronavirus", "corona", "virus", "stimulus", "buy"]

    @staticmethod
    def ticker_regex(text):
        three = [x.strip() for x in re.findall(r'\b[A-Z]{3}\b', text)]
        four = [x.strip() for x in re.findall(r'\b[A-Z]{4}\b', text)]
        five = [x.strip() for x in re.findall(r'\b[A-Z]{5}\b', text)]
        return list(set(three + four + five))

    def get_market_watch_article_data(self, article_url):
        data = {}
        keyword_occurrences = []
        soup = BeautifulSoup(requests.get(article_url).text, features="html.parser")
        # published_datetime = str(datetime.datetime.strptime(
        #     soup.find(class_="timestamp timestamp--pub").text.split("Published: ")[1].split(" ET")[0].replace("a.m.",
        #                                                                                                       "AM").replace(
        #         "p.m.", "PM"), "%B %d, %Y at %I:%M %p"))
        # article_headline = article_url.split("story/")[1].split("-2020")[0].replace("-", " ")
        # try:
        #     headline_sentiment = self.sentiment_evaluator.score_sentiment(article_headline)
        # except Exception:
        #     headline_sentiment = None
        try:
            tickers = [[x.text for x in x.find_all(class_="symbol")] for x in soup.find_all(class_="list--tickers")][0]
        except IndexError:
            tickers = None
        try:
            article_text = "".join([x.text.replace("\n", "") for x in soup.find(id="js-article__body").find_all("p")])
        except AttributeError:
            article_text = ""
        try:
            article_sentiment = self.sentiment_evaluator.score_sentiment(article_text)
        except ZeroDivisionError:
            article_sentiment = None
        for keyword in self.keywords:
            if keyword in article_text:
                keyword_occurrences.append(keyword)
        # data["headline_sentiment"] = headline_sentiment
        data["keyword_occurrences"] = keyword_occurrences
        # data["published_datetime"] = published_datetime
        data["tickers"] = tickers
        data["article_sentiment"] = article_sentiment
        return data

    def get_benzinga_article_data(self, article_url):
        data = {}
        keyword_occurrences = []
        soup = BeautifulSoup(requests.get(article_url).text, features="html.parser")
        article_headline = soup.find(id="title").text
        published_datetime = ""
        try:
            article_text = "".join([x.text for x in soup.find("body").find_all("p")])
            tickers = self.ticker_regex(article_text)
        except AttributeError:
            article_text = ""
            tickers = []
        try:
            article_sentiment = self.sentiment_evaluator.score_sentiment(article_text)
        except ZeroDivisionError:
            article_sentiment = None
        try:
            headline_sentiment = self.sentiment_evaluator.score_sentiment(article_headline)
        except Exception:
            headline_sentiment = None
        for keyword in self.keywords:
            if keyword in article_text:
                keyword_occurrences.append(keyword)
        data["headline_sentiment"] = headline_sentiment
        data["keyword_occurrences"] = keyword_occurrences
        data["published_datetime"] = published_datetime
        data["tickers"] = tickers
        data["sentiment"] = article_sentiment
        return data


if __name__ == '__main__':
    scraper = DataScraper()
    print(scraper.get_market_watch_article_data("https://www.marketwatch.com/articles/carnival-plans-to-set-sail-in-europe-early-next-month-51598099401?mod=home-page"))
    # print(scrapper.get_benzinga_article_data("https://www.benzinga.com/news/20/07/16772222/union-pacific-eyes-highway-to-rail-conversion-opportunities"))
