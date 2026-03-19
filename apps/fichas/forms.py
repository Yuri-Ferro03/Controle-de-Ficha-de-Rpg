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
        # Campos alinhados com o que é exibido na lista de monstros
        fields = [
            'nome',
            'tipo',
            'tamanho',
            'cr',
            'ac',
            'hp_media',
            'alignment',
            'forca',
            'destreza',
            'constituicao',
            'inteligencia',
            'sabedoria',
            'carisma',
            'pericias',
            'salvamentos',
            'percepcao_passiva',
            'sentidos',
            'idiomas',
            'movimento',
            'habilidades',
            'tracos_especiais',
            'source',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Monstro'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Dragão, Goblin, etc'}),
            'tamanho': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'T, S, M, L, H, G, C'}),
            'cr': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CR (ex: 1/4, 2, 5...)'}),
            'ac': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Classe de Armadura (AC)'}),
            'hp_media': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'HP médio'}),
            'alignment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alinhamento (ex: Caótico Mau)'}),
            'forca': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'FOR'}),
            'destreza': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'DES'}),
            'constituicao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'CON'}),
            'inteligencia': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'INT'}),
            'sabedoria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'SAB'}),
            'carisma': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'CAR'}),
            'pericias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Perícias (ex: Perícia +3, Furtividade +5)'}),
            'salvamentos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Testes de resistência (ex: FOR +2, DES +4)'}),
            'percepcao_passiva': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Percepção Passiva'}),
            'sentidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sentidos (ex: visão no escuro 60 pés)'}),
            'idiomas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Idiomas (ex: Comum, Dracônico)'}),
            'movimento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movimento (ex: 30 pés, voo 60 pés)'}),
            'habilidades': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Habilidades, ataques especiais, magias, etc.', 'rows': 4}),
            'tracos_especiais': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Traços especiais (como descritos no statblock).', 'rows': 4}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fonte (ex: Manual do Mestre)'}),
        }
