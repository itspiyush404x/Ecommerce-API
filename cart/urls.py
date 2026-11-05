from django.urls import path
from .views import CartView, CartItemUpdateDeleteView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/', CartView.as_view(), name='cart'),
    path('cart/items/<int:pk>', CartItemUpdateDeleteView.as_view(), name='cart'),
]