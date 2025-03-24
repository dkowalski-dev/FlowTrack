from django.urls import path
from . import views

urlpatterns = [
    path('browse/<str:pk>/', views.clients, name="clients"),
    path('new-client/<str:pk>', views.create_client, name="create_client"),
]