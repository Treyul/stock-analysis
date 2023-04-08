from django.urls import path
from . import views

urlpatterns = [
    path("",views.analysis),
    path("sort",views.shop_sort),
    path("retailsort",views.retail_sort)
]