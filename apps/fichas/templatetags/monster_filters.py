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


@register.filter
def stat_modifier(value):
    """Retorna o modificador de atributo de D&D (ex: +3, -1) para um valor de habilidade."""
    try:
        val = int(value)
    except (TypeError, ValueError):
        return ""

    mod = (val - 10) // 2
    return f"+{mod}" if mod >= 0 else str(mod)

@register.filter
def get_saves(value):
    """Retorna o dict de saves (save ou saves) do dados_completos."""
    if not isinstance(value, dict):
        return None
    return value.get('save') or value.get('saves')

@register.filter
def format_lair_or_regional(value):
    """Formata ações de lair ou efeitos regionais para exibição HTML"""
    if not value:
        return ""
    
    if not isinstance(value, list):
        return str(value)
    
    result = []
    for item in value:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict):
            if item.get('type') == 'list':
                # É uma lista de itens
                items = item.get('items', [])
                for list_item in items:
                    if isinstance(list_item, str):
                        result.append(f"• {list_item}")
                    else:
                        result.append(str(list_item))
            else:
                # Outro tipo de dict, converter para string
                result.append(str(item))
    
    return '\n'.join(result)

