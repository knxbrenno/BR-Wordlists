"""
(Opcional) Amplia seeds/nomes.txt com os prenomes mais frequentes do Brasil,
usando a API pública de nomes do IBGE (Censo). Requer internet.

    python fetch_ibge.py            # top 60 nomes nacionais
    python fetch_ibge.py --qtd 100

Os dados são estatísticas públicas de frequência de nomes, não dados pessoais.
"""
import argparse
import json
import sys
import urllib.request

from common import SEEDS, strip_accents

URL = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/ranking"


def buscar(qtd):
    req = urllib.request.Request(URL, headers={"User-Agent": "BR-Wordlists"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        dados = json.load(resp)
    nomes = [item["nome"].lower() for item in dados[0]["res"]]
    return [strip_accents(n) for n in nomes][:qtd]


def main():
    parser = argparse.ArgumentParser(description="Amplia seeds/nomes.txt com dados do IBGE.")
    parser.add_argument("--qtd", type=int, default=60, help="quantos nomes buscar (padrão: 60)")
    args = parser.parse_args()

    try:
        nomes = buscar(args.qtd)
    except OSError as err:
        print(f"Falha ao acessar a API do IBGE: {err}", file=sys.stderr)
        sys.exit(1)

    path = SEEDS / "nomes.txt"
    existentes = [l.strip() for l in path.read_text(encoding="utf-8").splitlines()
                  if l.strip() and not l.startswith("#")]
    combinados = list(dict.fromkeys(existentes + nomes))
    cabecalho = ("# Prenomes brasileiros muito comuns (semente).\n"
                 "# Ampliado com a API de nomes do IBGE (generators/fetch_ibge.py).\n")
    path.write_text(cabecalho + "\n".join(combinados) + "\n", encoding="utf-8")
    print(f"nomes.txt agora tem {len(combinados)} prenomes "
          f"({len(combinados) - len(existentes)} novos do IBGE).", file=sys.stderr)


if __name__ == "__main__":
    main()
