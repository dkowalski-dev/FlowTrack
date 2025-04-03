from django.shortcuts import render, redirect
from .models import Offer, Status, Note
from .forms import StatusForm, OfferForm, NoteForm

def offers(request):
    offers = Offer.objects.filter(owner=request.user)
    context = {"offers": offers}
    return render(request, "offers/offers.html", context)

def create_offer(request):
    form = OfferForm(user=request.user)

    if request.method == "POST":
        form = OfferForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('offers')

    context = {
        "form": form,
        "title": "Stwórz ofertę",
        }
    return render(request, "form_template.html", context)

def offer(request, pk):
    form = NoteForm()
    offer = Offer.objects.filter(owner=request.user, id=pk).first()
    notes = Note.objects.filter(offer=offer.id)
    if not offer:
        return redirect('offers')
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.offer = offer
            note.save()
    context = {
        "offer": offer,
        "form": form,
        "notes": notes,
    }
    return render(request, "offers/offer.html", context)

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
        
    context = {
        "form": form,
        "title": "Dodaj status"
       }
    return render(request, "form_template.html", context)

def update_status(request, pk):
    status = Status.objects.get(id=pk)
    form = StatusForm(instance=status)
    if request.method == "POST":
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('statuses')
    context = {
        "form": form,
        "title": "Edytuj status",
    }
    return render(request, "form_template.html", context)