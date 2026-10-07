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
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes

# # Local Application / Custom Imports
    # from decorators import rate_limit_fixed_window, rate_limit_sliding_window
from Catalog.models import Product, Category, Brand
from Catalog.Utils.validation import valid_cart, valid_product
from .serializers import   CategoryWriteSerializer
from .serializers import (
    ProductListSerializer,
    ProductListSerializer,
    ProductWriteSerializer,
    CategoryTreeSerializer,
    CategoryWriteSerializer,
    CategoryDetailSerializer,
    BrandMiniSerializer,
    BrandWriteSerializer,
    BrandDetailSerializer
)


# Create your views here.

# ---------------------------------------------------------------------
# PRODUCT
# ---------------------------------------------------------------------

class ProductListCreate(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "POST":
            return [IsAdminUser()]

        return [IsAdminUser()]

    def get(self, request):

        products = Product.objects.prefetch_related("images").all()

        paginator = PageNumberPagination()

        paginator.page_size = 10

        page = paginator.paginate_queryset(products, request)

        serializer = ProductListSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):

        serializer = ProductWriteSerializer(data=request.data)

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

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "POST":
            return [IsAdminUser()]

        return [IsAdminUser()]

    def get_objects(self, request, slug):
        try:
            return Product.objects.prefetch_related("images", "category", "brand").get(slug=slug)
        except Product.DoesNotExist:
            return None

    def get(self, request, slug):
        product = self.get_objects(request, slug)

        if product is None:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductDetailSerializer(product)

        return Response(
            serializer.data,
        )

    def put(self, request, slug):
        product = self.get_objects(request, slug)

        
        if product is None:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductWriteSerializer(
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
        

    
    def delete(self, request, slug):

        product = self.get_objects(request=request, slug=slug)

        if product is None:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        product.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )



# ---------------------------------------------------------------------
# CATEGORY
# ---------------------------------------------------------------------

class CategorylistCreate(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "POST":
            return [IsAdminUser()]

        return [IsAdminUser()]


    def get(self, request):

        category = Category.objects.prefetch_related("children").all()

        paginator = PageNumberPagination()

        paginator.page_size = 10

        page = paginator.paginate_queryset(category, request)

        serializer = CategoryTreeSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


    def post(self, request):

        serializer = CategoryWriteSerializer(data=request.data)

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

class CategoryDetail(APIView):
    def get_objects(self, request, slug):
        try:
            return Category.objects.prefetch_related("parent").get(slug=slug)
        except Category.DoesNotExist:
            return None

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "POST":
            return [IsAdminUser()]

        return [IsAdminUser()]
    
    
    def get(self, request, slug):
        category = self.get_objects(request, slug)

        if category is None:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategoryDetailSerializer(category)

        return Response(
            serializer.data,
        )

    def put(self, request, slug):
        category = self.get_objects(request, slug)

        
        if category is None:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategoryWriteSerializer(
            category,
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
        

    def delete(self, request, slug):

        category = self.get_objects(request, slug)

        if category is None:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        category.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )



# ---------------------------------------------------------------------
# BRAND
# ---------------------------------------------------------------------

class BrandlistCreate(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "POST":
            return [IsAdminUser()]

        return [IsAdminUser()]

    def get(self, request):

        brand = Brand.objects.all()

        paginator = PageNumberPagination()

        paginator.page_size = 10

        page = paginator.paginate_queryset(brand, request)

        serializer = BrandMiniSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    
    def post(self, request):

        serializer = BrandWriteSerializer(data=request.data)

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

class BrandDetail(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "POST":
            return [IsAdminUser()]

        return [IsAdminUser()]

    def get_objects(self, request, slug):
        try:
            return Brand.objects.get(slug=slug)
        except Brand.DoesNotExist:
            return None
    
    def get(self, request, slug):
        brand = self.get_objects(request, slug)

        if brand is None:
            return Response(
                {"error": "Brand not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = BrandDetailSerializer(brand)

        return Response(
            serializer.data,
        )

    def put(self, request, slug):
        brand = self.get_objects(request, slug)

        
        if brand is None:
            return Response(
                {"error": "Brand not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BrandWriteSerializer(
            brand,
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
        

    def delete(self, request, slug):

        brand = self.get_objects(request, slug)

        if brand is None:
            return Response(
                {"error": "Brand not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        brand.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


