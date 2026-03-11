import os
import json
import glob
import re
from django.core.management.base import BaseCommand
from apps.fichas.models import Monstro


class Command(BaseCommand):
    help = 'Importa monstros do 5etools JSON para o banco de dados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--caminho',
            type=str,
            default=r'5etools-mirror-3 5etools-src main data/bestiary',
            help='Caminho para a pasta bestiary'
        )
        parser.add_argument(
            '--arquivo',
            type=str,
            help='Importar apenas um arquivo específico'
        )
        parser.add_argument(
            '--limpar',
            action='store_true',
            help='Limpar monstros antes de importar'
        )

    def extrair_tipo_simples(self, tipo_obj):
        """Extrai o tipo simples de um objeto tipo complexo"""
        if isinstance(tipo_obj, str):
            return tipo_obj.lower()
        if isinstance(tipo_obj, dict):
            tipo = tipo_obj.get('type', 'unknown')
            return tipo.lower() if isinstance(tipo, str) else 'unknown'
        return 'unknown'

    def extrair_tamanho_simples(self, tamanho_lista):
        """Extrai o tamanho de uma lista e converte a letra em nome"""
        size_map = {
            'T': 'Tiny',
            'S': 'Small',
            'M': 'Medium',
            'L': 'Large',
            'H': 'Huge',
            'G': 'Gargantuan',
        }
        if isinstance(tamanho_lista, list) and len(tamanho_lista) > 0:
            raw = tamanho_lista[0]
            if isinstance(raw, str) and raw.upper() in size_map:
                return size_map[raw.upper()]
            return raw
        return None

    def extrair_ac_simples(self, ac_lista):
        """Extrai o AC de uma lista"""
        if isinstance(ac_lista, list) and len(ac_lista) > 0:
            if isinstance(ac_lista[0], dict):
                return ac_lista[0].get('ac', None)
            return ac_lista[0]
        return None

    def extrair_alignment(self, alignment_lista):
        """Extrai alignment de uma lista e converte códigos em palavras"""
        def expand_alignment(s):
            mapping = {
                'l': 'Lawful',
                'n': 'Neutral',
                'c': 'Chaotic',
                'g': 'Good',
                'e': 'Evil',
                'u': 'Unaligned',
            }
            # substitui cada letra por palavra seguida de espaço
            def rep(m):
                return mapping.get(m.group(0), '') + ' '
            res = re.sub(r'[lcngeu]', rep, str(s).lower())
            # remover espaços extras e capitalizar corretamente
            return ' '.join(res.split()).title()
        
        if not alignment_lista:
            return None
        
        if isinstance(alignment_lista, list):
            alignment_strs = []
            for item in alignment_lista:
                if isinstance(item, dict):
                    alignment_strs.append(expand_alignment(item.get('alignment', '')))
                elif isinstance(item, list):
                    alignment_strs.append(expand_alignment(','.join(str(x) for x in item)))
                else:
                    alignment_strs.append(expand_alignment(item))
            return ', '.join(alignment_strs) if alignment_strs else None
        return expand_alignment(alignment_lista) if alignment_lista else None

    def limpar_tags_5etools(self, texto):
        """Remove e processa tags de markup do 5etools"""
        if not isinstance(texto, str):
            return texto
        
        # Padrão para encontrar tags {@ ... }
        # Exemplos: {@atkm}, {@hit 19}, {@damage 4d12 + 10}, {@h}, etc
        
        def processar_tag(match):
            tag_completa = match.group(0)
            # Remove chaves e @ para processar
            conteudo = tag_completa[2:-1]  # Remove {@ e }
            
            # Extrai primeiro o tipo (antes do espaço) e o valor restante
            if ' ' in conteudo:
                partes = conteudo.split(' ', 1)
                tipo = partes[0]
                valor = partes[1].strip() if len(partes) > 1 else ''
            else:
                tipo = conteudo
                valor = ''

            # Se o valor contiver '|', há texto alternativo.
            # Para {@spell Nome|Fonte} queremos o nome; para outros tags,
            # o texto visível costuma ser o último elemento.
            if '|' in valor:
                partes = valor.split('|')
                if tipo == 'spell':
                    valor = partes[0].strip()
                else:
                    valor = partes[-1].strip()
            
            # Mapeamento de tipos de tags
            if tipo == 'h':
                return ''  # {@h} é apenas um marcador, remove
            elif tipo == 'atk':
                # aceitar variantes como: 'mw', 'rw', 'm', 'r', 'm/r', 'm,rw', etc.
                # o valor pode incluir bônus, ex. "m +19" ou "r +7"; separamos o primeiro
                # token para mapear e mantemos o resto (como o bônus) intacto.
                v = valor.lower().strip()
                if not v:
                    return ''
                # separar por vírgula ou barra
                parts = [p.strip() for p in re.split(r'[,/]', v) if p.strip()]
                mapped = []
                for p in parts:
                    # p pode ser algo como 'm +19' ou 'mw +12 +1' etc.
                    tokens = p.split()
                    core = tokens[0]
                    rest = ' '.join(tokens[1:]) if len(tokens) > 1 else ''
                    if core in ('mw', 'm'):
                        phrase = 'Melee Weapon Attack'
                    elif core in ('rw', 'r'):
                        phrase = 'Ranged Weapon Attack'
                    elif core in ('ms',):
                        phrase = 'Melee Spell Attack'
                    elif core in ('rs',):
                        phrase = 'Ranged Spell Attack'
                    elif core == 'mwc':
                        phrase = 'Melee or Ranged Weapon Attack'
                    else:
                        # fallback para palavras mais longas ou não reconhecidas
                        if core == 'melee':
                            phrase = 'Melee Weapon Attack'
                        elif core == 'ranged':
                            phrase = 'Ranged Weapon Attack'
                        else:
                            phrase = core
                    if rest:
                        phrase = f"{phrase} {rest}"
                    mapped.append(phrase)
                # Unir sem duplicatas preservando ordem
                seen = set()
                uniq = [x for x in mapped if not (x in seen or seen.add(x))]
                return ' / '.join(uniq)
            elif tipo == 'dc':
                return f'DC {valor}'
            elif tipo == 'hit':
                return f'+{valor}'
            elif tipo == 'damage':
                return valor
            elif tipo == 'atkm':
                return 'Melee Weapon Attack'
            elif tipo == 'recharge':
                return f'(Recharge {valor})'
            elif tipo == 'condition':
                return valor
            elif tipo == 'actSave':
                return f'DC {valor}'
            elif tipo == 'actSaveSuccess':
                return 'Half damage only'
            elif tipo == 'actSaveFail':
                return 'Half damage only'
            else:
                return valor if valor else ''
        
        # Encontra e substitui todos os tags {@...}
        # Regex melhorada para capturar mais tipos de tags
        texto_limpo = re.sub(r'\{@[a-zA-Z]+\s*[^}]*\}', processar_tag, texto)

        # expandir marcadores curtos m/r antes de bônus de ataque (após limpar tags)
        def expand_short_atk(match):
            tag = match.group(1).lower()
            if tag in ('m',):
                return 'Melee Attack '
            if tag in ('r',):
                return 'Ranged Attack '
            if tag in ('ms',):
                return 'Melee Spell Attack '
            if tag in ('rs',):
                return 'Ranged Spell Attack '
            if tag in ('m,r','r,m','m/r','r/m'):
                return 'Melee Attack / Ranged Attack '
            if tag in ('ms,rs','rs,ms','ms/rs','rs/ms'):
                return 'Melee Spell Attack / Ranged Spell Attack '
            return match.group(0)

        texto_limpo = re.sub(
            r"\b(m,r|r,m|m/r|r/m|ms,rs|rs,ms|ms/rs|rs/ms|m|r|ms|rs)\b(?=\s*\+\d)",
            expand_short_atk,
            texto_limpo
        )
        return texto_limpo

    def limpar_dados_recursivo(self, dados):
        """Limpa tags 5etools recursivamente em dicts e listas"""
        if isinstance(dados, dict):
            return {k: self.limpar_dados_recursivo(v) for k, v in dados.items()}
        elif isinstance(dados, list):
            return [self.limpar_dados_recursivo(item) for item in dados]
        elif isinstance(dados, str):
            return self.limpar_tags_5etools(dados)
        else:
            return dados

    def importar_monstros_de_arquivo(self, arquivo):
        """Importa monstros de um arquivo JSON"""
        self.stdout.write(f'Importando de {arquivo}...')

        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler {arquivo}: {e}'))
            return 0

        count = 0
        for monster in data.get('monster', []):
            nome = monster.get('name', 'Unknown')
            
            # Extrair tipo
            tipo_raw = monster.get('type', '')
            tipo = self.extrair_tipo_simples(tipo_raw)
            
            # FILTRAR: Excluir NPCs
            if tipo == 'npc':
                continue

            # Extrair campos para filtro
            tamanho = self.extrair_tamanho_simples(monster.get('size', []))
            cr = monster.get('cr', None)
            ac = self.extrair_ac_simples(monster.get('ac', []))
            hp_media = None
            if 'hp' in monster and isinstance(monster['hp'], dict):
                hp_media = monster['hp'].get('average', None)
            alignment = self.extrair_alignment(monster.get('alignment', []))

            # Extrair nome do livro/fonte
            source_abrev = monster.get('source', 'Unknown')
            # se tivermos apenas a sigla, acrescentar o nome completo
            source_map = {
                'PHB': "Player's Handbook",
                'DMG': "Dungeon Master's Guide",
                'MM': "Monster Manual",
                'SCAG': "Sword Coast Adventurer's Guide",
                'TCE': "Tasha's Cauldron of Everything",
                'VGtM': "Volo's Guide to Monsters",
                'XGE': "Xanathar's Guide to Everything",
                'MOT': "Mythic Odysseys of Theros",
                'EEPC': "Eberron: Rising from the Last War",
                'RMBZ': "Icewind Dale: Rime of the Frostmaiden",
                'FTOA': "Fizban's Treasury of Dragons",
                'STK': "Strixhaven: A Curriculum of Chaos",
                'UA': "Unearthed Arcana",
                'SKT': "Storm King's Thunder",
                'XMM': "Monster Manual",
                'LoX': "Light of Xaryxis",
                'BAM': "Boo's Astral Menagerie",
                'XPHB': "Player's Handbook (XPHB)",
                'PaBTSO': "Phandelver and Below: The Shattered Obelisk",
                # adicione outras siglas necessárias aqui
            }
            if isinstance(source_abrev, str):
                key = source_abrev.strip()
                if key in source_map:
                    source_abrev = f"{source_map[key]} ({key})"

            try:
                cleaned = self.limpar_dados_recursivo(monster)
                # certos campos podem vir como número em vez de lista;
                # transforme em lista de descrição para evitar erros de
                # template. Especialmente legendaryActionsLair aparece como
                # inteiro em alguns monstros ("Lich" etc.).
                if 'legendaryActionsLair' in cleaned:
                    val = cleaned['legendaryActionsLair']
                    if isinstance(val, int):
                        # não existem descrições detalhadas, apenas o número
                        cleaned['legendaryActionsLair'] = [
                            f"{val} lair actions"
                        ]
                    elif not isinstance(val, list):
                        # caso improvável, mas garanta iterável
                        cleaned['legendaryActionsLair'] = [val]

                Monstro.objects.update_or_create(
                    nome=nome,
                    defaults={
                        'tipo': tipo,
                        'tamanho': tamanho,
                        'cr': str(cr) if cr else None,
                        'ac': ac,
                        'hp_media': hp_media,
                        'alignment': alignment,
                        'dados_completos': cleaned,
                        'source': source_abrev,
                    }
                )
                count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao salvar {nome}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'[OK] Importados {count} monstros de {arquivo}'))
        return count

    def handle(self, *args, **options):
        if options['limpar']:
            self.stdout.write(self.style.WARNING('Limpando banco de dados...'))
            total = Monstro.objects.count()
            Monstro.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'[OK] Deletados {total} monstros'))

        caminho = options['caminho']
        total = 0

        if options['arquivo']:
            # Importar arquivo específico
            arquivo = options['arquivo']
            if os.path.isfile(arquivo):
                total = self.importar_monstros_de_arquivo(arquivo)
            else:
                self.stdout.write(self.style.ERROR(f'Arquivo não encontrado: {arquivo}'))
        else:
            # Importar todos os bestiary-*.json
            arquivos_bestiary = glob.glob(os.path.join(caminho, 'bestiary-*.json'))
            self.stdout.write(f'Encontrados {len(arquivos_bestiary)} arquivos de bestiary')

            for arquivo in sorted(arquivos_bestiary):
                total += self.importar_monstros_de_arquivo(arquivo)

        self.stdout.write(self.style.SUCCESS(f'\n[OK] Total de monstros importados: {total}'))
