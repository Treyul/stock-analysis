from django.urls import path
from . import views

urlpatterns = [
    path("",views.settings),
    path("setprice",views.setprice)
]