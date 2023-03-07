from django.shortcuts import render,redirect
from .forms import Login,CreateAccount
from .models import Users
from hashlib import sha512

# Create your views here.
def Signin(request):

    form = Login()

    if request.method == "POST":

        form = Login(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]

            password = form.cleaned_data["password"]

            user = Users.objects.filter(username = username, password = sha512(password.encode()).hexdigest())
            
            if user:
                print("yeah")
                return redirect("/")
            else:
                print("umm..")
                print(sha512(password.encode()).hexdigest())

    return render(request,"login.html",{"form":form})

def Signup(request):

    form = CreateAccount()

    if request.method == "POST":
        form = CreateAccount(request.POST)

        if form.is_valid():

            # get data from submitted
            name = form.cleaned_data["name"]

            username = form.cleaned_data["username"]

            owner = form.cleaned_data["owner"]

            shop = form.cleaned_data["shop"]
            
            # initialize user instance
            user = Users(username = username, first_name = name, shop_number = shop, rights = owner)
            
            # confirm passwords provided are correct
            confirm_password = form.cleaned_data["confirm_password"]
            
            password = form.cleaned_data["password"]          

            if password == confirm_password:

                # set password for the user
                user.create_password(password)

                # save user
                user.save()

                # redirect user to login page
                return redirect("/login")
            else:
                pass



            pass

    return render (request,"login.html",{"form":form})
