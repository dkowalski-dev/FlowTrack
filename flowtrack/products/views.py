from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm

def products(request):
    products = Product.objects.filter(owner=request.user)
    return render(request,"products/products.html", {"products": products})

def create_product(request):
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