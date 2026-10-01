from rest_framework import serializers
from .models import Product, Category, Brand, ProductImage, ProductVariant


class CategoryMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", "name", "slug")

class BrandMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ("id", "name", "slug", "logo")

class CategorySerializer(serializers.ModelSerializer):
    parent = CategoryMiniSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent")

class BrandMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ("id", "name", "slug", "description", "logo")



class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ("id", "url", "display_order")

class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = ()


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryMiniSerializer(read_only=True)
    brand = BrandMiniSerializer(read_only=True)
    display_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "brand",
            "base_price",
            "discount_price",
            "display_image",
            "is_active",
  
        ]

    def get_display_image(self, obj):
        image = obj.images.all().order_by("display_order").first()

        if image:
            return str(image.url)

        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryMiniSerializer(read_only=True)
    brand = BrandMiniSerializer(read_only=True)
    images = ProductImageSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "brand",
            "base_price",
            "discount_price",
            "images",
            "is_active",
  
        ]