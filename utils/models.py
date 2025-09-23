from datetime import date, datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager,PermissionsMixin
from hashlib import sha512

# create model for user management
class Users(AbstractBaseUser,PermissionsMixin):
    Username = models.CharField(max_length=50,unique=True)
    
    password = models.CharField(max_length=512)
    
    email = models.EmailField(max_length=100, null=True,unique=True)
    
    is_admin = models.BooleanField(null=False, default=False)
    
    Date_created = models.DateTimeField(default= datetime.today)
    
    Last_visit = models.DateTimeField(default= datetime.today)
    
    migrated = models.BooleanField(null=False, default=False)
    
    shop_number = models.CharField(max_length= 20, null= False)    
    
    @property
    def rights(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_superuser(self):
        return self.is_admin
        
    USERNAME_FIELD = "Username"
    objects = UserManager()
    
    def check_Password(self,password):
        
        print("********checking password********")        
        
        hashed_pass = sha512(password.encode()).hexdigest()

        if hashed_pass == self.password:
            return True
        else:
            return False
        
    def create_password(self,password):
                
        self.password = sha512(password.encode()).hexdigest()
        
    def rights(self):
        
        return False
    
    def get_scopes_for_user(self):
        
        if self.is_superuser:
            return ["read", "write", "order", "cart", "payment", "wishlist", "review", "admin_read", "admin_write", "admin_manage"]
        
        elif self.is_staff:
            return ["admin_read", "admin_write"]
        
        elif self.is_authenticated:
            return ["read", "write", "order", "cart", "payment", "wishlist", "review"]
        else:
            return ["read"]


class Products_Order_Logs(models.Model):

    name = models.CharField(max_length =50, unique=False, null=False)

    shop = models.ForeignKey(Users,on_delete=models.CASCADE,null=False, default=None)
    
    size_range = models.JSONField(null=False)

    colours = models.JSONField(null=False)

    amount = models.IntegerField(null=False)

    variation = models.JSONField( null=False)

    order_price = models.IntegerField(null=True)

    shipping_co = models.CharField(max_length =100,null=True)

    comments = models.TextField(null=True)

    order_date = models.DateField( default=date.today)

    proposed_arrival = models.DateField( null = True)

    arrival_date = models.DateField( null = True)

    arrived = models.BooleanField(default=False,null=False)

class Products_Logs(models.Model):

    product_name = models.CharField(unique=False,max_length=50,null=False)
    
    shop = models.ForeignKey(Users,null=False,on_delete=models.CASCADE,default=None)

    order_id = models.ForeignKey(Products_Order_Logs,on_delete=models.CASCADE,null=True)

    sizes = models.JSONField(null=False)

    colours = models.JSONField(null= False)

    product_variation = models.JSONField(null=False)

    amount = models.IntegerField(null=False)

    order_amount = models.IntegerField(null=True)

    Arrival_date = models.DateField(default=date.today)

    depletion_date = models.DateField(null=True,default=None)

class Products_Available(models.Model):

    name = models.CharField(max_length=50, null=False)
    
    # shop = models.ForeignKey(Users,null=False,on_delete=models.CASCADE,default=None)

    Batch_no = models.ForeignKey(Products_Logs, on_delete=models.CASCADE, null=False, related_name="availability")

    Colour = models.CharField(max_length=20, null=False)

    Size = models.CharField(max_length=7, null=False)

    Price = models.IntegerField(null=True)

    Amount = models.IntegerField(null=False)

class Wholesale_Sales_Logs(models.Model):

    product = models.CharField(max_length =50, null = False )

    Batch = models.ForeignKey(Products_Logs,on_delete=models.CASCADE, default=None, related_name="sales") 

    size = models.CharField (max_length=50,null = False)

    colour = models.CharField(max_length =50, null = False)

    shop_no = models.CharField(max_length =10,null = False)

    status = models.BooleanField( null = False )

    paid = models.BooleanField(null = False)

    date = models.DateField( default= date.today, null=False)

    price = models.IntegerField(null=False)

class Retail_Sales_Log(models.Model):

    product = models.CharField(max_length=50,null = False)

    size = models.CharField(max_length=50, null = False)

    colour = models.CharField(max_length=50,null = False)

    shop_no =models.CharField(max_length=10,null = False)

    status = models.BooleanField(default=False, null=False) 

    paid = models.BooleanField(null=False ,default=False)

    buyer_name = models.CharField(max_length=255,null = True)

    price = models.IntegerField(null=False)

    balanced_out = models.BooleanField(default=False)

    date = models.DateField( default= date.today, null=False)

class Credit_and_Debit_Management(models.Model):

    Shop_name = models.CharField(max_length=50 ,null=False)

    debt = models.IntegerField(null=False)

    Amount_paid = models.IntegerField(null=False)