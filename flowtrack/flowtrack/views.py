from django.shortcuts import redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType

def delete_object(request, model_name, object_id):
    content_type = get_object_or_404(ContentType, model=model_name)
    model = content_type.model_class()
    obj = get_object_or_404(model, id=object_id)
    obj.delete()

    last_page = request.GET.get('lastpage', 'offers')
    return redirect(last_page)