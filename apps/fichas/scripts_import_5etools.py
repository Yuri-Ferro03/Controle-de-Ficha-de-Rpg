# script opcional para rodar fora do Django (ex.: cron) e popular o banco via shell or fixtures
import os, django, requests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpg_manager.settings')
django.setup()
from apps.fichas.models import Monstro
URLS = ['https://5e.tools/data/bestiary/bestiary-mm.json',]
for url in URLS:
    print('Importando', url)
    r = requests.get(url)
    data = r.json()
    count = 0
    for m in data.get('monster', []):
        Monstro.objects.update_or_create(
            nome=m.get('name', 'Unknown'),
            defaults={
                'tipo': m.get('type', ''),
                'dados_completos': m,
                'source': url,
            }
        )
        count += 1
    print(f'Importados {count} monstros de {url}')
