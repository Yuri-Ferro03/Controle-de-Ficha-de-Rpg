import json
from django import template

register = template.Library()

@register.filter
def format_json(value):
    """Converte dicionário/JSON para string formatada"""
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return value
