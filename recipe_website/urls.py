from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usersapp import views as user_views
from webapp import views as webapp_views

handler403 = webapp_views.Error403View.as_view()
handler404 = webapp_views.Error404View.as_view()
handler500 = webapp_views.Error500View.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', user_views.CustomLoginView.as_view(), name='login'),
    path('logout/', user_views.CustomLogoutView.as_view(), name='logout'),
    path('', include('webapp.urls')),
]

# включаем возможность обработки картинок в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
