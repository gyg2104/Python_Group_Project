import pickle
import pandas as pd
import pandas.io.data as web
import datetime
from stock import Stock

class Portfolio(dict):
    
    def __init__(self):
        self.port = []

    def load_existing(self, port_file):
        try:
            self.port = pickle.load(open(port_file, "rb"))
            print("loaded portfolio!")
        except FileNotFoundError:
            print("That is not a valid portfolio name!")
        
    
    def buy(self, ticker, amount):
        opening, high, low, close, volume, adj_close = 0, 0, 0, 0, 0, 0
        stock_data = None
        time = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
        try:
            #if the stock market wasn't open today, or it is still open
            #can't get the data for it today, so error occurs
            stock_data = web.DataReader(ticker, 'yahoo', time)#datetime.date.today())
            print("Trying to buy...")
            vals = stock_data.values
            opening, high, low = vals[0][0], vals[0][1], vals[0][2]
            close, volume, adj_close = vals[0][3], vals[0][4], vals[0][5]
            
        except (OSError, IndexError):
            #either no data for the market today uploaded/ market not open
            #or the stock ticker doesn't exist
            print("Sorry, data for this stock on this day are unavailable!")
            print("Either you chose a nonexistent stock ticker, or the market results not in system!")
            return

        else:
            print("Buying succesful, here are the stats for ", ticker) 
            print(stock_data)
            #print(opening, high, low, close, volume, adj_close)
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
                    new_q = quant - sell_amt
                    i.setQuantity(new_q)
                    print("Sold ", sell_amt , " stocks")
                    sell_amt = 0
                else:
                    print("Sold ", quant , " stocks")
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
        pickle.dump(self.port, open("latest_portfolio.txt", "wb"))


def main():
    p = Portfolio()
    cont = "Y"
    print("Welcome!")
    while cont.upper() == "Y":
        print("Press 'L' to load port, 'B' to buy, 'S' to sell, 'V' to view, 'X' to save")
        choice = input("Your choice: ")
    
        if choice.upper() == 'L':
            file_name = input("Type the filename of the portfolio to load: ")
            p.load_existing(file_name)
            cont = input("Continue? press y/n: ")
        elif choice.upper() == 'B':
            ticker = input("Type the ticker of stock you would like to buy: ")
            num = 0
            try:
                num = int(input("Type amount of this stock you would like to buy: "))
                p.buy(ticker.upper(), num)
                cont = input("Continue? press y/n: ")
            except ValueError:
                print("Not a valid number")
                cont = input("COntinue? press y/n: ") 


        elif choice.upper() == 'S':
            ticker = input("Type the ticker of stock you would like to sell: ")
            num = 0
            try:
                num = int(input("Type amount of this stock you would like to sell: "))
                p.sell(ticker, num)
                cont = input("Continue? press y/n: ")
            except ValueError:
                print("Not a valid number")
                cont = input("COntinue? press y/n: ") 


        elif choice.upper() == 'V':
            p.view_port_stats()
            cont = input("Continue? press y/n: ")

        elif choice.upper() == 'X':
            p.save_portfolio()
            cont = input("Continue? press y/n: ")

        else:
            print("Not a valid choice")
            cont = input("Continue? press y/n: ")

            
    #p.load_existing("latest_portfolio.txt")
    #p.buy('AAPL', 7)
    #p.buy('AAPL', 25)
    #p.sell('AAPL', 21)
    #p.view_port_stats()
    #p.save_portfolio()

if __name__ == '__main__':
    main()

