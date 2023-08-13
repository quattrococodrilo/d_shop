from django.urls import path

from . import views

urlpatterns = [
    path("add-item-to-cart/", views.AddItemToCart.as_view(), name="add_item_to_cart"),
    path("get-item-cart/<int:pk>/", views.GetItemCart.as_view(), name="get_item_cart"),
]
