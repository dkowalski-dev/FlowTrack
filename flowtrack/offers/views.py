from django.shortcuts import render, redirect
from .models import Offer, Status, Note
from products.models import Product
from .forms import StatusForm, OfferForm, NoteForm, OfferProductsForm
from django.contrib import messages

def offers(request):
    offers = Offer.objects.filter(owner=request.user)
    context = {"offers": offers}
    return render(request, "offers/offers.html", context)

def create_offer(request):
    if Status.objects.filter(owner=request.user).first() is None:
        messages.warning(request, "Aby utworzyć ofertę musisz dodać przynajmniej jeden status")
        return redirect('create-status')

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
    products = offer.products.all()
    notes = Note.objects.filter(offer=offer.id)

    if not offer:
        return redirect('offers')
    if request.method == "POST":
        if "note_form" in request.POST:
            print("Notatka")
            form = NoteForm(request.POST)
            if form.is_valid():
                note = form.save(commit=False)
                note.offer = offer
                note.save()
                return redirect('offer', offer.id)
        if "description_form" in request.POST:
            print("Opis")
            form = OfferForm(request.POST, instance=offer)
            if form.is_valid():
                form.save()
                return redirect('offer', offer.id)
    context = {
        "offer": offer,
        "form": form,
        "notes": notes,
        "products": products
    }
    if request.GET.get('edit') == 'description':
        context['offer_form'] = OfferForm(instance=offer)
        
    return render(request, "offers/offer.html", context)

def add_product_to_offer(request, pk):
    offer = Offer.objects.get(id=pk)
    form = OfferProductsForm(user=request.user, offer=offer)
    context = {
        "form": form,
        "title": "Zaznacz produkty które chcesz dodać",
    }
    
    if request.method == "POST":
        form = OfferProductsForm(request.POST, user=request.user, offer=offer)
        if form.is_valid():
            products = form.cleaned_data['products']
            for product in products:
                offer.products.add(product)
            return redirect('offer', pk)
    return render(request,"form_template.html", context)

def delete_product_from_offer(request, pk, pi):
    print("Przekierowuje")
    offer = Offer.objects.filter(id=pk).first()
    if offer == None: return redirect('offers')

    product = Product.objects.filter(id=pi).first()
    if product == None: return redirect('offer', pk)

    offer.products.remove(product)
    return redirect('offer', offer.id)

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