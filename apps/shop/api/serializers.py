from rest_framework import serializers

from apps.shop.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "name",
            "slug",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "image",
            "description",
            "price",
            "available",
            "category",
        ]
