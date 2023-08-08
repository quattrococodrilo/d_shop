from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("products/", views.product_list, name="list"),
    path("product/<int:pk>", views.product_detail, name="product_detail"),
]
