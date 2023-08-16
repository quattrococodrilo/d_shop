from django.shortcuts import render

from apps.cart.cart import Cart


def cart_item_list(request):
    cart = Cart(request)

    return render(request, "cart/cart_item_list.html", {"cart": cart})
