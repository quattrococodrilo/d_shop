from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.cart.cart import Cart


class ItemCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)

    def save(self, product):
        cart = Cart(self.context.get("request"))
        quantity = self.validated_data["quantity"]
        cart.add(product, quantity)

    def update(self, product):
        cart = Cart(self.context.get("request"))
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

