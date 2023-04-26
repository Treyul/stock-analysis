from django.contrib.auth.decorators import login_required
from django.db.models import Count,Sum
from django.shortcuts import render
from utils.models import *
from utils.classes import *
from datetime import date
import json

# Home page view
@login_required(login_url="/login")
def Home(request):

    # get stock ordered pending arrival
    order_list = Products_Order_Logs.objects.filter(arrived = False).all()

    # get product in stock
    Products_in_stock = Products_Available.objects.values("name","Colour","Size").annotate(total=Sum('Amount'))

    # initilize the array to held the product which are in stock
    Products_in_stock_json=[]

    # iterate the db objects
    for product in Products_in_stock:

        # Set the boolean value that the product is not present in the array
        present = False

        # iterate through the array to check existence of the object
        for present_product in Products_in_stock_json:
            if present_product.name == product.get("name"):

                # break from the loop if the condition is met
                present = True
                break

        if present:
            product_colour = product.get("Colour")
            product_size = product.get("Size")
            product_amount = product.get("total")

            present_product.Total = present_product.Total + product_amount
            present_product.variation[product_size] = {product_colour:product_amount}
            present_product.colours.add(product_colour)
            present_product.sizes.add(product_size)

        elif not present:
            product_json = ProductsJson(name=product.get("name"))

            product_colour = product.get("Colour")
            product_size = product.get("Size")
            product_amount = product.get("total")

            product_json.Total = product_json.Total + product_amount
            product_json.variation[product_size] = {product_colour:product_amount}
            product_json.colours.add(product_colour)
            product_json.sizes.add(product_size)

            # add the obj to the array
            Products_in_stock_json.append(product_json)

    return render(request,"home.html",{"products" : Products_in_stock_json, "pending_order" : order_list})