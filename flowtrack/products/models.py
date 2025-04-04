from django.db import models
from django.contrib.auth.models import User
import uuid

class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    purchase_price = models.FloatField(default=0)
    sale_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.name)
