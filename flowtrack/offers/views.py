from django.shortcuts import render, redirect
from .models import Offer, Status
from .forms import StatusForm

def offers(request):
    offers = Offer.objects.filter(owner=request.user)
    context = {"offers": offers}
    return render(request, "offers/offers.html", context)

def statuses(request):
    statuses = Status.objects.filter(owner=request.user)
    context = {
        "statuses": statuses
    }
    return render(request, "offers/statuses.html", context)

def create_status(request):
    form = StatusForm()
    if request.method == "POST":
        form = StatusForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.owner = request.user
            status.save()
            return redirect('offers')
    context = {"form": form}
    return render(request, "offers/status_form.html", context)

def update_status(request, pk):
    status = Status.objects.get(id=pk)
    form = StatusForm(instance=status)
    if request.method == "POST":
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('statuses')
    context = {
        "form": form
    }
    return render(request, "offers/status_form.html", context)