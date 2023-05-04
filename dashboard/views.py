from django.shortcuts import render
from utils.models import *
from utils.classes import *
from utils.views import *
from django.db import transaction
from django.db.models import Q,Sum,Count
from django.contrib.auth.decorators import login_required


# def update_variable(value):
#     data = value
#     return data

# register.filter('update_variable', update_variable)

# Create your views here.
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

    # priced_arrived_products:
    return render(request ,"dashboard.html",{"priced_products":priced_arrived_products,"unpriced_products":unpriced_arrived_products, "pending_orders":pending_orders,"priced_worth":0,"order_worth":0})