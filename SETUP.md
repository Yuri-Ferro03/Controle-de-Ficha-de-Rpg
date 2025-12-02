# 📋 Guia de Setup - RPG Manager

## Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

## Instalação

### 1. Clone ou baixe o projeto
```bash
cd c:\Users\Labcrie\Downloads\rpg_manager
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual
**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente
```bash
copy .env.example .env
```
Edite o arquivo `.env` conforme necessário.

### 6. Execute as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crie um usuário administrador
```bash
python manage.py createsuperuser
```

### 8. Coleta arquivos estáticos
```bash
python manage.py collectstatic --noinput
```

### 9. Inicie o servidor de desenvolvimento
```bash
python manage.py runserver
```

Acesse em: http://localhost:8000

## URLs principais

- **Admin:** http://localhost:8000/admin/
- **Monstros:** http://localhost:8000/
- **Criar NPC:** http://localhost:8000/npc/criar/
- **Importar 5etools:** http://localhost:8000/monstros/importar/
- **API NPCs:** http://localhost:8000/api/npcs/
- **API Monstros:** http://localhost:8000/api/monstros/

## Problemas comuns

### Erro: "No module named 'django'"
**Solução:** Certifique-se de que o ambiente virtual está ativado e as dependências foram instaladas:
```bash
pip install -r requirements.txt
```

### Erro: "ModuleNotFoundError: No module named 'dotenv'"
**Solução:** Instale python-dotenv:
```bash
pip install python-dotenv
```

### Erro: "Port 8000 is already in use"
**Solução:** Use uma porta diferente:
```bash
python manage.py runserver 8001
```

## Estrutura do Projeto

```
rpg_manager/
├── apps/
│   └── fichas/
│       ├── models.py          # Modelos NPC e Monstro
│       ├── views.py           # Views web
│       ├── api_views.py       # Views da API REST
│       ├── serializers.py     # Serializers DRF
│       ├── forms.py           # Formulários Django
│       ├── admin.py           # Configuração admin
│       └── templates/
│           └── fichas/        # Templates HTML
├── rpg_manager/
│   ├── settings.py            # Configurações Django
│   ├── urls.py                # URLs principais
│   └── wsgi.py                # WSGI para produção
├── templates/                 # Templates globais (404, 500)
├── static/                    # Arquivos estáticos (gerado por collectstatic)
├── media/                     # Arquivos carregados
├── db.sqlite3                 # Banco de dados
├── manage.py                  # Gerenciador Django
├── requirements.txt           # Dependências Python
├── .env.example               # Exemplo de variáveis de ambiente
├── .gitignore                 # Arquivos a ignorar no Git
└── README.md                  # Este arquivo

## Melhorias Implementadas

✅ **Segurança:**
- [x] ALLOWED_HOSTS configurado
- [x] CSRF_TRUSTED_ORIGINS adicionado
- [x] Suporte a variáveis de ambiente
- [x] SECRET_KEY segura (precisa ser substituída em produção)

✅ **Autenticação:**
- [x] Views protegidas com @login_required
- [x] Permissões na API REST

✅ **API:**
- [x] Serializers com campos específicos
- [x] Read-only fields configurados
- [x] Permissões apropriadas

✅ **Frontend:**
- [x] Templates de erro (404, 500)
- [x] Bootstrap para UI moderna
- [x] Mensagens de feedback

✅ **DevOps:**
- [x] .gitignore criado
- [x] .env.example configurado
- [x] requirements.txt atualizado

## Próximos Passos Recomendados

1. Gerar uma SECRET_KEY segura para produção:
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. Configurar banco de dados PostgreSQL para produção

3. Implementar testes unitários

4. Configurar CI/CD (GitHub Actions, etc)

5. Deploy em produção (Heroku, AWS, DigitalOcean, etc)

## Suporte

Para mais informações sobre Django, visite: https://docs.djangoproject.com/
Para mais sobre Django REST Framework: https://www.django-rest-framework.org/
