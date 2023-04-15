from django.contrib.auth.decorators import login_required
from django.db.models import Count,Sum
from django.shortcuts import render
from utils.models import *
from datetime import date
import json


# Home page view
@login_required(login_url="/login")
def Home(request):

    # get products available
    products = AvailableStock.objects.all()
    # Products_Available_Objects = Products_Available.objects.filter()

    # get stock ordered pending arrival
    order_list = Products_Order_Logs.objects.filter(arrived = False).all()

    # print(Products_Available.objects.all())
    # print(Products_Available.objects.values("name","Colour","Size").annotate(total_amount=Sum('Amount')))
    print(Products_Available.objects.values("name","Colour").distinct())
    print(Products_Available.objects.values("name","Colour"))

    # change JSON string into OBJECT
            # Convert Available stock json literal strings into JSON objects
    for product in products:
        product.size_range = json.loads(product.size_range)
        
        product.colours = json.loads(product.colours)
        product.variation = json.loads(product.variation)

            # Convert Ordered stock json literal strings into JSON objects

    return render(request,"home.html",{"products" : products, "pending_order" : order_list})