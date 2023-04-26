from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Retail_Sales_Log)
admin.site.register(Products_Available)
admin.site.register(Products_Logs)
admin.site.register(Wholesale_Sales_Logs)
admin.site.register(Products_Order_Logs)