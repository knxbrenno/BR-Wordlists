"""Gera a wordlist de subdomínios, acrescentando variações numeradas e por ambiente."""
from common import read_seed, strip_accents, write_list

# Rótulos que costumam aparecer numerados (srv1, ns2, host3...).
NUMERAVEIS = {"srv", "servidor", "host", "ns", "mail", "vpn", "app", "web", "db"}
# Sufixos de ambiente comuns.
AMBIENTES = ["teste", "hml", "dev", "homolog", "qa"]


def generate():
    base = [strip_accents(s) for s in read_seed("subdominios.txt")]
    out = list(base)
    for label in base:
        if label in NUMERAVEIS:
            out.extend(f"{label}{n}" for n in range(1, 6))
        # Ambientes como prefixo: dev.api, hml.portal...
        if label in ("api", "portal", "sistema", "app", "sistemas"):
            out.extend(f"{amb}-{label}" for amb in AMBIENTES)
    return out


if __name__ == "__main__":
    write_list("subdominios_br.txt", generate(), "subdomínios comuns no Brasil")
