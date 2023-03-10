from django.shortcuts import render
from utils.models import AvailableStock,Ordered
from datetime import date
from django.contrib.auth.decorators import login_required
import json


# Home page view
@login_required(login_url="/login")
def Home(request):

    # get products available
    products = AvailableStock.objects.all()

    # get stock ordered pending arrival
    order_list = Ordered.objects.filter(arrived = False)


    # change JSON string into OBJECT
            # Convert Available stock json literal strings into JSON objects
    for product in products:
        product.size_range = json.loads(product.size_range)
        
        product.colours = json.loads(product.colours)
        product.variation = json.loads(product.variation)

            # Convert Ordered stock json literal strings into JSON objects
    for order in order_list:
        order.size_range = json.loads(order.size_range)
        order.colours = json.loads(order.colours)
        order.variation = json.loads(order.variation)    


    return render(request,"home.html",{"products" : products, "pending_order" : order_list})