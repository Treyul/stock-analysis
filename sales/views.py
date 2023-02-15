from django.shortcuts import render
from .forms import Wholesale
# Create your views here.
def baseSales(request):
    form = Wholesale()
    return render(request,"sales.html",{"form": form})