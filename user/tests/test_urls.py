from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..urls import TokenObtainPairView, TokenRefreshView
from ..views import RegisterView, LogoutView, UserDetailView, AddressListCreateView, AddressDetailView


class TestAuthUrls(SimpleTestCase):

    def test_login_url(self):
        url = reverse('token_obtain_pair')
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url(self):
        url = reverse('token_refresh')
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

class TestUserUrls(SimpleTestCase):

    def test_user_detail_url(self):
        url = reverse('user_detail')
        self.assertEqual(resolve(url).func.view_class, UserDetailView)

    def test_address_list_create_url(self):
        url = reverse('address_list_create')
        self.assertEqual(resolve(url).func.view_class, AddressListCreateView)

    def test_address_detail_url(self):
        url = reverse('address_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, AddressDetailView)









