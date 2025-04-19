from django.urls import path
from . import views

urlpatterns = [
    path('', views.offers, name="offers"),
    path('create-offer/', views.create_offer, name="create-offer"),
    path('offer/<uuid:pk>/', views.offer, name="offer"),
    path('offer-delete-product/<uuid:pk>/<uuid:pi>', views.delete_product_from_offer, name="delete-product-from-offer"),
    path('offer-add-product/<uuid:pk>', views.add_product_to_offer, name="add-product-to-offer"),
    path('update-status/<uuid:pk>', views.update_status, name="update-status"),
    path('statuses/', views.statuses, name="statuses"),
]