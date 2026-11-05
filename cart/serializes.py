from rest_framework import serializers
from .models import Cart, CartItem
from Catalog.serializers import ProductVariantSerializer


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'items', 'item_count', 'subtotal')
    
    def get_items(self, obj):
        return CartItemSerializer(obj.items.all(), many=True).data

    def get_item_count(self, obj):
        return sum(item.quantity for item in obj.items.all())
        # return len(obj.items.all())

    def get_subtotal(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())

class CartItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_variant', 'price', 'quantity', "line_total"]  


    def get_line_total(self, obj):
        return obj.price * obj.quantity


class CartItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product_variant', 'quantity' ]


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity' ]


