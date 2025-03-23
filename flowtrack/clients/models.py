from django.db import models
import uuid

class Client(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=120, blank=True, null=True)
    region = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        abstract = True

class IndividualClient(Client):
    name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    
class CompanyClient(Client):
    company_name = models.CharField(max_length=255, blank=True, null=True)
    nip = models.CharField(max_length=20, null=True, blank=True)