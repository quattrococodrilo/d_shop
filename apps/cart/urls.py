from django.urls import path, include
from . import views

app_name="cart"

urlpatterns = [
    path("api/v1/", include("apps.cart.api.urls")),
    path("list/", views.cart_item_list, name="cart_item_list"),
]
