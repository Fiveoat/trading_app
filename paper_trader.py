import csv


class PaperTrader:
    def __init__(self, user):
        self.user = user

    def buy_stock(self, ticker, price, limit_order=None, stop_loss=None):
        # TODO: HOOK UP STOCK DATA TO BUY, WRITE TO INDIVIDUAL FILES
        pass

    def sell_stock(self, ticker, price, limit_order=None):
        # TODO: HOOK UP STOCK DATA TO SELL, WRITE TO INDIVIDUAL FILES
        pass

    def update_current_holdings(self):
        # TODO: MAKE CSV OUTLINE / WRITE DATA, READ EXISTING DATA
        writer = csv.writer(open(f"Files/{self.user}_trades.csv"))
        headers = ["Ticker", "Purchase Price", "Current Price", "Stop Loss", "Limit Order", "Percent Return",
                   "Active"]
        writer.writerow(headers)
        with csv.reader(open(f"Files/{self.user}_trades.csv")) as trades:
            pass
