import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "generators"))

import common
import passwords
import subdomains
import usernames
import web_paths


def no_duplicates(items):
    items = list(items)
    return len(items) == len(set(items))


def test_strip_accents_and_leet():
    assert common.strip_accents("ação") == "acao"
    assert common.strip_accents("José") == "Jose"
    assert common.leet_variant("senha") == "$3nh@"


def test_case_variants_are_unique():
    assert common.case_variants("abc") == ["abc", "Abc", "ABC"]
    assert no_duplicates(common.case_variants("abc"))


def test_passwords_contain_known_patterns():
    lista = set(passwords.gerar("medio"))
    for esperado in ("senha123", "flamengo2024", "Brasil@2024", "admin123", "mudar123"):
        assert esperado in lista, esperado


def test_password_levels_grow():
    tamanhos = [len(set(passwords.gerar(n))) for n in ("pequeno", "medio", "grande")]
    assert tamanhos == sorted(tamanhos)
    assert tamanhos[0] > 0


def test_passwords_have_no_accents_or_spaces():
    amostra = list(passwords.gerar("pequeno"))[:2000]
    for senha in amostra:
        assert senha == common.strip_accents(senha)
        assert " " not in senha


def test_usernames_formats():
    lista = set(usernames.generate())
    assert "maria.silva" in lista
    assert "msilva" in lista
    assert "admin" in lista


def test_write_list_deduplicates(tmp_path, monkeypatch):
    monkeypatch.setattr(common, "OUT", tmp_path)
    common.write_list("x.txt", ["a", "b", "a", "", "c", "b"])
    assert (tmp_path / "x.txt").read_text(encoding="utf-8").split() == ["a", "b", "c"]


def test_web_paths_backup_extensions():
    lista = set(web_paths.generate())
    assert "backup.sql" in lista
    assert "nfe" in lista
    assert ".env" in lista


def test_subdomains_numbered_and_environments():
    lista = set(subdomains.generate())
    assert "srv1" in lista
    assert "hml-api" in lista
    assert "sei" in lista
