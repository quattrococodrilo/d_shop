from django.core.paginator import Paginator
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, render

from apps.shop.models import Category, Product


def index(request):
    return render(request, "shop/index.html")


def product_list(request):
    q = request.GET.get("q", "")
    q_category = request.GET.get("category", "")
    page = request.GET.get("page", 1)

    categories = Category.objects.all()
    products_query = Product.objects
    url_query = ""

    if q_category:
        products_query = products_query.filter(category__slug=q_category)
        url_query = f"&category={q_category}"

    if q:
        products_query = products_query.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )
        url_query += f"&q={q}"

    if not q and not q_category:
        products_query = products_query.all()

    paginator = Paginator(products_query, 10)
    products = paginator.get_page(page)

    return render(
        request,
        "shop/product/list.html",
        {
            "categories": categories,
            "products": products,
            "q": "q=" + q if q else "",
            "input_query": q,
            "q_category": "category=" + q_category if q_category else "",
            "url_query": url_query,
        },
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
        },
    )
