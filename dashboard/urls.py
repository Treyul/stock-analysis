from django.urls import path
from . import views

urlpatterns = [
    path("",views.home),
    path("sale-analysis",views.sale_dataset),
    path("edit-prices",views.change_price),
    path("product-arrival",views.Change_order_status_Arrived),
    path("set-price",views.change_price),
    # path(),
]