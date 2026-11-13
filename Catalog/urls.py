from django.urls import path
from . import views

urlpatterns = [
    path("products", views.ProductListCreate.as_view(), name='products'),
    path("products/<str:slug>", views.ProductDetail.as_view(), name='product_detail'),

    path("categories", views.CategoryListCreate.as_view(), name='categories'),
    path("categories/<str:slug>", views.CategoryDetail.as_view(), name='category_detail'),

    path("brands", views.BrandListCreate.as_view(), name='brands'),
    path("brands/<str:slug>", views.BrandDetail.as_view(), name='brand_detail'),
]