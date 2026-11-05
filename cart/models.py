from django.db import models

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(
        'user.User',
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product_variant = models.ForeignKey(
        'Catalog.ProductVariant',
        on_delete=models.CASCADE,
    
    )
    price = models.DecimalField(max_digits=30, decimal_places=2, editable=False)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} of {self.product_variant.product.name} in cart {self.cart.id}"

    def save(self, *args, **kwargs):
        # Update the price to match the product variant's price
        self.price = self.product_variant.price
        super().save(*args, **kwargs)

