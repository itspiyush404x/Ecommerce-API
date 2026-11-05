from .models import Cart, CartItem
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializes import CartSerializer, CartItemWriteSerializer, CartItemUpdateSerializer


# Create your views here.

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.prefetch_related('items').get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemWriteSerializer(data=request.data)
        if serializer.is_valid():
            cart.items.create(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class CartItemUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_objects(self, request, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return None

    def patch(self, request, pk):
        cart_item = self.get_objects(request, pk)

        if cart_item is None:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemUpdateSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart_item = self.get_objects(request, pk)

        if cart_item is None:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







    



    


   