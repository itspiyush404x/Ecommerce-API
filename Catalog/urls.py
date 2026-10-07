from django.urls import path
from . import views

urlpatterns = [
    path("products", views.ProductListCreate.as_view()),
    path("products/<str:slug>", views.ProductDetail.as_view()),

    path("categories", views.CategorylistCreate.as_view()),
    path("categories/<str:slug>", views.CategoryDetail.as_view()),

    path("brands", views.BrandlistCreate.as_view()),
    path("brands/<str:slug>", views.BrandDetail.as_view()),
]