from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.cart.cart import Cart
from apps.shop.api.serializers import ProductSerializer
from apps.shop.models import Product


class ItemCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)

    def save(self, product):
        cart = Cart(self.context.get("request"))
        quantity = self.validated_data["quantity"]
        cart.add(product, quantity)


class CartItemsSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2) 
    # product = serializers.SerializerMethodField(method_name="get_product")
    product = ProductSerializer()

    # def get_product(self, obj):
    #     return ProductSerializer(obj.product).data
