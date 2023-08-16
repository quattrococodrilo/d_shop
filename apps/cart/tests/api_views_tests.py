from django.conf import settings
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.shop.seeder.factories import ProductFactory


class AddItemToCartViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_add_item_respond_ok(self):
        product = ProductFactory.create()

        response = self.client.post(
            reverse("cart:add_item_to_cart"),
            {
                "product_id": product.id,
                "quantity": 2,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("message") == "Product added")

        session = self.client.session
        cart_content = session.get(settings.CART_SESSION_ID)
        self.assertEqual(
            cart_content,
            {str(product.id): {"quantity": 2, "price": f"{product.price}.00"}},
        )


class CartItemsViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_cart_items_respond_ok(self):
        products = ProductFactory.create_batch(5)

        response = self.client.get(
            reverse("cart:get_cart_items"),
        )
    
        for product in products:
            self.client.post(
                reverse("cart:add_item_to_cart"),
                {
                    "product_id": product.id,
                    "quantity": 2,
                },
            )


        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print(response.data)
