from django.contrib import admin
from .models import Category, Recipe

admin.site.site_title = 'Админ-панель сайта ВкуснаяЕда'
admin.site.site_header = 'Админ-панель сайта ВкуснаяЕда'

# Отображение моделей Category и Recipe в админке проекта
admin.site.register(Category)
admin.site.register(Recipe)
