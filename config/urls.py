from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

# Add media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# i18n URL patterns
urlpatterns += i18n_patterns(
    path('', include('apps.core.urls')),
    path('cars/', include('apps.cars.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('users/', include('apps.users.urls')),
    path('analytics/', include('apps.analytics.urls')),
    prefix_default_language=False,
)

# Custom error handlers
handler404 = 'apps.core.views.error_404'
handler500 = 'apps.core.views.error_500'
