import pickle
import pandas as pd
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
        #stock = pd.io.data.get_data_yahoo(ticker, start = datetime.date.today(), end = datetime.date.today())
        stock_data = web.DataReader(ticker, 'yahoo', datetime.date.today())
        print("Buying...")
        print(stock)
        vals = stock_data.values
        open, high, low = vals[0][0], vals[0][1], vals[0][2]
        close, volume, adj_close = vals[0][3], vals[0][4], vals[0][5]
        print(open, high, low, close, volume, adj_close)
        #i'm not sure which of this data we actually need, but whatever we need I will use 
        #right here to create a stock using Brandon's stock class
        #something like stock = create_stock(ticker, close)
        #then i will add this stock along with however many we bought to the dictionary port
        #keep in mind that port will map a stock ticker to an array of x amts of stocks
        #so that if we buy a stock that we already have stocks of, then we can append to array
        #so we will add "amount" amounts of this stock to the array that is mapped to the key ticker
        #i need to look at brandon's code to implement this but i just wanted to let you know
        #how it will work
        

    def sell(self, ticker, amount):
        #removes a stock from the dict (x amount of this stock)
        #once again, i need to actually implement the adding first
        #but anyway, what it will do is find the ticker matching the param
        #and then in the array of stocks stored it will remove x of them
        #and tell you how much you lost/gained by looking at the stock's purchase
        #value vs current value
        pass

    def stock_viewer(self, ticker):
        #prints today's info about a stock given a ticker symbol
        stock_info = web.DataReader(ticker, 'yahoo', datetime.date.today())
        print(stock_info)

    def view_port_stats(self):
        #I need to implement the adding of the stocks to the dictionary port first
        #so I need to look @ brandon's stuff first - but this will just print out the 
        #info about the stocks that we have for every key (which is a ticker) in the dictionary
        pass

    def save_portfolio(self):
        #saves current port to a file
        pickle.dump(port, "latest_portfolio.txt")


def main():
    p = Portfolio()
    p.buy('AAPL', 1)

if __name__ == '__main__':
    main()

