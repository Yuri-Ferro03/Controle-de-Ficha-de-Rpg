from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api_views import NPCViewSet, MonstroViewSet
router = DefaultRouter()
router.register(r'npcs', NPCViewSet, basename='npcs')
router.register(r'monstros', MonstroViewSet, basename='monstros')
urlpatterns = [
    path('', include(router.urls)),
]
