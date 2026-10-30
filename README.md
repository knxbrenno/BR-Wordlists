# BR-Wordlists

Wordlists com foco no Brasil, **geradas por script** a partir de dados públicos e de padrões reais, não de vazamentos. A maioria das listas prontas (SecLists, rockyou) é em inglês e cobre mal os padrões brasileiros: times de futebol, `Senha@2024`, `mudar123`, nomes e sobrenomes comuns, caminhos como `/nfe` e `/boleto`, subdomínios como `sei.` e `nfe.`.

O repositório traz os **geradores**, as **listas-semente** e as wordlists pequenas e médias já prontas. As versões grandes você gera localmente em segundos.

## Para que serve

A finalidade principal é **defensiva**:

- **Blocklist de senhas fracas:** use `senhas_br_*.txt` para o seu sistema **recusar no cadastro** as senhas brasileiras mais previsíveis, do mesmo jeito que grandes serviços bloqueiam `123456` e `password`.
- **Auditoria da própria base:** com autorização, rode a lista contra os hashes dos seus usuários para descobrir quem usa senha fraca e orientar a troca.
- **Teste da superfície exposta:** veja se o seu site responde em `/backup.sql`, `/.env`, `/nfe`, ou se há subdomínios esquecidos (`hml.`, `antigo.`).

E, para quem faz **teste de intrusão com escopo e autorização**, serve como wordlist de reconhecimento, enumeração de usuários e fuzzing, localizada para alvos brasileiros.

> **Uso responsável.** Estas listas só devem ser usadas em sistemas que você **é dono** ou tem **autorização por escrito** para testar. Acessar sistemas de terceiros sem autorização é crime no Brasil (Lei 12.737/2012 e art. 154-A do Código Penal). O projeto é material educacional e de defesa; o uso é responsabilidade de quem o utiliza.

## De onde vêm os dados

Nada aqui vem de bases de dados vazadas. Tudo é **gerado**:

| Fonte | O que é |
|---|---|
| Dicionário / conhecimento público | palavras comuns em português, times de futebol, termos de sistemas BR |
| API de nomes do IBGE (opcional) | prenomes mais frequentes do país (estatística pública, não dado pessoal) |
| Padrões de mutação | ano, sufixos (`123`, `@2024`), *leet* (`a→@`), capitalização |

Isso é de propósito: não espalha dados pessoais de ninguém, não infringe a LGPD e é totalmente reproduzível: qualquer um audita e regenera.

## Listas geradas

| Arquivo | Conteúdo |
|---|---|
| `senhas_br_<nível>.txt` | candidatas de senha no padrão brasileiro |
| `usuarios_br.txt` | logins no padrão BR (`joao.silva`, `jsilva`, `admin`...) |
| `web_paths_br.txt` | caminhos e arquivos web comuns em sites brasileiros |
| `subdominios_br.txt` | rótulos de subdomínio comuns no Brasil |

Níveis de senha: `pequeno` (~12 mil), `medio` (~23 mil), `grande` (~110 mil) e `enorme`. As versões `grande` e `enorme` **não** ficam no git; gere-as quando precisar.

## Uso

Requer apenas Python 3 (sem dependências externas).

```bash
git clone https://github.com/knxbrenno/BR-Wordlists.git
cd BR-Wordlists

# Gera todas as listas (nível médio de senhas)
python build.py

# Só as senhas, no nível grande
python generators/passwords.py --nivel grande

# (Opcional) amplia os nomes com o ranking do IBGE antes de gerar
python generators/fetch_ibge.py --qtd 100
python build.py --nivel grande
```

As listas são sempre ordenadas da candidata **mais provável para a menos provável**, então um ataque autorizado (ou uma auditoria) encontra as senhas fracas logo no começo.

### Exemplo: bloquear senhas fracas no cadastro

```python
with open("wordlists/senhas_br_medio.txt", encoding="utf-8") as f:
    FRACAS = set(l.strip() for l in f)

def senha_aceitavel(senha):
    return senha.lower() not in FRACAS
```

## Estrutura

```
BR-Wordlists/
├── build.py              # gera todas as listas de uma vez
├── generators/
│   ├── common.py         # utilitários (leet, acentos, gravação sem duplicatas)
│   ├── passwords.py      # senhas (palavras-base + regras)
│   ├── usernames.py      # logins no padrão BR
│   ├── web_paths.py      # caminhos web
│   ├── subdomains.py     # subdomínios
│   └── fetch_ibge.py     # (opcional) amplia os nomes com o IBGE
├── seeds/                # listas-semente editáveis
├── wordlists/            # listas geradas (pequena/média versionadas)
└── tests/
```

Quer melhorar a cobertura? Edite os arquivos em `seeds/` (adicione times, gírias regionais, termos de um setor) e rode `python build.py` de novo.

## Testes

```bash
pip install pytest
python -m pytest
```

## Licença

Material educacional, distribuído como está. Use com responsabilidade e dentro da lei.
