from django.urls import path
from . import views

urlpatterns = [
    path("",views.baseSales),
    path("retail",views.Retailsales),
    path("search",views.search),
    path("changepay",views.changepay),
    path("changereturn",views.changereturn),
    path("retail/changereturn",views.changereturnretail),
    path("retail/changepay",views.changepayretail)
    ]