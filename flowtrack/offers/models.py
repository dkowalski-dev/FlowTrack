import uuid

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from products.models import Product


class StatusChoices(models.TextChoices):
    ONGOING = "ongoing", "W toku"
    FAILED = "failed", "Zakończone niepomyślnie"
    SUCCESS = "success", "Zakończone sukcesem"


class Status(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(
        max_length=7, choices=StatusChoices, default=StatusChoices.ONGOING
    )

    def __str__(self):
        return self.name


class Offer(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    client_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    client_id = models.UUIDField(null=True)
    client = GenericForeignKey("client_type", "client_id")
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(Product, through="OfferProduct", blank=True)
    description = models.TextField(blank=True, default="")

    @property
    def display_client_name(self):
        if hasattr(self.client, "company_name"):
            return self.client.company_name
        elif hasattr(self.client, "name") or hasattr(self.client, "last_name"):
            return f"{self.client.name} {self.client.last_name}"
        else:
            return "-"

    class Meta:
        ordering = ["-created"]


class OfferProduct(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    offer_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["offer", "product"], name="unique_offer_group"
            )
        ]


class Note(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ["-created"]
