from django.shortcuts import render
from .forms import Update_Available, Order_Form

# Create your views here.
def update_available_stock(request):
    return render(request,"index.html",{"form": Update_Available()})

def update_stock_ordered(request):
    return render(request,"index.html",{"form":Order_Form()})
