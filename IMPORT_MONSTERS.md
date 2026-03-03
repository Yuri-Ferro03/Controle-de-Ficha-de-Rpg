# Importar Monstros do 5etools

## Passo 1: Fazer as migrations

Após atualizar o modelo, execute:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Passo 2: Importar monstros dos JSONs locais

Execute o script de importação:

```bash
python manage.py shell < apps/fichas/scripts_import_5etools.py
```

Ou use o shell do Django:

```bash
python manage.py shell
```

Depois dentro do shell:

```python
from apps.fichas.scripts_import_5etools import *
importar_monstros_de_arquivo(r"5etools-mirror-3 5etools-src main data\bestiary\bestiary-mm.json")
```

## Passo 3: Usar a API com filtros

### Filtros disponíveis:

**Listar todos os monstros:**

```
GET /api/monstros/
```

**Buscar por nome:**

```
GET /api/monstros/?search=dragon
```

**Filtrar por tipo:**

```
GET /api/monstros/?tipo=dragon
```

**Filtrar por tamanho:**

```
GET /api/monstros/?tamanho=L
```

**Filtrar por Challenge Rating (CR):**

```
GET /api/monstros/?cr=5
```

**Filtrar por intervalo de CR:**

```
GET /api/monstros/?cr_min=3&cr_max=8
```

**Filtrar por Armor Class (AC):**

```
GET /api/monstros/?ac=15
```

**Filtrar por fonte/livro:**

```
GET /api/monstros/?source=MM
```

**Combinar múltiplos filtros:**

```
GET /api/monstros/?tipo=humanoid&cr_min=1&cr_max=5&search=elf
```

**Ordenar resultados:**

```
GET /api/monstros/?ordering=cr
GET /api/monstros/?ordering=-hp_media
```

**Ver filtros disponíveis:**

```
GET /api/monstros/filtros_disponiveis/
```

## Campos do Modelo Atualizado:

- `nome`: Nome da criatura
- `tipo`: Tipo (humanoid, beast, dragon, etc)
- `tamanho`: Tamanho (T, S, M, L, H, G, C)
- `cr`: Challenge Rating (1/8, 1/4, 1/2, 1, 2, 3, etc)
- `ac`: Armor Class (inteiro)
- `hp_media`: HP médio
- `alignment`: Alinhamento
- `source`: Fonte/Livro (MM, PHB, etc)
- `dados_completos`: Todos os dados JSON originais do 5etools
- `criado_em`: Data de criação no BD

## Códigos de Tamanho:

- T = Tiny
- S = Small
- M = Medium
- L = Large
- H = Huge
- G = Gargantuan
- C = Colossal

## Códigos de Fonte (exemplos):

- MM = Monster Manual
- MM = D&D Monster Manual
- PHB = Player's Handbook
- XANATHAR = Xanathar's Guide
- etc (ver em /api/monstros/filtros_disponiveis/)
