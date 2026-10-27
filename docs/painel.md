# Painel web do MarsMission

Painel em Streamlit (ADR 0010). Lê `results/` e `config/` e chama funções testadas de `src/orbital`. Não copia números
nem altera cálculos. O Replit é o ambiente de execução do painel. Desenvolver nele (ou em qualquer outro ambiente) só
com branch, hook, revisão independente e PR; o Replit Agent e commits diretos na `main` são proibidos (CLAUDE.md,
"Restrições", decisão do Fabio em 2026-10-27).

## Páginas

| Página | O que mostra | De onde vem |
| :- | :- | :- |
| Visão geral | Missão de referência (cronograma TDB, durações, Δv, reentrada); arquitetura final (orbitador, lander com MAV, helicópteros e braço); lançadores e margens; número de lançamentos; verificação contra dados publicados | `results/etapa1.3/missoes.yaml`, `results/etapa2.5/arquitetura.yaml`, `results/etapa1.2/verificacao_*.yaml` |
| Trajetória | Órbitas de Terra e Marte nas datas reais (DE440) e arcos de Lambert de ida e volta, em 2D | `orbital.porkchop`, `orbital.lambert`, `orbital.kepler` (calculado na hora; precisa dos kernels) |
| Porkchops | Contornos de C3 e v∞ das janelas de ida e de volta de `config/janelas.yaml`, com valores no cursor (inclusive DLA na ida), mínimos e missão de referência | `results/painel/porkchop_*.npz` (gerado por `tools/exporta_painel.py`), `results/etapa1.2/minimos_*.yaml` |
| Orçamento de massa | Controles para a plataforma do lander (P-017), a margem de Δv (P-014) e o Isp e a fração estrutural dos estágios MMH/MON; recalcula os veículos e mostra que lançadores continuam servindo | `orbital.veiculos`, `orbital.lancamento` |
| Premissas e decisões | Todas as premissas de `config/premissas.yaml`, com status, e os ADRs (texto e link) | `config/premissas.yaml`, `docs/adr/` |

**Rótulos.** Todo número exibido traz um rótulo:
- **verificado contra dados publicados:** comparação com NASA/TM-2010-216764 e JPL 82-43;
- **calculado:** saída das ferramentas ou de `src/orbital`;
- **premissa** seguido do status lido de `config/premissas.yaml` (hoje, NÃO VALIDADA).

Os valores de base do Isp e da fração estrutural dos estágios MMH/MON têm fonte publicada e não são premissas:
aparecem como "dado de fonte publicada [Fnn]", com a primeira fonte citada no config. Os valores das tabelas de
referência na verificação (NASA/TM-2010-216764 e JPL 82-43) aparecem como "dado publicado".

As faixas dos controles vêm dos arquivos, não do painel:
- **Plataforma do lander:** de L1 a SRL 2024 − MAV, lidas de `results/etapa2.3/plataformas.yaml`.
- **Margem de Δv, Isp e fração estrutural:** as faixas de sensibilidade de `config/dimensionamento.yaml`.

## Rodar localmente

```bash
conda env create -f environment.yml          # Python do conda; dependências do pyproject.toml via pip
conda activate marsmission
python tools/fetch_kernels.py                # kernels SPICE (~33 MB), com conferência do MD5
python -m streamlit run src/painel/app.py
```

## Dependências: uma só lista

As dependências estão só no `pyproject.toml`:
- obrigatórias: numpy, scipy, matplotlib, pyyaml, spiceypy e pillow (só com piso, ver o cabeçalho do `pyproject.toml`);
- extra `painel`: streamlit, plotly e pandas;
- extra `dev`: pytest.

Os três ambientes instalam o mesmo pacote:
- `environment.yml` (local e CI): o conda fornece o Python 3.11.18 e instala o pacote com `pip install -e .[dev,painel]`;
- Replit: `pip install -e '.[painel]'`.

**Conferência da troca conda-forge → wheels do PyPI e da mudança das funções para `src/`:**
`results/conferencia/regeneracao_painel.md`, gerado por `tools/confere_regeneracao.py` num worktree fixo no commit 310b8c3.
- O que a ferramenta faz: regenera todo o `results/` numa cópia, no ambiente pip, e compara com o versionado.
- Resultado: 62 de 62 idênticos, nenhum só dentro da tolerância (P-039, P-040) e nenhum diferente.
- Os commits seguintes do PR mudam em `src/orbital` só docstrings e não tocam `tools/` nem `config/`.
- O CI repete a conferência a cada PR (`.github/workflows/regeneracao.yml`).

**Ambiente local antigo:** o env `marsmission` criado antes desta mudança não tem streamlit nem plotly. Nele, o
pre-commit pula `tests/test_painel_app.py`. Recrie com `conda env remove -n marsmission && conda env create -f environment.yml`.

**Worktrees:** o pacote é instalado em modo editável apontando para o `src/` da árvore em que foi instalado. Rodar o
Streamlit dentro de outra worktree importa `painel` e `orbital` da árvore principal. `tools/` e o pytest não são
afetados, porque põem o próprio `src/` na frente.

## Replit

Consultado na documentação oficial em 2026-10-27. **O painel não foi executado no Replit por este estudo.** O que está
marcado "não conferido" precisa ser confirmado na primeira importação.

**Nota (2026-10-27):** primeira importação feita; resultados em "Primeira execução no workspace", abaixo.
- Com as dependências da época (streamlit 1.65.0), a instalação falhou no pillow.
- Com `pillow>=13.0.0` e streamlit 1.66.1 (ADR 0010, nota de 2026-10-27), o painel foi executado dentro do workspace e
  aberto em `127.0.0.1:8501`.
- A frase acima ("O painel não foi executado no Replit por este estudo") deixa de valer. Continuam não conferidos o
  Webview do Replit e o endereço externo.

### Importar do GitHub
1. **Repositório público:** abrir `https://replit.com/github.com/fasn98/MarsMission` ("Rapid import").
   - Alternativa: replit.com/import → GitHub → escolher o repositório → Import.
   - Fonte: [Import from GitHub](https://docs.replit.com/getting-started/quickstarts/import-from-github).
2. **Configuração:** o Replit lê o `.replit` deste repositório.
   - O botão **Run** instala o pacote com o extra `painel` e baixa e confere os kernels com `tools/fetch_kernels.py`.
   - O download só acontece na primeira execução ou se o MD5 não bater.
   - Depois sobe o Streamlit na porta 8501, exposta na 80.
3. **Gerenciador de pacotes:** a documentação diz: "When you create a Python Replit App, your package manager is poetry
   by default" e "`pip install` does not manage your dependencies"
   ([Dependency management](https://docs.replit.com/replit-workspace/dependency-management)).
   - Por isso o `.replit` chama o `pip` explicitamente e desliga `packager.features.guessImports`, para o Replit não
     escrever no `pyproject.toml`.
   - **Não conferido:** se o ambiente do Replit mantém a instalação do `pip` entre sessões. O comando de Run reinstala a
     cada execução, sem efeito quando já está instalado.
   - **Também não conferidos:** a grafia do módulo `python-3.11` e o canal do Nix.
     - **Nota (2026-10-27): conferido.** No workspace importado, o módulo `python-3.11` forneceu o Python 3.11.14.
       O canal `stable-25_05` foi aceito (o `NIX_PATH` aponta `nixpkgs-stable-25_05`), e o `.replit` passou a usá-lo.
       O canal `stable-24_05`, que estava antes no `.replit`, não foi testado.

### Primeira execução no workspace (2026-10-27)
- **Instalação: falhou** (observado). O `pip install -e ".[painel,dev]"`, rodado à mão no Shell (o Run do `.replit` usa
  `.[painel]`), parou no pillow, dependência do matplotlib e do streamlit.
  - Observado, sem fonte oficial do Replit: o índice de pacotes do Replit (`package-firewall.replit.internal`, servidor
    `SocketFirewall/2.12.1`) devolveu HTTP 403: "Access denied: Your download has been blocked by the Socket Security
    Policy. Reason: Critical CVE." O motivo é o texto do firewall; as fontes dos avisos estão na ADR 0010.
  - Observados como bloqueados: pillow 10.4.0, 11.3.0, 12.0.0, 12.1.0, 12.2.0 e 12.3.0. O pillow 13.0.0 passa.
  - Observado: as outras dependências diretas fixadas no `pyproject.toml` passaram.
- **Kernels: conferidos.** `tools/fetch_kernels.py` baixou os dois kernels. Os MD5 batem com `config/kernels.yaml`:
  `naif0012.tls` `25a2fff30b0dedb4d76c06727b1895b1` e `de440s.bsp` `3917ee56769db332790c751e2168843d`.
- **Com `pillow>=13.0.0` e streamlit 1.66.1** (branch `fix/deps-pillow-13`, commit 0a46b5e; ADR 0010, nota de
  2026-10-27), no mesmo workspace:
  - **Instalação:** funcionou. `pip check`: "No broken requirements found".
  - **pytest:** 183 passaram e 2 foram pulados (Vallado e Curtis, já pulados antes).
  - **Painel:** subiu pelo comando de Run do `.replit`, com `--server.headless true` a mais. As cinco páginas foram
    abertas num Chromium headless, sem exceção e sem alerta do Streamlit.
  - **Console do navegador:** pela raiz `/`, vazio. Pelas URLs das páginas, dois 404 em `/<página>/_stcore/health` e
    `/<página>/_stcore/host-config`.
    - Em `/visao-geral` aparece ainda o aviso "The page that you have requested does not seem to exist. Running the
      app's main page.": a página padrão fica em `/`.
  - **Números exibidos, conferidos contra `results/`:**
    - partida da missão de referência: 2028-11-24 (`results/etapa1.3/missoes.yaml`);
    - orbitador injetado: 6 310 kg (6 310,3 na soma da tabela), contra 6310.348840517989 em
      `results/etapa2.5/arquitetura.yaml`;
    - pior margem do Vulcan VC6: 31 % no orbitador e 122 % no lander, contra 0.3141237151049956 e 1.2173610409903444
      no mesmo arquivo.
- **Não conferido:** o painel no navegador do próprio Replit (Webview) e pelo endereço externo; a conferência acima usou
  `127.0.0.1:8501` dentro do workspace.

### Atualizar
Nada de Replit Agent nem de commit direto na `main` (CLAUDE.md). Para trazer uma versão nova da `main`:
- no **Shell** do Replit, rodar `git pull`;
- ou usar o painel **Git** do Replit (pull).

Depois, **Run** de novo. Se o `pyproject.toml` mudou, o comando de Run reinstala.

### Publicar com endereço permanente
- **O "Run" do workspace não é endereço permanente.** O link de desenvolvimento só funciona com o workspace aberto
  (não conferido numa página oficial dedicada).
- **Publicar** cria a publicação pela seção `[deployment]` do `.replit`: `build` instala e baixa os kernels; `run` sobe o
  Streamlit.
- **O que diz a página oficial de planos** ([Plans](https://docs.replit.com/billing/plans)):
  - **Starter (gratuito):** "Get 1 free published app"; "This published link will automatically go down after 30 days".
    Os créditos do Starter cobrem "Publishing (Autoscale, static)".
  - **Mais publicações:** "Additional published apps beyond this require Core or Pro".
  - **Core:** "Unlimited published apps".
  - **Preço** ([replit.com/pricing](https://replit.com/pricing)): Core a US$ 20/mês, ou US$ 18/mês na cobrança anual.
- **Conclusão:** um endereço que não expira depende de plano pago (Core ou Pro). No Starter, a publicação sai do ar em
  30 dias.
- **Não encontrado na documentação oficial consultada:**
  - o formato exato do endereço publicado;
    - **Nota (2026-10-27):** encontrado depois em [Custom domains](https://docs.replit.com/cloud-services/deployments/custom-domains):
      `<subdomínio>.replit.app` (ver a comparação com o Streamlit Community Cloud).
  - o preço por tipo de publicação;
  - qual plano permite domínio próprio.

## Hospedagem gratuita: Streamlit Community Cloud

Consultado na documentação oficial em 2026-10-27. **Nada foi publicado.** É uma opção ao lado do Replit pago, e a
escolha é do Fabio.

- **Custo e visibilidade** ([streamlit.io/cloud](https://streamlit.io/cloud)): "Totally free"; "Public apps only".
  - A visibilidade segue o repositório: "if your repo is private your app will be private and if your repo is public
    your app will be public"; "You are only allowed one private app at a time"
    ([Share your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app)).
- **Endereço:** `<subdomínio>.streamlit.app`
  ([Manage your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app)).
- **Dorme por inatividade** (mesma página): "All apps without traffic for 12 hours go to sleep".
  - Qualquer visitante acorda o app pelo botão "Yes, get this app back up!".
  - Memória: "690MB minimum, 2.7GBs maximum", com a ressalva "These limits may change at any time without notice"
    (valores da documentação, de fevereiro de 2024).
- **Arquivo de dependências**
  ([App dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)):
  - O Community Cloud usa o primeiro que encontrar, na ordem `uv.lock`, `Pipfile`, `environment.yml`,
    `requirements.txt` e `pyproject.toml` (este, "poetry").
  - A busca começa na pasta do arquivo de entrada e depois vai à raiz do repositório.
  - Neste repositório, valeria o `environment.yml` da raiz, que instala o pacote com
    `pip install -e .[dev,painel]`. **Não conferido** se isso funciona lá.
- **Kernels SPICE: não conferido.** O Community Cloud só roda o app; não foi encontrada na documentação uma etapa de
  build equivalente ao `build` do Replit.
  - Sem `tools/fetch_kernels.py`, a página Trajetória mostra o aviso de kernels ausentes (`src/painel/app.py`).
  - As outras páginas leem `results/` e `config/`.
  - Resolver isso exigiria mudar o código, com PR e justificativa.
- **Pillow:** com o `pyproject.toml` atual (streamlit 1.66.1 e `pillow>=13.0.0`; ADR 0010, nota de 2026-10-27), o pip
  instala o pillow 13.0.0 ou posterior (13.0.0 no CI do PR #13), com os avisos "Critical" das versões até a 12.3.0
  corrigidos. **Não conferido** no Community Cloud.

### Comparação

| | Replit | Streamlit Community Cloud |
| :- | :- | :- |
| Endereço permanente | Só com plano pago: Core (US$ 18/mês na cobrança anual) ou Pro. No Starter, o link "will automatically go down after 30 days" | Gratuito; o app dorme após 12 h sem tráfego |
| Endereço | `<subdomínio>.replit.app` ([Custom domains](https://docs.replit.com/cloud-services/deployments/custom-domains)) | `<subdomínio>.streamlit.app` |
| Repositório | Importação pública conferida; privado não conferido | Público, para app público |
| Etapa de build (kernels) | Sim (`[deployment] build` do `.replit`) | Não encontrada na documentação |
| Instalação | O pillow 13.0.0 passa no firewall de pacotes; o pillow de 10.4.0 a 12.3.0 (o streamlit 1.65.0 exige `pillow<13`) era bloqueado (observação de 2026-10-27, sem fonte oficial do Replit) | Não conferida |

### Alternativa estática (GitHub Pages)
Sem plano pago, a alternativa permanente é uma página estática no GitHub Pages do repositório. **Não foi construída.**
- **O que funcionaria:** visão geral, premissas e decisões, trajetória e porkchops. Seriam páginas HTML com gráficos
  Plotly exportados por um script em `tools/` a partir de `results/`.
- **O que não funcionaria como hoje:** os controles do orçamento de massa. Uma página estática não roda `src/orbital`.
  Os controles teriam de usar uma grade de casos calculada antes por um script em `tools/`, gravada em `results/`.
- **Rótulos:** seguiriam a mesma regra.

## Testes

- **`tests/test_painel_dados.py`:** a camada de dados.
  - Reproduz `results/etapa2.5/arquitetura.yaml`: massas injetadas, margens e três casos de sensibilidade.
  - Todo número tem rótulo válido, e o rótulo de premissa segue o status do arquivo.
  - O porkchop exportado bate com a missão de referência no ponto da grade.
  - A trajetória fecha nas chegadas.
  - As ferramentas usam as funções de `src/`.
- **`tests/test_painel_app.py`:** cada página roda sem exceção (Streamlit AppTest). Com a plataforma do lander no limite
  superior, o lander perde o Falcon Heavy com recuperação e o Vulcan VC2.
