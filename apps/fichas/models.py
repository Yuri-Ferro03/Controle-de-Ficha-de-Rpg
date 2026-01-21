from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class NPC(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    atributos = models.JSONField(default=dict, blank=True)
    pdf = models.FileField(upload_to='npc_pdfs/', blank=True, null=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.nome


class Monstro(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    dados_completos = models.JSONField(default=dict, blank=True)
    source = models.CharField(max_length=50, default='5etools')
    pdf = models.FileField(upload_to='monstro_pdfs/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    

class InitiativeSession(models.Model):
    nome = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    current_index = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nome} ({self.owner})"

    def participants_ordered(self):
        return self.participants.order_by('-initiative', 'created_at')

    def participant_count(self):
        return self.participants.count()


class InitiativeParticipant(models.Model):
    session = models.ForeignKey(InitiativeSession, related_name='participants', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    initiative = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-initiative', 'created_at']

    def __str__(self):
        return f"{self.name} ({self.initiative})"
    
