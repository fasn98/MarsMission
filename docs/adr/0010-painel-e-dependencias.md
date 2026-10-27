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

## Nota (2026-10-27): pillow ≥ 13.0.0 e streamlit 1.66.1
- **Decisão do Fabio:** exceção à regra de versões publicadas há mais de duas semanas (cabeçalho do `pyproject.toml`).
  - O streamlit vai de 1.65.0 para 1.66.1 (upload no PyPI em 21/10/2026).
  - Entra `pillow>=13.0.0` nas dependências obrigatórias (13.0.0: 16/10/2026).
  - A regra volta a valer na próxima atualização de dependências.
- **Motivo:** avisos de segurança "Critical" do Pillow, corrigidos na 13.0.0.
  - As notas oficiais do Pillow 13.0.0 (https://pillow.readthedocs.io/en/stable/releasenotes/13.0.0.html, seção Security) listam como "Critical" o CVE-2026-96639
    (GHSA-v9pv-5gc8-w2m6) e os GHSA-5x8w-8jj5-q52h e GHSA-8g5g-8vmr-9782, estes sem CVE nas notas.
  - Avisos do projeto no GitHub (https://github.com/python-pillow/Pillow/security/advisories/):
    - GHSA-v9pv-5gc8-w2m6: CVE-2026-96639, CVSS 9.8, afetadas ">= 11.0.0, <= 12.3.0", corrigida "13.0.0";
    - GHSA-5x8w-8jj5-q52h: CVE-2026-112398, afetadas "<= 12.3.0", corrigida "13.0.0".
  - O streamlit até a 1.66.0 exige `pillow<13`; a 1.66.1 exige `pillow<14` (metadados das wheels no PyPI).
  - Observado no workspace do Replit em 2026-10-27, sem fonte oficial do Replit: o índice de pacotes dele devolve
    HTTP 403 para o pillow de 10.4.0 a 12.3.0 ("Blocked by Security Policy. Reason: Critical CVE"), e a instalação do
    painel parava nele. A 13.0.0 passa.
- **Prova:**
  - pytest: 183 passaram e 2 foram pulados (Vallado e Curtis, já pulados antes).
  - `results/` regenerado num worktree fixo no commit 0a46b5e (`results/conferencia/regeneracao_pillow13.md`): 62
    versionados, 45 idênticos, 17 dentro da tolerância e 0 diferentes.
    - O relatório não registra a versão do pillow (`tools/confere_regeneracao.py` não a lista). O `pip` do ambiente
      mostrava pillow 13.0.0 antes da regeneração.
    - O ambiente foi o do Replit (Python 3.11.14, Xeon Platinum 8581C), não o do `environment.yml`. Com máquina e Python
      diferentes dos da conferência anterior (`regeneracao_painel.md`, 62 idênticos), não se separa o efeito do pillow
      do efeito da CPU.
  - A conferência no ambiente oficial é o workflow `regeneracao.yml` do CI (conda, Python 3.11.18), que roda porque o
    `pyproject.toml` mudou.
- O restante desta ADR continua vigente.

## Nota (2026-10-27): desenvolvimento no Replit
- **Decisão do Fabio:** o Contexto acima diz que o Replit roda o repositório "sem alteração de código lá". Isso deixa de
  valer.
- Desenvolvimento passa a ser permitido em qualquer ambiente (notebook, Claude Code na web, Claude Code no Replit),
  sempre com branch, hook, revisão independente e PR.
- Proibido: Replit Agent e commits diretos na `main`. A regra está em CLAUDE.md, "Restrições".
- O restante desta ADR continua vigente.
