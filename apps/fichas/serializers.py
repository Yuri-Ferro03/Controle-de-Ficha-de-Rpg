from rest_framework import serializers
from .models import NPC, Monstro
class NPCSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPC
    fields = ['id', 'nome', 'descricao', 'atributos', 'pdf', 'criado_por', 'criado_em']
    read_only_fields = ['criado_por', 'criado_em', 'id']
class MonstroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monstro
        fields = ['id', 'nome', 'tipo', 'tamanho', 'cr', 'ac', 'hp_media', 'alignment', 'dados_completos', 'source', 'pdf', 'criado_em']
        read_only_fields = ['criado_em', 'id']
