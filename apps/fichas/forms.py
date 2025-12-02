from django import forms
from .models import NPC, Monstro

class NPCForm(forms.ModelForm):
    class Meta:
        model = NPC
        fields = ['nome', 'descricao', 'atributos', 'pdf']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do NPC'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição...', 'rows': 4}),
            'atributos': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'JSON dos atributos (opcional)', 'rows': 4}),
            'pdf': forms.FileInput(attrs={'class': 'form-control'}),
        }

class MonstroForm(forms.ModelForm):
    class Meta:
        model = Monstro
        fields = ['nome', 'tipo', 'dados_completos', 'source', 'pdf']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Monstro'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Dragão, Goblin, etc'}),
            'dados_completos': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'JSON com dados completos (opcional)', 'rows': 6}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fonte (ex: Manual do Mestre)'}),
            'pdf': forms.FileInput(attrs={'class': 'form-control'}),
        }
