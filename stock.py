import pickle
import pandas as pd
import numpy as np
import pandas.io as web 
import datetime

class Stock(object):
    #Name, Quantity, Price, Date
    
    def __init__(self, name, quantity, price, date):
    	self.name = name
	self.quantity = quanitity
	self.price = price
	self.date = date

    def getVal(self):
    	val = quantity * price
	return val

    #Methods
    #Buy/Create Stock(Name, Quantity, Date)
    #getName(Name)
    #getQuant(Name)
    #getVal(Name)
    #
