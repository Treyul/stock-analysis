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

class users(models.Model):

    username = models.CharField(max_length =255, primary_key=True,unique=True, null=False)

    Fullname = models.CharField(max_length =255,null=False)

    password = models.TextField( null=False)

    rights = models.CharField(max_length =15, null=False,default="attendant")

    shop = models.CharField(max_length =20, null= False)