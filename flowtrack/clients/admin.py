from django.contrib import admin

from .models import CompanyClient, IndividualClient

admin.site.register(IndividualClient)
admin.site.register(CompanyClient)
