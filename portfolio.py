import pickle
import pandas as pd
import pandas.io.data as web
import datetime
from stock import Stock
import pylab

class WrongDayException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

class Portfolio(dict):
    
    def __init__(self):
        self.port = []

    def load_existing(self, port_file):
        try:
            self.port = pickle.load(open(port_file, "rb"))
            print("loaded portfolio!")
        except FileNotFoundError:
            print("That is not a valid portfolio name!")
        
    
    def buy(self, ticker, amount, time):
        opening, high, low, close, volume, adj_close = 0, 0, 0, 0, 0, 0
        stock_data = None
        #assume that you add the stock to this portfolio tracker 
        #the day after when the yahoo financial website is updated
        #and the closing time details have been uploaded
        #time = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
        try:
            #you bought a stock yesterday, get the info on it
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
            my_stock = Stock(ticker, amount, adj_close, time)
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
        time = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
        #datetime.date.today()
        if time.weekday() > 4:
            if time.weekday() == 5:
                time = datetime.date.fromordinal(datetime.date.today().toordinal()-2)
            else:
                time = time = datetime.date.fromordinal(datetime.date.today().toordinal()-3)

        
        count = 0
        total_port_value = 0
        total_port_perf = 0
        total_initial = 0
        if not self.port:
            print("You don't own any stocks!")
        for i in self.port:
            count = count + 1
            print("Stock ", count)
            print(i.name)
            print("Amt: ",i.quantity)
            print("Bought for: ", i.price, " each")
            print("On date: ", i.date)
            try:
                print("Initial investment: ", (i.price * i.quantity))
                total_initial = total_initial + (i.price * i.quantity)
                cur_val =  web.DataReader(i.name, 'yahoo', time).values[0][5]
                print("Current stock price: ", cur_val)
                total_port_value = total_port_value + (cur_val * i.quantity)
                perf_val = (cur_val - i.price) * i.quantity
                print("Current value of investment: $", (cur_val * i.quantity))
                print("Gain or Loss: $", perf_val)
                total_port_perf = total_port_perf + perf_val
            except:
    
                print("Market data for today unavailable, analysis cannot be done yet")
                pass     

         
        print("XXXXXXXXXXXXXXXXXXX")
        print("Total money initially invested: ", total_initial)
        print("Total current portfolio value: ", total_port_value)
        print("Total portfolio gain or loss: ", total_port_perf)
        try:
            perc_gain = (total_port_perf/(total_port_value - total_port_perf))*100
            print("Total portfolio % gain: ", perc_gain, "%")
        except ZeroDivisionError:
            print("% Gain results unavailable")

    def analyze(self):
        #pie chart composition of portfolio
        p_data = []
        for stock in self.port:
            p_data.append({"name": stock.name, "quantity": stock.quantity, "price": stock.price, \
                "date": stock.date, "value": stock.getVal()})

        p_data = pd.DataFrame(p_data)
        p_data_g = p_data.groupby("name").sum() #grouups stocks of same ticker purchased at dif time
        p_data_g["pct_value"] = p_data_g["value"]/sum(p_data_g["value"])
        f = p_data_g.plot(kind = "pie", y = "pct_value", autopct='%.2f')
        pylab.show(f)
        
        #time series and prediction analysis
        today = datetime.date.fromordinal(datetime.date.today().toordinal())
        #if today.weekday() > 4:
         #   today = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
        prices = {}
        for stock in self.port:
            start_date = stock.date
            print(start_date)
            print(today)
            p = web.DataReader(stock.name, "yahoo", start_date, today)
            p["quantity"] = stock.quantity
            prices[str(stock.name) + "_" + str(stock.date)] = p
        prices = pd.Panel(prices)
        pylab.show((prices.ix[:,:,"quantity"]*prices.ix[:,:,"Adj Close"]).sum(axis=1).plot())
        print(prices)


    def save_portfolio(self):
        #saves current port to a file
        pickle.dump(self.port, open("latest_portfolio.txt", "wb"))


def main():
    p = Portfolio()
    cont = "Y"
    print("Welcome!")
    while cont.upper() == "Y":
        print("Press 'L'- load, 'B' - buy, 'S'- sell, 'V'- view, 'X'- save, 'A' - analyze ")
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
                d = input("Enter the date purchased in format YYYY-MM-DD: ")
                date = datetime.datetime(*map(int, d.split("-")))
                if date == datetime.date.today():
                    date = time = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
                if date.weekday() > 4:
                    raise WrongDayException("Chose day over 4")
                p.buy(ticker.upper(), num, date)
                cont = input("Continue? press y/n: ")
            except TypeError:
                print("Wrong format")
            except ValueError:
                print("Not a valid number")
                cont = input("Continue? press y/n: ") 
            except WrongDayException:
                print("Stock market wasn't open on that day!")
                cont = input("Continue? press y/n: ")


        elif choice.upper() == 'S':
            ticker = input("Type the ticker of stock you would like to sell: ")
            num = 0
            try:
                num = int(input("Type amount of this stock you would like to sell: "))
                p.sell(ticker.upper(), num)
                cont = input("Continue? press y/n: ")
            except ValueError:
                print("Not a valid number")
                cont = input("Continue? press y/n: ") 


        elif choice.upper() == 'V':
            p.view_port_stats()
            cont = input("Continue? press y/n: ")

        elif choice.upper() == 'A':
            p.analyze()
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

