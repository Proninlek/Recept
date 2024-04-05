from django.apps import AppConfig


class UsersappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usersapp'
    verbose_name = 'Пользователи сайта'

    # Для автоматического создания профилей при регистрации
    def ready(self):
        import usersapp.signals
