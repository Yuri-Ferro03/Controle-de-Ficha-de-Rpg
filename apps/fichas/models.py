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
    tipo = models.CharField(max_length=100, blank=True, null=True)  # humanoid, beast, dragon, etc
    tamanho = models.CharField(max_length=50, blank=True, null=True)  # T, S, M, L, H, G, C
    cr = models.CharField(max_length=10, blank=True, null=True)  # Challenge Rating (1/8, 1/4, 1, 2, etc)
    ac = models.IntegerField(blank=True, null=True)  # Armor Class
    hp_media = models.IntegerField(blank=True, null=True)  # Hit points average
    source = models.CharField(max_length=50, default='5etools')  # Which book/supplement
    alignment = models.CharField(max_length=100, blank=True, null=True)  # e.g., "Chaotic Evil"
    # Atributos básicos (para monstros criados manualmente)
    forca = models.IntegerField(blank=True, null=True)
    destreza = models.IntegerField(blank=True, null=True)
    constituicao = models.IntegerField(blank=True, null=True)
    inteligencia = models.IntegerField(blank=True, null=True)
    sabedoria = models.IntegerField(blank=True, null=True)
    carisma = models.IntegerField(blank=True, null=True)
    # Campos livres para monstros cadastrados manualmente
    caracteristicas = models.TextField(blank=True, null=True)
    habilidades = models.TextField(blank=True, null=True)
    tracos_especiais = models.TextField(blank=True, null=True)
    dados_completos = models.JSONField(default=dict, blank=True)
    pdf = models.FileField(upload_to='monstro_pdfs/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['nome']
        indexes = [
            models.Index(fields=['tipo']),
            models.Index(fields=['cr']),
            models.Index(fields=['tamanho']),
            models.Index(fields=['source']),
        ]
    
    def __str__(self):
        return f"{self.nome} (CR {self.cr})"
    

class InitiativeSession(models.Model):
    nome = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    criado_em = models.DateTimeField(auto_now_add=True)

    current_turn = models.IntegerField(default=0)
    round_number = models.IntegerField(default=1)

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
    
def next_turn(session):
    participants = list(session.participants.all())

    if not participants:
        return

    session.current_turn += 1

    if session.current_turn >= len(participants):
        session.current_turn = 0
        session.round_number += 1

    session.save()