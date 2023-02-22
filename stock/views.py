from django.shortcuts import render
from .forms import Update_Available, Order_Form

# Create your views here.
def update_available_stock(request):
    # get form data if post request is made
    if request.method == "POST":
        form = Update_Available(request.post)
        if form.is_valid():
            print(form.cleaned_data)
        pass

    #default rendering for get request
    return render(request,"index.html",{"form": Update_Available()})

def update_stock_ordered(request):

    # get form data if post request is made
    if request.method == "POST":
        pass

    # default rendering for get request
    return render(request,"index.html",{"form":Order_Form()})
