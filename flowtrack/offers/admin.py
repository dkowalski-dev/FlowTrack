from django.contrib import admin
from .models import Offer, Status, Note, OfferProduct

admin.site.register(Offer)
admin.site.register(Status)
admin.site.register(Note)
admin.site.register(OfferProduct)