from django.urls import path
from . import views

urlpatterns = [
    path("",views.baseSales),
    path("retail",views.Retailsales),
    path("search",views.search)

    ]