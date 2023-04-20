from django.shortcuts import render
from django.http import JsonResponse
from .forms import Wholesale,Retail_sales,Search_sales
from utils.models import *
from datetime import date
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from operator import itemgetter
# TODO show client when colour or size is depleted
#TODO for retail sales price is gotten from client
# Define function to set json strings to Boolena values
def json_bool(value):
    if value == "False":
        return False
    else:
        return True

#View for local sales 
@login_required
def baseSales(request):
    form = Wholesale()

    if request.method == "POST":

        # get JSON data sent through fetch
        sales_data = json.load(request)

        # get the data from the JSON object
        product,colour,size,shop,paid = itemgetter("product","color","sizes","name","paid")(sales_data)
 
        Available_Product = Products_Available.objects.filter(name=product,Colour=colour,Size=size).first()

        if not Available_Product:
            response_message = {"message": "error","error": f"The product is not available"}
        elif Available_Product:
            # update the product
            Parent_Product_log = Available_Product.Batch_no
            Parent_Product_log.amount = Parent_Product_log.amount - 1

            # TODO delete if the amount is 0

            Wholesale_sale = Wholesale_Sales_Logs(product=product, Batch=Parent_Product_log, size=size, colour=colour, shop_no=shop, status=False, paid=paid,price=Available_Product.Price )

            Available_Product.save()
            Wholesale_sale.save()
            Parent_Product_log.save()
            response_message = {"message": "success","success": "Sale successfully added"}

        return JsonResponse(response_message)
    
    # fetch  the sales for the day
    sales = Wholesale_Sales_Logs.objects.filter(date=date.today())
    return render(request,"record.html",{"form": form,"sales":sales})

# view for retail sales
@login_required
def Retailsales(request):

    form = Retail_sales()

    if request.method == "POST":

        sales_data = json.load(request)

        # check if it is a retail sale or a brokering sale
        product,colour,size,shop,paid,price = itemgetter("product","color","sizes","name","paid","amount")(sales_data)
        buyer = sales_data.get("buyer")

        if shop != request.user.shop_number:
            response = brokering(request,sales_data)
            return JsonResponse(response)

        # Iterate through the sales Objects
        Available_Product = Products_Available.objects.filter(name=product,Colour=colour,Size=size).first()

        if not Available_Product:
            response_message = {"message": "error","error": f"The product is not available"}
        elif Available_Product:

            # update the product
            Parent_Product_log = Available_Product.Batch_no
            Parent_Product_log.amount = Parent_Product_log.amount - 1
            Available_Product.Amount = Available_Product.Amount -1

            if buyer:
                sale = Retail_Sales_Log(product=product,size=size,colour=colour,shop_no=shop,buyer_name=buyer,paid=paid,status=False,date=date.today(),price=price)
                sale.save()
                response_message = {"message":"success"}
                return response_message
            elif not buyer:
                sale = Retail_Sales_Log(product=product,size=size,colour=colour,shop_no=shop,paid=paid,status=False,date=date.today(),price=price)
                sale.save()
                response_message = {"message":"success"}
                return response_message
            
            Parent_Product_log.save()
            Available_Product.save()
            response_message = {"message": "success","success": "Sale successfully added"}


    return render(request,"retailrecords.html",{"form":form})

@login_required
def brokering(request,sales_object):


    product,colour,size,shop,paid,price = itemgetter("product","color","sizes","name","paid","amount")(sales_object)
    buyer = sales_object.get("buyer")


    # save the object
    if buyer:
        sale = Retail_Sales_Log(product=product,size=size,colour=colour,shop_no=shop,buyer_name=buyer,paid=paid,status=False,date=date.today(),price=price)
        sale.save()
        response_message = {"message":"success"}
        return response_message
    elif not buyer:
        sale = Retail_Sales_Log(product=product,size=size,colour=colour,shop_no=shop,paid=paid,status=False,date=date.today(),price=price)
        sale.save()
        response_message = {"message":"success"}
        return response_message


@login_required
def shop_sales(request,sales_object):
        product,colour,size,shop,paid = itemgetter("product","color","sizes","name","paid")(sales_data)
 
        Available_Product = Products_Available.objects.filter(name=product,Colour=colour,Size=size).first()

        if not Available_Product:
            response_message = {"message": "error","error": f"The product is not available"}
        elif Available_Product:
            # update the product
            Parent_Product_log = Available_Product.Batch_no
            Parent_Product_log.amount = Parent_Product_log.amount - 1

            # TODO delete if the amount is 0

            Wholesale_sale = Wholesale_Sales_Logs(product=product, Batch_no=Parent_Product_log, size=size, colour=colour, shop_no=shop, status=False, paid=paid,price=Available_Product.price )

            Available_Product.save()
            Wholesale_sale.save()

            return response_message

@login_required
def search(request):

    form = Search_sales()

    # get data sent using fetch
    if request.method == 'POST':

        search_filters = json.load(request)

        # build a query
        query = Q()
        # build query
        if search_filters.get("product"):
            query &= Q(product=search_filters["product"])
            # pass
        if search_filters.get("shop_no"):
            query &= Q(shop_no = search_filters["shop_no"])
            # pass
        if search_filters.get("size"):
            query &= Q(size = search_filters["size"])
            # pass
        if search_filters.get("colour"):
            query &= Q(colour = search_filters["colour"])
            # pass
        if search_filters.get("start_date"):
            query &= Q(date__range = [search_filters["start_date"],search_filters["end_date"]])
        
        # filter the paid and returned booleans 
        query &= Q(paid = search_filters["paid"])
        query &= Q(status = search_filters["returned"])

        retail_results = RetailSales.objects.filter(query).all().values().order_by("-date")

        wholesale_results = LocalSales.objects.filter(query).all().values().order_by("-date")

        response_message = {"message":"success", "retail results": list(retail_results),"wholesale results": list(wholesale_results)}
        return JsonResponse(response_message)

    return render(request ,"search.html",{"form":form})


@login_required
def changepay(request):

    if request.method == "POST":

        sale_object = json.load(request)

        # get attributes of the sale object
        name,size,colour,shop,ret,pay = itemgetter("name","size","colour","shop","return","pay")(sale_object)

        ret = json_bool(ret)
        pay = json_bool(pay)

        # get the db object
        sale_db_object = LocalSales.objects.filter(product=name,size=size,colour=colour,shop_no=shop,status=ret,paid=pay).first()

        # set the new status
        if sale_db_object:
            sale_db_object.paid = not pay
            sale_db_object.save()
            response_message = {"message":"success"}
        elif not sale_db_object:
            response_message = {"message":"error","error":"Please refresh page and try again"}    
            
        return JsonResponse(response_message)


@login_required
def changepayretail(request):

    if request.method == "POST":

        sale_object = json.load(request)

        # get attributes of the sale object
        name,size,colour,shop,ret,pay = itemgetter("name","size","colour","shop","return","pay")(sale_object)

        ret = json_bool(ret)
        pay = json_bool(pay)

        # get the db object
        sale_db_object = RetailSales.objects.filter(product=name,size=size,colour=colour,shop_no=shop,status=ret,paid=pay).first()

        # set the new status
        if sale_db_object:
            sale_db_object.paid = not pay
            sale_db_object.save()
            response_message = {"message":"success"}
        elif not sale_db_object:
            response_message = {"message":"error","error":"Please refresh page and try again"}    
            
        return JsonResponse(response_message)

def changereturn(request):
    
    if request.method == "POST":

        sale_object = json.load(request)

        #get attributes of the sale object
        name,size,colour,shop,ret,pay = itemgetter("name","size","colour","shop","return","pay")(sale_object)
        
        # change the json strings value to truthy values
        ret = json_bool(ret)
        pay = json_bool(pay)

        # get the db object
        sale_db_object = LocalSales.objects.filter(product=name,size=size,colour=colour,shop_no=shop,status=ret,paid=pay).first()
        
        # set the new status and save the changes
        if sale_db_object:
            sale_db_object.status = not ret

            # Add the returned stock to available stock
            available_stock = AvailableStock.objects.filter(name = name).first()

            # product was not depleted
            if available_stock:

                #store the data in variables
                available_sizes = json.loads(available_stock.size_range)
                available_colours = json.loads(available_stock.colours)
                avaiable_variation = json.loads(available_stock.variation)

                # add the returned product to db
                if size not in available_sizes:
                    available_sizes.append(size)

                if colour not in available_colours:
                    available_colours.append(colour)

                # get the size in variation
                object_sizes = avaiable_variation.get(size)
                
                # check if the size was still available
                if object_sizes:

                    # check if the colour for the size was still available
                    object_colour = object_sizes.get(colour)

                    if object_colour:
                        object_sizes[colour] = object_colour + 1
                    elif not object_colour:
                        object_sizes[colour] = 1

                elif not object_sizes:
                    # create object for the size
                    new_object = {}
                    new_object[colour] = 1
                    avaiable_variation[size] = new_object
                
            # product was depleted
            elif not available_stock:

                # initialize the arrays and object to store the data
                available_sizes = []
                available_colours = []
                avaiable_variation = {}
                
                available_sizes.append(size)
                available_colours.append(colour)

                # create object for the colour
                new_object = {}
                new_object[colour] = 1

                avaiable_variation[size] = new_object
                
                returned_stock = AvailableStock(name=name,size_range = json.dumps(available_sizes),colours = json.dumps(available_colours), amount=1, variation = json.dumps(avaiable_variation),date= date.today())
                returned_stock.save()
            
            # save the object
            sale_db_object.save()
            # print(sale_db_object)
            response_message = {"message":"success"}
        elif not sale_db_object:
            response_message = {"message":"error","error":"Please refresh page and try again"}
        return JsonResponse(response_message)        



def changereturnretail(request):
    
    if request.method == "POST":

        sale_object = json.load(request)

        #get attributes of the sale object
        name,size,colour,shop,ret,pay = itemgetter("name","size","colour","shop","return","pay")(sale_object)
        
        # change the json strings value to truthy values
        ret = json_bool(ret)
        pay = json_bool(pay)

        # get the db object
        sale_db_object = LocalSales.objects.filter(product=name,size=size,colour=colour,shop_no=shop,status=ret,paid=pay).first()
        
        # set the new status and save the changes
        if sale_db_object:
            sale_db_object.status = not ret
            sale_db_object.save()
            print(sale_db_object)
            response_message = {"message":"success"}
        elif not sale_db_object:
            response_message = {"message":"error","error":"Please refresh page and try again"}
        return JsonResponse(response_message)        