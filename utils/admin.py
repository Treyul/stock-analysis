from django.contrib import admin

# Register your models here.
from .models import RetailSales,Stock,AvailableStock,LocalSales,Ordered

admin.site.register(RetailSales)
admin.site.register(Stock)
admin.site.register(AvailableStock)
admin.site.register(LocalSales)
admin.site.register(Ordered)