from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from .models import Recipe, Category
from .forms import RecipeForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
import logging

logger = logging.getLogger(__name__)


class RecipeListView(ListView):
    """
    Отображает список объектов модели Recipe
    """
    model = Recipe
    template_name = 'webapp/home.html'
    context_object_name = 'recipes'
    # Сортировка объектов по дате публикации в убывающем порядке
    ordering = ['-created_date']
    # Пагинация постов с рецептами
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        try:
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.all()
            return context
        except Exception as e:
            logger.error(f"An error occurred in RecipeListView: {str(e)}")
            raise


class UserRecipeListView(ListView):
    """
    Отображает список объектов модели Recipe конкретного пользователя
    """
    model = Recipe
    template_name = 'webapp/user_recipes.html'
    context_object_name = 'recipes'
    paginate_by = 5

    def get_queryset(self):
        try:
            user = get_object_or_404(User, username=self.kwargs.get('username'))
            return Recipe.objects.filter(author=user).order_by('-created_date')
        except Exception as e:
            logger.error(f"An error occurred in UserRecipeListView: {str(e)}")
            raise

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        try:
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.all()
            return context
        except Exception as e:
            logger.error(f"An error occurred in UserRecipeListView: {str(e)}")
            raise


class RecipeByCategoryView(ListView):
    """
    Отображает список объектов модели Recipe по ключу выбранной модели Category
    """
    model = Recipe
    template_name = 'webapp/recipes_by_category.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        try:
            category = get_object_or_404(Category, id=self.kwargs['category_id'])
            return Recipe.objects.filter(category=category)
        except Exception as e:
            logger.error(f"An error occurred in RecipeByCategoryView: {str(e)}")
            raise

    def get_context_data(self, **kwargs):
        # Добавлен обработчик переменной 'categories' для меню категорий рецептов
        try:
            context = super().get_context_data(**kwargs)
            context['category'] = get_object_or_404(Category, id=self.kwargs['category_id'])
            context['categories'] = Category.objects.all()
            return context
        except Exception as e:
            logger.error(f"An error occurred in RecipeByCategoryView: {str(e)}")
            raise


class RecipeDetailView(DetailView):
    """
    Отображение подробной информации о конкретном объекте модели Recipe
    """
    model = Recipe

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        try:
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.all()
            return context
        except Exception as e:
            logger.error(f"An error occurred in RecipeDetailView: {str(e)}")
            raise


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """
    Создание новых объектов модели Recipe,
    где автором будет текущий аутентифицированный пользователь
    """
    model = Recipe
    # Кастомный виджет формы поля
    # form_class = RecipeForm
    fields = ['title', 'category', 'description',
              'ingredients', 'cooking_steps',
              'cooking_time', 'active', 'image', ]

    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
            form.instance.title = form.cleaned_data['title'].upper()
            result = super().form_valid(form)
            messages.success(self.request, f'Рецепт успешно добавлен.')
            return result
        except Exception as e:
            logger.error(f"An error occurred in RecipeCreateView: {str(e)}")
            messages.error(self.request, f'Произошла ошибка при сохранении рецепта.')
            raise

    def form_invalid(self, form):
        try:
            return super().form_invalid(form)
        except Exception as e:
            logger.error(f"An error occurred in RecipeCreateView: {str(e)}")
            raise

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        try:
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.all()
            return context
        except Exception as e:
            logger.error(f"An error occurred in RecipeCreateView: {str(e)}")
            raise


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Обновление созданных объектов модели Recipe, при условии,
    что текущий пользователь является автором этих рецептов
    """
    model = Recipe
    fields = ['title', 'category', 'description',
              'ingredients', 'cooking_steps',
              'cooking_time', 'active', 'image', ]

    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
            form.instance.title = form.cleaned_data['title'].upper()
            result = super().form_valid(form)
            messages.success(self.request, f'Рецепт успешно изменен.')
            return result
        except Exception as e:
            logger.error(f"An error occurred in RecipeUpdateView: {str(e)}")
            raise

    def test_func(self):
        # Проверка, что авторизованный пользователь является автором рецепта
        try:
            recipe = self.get_object()
            if self.request.user == recipe.author:
                return True
            return False
        except Exception as e:
            logger.error(f"An error occurred in RecipeUpdateView: {str(e)}")
            raise

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        try:
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.all()
            return context
        except Exception as e:
            logger.error(f"An error occurred in RecipeUpdateView: {str(e)}")
            raise


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление объектов модели Recipe, при условии,
    что текущий пользователь является автором объекта
    """
    model = Recipe
    success_url = reverse_lazy('webapp-home')

    def test_func(self):
        # Проверка, что авторизованный пользователь является автором рецепта
        try:
            recipe = self.get_object()
            if self.request.user == recipe.author:
                return True
            return False
        except Exception as e:
            logger.error(f"An error occurred in RecipeDeleteView: {str(e)}")
            raise

    def delete(self, request, *args, **kwargs):
        try:
            messages.success(self.request, f'Рецепт успешно удален.')
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred in RecipeDeleteView: {str(e)}")
            messages.error(self.request, f'Произошла ошибка при удалении рецепта.')
            raise

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        try:
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.all()
            return context
        except Exception as e:
            logger.error(f"An error occurred in RecipeDeleteView: {str(e)}")
            raise


class AboutView(TemplateView):
    """
    Отображение страницы с описанием о сайте (через класс)
    """
    template_name = 'webapp/about.html'
    extra_context = {'title': 'О клубе любителей готовить'}

    def get_context_data(self, **kwargs):
        # Обработчик переменной 'categories' для меню категорий рецептов
        try:
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.all()
            return context
        except Exception as e:
            logger.error(f"An error occurred in AboutView: {str(e)}")
            raise


class Error403View(View):
    """
    Пользовательское представление ошибки 403
    """
    try:
        def get(self, request, *args, **kwargs):
            return render(request, 'errors/403.html', status=403)
    except Exception as e:
        logger.error(f"An error occurred in Error404View: {str(e)}")
        raise


class Error404View(View):
    """
    Пользовательское представление ошибки 404
    """
    try:
        def get(self, request, *args, **kwargs):
            return render(request, 'errors/404.html', status=404)
    except Exception as e:
        logger.error(f"An error occurred in Error404View: {str(e)}")
        raise


class Error500View(View):
    """
    Пользовательское представление ошибки 500
    """
    try:
        def get(self, request, *args, **kwargs):
            return render(request, 'errors/500.html', status=500)
    except Exception as e:
        logger.error(f"An error occurred in Error500View: {str(e)}")
        raise
