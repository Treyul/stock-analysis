from django.shortcuts import render
from utils.models import LocalSales,RetailSales
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Count,Sum
from django.contrib.auth.decorators import login_required
import json

# define functions to be used oin the analysis
def get_debts_and_credits_summation(request):

    # get local sales sold on credit
    local_owed = LocalSales.objects.filter(status=False,paid= False).values("shop_no").order_by("shop_no").annotate(sum= Sum("price"),count=Count("price")) 
    
    # get unpaid retail summation
    retail_owe = RetailSales.objects.filter(~Q(shop_no= request.user.shop_number),balanced_out = False).values("shop_no").order_by("shop_no").annotate(count = Sum("amount"))


    return local_owed,retail_owe

def debts_and_credits_data(request):

    local_owed = LocalSales.objects.filter(status=False,paid=False).order_by("shop_no")

    retail_owe = RetailSales.objects.filter(~Q(shop_no = request.user.shop_number),balanced_out = False).order_by("shop_no")

    return local_owed, retail_owe

@login_required
def analysis(request):

    owes = get_debts_and_credits_summation(request)
    owe_data= debts_and_credits_data(request)

    # iterate through the data
    for index,objects in enumerate(owes):
        for summation_obj in objects:
            shop_number  = summation_obj.get("shop_no")

            # create object to store the data
            sale_data = []
            # iterate through the data
            for obj_data in owe_data[index]:
                if obj_data.shop_no == shop_number:
                    sale_data.append(obj_data)

            summation_obj["data"] = sale_data
    
    print(list(owes[0]))
    # for i,k in enumerate(owes):
    #     print(i,k)
    # for i in owe_data[0]:
    #     print(i.shop_no)
    # for summation_obj in owes[0]:
    #     print(k.get("shop_no")


    return render(request,"analysis.html",{"localsum":list(owes[0]),"retailsum":list(owes[1]),})

@login_required
def balancing_out(request):

    if request.method == "POST":

        # get data
        data = json.loads(request)

        return JsonResponse()

