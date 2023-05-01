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