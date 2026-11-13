from rest_framework.test import APITestCase
from django.urls import reverse


import tempfile
from django.test import override_settings

from Catalog.models import Brand
from Catalog.tests.helpers import InitUsers, InitBrands, get_test_image


#--------------------------------------------------------------------------
# Testing Brand views
#--------------------------------------------------------------------------
@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class TestBrandListCreateViews(APITestCase):

    def setUp(self):
        self.user, self.admin = InitUsers()
        self.brand1, self.brand2 = InitBrands()
        self.url = reverse('brands')


    # test for get request
    def test_brand_list_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertDictEqual(response.data['results'][0], {'id': 1, 'name': 'Dell', 'slug': 'dell', 'logo': '/media/dell.png'})

    # test for post request
    def test_admin_can_create_brand_POST(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            self.url,
            data={
                'name': 'Apple',
                "description":'Best Phone, Tablets and laptops',
                'logo':get_test_image(),
                'is_active':True
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Brand.objects.count(), 3)


    def test_normal_user_cannot_create_brand_POST(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.url,
            data={
                'name': 'Apple',
                "description":'Best Phone, Tablets and laptops',
                'logo':get_test_image(),
                'is_active':True
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Brand.objects.count(), 2)


    def test_unknown_user_cannot_create_brand_POST(self):
        response = self.client.post(
            self.url,
            data={
                'name': 'Apple',
                "description":'Best Phone, Tablets and laptops',
                'logo':get_test_image(),
                'is_active':True
            },
            format='multipart',
        )

        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(Brand.objects.count(), 2)
        

class TestBrandDetailViews(APITestCase):
    
    def setUp(self):
        self.user, self.admin = InitUsers()
        brand1, brand2 = InitBrands()
        self.url = reverse('brand_detail', args=[brand1.slug])


    # test for get request
    def test_brand_detail_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {'id': 1, 'name': 'Dell', 'slug': 'dell', 'logo': '/media/dell.png', 'description': 'Best Computer and Laptop', 'is_active': True})

    
    # test for patch request
    def test_admin_can_update_brand_PATCH(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(self.url, data={'description': "World's Best Computer and Laptop"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], "World's Best Computer and Laptop")

    def test_normal_user_cannot_update_brand_PATCH(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(self.url, data={'description': "World's Best Computer and Laptop"})

        self.assertEqual(response.status_code, 403)

    def test_unknown_user_cannot_update_brand_PATCH(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(self.url, data={'description': "World's Best Computer and Laptop"})

        self.assertIn(response.status_code, [401, 403])
    

    # test for delete request
    def test_admin_can_delete_brand_DELETE(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Brand.objects.count(), 1)
    
    def test_normal_user_cannot_delete_brand_DELETE(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Brand.objects.count(), 2)

    def test_unknown_user_cannot_delete_brand_DELETE(self):
        response = self.client.delete(self.url)

        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(Brand.objects.count(), 2)
        
        



