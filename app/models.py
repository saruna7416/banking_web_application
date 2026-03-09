from django.db import models
from decimal import Decimal
# Create your models here.
class Account(models.Model):
    account_num = models.BigAutoField(primary_key=True)
    name  = models.CharField(max_length=100)
    phone = models.PositiveBigIntegerField(unique=True)
    gender = models.CharField(max_length=7)
    email = models.EmailField(unique=True)
    address = models.TextField()
    dob = models.DateField()
    aadhar = models.PositiveBigIntegerField(unique=True)
    balance = models.DecimalField(
        decimal_places=2,
        max_digits=7,
        default=Decimal("1000.00")
    )
    pin = models.CharField(null=True)
    
