from datetime import date
from django.db import models
# from django.models import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
# from django.utils import timezone

# Create your models here.

class RetailSales(models.Model):

    product = models.CharField(max_length=50,null = False)

    size = models.CharField(max_length=50, null = False)

    colour = models.CharField(max_length=50,null = False)

    shop_no =models.CharField(max_length=10,null = False)

    status = models.BooleanField( null = False) 

    paid = models.BooleanField( default = False)

    buyer = models.CharField(max_length=255,null = True)

    amount = models.IntegerField(null = True)

    balanced_out = models.BooleanField(default=False)

    date = models.DateField( default= date.today, null=False)


class Stock(models.Model):

    name = models.CharField(max_length=50,unique=False, null=False)

    size_range = models.TextField( null=False)

    colours = models.TextField(null=False)

    amount = models.IntegerField(null=False)

    variation = models.TextField(null=False)

    Shipper_name = models.CharField(max_length=255,null=True)

    date = models.DateField(default=date.today)

    depletion_date = models.DateField(null=True,default= None)



class AvailableStock(models.Model):


    name = models.CharField(max_length= 50, primary_key=True,unique=True, null=False)

    size_range = models.TextField(null=False)

    colours = models.TextField( null=False)

    amount = models.IntegerField(null=False)

    variation = models.TextField( null=False)

    date = models.DateField( default=date.today, null=False)

    price = models.IntegerField(null = True)


    # function to return the worth of goods in stock
    def worth(self):
        return self.amount * self.price
    

class LocalSales(models.Model):

    # index = models.Integer, index = True,primary_key = True, unique= True,null=False)

    product = models.CharField(max_length =50, null = False )

    size = models.CharField (max_length=50,null = False)

    colour = models.CharField(max_length =50, null = False)

    shop_no = models.CharField(max_length =10,null = False)

    status = models.BooleanField( null = False )

    paid = models.BooleanField(null = False)

    date = models.DateField( default= date.today, null=False)

    price = models.IntegerField(null=False)


class Ordered(models.Model):

    # index = models.Integer, index = True,primary_key = True, unique= True,null=False)

    name = models.CharField(max_length =50, unique=False, null=False)

    size_range = models.TextField(null=False)

    colours = models.TextField(null=False)

    amount = models.IntegerField(null=False)

    variation = models.TextField( null=False)

    order_price = models.IntegerField(null=False)

    shipping_co = models.CharField(max_length =100,null=True)

    comments = models.TextField(null=True)

    order_date = models.DateField( default=date.today)

    arrival_date = models.DateField( null = True)

    arrived = models.BooleanField(default=False,null=False)

class Products_Order_Logs(models.Model):

    name = models.CharField(max_length =50, unique=False, null=False)

    size_range = models.JSONField(null=False)

    colours = models.JSONField(null=False)

    amount = models.IntegerField(null=False)

    variation = models.JSONField( null=False)

    order_price = models.IntegerField(null=True)

    shipping_co = models.CharField(max_length =100,null=True)

    comments = models.TextField(null=True)

    order_date = models.DateField( default=date.today)

    proposed_arrival = models.DateField( null = True)

    arrival_date = models.DateField( null = True)

    arrived = models.BooleanField(default=False,null=False)

class Products_Logs(models.Model):

    product_name = models.CharField(unique=False,max_length=50,null=False)

    order_id = models.ForeignKey(Products_Order_Logs,on_delete=models.CASCADE,null=True)

    sizes = models.JSONField(null=False)

    colours = models.JSONField(null= False)

    product_variation = models.JSONField(null=False)

    amount = models.IntegerField(null=False)

    Arrival_date = models.DateField(default=date.today)

    depletion_date = models.DateField(null=True,default=None)


class Products_Available(models.Model):

    name = models.CharField(max_length=50, null=False)

    Batch_no = models.ForeignKey(Products_Logs, on_delete=models.CASCADE, null=False)

    Colour = models.CharField(max_length=20, null=False)

    Size = models.CharField(max_length=7, null=False)

    Price = models.IntegerField(null=True)

    Amount = models.IntegerField(null=False)

class Wholesale_Sales_Logs(models.Model):

    product = models.CharField(max_length =50, null = False )

    Batch = models.ForeignKey(Products_Logs,on_delete=models.CASCADE, default=None) 

    size = models.CharField (max_length=50,null = False)

    colour = models.CharField(max_length =50, null = False)

    shop_no = models.CharField(max_length =10,null = False)

    status = models.BooleanField( null = False )

    paid = models.BooleanField(null = False)

    date = models.DateField( default= date.today, null=False)

    price = models.IntegerField(null=False)

