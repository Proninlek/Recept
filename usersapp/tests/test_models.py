from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        # Создать тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_profile_creation(self):
        # Создать профиль пользователя (тест нужно проводить на реальном файле изображения)
        profile = Profile.objects.create(user=self.user, image='path/to/test/image.jpg')

        # Проверяем, что профиль успешно создан
        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.image.name, 'path/to/test/image.jpg')

    def test_profile_image_compression(self):
        # Создаем профиль пользователя с изображением размером больше 300x300
        image_path = 'path/to/large/image.jpg'
        profile = Profile.objects.create(user=self.user, image=image_path)

        # Проверяем, что изображение было сжато
        img = profile.image.open()
        self.assertTrue(img.width <= 300)
        self.assertTrue(img.height <= 300)

    def test_profile_deletion(self):
        # Создаем профиль пользователя
        profile = Profile.objects.create(user=self.user, image='path/to/test/image.jpg')

        # Удаляем профиль и проверяем, что он успешно удален
        profile.delete()
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(user=self.user)

    def test_profile_save_with_invalid_image(self):
        # Создаем профиль пользователя с некорректным изображением
        profile = Profile.objects.create(user=self.user, image='path/to/nonimage/file.txt')

        # Проверяем, что изображение не было сжато
        img = profile.image.open()
        self.assertEqual(img.width, 0)
        self.assertEqual(img.height, 0)
