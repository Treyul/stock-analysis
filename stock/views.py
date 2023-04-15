from django.shortcuts import render
import json
from .forms import Update_Available, Order_Form
from utils.models import *
from datetime import date
from django.contrib import messages

# Create your views here.
def update_available_stock(request):
    # get form data if post request is made
    if request.method == "POST":
        form = Update_Available(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data.get("name")
            product_sizes_json = []
            product_data = form.cleaned_data.get("stock_data")
            product_data_json = json.loads(product_data)
            product_colours_json = json.loads(form.cleaned_data["colour"])

            # create a list for the product sizes
            for size in product_data_json.keys():
                product_sizes_json.append(size)

            # count the total amount of shoes
            Total_amount = 0
            for colour in product_data_json.values():
                for amount in colour.values():
                    Total_amount = Total_amount + amount

            # add product to Logs
            stock = Products_Logs(product_name=product_name, sizes = product_sizes_json, colours=product_colours_json,amount = Total_amount, product_variation = product_data_json )
            
            # iterate through the variation to create the products availabe objects
            stock.save()
            
            for size,variation in product_data_json.items():
                # initialize the object
                New_Product = Products_Available(name=product_name, Batch_no=stock,Size=size)
                
                # set the attributres for the colour and amount
                for colour,amount in variation.items():
                    print(colour,amount)
                    New_Product.Colour = colour
                    New_Product.Amount = amount

                # save the children object to the db
                New_Product.save()
                print("done")
            

            
            # Query db if a similar product is also available
            # Available_product =  AvailableStock.objects.filter(name=product_name).first()

            # # if it does not exist
            # if not Available_product:

            #     # convert variables into JSON strings
                

            #     # create db object and commit to db
            #     Available_product = AvailableStock(name=product_name,size_range=product_sizes,colours=product_colours,amount=Total_amount,variation= product_data,date=date.today())
            #     Available_product.save()

            #     messages.add_message(request, messages.INFO, "successfully added stock")

            # # if there exists a similar product
            # elif Available_product:

            #     # update variation
            #     previous_stock_data = json.loads(Available_product.variation)
            #     for size in previous_stock_data:
            #         # test for presence of old sizes in  new sizes
                    
            #         # if size is not present in new stock
            #         if size not in product_data_json:

            #             # add new size to the variation
            #             product_data_json[size] = previous_stock_data[size]

            #         elif size in product_data_json:

            #             # get old and new color variation for the size
            #             previous_colours = previous_stock_data[size]
            #             new_colors = product_data_json[size]

            #             # test if there are new colors in the size
            #             for color in previous_colours:
                            
            #                 # insert color not present
            #                 if color not in new_colors:
            #                     new_colors[color] = previous_colours[color]

            #                 # update the number of shoes
            #                 elif color in new_colors:
            #                     new_colors[color] = previous_colours[color] + new_colors[color]

            #     # update total amount
            #     Total_amount = Total_amount + Available_product.amount

            #     # update size range
            #     previous_sizes = json.loads(Available_product.size_range)
            #     for size in product_sizes_json:
            #         if size not in previous_sizes:
            #             previous_sizes.append(size)
                
            #     #uodate colours
            #     previous_colour = json.loads(Available_product.colours)
            #     for colour in product_colours_json:
            #         if colour not in previous_colour:
            #             previous_colour.append(colour)

            #     # return variable into JSON strings to be store into db
            #     Available_product.size_range = json.dumps(previous_sizes)
            #     Available_product.colours = json.dumps(previous_colour)
            #     Available_product.amount = Total_amount
            #     Available_product.variation = json.dumps(product_data_json)

            #     # Available_product.save()


    #default rendering for get request
    return render(request,"index.html",{"form": Update_Available()})

def update_stock_ordered(request):

    # get form data if post request is made
    if request.method == "POST":
        form = Order_Form(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            product_name = form.cleaned_data["name"]
            product_sizes_json = []
            product_data = form.cleaned_data["stock_data"]
            product_data_json = json.loads(product_data)
            Product_order_price = form.cleaned_data.get("price")
            product_colours_json = json.loads(form.cleaned_data["colour"])

            # create a list for the product sizes
            for size in product_data_json.keys():
                product_sizes_json.append(size)

            # count the total amount of shoes
            Total_amount = 0
            for colour in product_data_json.values():
                for amount in colour.values():
                    Total_amount = Total_amount + amount

            # add order
            # comments,shipping co, arrival date
            # Fill the columns that can be null in db if they are pro
            new_order = Products_Order_Logs(name=product_name,size_range=product_sizes_json,colours=product_colours_json,variation=product_data_json,amount=Total_amount,arrived=False)
            if form.cleaned_data.get("Shipper"):
                new_order.shipping_co = form.cleaned_data.get("Shipper")
            if form.cleaned_data.get("arrival"):
                new_order.proposed_arrival = form.cleaned_data.get("arrival")
            if Product_order_price:
                new_order.order_price = Product_order_price

            new_order.save()
                
    # default rendering for get request
    return render(request,"index.html",{"form":Order_Form()})
