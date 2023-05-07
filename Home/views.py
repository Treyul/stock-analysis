from django.contrib.auth.decorators import login_required
from django.db.models import Count,Sum
from django.shortcuts import render
from utils.models import *
from utils.classes import *
from utils.views import *
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
    Products_in_stock_json= get_priced_products(request)

    return render(request,"home.html",{"products" : Products_in_stock_json, "pending_order" : order_list})