# ADR 0010 — Painel web em Streamlit, dependências só no pyproject.toml e funções de massa em src/

Status: Accepted (Fabio, 2026-10-27, portão do painel)
Data: 2026-10-27

## Contexto
Com as Fases 1 e 2 concluídas (PR #10), o Fabio pediu um painel web acessível de qualquer lugar. O Replit é só o
ambiente de execução: ele importa o repositório do GitHub e roda, sem alteração de código lá. Até aqui:
- o ambiente vinha só do `environment.yml` (pacotes do conda-forge);
- o cálculo dos veículos e das margens estava em scripts de `tools/` (`plataformas.py`, `lancamento.py` e as
  ferramentas que eles importavam).

## Decisão
1. **Framework:** Streamlit. Os controles deslizantes recalculam com `src/` sem código de front-end.
   - A camada de dados (`src/painel/dados.py`) é Python puro e testada.
   - As figuras ficam em `src/painel/graficos.py` (Plotly) e a interface em `src/painel/app.py`.
2. **Dependências:** o `pyproject.toml` é a única lista, com versões fixas (extras `painel` e `dev`).
   - `environment.yml` só fornece o Python pelo conda e instala o pacote com `pip install -e .[dev,painel]`.
   - O Replit instala o mesmo pacote.
   - **Condição do Fabio:** regenerar todo o `results/` depois da troca conda-forge → wheels do PyPI e mostrar
     que sai idêntico (ou listar as diferenças) antes do merge; CI verde com a instalação nova.
3. **Funções de massa em `src/`:** as funções de `tools/plataformas.py` e `tools/lancamento.py` que o painel usa
   passam para `src/orbital`, junto com as que elas chamavam em outras ferramentas, sem mudança de física. `tools/`
   passa a chamar `src/`. Motivo: o Twin (Fase 8) vai reutilizá-las, e o painel não deve importar scripts. Prova:
   pytest e `results/` regenerado (`results/conferencia/regeneracao_painel.md`: 62 de 62 idênticos no ambiente pip,
   commit 310b8c3).

## Consequências
- **Módulos novos em `src/orbital`:**
  - `config` (leitura do config, parâmetros orbitais);
  - `dimensionamento` (Etapa 1.4);
  - `mav` (MAV, armazenamento e energia, Etapa 2.2);
  - `massa_plataformas` (Etapa 2.3);
  - `veiculos` (massas injetadas).
- **Ampliados:** `lancamento` (margens de injeção direta) ganhou funções.
- **Formato novo de resultado:** as grades dos porkchops em `results/painel/`, geradas por `tools/exporta_painel.py`.
- **Conferência:** `tools/confere_regeneracao.py` (PR #11) regenera todo o `results/` numa cópia e compara com o
  versionado. Para este PR: `results/conferencia/regeneracao_painel.md`.
- **Uso e publicação no Replit:** `docs/painel.md`, inclusive o que exige plano pago e a alternativa estática
  (GitHub Pages).
