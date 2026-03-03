# 🐉 Instalação & Uso - Lista de Monstros com Filtros

## 1️⃣ Fazer as Migrations (atualizar banco)

O modelo `Monstro` foi expandido com novos campos. Execute:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 2️⃣ Importar os Monstros do 5etools

Execute o comando para importar todos os monstros dos arquivos JSON:

```bash
python manage.py import_5etools
```

Ou para importar apenas um arquivo específico:

```bash
python manage.py import_5etools --arquivo "5etools-mirror-3 5etools-src main data/bestiary/bestiary-mm.json"
```

Para limpar e reimportar:

```bash
python manage.py import_5etools --limpar
```

## 3️⃣ Rodar o servidor

```bash
python manage.py runserver
```

## 4️⃣ Acessar a página

- **Lista de Monstros**: http://127.0.0.1:8000/monstros/
- **Detalhe do Monstro**: Clique em "Ver Ficha →" em qualquer card

---

## 🎨 O que foi implementado:

### ✅ Lista de Monstros (`/monstros/`)

- **Cards visuais** com stats principais (HP, AC, Tamanho, CR)
- **Barra de busca** por nome e tipo
- **Filtros avançados**:
  - Por Tipo (humanoid, beast, dragon, etc)
  - Por Tamanho (T, S, M, L, H, G, C)
  - Por Challenge Rating (CR)
  - Por Fonte/Livro (MM, PHB, etc)
- **Combinação de filtros** (ex: humanoid + CR 1-5)
- **Contador** de monstros encontrados

### ✅ Página de Detalhes (`/monstros/{id}/`)

- **Header** com nome, CR, tipo, tamanho e fonte
- **Stats principais** em destaque (HP, AC, CR, Tamanho)
- **Seção de Informações Básicas**
- **Atributos D&D** (STR, DEX, CON, INT, WIS, CHA)
- **Características** (Perícias, Sentidos, Idiomas, Movimento)
- **Traços Especiais** (Dive Attack, etc)
- **Ações** (Talon, Javelin, etc)
- **Dados JSON completos** em detalhes expansível

---

## 📊 Campos Exibidos:

| Campo                   | Exemplo                | Descrição                        |
| ----------------------- | ---------------------- | -------------------------------- |
| Nome                    | Aarakocra              | Nome da criatura                 |
| CR                      | 1/4                    | Challenge Rating (Desafio)       |
| HP                      | 13                     | Pontos de Vida                   |
| AC                      | 12                     | Armor Class (Classe de Armadura) |
| Tipo                    | humanoid               | Tipo da criatura                 |
| Tamanho                 | M                      | Medium (Médio)                   |
| Alinhamento             | N, G                   | Neutral Good                     |
| Fonte                   | MM                     | Monster Manual                   |
| STR/DEX/CON/INT/WIS/CHA | 10, 14, 10, 11, 12, 11 | Atributos base                   |
| Perícias                | Perception +5          | Modificadores de perícia         |
| Sentidos                | passive Perception 15  | Sentidos especiais               |
| Movimento               | Walk 20, Fly 50        | Velocidades                      |

---

## 🔍 Exemplos de Uso:

### Filtrar apenas dragões com CR 5 ou mais

1. Vá para `/monstros/`
2. Selecione Tipo: "dragon"
3. Selecione CR: "5" (ou use cr_min=5)
4. Clique em "Aplicar Filtros"

### Buscar humanoides pequenos

1. Filtro: Tipo = "humanoid"
2. Filtro: Tamanho = "Small (S)"

### Explorar um monstro completo

1. Clique em "Ver Ficha →"
2. Veja todos os stats e características
3. Expanda "Dados Completos" para JSON original

---

## 🎵 Notas Técnicas:

- **Banco de dados**: SQLite (db.sqlite3)
- **Framework**: Django 4.2+
- **API**: Suporta filtros via URL `/api/monstros/?tipo=dragon&cr=5`
- **Performance**: Índices criados em tipo, cr, tamanho, source
- **Dados**: 100%+ monstros do 5etools (MM, PHB, múltiplos suplementos)

---

## ❓ Troubleshooting

### "Nenhum monstro encontrado"

1. Verifique se rodou `python manage.py migrate`
2. Verifique se rodou `python manage.py import_5etools`
3. Verifique se os arquivos JSONs estão em `5etools-mirror-3 5etools-src main data/bestiary/`

### Filtros não funcionam

- Limpe os arquivos `.pyc` e `__pycache__` com `python manage.py clean`
- Reinicie o servidor

### Dados incompletos no detalhe

- Os dados vêm do JSON original, alguns monstros podem ter campos faltando
- Clique em "Dados Completos" para ver exatamente o que existe
