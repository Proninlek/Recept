from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
import os
from ..models import Category, Recipe


class RecipeModelTest(TestCase):
    """
    Тестирование модели Recipe
    """

    def setUp(self):
        # Подготовка данных для тестов
        self.category = Category.objects.create(name='Test Category')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            category=self.category,
            description='Test description',
            ingredients='Test ingredients',
            cooking_steps='Test cooking steps',
            cooking_time='00:30:00',
            image='path/to/test/image.jpg',
            author=self.user,
        )

    def tearDown(self):
        # Очистка ресурсов, созданных во время теста (загруженные файлы)
        if self.recipe.image:
            image_path = os.path.join(settings.MEDIA_ROOT + f'/users_media/upload/', str(self.recipe.image))
            if os.path.exists(image_path):
                os.remove(image_path)

    def test_recipe_save_method(self):
        # Проверка, что метод save работает корректно
        self.assertEqual(Recipe.objects.count(), 1, msg='Количество рецептов в базе данных должно быть 1.')
        self.assertEqual(self.recipe.title, 'Test Recipe', msg='Название рецепта должно быть "Test Recipe".')

    def test_get_absolute_url_method(self):
        # Проверка, что метод get_absolute_url возвращает правильный URL
        expected_url = reverse('recipe-detail', args=[str(self.recipe.pk)])
        self.assertEqual(self.recipe.get_absolute_url(), expected_url, msg='Неправильный URL для get_absolute_url.')

    def test_str_representation(self):
        # Проверка, что метод __str__ возвращает правильное строковое представление объекта
        self.assertEqual(str(self.recipe), 'Test Recipe', msg='Неправильное строковое представление объекта.')

    def test_invalid_recipe_creation(self):
        # Попытка создания рецепта без обязательных полей
        recipe = Recipe()  # Создаем объект рецепта без обязательных полей
        with self.assertRaises(ValidationError,
                               msg='Создание рецепта без обязательных полей должно вызывать ValidationError.'):
            recipe.full_clean()  # Вызываем full_clean() для явной валидации

    def test_recipe_delete_method(self):
        # Проверка, что метод delete работает корректно
        self.recipe.delete()
        self.assertEqual(Recipe.objects.count(), 0, msg='Метод delete не удаляет рецепт.')

    def test_delete_recipe_with_image(self):
        # Проверка, что удаление рецепта также удаляет связанные изображения
        recipe_id = self.recipe.id
        self.recipe.delete()
        with self.assertRaises(Recipe.DoesNotExist, msg='Рецепт не удаляется из базы данных после delete.'):
            Recipe.objects.get(pk=recipe_id)

        image_path = os.path.join(settings.MEDIA_ROOT, f'users_media/upload/user_{self.user.id}/{self.recipe.image}')
        self.assertFalse(os.path.exists(image_path), msg='Файл изображения не удаляется после удаления рецепта.')
