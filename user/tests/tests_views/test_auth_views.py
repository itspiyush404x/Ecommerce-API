from rest_framework.test import APITestCase
from django.urls import reverse

from user.tests.helpers import InitUsers, InitAddress
from user.models import User




class TestRegisterView(APITestCase):

    def setUp(self):
        self.url = reverse('register')
        self.user1, self.user2 = InitUsers()

        

    
    def test_create_user_POST(self):
        response = self.client.post(
            self.url,
            {
                'username':'user',
                'email':'user@gmail.com',
                'password':'pass12345',
                'phone':"9876543210"
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 3)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_cannot_create_with_existing_username_POST(self):
        response = self.client.post(
            self.url,
            {
                'username':'user1',
                'email':'user@gmail.com',
                'password':'pass12345',
                'phone':"9876543210"
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_user_cannot_create_with_existing_email_POST(self):
        response = self.client.post(
            self.url,
            {
                'username':'user',
                'email':'user1@gmail.com',
                'password':'pass12345',
                'phone':"9876543210"
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_user_cannot_create_without_password_POST(self):
        response = self.client.post(
            self.url,
            {
                'username':'user',
                'email':'user1@gmail.com',
                'phone':"9876543210"
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_password_is_hashed(self):

        self.assertEqual(self.user1.check_password(raw_password='pass12345'), True)

class TestLoginView(APITestCase):

    def setUp(self):
        self.url = reverse('token_obtain_pair')
        self.user1, self.user2 = InitUsers()

    
    def test_login_with_correct_credentials_Post(self):
        response = self.client.post(
            self.url,
            {
                'username':'user1',
                'password':'pass12345'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('refresh', response.data)
    
    def test_login_with_wrong_credentials_Post(self):
        response = self.client.post(
            self.url,
            {
                'username':'user1',
                'password':'pass444444'
            }
        )

        self.assertEqual(response.status_code, 401)
    
class TestLogoutView(APITestCase):

    def setUp(self):
        self.url = reverse('logout')
        self.user1, _ = InitUsers()
        self.login_response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'username':'user1',
                'password':'pass12345'
            }
        )
    

    def Test_logout_with_valid_refresh_token_POST(self):
        response = self.client.post(
            self.url,
            {
                'refresh':self.login_response.data['refresh']
            }
        )

        self.assertEqual(response.status_code, 205)
    
    



