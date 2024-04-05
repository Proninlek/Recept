from django import template

register = template.Library()


@register.filter(name='total_minutes')
def total_minutes(value):
    """
    Пользовательский фильтр для вывода занчения времени приготовления в минутах с учетом часов
    """
    total_minutes = value.seconds // 60
    return f"{total_minutes} мин."
