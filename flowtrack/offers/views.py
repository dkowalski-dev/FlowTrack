from django.shortcuts import render
from .models import Offer
def offers(request):
    offers = Offer.objects.filter(owner=request.user)
    context = {"offers": offers}
    return render(request, "offers/offers.html", context)