from django.contrib import admin
from .models import NPC, Monstro

@admin.register(NPC)
class NPCAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_por', 'criado_em')
    search_fields = ('nome',)
    ordering = ('nome',)
    readonly_fields = ('criado_em',)

@admin.register(Monstro)
class MonstroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo')
    search_fields = ('nome', 'tipo')
    ordering = ('nome',)
