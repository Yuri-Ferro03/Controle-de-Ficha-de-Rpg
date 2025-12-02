from django.urls import include, path
from . import views

app_name = 'fichas'

urlpatterns = [
    path('', views.home, name='home'),
    path('npcs/', views.lista_npcs, name='lista_npcs'),
    path('npcs/<int:id>/', views.detalhe_npc, name='detalhe_npc'),
    path('npcs/criar/', views.criar_npc, name='criar_npc'),
    path('npcs/<int:id>/editar/', views.editar_npc, name='editar_npc'),
    path('monstros/', views.lista_monstros, name='lista_monstros'),
    path('monstros/<int:id>/', views.detalhe_monstro, name='detalhe_monstro'),
    path('monstros/criar/', views.criar_monstro, name='criar_monstro'),
]
