from django.shortcuts import render
from django.http import Http404, HttpResponseForbidden
import logging

logger = logging.getLogger(__name__)


class CustomExceptionHandlerMiddleware:
    """
    Кастомное логирование необработанных исключений и
    возврат страницы с ошибками 404, 403 и 500
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Логирование исключения
        logger.exception(f"An error occurred: {exception}")

        # Возвращаем пользователю страницу с ошибкой 500
        if isinstance(exception, Exception):
            # Передайте дополнительную информацию в контекст, если это нужно
            return render(request, 'errors/500.html', {'exception': str(exception)}, status=500)

        # Возвращаем пользователю страницу с ошибкой 404
        if isinstance(exception, Http404):
            return render(request, 'errors/404.html', status=404)

        # Возвращаем пользователю страницу с ошибкой 403 (доступ запрещен)
        if isinstance(exception, PermissionError):
            return render(request, 'errors/403.html', status=403)

        # Возвращаем None, чтобы Django продолжил обработку исключения
        return None
