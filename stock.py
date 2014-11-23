import pickle
import pandas as pd
import numpy as np
import pandas.io as web 
import datetime

class Stock(object):
    #Name, Quantity, Price, Date
    
    def __init__(self, name, quantity, price, date):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.date = date
        self.val = quantity * price

    def getVal(self):
        #val = quantity * price
        return self.val
    
    def setName(self, name):
        self.name = name

    def setQuantity(self, quantity):
        self.quantity = quantity

    def setPrice(self, price):
        self.price = price

    def setDate(self, date):
        self.date = date
