from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Service(models.Model):
    contract = models.ForeignKey(Contract, related_name='services', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    file = models.FileField(upload_to='invoices/')
    invoice_number = models.CharField(max_length=255, blank=True)
    date = models.DateField(blank=True, null=True)
    total_amount = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=50, default='pending')

class Discrepancy(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='discrepancies', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount_difference = models.FloatField()