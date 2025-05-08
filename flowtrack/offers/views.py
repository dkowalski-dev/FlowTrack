from django.shortcuts import render, redirect
from .models import Offer, Status, Note, OfferProduct
from products.models import Product, Category
from .forms import StatusForm, OfferForm, NoteForm, OfferProductsForm
from django.contrib import messages
from usersapp.models import UserSettings
from flowtrack.utils import paginObjects
from django.db.models import Q
from itertools import chain

def offers(request):
    settings = UserSettings.objects.get_or_create(user=request.user)[0]
    search_query = request.GET.get('search_query', '').lower()
    status_filter = request.GET.getlist('status')

    offers_query = Offer.objects.filter(owner=request.user).filter(
        Q(created__icontains=search_query)|
        Q(status__name__icontains=search_query) |
        Q(description__icontains=search_query)
    )

    offers_clients = Offer.objects.filter(owner=request.user)
    offers_clients = [
        offer for offer in offers_clients
        if search_query in offer.display_client_name.lower()
        or search_query in offer.client.get_region_display().lower()
        or search_query in offer.client.email.lower()
        or search_query in offer.client.phone
        or search_query in offer.client.address.lower()
    ]

    offers = list({offer.id: offer for offer in chain(offers_query, offers_clients)}.values())       

    if status_filter:
        offers = [
            offer for offer in offers
            if offer.status.type in status_filter
        ]
    else:
        offers = [
            offer for offer in offers
            if offer.status.type == 'ongoing'
        ]
    
    print(status_filter)

    if settings.offers_sort == "client":
        offers = sorted(offers, key = lambda offer: offer.client.company_name.lower() if hasattr(offer.client, 'company_name') else offer.client.name.lower())
    elif settings.offers_sort == "region":
        offers = sorted(offers, key = lambda offer: offer.client.region )
    else:
        sort_field = settings.offers_sort
        reverse = sort_field.startswith('-')
        sort_key = sort_field.lstrip('-')
        offers = sorted(offers, key=lambda offer: getattr(offer, sort_key), reverse=reverse)


    offers, page_range = paginObjects(request, offers, settings.offers_paginator)

    context = {
        "offers": offers,
        "settings": settings,
        "search_query": search_query,
        "page_range": page_range,
        "status": status_filter,
        }
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
    new_note_form = NoteForm()
    offer = Offer.objects.filter(owner=request.user, id=pk).first()
    products = OfferProduct.objects.filter(offer=offer)
    notes = Note.objects.filter(offer=offer.id)

    if not offer:
        return redirect('offers')
    if request.method == "POST":
        if "new_note_form" in request.POST:
            new_note_form = NoteForm(request.POST)
            if new_note_form.is_valid():
                note = new_note_form.save(commit=False)
                note.offer = offer
                note.save()
                return redirect('offer', offer.id)
        if "edit_note_form" in request.POST:
            note = Note.objects.filter(id=request.GET.get('note_id')).first()
            if note:
                edit_note_form = NoteForm(request.POST, instance=note)
                if edit_note_form.is_valid():
                    edit_note_form.save()
                    return redirect('offer', offer.id)
            else:
                messages.warning(request,"Coś poszło nie tak")
                return redirect('offer', offer.id)
            
        if "description_form" in request.POST:
            offer_form = OfferForm(request.POST, instance=offer)
            if offer_form.is_valid():
                offer_form.save()
                return redirect('offer', offer.id)
            
        if "client_form" in request.POST:
            client_form = OfferForm(request.POST, instance=offer, user=request.user)
            if client_form.is_valid():
                client_form.save()
                return redirect('offer', offer.id) 
    context = {
        "offer": offer,
        "new_note_form": new_note_form,
        "notes": notes,
        "products": products
    }
    if request.GET.get('edit') == 'description':
        context['offer_form'] = OfferForm(instance=offer)
    if request.GET.get('edit') == 'note':
        note = Note.objects.filter(id=request.GET.get('note_id')).first()
        if note:
            context['edit_note_form'] = NoteForm(instance=note)
    if request.GET.get('edit') == 'client':
        context['client_form'] = OfferForm(instance=offer, user=request.user)
    
    return render(request, "offers/offer.html", context)

def add_product_to_offer(request, pk):
    offer = Offer.objects.get(id=pk)
    settings = UserSettings.objects.get_or_create(user=request.user)[0]
    search_query = request.GET.get('search_query', '')
    category_query = request.GET.get('category_query', '')
    categories = Category.objects.filter(owner=request.user)
    offer_products = OfferProduct.objects.filter(offer=offer)

    products = Product.objects.filter(owner=request.user)
    if category_query:
        products = products.filter(category_id=category_query)
    products = products.exclude(id__in=offer_products.values_list('product_id', flat=True))
    products = products.filter(
        Q(serial_number__icontains=search_query) |
        Q(name__icontains=search_query)
        ).order_by(settings.products_sort)
    
    products, page_range = paginObjects(request, products, settings.produtcs_paginator)

    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_ids')
        products_add = Product.objects.filter(owner=request.user, id__in=selected_ids)
        offer_products = [
            OfferProduct(offer=offer, product=product, offer_price=product.sale_price)
            for product in products_add
        ]
        OfferProduct.objects.bulk_create(offer_products)
        return redirect('offer', offer.id)
    
    context = {
        "products": products,
        "offer": offer,
        "search_query": search_query,
        "category_query": category_query,
        "categories": categories,
        "page_range": page_range,
    }
    
    return render(request,"offers/add_products.html", context)

def delete_product_from_offer(request, pk, pi):
    offer = Offer.objects.filter(owner=request.user, id=pk).first()
    if offer == None: return redirect('offers')

    product = Product.objects.filter(owner=request.user, id=pi).first()
    if product == None: return redirect('offer', pk)

    OfferProduct.objects.filter(offer=offer, product=product).delete()
    return redirect('offer', offer.id)

def statuses(request):
    settings = UserSettings.objects.get_or_create(user=request.user)[0]
    search_query = request.GET.get('search_query', '')
    statuses = Status.objects.filter(owner=request.user).filter(
        Q(name__icontains=search_query)
    ).order_by(settings.statuses_sort)
    statuses, page_range = paginObjects(request, statuses, settings.statuses_paginator)

    form = StatusForm()
    if request.method == "POST":
        form = StatusForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.owner = request.user
            status.save()
            return redirect('statuses')
        
    context = {
        "search_query": search_query,
        "statuses": statuses,
        "form": form,
        "page_range": page_range
    }
    return render(request, "offers/statuses.html", context)

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