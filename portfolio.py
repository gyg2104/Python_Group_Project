import pickle
import pandas
import pandas.io.data as web
import datetime

class Portfolio(dict):
    def __init__(self):
        port = {}
        counter = 0 #remove later

    #probably don't need a create new method

    def load_existing(self, port_file):
        port = pickle.load(port_file)
        
    
    def buy(self, ticker, amount):
        stock = web.DataReader(ticker, 'yahoo', datetime.date.today())
        
        print stock
        #holder

    def sell(self, ticker, amount):
        #holder

    def stock_viewer(self, ticker):
        #holder

    def view_port_stats(self):
        #holder

    def save_portfolio(self):
        #holder


def main():
    p = Portfolio()
    p.buy('AAPL', 1)

if __name__ == '__main__':
    main()

