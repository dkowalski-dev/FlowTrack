from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=30, blank=True, default="")
    company_name = models.CharField(max_length=255, blank=True, default="")
    nip = models.CharField(max_length=10, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=16, blank=True, default="")
    address = models.CharField(max_length=120, blank=True, default="")
    #Wyświetlanie listy ofert
    show_created = models.BooleanField(default=True)
    show_client = models.BooleanField(default=True)
    show_client_email = models.BooleanField(default=True)
    show_client_phone = models.BooleanField(default=True)
    show_client_address = models.BooleanField(default=True)
    show_client_region = models.BooleanField(default=True)
    show_status = models.BooleanField(default=True)
    show_description = models.BooleanField(default=False)
    default_sort = models.CharField

