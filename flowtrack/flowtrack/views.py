from django.shortcuts import redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from products.models import Product
from django.contrib import messages

def delete_object(request, model_name, object_id):
    if model_name == 'category':
        if Product.objects.filter(owner=request.user, category=object_id).first() != None:
            messages.warning(request, "Nie możesz usunąć kategorii jeżeli masz do niej przypisane produkty")
            return redirect('categories')
        
    content_type = get_object_or_404(ContentType, model=model_name)
    model = content_type.model_class()
    obj = get_object_or_404(model, id=object_id)
    obj.delete()

    last_page = request.GET.get('lastpage', 'offers')
    return redirect(last_page)