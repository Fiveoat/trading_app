import csv
from stock_data_handler import StockDataHandler


class PaperTrader:
    def __init__(self, user):
        self.user = user

    def read_current_csv(self):
        with open(f"Files/{self.user}_trades.csv", "r") as trades:
            for row in csv.DictReader(trades):
                print(row)

    def buy_stock(self, ticker, price, limit_order=None, stop_loss=None):
        # TODO: HOOK UP STOCK DATA TO BUY, WRITE TO INDIVIDUAL FILES
        headers = ["Ticker", "Purchase Price", "Current Price", "Stop Loss", "Limit Order", "Percent Return", "Active"]
        with open(f"Files/{self.user}_trades.csv", "w+") as trades:
            writer = csv.DictWriter(trades, fieldnames=headers)
            stock_data_handler = StockDataHandler(ticker)
            current_price = stock_data_handler.get_today_data()['Close']
            writer.writerow(
                {'Ticker': ticker, 'Purchase Price': price, 'Current Price': current_price, 'Stop Loss': stop_loss,
                 'Limit Order': limit_order, 'Percent Return': "", 'Active': True})

    def sell_stock(self, ticker, price, limit_order=None):
        # TODO: HOOK UP STOCK DATA TO SELL, WRITE TO INDIVIDUAL FILES
        headers = ["Ticker", "Purchase Price", "Current Price", "Stop Loss", "Limit Order", "Percent Return",
                   "Active"]
        with open(f"Files/{self.user}_trades.csv", "w+") as trades:
            writer = csv.DictWriter(trades, headers)
            writer.writerow([ticker, price, "", "", limit_order, "", ""])

    def update_current_holdings(self):
        # TODO: MAKE CSV OUTLINE / WRITE DATA, READ EXISTING DATA
        headers = ["Ticker", "Purchase Price", "Current Price", "Stop Loss", "Limit Order", "Percent Return",
                   "Active"]
        with open(f"Files/{self.user}_trades.csv", "w+") as trades:
            writer = csv.writer(trades)
            writer.writerow(headers)


if __name__ == '__main__':
    paper_trader = PaperTrader("fiveoat")
    paper_trader.buy_stock("MITT", 3.50, 3.5, .1)
    paper_trader.read_current_csv()
    paper_trader.buy_stock("BA", 241.88, 241, .05)
    paper_trader.read_current_csv()
