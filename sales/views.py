from django.shortcuts import render
from django.http import JsonResponse
from .forms import Wholesale,Retail_sales,Search_sales
from utils.models import AvailableStock,RetailSales,LocalSales
from datetime import date
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# TODO show client when colour or size is depleted
#TODO for retail sales price is gotten from client

#View for local sales 
@login_required
def baseSales(request):
    form = Wholesale()

    if request.method == "POST":

        # get JSON data sent through fetch
        sales_data = json.load(request)
        
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
            amount_sold = 0 

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
                    shop = sold_color["name"]
                    # covert paid string to boolean value
                    status = False
                    paid = sold_color["paid"]
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
                                AvailableStock.query.filter_by(name=key).delete()
                                
                                # Stock_log.depletion_date = date.today()
                                response_message = {"message":"success","success":f"The ${key} is now depleted"}

                                return JsonResponse(response_message)

                        # TODO delete object from variation
                        # elif old_color[color]  == 0
                        #     return

                        # upload sale to database
                        sale = LocalSales(product=key,size=size,colour=color,shop_no=shop,paid=paid,status=status,date=date.today(),price=stock.price)

                        sale.save()
                            # TODO remove stock color and sizes and product altogether if depleted

                        
            # update stock amount remaining, variation, date
            stock.amount = stock.amount - 1

            # if stock.amount

            stock.variation = json.dumps(available_stock)

            stock.date = date.today()

            stock.sizes = json.dumps(available_sizes)

            
            response_message = {"message":"success"}
            # for key in sales_data:
            sales_data =  json.dumps(sales_data)


            return JsonResponse(response_message)

    return render(request,"record.html",{"form": form})


# view for retail sales
@login_required
def Retailsales(request):

    form = Retail_sales()

    # get data if 
    if request.method == "POST":

        sales_data = json.load(request)

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
            amount_sold = 0 

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
                    shop = sold_color["name"]
                    # covert paid string to boolean value
                    status = False
                    paid = sold_color["paid"]
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
                                AvailableStock.query.filter_by(name=key).delete()
                                
                                # Stock_log.depletion_date = date.today()
                                response_message = {"message":"success","success":f"The ${key} is now depleted"}

                                return JsonResponse(response_message)

                        # TODO delete object from variation
                        # elif old_color[color]  == 0
                        #     return

                        # upload sale to database
                        sale = LocalSales(product=key,size=size,colour=color,shop_no=shop,paid=paid,status=status,date=date.today(),price=stock.price)

                        sale.save()
                            # TODO remove stock color and sizes and product altogether if depleted

                        
            # update stock amount remaining, variation, date
            stock.amount = stock.amount - 1

            # if stock.amount

            stock.variation = json.dumps(available_stock)

            stock.date = date.today()

            stock.sizes = json.dumps(available_sizes)

            
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

    return render(request,"record.html",{"form":form})

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
            # pass

        retail_results = RetailSales.objects.filter(query).all().values()
        print(RetailSales.objects.filter(query).all())

        wholesale_results = LocalSales.objects.filter(query).all().values()

        response_message = {"message":"success", "retail results": list(retail_results),"wholesale results": list(wholesale_results)}
        return JsonResponse(response_message)

    return render(request ,"search.html",{"form":form})