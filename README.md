# RPG Manager (Django)
Projeto inicial para gerenciar fichas de NPC e monstros.
## Como rodar
1. Crie um virtualenv e ative:
```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```
2. Faça migrations e crie superuser:
```bash
python manage.py migrate
python manage.py createsuperuser
```
3. Rode o servidor:
```bash
python manage.py runserver
```
4. Acesse http://127.0.0.1:8000/ e http://127.0.0.1:8000/admin/
Endpoints da API (DRF):
- GET/POST/PUT/DELETE /api/npcs/
- GET/POST/PUT/DELETE /api/monstros/
