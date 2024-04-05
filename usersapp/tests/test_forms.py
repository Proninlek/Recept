from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from ..forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


class UserRegisterFormTest(TestCase):
    def test_valid_user_register_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_register_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'invalidemail',  # Invalid email
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserUpdateFormTest(TestCase):
    def test_valid_user_update_form(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
        form_data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
        }
        form = UserUpdateForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

    def test_invalid_user_update_form(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
        form_data = {
            'username': '',
            'email': 'updateduser@example.com',
        }
        form = UserUpdateForm(data=form_data, instance=user)
        self.assertFalse(form.is_valid())


class ProfileUpdateFormTest(TestCase):
    def test_valid_profile_update_form(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
        profile = user.profile
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        form_data = {
            'image': image,
        }
        form = ProfileUpdateForm(data=form_data, files={'image': image}, instance=profile)
        self.assertTrue(form.is_valid())

    def test_invalid_profile_update_form(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
        profile = user.profile
        form_data = {}
        form = ProfileUpdateForm(data=form_data, instance=profile)
        self.assertFalse(form.is_valid())
