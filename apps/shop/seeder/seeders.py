import json
import pathlib

import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify

from apps.shop.models import Category, Product
from apps.shop.seeder.factories import CategoryFactory, ProductFactory


def generic_seeder():
    categories = CategoryFactory.create_batch(5)
    for category in categories:
        ProductFactory.create_batch(10, category=category)


def seeder():
    dir_path = pathlib.Path(__file__).parent
    products_file = dir_path / "products.json"
    products = json.load(products_file.open("r"))

    for product_data in products["products"]:
        category_name = product_data["category"].replace(" ", "-")
        category_slug = slugify(category_name)

        category, _ = Category.objects.get_or_create(
            name=category_name,
            slug=category_slug,
        )

        product_name = (
            product_data["title"] if "title" in product_data else product_data["name"]
        )

        product, _ = Product.objects.get_or_create(
            category=category,
            name=product_name,
            slug=slugify(product_name),
            description=product_data["description"],
            price=product_data["price"],
            available=True,
        )

        if not product.image and "images" in product_data:
            image_url = product_data["images"][0]
            response = requests.get(image_url)

            if response.status_code == 200:
                try:
                    image_extension = image_url.rsplit(".", 1)[1].lower()
                except IndexError as e:
                    print(image_url)
                    raise e
                image_content = ContentFile(response.content)
                product.image.save(
                    name=f"{product.slug}.{image_extension}",
                    content=image_content,
                    save=True,
                )
