from django.shortcuts import render
from utils.models import AvailableStock
from django.db.models import Q

# Create your views here.
def settings(request):

    unpriced_stock = AvailableStock.objects.filter(price = None)
    priced_stock = AvailableStock.objects.filter(~Q(price = None))

    print(unpriced_stock)
    print(priced_stock)

    return render(request,"settings.html")