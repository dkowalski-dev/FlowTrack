from django.db import models
from django.contrib.auth.models import User
import uuid

class Category(models.Model):
    choices = (
        ('0', '0%'),
        ('5', '5%'),
        ('8', '8%'),
        ('23', '23%'),
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    vat = models.CharField(max_length=2, choices=choices, default='23')

    @property
    def full_name(self):
        return str(' - '.join([self.name, self.vat+'%']))
    
    def __str__(self):
        return str(' '.join([self.name, self.vat+'%']))

class Product(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100, blank=True, default='')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, default='', null=True)
    purchase_price = models.FloatField(default=0)
    sale_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.name)
