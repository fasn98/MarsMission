# MarsMission — Missão robótica de ida e volta Terra–Marte–Terra

Estudo conceitual (nível Pré-Fase A) de uma missão **robótica** de ida e volta a Marte.
Autor: Fabio Nogueira ([@fasn98](https://github.com/fasn98)). O cenário tripulado está fora do escopo.

## Fase 1 — Mecânica orbital e orçamento de Δv

| Etapa | Conteúdo | Estado |
| :- | :- | :- |
| 1.1 | Infraestrutura, efemérides DE440 via SPICE, verificação contra o JPL Horizons | aguardando aprovação |
| 1.2 | Lambert (Izzo, 2015), porkchop plots 2028–2035, verificação contra NASA/TM-2010-216764 | não iniciada |
| 1.3 | Missões completas (classes conjunção e oposição), Δv a partir de órbitas de estacionamento | não iniciada |
| 1.4 | Orçamento de Δv com margem e primeiro dimensionamento; comparação com NASA/SP-2009-566 | não iniciada |

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
conda env create -f environment.yml      # Python 3.11 + numpy, scipy, matplotlib, pytest, spiceypy
conda activate marsmission
git config core.hooksPath .githooks      # pre-commit roda o pytest
python tools/fetch_kernels.py            # baixa DE440 (~120 MB) e naif0012.tls, confere MD5
python -m pytest
```

Sem conda: `python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt`.

## Licença

MIT — ver [`LICENSE`](LICENSE).
