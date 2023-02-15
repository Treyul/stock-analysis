from django.shortcuts import render
from .forms import Wholesale,Retail_sales
# Create your views here.
def baseSales(request):
    form = Wholesale()
    return render(request,"record.html",{"form": form})

def RetailSales(request):

    form = Retail_sales()

    return render(request,"record.html",{"form":form})