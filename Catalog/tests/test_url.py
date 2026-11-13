from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Catalog.views import (
    ProductListCreate,
    ProductDetail,
    CategoryListCreate,
    CategoryDetail,
    BrandListCreate,
    BrandDetail
)




class TestProductUrls(SimpleTestCase):

    def test_product_url_resolve(self):
        url = reverse('product')
        self.assertEqual(resolve(url).func.view_class, ProductListCreate)

    def test_product_detail_url_resolve(self):
        url = reverse('product_detail', args=[2])
        self.assertEqual(resolve(url).func.view_class, ProductDetail)


class TestCategoryUrls(SimpleTestCase):

    def test_category_url_resolve(self):
        url = reverse('categories')
        self.assertEqual(resolve(url).func.view_class, CategoryListCreate)

    def test_category_detail_url_resolve(self):
        url = reverse('categories_detail', args=[2])
        self.assertEqual(resolve(url).func.view_class, CategoryDetail)


class TestBrandUrls(SimpleTestCase):

    def test_brand_url_resolve(self):
        url = reverse('brands')
        self.assertEqual(resolve(url).func.view_class, BrandListCreate)

    def test_brand_detail_url_resolve(self):
        url = reverse('brands_detail', args=[2])
        self.assertEqual(resolve(url).func.view_class, BrandDetail)