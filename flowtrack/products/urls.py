from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name="products"),
    path('create-product', views.create_product, name="create-product"),
    path('update-product/<uuid:pk>', views.update_product, name="update-product"),
    path('categories/', views.categories, name="categories"),
    path('update-category/<uuid:pk>', views.update_category, name="update-category"),
]
