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

    # query product logs for all products and get the no of restocks
    Number_of_restocks = Products_Logs.objects.values("product_name").annotate(number = Count("product_name"))
    # Amounts_Available = Products_Available.objects.values("name").annotate(amount = Sum("Amount"))

    product_analysis = []

    # populate the array
    for product in Number_of_restocks:
        product_log = Product_Log_History(product["product_name"].lower(),product["number"])
        product_analysis.append(product_log)

    product_logs = Products_Logs.objects.order_by("-Arrival_date").values()
    for product in product_logs:
        for product_log in product_analysis:
            if product["product_name"].lower() == product_log.name:
                product_log.product_logs.append(product)
                product_log.ordered = product_log.ordered + product["order_amount"]
                product_log.available = product_log.available + product["amount"]
                break   

    Wholesale_sales_data =Wholesale_Sales_Logs.objects.values("product","date").annotate(sales=Count("date")).order_by("date")
    # {'product': 'test76', 'date': datetime.date(2023, 4, 20), 'sales': 1}
    for sale in Wholesale_sales_data:
        for product in product_analysis:
            if product.name == sale.get("product").lower():
                product.sales_history[0].append(sale.get("date"))
                product.sales_history[1].append(sale.get("sales"))
                break

    Retail_sales_data =Retail_Sales_Log.objects.values("product","date").annotate(sales=Count("date")).order_by("date")
    for sale in Retail_sales_data:
        for product in product_analysis:
            if product.name == sale.get("product").lower():
                product.retail_sales_history[0].append(sale.get("date"))
                product.retail_sales_history[1].append(sale.get("sales"))
                break


    analysis_json = []
    for product in product_analysis:
        analysis_json.append(product.__dict__)
    
    return analysis_json


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

    Depleted_Products = Products_Logs.objects.filter(~Q(depletion_date = None))
    
    Amounts_Available = Products_Available.objects.values("name").annotate(amount = Sum("Amount"))
    # print(Depleted_Products)
    analysis_json = stock_analyis(request)
    return render(request ,"dashboard.html",{"priced_products":priced_arrived_products,"unpriced_products":unpriced_arrived_products, "pending_orders":pending_orders,"priced_worth":0,"order_worth":0,"analysis":analysis_json})


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

    # analysis = stock_analyis(request)
    analysis_json = stock_analyis(request)
    
    return JsonResponse({"wholesale":wholesale_dataset,"retail":retail_dataset,"analysis":analysis_json})

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