from django.db import models
from django.contrib.auth.models import User
from django.db import connections
# Create your models here.

class Ins(models.Model):

# Create your models here.
    lname=models.CharField(max_length = 100)
    fname=models.CharField(max_length = 100)
    # address=models.CharField(max_length = 100)
    # msi = models.CharField(max_length=20)
    # nida = models.CharField(max_length=20)
    # score = models.IntegerField()
    # email = models.CharField(max_length=100)
    # activationd = models.DateField()
    # dob=models.DateField()
    
     

    
    # interest_amount=models.IntegerField()
    class Meta:
        db_table="insurance"

class Form(models.Model):

# Create your models here.
    email=models.CharField(max_length = 100)
    password=models.IntegerField()
    

    
    # interest_amount=models.IntegerField()
    class Meta:
        db_table="form"
