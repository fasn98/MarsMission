# Etapa 2.3: plataformas do orbitador e do lander

Estado: **aguardando o portão do Fabio**. Resultados: `results/etapa2.3/plataformas.md` e `.yaml`, gerados
por `tools/plataformas.py` a partir de `config/plataformas.yaml`.

## 1. O que existe publicado

- **Orbitador.** Só o **Mars Odyssey** tem massa publicada por subsistema (press kit de lançamento,
  pp. 28–31 [F63]).
  - Do MRO, só a comunicação: 107,7 kg [F64].
  - Do MAVEN, Mars Express, TGO, MGS, MCO e ERO, só totais. As massas por subsistema desses veículos
    não foram encontradas em fonte primária.
- **Lander.** **Nenhum** lander de Marte (Phoenix, InSight, Viking, MPL, SRL) tem a lista completa
  por subsistema em fonte primária pública.
  - O que existe: comunicação e radar do Phoenix (DESCANSO, Tab. 2-16, p. 70 [F74]) e totais.
  - O núcleo (estrutura, pernas, térmico, comando e dados, GNC, propulsão de descida seca, cabeamento)
    fica sem divisão. Por isso a escala dele vira uma decisão (P-035, opções L1 e L2).
- **Margem.**
  - O AIAA S-120A-2015 é pago e não foi lido.
  - A Tabela 1 dele está reproduzida pela NASA em NASA/TM-20240014203, Fig. 2, p. 4 [F70]; conferi
    os valores na imagem da página.
  - Também conferidos: a filosofia de margens da ESA (SRE-PA/2011.097, p. 5 [F71]) e a GSFC-STD-1000
    Rev I (Tab. 1.06-1, p. 10 [F72]).

## 2. Fronteiras (sem dupla contagem)

| Fica fora da plataforma | Onde já está |
| :- | :- |
| Tanques, motores, estrutura dos estágios do orbitador | fração estrutural ε dos estágios |
| Propulsão seca do Odyssey (49,7 kg) | idem; excluída da lista |
| Captura, contenção, montagem e cápsula | carga útil CU-2 (709,9 kg até Marte) |
| Instrumentos do Odyssey (44,5 kg) | excluídos (a carga útil é a CU-2) |
| Aeroshell, paraquedas e propelente de descida do lander | razão pousada/entrada (P-018) |
| MAV, o aquecimento dele e a energia desse aquecimento | bloco do MAV (O4, energia solar) |

Sobreposições que restam, todas para o lado conservador:
1. A estrutura do Odyssey inclui o módulo de propulsão, que também está em parte no ε dos estágios.
2. O "restante de energia" do Odyssey e o núcleo do Phoenix ainda contêm os seus próprios painéis e
   baterias. Os painéis e baterias dimensionados aqui são somados por cima.
3. O núcleo do Phoenix inclui a propulsão de descida seca. Se a razão P-018 (tirada do SRL) já cobrir
   essa massa, há dupla contagem. A fonte não deixa claro o que a "capacidade de 2900 kg" do SRL
   inclui [F41].

## 3. Orbitador (massas em kg)

| Subsistema | Básica | Análogo e fonte | Categoria S-120A | MGA (ponto médio de E1) | Prevista |
| :- | -: | :- | :- | -: | -: |
| Estrutura | 81,7 | Odyssey, p. 30 [F63] | estrutura primária | 21,5 % | 99,3 |
| Controle térmico | 20,3 | Odyssey, p. 30 | controle térmico | 40,0 % | 28,4 |
| Comunicação (X + UHF, relé) | 23,9 | Odyssey, p. 28 | eletrônica 0–5 kg | 27,5 % | 30,5 |
| Comando e dados | 11,1 | Odyssey, p. 28 | eletrônica 5–15 kg | 20,0 % | 13,3 |
| GNC | 23,4 | Odyssey, p. 28 | eletrônica 5–15 kg | 20,0 % | 28,1 |
| Mecanismos | 24,2 | Odyssey, p. 31 | mecanismos | 21,5 % | 29,4 |
| Painel solar | 29,3 | calculado (abaixo) | painel solar | 27,5 % | 37,4 |
| Bateria | 58,5 | calculado (abaixo) | baterias | 22,5 % | 71,7 |
| Restante de energia | 67,2 | Odyssey: 86,0 − 1500 W/80 W/kg | eletrônica > 15 kg | 15,0 % | 77,3 |
| Cabeamento | 55,2 | 5 % da massa seca nominal [F71] (P-031) | cabeamento | 75,0 % | 96,7 |
| **Total** | **394,9** | | | | **512,0** |

**Energia:**
- **Órbita e eclipse.** Órbita de 300 × 26.950 km, com período de 18,73 h. O pior eclipse dura **3,44 h**:
  sombra cilíndrica, Sol no plano da órbita, apoapse atrás de Marte. É o pior caso geométrico.
- **Carga: 510 W** no sol e no eclipse (P-028).
  - Barramento do Mars Express no modo de comunicação: 445 W [F68].
  - Electra em full duplex: 65 W [F69].
- **Painel: 654 W no afélio** (1,666 UA [F56]), com eficiência de recarga de 0,8 (P-029).
  - Potência específica de 80 W/kg a 1 UA [F55], vezes 0,774 de perdas (P-030, do MRO [F65]), dividida
    por d²: dá **22,3 W/kg**.
  - O enunciado fala em ~1,52 UA. Usei o afélio por ser o pior caso; a 1,524 UA o painel cai ~16 %.
- **Bateria: 1755 Wh no eclipse.**
  - Profundidade de descarga de 30 % [F73]: 5851 Wh nominais.
  - A 100 Wh/kg [F73], são 58,5 kg.
  - Análogos: TGO ~5100 Wh; MRO 2 × 50 Ah, com "only about 40%" usados [F66]; MGS limitado a 27 % [F67].

**Comparação topo-para-baixo**, só como ordem de grandeza:

| Análogo | Massa | O que inclui |
| :- | -: | :- |
| Odyssey | 282,1 | seco sem propulsão e sem instrumentos |
| Mars Express | 439 | barramento, com propulsão [F68] |
| MRO | 892 | "outros secos", com propulsão [F65] |
| ERO | 2200 | módulo principal, com propulsão elétrica e painéis de 41 kW [F22] |

A lista deste estudo dá 395 kg de massa básica e 512 kg de prevista.

## 4. Lander (massas em kg)

**Itens comuns às duas opções:**

| Subsistema | Básica | Análogo e fonte | Categoria | MGA | Prevista |
| :- | -: | :- | :- | -: | -: |
| UHF (relé com o orbitador) | 6,5 | Phoenix [F74] | eletrônica 0–5 kg | 27,5 % | 8,3 |
| Banda X (cruzeiro) | 14,7 | Phoenix [F74] | eletrônica 0–5 kg | 27,5 % | 18,7 |
| Radar de pouso | 5,0 | Phoenix [F74] | eletrônica 0–5 kg | 27,5 % | 6,4 |
| Coleta e transferência de amostras | 59,0 | carga útil do Phoenix [F40] (P-034) | instrumentação | 50,0 % | 88,5 |
| Painel solar (4,2 m²) | 17,3 | rendimento do Phoenix [F75][F76]; 330 W/m² e 80 W/kg [F55] | painel solar | 27,5 % | 22,1 |
| Bateria | 58,3 | 1750 Wh na noite, 30 %, 100 Wh/kg [F73] | baterias | 22,5 % | 71,5 |

**Núcleo do Phoenix** = 410 − 67 − 59 − 26,2 = **257,8 kg** [F40][F74]. Inclui estrutura, pernas,
térmico, comando e dados, GNC, propulsão de descida seca e cabeamento.

| Opção (P-035) | Núcleo básico | Núcleo previsto (21,5 %) | **Plataforma prevista** |
| :- | -: | -: | -: |
| **L1**: núcleo do Phoenix sem escala | 257,8 | 313,2 | **529** |
| **L2**: núcleo = 75,2 % da massa pousada seca, como no Phoenix | 1351,4 | 1642,0 | **1857** |

- **L1** é otimista: o Phoenix sustenta 59 kg de carga, e aqui o lander leva ~300 kg de MAV com o
  aquecimento dele.
- **L2** é pessimista: escala com a massa coisas que não crescem com ela, como aviônica e comunicação.
- **Comparação com o SRL:** ≤ 2100 kg secos na superfície [F77], menos o MAV de 400 kg [F35] e o SFR de
  < 230 kg [F78], dá ~1470 kg ou mais. Esse número inclui itens do MSR que talvez não se apliquem aqui
  (braço de transferência, helicópteros, MLS).

**Energia do lander:**
- 3500 Wh/sol, 142 W médios (P-032), igual à geração do Phoenix [F76].
- Metade do sol é noite.
- Não estão modelados: poeira, tempestades e estação do ano.
- O sistema de lançamento e ereção do MAV (MLS) **não está incluído**: não tem massa publicada.

## 5. Margem: critérios lado a lado

| Critério | Orbitador | Lander L1 | Lander L2 |
| :- | -: | -: | -: |
| S-120A, E1, ponto médio (base, P-033) | 512 | 529 | 1857 |
| S-120A, E1, mínimo | 482 | 500 | 1791 |
| S-120A, E1, máximo | 542 | 557 | 1924 |
| E1 médio + 15 % da básica (GSFC, pré-Fase A [F72]) | 571 | 591 | 2084 |
| ESA: 20 % no equipamento e 20 % no sistema [F71] | 569 | 603 | 2178 |

A categoria E1 ("Estimated": "parametric analysis, or incomplete requirements" [F70]) é a deste estudo.
Nenhum item tem desenho; todos vêm de análogos.

## 6. Massa total na órbita baixa, antes e depois (kg)

As plataformas novas foram aplicadas à varredura completa da Etapa 2.1, com o MAV O4 solar. A regra
dos 5 % do ADR 0005 foi reaplicada.

| Caso | Plataforma orbitador | Plataforma lander | Total (iii) a 26.950 km | Total (A) a 26.950 km | Apoapse pela regra dos 5 % | Total (iii) nele | Total (A) nele |
| :- | -: | -: | -: | -: | -: | -: | -: |
| **Antes** (P-016 = P-017 = 850) | 850 | 850 | **31.233** | **21.298** | 26.950 | 31.233 | 21.298 |
| **L1**, E1 médio | 512 | 529 | **23.999** | **16.219** | 26.950 | 23.999 | 16.219 |
| L1, E1 mín. / máx. | 482 / 542 | 500 / 557 | 23.356 / 24.642 | 15.768 / 16.670 | 26.950 | 23.356 / 24.642 | 15.768 / 16.670 |
| L1, GSFC | 571 | 591 | 25.307 | 17.149 | 26.950 | 25.307 | 17.149 |
| L1, ESA | 569 | 603 | 25.337 | 17.195 | 26.950 | 25.337 | 17.195 |
| **L2**, E1 médio | 512 | 1857 | **32.165** | **24.385** | **24.992** | 32.552 | 24.572 |
| L2, E1 mín. / máx. | 482 / 542 | 1791 / 1924 | 31.286 / 33.043 | 23.698 / 25.071 | 24.992 | 31.664 / 33.441 | 23.880 / 25.264 |
| L2, GSFC | 571 | 2084 | 34.480 | 26.323 | 24.067 | 35.104 | 26.624 |
| L2, ESA | 569 | 2178 | 35.014 | 26.873 | 24.067 | 35.637 | 27.174 |

**Leitura (sem decisão):**
1. **O orbitador cai de 850 para 482–571 kg.** Esse resultado tem análogo por subsistema e muda pouco
   com o critério de margem.
2. **O lander domina a incerteza.**
   - Com L1, o total cai ~23 % (31,2 → 24,0 t pela regra iii).
   - Com L2, sobe ~3 % (32,2 t) e a regra dos 5 % puxa o apoapse para 24.067–24.992 km.
3. **A faixa L1–L2 (529 a 1857 kg) vem da falta de quebra publicada do lander, não do método.** O
   número do SRL (≥ ~1470 kg) fica perto de L2, mas inclui itens do MSR.
4. **A conta "antes" reproduz exatamente os 31.233 / 21.298 kg da Etapa 2.2.** Isso confere que a
   troca de plataforma é a única mudança.

## 7. Premissas novas (NÃO VALIDADAS)

| Premissa | Conteúdo |
| :- | :- |
| P-028 | Carga do orbitador de 510 W (Mars Express + Electra) |
| P-029 | Eficiência de recarga de 0,8 (sem fonte para Li-ion) |
| P-030 | Fator de perdas do painel de 0,774 (do MRO) |
| P-031 | Cabeamento sobre a plataforma + CU-2 |
| P-032 | Energia do lander: 3500 Wh/sol, metade à noite |
| P-033 | Ponto médio da faixa E1 e a classificação dos subsistemas |
| P-034 | Amostras = carga útil do Phoenix |
| P-035 | Opções L1 e L2 do núcleo do lander |

**P-016 e P-017** (850 kg, média geométrica) **continuam no `config`**, porque só o Fabio muda o status.
As novas plataformas entram como sobreposição em `tools/plataformas.py`. Se aprovadas, P-016 e P-017
passam a ser substituídas pelos valores daqui.

## 8. Limitações

- Potência do sistema de captura (CU-2) não incluída: não tem valor publicado.
- MLS do lander não incluído: não tem massa publicada.
- Odyssey é um orbitador de 725 kg. A estrutura, o GNC (rodas de reação) e o térmico dele não foram
  escalados para um orbitador que chega a Marte com várias toneladas.
- Eclipse no pior caso geométrico, sem penumbra e sem a geometria sazonal real.
- Painel do lander com o rendimento do Phoenix a 68° N, sem poeira.
- A reprodução da tabela do S-120A é de 2024 (NESC). A Rev B da norma está em revisão (NTRS
  20250005278), e a fonte não foi conferida contra o texto pago da norma.
