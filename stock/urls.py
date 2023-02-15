from django.urls import path
from . import views

urlpatterns = [
    path("Addorders",views.update_stock_ordered),
    path("updateAvailable",views.update_available_stock)
]