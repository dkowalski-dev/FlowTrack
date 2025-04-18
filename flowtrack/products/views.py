from django.shortcuts import render, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.contrib import messages
from django.core.paginator import Paginator
from flowtrack.utils import paginObjects

def products(request):
    products = Product.objects.filter(owner=request.user)
    products, page_range = paginObjects(request, products, 10)
    context = {
        "products": products,
        "current_page": products.number,
        "page_range": page_range
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
    form = CategoryForm()
    categories = Category.objects.filter(owner=request.user)

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
    }
    return render(request, "products/categories.html", context)
    