from django.shortcuts import redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from urllib.parse import urlencode
from products.models import Product
from offers.models import Offer
from django.contrib import messages
from clients.models import CompanyClient, IndividualClient

def delete_object(request, model_name, object_id):
    if model_name == 'category':
        if Product.objects.filter(owner=request.user, category=object_id).first() != None:
            messages.warning(request, "Nie możesz usunąć kategorii jeżeli masz do niej przypisane produkty")
            return redirect('categories')
    
    if model_name == "status":
        if Offer.objects.filter(owner=request.user, status=object_id).first() != None:
            messages.warning(request, "Nie możesz usunąć statusu jeśli masz do niego przypisane oferty")
            return redirect('statuses')
        
    if model_name == "individualclient":
        model_class = IndividualClient
    elif model_name == "companyclient":
        model_class = CompanyClient

    if model_name == "individualclient" or model_name == "companyclient":
        user_type = ContentType.objects.get_for_model(model_class)
        print(user_type, type(user_type))
        if Offer.objects.filter(owner=request.user, client_id=object_id, client_type=user_type).first() != None:
            messages.warning(request, "Nie możesz usunąć klienta jeśli masz przypisane do niego oferty!")
            return redirect("clients", 'all')
        
    content_type = get_object_or_404(ContentType, model=model_name)
    model = content_type.model_class()
    obj = get_object_or_404(model, id=object_id)
    obj.delete()
    if model_name == "offer":
        messages.info(request, "Oferta została usunięta")
        query_string = urlencode({"status": "ongoing"})
        return redirect(f"/offers?{query_string}")
    last_page = request.GET.get('lastpage', 'offers')
    return redirect(last_page)

def delete_multiple_objects(request):
    model = request.POST.get('model')
    if model == "product":
        selected_ids = request.POST.getlist('selected_ids')
        Product.objects.filter(owner=request.user, id__in=selected_ids).delete()
        return redirect("products")
    return redirect("products")