from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address =  models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True,blank=True)
    image = models.ImageField(default='profile_icon.png', upload_to='Profile_Images')
    
    def __str__(self):
        return f'{self.staff.username}-Profile'
    

class Customer(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=254, null=True, unique=True)
    contact = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    car_make = models.CharField(max_length=100, null=True, blank=True)
    plate_no = models.CharField(max_length=10, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    