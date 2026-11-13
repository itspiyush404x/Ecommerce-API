from rest_framework.test import APITestCase
from django.urls import reverse

from Catalog.models import Product
from Catalog.tests.helpers import InitProducts, InitUsers






#--------------------------------------------------------------------------
# Testing Product views
#--------------------------------------------------------------------------
class TestProductListCreateViews(APITestCase):

    def setUp(self):
        self.user, self.admin = InitUsers()
        product1, product2 = InitProducts()
        self.url = reverse('products')
        

    def test_product_list_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertDictEqual(response.data['results'][0], {'id': 1, 'name': 'Dell latidue 7390', 'slug': 'dell-latidue-7390', 'category': {'id': 1, 'name': 'Electronics', 'slug': 'electronics'}, 'brand': {'id': 1, 'name': 'Dell', 'slug': 'dell', 'logo': '/media/dell.png'}, 'base_price': '35000.00', 'discount_price': '27000.00', 'display_image': None, 'is_active': True})

    # test for post request
    def test_admin_can_create_product_POST(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            self.url,
            data={
                "name":"Dell Mouse",
                "description":"Wireless Mouse",
                "category":1,
                "brand":1,
                "base_price":700,
                "discount_price":500,
                "is_active":True,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 3)

    def test_normal_user_cannot_create_product_POST(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.url,
            data={
                "name":"Dell Mouse",
                "description":"Wireless Mouse",
                "category":1,
                "brand":1,
                "base_price":700,
                "discount_price":500,
                "is_active":True,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Product.objects.count(), 2)

    def test_unknown_user_cannot_create_product_POST(self):
        response = self.client.post(
            self.url,
            data={
                "name":"Dell Mouse",
                "description":"Wireless Mouse",
                "category":1,
                "brand":1,
                "base_price":700,
                "discount_price":500,
                "is_active":True,
            },
            format='json',
        )

        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(Product.objects.count(), 2)
        

class TestViews(APITestCase):

    def setUp(self):
        self.user, self.admin = InitUsers()
        product1, product2 = InitProducts()
        self.url = reverse('product_detail', args=[product1.slug])


    # test for get request
    def test_product_detail_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.data,
            {
                "id": 1,
                "name": "Dell latidue 7390",
                "slug": "dell-latidue-7390",
                "category": {
                    "id": 1,
                    "name": "Electronics",
                    "slug": "electronics",
                    "description": "All Electronic from a fan to phone",
                    "parent": None,
                    "is_active": True,
                },
                "brand": {
                    "id": 1,
                    "name": "Dell",
                    "slug": "dell",
                    "logo": "/media/dell.png",
                    "description": "Best Computer and Laptop",
                    "is_active": True,
                },
                "base_price": "35000.00",
                "discount_price": "27000.00",
                "images": [],
                "variants": [],
                "is_active": True,
            }
        )

    
    # test for patch request
    def test_admin_can_update_product_PATCH(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(self.url, data={'description': "Best wireless mouse"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], "Best wireless mouse")

    def test_normal_user_cannot_update_product_PATCH(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(self.url, data={'description': "Best wireless mouse"})

        self.assertEqual(response.status_code, 403)

    def test_unknown_user_cannot_update_product_PATCH(self):
        response = self.client.patch(self.url, data={'description': "Best wireless mouse"})

        self.assertIn(response.status_code, [401, 403])
       

    # test for delete request
    def test_admin_can_delete_product_DELETE(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 1)
    
    def test_normal_user_cannot_delete_product_DELETE(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Product.objects.count(), 2)

    def test_unknown_user_cannot_delete_product_DELETE(self):
        response = self.client.delete(self.url)

        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(Product.objects.count(), 2)
        
      


        






