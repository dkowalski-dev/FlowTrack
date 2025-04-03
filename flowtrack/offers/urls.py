from django.urls import path
from . import views

urlpatterns = [
    path('', views.offers, name="offers"),
    path('create-offer/', views.create_offer, name="create-offer"),
    path('create-status/', views.create_status, name="create-status"),
    path('offer/<uuid:pk>/', views.offer, name="offer"),
    path('update-status/<uuid:pk>', views.update_status, name="update-status"),
    path('statuses/', views.statuses, name="statuses"),
]