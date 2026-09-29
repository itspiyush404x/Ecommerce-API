# Standard Library Imports
import json
import os

# Third-Party Library Imports (Django)
from django.views.decorators.csrf import csrf_exempt

# Third-Party Library Imports (Django REST Framework)
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

# # Local Application / Custom Imports
    # from decorators import rate_limit_fixed_window, rate_limit_sliding_window
from Catalog.models import Product
from Catalog.Utils.validation import valid_cart, valid_product
from .serializers import ProductSerializer


# Create your views here.
class ProductListCreate(APIView):
    def get(self, request):

        products = Product.objects.all()

        paginator = PageNumberPagination()

        paginator.page_size = 2

        page = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    
    def post(self, request):

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errorss,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProductDetail(APIView):
    def get_objects(self, request, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_objects(request, pk)

        if product is None:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product)

        return Response(
            serializer.data,
        )

    def put(self, request, pk):
        product = self.get_objects(request, pk)

        
        if product is None:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(
            product,
            data=request.data,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        

    def delete(self, request, pk):

        product = self.get_object(pk)

        if product is None:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        product.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


