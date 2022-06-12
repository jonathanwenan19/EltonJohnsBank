from enum import unique
from string import digits
from typing_extensions import Required
from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class account_user(models.Model):
    id = models.AutoField(primary_key= True, db_column="account_no")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length= 100)
    username = models.CharField(max_length= 100)
    password= models.CharField(max_length=100)
    pin = models.IntegerField()
    card_no = models.CharField(max_length=16)
    balance = models.DecimalField(max_digits=15, decimal_places=3)

    def __str__(self):
        return self.username

    user_objects = models.Manager()


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,blank = False)
    last_name = models.CharField(max_length= 100,blank = False)
    pin = models.CharField(max_length=6,blank = False)
    card_no = models.CharField(primary_key = True,max_length=16, blank = False, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=3,blank= False)
    

#class transaction(models.Model):
 #   sender = models.OneToOneField(User, on_delete=models.CASCADE)
  #  payment_id = models.UUIDField(default=uuid.uuid4, editable=False,primary_key= True )
   # receiver_no = models.CharField(max_length=16, blank = False)
   # amount = models.DecimalField(max_digits=15, decimal_places=3,blank= False)
   # notes = models.CharField(max_length = 100)


class payments(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False , primary_key= True)
    receiver_no = models.CharField(max_length=16, blank = False)
    amount = models.DecimalField(max_digits=15, decimal_places=3,blank= False)
    notes = models.CharField(max_length = 100, blank = False)

class profilepic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to = "profile_pics")

    def __str__(self):
        return f'{self.user.username} Profile'

class photos(models.Model):
    id = models.AutoField(primary_key= True)
    image = models.ImageField(upload_to='nodeflux_photos/')

    



    



