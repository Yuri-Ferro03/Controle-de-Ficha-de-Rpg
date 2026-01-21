from django import forms
from .models import NPC, Monstro
from .models import InitiativeSession, InitiativeParticipant


class InitiativeSessionForm(forms.ModelForm):
    class Meta:
        model = InitiativeSession
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da sessão de iniciativa'})
        }


class InitiativeParticipantForm(forms.ModelForm):
    class Meta:
        model = InitiativeParticipant
        fields = ['name', 'initiative']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do participante'}),
            'initiative': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor de iniciativa'})
        }

class NPCForm(forms.ModelForm):
    class Meta:
        model = NPC
        fields = ['nome', 'descricao', 'pdf']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do NPC'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição...', 'rows': 4}),
            'pdf': forms.FileInput(attrs={'class': 'form-control'}),
        }

class MonstroForm(forms.ModelForm):
    class Meta:
        model = Monstro
        fields = ['nome', 'tipo', 'source', 'pdf']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Monstro'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Dragão, Goblin, etc'}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fonte (ex: Manual do Mestre)'}),
            'pdf': forms.FileInput(attrs={'class': 'form-control'}),
        }
