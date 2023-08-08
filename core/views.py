from django.shortcuts import render

from apps.shop.models import Product


def home(request):
    products = Product.objects.exclude(image="").order_by("-created")[:6]

    return render(
        request,
        "shop/index.html",
        {
            "products": products,
        },
    )
