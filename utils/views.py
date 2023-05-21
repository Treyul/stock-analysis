from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import transaction
from django.db.models import Q,Sum,Count
from .classes import *
from .models import *


# @login_required
# @transaction.atomic
def get_unpriced_products(request):

    # if request.method =="POST":

        unpriced_stock_objects = Products_Available.objects.filter(Price = None).values("name","Colour","Size").annotate(total=Sum('Amount'))

        unpriced_stock = []

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
                if present_product.variation.get(product_size):
                     present_product.variation[product_size][product_colour] = product_amount
                else:
                    present_product.variation[product_size] = {product_colour:product_amount}
                present_product.colours.add(product_colour)
                present_product.sizes.add(product_size)

            elif not present:
                product_json = ProductsJson(name=product.get("name"),paid=False)

                product_colour = product.get("Colour")
                product_size = product.get("Size")
                product_amount = product.get("total")

                product_json.Total = product_json.Total + product_amount
                product_json.variation[product_size] = {product_colour:product_amount}
                product_json.colours.add(product_colour)
                product_json.sizes.add(product_size)

                # add the obj to the array
                unpriced_stock.append(product_json)


        return unpriced_stock
    

#  
def get_priced_products(request):

    # if request.method =="POST":

        # get the priced product that have arrived
        priced_stock_objects = Products_Available.objects.filter(~Q(Price = None)).values("name","Colour","Size","Price").annotate(total=Sum('Amount'))

        # initialize array to hold the db objects
        priced_stock = []

        # iterate through the db object to ensure uniqueness in the final array
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
                product_json = ProductsJson(name=product.get("name"),paid=True)

                product_colour = product.get("Colour")
                product_size = product.get("Size")
                product_amount = product.get("total")
                product_json.price = product.get("Price")

                
                product_json.Total = product_json.Total + product_amount
                product_json.variation[product_size] = {product_colour:product_amount}
                product_json.colours.add(product_colour)
                product_json.sizes.add(product_size)

                # add the obj to the array
                priced_stock.append(product_json)
    
        # print(priced_stock)
        return priced_stock
    