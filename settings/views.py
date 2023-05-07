from django.shortcuts import render
from utils.models import *
from django.http import JsonResponse
from django.db.models import Q,Sum
from utils.classes import *
import json

# Create your views here.
def settings(request):

    # unpriced_stock = Products_Available.objects.filter(price = None).all()
    # priced_stock = Products_Available.objects.filter(~Q(price = None)).all()
    priced_stock_objects = Products_Available.objects.filter(~Q(Price = None)).values("name","Colour","Size").annotate(total=Sum('Amount'))
    unpriced_stock_objects = Products_Available.objects.filter(Price = None).values("name","Colour","Size").annotate(total=Sum('Amount'))
    priced_stock = []
    unpriced_stock = []

    for product in priced_stock_objects:

        # Set the boolean value that the product is not present in the array
        present = False

        # iterate through the array to check existence of the object
        for present_product in priced_stock:
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
            priced_stock.append(product_json)
    
    
    for product in unpriced_stock_objects:

        # Set the boolean value that the product is not present in the array
        present = False

        # iterate through the array to check existence of the object
        for present_product in unpriced_stock:
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
            unpriced_stock.append(product_json)

    return render(request,"settings.html",{"priced_stock":priced_stock,"unpriced_stock":unpriced_stock})

def setprice(request):

    if request.method == "POST":

        data =  json.load(request)
        print(data)
        
        available = Products_Available.objects.filter(name = data["product"]).all()

        #set the price
        for db_obj in available:
            db_obj.Price = data["price"]
            db_obj.save()


        response_message = {"message":"success"}

        return JsonResponse(response_message) 