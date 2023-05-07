class ProductsJson():

    name = ""
    sizes = []
    colours = []
    variation = {}
    Total = 0
    price = 0

    def __init__(self,name):
        self.name = name
        self.sizes = set([])
        self.colours = set([])
        self.variation = {}
        self.Total = 0
        self.price = 0

    def worth(self):
        return self.price * self.Total
    

class Product_Log_History():

    name = ""
    no_of_restocks = 0
    product_logs = []

    def __init__(self,name):

        self.name = name
        self.no_of_restocks = 0
        self.product_logs = []
        
