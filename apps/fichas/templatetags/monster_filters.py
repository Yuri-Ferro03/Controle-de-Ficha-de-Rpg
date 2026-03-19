import json
import re
from django import template

register = template.Library()


@register.filter
def clean_5etools(value):
    """Remove tags especiais do 5etools (ex: {@spell}, {@dc}, {@condition}, etc.)."""
    if not isinstance(value, str):
        return value

    # Some tags include a source after a pipe (|), like {@spell Fireball|XPHB}.
    # Prefer to keep the displayed text and discard the source.

    # Replace DC tags early to keep "DC".
    value = re.sub(r'\{@dc\s+(\d+)\}', r'DC \1', value)

    # Generic tag cleanup:
    #   {@tag Text|Source} -> Text
    #   {@tag Text}       -> Text
    #   {@tag|Source}     -> tag (e.g. {@advantage|XPHB} -> advantage)
    def _replace_tag(match):
        tag = match.group('tag')
        text = match.group('text')
        if text:
            return text
        return tag

    value = re.sub(
        r'\{@(?P<tag>[^\s|}]+)(?:\s+(?P<text>[^}|]+))?(?:\|[^}]+)?\}',
        _replace_tag,
        value,
    )

    # In some imported content, the literal token "XPHB" ends up in-place of proper terms.
    # Replace some common patterns to keep the text readable.
    value = re.sub(r"\bhalf its XPHB\b", "half its speed", value)
    value = re.sub(r"\bhas XPHB on saving throws\b", "has advantage on saving throws", value)
    value = re.sub(r"\bunimpeded by magical XPHB\b", "unimpeded by magical darkness", value)
    value = re.sub(r"\breviving with all its XPHB\b", "reviving with all its hit points", value)
    value = re.sub(r"\bthe XPHB condition\b", "the condition", value)

    # As a fallback, just remove stray XPHB tokens
    value = re.sub(r"\bXPHB\b", "", value)

    # Cleanup extra whitespace left by removals
    value = re.sub(r"\s{2,}", " ", value)
    # Remove spaces before punctuation introduced by removed tokens
    value = re.sub(r"\s+([,.;:])", r"\1", value)
    value = value.strip()

    return value


@register.filter
def clean_5etools_list(value):
    """Aplica clean_5etools para cada item em uma lista."""
    if not isinstance(value, list):
        return value

    return [clean_5etools(v) for v in value]


@register.filter
def format_json(value):
    """Converte dicionário/JSON para string formatada"""
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return value


@register.filter
def parse_blocks(value):
    """Converte texto livre em blocos {name, desc}.

    Suporta dois formatos ao digitar no campo de texto:

    1) "Nome: descrição" na mesma linha
       - Ex.: "Ataque furtivo: o monstro causa muito dano";
    2) Duas (ou mais) linhas, primeira só com o nome e as seguintes como descrição
       - Ex.:
            "Ataque furtivo"
            "O monstro causa muito dano"

    Linhas vazias são ignoradas. Vários blocos podem ser separados por
    linhas em branco ou apenas continuando o texto.
    """
    if not value:
        return []

    blocks = []
    current = None

    for raw in str(value).splitlines():
        line = raw.strip()
        if not line:
            # Linha em branco: apenas termina o parágrafo atual
            current = current  # explícito para clareza; não faz nada
            continue

        # Formato "Nome: desc" em uma linha só
        if ":" in line:
            name, desc = line.split(":", 1)
            blocks.append({"name": name.strip(), "desc": desc.strip()})
            current = None
            continue

        # Sem ":" na linha
        if current is None or current.get("desc"):
            # Começa um novo bloco apenas com o nome
            current = {"name": line, "desc": ""}
            blocks.append(current)
        else:
            # Já existe um bloco corrente sem descrição: esta linha vira/continua a descrição
            if current["desc"]:
                current["desc"] += " " + line
            else:
                current["desc"] = line

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
def spellcasting_daily_label(value):
    """Formata o rótulo de uso diário de magias"""
    if not isinstance(value, str):
        return value

    # Padrão típico do 5etools: "1e", "2e", "3e" para usos por dia.
    m = re.match(r'^(?P<num>\d+)e$', value)
    if m:
        num = int(m.group('num'))
        if num == 1:
            return '1 vez por dia'
        return f'{num} vezes por dia'

    # Preserve text already legível (ex: "Livremente")
    return value


@register.filter
def format_speed(value):
    """Formata valores de velocidade (ft.) recebidos do JSON do 5etools.

    Pode receber:
    - número (30)
    - string ("30")
    - dict com {'number': 30, 'condition': '(hover)'}
    - texto já formatado ("30 ft.")
    """
    if value is None:
        return ""

    if isinstance(value, str):
        if 'ft' in value:
            return value
        if value.isdigit():
            return f"{value} ft."
        return value

    if isinstance(value, dict):
        # Alguns monstros usam {'number': 0, ...} para velocidades 0.
        number = value.get('number')
        if number is None:
            number = value.get('value')
        if number is None:
            number = value.get('speed')
        condition = value.get('condition') or ''

        if number is None:
            return str(value)

        try:
            num = int(number)
        except (TypeError, ValueError):
            num = number

        result = f"{num} ft."
        cond = str(condition).strip()
        if cond:
            if not (cond.startswith('(') and cond.endswith(')')):
                cond = f"({cond})"
            result = f"{result} {cond}"
        return result

    if isinstance(value, (int, float)):
        return f"{value} ft."

    return str(value)


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

