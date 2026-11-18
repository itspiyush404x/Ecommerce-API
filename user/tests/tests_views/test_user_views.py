from rest_framework.test import APITestCase
from django.urls import reverse

from ..helpers import InitUsers, InitAddress



class TestUserDetailViewView(APITestCase):

    def setUp(self):
        self.user1, _ = InitUsers()
        self.url = reverse("user_detail")

    # test for get request
    def test_no_login_give_401_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)

    
    def test_login_user_get_its_own_data_GET(self):
        self.client.force_authenticate(self.user1)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {'id': 1, 'username': 'user1', 'email': 'user1@gmail.com', 'phone': '1234567890'})


    # test for patch request
    def test_user_can_update_its_details_PATCH(self):
        self.client.force_authenticate(self.user1)

        response = self.client.patch(
            self.url,
            {
                'email':'user11@gmail.com',
                'phone':'5432167890'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user1.email, 'user11@gmail.com')
        self.assertEqual(self.user1.phone, '5432167890')

    def test_user_cannot_update_to_email_that_another_user_already_has_PATCH(self):
        self.client.force_authenticate(self.user1)

        response = self.client.patch(
            self.url,
            {
                'email':'user2@gmail.com',
            }
        )

        self.assertEqual(response.status_code, 400)



class TestAddressListCreateView(APITestCase):

    def setUp(self):
        self.user1, _ = InitUsers()
        self.address = InitAddress(self.user1)
        self.url = reverse('address_list_create')


    # test for get requests
    def test_no_login_give_401_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)

    def test_address_list_GET(self):
        self.client.force_authenticate(self.user1)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        # self.assertDictEqual(response.data, [{'id': 1, 'user': 1, 'name': 'Home', 'phone': '9999999999', 'address': '12 MG Road', 'city': 'Jaipur', 'state': 'Rajasthan', 'postal_code': '302001', 'country': 'India', 'is_default': False}] )
        self.assertListEqual(response.data, [{'id': 1, 'user': 1, 'name': 'Home', 'phone': '9999999999', 'address': '12 MG Road', 'city': 'Jaipur', 'state': 'Rajasthan', 'postal_code': '302001', 'country': 'India', 'is_default': False}] )

    # test for post requests
    def test_user_can_create_new_address_POST(self):
        self.client.force_authenticate(self.user1)

        response = self.client.post(
            self.url,
            {
                "name": "work",
                "phone": "9999999999",
                "address": "12 Tonk Road",
                "city": "Jaipur",
                'country':'India',
                "state":"Rajasthan",
                "postal_code": "302001",
            }
        )

        self.assertEqual(response.status_code, 201)



class TestAddressDetailView(APITestCase):

    def setUp(self):
        self.user1, self.user2 = InitUsers()
        self.address = InitAddress(self.user1)
        self.url = reverse('address_detail', args=[1])
    

    # test for get requests
    def test_no_login_give_401_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)
    
    def test_owner_can_get_own_address_GET(self):
        self.client.force_authenticate(self.user1)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {'id': 1, 'user': 1, 'name': 'Home', 'phone': '9999999999', 'address': '12 MG Road', 'city': 'Jaipur', 'state': 'Rajasthan', 'postal_code': '302001', 'country': 'India', 'is_default': False})

    def test_other_user_cannot_get_address_GET(self):
        self.client.force_authenticate(self.user2)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    
    # test for patch request
    def test_owner_can_update_own_address_PATCH(self):
        self.client.force_authenticate(self.user1)

        response = self.client.patch(
            self.url,
            {
                'phone':"1111111111"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user1.addresses.first().phone, "1111111111")

    def test_other_user_cannot_update_address_PATCH(self):
        self.client.force_authenticate(self.user2)

        response = self.client.patch(
            self.url,
            {
                'phone':"1111111111"
            }
        )

        self.assertEqual(response.status_code, 404)

    def test_address_cannot_assign_to_other_user_PATCH(self):
        self.client.force_authenticate(self.user1)

        response = self.client.patch(
            self.url,
            {
                "user":self.user2.pk
            }
        )

        self.assertEqual(self.address.user, self.user1)

    
    # tests for delete
    def test_owner_can_delete_own_address_DELETE(self):
        self.client.force_authenticate(self.user1)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.user1.addresses.all().count(), 0)
    
    def test_other_user_cannot_delete_address_DELETE(self):
        self.client.force_authenticate(self.user2)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.user1.addresses.all().count(), 1)

    

    
    

        