from django.db import models
from hashlib import sha512
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser):

    rights = models.BooleanField( null = False)

    shop_number = models.CharField(max_length= 20, null= False)

    def create_password(self,password):

        self.password = sha512(password.encode()).hexdigest()

    def confirm_password(self,password):

        provided_password = sha512(password.encode()).hexdigest()

        if provided_password != self.password:
            return False
        elif provided_password == self.password:
            return True
        else:
            return 404
