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

**Endereços.** A Visão geral é a página padrão, na raiz `/`. Ela também abre em `/visao-geral` (página oculta com o
mesmo conteúdo, para links salvos). As outras ficam em `/trajetoria`, `/porkchops`, `/orcamento` e `/premissas`.

**Nomes exibidos.** As chaves internas aparecem por extenso:
- a órbita em Marte, pela `descricao` de `config/parametros_orbitais.yaml`;
- a missão (ex.: `2028-conjuncao` → "conjunção de 2028"), pelo id de `results/etapa1.3/missoes.yaml`;
- os mínimos dos porkchops, segundo a nota gravada em `results/etapa1.2/minimos_*.yaml` (o teste confere a nota);
- os estágios do orçamento, com os mesmos nomes de `results/etapa2.5/arquitetura.yaml`.
A altitude da órbita em Marte aparece com o rótulo da fonte do config ([F18]).

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

**Nota (2026-10-27): formato dos relatórios de conferência.**
- Desde o PR #17, o relatório de `tools/confere_regeneracao.py` registra as versões de todas as dependências do
  `pyproject.toml` (inclusive o pillow), o Python, a CPU, o sistema e o commit.
- Os relatórios de `results/conferencia/` anteriores ao #17 estão no formato antigo, sem pillow, sistema nem commit:
  `regeneracao_painel`, `regeneracao_pillow13`, `regeneracao_pos_correcao` e `regeneracao_reprodutibilidade_1.4`
  (`.md` e `.yaml`). O de `reprodutibilidade_1.4` também não registra a CPU.
- Eles não foram regravados porque são registros datados de execuções em ambientes e commits específicos. Não entram
  na comparação da regeneração.

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
      - **Nota (2026-10-27):** com o alias `/visao-geral` (ver "Endereços", no início), o aviso deixou de aparecer: o
        endereço abre a Visão geral. Observado no mesmo workspace e no mesmo Chromium headless, em `127.0.0.1:8502`,
        com o código deste alias antes do rebase (commit f256ba0). Os dois 404 de `/<página>/_stcore/...`
        continuam e não foram investigados.
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
  - **Nota (2026-10-27):** agora vale `src/painel/requirements.txt`, na pasta do arquivo de entrada, que tem prioridade
    sobre o `environment.yml` da raiz. Ver "Publicar no Streamlit Community Cloud", abaixo.
- **Kernels SPICE: não conferido.** O Community Cloud só roda o app; não foi encontrada na documentação uma etapa de
  build equivalente ao `build` do Replit.
  - Sem `tools/fetch_kernels.py`, a página Trajetória mostra o aviso de kernels ausentes (`src/painel/app.py`).
  - As outras páginas leem `results/` e `config/`.
  - Resolver isso exigiria mudar o código, com PR e justificativa.
  - **Nota (2026-10-27):** resolvido no código. A página Trajetória baixa os kernels que faltam, com a rotina de
    `tools/fetch_kernels.py` (agora em `src/orbital/kernels.py`), e confere o MD5. Ver a subseção abaixo.
- **Pillow:** com o `pyproject.toml` atual (streamlit 1.66.1 e `pillow>=13.0.0`; ADR 0010, nota de 2026-10-27), o pip
  instala o pillow 13.0.0 ou posterior (13.0.0 no CI do PR #13), com os avisos "Critical" das versões até a 12.3.0
  corrigidos. **Não conferido** no Community Cloud.

### Publicar no Streamlit Community Cloud

Preparado em 2026-10-27, **sem publicar**: a publicação é feita pelo Fabio, pela interface do Community Cloud. Fontes
oficiais consultadas nessa data.

**Passo a passo**
1. **Conta** ([Create your account](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/create-your-account)):
   entrar em share.streamlit.io com GitHub, Google ou código por e-mail. Depois, conectar a conta do GitHub
   ([Connect your GitHub account](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account)).
   - Com isso, já dá para publicar de repositórios públicos: "you'll be able to deploy apps from your public
     repositories".
   - É preciso ter direito de administrador no repositório.
2. **Criar o app** ([Deploy your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)):
   clicar em **Create app** e depois em **Yup, I have an app**. Preencher:
   - **Repository:** `fasn98/MarsMission`;
   - **Branch:** `main`;
   - **Main file path:** `src/painel/app.py`;
   - **App URL** (opcional): o subdomínio de `<subdomínio>.streamlit.app`.
3. **Python 3.11:** em **Advanced settings**, escolher **3.11** antes de salvar.
   - A documentação diz que o Community Cloud "defaults to version 3.12". O `pyproject.toml` exige `>=3.11,<3.12`, então
     com o padrão a instalação falha.
   - A lista de versões oferecidas não está na página: ela diz só que são aceitas as versões "still receiving security
     updates". **Não conferido** que a 3.11 aparece na lista.
   - A versão não muda depois: "After you have deployed an app, you must delete it and redeploy it to change the version
     of Python it uses" ([Upgrade Python](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/upgrade-python)).
4. **Save.** A página diz que "most apps are deployed within a few minutes".

**Dependências (fonte única)**
- O Community Cloud usa o primeiro arquivo que encontrar, na ordem `uv.lock`, `Pipfile`, `environment.yml`,
  `requirements.txt`, `pyproject.toml` (poetry). Procura primeiro na pasta do arquivo de entrada e depois na raiz
  ([App dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)).
- `src/painel/requirements.txt` fica na pasta do arquivo de entrada e tem só `-e .[painel]`. Não é uma lista de
  dependências: instala este repositório pelo `pyproject.toml`, com o extra `painel`.
  - O modo editável é necessário: `orbital.config.RAIZ` precisa da árvore do repositório para ler `config/` e `results/`.
  - Sem esse arquivo, valeria o `environment.yml` da raiz (conda).
- O pip resolve o `.` a partir da pasta atual, não da pasta do arquivo. Isso foi conferido com `pip install --dry-run`
  em 2026-10-27.
  - A documentação diz que, no Community Cloud, "the working directory is always the root of your repository"
    ([File organization](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization)).
  - **Não conferido** que a instalação também roda da raiz.
  - A mesma página de dependências diz que o `requirements.txt` é processado primeiro com o uv, com o pip como
    alternativa. Com uv 0.13.4, `uv pip install --dry-run -r src/painel/requirements.txt` a partir da raiz também
    resolveu o `.` para a raiz do repositório (conferido em 2026-10-27, workspace do Replit, CPU Intel Xeon Platinum
    8581C).
- Conferido em 2026-10-27 (workspace do Replit, CPU Intel Xeon Platinum 8581C), num venv limpo (Python 3.11.14, sem o
  `.pythonlibs` do Replit), com
  `pip install -r src/painel/requirements.txt` a partir da raiz:
  - instala o pacote em modo editável, com pillow 13.0.0, streamlit 1.66.1, plotly 7.1.0, pandas 3.0.6 e numpy 2.4.6;
  - o pytest fica de fora, porque é do extra `dev`;
  - `RAIZ` aponta para o repositório.
- `.streamlit/config.toml` está na raiz, como exige a mesma página.

**Kernels SPICE na primeira execução**
- Ao abrir a página Trajetória, o painel baixa os kernels de `config/kernels.yaml` que faltam e confere o MD5 de todos.
  A rotina é a de `tools/fetch_kernels.py`, agora em `src/orbital/kernels.py`.
  - Enquanto isso, aparece o aviso "Baixando e conferindo os kernels SPICE…".
  - Se um MD5 não conferir, a página mostra o erro, com o MD5 esperado e o obtido, e não calcula nada.
  - **Prazo por arquivo:** `download_kernels.timeout_s` de `config/operacional.yaml`. É um parâmetro operacional, não
    uma
    premissa científica (decisão do Fabio, 2026-10-27, com justificativa no arquivo).
    - Limita cada operação de rede e o tempo total do arquivo, conferido a cada bloco. No pior caso o arquivo leva
      perto de 2× o prazo, e a resolução de DNS fica de fora.
    - Passou do prazo, ou a rede falhou: a página mostra a mensagem e o botão **Tentar de novo**.
- O resultado fica no cache do Streamlit (`st.cache_resource`): uma vez por processo do servidor. Uma falha não entra no
  cache; recarregar a página tenta de novo.
- As outras páginas leem só `results/` e `config/` e não precisam dos kernels.
- **Disco:** a documentação oficial consultada não diz se o disco do app persiste entre reinicializações. O painel
  trata o disco como não permanente: depois de uma reinicialização, ou de acordar após dormir, o download se repete
  na primeira visita à Trajetória se os kernels tiverem sumido. **Não conferido** no Community Cloud, assim como o
  acesso de saída a naif.jpl.nasa.gov.
- Conferido em 2026-10-27 (workspace do Replit, CPU Intel Xeon Platinum 8581C), num venv limpo e Chromium headless:
  - sem kernels, a primeira visita à Trajetória mostrou o aviso, baixou os dois kernels (MD5 conferem) e desenhou a
    trajetória, em 9,0 s;
  - a segunda visita não baixou de novo;
  - com um MD5 errado no config (só no disco, revertido depois), a página mostrou "Não foi possível obter os kernels
    SPICE: MD5 dos kernels não confere com kernels.yaml: naif0012.tls esperado …, obtido …";
  - com o prazo reduzido no config (só no disco, revertido depois), a página mostrou "… passou do prazo de … s
    (config/operacional.yaml). Nada foi calculado.";
  - o botão **Tentar de novo** e o cálculo depois do clique foram conferidos por teste (`tests/test_painel_app.py`), não
    no navegador.

**Memória**
- **Limite publicado** ([Manage your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app)):
  "Memory: 690MB minimum, 2.7GBs maximum", valores "as of February 2024", com a ressalva "These limits may change at any
  time without notice". Acima do limite, o app "may slow down from throttling or become nonfunctional".
- **Medido localmente** (observação de ambiente, 2026-10-27, workspace do Replit, CPU Intel Xeon Platinum 8581C; não é
  resultado do estudo):
  - método: pico de memória residente (VmHWM, `/proc/<pid>/status`) do processo do Streamlit, num venv limpo;
  - navegação: um Chromium headless abriu Trajetória (com o download dos kernels), Visão geral, Porkchops, Orçamento,
    Premissas, `/visao-geral` e Trajetória de novo;
  - resultado: pico de **193,8 MiB** (cerca de 203 MB). No início eram 72,4 MiB.
  - Isso é menos de um terço do mínimo publicado de 690 MB.
- **Limites da medição:**
  - uma única sessão;
  - controles na posição padrão: sem trocar janelas do porkchop nem mexer nos controles do orçamento, o que enche mais
    caches;
  - máquina do Replit, não do Community Cloud. Com vários visitantes ao mesmo tempo, a memória cresce;
  - **não conferido** no Community Cloud.

**Atualizar**
- "Streamlit Community Cloud will monitor your repository and automatically copy any file changes you commit"; "You will
  immediately see commits reflected in your deployed app for most changes"
  ([Edit your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/edit-your-app)).
- Com o branch `main`, cada merge de PR atualiza o app.
- A documentação não diz o que acontece quando muda um arquivo de dependências. **Não conferido** se o
  `pyproject.toml` alterado é reinstalado sem reiniciar o app pela interface ("Manage app" → reboot).
- Atualizações vindas do GitHub são limitadas a "no more than five per minute"
  ([Status and limitations](https://docs.streamlit.io/deploy/streamlit-community-cloud/status)).

**Limitações**
- **App público:** "Public apps only" ([streamlit.io/cloud](https://streamlit.io/cloud)). Com repositório público, o
  app é público ([Share your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app)).
- **Dorme sem uso:** "All apps without traffic for 12 hours go to sleep". Qualquer visitante acorda o app pelo botão
  "Yes, get this app back up!" (Manage your app).
- **Domínio próprio:** a documentação oficial consultada só descreve o endereço `<subdomínio>.streamlit.app` e não
  menciona domínio próprio. **Não conferido** que ele não seja possível.
- **Outras, da página Status and limitations:**
  - hospedagem "in the United States", sem opção de mudar;
  - Debian 11 ("bullseye").

### Comparação

| | Replit | Streamlit Community Cloud |
| :- | :- | :- |
| Endereço permanente | Só com plano pago: Core (US$ 18/mês na cobrança anual) ou Pro. No Starter, o link "will automatically go down after 30 days" | Gratuito; o app dorme após 12 h sem tráfego |
| Endereço | `<subdomínio>.replit.app` ([Custom domains](https://docs.replit.com/cloud-services/deployments/custom-domains)) | `<subdomínio>.streamlit.app` |
| Repositório | Importação pública conferida; privado não conferido | Público, para app público |
| Etapa de build (kernels) | Sim (`[deployment] build` do `.replit`) | Não encontrada na documentação; o painel baixa os kernels na primeira visita à Trajetória |
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
