from database_handler import DatabaseHandler, PaperTrades, Tickers, PaperTradeTickerRelationships
from stock_data_handler import StockDataHandler
from slacking import SlackHandler
from datetime import datetime
import pandas as pd


class PaperTrader(DatabaseHandler):
    """
    USERS >
        CURRENT HOLDINGS >
            ACTIVE TRADES >
                TICKERS >
                    PULL DAY TICKER DATA >
                        CALCULATE CURRENT ROI
                    COMBINE >
                    TRANSACTIONS >
                        ALL BOUGHT >
                        ALL SOLD >
                    SUM ALL ASSETS >
                        SECURITY HOLDINGS >
                        CASH HOLDINGS >
    """

    def __init__(self):
        super().__init__()
        self.slack = SlackHandler()

    def get_all_transactions_for_user(self, user_id):
        self.session.query(PaperTrades).filter_by(user_id=user_id)

    def calculate_current_returns(self, user_id):
        holdings = {}
        transactions = [x for x in self.session.query(PaperTrades).filter_by(user_id=user_id)]
        for transaction in transactions:
            if transaction.ticker not in holdings.keys():
                holdings[transaction.ticker] = transaction.purchase_price
            else:
                stock_data = StockDataHandler(transaction.ticker)
                last_price = stock_data.get_today_data().Close
                current_return = last_price / transaction.purchase_price
                print(current_return)
                holdings[transaction.ticker] = holdings[transaction.ticker] + transaction.purchase_price
        print(holdings)

    def buy_stock(self, symbol, price, quantity):
        if symbol not in [x.symbol for x in self.session.query(Tickers).all()]:
            raise ValueError()
        trade = PaperTrades()
        trade.ticker = symbol
        trade.quantity = quantity
        trade.purchase_price = price
        trade.active = True
        trade.trade_datetime = datetime.utcnow()
        trade.user_id = 1
        self.session.add(trade)
        self.session.commit()
        x = self.session.query(PaperTrades).filter_by(ticker=symbol, quantity=quantity, purchase_price=price).all()[0]
        ticker_trade = PaperTradeTickerRelationships()
        ticker_trade.trade_id = x.trade_id
        ticker_trade.ticker = symbol
        self.session.add(ticker_trade)
        self.session.commit()
        self.slack.send_message(self.slack.fiveoat, f"Your purchase of {quantity} shares of {symbol} at ${price} "
                                                    f"was successful.")

    def sell_stock(self, symbol, price, quantity):
        current_holding = [x for x in self.session.query(PaperTrades).filter_by(ticker=symbol).all()][0]
        if quantity == current_holding.quantity:
            current_holding.active = False
        net_price = price - current_holding.purchase_price
        net_total = net_price * quantity

    def get_current_holdings(self, user_id):
        print(len([x for x in self.session.query(PaperTrades).filter_by(user_id=user_id, active=True).all()]))


if __name__ == '__main__':
    paper_trader = PaperTrader()
    paper_trader.get_current_holdings(1)
    paper_trader.calculate_current_returns(1)
    # paper_trader.sell_stock("FB", 5.80, 60)
    # paper_trader.buy_stock("FB", 4.20, 69)
    # print(paper_trader.query(
    #     "SELECT p.purchase_price, t.symbol, p.trade_datetime, u.first, u.last, ar.title, ar.sentiment FROM users u "
    #     "INNER JOIN paper_trades p ON p.user_id = u.user_id "
    #     "INNER JOIN tickers t ON p.ticker = t.symbol "
    #     "INNER JOIN ticker_article_relationships a ON a.symbol = t.symbol "
    #     "INNER JOIN articles ar ON a.article_id = ar.article_id"))
