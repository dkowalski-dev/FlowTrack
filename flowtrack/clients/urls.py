from clients import views
from django.urls import path

urlpatterns = [
    path("browse/<str:client_type>/", views.clients, name="clients"),
    path(
        "update-client/<str:pk>/<str:client_type>",
        views.update_client,
        name="update-client",
    ),
    path("new-client/<str:client_type>", views.create_client, name="create-client"),
]
