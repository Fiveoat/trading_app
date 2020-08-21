from database_handler import DatabaseHandler, PaperTrades, Tickers


class PaperTrader(DatabaseHandler):
    def __init__(self):
        super().__init__()

    def buy_stock(self, symbol, price, quantity):
        # TODO : CHECK IF ALREADY OWNED
        if symbol not in [x.symbol for x in self.session.query(Tickers).all()]:
            raise ValueError()
        trade = PaperTrades()
        trade.ticker = symbol
        trade.quantity = quantity
        trade.purchase_price = price
        trade.active = True
        self.session.add(trade)
        self.session.commit()

    def sell_stock(self, symbol, price, quantity):
        current_holding = [x for x in self.session.query(PaperTrades).filter_by(ticker=symbol).all()][0]
        if quantity == current_holding.quantity:
            current_holding.active = False
        net_price = price - current_holding.purchase_price
        net_total = net_price * quantity

    def get_current_holdings(self, ticker=None):
        pass


if __name__ == '__main__':
    paper_trader = PaperTrader
    paper_trader.buy_stock(symbol="MITT", price=4.20, quantity=69)
