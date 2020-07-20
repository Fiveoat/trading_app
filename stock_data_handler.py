import yfinance as yf
from datetime import datetime, timedelta


class StockDataHandler:
    # TODO: ADD METHODS THAT PULL DATA FROM THE DATAFRAME & CRUNCH NUMBERS
    def __init__(self, ticker):
        self.ticker = ticker

    def get_today_data(self):
        return yf.Ticker(self.ticker).history(period='1d').iloc[:99].max()

    def get_past_data(self, num_days):
        return yf.Ticker(self.ticker).history(period='1d', start=datetime.now().date() - timedelta(days=int(num_days)),
                                              end=datetime.now().date())


if __name__ == '__main__':
    stock_data = StockDataHandler('MITT')
    print(stock_data.get_today_data())
    print(stock_data.get_past_data(10))
