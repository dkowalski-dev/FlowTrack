from django.shortcuts import render, redirect
from .models import IndividualClient, CompanyClient
from .forms import IndividualClientForm, CompanyClientForm
from django.db.models import Q
from flowtrack.utils import paginObjects

def clients(request, client_type):
    company_search_query = request.GET.get('company_search_query', '')
    individual_search_query = request.GET.get('individual_search_query', '')

    if client_type in ['all', 'com']:
        company_client_list = CompanyClient.objects.filter(owner=request.user).filter(
            Q(email__icontains=company_search_query) |
            Q(phone__icontains=company_search_query) |
            Q(address__icontains=company_search_query) |
            Q(region__icontains=company_search_query) |
            Q(contact_person__icontains=company_search_query) |
            Q(company_name__icontains=company_search_query) |
            Q(nip__icontains=company_search_query)
        )
        company_client_list, company_page_range = paginObjects(request, company_client_list, 2, page_key="company_page")
    else:
        company_client_list = []
        company_page_range = 0

    if client_type in ['all', 'ind']:
        individual_client_list = IndividualClient.objects.filter(owner=request.user).filter(
            Q(email__icontains=individual_search_query) |
            Q(phone__icontains=individual_search_query) |
            Q(address__icontains=individual_search_query) |
            Q(region__icontains=individual_search_query) |
            Q(name__icontains=individual_search_query) |
            Q(last_name__icontains=individual_search_query) 
        )
        individual_client_list, individual_page_range = paginObjects(request, individual_client_list, 2, page_key="individual_page")
    else:
        individual_client_list = []
        individual_page_range = 0

    context = {
        "individual_client_list": individual_client_list,
        "company_client_list": company_client_list,
        "company_search_query": company_search_query,
        "individual_search_query": individual_search_query,
        "client_type": client_type,
        "company_page_range": company_page_range,
        "individual_page_range": individual_page_range
    }
    return render(request, "clients/clients.html", context)

def create_client(request, client_type):
    if client_type == "ind":
        form = IndividualClientForm()
    elif client_type == "com":
        form = CompanyClientForm()
    else:
        return redirect("clients", client_type="all")
    
    if request.method == "POST":
        if client_type == "ind":
            form = IndividualClientForm(request.POST)
        elif client_type == "com":
            form = CompanyClientForm(request.POST)
        else:
            return redirect("clients", client_type="all")
        if form.is_valid():
            client = form.save(commit=False)
            client.owner = request.user
            client.save()
            return redirect("clients", client_type="all")
    
    context = {
        "form": form,
        "title": "Dodaj klienta"
    }
    return render(request, "form_template.html", context)

def update_client(request, pk, client_type):
    if client_type == "ind":
        client = IndividualClient.objects.get(id=pk)
        form = IndividualClientForm(instance=client)
    elif client_type == "com":
        client = CompanyClient.objects.get(id=pk)
        form = CompanyClientForm(instance=client)
    if request.method == "POST":
        if client_type == "ind":
            form = IndividualClientForm(request.POST, instance=client)
            if form.is_valid():
                form.save()
                return redirect("clients", client_type="all")
        elif client_type == "com":
            form = CompanyClientForm(request.POST, instance=client)
            if form.is_valid():
                form.save()
                return redirect("clients", client_type="all")
    context = { 
        "form": form,
         "title": "Edytuj dane" 
         }
    return render(request, "form_template.html", context)