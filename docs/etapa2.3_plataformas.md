# Etapa 2.3: plataformas do orbitador e do lander

Estado: **decidida pelo Fabio no portão da Etapa 2.3** (2026-10-27). Resultados em
`results/etapa2.3/plataformas.md` e `.yaml`, gerados por `tools/plataformas.py` a partir de
`config/plataformas.yaml`.

## Decisões do portão

| Item | Decisão | Onde |
| :- | :- | :- |
| Orbitador | Lista por subsistema desta etapa, margem média da categoria E1 do S-120A: **442,3 kg** | P-016, `config/dimensionamento.yaml` |
| Lander | Base = **L3** (lander do MSR sem MAV e sem rover de busca, 1470 kg) **+ amostras da P-034 como alocação provisória** (88,5 kg): **1558,5 kg**. Faixa de L1 (529 kg) ao SRL 2024 − MAV (~2500 kg, comparabilidade não confirmada); L2 só como referência | P-017, P-034, P-035, `config/superficie.yaml` |
| Margem | Ponto médio da E1 na base; GSFC (+15 %) e ESA na sensibilidade | P-033 |
| Cabeamento | Base corrigida: só a plataforma (seção 3) | P-031 |
| Órbita de encontro | Regra dos 5 % reaplicada: **300 × 24.992 km** | ADR 0005 (atualização) |
| RSS do orbitador | Lacuna declarada, sem número; massa publicada do RSS é pesquisa da Etapa 2.5 | seção 7 |
| Coleta de amostras | Conceito (braço no lander, rover próprio, outro) e objetivo científico (solo no sítio × rochas selecionadas) ficam para a Etapa 2.5, decisão do Fabio | seção 7 |
| SRL 2024 | Documento com massa seca: pesquisa da Etapa 2.5 | seção 7 |

`tests/test_plataforma.py` confere que os valores do `config` são os calculados pela ferramenta.

## 1. O que existe publicado

- **Orbitador.**
  - Só o **Mars Odyssey** tem massa publicada por subsistema (press kit, pp. 28–31 [F33]).
  - Do MRO, só a comunicação (107,7 kg [F64]).
  - Do MAVEN, Mars Express, TGO, MGS, MCO e ERO, só totais. Massas por subsistema desses veículos não
    foram encontradas em fonte primária.
- **Lander.**
  - **Nenhum** lander de Marte (Phoenix, InSight, Viking, MPL, SRL) tem a lista completa por subsistema
    em fonte primária pública.
  - Existem a comunicação e o radar do Phoenix (DESCANSO, Tab. 2-16, p. 70 [F74]) e totais.
  - Para o SRL há só alocações de topo [F77][F78][F35].
- **Margem.**
  - O AIAA S-120A-2015 é pago e não foi lido.
  - A Tabela 1 dele está reproduzida pela NASA (NASA/TM-20240014203, Fig. 2, p. 4 [F70]); conferi os
    valores na imagem da página.
  - Também conferidos: a filosofia de margens da ESA (SRE-PA/2011.097, p. 5 [F71]) e a GSFC-STD-1000
    Rev I (Tab. 1.06-1, p. 10 [F72]).

## 2. Fronteiras (sem dupla contagem)

| Fica fora da plataforma | Onde já está |
| :- | :- |
| Tanques, motores e estrutura dos estágios do orbitador | fração estrutural ε dos estágios |
| Propulsão seca do Odyssey (49,7 kg) | idem; excluída da lista |
| Captura, contenção, montagem e cápsula | carga útil CU-2 (709,9 kg até Marte) |
| Instrumentos do Odyssey (44,5 kg) | excluídos (a carga útil é a CU-2) |
| Aeroshell, paraquedas e propelente de descida do lander | razão pousada/entrada (P-018) |
| MAV, aquecimento dele e energia desse aquecimento | bloco do MAV (O4, energia solar) |

Sobreposições que restam, todas para o lado conservador:
1. A estrutura do Odyssey inclui a do módulo de propulsão.
2. O "restante de energia" do Odyssey ainda contém a bateria dele.
3. O L3 (SRL) inclui o controle térmico do MAV do MSR. O aquecimento do MAV daqui também está no bloco
   do MAV.

## 3. Cabeamento: o que estava errado e a correção

- **Primeira versão (portão).** Básica de 55,2 kg e prevista de 96,7 kg. Dois efeitos somados:
  1. **A MGA de 75 % é a da norma.** O cabeamento tem a faixa E1 mais alta da Tabela 1 do S-120A
     (50–100 % [F70]); o ponto médio é 75 %. Isso não é erro.
  2. **A base incluía a CU-2.** A regra de 5 % [F71] era aplicada sobre plataforma + CU-2.
     - 37,4 kg dos 55,2 kg básicos vinham da CU-2 (0,05/0,95 × 709,9 kg).
     - Com isso, a margem de 75 % incidia sobre massa derivada da carga útil.
- **Correção (P-031).** A base passa a ser só a plataforma. A CU-2 é uma alocação de carga útil que
  já traz o seu cabeamento, e o ε dos estágios já inclui o deles.
- **Resultado:** cabeamento de **17,7 kg básicos e 31,0 kg previstos**, contra 96,7 kg antes.

## 4. Orbitador, na órbita de 300 × 24.992 km (massas em kg)

| Subsistema | Básica | Análogo e fonte | Categoria S-120A | MGA (E1 média) | Prevista |
| :- | -: | :- | :- | -: | -: |
| Estrutura | 81,7 | Odyssey, p. 30 [F33] | estrutura primária | 21,5 % | 99,3 |
| Controle térmico | 20,3 | Odyssey, p. 30 | controle térmico | 40,0 % | 28,4 |
| Comunicação (X + UHF, relé) | 23,9 | Odyssey, p. 28 | eletrônica 0–5 kg | 27,5 % | 30,5 |
| Comando e dados | 11,1 | Odyssey, p. 28 | eletrônica 5–15 kg | 20,0 % | 13,3 |
| GNC | 23,4 | Odyssey, p. 28 | eletrônica 5–15 kg | 20,0 % | 28,1 |
| Mecanismos | 24,2 | Odyssey, p. 31 | mecanismos | 21,5 % | 29,4 |
| Painel solar | 29,5 | calculado | painel solar | 27,5 % | 37,6 |
| Bateria | 55,0 | calculado | baterias | 22,5 % | 67,4 |
| Restante de energia | 67,2 | Odyssey: 86,0 − 1500 W / 80 W/kg | eletrônica > 15 kg | 15,0 % | 77,3 |
| Cabeamento | 17,7 | 5 % da plataforma [F71] (P-031) | cabeamento | 75,0 % | 31,0 |
| **Total** | **354,1** | | | | **442,3** |

**Energia:**
- **Eclipse:** o pior dura **3,24 h** num período de 17,14 h, com sombra cilíndrica e o Sol no plano
  da órbita (pior caso geométrico).
- **Carga:** 510 W no sol e no eclipse (P-028). É a soma do barramento do Mars Express no modo de
  comunicação, 445 W [F68], com o Electra em full duplex, 65 W [F69].
- **Painel:** 658 W no afélio (1,666 UA [F56]).
  - Recarga com eficiência de 0,8 (P-029).
  - Potência específica: 80 W/kg a 1 UA [F55] × 0,774 (P-030, do MRO [F65]) ÷ d² = **22,3 W/kg**.
- **Bateria:** 1650 Wh no eclipse.
  - Com 30 % de profundidade de descarga [F73], são 5500 Wh nominais.
  - A 100 Wh/kg [F73], dá 55,0 kg.

**Iteração.** A bateria depende do eclipse e, portanto, do apoapse.
- No apoapse de 26.950 km a plataforma tinha 446,6 kg; a regra dos 5 % levou o apoapse a 24.992 km.
- Ali a plataforma tem 442,3 kg e a regra mantém os 24.992 km: convergiu em duas iterações.

**Comparação topo-para-baixo** (ordem de grandeza):

| Análogo | Massa | O que inclui |
| :- | -: | :- |
| Odyssey | 282,1 kg | seco, sem propulsão e sem instrumentos |
| Mars Express | 439 kg | barramento, com propulsão [F68] |
| MRO | 892 kg | "outros secos", com propulsão [F65] |
| ERO | 2200 kg | com propulsão elétrica [F22] |

## 5. Lander (massas em kg)

**Base (P-017): 1558,5 kg** = L3 + amostras.

**L3: 1470 kg**, lander do MSR sem MAV e sem rover de busca.
- **Conta:** até 2100 kg secos na superfície ("as much as 2100 kg of dry mass to the surface" [F77]),
  menos o MAV de 400 kg [F35] e o rover de busca (SFR, "Mass = < 230 kg" [F78]).
- **É um limite inferior dessa conta:** como o SFR é "< 230 kg", um SFR mais leve daria um L3 maior.
- **Sem margem adicional no caso de base:** é um valor de alocação.
- **Cobre ao menos parte do sistema de lançamento e ereção do MAV (MLS)**, que não tem massa publicada.
- **Incerteza declarada:** os itens próprios do MSR, como o braço de transferência de amostras e o apoio
  aos helicópteros.
- **Fonte de 2020:** o documento do SRL só tem o resumo público.

**Amostras: 88,5 kg**, ALOCAÇÃO PROVISÓRIA.
- É o item da P-034: carga útil do Phoenix (braço e instrumentos [F40]), 59 kg com MGA E1 de 50 %.
- Entra porque o L3 tira o rover de busca e nada mais coleta amostras.
- O conceito de coleta e o objetivo científico ficam para a Etapa 2.5.

**Base com margem alternativa:**
- GSFC: 1787,9 kg (L3 × 1,15 + amostras com E1 e 15 %).
- ESA: 2201,8 kg ((1470 + 59) × 1,44).

**Limite superior da faixa: SRL de 2024 − MAV ≈ 2500 kg, COMPARABILIDADE NÃO CONFIRMADA.**
- Conta: ~2900 kg ("nearly 1100 kg capability for Mars2020 vs 2900 kg for SRL", [F41] p. 1) menos o
  MAV de 400 kg [F35].
- A fonte fala em carga pousada, não em massa seca. Não se sabe se é a mesma grandeza dos 2100 kg
  "secos" de 2020.
- Documento do SRL 2024 com massa seca: pesquisa da Etapa 2.5.

**Limite inferior L1 e referência L2 (P-035), por subsistema:**

| Subsistema | Básica | Análogo e fonte | Categoria | MGA | Prevista |
| :- | -: | :- | :- | -: | -: |
| Núcleo do Phoenix (L1, sem escala) | 257,8 | 410 − 67 − 59 − 26,2 [F40][F74] | estrutura primária | 21,5 % | 313,2 |
| Núcleo escalado (L2, 75,2 % da massa pousada seca) | 1351,4 | idem | estrutura primária | 21,5 % | 1642,0 |
| UHF (relé com o orbitador) | 6,5 | Phoenix [F74] | eletrônica 0–5 kg | 27,5 % | 8,3 |
| Banda X (cruzeiro) | 14,7 | Phoenix [F74] | eletrônica 0–5 kg | 27,5 % | 18,7 |
| Radar de pouso | 5,0 | Phoenix [F74] | eletrônica 0–5 kg | 27,5 % | 6,4 |
| Amostras | 59,0 | carga útil do Phoenix [F40] (P-034) | instrumentação | 50,0 % | 88,5 |
| Painel solar (4,2 m²) | 17,3 | Phoenix [F40][F76]; [F55] | painel solar | 27,5 % | 22,1 |
| Bateria | 58,3 | 1750 Wh na noite [F73] | baterias | 22,5 % | 71,5 |
| **L1 / L2** | 418,7 / 1512,3 | | | | **529 / 1857** |

A base (1558,5 kg) fica dentro da faixa de 529 a ~2500 kg, entre o L2 (1857 kg) e o L1.

## 6. Massa total na órbita baixa, antes e depois (kg)

A regra dos 5 % do ADR 0005 foi reaplicada em todos os casos. O mínimo da varredura fica no extremo
(33.793 km) em todos eles.

| Caso | Plataforma orbitador | Plataforma lander | Apoapse pela regra dos 5 % | **Total (iii)** | **Total (A)** |
| :- | -: | -: | -: | -: | -: |
| Antes (P-016 = P-017 = 850) | 850 | 850 | 26.950 | 31.233 | 21.298 |
| **Base: orbitador E1 médio + L3 + amostras** | **442** | **1558,5** | **24.992** | **29.607** | **22.083** |
| *Faixa de margens* | | | | | |
| Orbitador E1 mínimo | 422 | 1558,5 | 24.992 | 29.279 | 21.890 |
| Orbitador E1 máximo | 463 | 1558,5 | 24.992 | 29.935 | 22.276 |
| GSFC: +15 % nos dois | 495 | 1788 | 24.992 | 31.861 | 23.989 |
| ESA: 20 % × 20 % nos dois | 510 | 2202 | 24.067 | 34.840 | 26.767 |
| *Faixa do lander (orbitador E1 médio)* | | | | | |
| Limite inferior: L1 | 442 | 529 | 26.950 | 22.914 | 15.579 |
| Limite superior: SRL 2024 − MAV (comparabilidade não confirmada) | 442 | 2500 | 23.176 | 35.788 | 28.058 |
| Referência: L2 (antigo limite superior) | 442 | 1857 | 24.067 | 31.637 | 24.013 |

- **No caso de base:**
  - O total pela regra (iii) cai 5,2 % (31.233 → 29.607 kg), 4,6 % acima do mínimo de 28.309 kg.
  - O total da missão A sobe 3,7 % (21.298 → 22.083 kg).
- **Por que os dois andam em sentidos opostos:**
  - O orbitador ficou 408 kg mais leve, e ele pesa mais na regra (iii), que usa a pior janela de volta.
  - O lander ficou 708,5 kg mais pesado.
- **Para comparar no apoapse antigo** (26.950 km), o caso de base dá 29.243 kg (iii) e 21.907 kg (A).
- **Primeiro portão desta etapa** (L3 sem amostras, 1470 kg): mesmo apoapse, 29.063 kg (iii) e
  21.539 kg (A).
- **Nos casos de sensibilidade,** a plataforma do orbitador é a calculada no apoapse do caso de base.
- **A conta "antes" reproduz exatamente os 31.233 / 21.298 kg da Etapa 2.2.**

## 7. Lacunas e decisões sobre a revisão independente

1. **Sensores de encontro (RSS) do orbitador: lacuna declarada, sem número.**
   - **Verificado agora:** os 620 kg do CCRS de 2024 (CU-2) **não** incluem o RSS.
     - A fonte diz que são "composed of the capture, assembly and micrometeoroid enclosures with
       approximate masses of 240 kg, 280 kg, and 100 kg" ([F23] p. 5).
     - "detect and rendezvous with the OS" é objetivo da missão ERO, não do CCRS (p. 3).
     - O RSS só aparece na lista de siglas do artigo.
   - A lista do Odyssey também não o tem. Logo, o RSS está fora das duas contas.
   - Massa publicada do RSS do ERO ou de outro análogo: pesquisa da Etapa 2.5. Nenhum número sem fonte.
2. **Coleta de amostras: alocação provisória.**
   - O item da P-034 (88,5 kg previstos) foi somado ao L3.
   - O conceito (braço no lander, rover próprio, outro) e o objetivo científico (solo no sítio ×
     rochas selecionadas) ficam para a Etapa 2.5, como decisão do Fabio.
3. **SRL 2024:**
   - O limite superior da faixa do lander passa a ~2500 kg, com comparabilidade não confirmada.
   - Pesquisa de documento do SRL 2024 com massa seca: Etapa 2.5.

## 8. Resultados de etapas anteriores e dependências da ferramenta

- **Etapas 1.4, 2.1 e 2.2:** os resultados (`results/etapa1.4`, `etapa2.1`, `etapa2.2`) foram gerados
  com P-016 = P-017 = 850 kg.
  - Ficam como registro dessas etapas e não foram regenerados.
  - Se as ferramentas delas forem rodadas de novo, usarão as plataformas novas do `config`.
- **Arquivos que `tools/plataformas.py` lê, sem recalcular:**
  - `results/etapa2.1/varredura_encontro_rp300_O4.yaml`: o apoapse e o Δv do MAV antes desta etapa.
    Servem de ponto de partida da iteração, das colunas "no apoapse anterior" e do MAV da referência L2.
  - `results/etapa2.2/mav_propulsao.yaml`: a opção e a fonte de energia do MAV.
- **Efeito de regenerar essas etapas:** o ponto de partida muda.
  - A iteração converge no mesmo apoapse se as plataformas forem as mesmas.
  - O caso "antes" usa 850/850 explícitos e não depende delas.

## 9. Premissas (NÃO VALIDADAS)

| Premissa | Conteúdo |
| :- | :- |
| P-016 | Revista: 442,3 kg |
| P-017 | Revista: 1558,5 kg (L3 + amostras provisórias); faixa 529 a ~2500 kg |
| P-028 | Carga de 510 W |
| P-029 | Eficiência de recarga de 0,8 |
| P-030 | Fator de perdas do painel de 0,774 |
| P-031 | Revista: cabeamento só sobre a plataforma |
| P-032 | Energia do lander (limites L1/L2) |
| P-033 | Ponto médio da E1 |
| P-034 | Amostras = carga útil do Phoenix (base provisória e limites L1/L2) |
| P-035 | L1 limite inferior; SRL 2024 − MAV limite superior; L2 referência |

## 10. Limitações

- Potência do sistema de captura (CU-2) não incluída: não tem valor publicado.
- O L3 é uma alocação de 2020 com só o resumo público. O conteúdo exato da massa "seca na superfície"
  não está publicado.
- Sensores de encontro (RSS) sem massa: fora das contas do orbitador e da CU-2.
- A estrutura, o GNC e o térmico do Odyssey (725 kg no lançamento) não foram escalados.
- Eclipse no pior caso geométrico. Painel do lander (limites L1/L2) sem poeira.
- A tabela do S-120A é a reproduzida pelo NESC (2024). A Rev B da norma está em revisão (NTRS
  20250005278).

## Atualização (Etapa 2.5, 2026-10-27): sensores de encontro alocados
Pedido do Fabio na Etapa 2.5: os sensores de encontro (RSS), que estavam como lacuna, foram alocados na lista
do orbitador.
- Duas câmeras de ângulo estreito do ERO, 2 × 14,5 kg [F88].
- LIDAR análogo (RVS3000-3D), ca. 13 kg [F89].
- Margem E1 de 20 % nos dois.

Antes → depois (`results/etapa2.3/plataformas.yaml`):

| Item | Antes | Depois |
| :- | -: | -: |
| Plataforma do orbitador (prevista) | 442,3 kg | **496,5 kg** |
| Total pela regra (iii) | 29.607 kg | **30.470 kg** |
| Total na missão A | 22.083 kg | **22.590 kg** |

- O apoapse da regra dos 5 % não muda (24.992 km).
- A câmera de ângulo largo e a potência do RSS seguem como lacuna.
- Os números das seções acima são os de antes desta atualização.

## Atualização (Etapa 2.5, 2026-10-27): helicópteros de coleta no lander (ADR 0009)
A plataforma do lander passa de 1558,5 para **1564,9 kg**, com 2 helicópteros de 2,5 kg cada [F98] e margem E1.
O braço (P-034) deixa de ser provisório: vira a coleta de reserva.

| Item | Antes | Depois |
| :- | -: | -: |
| Total pela regra (iii) | 30.470 kg | **30.509 kg** |
| Total na missão A | 22.590 kg | **22.630 kg** |

O apoapse não muda (24.992 km). Fonte: `results/etapa2.3/plataformas.yaml`.

## Nota (2026-10-27): redimensionamento da Etapa 3.1 (ADR 0011)
- Desde o ADR 0011, `results/etapa2.3/plataformas.md` sai com os motores da Etapa 3.1 (Isp de 310 s e 292 s, perdas
  calculadas).
- A linha "Antes (P-016 = P-017 = 850 kg)" usa as plataformas de 850 kg com essa propulsão nova (35.630 / 23.799 kg).
  Ela não reproduz mais os 31.233 / 21.298 kg da Etapa 2.2; a frase da §6 sobre isso vale para a propulsão da época.
- Os números vigentes estão na errata de 2026-10-27 de `docs/fase2_relatorio.md`.

## Nota (2026-10-28): ε do MAV pressurizado (ADR 0007)
Com ε = 0,230 no MAV, a linha "Antes (P-016 = P-017 = 850 kg)" de `results/etapa2.3/plataformas.md` passa a dar
35.412 / 23.580 kg (a nota de 2026-10-27 citava 35.630 / 23.799 kg). Os números vigentes estão na errata de 2026-10-28
de `docs/fase2_relatorio.md` e em `results/`.

## Nota (Etapa 4.1, 2026-10-31): carga do orbitador de 1.022 W e captura C4
A carga do orbitador passou a 1.022 W (P-028, ADR 0015), e a captura proposta passou a 10 × R-4D-11 (C4, P-055). Os
números de massa, de órbita de encontro, de perdas e de margens deste documento mudaram. **Os números vigentes estão na
errata de 2026-10-31 de `docs/fase3_relatorio.md`.**
