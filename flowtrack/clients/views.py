from django.shortcuts import render, redirect
from .models import IndividualClient, CompanyClient
from .forms import IndividualClientForm, CompanyClientForm

def clients(request, client_type):
    individual_client_list = IndividualClient.objects.filter(owner=request.user) if client_type in ['all', 'ind'] else []
    company_client_list = CompanyClient.objects.filter(owner=request.user) if client_type  in ['all', 'com'] else []
    context = {
        "individual_client_list": individual_client_list,
        "company_client_list": company_client_list
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
            form = IndividualClientForm(request.POST, isinstance=client)
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