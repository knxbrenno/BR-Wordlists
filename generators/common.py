"""Utilitários compartilhados pelos geradores."""
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEEDS = ROOT / "seeds"
OUT = ROOT / "wordlists"

# Substituições leet mais comuns no Brasil (uma por letra, as que as pessoas realmente usam).
LEET = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "$"}


def strip_accents(text):
    """'ação' -> 'acao'. A maioria dos sistemas não aceita acento em senha/usuário."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def read_seed(name):
    """Lê uma lista-semente (uma entrada por linha), ignorando vazias e comentários (#)."""
    path = SEEDS / name
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def leet_variant(word):
    """Aplica as substituições leet à palavra inteira (ex.: senha -> $3nh@)."""
    return "".join(LEET.get(c, c) for c in word.lower())


def case_variants(word):
    """Capitalizações que as pessoas realmente usam: toda minúscula, Primeira, TUDO."""
    seen = []
    for variant in (word.lower(), word.capitalize(), word.upper()):
        if variant not in seen:
            seen.append(variant)
    return seen


def write_list(name, items, note=""):
    """
    Grava a wordlist removendo duplicatas e preservando a ordem (mais prováveis primeiro).
    Retorna a quantidade de linhas gravadas.
    """
    OUT.mkdir(parents=True, exist_ok=True)
    seen = set()
    ordered = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            ordered.append(item)

    path = OUT / name
    path.write_text("\n".join(ordered) + "\n", encoding="utf-8")
    try:
        rotulo = path.relative_to(ROOT)
    except ValueError:
        rotulo = path
    msg = f"{rotulo}: {len(ordered):,} linhas".replace(",", ".")
    if note:
        msg += f"  ({note})"
    print(msg, file=sys.stderr)
    return len(ordered)
