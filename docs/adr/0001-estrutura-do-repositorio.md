# ADR 0001 — Estrutura do repositório

Status: Accepted (Fabio, 2026-10-26)
Data: 2026-10-26

## Contexto
Estudo Pré-Fase A em Python 3.11. As regras do estudo exigem separar a configuração do resultado e
proibir resultado escrito à mão. O repositório também precisa rodar no CI do GitHub Actions.

## Decisão
- Pacote `src/orbital/` (layout src), testes em `tests/` com `pythonpath = src` no pytest.
- `config/` (entrada: kernels, premissas, parâmetros), `results/` (saída só de `tools/`),
  `tools/` (scripts executáveis), `docs/` (fontes, relatórios, ADRs).
- Kernels SPICE fora do git (`data/kernels/`), baixados por `tools/fetch_kernels.py` com MD5
  fixado em `config/kernels.yaml`. No CI, ficam em cache.
- Dados de referência externos (Horizons) ficam versionados em `tests/data/` como resposta bruta
  da API, com a URL da consulta, gerados por script.
- O hook de pre-commit em `.githooks/` (ativado com `core.hooksPath`) roda o pytest. O CI roda o
  mesmo pytest em PRs e na main.
- Ambiente: `environment.yml` (conda-forge, versões fixas) é a fonte única, usada localmente e no CI
  (`conda-incubator/setup-miniconda`).

## Consequências
- Clonar e testar exige baixar ~33 MB de kernels uma vez.
- O hook depende do Python do ambiente ativo (`MARSMISSION_PYTHON` pode forçar outro).
