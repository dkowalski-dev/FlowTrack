from django.db import models
import uuid
from django.contrib.auth.models import User

class Client(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=16, blank=True, default="")
    address = models.CharField(max_length=120, blank=True, default="")
    region = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        abstract = True

class IndividualClient(Client):
    name = models.CharField(max_length=30, blank=True, default="")
    last_name = models.CharField(max_length=30, blank=True, default="")

    def __str__(self):
        return self.name + ' ' + self.last_name
    
class CompanyClient(Client):
    contact_person = models.CharField(max_length=30, blank=True, default="")
    company_name = models.CharField(max_length=255, blank=True, default="")
    nip = models.CharField(max_length=10, blank=True, default="")

    def __str__(self):
        return self.company_name