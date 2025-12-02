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
    # URLs de autenticação padrão (login/logout/password) em /accounts/
    path('accounts/', include('django.contrib.auth.urls')),
    # Login para a browsable API do DRF
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Registro de novos usuários
    path('registro/', fichas_views.registro, name='registro'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Servir arquivos estáticos em desenvolvimento
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
