from django.urls import path
from . import views

urlpatterns = [
    path('', views.offers, name="offers"),
]