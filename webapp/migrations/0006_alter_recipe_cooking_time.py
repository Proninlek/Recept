# Generated by Django 4.2.8 on 2023-12-13 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.DurationField(verbose_name='Время приготовления (чч:мм:сс)'),
        ),
    ]
