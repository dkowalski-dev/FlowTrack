from django.shortcuts import render
from .models import IndividualClient, CompanyClient

def clients(request):
    individual_client_list = IndividualClient.objects.filter(owner=request.user)
    company_client_list = CompanyClient.objects.filter(owner=request.user)
    context = {
        "individual_client_list": individual_client_list,
        "company_client_list": company_client_list
    }
    return render(request, "clients/clients.html", context)