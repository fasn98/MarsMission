# MarsMission — Missão robótica de ida e volta Terra–Marte–Terra

Estudo conceitual (nível Pré-Fase A) de uma missão **robótica** de ida e volta a Marte.
Autor: Fabio Nogueira ([@fasn98](https://github.com/fasn98)). O cenário tripulado está fora do escopo.

## Fase 1 — Mecânica orbital e orçamento de Δv

| Etapa | Conteúdo | Estado |
| :- | :- | :- |
| 1.1 | Infraestrutura, efemérides DE440 (de440s) via SPICE, verificação contra o JPL Horizons | concluída (PR #1) |
| 1.2 | Lambert (Izzo, 2015), porkchops de ida 2028–2035 (verificação: NASA/TM-2010-216764) e de retorno 2030–2039 (verificação do método: JPL 82-43 Parte 5) | concluída (PRs #2 e #3) |
| 1.3 | Missões completas (classes conjunção e oposição), Δv a partir de órbitas de estacionamento; comparação com DRA 5.0 | missão de referência (ADR 0003) e envelope de 5,91 km/s (ADR 0004) definidos |
| 1.4 | Carga útil (CU-2), orçamento de Δv com margem, dimensionamento por estágios (regra iii) e comparação com o MSR | concluída; relatório da Fase 1 em docs/fase1_relatorio.md |

## Fase 2 — Arquitetura e dimensionamento

| Etapa | Conteúdo | Estado |
| :- | :- | :- |
| 2.1 | Arquitetura de superfície: pouso, subida (MAV) e encontro | aguardando portão |
| 2.2 | Estudo de troca do ISRU | não iniciada |
| 2.3 | Plataforma do orbitador por subsistema | não iniciada |
| 2.4 | Lançamento e DLA | não iniciada |
| 2.5 | Arquitetura integrada | não iniciada |

Modelo: cônicas emendadas, manobras impulsivas, sem perturbações. As limitações estão descritas no
relatório de cada etapa.

## Regras do estudo

1. Só física e fontes verificáveis. Toda constante cita uma fonte primária no código e em
   [`docs/fontes.md`](docs/fontes.md).
2. Valor sem fonte entra em [`config/premissas.yaml`](config/premissas.yaml) marcado **NÃO VALIDADA**.
   Só o autor altera esse status.
3. Configuração em `config/`, resultados em `results/`. Resultados são gerados só por scripts em `tools/`.
4. "Verificado" significa comparado com dados publicados. Este estudo não afirma validação.

## Estrutura

```
src/orbital/   código da mecânica orbital (pacote Python)
config/        parâmetros, kernels e premissas — entrada
results/       saída gerada por tools/ — nunca editada à mão
tools/         scripts que baixam dados e geram resultados
tests/         pytest; tests/data/ guarda respostas brutas de fontes externas
docs/          fontes, relatórios e decisões (docs/adr/)
data/kernels/  kernels SPICE baixados (fora do git)
```

## Como rodar

```bash
conda env create -f environment.yml      # versões fixas; o CI usa o mesmo arquivo
conda activate marsmission
git config core.hooksPath .githooks      # pre-commit roda o pytest
python tools/fetch_kernels.py            # baixa de440s.bsp (~33 MB) e naif0012.tls, confere MD5
python -m pytest
```

## Licença

MIT — ver [`LICENSE`](LICENSE).
