from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.api.serializers import ItemCartSerializer
from apps.cart.cart import Cart
from apps.shop.models import Product


class AddItemToCart(APIView):
    def post(self, request):
        item_serializer = ItemCartSerializer(
            data=request.data, context={"request": request}
        )

        if item_serializer.is_valid():
            product = get_object_or_404(
                Product, id=item_serializer.validated_data.get("product_id")
            )

            item_serializer.save(product)

            return Response(
                data={"message": "Product added"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={"message": "ERROR", "errors": item_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetItemCart(APIView):
    def get(self, request, pk):
        cart = Cart(request)
        quantity = cart.cart[str(pk)]["quantity"]

        data = {
            "product_id": pk,
            "quantity": quantity,
        }
        serializer = ItemCartSerializer(data)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
