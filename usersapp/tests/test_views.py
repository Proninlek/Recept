from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Profile
from webapp.models import Category


class RegisterViewTest(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)


class CustomLoginViewTest(TestCase):
    def test_custom_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)


class CustomLogoutViewTest(TestCase):
    def test_custom_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
