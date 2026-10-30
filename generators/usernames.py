"""
Gera usuários/logins no padrão brasileiro a partir de prenomes e sobrenomes.

Uso defensivo: avaliar se o padrão de login da organização é fácil de adivinhar.
Uso ofensivo: enumeração de usuários em testes autorizados.
"""
from common import read_seed, strip_accents, write_list

# Logins genéricos e de serviço que existem em quase todo lugar.
GENERICOS = [
    "admin", "administrador", "root", "suporte", "ti", "teste", "user", "usuario",
    "financeiro", "rh", "comercial", "vendas", "contato", "atendimento", "sistema",
    "gerente", "diretoria", "recepcao", "estagiario", "webmaster", "operador",
]


def formatos(nome, sobrenome):
    """Formatos de login mais usados em empresas brasileiras."""
    n, s = nome, sobrenome
    ini = n[0]
    return [
        n,
        f"{n}.{s}",
        f"{n}{s}",
        f"{n}_{s}",
        f"{ini}{s}",       # jsilva
        f"{ini}.{s}",      # j.silva
        f"{n}.{s[0]}",     # joao.s
        f"{s}.{n}",
    ]


def generate(limite_nomes=30, limite_sobrenomes=25):
    nomes = [strip_accents(n) for n in read_seed("nomes.txt")][:limite_nomes]
    sobrenomes = [strip_accents(s) for s in read_seed("sobrenomes.txt")][:limite_sobrenomes]

    out = list(GENERICOS)
    out.extend(nomes)  # só o primeiro nome também é um login comum
    for nome in nomes:
        for sobrenome in sobrenomes:
            out.extend(formatos(nome, sobrenome))
    return out


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gera a wordlist de usuários no padrão BR.")
    parser.add_argument("--nomes", type=int, default=30, help="quantos prenomes usar (padrão: 30)")
    parser.add_argument("--sobrenomes", type=int, default=25, help="quantos sobrenomes usar (padrão: 25)")
    args = parser.parse_args()

    write_list("usuarios_br.txt", generate(args.nomes, args.sobrenomes),
               f"{args.nomes} nomes x {args.sobrenomes} sobrenomes")
