import json
from json import JSONEncoder
import datetime

class ProductsJson():

    name = ""
    sizes = []
    colours = []
    variation = {}
    Total = 0
    price = 0
    # paid = False

    def __init__(self,name,paid):
        self.name = name
        self.sizes = set([])
        self.colours = set([])
        self.variation = {}
        self.Total = 0
        self.price = 0
        self.paid = paid

    def worth(self):
        return self.price * self.Total
    

class Product_Log_History():

    name = ""
    no_of_restocks = 0
    product_logs = []

    def __init__(self,name,restocks):

        self.name = name
        self.no_of_restocks = restocks
        self.product_logs = []
        self.available = 0
        self.ordered = 0
        self.price = 0
        self.sales_history = [[],[]]
        self.retail_sales_history =[[],[]]
        self.performance = [[],[]]
        

