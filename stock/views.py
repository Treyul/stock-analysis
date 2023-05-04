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
                
                # set the attributres for the colour and amount
                for colour,amount in variation.items():
                    New_Product = Products_Available(name=product_name, Batch_no=stock,Size=size)
                    print(colour,amount)
                    New_Product.Colour = colour
                    New_Product.Amount = amount
                    New_Product.save() 
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
