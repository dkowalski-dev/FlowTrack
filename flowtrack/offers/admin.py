from django.contrib import admin
from offers.models import Note, Offer, OfferProduct, Status

admin.site.register(Offer)
admin.site.register(Status)
admin.site.register(Note)
admin.site.register(OfferProduct)
