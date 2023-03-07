from django.urls import path
from . import views

urlpatterns = [
path("",views.Signin),
path("createaccount",views.Signup)
]