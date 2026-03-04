import json
from django import template

register = template.Library()


@register.filter
def format_json(value):
    """Converte dicionário/JSON para string formatada"""
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return value


@register.filter
def parse_blocks(value):
    """Converte texto com linhas em blocos {name, desc}.

    Cada linha é interpretada como:
        "Nome: descrição" -> name/desc separados
        "Apenas nome"     -> name, desc vazio
    """
    if not value:
        return []

    blocks = []
    for raw in str(value).splitlines():
        line = raw.strip()
        if not line:
            continue
        if ":" in line:
            name, desc = line.split(":", 1)
        else:
            name, desc = line, ""
        blocks.append({"name": name.strip(), "desc": desc.strip()})
    return blocks
