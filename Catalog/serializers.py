from rest_framework import serializers
from .models import Product, Category, Brand, ProductImage, ProductVariant

# ---------------------------------------------------------------------
# CATEGORY
# ---------------------------------------------------------------------
class CategoryMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", "name", "slug")

class CategoryDetailSerializer(CategoryMiniSerializer):
    parent = CategoryMiniSerializer(read_only=True)

    class Meta(CategoryMiniSerializer.Meta):
        fields = CategoryMiniSerializer.Meta.fields + ("description", "parent", "is_active")

class CategoryTreeSerializer(CategoryMiniSerializer):
    """Used for /categories/ (menu tree).
 
    In the view, start from top-level categories only:
        Category.objects.filter(parent__isnull=True, is_active=True)
    """
 
    children = serializers.SerializerMethodField()
 
    class Meta(CategoryMiniSerializer.Meta):
        fields = CategoryMiniSerializer.Meta.fields + ("children",)
 
    def get_children(self, obj):
        kids = obj.children.filter(is_active=True)
        return CategoryTreeSerializer(kids, many=True, context=self.context).data

class CategoryWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("name", "description", "parent", "is_active")


# ---------------------------------------------------------------------
# BRAND
# ---------------------------------------------------------------------
class BrandMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ("id", "name", "slug", "logo")

class BrandDetailSerializer(BrandMiniSerializer):

    class Meta(BrandMiniSerializer.Meta):
        model = Brand
        fields = BrandMiniSerializer.Meta.fields + ("description", "is_active")

class BrandWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ("name", "description", "logo", "is_active")





# ---------------------------------------------------------------------
# PRODUCT IMAGE
# ---------------------------------------------------------------------
class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ("id", "url", "display_order")



# ---------------------------------------------------------------------
# PRODUCT VARIANT
# ---------------------------------------------------------------------
class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = ()


# ---------------------------------------------------------------------
# PRODUCT
# ---------------------------------------------------------------------

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
    category = CategoryDetailSerializer(read_only=True)
    brand = BrandDetailSerializer(read_only=True)
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

class ProductWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "category",
            "brand",
            "base_price",
            "discount_price",
            "is_active",
  
        ]

     