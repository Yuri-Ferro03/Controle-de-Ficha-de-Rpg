import os
import json
import glob
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
            return tipo_obj
        if isinstance(tipo_obj, dict):
            return tipo_obj.get('type', 'unknown')
        return 'unknown'

    def extrair_tamanho_simples(self, tamanho_lista):
        """Extrai o tamanho de uma lista"""
        if isinstance(tamanho_lista, list) and len(tamanho_lista) > 0:
            return tamanho_lista[0]
        return None

    def extrair_ac_simples(self, ac_lista):
        """Extrai o AC de uma lista"""
        if isinstance(ac_lista, list) and len(ac_lista) > 0:
            if isinstance(ac_lista[0], dict):
                return ac_lista[0].get('ac', None)
            return ac_lista[0]
        return None

    def extrair_alignment(self, alignment_lista):
        """Extrai alignment de uma lista"""
        if isinstance(alignment_lista, list):
            return ', '.join(alignment_lista)
        return None

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

            # Extrair campos para filtro
            tipo = self.extrair_tipo_simples(monster.get('type', ''))
            tamanho = self.extrair_tamanho_simples(monster.get('size', []))
            cr = monster.get('cr', None)
            ac = self.extrair_ac_simples(monster.get('ac', []))
            hp_media = None
            if 'hp' in monster and isinstance(monster['hp'], dict):
                hp_media = monster['hp'].get('average', None)
            alignment = self.extrair_alignment(monster.get('alignment', []))

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
                self.stdout.write(self.style.ERROR(f'Erro ao salvar {nome}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'✓ Importados {count} monstros de {arquivo}'))
        return count

    def handle(self, *args, **options):
        if options['limpar']:
            self.stdout.write(self.style.WARNING('Limpando banco de dados...'))
            total = Monstro.objects.count()
            Monstro.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'✓ Deletados {total} monstros'))

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

        self.stdout.write(self.style.SUCCESS(f'\n✓ Total de monstros importados: {total}'))
