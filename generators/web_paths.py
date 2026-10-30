"""Gera a wordlist de caminhos web, acrescentando variações comuns às sementes."""
from common import read_seed, strip_accents, write_list

# Extensões usadas quando o caminho não tem uma.
EXTENSOES = ["php", "asp", "aspx", "jsp", "html"]
# Nomes de arquivo que costumam vazar e merecem várias extensões de backup.
SENSIVEIS = {"backup", "config", "configuracao", "banco", "db", "dump", "sistema"}
EXT_BACKUP = ["sql", "zip", "tar.gz", "bak", "old", "rar", "7z"]


def generate():
    base = read_seed("web_paths.txt")
    out = []
    for path in base:
        path = strip_accents(path)
        out.append(path)
        # Variante com e sem barra no fim.
        if not path.endswith("/") and "." not in path.split("/")[-1]:
            out.append(path + "/")
        # Nomes sensíveis sem extensão ganham extensões de backup.
        nome = path.split("/")[-1]
        if nome in SENSIVEIS and "." not in nome:
            out.extend(f"{path}.{ext}" for ext in EXT_BACKUP)
    return out


if __name__ == "__main__":
    write_list("web_paths_br.txt", generate(), "caminhos web comuns em sites BR")
