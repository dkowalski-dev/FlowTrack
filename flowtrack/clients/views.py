from django.shortcuts import render, redirect
from .models import IndividualClient, CompanyClient
from .forms import IndividualClientForm, CompanyClientForm

def clients(request, pk):
    individual_client_list = IndividualClient.objects.filter(owner=request.user) if pk in ['all', 'ind'] else []
    company_client_list = CompanyClient.objects.filter(owner=request.user) if pk  in ['all', 'com'] else []
    context = {
        "individual_client_list": individual_client_list,
        "company_client_list": company_client_list
    }
    return render(request, "clients/clients.html", context)

def create_client(request, pk):
    if pk == "ind":
        form = IndividualClientForm()
    elif pk == "com":
        form = CompanyClientForm()
    else:
        return redirect("clients", pk="all")
    context = {
        "form": form
    }
    if request.method == "POST":
        if pk == "ind":
            form = IndividualClientForm(request.POST)
        elif pk == "com":
            form = CompanyClientForm(request.POST)
        else:
            return redirect("clients", pk="all")
        if form.is_valid():
            client = form.save(commit=False)
            client.owner = request.user
            client.save()
            return redirect("clients", pk="all")
    return render(request, "clients/client_form.html", context)
