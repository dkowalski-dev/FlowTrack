from django.urls import path
from usersapp import views

urlpatterns = [
    path("", views.index, name="index"),
    path("settings/", views.settings, name="settings"),
]
