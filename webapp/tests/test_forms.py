from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..forms import RecipeForm

"""
Тест роверяет, что форма считается допустимой (валидной), если ей предоставлены корректные данные, и недопустимой, 
если ей предоставлены некорректные данные
"""


class RecipeFormTest(TestCase):
    def test_valid_form(self):
        # Создаем изображение для теста
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

        # Подготавливаем данные для формы
        form_data = {
            'title': 'Test Recipe',
            'category': 1,
            'description': 'Test description',
            'ingredients': 'Test ingredients',
            'cooking_steps': 'Test cooking steps',
            'cooking_time': '01:00:00',
            'active': True,
        }

        # Для успешного теста при создании рецепта нужно добавлять путь к реальному файлу, так как поле image
        # обязательное, изображение проходит дополнительные проверки перед сохранением)
        form = RecipeForm(data=form_data, files={'image': image})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Подготавливаем некорректные данные для формы (пропущено обязательное поле)
        form_data = {
            'title': 'Test Recipe',
            'category': 1,
            'description': 'Test description',
            'ingredients': 'Test ingredients',
            'cooking_steps': 'Test cooking steps',
            'cooking_time': '01:00:00',
            'active': True,
            # Пропущено изображение, которое обязательно
        }

        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['image'], ['Обязательное поле.'])
