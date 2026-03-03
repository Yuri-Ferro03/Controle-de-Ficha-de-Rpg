# script para importar monstros do 5etools localmente
import os
import json
import django
import glob

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpg_manager.settings')
django.setup()

from apps.fichas.models import Monstro

# Caminho para a pasta de bestiary
BESTIARY_PATH = r"5etools-mirror-3 5etools-src main data\bestiary"

def extrair_tipo_simples(tipo_obj):
    """Extrai o tipo simples de um objeto tipo complexo"""
    if isinstance(tipo_obj, str):
        return tipo_obj
    if isinstance(tipo_obj, dict):
        return tipo_obj.get('type', 'unknown')
    return 'unknown'

def extrair_tamanho_simples(tamanho_lista):
    """Extrai o tamanho de uma lista"""
    if isinstance(tamanho_lista, list) and len(tamanho_lista) > 0:
        return tamanho_lista[0]
    return None

def extrair_ac_simples(ac_lista):
    """Extrai o AC de uma lista"""
    if isinstance(ac_lista, list) and len(ac_lista) > 0:
        if isinstance(ac_lista[0], dict):
            return ac_lista[0].get('ac', None)
        return ac_lista[0]
    return None

def extrair_alignment(alignment_lista):
    """Extrai alignment de uma lista"""
    if isinstance(alignment_lista, list):
        return ', '.join(alignment_lista)
    return None

def importar_monstros_de_arquivo(arquivo):
    """Importa monstros de um arquivo JSON"""
    print(f'Importando de {arquivo}...')
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f'Erro ao ler {arquivo}: {e}')
        return 0
    
    count = 0
    for monster in data.get('monster', []):
        nome = monster.get('name', 'Unknown')
        
        # Extrair campos para filtro
        tipo = extrair_tipo_simples(monster.get('type', ''))
        tamanho = extrair_tamanho_simples(monster.get('size', []))
        cr = monster.get('cr', None)
        ac = extrair_ac_simples(monster.get('ac', []))
        hp_media = None
        if 'hp' in monster and isinstance(monster['hp'], dict):
            hp_media = monster['hp'].get('average', None)
        alignment = extrair_alignment(monster.get('alignment', []))
        
        # Extrair nome do livro/fonte
        source_abrev = monster.get('source', 'Unknown')
        
        try:
            Monstro.objects.update_or_create(
                nome=nome,
                defaults={
                    'tipo': tipo,
                    'tamanho': tamanho,
                    'cr': str(cr) if cr else None,
                    'ac': ac,
                    'hp_media': hp_media,
                    'alignment': alignment,
                    'dados_completos': monster,
                    'source': source_abrev,
                }
            )
            count += 1
        except Exception as e:
            print(f'Erro ao salvar {nome}: {e}')
    
    print(f'✓ Importados {count} monstros de {arquivo}')
    return count

# Importar de todos os arquivos bestiary-*.json
arquivos_bestiary = glob.glob(os.path.join(BESTIARY_PATH, 'bestiary-*.json'))
total = 0

print(f'Encontrados {len(arquivos_bestiary)} arquivos de bestiary')

for arquivo in arquivos_bestiary:
    total += importar_monstros_de_arquivo(arquivo)

print(f'\n✓ Total de monstros importados: {total}')

