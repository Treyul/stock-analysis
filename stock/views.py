from django.shortcuts import render
import json
from .forms import Update_Available, Order_Form
from utils.models import AvailableStock,Stock,Ordered
from datetime import date

# Create your views here.
def update_available_stock(request):
    # get form data if post request is made
    if request.method == "POST":
        form = Update_Available(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data["name"]
            product_sizes =[]
            product_sizes_json = []
            product_data = form.cleaned_data["stock_data"]
            product_data_json = json.loads(product_data)
            product_colours = form.cleaned_data["colour"]
            product_colours_json = json.loads(form.cleaned_data["colour"])

            # create a list for the product sizes
            for size in product_data_json.keys():
                product_sizes.append(size)
                product_sizes_json.append(size)

            # change data type of the product sizes,colours to be compliant with the datatype of db column
            product_sizes = json.dumps(product_sizes)

            # count the total amount of shoes
            Total_amount = 0
            for colour in product_data_json.values():
                for amount in colour.values():
                    Total_amount = Total_amount + amount

            # add product to Logs
            stock = Stock(name = product_name, size_range = product_sizes, colours=product_colours,amount = Total_amount, variation = product_data)
            stock.save()

            
            # Query db if a similar product is also available
            Available_product =  AvailableStock.objects.filter(name=product_name).first()

            # if it does not exist
            if not Available_product:

                # convert variables into JSON strings
                

                # create db object and commit to db
                Available_product = AvailableStock(name=product_name,size_range=product_sizes,colours=product_colours,amount=Total_amount,variation= product_data,date=date.today())
                Available_product.save()

            # if there exists a similar product
            elif Available_product:

                # update variation
                previous_stock_data = json.loads(Available_product.variation)
                for size in previous_stock_data:
                    # test for presence of old sizes in  new sizes
                    
                    # if size is not present in new stock
                    if size not in product_data_json:

                        # add new size to the variation
                        product_data_json[size] = previous_stock_data[size]

                    elif size in product_data_json:

                        # get old and new color variation for the size
                        previous_colours = previous_stock_data[size]
                        new_colors = product_data_json[size]

                        # test if there are new colors in the size
                        for color in previous_colours:
                            
                            # insert color not present
                            if color not in new_colors:
                                new_colors[color] = previous_colours[color]

                            # update the number of shoes
                            elif color in new_colors:
                                new_colors[color] = previous_colours[color] + new_colors[color]

                # update total amount
                Total_amount = Total_amount + Available_product.amount

                # update size range
                previous_sizes = json.loads(Available_product.size_range)
                for size in product_sizes_json:
                    if size not in previous_sizes:
                        previous_sizes.append(size)
                
                #uodate colours
                previous_colour = json.loads(Available_product.colours)
                for colour in product_colours_json:
                    if colour not in previous_colour:
                        previous_colour.append(colour)

                # return variable into JSON strings to be store into db
                Available_product.size_range = json.dumps(previous_sizes)
                Available_product.colours = json.dumps(previous_colour)
                Available_product.amount = Total_amount
                Available_product.variation = json.dumps(product_data_json)

                Available_product.save()


    #default rendering for get request
    return render(request,"index.html",{"form": Update_Available()})

def update_stock_ordered(request):

    # get form data if post request is made
    if request.method == "POST":
        form = Update_Available(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data["name"]
            product_sizes =[]
            product_data = form.cleaned_data["stock_data"]
            product_data_json = json.loads(product_data)
            product_colours = json.loads(form.cleaned_data["colour"])
            pass
    # default rendering for get request
    return render(request,"index.html",{"form":Order_Form()})
