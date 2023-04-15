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

            Wholesale_sale = Wholesale_Sales_Logs(product=product, Batch_no=Parent_Product_log, size=size, colour=colour, shop_no=shop, status=False, paid=paid,price=Available_Product.price )

            Available_Product.save()
            Wholesale_sale.save()

    # fetch  the sales for the day
    sales = LocalSales.objects.filter(date=date.today())
    return render(request,"record.html",{"form": form,"sales":sales})


# view for retail sales
@login_required
def Retailsales(request):

    form = Retail_sales()

    # get data if 
    if request.method == "POST":

        sales_data = json.load(request)

        # check if it is a retail sale or a brokering sale
        for key in sales_data:
            for size in sales_data[key]:
                sale_size = sales_data[key][size]
                shop_number = sale_size.get("name")
                print(shop_number)

                if shop_number != request.user.shop_number:
                    response = brokering(request,sales_data)
                    return JsonResponse(response)

        # Iterate through the sales Objects
        for key in sales_data:

            # check product exists
            stock = AvailableStock.objects.filter(name=key).first()

            # if the stock does not exist
            if not stock:
                response_message = {"message": "error","error": f"The product {key} does not exist"}
                return JsonResponse(response_message)
            
            # Change JSON strings to JSON obj
            available_stock = json.loads(stock.variation)
            available_sizes = json.loads(stock.size_range)
            sold_stock = sales_data[key]

            # check if size exists
            for size in sold_stock:

                # return error if size is not available in database
                if size not in available_stock:
                    response_message = {"message":"error","error":f"size {size} not found"}
                    return JsonResponse(response_message)

                elif size in available_stock:

                    # Return error if the stock in question has not been priced
                    if not stock.price:
                        response_message = {"message":"error","error":"Stock is yet to be priced Cannot make sale"}
                        return JsonResponse(response_message)
                    
                    # get size objects
                    old_color = available_stock[size]
                    sold_color = sold_stock[size]

                    color = sold_color["color"]
                    shop = sold_color.get("name")
                    buyer = sold_color.get("buyer")
                    price = sold_color["amount"]
                    paid = sold_color["paid"]
                    # covert paid string to boolean value
                    status = False
                    if paid == "false":
                        paid = False
                    elif paid == "true":
                        paid = True

                    # Check if the color is available
                    if color not in old_color:
                        response_message = {"message":"error","error":f"The colour {color} in size {size} not found"}
                        return JsonResponse(response_message)

                    elif color in old_color:

                        old_color[color] = old_color[color] - 1
                        
                        #Incase of incorrect data in db catch error of zero stock
                        if old_color[color] < 0:
                            response_message = {"message":"error","error":f"Cannot have negative stock amount"}
                            return JsonResponse(response_message)
                        
                        # delete color if it is depeleted
                        elif old_color[color] == 0:
                            del old_color[color]

                            # test also if stock size is depleted
                            if len(old_color) == 0:
                                del available_stock[size]


                                # Update size lists
                                available_sizes.remove(size)

                                # update db object
                                stock.size_range = json.dumps(available_sizes)


                            # test if the stock id depleted altogether
                            if len(available_stock) == 0:
                                stock.delete()
                                
                                # Stock_log.depletion_date = date.today()
                                response_message = {"message":"success","success":f"The ${key} is now depleted"}

                                return JsonResponse(response_message)

                        # TODO delete object from variation
                        # elif old_color[color]  == 0
                        #     return

                        # upload sale to database
                        print(shop,buyer)
                        if shop and not buyer:
                            print("1")
                            sale = RetailSales(product=key,size=size,colour=color,shop_no=shop,paid=paid,status=status,date=date.today(),amount=price)
                            sale.save() 
                        elif buyer and not shop:
                            print("2")
                            sale = RetailSales(product=key,size=size,colour=color,buyer=buyer,paid=paid,status=status,date=date.today(),amount=price)
                            sale.save() 
                        elif buyer and shop:
                            print("3")
                            sale = RetailSales(product=key,size=size,colour=color,shop_no=shop,buyer=buyer,paid=paid,status=status,date=date.today(),amount=price)
                            sale.save()
                        elif not buyer and not shop:
                            print("4")
                            sale = RetailSales(product=key,size=size,colour=color,paid=paid,status=status,date=date.today(),amount=price)
                            sale.save()

            
                            # TODO remove stock color and sizes and product altogether if depleted

                        
            # update stock amount remaining, variation, date
            stock.amount = stock.amount - 1

            # if stock.amount

            stock.variation = json.dumps(available_stock)

            stock.date = date.today()

            stock.sizes = json.dumps(available_sizes)

            stock.save()

            
            response_message = {"message":"success"}
            # for key in sales_data:
            sales_data =  json.dumps(sales_data)


            return JsonResponse(response_message)

        pass

        # form = Retail_sales(request.post)

        # if form.is_valid():

        #     # get data submitted
        #     product_name = form.cleaned_data["product"]
        #     size = form.cleaned_data["size"]
        #     colour = form.cleaned_data["colour"]
        #     name = form.cleaned_data["name"] 
        #     paid = form.cleaned_data["paid"] 
        #     buyer = form.cleaned_data["buyer"]
        #     amount = form.cleaned_data["amount"]
        #     pass

    return render(request,"retailrecords.html",{"form":form})

@login_required
def brokering(request,sales_object):

    for key in sales_object:

        product = key

        sale_data = sales_object[product]

        for size in sale_data:

            sale_size = size

            sale_details = sale_data[size]

            color = sale_details["color"]
            shop = sale_details.get("name")
            buyer = sale_details.get("buyer")
            price = sale_details["amount"]
            paid = sale_details["paid"]

        # if not 
            if paid == "false":
                paid = False
            elif paid == "true":
                paid = True

            # save the object
            if buyer:
                sale = RetailSales(product=product,size=sale_size,colour=color,shop_no=shop,buyer=buyer,paid=paid,status=False,date=date.today(),amount=price)
                sale.save()
                response_message = {"message":"success"}
                return response_message
            elif not buyer:
                sale = RetailSales(product=product,size=sale_size,colour=color,shop_no=shop,paid=paid,status=False,date=date.today(),amount=price)
                sale.save()
                response_message = {"message":"success"}
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