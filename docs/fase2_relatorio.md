# Fase 2: arquitetura e dimensionamento

Estudo conceitual (pré-Fase A) de uma missão **robótica** de retorno de amostras Terra–Marte–Terra.
Os números deste relatório vêm de `results/`, gerados por `tools/`. Cada tabela indica o arquivo de origem.
"Verificado" só se usa para comparação com dados publicados.

## 1. Resultado em uma página

Fonte: `results/etapa2.5/arquitetura.md`.

**Missão de referência:** conjunção de 2028, missão A (ADR 0003). Datas em TDB:

| Evento | Data |
| :- | :- |
| Partida da Terra | 2028-11-24 |
| Chegada a Marte | 2029-09-20 |
| Partida de Marte | 2030-11-08 |
| Chegada à Terra | 2031-09-23 |

Estada em Marte de 414 d; reentrada a 12,34 km/s.

**Arquitetura:**
- Dois veículos em lançamentos separados, cada um injetado direto na trajetória pelo lançador (ADR 0008).
- **Orbitador:** captura propulsiva na órbita de 1 sol (ADR 0003). Desce para a órbita de encontro de
  **300 × 24.992 km** (ADR 0005).
- **Lander:** entrada direta, pouso em Jezero. Leva o MAV hipergólico (ADR 0007), um braço de coleta de
  reserva e dois helicópteros que recuperam os tubos do Perseverance (ADR 0009).
- **ISRU:** fora (ADR 0006).

**Massas injetadas e lançadores** (pior margem nas quatro janelas do envelope, 2028–2035):

| Veículo | Massa injetada | Lançadores e pior margem |
| :- | -: | :- |
| Orbitador (regra iii) | **6.310 kg** | Falcon Heavy descartável **+78 %**; Vulcan VC6 **+31 %** |
| Lander | **3.740 kg** | Falcon Heavy +25 % (recuperação) / +200 % (descartável); Vulcan VC2 +16 %, VC4 +73 %, VC6 +122 % |

- **Lançamentos:** 2.
- **Envelope de Δv (ADR 0004):** 5,912 km/s, definido pela conjunção de 2033 com |DLA| ≤ 50°.
- **"Lançador operacional"** vale na data da fonte citada. A disponibilidade em 2028 e depois não foi avaliada.

## 2. Método (o que cada etapa fez)

| Etapa | Pergunta | Ferramenta | Resultado | Decisão |
| :- | :- | :- | :- | :- |
| 2.1 | Arquitetura de superfície (S1–S4) e órbita de encontro | `tools/superficie.py`, `tools/varredura_encontro.py` | S2: entrada direta + encontro em órbita elíptica; varredura do apoapse com periapse de 300 km e regra dos 5 % | ADR 0005 |
| 2.2 | ISRU de O2 para o MAV | `tools/isru.py` | ISRU pesa 2,0 a 2,5 t a mais que o MAV LOX/CH4 com tudo da Terra (`results/etapa2.2/isru.md`) | ADR 0006 |
| 2.2b | Propulsão do MAV | `tools/mav_propulsao.py` | hipergólico 34,2 t, LOX/CH4 35,1 t, sólido 41,3 t na órbita baixa, pela regra (iii), à órbita da época (`results/etapa2.2/mav_propulsao.md`) | ADR 0007 |
| 2.3 | Plataformas por subsistema | `tools/plataformas.py` | orbitador pelos subsistemas do Odyssey; lander L3 (MSR); margem AIAA S-120A E1 | P-016, P-017 |
| 2.4 | Lançamento e DLA | `tools/lancamento.py` | injeção direta × órbita baixa + estágio próprio, por janela; revisão de 2033 | ADR 0008; ADR 0004 (atualização) |
| 2.5 | Arquitetura integrada | `tools/confere_2033.py`, `tools/coleta.py`, `tools/arquitetura.py` | 2.1/2.2 conferidas; sensores de encontro alocados; conceito de coleta; tabela integrada | ADR 0009 |

**Física reaproveitada da Fase 1:**
- efemérides DE440;
- Lambert de Izzo;
- busca de missões com limite de reentrada e, desde a 2.4, limite opcional de |DLA|;
- equação do foguete por estágio.

**Acrescentado na Fase 2:**
- Δv de subida (Bowles et al. 2013);
- perda gravitacional vertical (conservadora);
- eclipse no pior caso geométrico;
- dimensionamento de painéis e baterias;
- geometria de lançamento: cos i = cos φ · sen Σ, e giro de plano no perigeu θ = arcsin(sen β / sen ν∞).

## 3. Composição dos veículos (`results/etapa2.5/arquitetura.md`)

**Orbitador (regra iii), 6.310 kg injetados:**

| Item | Propelente | Inerte / massa |
| :- | -: | -: |
| Estágio de inserção em Marte (MMH/MON) | 2.478 | 782 |
| Estágio de retorno (MMH/MON) | 1.401 | 443 |
| CU-2: CCRS | — | 620 |
| CU-2: cápsula EEV com contêiner | — | 90 |
| Plataforma (lista por subsistema + sensores de encontro) | — | 496 |

**Lander, 3.740 kg injetados:**

| Item | Massa |
| :- | -: |
| Estágio de cruzeiro | 84 de propelente + 27 inerte |
| Sistema de entrada, descida e pouso (P-018) | 1.782 |
| Plataforma L3 | 1.470 |
| Braço de coleta | 88 |
| Helicópteros | 6 |
| MAV + energia de aquecimento | 282 |
| Painéis do armazenamento criogênico no cruzeiro (só para MAV criogênico) | 0 |

Massa de entrada 3.629 kg; massa pousada 1.847 kg.

## 4. Sensibilidade (`results/etapa2.5/arquitetura.md`)

Uma premissa por vez, com a órbita de encontro de base.

| Caso | Orbitador injetado | Orbitador: FH desc. / VC6 | Lander injetado | Lander: FH rec. / FH desc. / VC2 / VC4 / VC6 |
| :- | -: | -: | -: | -: |
| Base | 6.310 | +78 % / +31 % | 3.740 | +25 / +200 / +16 / +73 / +122 % |
| Margem de massa GSFC (P-033) | 6.623 | +69 % / +25 % | 4.206 | +11 / +167 / +3 / +54 / +97 % |
| Margem de massa ESA (P-033) | 6.714 | +67 % / +24 % | 5.044 | **−7** / +123 / **−14** / +29 / +64 % |
| Lander no limite inferior L1 (P-035; sem helicópteros) | 6.310 | +78 % / +31 % | 1.642 | +185 / +584 / +163 / +295 / +405 % |
| Lander no limite superior, SRL 2024 (P-035) | 6.310 | +78 % / +31 % | 5.633 | **−17** / +99 / **−23** / +15 / +47 % |
| Razão pousada/entrada 0,624 (P-018) | 6.310 | +78 % / +31 % | 3.051 | +53 / +268 / +42 / +113 / +172 % |
| Margem de Δv 5 % (P-014) | 5.785 | +94 % / +43 % | 3.645 | +28 / +208 / +19 / +78 / +128 % |
| Margem de Δv 20 % (P-014) | 7.548 | +49 % / +10 % | 4.007 | +17 / +180 / +8 / +62 / +107 % |
| Sem penalidade de DLA (P-036) | 6.310 | +93 % / +43 % | 3.740 | +35 / +226 / +25 / +88 / +141 % |

**Leitura:**
- O orbitador fica servido pelos dois lançadores escolhidos em todos os casos.
- **Com a margem ESA ou com a plataforma no limite superior, o lander perde dois lançadores:** o Falcon Heavy
  com recuperação e o Vulcan VC2. Nesses casos só o Falcon Heavy descartável e os Vulcan VC4 e VC6 servem.
- As premissas de maior efeito são a plataforma do lander (P-017/P-035, faixa de 1,6 a 5,6 t injetados)
  e a margem de Δv (P-014).

## 5. Decisões (ADRs)

| ADR | Decisão |
| :- | :- |
| 0003 | Missão A (conjunção de 2028), órbita de 1 sol, captura propulsiva; aerocaptura só comparada. Errata de datas (TDB) na Etapa 2.4 |
| 0004 | Envelope = maior dos mínimos por janela (2028–2035); estagiamento pela regra (iii). Atualizado na 2.4: 2033 com \|DLA\| ≤ 50°, envelope de 5,912 km/s |
| 0005 | Família S2 (entrada direta + encontro em órbita elíptica), periapse de 300 km, regra dos 5 %. Apoapse 18.483 → 26.950 → 24.992 km |
| 0006 | ISRU fora da arquitetura |
| 0007 | MAV hipergólico armazenável (O4); sólido como alternativa de maior maturidade |
| 0008 | Injeção direta pelo lançador; orbitador em Falcon Heavy descartável ou Vulcan VC6 |
| 0009 | Coleta: helicópteros recuperam os tubos do Perseverance (primário) + braço no lander (reserva) |

## 6. Fontes

`docs/fontes.md`, F1 a F103:
- F79–F87: lançadores e DLA;
- F88–F89: sensores de encontro; F90: massa do SRL em 2023;
- F92–F103: conceito de coleta e situação do MSR.

Quando o documento original é pago (AIAA S-120A), a fonte usada é a reprodução pública citada [F70].

## 7. Limitações

- **Plataformas:**
  - Só o Odyssey tem massa publicada por subsistema. Os subsistemas dele não foram escalados para um
    orbitador maior.
  - Nenhum lander de Marte tem quebra publicada. O L3 é uma alocação do MSR de 2020.
- **Lançamento:**
  - Capacidades interpoladas entre pontos publicados.
  - Penalidade de DLA aproximada a partir de uma tabela de Atlas V/Delta IV (P-036).
  - Coifa, período de lançamento e janela finita não avaliados.
- **Opção (b) de lançamento** (alternativa): giro de plano num único impulso no perigeu; armazenamento de
  LH2 na órbita baixa não modelado.
- **Superfície:**
  - Painel do lander sem poeira.
  - Aquecimento do MAV com escala sem fonte (P-027).
  - Encontro em órbita elíptica alta, diferente do MSR, que usava órbita baixa.
- **Sensibilidade:** feita com a órbita de encontro de base, sem reaplicar a regra dos 5 %.
- **Etapas 1.4, 2.1 e 2.2:** os resultados ficam como registro da época, com plataformas de 850 kg.
  - 2.1 e 2.2: a conferência da 2.5 rodou as ferramentas de novo com a 2033 nova. Os 15 arquivos que elas
    geram hoje saíram iguais; três arquivos antigos, sem sufixo, não são mais gerados e não foram conferidos
    (`results/etapa2.5/conferencia_2033.md`).
  - 1.4: não foi conferida. A regra (i) dela usou a trajetória antiga de 2033 e fica desatualizada (ADR 0004,
    atualização da Etapa 2.4).

## 8. Lacunas e riscos declarados

- **Sensores de encontro:** a câmera de ângulo largo e a potência do conjunto não têm valor publicado. O
  LIDAR usa um análogo [F89].
- **Potência do sistema de captura (CU-2):** sem valor publicado.
- **MLS (lançamento e ereção do MAV):** sem massa publicada; coberto ao menos em parte pelo L3.
- **SRL 2024:** nenhum documento de 2023–2025 publica a massa seca na superfície.
  - Valores publicados: 2100 kg secos em 2020 [F77]; até 2275 kg em agosto de 2023 [F90]; 2900 kg pousados em
    2024 [F41].
  - Como o SRL pousa com propulsão própria ([F24] slide 10), os 2900 kg provavelmente são massa total.
  - A comparabilidade do limite de 2500 kg segue não confirmada.
- **Transferência dos tubos dos helicópteros para o MAV:** sem item próprio; coberta só pelo L3.
- **Coleta (ADR 0009):**
  - integridade atual do depósito Three Forks;
  - Perseverance ativo na data do pouso;
  - pouso de precisão perto do depósito, não avaliado;
  - situação do programa MSR: término proposto em maio de 2025 [F101]; página do programa no passado em
    17/09/2026 [F103].
- **Twin (Fase 8):** os helicópteros são candidatos à simulação, reaproveitando o DroneSimulator.

## 9. Premissas NÃO VALIDADAS

A lista é gerada em **`results/fase2/premissas_nao_validadas.md`** por `tools/lista_premissas.py`. Ao fim
da Fase 2, as 38 premissas (P-001 a P-038) estão com status NÃO VALIDADA. Só o Fabio altera o status.

## Nota (2026-10-27): reprodutibilidade
- **Arquivos antigos removidos:** os três arquivos sem sufixo citados na conferência das Etapas 2.1 e 2.2 foram
  removidos (último commit em que existiam: b97d565). Detalhes em `docs/etapa2.1_superficie.md`.
- **Etapa 1.4 regenerada:** os resultados da 1.4 estavam atrasados em relação à 2033 com |DLA| ≤ 50° e foram
  regenerados. Errata em `docs/etapa1.4_dimensionamento.md`. Os números desta fase não mudam.
- **Prevenção:** a verificação de CI `.github/workflows/regeneracao.yml` regenera todo o `results/` e compara com o
  versionado.
- **"Idêntico" com tolerância declarada:** CPUs diferentes mudam os últimos dígitos (1e-16 a 8e-15 relativo, observado
  no CI). A comparação usa as premissas novas P-039 (números: passa se |a − b| ≤ max(1e-9 · |b|, 1e-10)) e P-040 (PNG: até
  0,1 % dos pixels), ambas NÃO VALIDADAS. O limite numérico vem da precisão relevante do estudo (~1e-4 relativo), não do
  ruído observado; diferença acima dele é problema a investigar. Com elas, são 40 premissas (P-001 a P-040), todas NÃO VALIDADAS
  (`results/fase2/premissas_nao_validadas.md`).

## Nota (2026-10-27): premissa P-041 na lista gerada
- A Etapa 3.1 acrescenta a P-041 (parâmetros numéricos da queima finita, NÃO VALIDADA) a `config/premissas.yaml`.
- `tools/lista_premissas.py` lista todas as premissas. Por isso `results/fase1/premissas.md` e
  `results/fase2/premissas_nao_validadas.md` foram regenerados e agora mostram 41 premissas (P-001 a P-041), todas NÃO
  VALIDADAS.
- Nenhum número desta fase muda.

## Nota (2026-10-27): premissas P-042 e P-043 na lista gerada
- A Etapa 3.1 (várias queimas e conferência com o ERO) acrescenta a P-042 e a P-043, ambas NÃO VALIDADAS.
- `results/fase1/premissas.md` e `results/fase2/premissas_nao_validadas.md` foram regenerados e agora mostram 43 premissas
  (P-001 a P-043), todas NÃO VALIDADAS.
- Nenhum número desta fase muda.

## Errata (2026-10-27): redimensionamento da Etapa 3.1 (ADR 0011)
**O que muda.** A arquitetura das Etapas 2.3 a 2.5 foi redimensionada com os motores escolhidos na Etapa 3.1:
- Isp de 310 s do R-4D-11 na inserção, no retorno e no MAV (antes 321 s e 343 s);
- Isp de 292 s do 10N no cruzeiro do lander (antes 321 s);
- perdas de queima finita calculadas na captura e na saída de Marte, no lugar da P-015: **72,6** e **56,4 m/s**, antes 18 e
  11 m/s (`results/etapa3.1/perdas_calculadas.md`).

As §1, §3 e §4 deste relatório ficam como registro; **os números vigentes são os abaixo**, de
`results/etapa2.5/arquitetura.md`. As Etapas 1.4, 2.1 e 2.2 continuam como registro da época.

**Massas (kg)**

| Item | Antes | Agora |
| :- | -: | -: |
| Orbitador injetado (regra iii) | 6.310 | **7.205** |
| Estágio de inserção: propelente / inerte | 2.478 / 782 | 2.990 / 944 |
| Estágio de retorno: propelente / inerte | 1.401 / 443 | 1.569 / 496 |
| Lander injetado | 3.740 | **4.066** |
| Cruzeiro do lander: propelente / inerte | 84 / 27 | 100 / 32 |
| Entrada, descida e pouso (P-018) | 1.782 | 1.932 |
| MAV + energia do aquecimento | 282 | 438 |
| Massa de entrada / pousada | 3.629 / 1.847 | 3.934 / 2.003 |
| Total na órbita baixa (regra iii), modelo (`results/etapa2.3/plataformas.md`) | 30.509 | 34.216 |

A órbita de encontro não muda: 300 × 24.992 km (a regra dos 5 % foi reaplicada).

A referência L2 (só referência, fora da faixa) também cresce, porque o núcleo dela escala com o MAV: plataforma de
1.857 para 2.440 kg e total (iii) no apoapse dela de 32.307 para 39.850 kg (`results/etapa2.3/plataformas.md`).

**Margens dos lançadores escolhidos** (pior das quatro janelas): ver a nota de 2026-10-27 no ADR 0008. Todos continuam
servindo, com margens menores:
- orbitador: Falcon Heavy descartável +56 %, Vulcan VC6 +15 %;
- lander: Vulcan VC2 +6 %.

**Sensibilidade** (antes → agora; margens do orbitador: FH descartável / VC6; do lander: FH recuperação / FH descartável /
VC2 / VC4 / VC6)

| Caso | Orbitador injetado (kg) | Margens do orbitador | Lander injetado (kg) | Margens do lander |
| :- | -: | :- | -: | :- |
| Base | 6.310 → 7.205 | +78 % / +31 % → +56 % / +15 % | 3.740 → 4.066 | +25 % / +200 % / +16 % / +73 % / +122 % → +15 % / +176 % / +6 % / +60 % / +104 % |
| Margem de massa GSFC (+15 % da básica) nas duas plataformas | 6.623 → 7.563 | +69 % / +25 % → +48 % / +10 % | 4.206 → 4.533 | +11 % / +167 % / +3 % / +54 % / +97 % → +3 % / +148 % / −5 % / +43 % / +83 % |
| Margem de massa ESA (20 % × 20 %) nas duas plataformas | 6.714 → 7.666 | +67 % / +24 % → +46 % / +8 % | 5.044 → 5.374 | −7 % / +123 % / −14 % / +29 % / +64 % → −13 % / +109 % / −20 % / +21 % / +54 % |
| Plataforma do lander no limite inferior (L1; sem os helicópteros, como definido na Etapa 2.3) | 6.310 → 7.205 | +78 % / +31 % → +56 % / +15 % | 1.642 → 1.962 | +185 % / +584 % / +163 % / +295 % / +405 % → +138 % / +472 % / +120 % / +231 % / +323 % |
| Plataforma do lander no limite superior (SRL 2024 − MAV) | 6.310 → 7.205 | +78 % / +31 % → +56 % / +15 % | 5.633 → 5.965 | −17 % / +99 % / −23 % / +15 % / +47 % → −22 % / +88 % / −27 % / +9 % / +39 % |
| Razão pousada/entrada 0,624 (Viking, a partir de órbita) em vez de 0,509 | 6.310 → 7.205 | +78 % / +31 % → +56 % / +15 % | 3.051 → 3.317 | +53 % / +268 % / +42 % / +113 % / +172 % → +41 % / +238 % / +30 % / +96 % / +150 % |
| Margem de Δv 5 % (base 10 %) | 5.785 → 6.549 | +94 % / +43 % → +71 % / +27 % | 3.645 → 3.889 | +28 % / +208 % / +19 % / +78 % / +128 % → +20 % / +189 % / +11 % / +67 % / +113 % |
| Margem de Δv 20 % (base 10 %) | 7.548 → 8.778 | +49 % / +10 % → +28 % / −6 % | 4.007 → 4.627 | +17 % / +180 % / +8 % / +62 % / +107 % → +1 % / +143 % / −7 % / +40 % / +79 % |
| Sem penalidade de DLA (multiplicador 1) | 6.310 → 7.205 | +93 % / +43 % → +69 % / +25 % | 3.740 → 4.066 | +35 % / +226 % / +25 % / +88 % / +141 % → +24 % / +200 % / +15 % / +73 % / +122 % |

**Leitura nova:**
- Com margem de Δv de 20 % (P-014), o orbitador perde o Vulcan VC6 (−6 %).
- Com a margem de massa GSFC, o lander perde o Vulcan VC2 (−5 %).
- O Vulcan VC4, que não era escolhido, deixa de servir o orbitador no caso de base.

**Premissas:**
- **Nova:** P-044 (ponto fixo entre perdas e massas).
- A P-015 fica restrita à saída da Terra e às etapas anteriores.
- `results/fase1/premissas.md` e `results/fase2/premissas_nao_validadas.md` foram regenerados: 44 premissas, todas NÃO
  VALIDADAS.

## Errata (2026-10-28): fração estrutural do MAV pressurizado (ADR 0007)
**O que muda.** O ε do MAV O4 passa de 0,238 (MAV com turbobomba) para **0,230** (MAV pressurizado), ambos de Bowles et
al. [F46], Tab. 5. Os números da errata de 2026-10-27 que mudam são os abaixo; **os vigentes são os da coluna "Agora"**,
de `results/etapa2.5/arquitetura.md` e `results/etapa2.3/plataformas.md`.

| Item | Errata de 2026-10-27 | Agora |
| :- | -: | -: |
| Lander injetado | 4.066 | **3.996** |
| Cruzeiro do lander: propelente / inerte | 100 / 32 | 99 / 31 |
| Entrada, descida e pouso (P-018) | 1.932 | 1.898 |
| MAV + energia do aquecimento | 438 | 403 |
| Massa de entrada / pousada | 3.934 / 2.003 | 3.866 / 1.968 |
| Total na órbita baixa (regra iii), modelo | 34.216 | 34.003 |

O orbitador (7.205 kg) e a órbita de encontro (300 × 24.992 km) não mudam. A referência L2 passa de 2.440 para 2.309 kg.

**Margens do lander** (pior janela): Falcon Heavy com recuperação +17 %, Vulcan VC2 +8 % (antes +15 % e +6 %). Ver a nota
de 2026-10-28 no ADR 0008.

**Sensibilidade** (`results/etapa2.5/arquitetura.md`): os mesmos casos perdem lançador.
- Margem de Δv de 20 %: o orbitador perde o VC6 (−6 %), e o lander perde o VC2 (−3 %, antes −7 %).
- GSFC: o lander perde o VC2 (−3 %, antes −5 %).
- ESA: o lander perde o Falcon Heavy com recuperação (−12 %) e o VC2 (−18 %).
- Casos novos de ε do MAV: 0,238 e 0,176 não derrubam nenhum lançador. O caso 0,300 (P-045) derruba os dois do lander.

**RISCO de projeto (MAV perto da assíntota da equação do foguete).**
- Com Isp de 310 s e Δv de subida de 5,764 km/s (com margem), o MAV fica perto da assíntota da equação do foguete.
- Um ε só um pouco acima do de Bowles faz a massa crescer muito. Com ε = 0,300 (P-045, sem fonte, só ilustração), o
  lander vai a 5.368 kg e perde os dois lançadores escolhidos: Falcon Heavy com recuperação −13 % e Vulcan VC2 −19 %.
- Ligado à **Etapa 3.3**: uma órbita de encontro mais baixa, com orbitador elétrico, reduz o Δv do MAV.

**Premissas:** P-045 nova; total de 45, todas NÃO VALIDADAS (`results/fase2/premissas_nao_validadas.md`).
