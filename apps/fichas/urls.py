from django.urls import include, path
from . import views

app_name = 'fichas'

urlpatterns = [
    path('', views.home, name='home'),
    path('npcs/', views.lista_npcs, name='lista_npcs'),
    path('npcs/<int:id>/', views.detalhe_npc, name='detalhe_npc'),
    path('npcs/criar/', views.criar_npc, name='criar_npc'),
    path('npcs/<int:id>/editar/', views.editar_npc, name='editar_npc'),
    path('npcs/<int:id>/deletar/', views.deletar_npc, name='deletar_npc'),
    path('monstros/', views.lista_monstros, name='lista_monstros'),
    path('monstros/<int:id>/', views.detalhe_monstro, name='detalhe_monstro'),
    path('monstros/criar/', views.criar_monstro, name='criar_monstro'),
    path('monstros/<int:id>/editar/', views.editar_monstro, name='editar_monstro'),
    path('monstros/<int:id>/deletar/', views.deletar_monstro, name='deletar_monstro'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/<str:username>/', views.perfil_usuario, name='perfil_usuario'),
    path('iniciativa/', views.iniciativa_list, name='iniciativa_list'),
    path('iniciativa/criar/', views.iniciativa_create, name='iniciativa_create'),
    path('iniciativa/<int:session_id>/', views.iniciativa_detail, name='iniciativa_detail'),
    path('iniciativa/<int:session_id>/adicionar/', views.iniciativa_add_participant, name='iniciativa_add_participant'),
    path('iniciativa/<int:session_id>/proximo/', views.iniciativa_next, name='iniciativa_next'),
    path('iniciativa/<int:session_id>/anterior/', views.iniciativa_prev, name='iniciativa_prev'),
    # rotas simples do tracker (session-based, usadas no offcanvas)
    path('iniciativa/adicionar/', views.iniciativa_simple_add, name='iniciativa_simple_add'),
    path('iniciativa/remover/', views.iniciativa_simple_remove, name='iniciativa_simple_remove'),
    path('iniciativa/proximo/', views.iniciativa_simple_next, name='iniciativa_simple_next'),
    path('iniciativa/anterior/', views.iniciativa_simple_prev, name='iniciativa_simple_prev'),
    path('iniciativa/limpar/', views.iniciativa_simple_clear, name='iniciativa_simple_clear'),
]
