from rest_framework.test import APITestCase
from django.urls import reverse

from Catalog.models import Category
from Catalog.tests.helpers import InitUsers, InitCategories


#--------------------------------------------------------------------------
# Testing Category views
#--------------------------------------------------------------------------
class TestCategoryListCreateView(APITestCase):

    def setUp(self):
        self.url = reverse('categories')
        self.user, self.admin = InitUsers()
        InitCategories()


    def test_category_list_GET(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertDictEqual(response.data['results'][0], {'id': 1, 'name': 'Electronics', 'slug': 'electronics', 'children': []})
    

    def test_admin_can_create_category_POST(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            self.url,
            data={
                'name':'Cloths',
                'description':"all type of cloths",
                'parent':None,
                'is_active':True,
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 3)
    
    def test_normal_user_cannot_create_category_POST(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.url,
            data={
                'name':'Cloths',
                'description':"all type of cloths",
                'parent':None,
                'is_active':True,
            },
            format="json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Category.objects.count(), 2)

    def test_unknown_user_cannot_create_category_POST(self):
        response = self.client.post(
            self.url,
            data={
                'name':'Cloths',
                'description':"all type of cloths",
                'parent':None,
                'is_active':True,
            },
            format="json"
        )

        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(Category.objects.count(), 2) 


class TestCategoryDetailView(APITestCase):

    def setUp(self):
        cat1, cat2 = InitCategories()
        self.user, self.admin = InitUsers()

        self.url = reverse('category_detail', args=[cat1.slug])
    
    
    # test for get request
    def test_category_detail_GET(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {'id': 1,'name': 'Electronics', 'slug': 'electronics', 'description': 'All Electronic from a fan to phone', 'parent': None, 'is_active': True})
    

    # test for patch request
    def test_admin_can_update_category_PATCH(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(self.url, data={'description': 'All Electronic in best quality'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], 'All Electronic in best quality')

    def test_normal_user_cannot_update_category_PATCH(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(self.url, data={'description': 'All Electronic in best quality'})

        self.assertEqual(response.status_code, 403)

    def test_unknown_user_cannot_update_category_PATCH(self):
        response = self.client.patch(self.url, data={'description': 'All Electronic in best quality'})

        self.assertIn(response.status_code, [401, 403])
    


    # test for delete request
    def test_admin_can_delete_category_DELETE(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Category.objects.count(), 1)
    
    def test_normal_user_cannot_delete_category_DELETE(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Category.objects.count(), 2)

    def test_unknown_user_cannot_delete_category_DELETE(self):
        response = self.client.delete(self.url)

        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(Category.objects.count(), 2)
        
        




