from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=20)
    viewpassword=models.CharField(max_length=20)

class Landowner(models.Model):
    name=models.CharField(max_length=40,null=True)
    address=models.CharField(max_length=40,null=True)
    email=models.CharField(max_length=40,null=True)
    phone=models.CharField(max_length=40,null=True)
    license_no=models.CharField(max_length=40,null=True)
    user=models.ForeignKey(Login,on_delete=models.CASCADE,null=True)

class User(models.Model):
    name=models.CharField(max_length=40,null=True)
    address=models.CharField(max_length=40,null=True)
    email=models.CharField(max_length=40,null=True)
    phone=models.CharField(max_length=40,null=True)
    aadhaar_no=models.CharField(max_length=40,null=True)
    user=models.ForeignKey(Login,on_delete=models.CASCADE,null=True)

class Landarea(models.Model):
    location=models.TextField(null=True)
    image=models.ImageField(upload_to="uploadImage",max_length=None,null=True)
    sqft=models.CharField(max_length=10,null=True)
    price=models.IntegerField(null=True)
    description=models.TextField(null=True)
    status=models.CharField(max_length=40,null=True,default='Available')
    date=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(Landowner,on_delete=models.CASCADE,null=True)

class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    land=models.ForeignKey(Landarea,on_delete=models.CASCADE,null=True)
    date=models.DateTimeField(auto_now_add=True)
    price=models.IntegerField(null=True)
    advance=models.IntegerField(null=True)
    status=models.CharField(max_length=40,null=True,default='Booked')


    



