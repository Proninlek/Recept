from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    """
    Кастомный виджет для формы поля cooking_time модели Recipe
    """

    class Meta:
        model = Recipe
        fields = ['title', 'category', 'description', 'ingredients', 'cooking_steps', 'cooking_time', 'active',
                  'image', ]
        widgets = {
            'cooking_time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }
