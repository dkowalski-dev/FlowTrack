from django.contrib import admin
from .models import IndividualClient, CompanyClient

admin.site.register(IndividualClient)
admin.site.register(CompanyClient)