from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.fichas import views as fichas_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='fichas/', permanent=False)),
    path('admin/', admin.site.urls),
    path('fichas/', include(('apps.fichas.urls', 'fichas'), namespace='fichas')),
    path('api/', include('apps.fichas.api_urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('registro/', fichas_views.registro, name='registro'),
]

# Apenas media deve ser servido automaticamente no DEV
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
