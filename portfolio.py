import pickle
import pandas as pd
import pandas.io.data as web
import datetime
from stock import Stock

class Portfolio(dict):
    
    def __init__(self):
        self.port = []

    def load_existing(self, port_file):
        self.port = pickle.load(port_file)
        
    
    def buy(self, ticker, amount):
        time = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
        stock_data = web.DataReader(ticker, 'yahoo', time)#datetime.date.today())
        print("Buying...")
        print(stock_data)
        vals = stock_data.values
        opening, high, low = vals[0][0], vals[0][1], vals[0][2]
        close, volume, adj_close = vals[0][3], vals[0][4], vals[0][5]
        print(opening, high, low, close, volume, adj_close)
        my_stock = Stock(ticker, amount, close, datetime.date.today())
        self.port.append(my_stock)
        

    def sell(self, ticker, amount):
        ticker_stocks = []
        sell_amt = amount
        sold_all = False
        for i in self.port:
            name = i.name
            if name == ticker:
                quant = i.quantity
                if quant > sell_amt:
                    price = i.price
                    new_q = quant - sell_amt
                    i.setQuantity(new_q)
                    print("Sold ", sell_amt , " stocks, made a total of: ", price*sell_amt)
                    sell_amt = 0
                else:
                    price = i.price
                    print("Sold ", quant , " stocks, made a total of: ", price*quant)
                    sell_amt = sell_amt - quant
                    i.setQuantity(0)
            if sell_amt == 0:
                sold_all = True
                break
           
        if sold_all == True:
            print("Transaction complete")
        else:
            print("You tried to sell more stock than you owned, sold as much as possible")
        temp_p = [i for i in self.port if not i.quantity == 0]
        self.port = temp_p

                

    def stock_viewer(self, ticker):
        #prints today's info about a stock given a ticker symbol
        stock_info = web.DataReader(ticker, 'yahoo', datetime.date.today())
        print(stock_info)

    def view_port_stats(self):
        count = 0
        if not self.port:
            print("You don't own any stocks!")
        for i in self.port:
            count = count + 1
            print("Stock ", count)
            print(i.name)
            print("Amt: ",i.quantity)
            print("Bought for: ", i.price, " each")
            print("On date: ", i.date)



    def save_portfolio(self):
        #saves current port to a file
        pickle.dump(self.port, "latest_portfolio.txt")


def main():
    p = Portfolio()
    p.buy('AAPL', 7)
    p.buy('AAPL', 25)
    p.sell('AAPL', 21)
    p.view_port_stats()

if __name__ == '__main__':
    main()

