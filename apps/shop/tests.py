from django.test import TestCase
from django.test.client import Client
from django.urls.base import reverse

from .seeder.factories import CategoryFactory, ProductFactory


class ProductTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = CategoryFactory.create()
        self.category_products = ProductFactory.create_batch(5, category=self.category)
        self.category_products[0].name = "Hello World"
        self.category_products[0].save()
        self.products = ProductFactory.create_batch(10)
        for product in self.products[:5]:
            product.name = "Hello World"
            product.save()

    def test_list_view(self):
        response = self.client.get(reverse("shop:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.category_products[0].name)
        self.assertEqual(len(response.context["products"].object_list), 10)

        response = self.client.get(
            reverse("shop:list"), {"category": self.category.slug}
        )
        self.assertEqual(len(response.context["products"].object_list), 5)

        response = self.client.get(reverse("shop:list"), {"q": "Hello World"})
        self.assertEqual(len(response.context["products"].object_list), 6)

        response = self.client.get(
            reverse("shop:list"),
            {
                "q": "Hello World",
                "category": self.category.slug,
            },
        )
        self.assertEqual(len(response.context["products"].object_list), 1)

    def test_detail_view(self):
        product = ProductFactory.create()

        response = self.client.get(
            reverse("shop:product_detail", kwargs={"pk": product.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shop/product/detail.html")
        self.assertContains(response, product.name)
        self.assertContains(response, product.price)
