import uuid

from django.contrib.auth.models import User
from django.db import models

from .utils import formatted_price


class Category(models.Model):
    choices = (
        ("0", "0%"),
        ("5", "5%"),
        ("8", "8%"),
        ("23", "23%"),
    )
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    vat = models.CharField(
        max_length=2, choices=choices, default="23"
    )  # Tutaj jeszcze wróć i się zastanów czy nie zmienić tego na intiger w razie operacji w przyszłości

    @property
    def full_name(self):
        return str(" - ".join([self.name, self.vat + "%"]))

    def __str__(self):
        return str(" ".join([self.name, self.vat + "%"]))

    class Meta:
        ordering = ["name"]


class Product(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100, blank=True, default="")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, default="", null=True
    )
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    @property
    def purchase_formatted(self):
        return formatted_price(self.purchase_price)

    @property
    def sale_formatted(self):
        return formatted_price(self.sale_price)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ["name"]
