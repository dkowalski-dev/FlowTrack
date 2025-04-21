from django.shortcuts import render, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.contrib import messages
from django.db.models import Q
from flowtrack.utils import paginObjects
from usersapp.models import UserSettings

def products(request):
    settings = UserSettings.objects.get_or_create(user=request.user)[0]
    search_query = request.GET.get('search_query', '')
    category_query = request.GET.get('category_query', '')
    categories = Category.objects.filter(owner=request.user)

    try: 
        products = Product.objects.filter(owner=request.user, category_id=category_query).filter(
        Q(serial_number__icontains=search_query) |
        Q(name__icontains=search_query)
        ).order_by(settings.products_sort)
    except: 
        products = Product.objects.filter(owner=request.user).filter(
        Q(serial_number__icontains=search_query) |
        Q(name__icontains=search_query)
        ).order_by(settings.products_sort)

    products, page_range = paginObjects(request, products, settings.produtcs_paginator)
    context = {
        "products": products,
        "page_range": page_range,
        "search_query": search_query,
        "category_query": category_query,
        "categories": categories,
    }
    return render(request,"products/products.html", context)

def create_product(request):
    if Category.objects.filter(owner=request.user).first () == None:
        messages.warning(request, "Aby dodać produkty musisz posiadać przynajmniej jedną kategorię")
        return redirect('categories')
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('products')
    context = {
        "form": form,
        "title": "Dodaj produkt",
    }
    return render(request, "form_template.html", context)

def update_product(request, pk):
    product = Product.objects.filter(id=pk, owner=request.user).first()
    if product == None: return redirect('products') 
    form = ProductForm(instance=product, user=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('products')
    context = {
        "form": form,
        "title": "Edytuj produkt",
    }
    return render(request, "form_template.html", context)

def categories(request):
    settings = UserSettings.objects.get_or_create(user=request.user)[0]
    form = CategoryForm()
    search_query = request.GET.get('search_query', '')
    categories = Category.objects.filter(owner=request.user, name__icontains=search_query).order_by(settings.categories_sort)
    categories, page_range = paginObjects(request, categories, settings.categories_paginator)

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.owner = request.user
            category.save()
            return redirect('categories')
        
    context = {
        "form": form,
        "categories": categories,
        "search_query": search_query,
        "page_range": page_range
    }
    return render(request, "products/categories.html", context)
    
def update_category(request, pk):
    category = Category.objects.filter(owner=request.user, id=pk).first()
    if category == None:
        return redirect('categories')
    form = CategoryForm(instance=category)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    
    return render(request, "form_template.html", {"form": form, "title": "Edytuj kategorię"})