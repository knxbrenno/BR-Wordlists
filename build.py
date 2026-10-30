"""
Gera todas as wordlists de uma vez.

    python build.py                 # nível médio de senhas + demais listas
    python build.py --nivel grande  # senhas maiores

As listas ficam em wordlists/. As muito grandes não são versionadas no git
(veja .gitignore); gere-as localmente quando precisar.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "generators"))

import passwords
import subdomains
import usernames
import web_paths
from common import write_list


def main():
    parser = argparse.ArgumentParser(description="Gera todas as wordlists.")
    parser.add_argument("--nivel", choices=passwords.NIVEIS, default="medio",
                        help="tamanho da lista de senhas (padrão: medio)")
    args = parser.parse_args()

    total = 0
    total += write_list(f"senhas_br_{args.nivel}.txt", passwords.gerar(args.nivel), f"nível {args.nivel}")
    total += write_list("usuarios_br.txt", usernames.generate(), "usuários padrão BR")
    total += write_list("web_paths_br.txt", web_paths.generate(), "caminhos web BR")
    total += write_list("subdominios_br.txt", subdomains.generate(), "subdomínios BR")
    print(f"\nTotal: {total:,} linhas geradas.".replace(",", "."))


if __name__ == "__main__":
    main()
