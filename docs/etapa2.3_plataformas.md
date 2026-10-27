# Etapa 2.3: plataformas do orbitador e do lander

Estado: **decidida pelo Fabio no portão da Etapa 2.3** (2026-10-27). Resultados em
`results/etapa2.3/plataformas.md` e `.yaml`, gerados por `tools/plataformas.py` a partir de
`config/plataformas.yaml`.

## Decisões do portão

| Item | Decisão | Onde |
| :- | :- | :- |
| Orbitador | Lista por subsistema desta etapa, margem média da categoria E1 do S-120A: **442,3 kg** | P-016, `config/dimensionamento.yaml` |
| Lander | Base **L3** = lander do MSR sem MAV e sem rover de busca: **1470 kg**; L1 e L2 ficam como limites | P-017, `config/superficie.yaml` |
| Margem | Ponto médio da E1 na base; GSFC (+15 %) e ESA na sensibilidade | P-033 |
| Cabeamento | Base corrigida: só a plataforma (seção 3) | P-031 |
| Órbita de encontro | Regra dos 5 % reaplicada: **300 × 24.992 km** | ADR 0005 (atualização) |

`tests/test_plataforma.py` confere que os valores do `config` são os calculados pela ferramenta.

## 1. O que existe publicado

- **Orbitador.**
  - Só o **Mars Odyssey** tem massa publicada por subsistema (press kit, pp. 28–31 [F63]).
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
| Estrutura | 81,7 | Odyssey, p. 30 [F63] | estrutura primária | 21,5 % | 99,3 |
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

**Base L3 (P-017): 1470 kg**, lander do MSR sem MAV e sem rover de busca.
- **Conta:** até 2100 kg secos na superfície ("as much as 2100 kg of dry mass to the surface" [F77]),
  menos o MAV de 400 kg [F35] e o rover de busca (SFR, "Mass = < 230 kg" [F78]).
- **É um limite inferior dessa conta:** como o SFR é "< 230 kg", um SFR mais leve daria um L3 maior.
- **Sem margem adicional no caso de base:** é um valor de alocação.
  - Com GSFC (+15 %), vira 1690 kg.
  - Com ESA (× 1,2 × 1,2), vira 2117 kg.
- **Cobre ao menos parte do sistema de lançamento e ereção do MAV (MLS)**, que não tem massa publicada.
- **Incerteza declarada:** os itens próprios do MSR, como o braço de transferência de amostras e o apoio
  aos helicópteros. O valor é de 2020; versões posteriores do SRL não foram comparadas.
- **Fonte de 2020:** o documento do SRL só tem o resumo público.
- **Dado posterior já no repositório:** em 2024, o SRL aparece com ~2900 kg pousados [F41] (o antigo teto da P-017).
  Menos o MAV de 400 kg, dá ~2500 kg, acima do limite L2 (1857 kg). Não se sabe se os 2900 kg são comparáveis aos
  2100 kg "secos" de 2020.

**Limites da faixa (P-035), por subsistema:**

| Subsistema | Básica | Análogo e fonte | Categoria | MGA | Prevista |
| :- | -: | :- | :- | -: | -: |
| Núcleo do Phoenix (L1, sem escala) | 257,8 | 410 − 67 − 59 − 26,2 [F40][F74] | estrutura primária | 21,5 % | 313,2 |
| Núcleo escalado (L2, 75,2 % da massa pousada seca) | 1351,4 | idem | estrutura primária | 21,5 % | 1642,0 |
| UHF (relé com o orbitador) | 6,5 | Phoenix [F74] | eletrônica 0–5 kg | 27,5 % | 8,3 |
| Banda X (cruzeiro) | 14,7 | Phoenix [F74] | eletrônica 0–5 kg | 27,5 % | 18,7 |
| Radar de pouso | 5,0 | Phoenix [F74] | eletrônica 0–5 kg | 27,5 % | 6,4 |
| Amostras | 59,0 | carga útil do Phoenix [F40] (P-034) | instrumentação | 50,0 % | 88,5 |
| Painel solar (4,2 m²) | 17,3 | Phoenix [F75][F76]; [F55] | painel solar | 27,5 % | 22,1 |
| Bateria | 58,3 | 1750 Wh na noite [F73] | baterias | 22,5 % | 71,5 |
| **L1 / L2** | 418,7 / 1512,3 | | | | **529 / 1857** |

O L3 (1470 kg) fica dentro da faixa, perto do L2.

## 6. Massa total na órbita baixa, antes e depois (kg)

A regra dos 5 % do ADR 0005 foi reaplicada em todos os casos. O mínimo da varredura fica no extremo
(33.793 km) em todos eles.

| Caso | Plataforma orbitador | Plataforma lander | Apoapse pela regra dos 5 % | **Total (iii)** | **Total (A)** |
| :- | -: | -: | -: | -: | -: |
| Antes (P-016 = P-017 = 850) | 850 | 850 | 26.950 | 31.233 | 21.298 |
| **Base: orbitador E1 médio + L3** | **442** | **1470** | **24.992** | **29.063** | **21.539** |
| GSFC: +15 % nos dois | 495 | 1690 | 24.992 | 31.262 | 23.391 |
| ESA: 20 % × 20 % nos dois | 510 | 2117 | 24.067 | 34.318 | 26.245 |
| Orbitador E1 mínimo + L3 | 422 | 1470 | 24.992 | 28.735 | 21.346 |
| Orbitador E1 máximo + L3 | 463 | 1470 | 24.992 | 29.391 | 21.732 |
| Limite inferior do lander (L1) | 442 | 529 | 26.950 | 22.914 | 15.579 |
| Limite superior do lander (L2) | 442 | 1857 | 24.067 | 31.637 | 24.013 |

- **No caso de base:**
  - O total pela regra (iii) cai 7 % (31.233 → 29.063 kg), 4,7 % acima do mínimo de 27.765 kg.
  - O total da missão A sobe 1 % (21.298 → 21.539 kg).
- **Por que os dois andam em sentidos opostos:**
  - O orbitador ficou 408 kg mais leve, e ele pesa mais na regra (iii), que usa a pior janela de volta.
  - O lander ficou 620 kg mais pesado.
- **Para comparar no apoapse antigo** (26.950 km), o caso de base dá 28.699 kg (iii) e 21.364 kg (A).
- **Nos casos de sensibilidade,** a plataforma do orbitador é a calculada no apoapse do caso de base.
- **A conta "antes" reproduz exatamente os 31.233 / 21.298 kg da Etapa 2.2.**

## 7. Lacunas apontadas na revisão independente (decisão do Fabio)

1. **Sensores de encontro (RSS) do orbitador sem alocação.**
   - A P-016 antiga (850 kg) dizia que a plataforma os levava, porque o CCRS de 2021 é "w/o RSS" [F22].
   - A lista nova vem do Odyssey, que não tinha RSS.
   - Não se sabe se os 620 kg do CCRS de 2024 (CU-2 [F23]) os incluem.
   - O RSS pode ter ficado fora das duas contas.
2. **A base L3 não tem coleta nem busca de amostras.**
   - O L3 tira o rover de busca do MSR (230 kg).
   - O item "amostras" (P-034: 59 kg básicos, 88,5 kg previstos) só entra nos limites L1 e L2.
   - O braço do SRL só transfere tubos já coletados. O conceito de coleta deste estudo não está definido.

## 8. Resultados de etapas anteriores

Os resultados das Etapas 1.4, 2.1 e 2.2 (`results/etapa1.4`, `etapa2.1`, `etapa2.2`) foram gerados com
P-016 = P-017 = 850 kg. Eles ficam como registro dessas etapas e não foram regenerados. Se as
ferramentas delas forem rodadas de novo, usarão as plataformas novas do `config`.

## 9. Premissas (NÃO VALIDADAS)

| Premissa | Conteúdo |
| :- | :- |
| P-016 | Revista: 442,3 kg |
| P-017 | Revista: 1470 kg |
| P-028 | Carga de 510 W |
| P-029 | Eficiência de recarga de 0,8 |
| P-030 | Fator de perdas do painel de 0,774 |
| P-031 | Revista: cabeamento só sobre a plataforma |
| P-032 | Energia do lander (limites L1/L2) |
| P-033 | Ponto médio da E1 |
| P-034 | Amostras = carga útil do Phoenix (só nos limites L1 e L2) |
| P-035 | L1 e L2 como limites; L3 como base |

## 10. Limitações

- Potência do sistema de captura (CU-2) não incluída: não tem valor publicado.
- O L3 é uma alocação de 2020 com só o resumo público. O conteúdo exato da massa "seca na superfície"
  não está publicado.
- A estrutura, o GNC e o térmico do Odyssey (725 kg no lançamento) não foram escalados.
- Eclipse no pior caso geométrico. Painel do lander (limites L1/L2) sem poeira.
- A tabela do S-120A é a reproduzida pelo NESC (2024). A Rev B da norma está em revisão (NTRS
  20250005278).
