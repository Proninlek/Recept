from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Recipe, Category


class RecipeViewsTest(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создаем категорию
        self.category = Category.objects.create(name='Test Category')

        # Создаем рецепт
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

    def test_recipe_list_view(self):
        response = self.client.get(reverse('webapp-home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe')

    def test_user_recipe_list_view(self):
        response = self.client.get(reverse('user-recipes', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe')

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipe-detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe')

    def test_recipe_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'title': 'New Recipe',
            'category': self.category.id,
            'description': 'New description',
            'ingredients': 'New ingredients',
            'cooking_steps': 'New cooking steps',
            'cooking_time': '01:00:00',
            'active': True,
            'image': 'path/to/new/image.jpg',
        }
        response = self.client.post(reverse('recipe-create'), data)
        self.assertEqual(response.status_code, 200)  # Проверка на успешное перенаправление

        # После создания рецепта, проверяем, что он существует (для корректной проверки при создании рецепта нужно
        # добавлять путь к реальному файлу, так как поле image обязательное)
        created_recipe = Recipe.objects.filter(title='New Recipe').first()
        self.assertIsNotNone(created_recipe, "Рецепт не был создан.")

    def test_recipe_update_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('recipe-update', args=[self.recipe.id]), {
            'title': 'Updated Recipe',
            'category': self.category.id,
            'description': 'Updated description',
            'ingredients': 'Updated ingredients',
            'cooking_steps': 'Updated cooking steps',
            'cooking_time': '01:30:00',
            'active': True,
            'image': 'path/to/updated/image.jpg',
        })
        self.assertEqual(response.status_code, 302)  # Проверка на успешное перенаправление
        updated_recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(updated_recipe.title, 'UPDATED RECIPE')

    def test_recipe_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('recipe-delete', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 302)  # Проверка на успешное перенаправление
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(id=self.recipe.id)

    def test_about_view(self):
        response = self.client.get(reverse('webapp-about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'О клубе любителей готовить')
