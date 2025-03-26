from django.urls import path
from . import views

urlpatterns = [
    path('', views.offers, name="offers"),
    path('create-status/', views.create_status, name="create-status"),
    path('update-status/<uuid:pk>', views.update_status, name="update-status"),
    path('statuses/', views.statuses, name="statuses"),
]