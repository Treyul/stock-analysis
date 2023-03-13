from django.shortcuts import render
from utils.models import AvailableStock
from django.http import JsonResponse
from django.db.models import Q
import json

# Create your views here.
def settings(request):

    unpriced_stock = AvailableStock.objects.filter(price = None).all()
    priced_stock = AvailableStock.objects.filter(~Q(price = None)).all()

    # convert JSON string into JSON Objects
    for product in priced_stock:
        product.size_range = json.loads(product.size_range)
        
        product.colours = json.loads(product.colours)
        product.variation = json.loads(product.variation)
    for product in unpriced_stock:
        product.size_range = json.loads(product.size_range)
        
        product.colours = json.loads(product.colours)
        product.variation = json.loads(product.variation)

    return render(request,"settings.html",{"priced_stock":priced_stock,"unpriced_stock":unpriced_stock})

def setprice(request):

    if request.method == "POST":

        data =  json.load(request)
        
        available = AvailableStock.objects.filter(name = data["product"]).first()

        #set the price
        available.price = data["price"]

        available.save()

        response_message = {"message":"success"}

        return JsonResponse(response_message) 