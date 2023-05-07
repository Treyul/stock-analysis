from django.shortcuts import render
from utils.models import *
from utils.classes import *
from utils.views import *
from django.db import transaction
from django.db.models import Q,Sum,Count,F
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

"""
For stock analysis
No of restock = group product logs by product name count columns

1. [DONE] Count the number of appearances of a product in product logs and order label
2. Sum the amount ordered in product logs SP1
3. Order by batches
4. get depletion date and arrival date
5. difference in no.5 as Time for depletion

1. [DONE]group by batches 
2. [DONE] Sum the amount of product in each batch  SA1

1. product sold in each batch = SP1-SA1 if not depleted

"""

@login_required
def stock_analyis(request):
    
    pass


@login_required
@transaction.atomic
def Change_order_status_Arrived(request):

    if request.method == "POST":
        pass
    pass


@login_required
def home(request):

    unpriced_arrived_products = get_unpriced_products(request)

    priced_arrived_products = get_priced_products(request)

    pending_orders = Products_Order_Logs.objects.filter(arrived = False).all()

    # get number of restocks and variation in each restock
    Number_of_restocks = Products_Logs.objects.values("product_name").annotate(number = Count("product_name"))
    product_logs = Products_Logs.objects.all()

    Depleted_Products = Products_Logs.objects.filter(~Q(depletion_date = None))
    
    Amounts_Available = Products_Available.objects.values("name").annotate(amount = Sum("Amount"))
    print(Depleted_Products)
    return render(request ,"dashboard.html",{"priced_products":priced_arrived_products,"unpriced_products":unpriced_arrived_products, "pending_orders":pending_orders,"priced_worth":0,"order_worth":0})


@login_required
def sale_dataset(request):

    # query database for the last five days sales
    wholesale_sales = Wholesale_Sales_Logs.objects.filter(~Q(status=None)).values("date").annotate(sum=Sum("price")).order_by("-date")[:5]
    retail_sales = Retail_Sales_Log.objects.filter(~Q(status=None)).values("date").annotate(sum =Sum("price")).order_by("-date")[:5]

    wholesale_dataset = [[],[]]
    retail_dataset =[[],[]]

    for obj in wholesale_sales:
        
        wholesale_dataset[0].append(obj["date"])
        wholesale_dataset[1].append(obj["sum"])

    for obj in retail_sales:

        retail_dataset[0].append(obj["date"])
        retail_dataset[1].append(obj["sum"])

    # reverse arrays
    for array in wholesale_dataset:
        array.reverse()

    for array in retail_dataset:
        array.reverse()

    
    return JsonResponse({"wholesale":wholesale_dataset,"retail":retail_dataset})

@login_required
@transaction.atomic
def change_price(request):

    if request.method == "POST":
        Json_Message ={}

        data = json.load(request)

        available = Products_Available.objects.filter(name = data["product"]).all()

        #set the price
        for db_obj in available:
            db_obj.Price = data["price"]
            db_obj.save()


        Json_Message["message"] = "success"
        Json_Message["success"] = "Price successfully set"

    
        return JsonResponse(Json_Message)