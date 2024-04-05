from django.contrib import admin
from .models import Profile

# Отображение модели Profile в админке проекта
admin.site.register(Profile)
