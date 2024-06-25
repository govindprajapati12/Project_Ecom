from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    # email = models.EmailField(unique=True)
    first_name= models.TextField(max_length=2000,blank=True,null=True)
    last_name= models.TextField(max_length=2000,blank=True,null=True)
    phone_number = PhoneNumberField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    company_address= models.TextField(blank=True,null=True)
    profile_image=models.ImageField(upload_to='porfiles/' ,default='')

 
