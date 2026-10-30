"""
Gera candidatas de senha no padrão brasileiro a partir de palavras-base + regras.

Finalidade principal (defensiva):
  - montar uma BLOCKLIST: um sistema pode recusar no cadastro qualquer senha
    que apareça nesta lista, eliminando as senhas fracas mais previsíveis do país;
  - auditar a própria base: rodar contra os hashes dos seus usuários (com
    autorização) para descobrir quem usa senha fraca e orientar a troca.
Finalidade secundária: testes de intrusão com escopo e autorização.

NADA aqui vem de vazamentos de dados reais. Tudo é gerado a partir de
palavras públicas (dicionário, times, prenomes) combinadas com padrões.
"""
import argparse
import datetime

from common import case_variants, leet_variant, read_seed, strip_accents, write_list

ANO_ATUAL = datetime.date.today().year

# Sufixos numéricos e de pontuação mais comuns depois de uma palavra.
SUFIXOS_BASE = ["", "1", "12", "123", "1234", "12345", "123456", "!", "@", "#", "*",
                "00", "01", "10", "99", "2", "321"]

# Anos plausíveis em senha (recentes + década de nascimento comum).
def anos():
    recentes = [str(a) for a in range(ANO_ATUAL, ANO_ATUAL - 8, -1)]
    nascimento = [str(a) for a in range(1998, 1975, -1)]
    return recentes + nascimento


def sufixos(nivel):
    """Conjunto de sufixos conforme o nível de tamanho escolhido."""
    s = list(SUFIXOS_BASE)
    s += anos()
    s += [f"@{a}" for a in anos()[:8]]   # Senha@2024
    s += [f"!{a}" for a in anos()[:4]]
    if nivel in ("grande", "enorme"):
        s += [f"#{a}" for a in anos()[:8]]
        s += [f"{n:02d}" for n in range(100)]      # 00..99
        s += [f"@{n}" for n in range(10)]
    return list(dict.fromkeys(s))  # remove duplicatas preservando a ordem


def palavras_base(nivel):
    """Palavras que viram senha: comuns + times + prenomes + termos genéricos."""
    base = []
    base += read_seed("palavras_comuns.txt")
    base += read_seed("times.txt")
    base += ["senha", "senha123", "mudar", "mudar123", "123mudar", "qwerty",
             "brasil", "admin", "teste", "acesso", "trocar"]
    nomes = [strip_accents(n) for n in read_seed("nomes.txt")]
    base += nomes[: 20 if nivel == "pequeno" else 50]
    # Remove acento e normaliza; mantém a ordem (mais prováveis primeiro).
    return list(dict.fromkeys(strip_accents(p).lower() for p in base))


def gerar(nivel):
    base = palavras_base(nivel)
    sufs = sufixos(nivel)

    # Quais capitalizações/leet aplicar a cada palavra, por nível.
    if nivel == "pequeno":
        transform = lambda w: [w.lower(), w.capitalize()]
    elif nivel == "medio":
        transform = lambda w: case_variants(w)
    else:
        transform = lambda w: case_variants(w) + [leet_variant(w), leet_variant(w).capitalize()]

    for palavra in base:
        for forma in dict.fromkeys(transform(palavra)):
            for suf in sufs:
                yield forma + suf


NIVEIS = ("pequeno", "medio", "grande", "enorme")


def main():
    parser = argparse.ArgumentParser(description="Gera a wordlist de senhas no padrão BR.")
    parser.add_argument("--nivel", choices=NIVEIS, default="medio",
                        help="tamanho da lista (padrão: medio)")
    parser.add_argument("--saida", help="nome do arquivo (padrão: senhas_br_<nivel>.txt)")
    args = parser.parse_args()

    nome = args.saida or f"senhas_br_{args.nivel}.txt"
    write_list(nome, gerar(args.nivel), f"nível {args.nivel}")


if __name__ == "__main__":
    main()
