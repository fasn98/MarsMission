# Arquitetura integrada (gerado por tools/arquitetura.py)

Missão de referência 2028-conjuncao; órbita de encontro 300 × 24 992 km; envelope de Δv 5,912 km/s; injeção direta (ADR 0008); 2 lançamentos. Massas em kg.

## Orbitador (regra iii)

| Item | Propelente | Inerte / massa |
| :- | -: | -: |
| Estágio de inserção em Marte (MMH/MON) | 2 990 | 944 |
| Estágio de retorno (MMH/MON) | 1 569 | 496 |
| Carga útil CU-2: CCRS (captura + montagem + proteção contra micrometeoroides) | — | 620 |
| Carga útil CU-2: EEV com COS (valor máximo esperado) | — | 90 |
| Plataforma (P-016, lista por subsistema + sensores de encontro) | — | 496 |
| **Massa injetada** | | **7 205** |

## Lander

| Item | Propelente | Inerte / massa |
| :- | -: | -: |
| Estágio de cruzeiro (correções de trajetória) | 99 | 31 |
| Sistema de entrada, descida e pouso (aeroshell, paraquedas, propelente de descida; P-018) | — | 1 898 |
| Plataforma de superfície L3 (lander do MSR sem MAV e sem rover de busca) | — | 1 470 |
| Braço de coleta de reserva (P-034, com margem) | — | 88 |
| Helicópteros de recuperação (ADR 0009, com margem) | — | 6 |
| MAV hipergólico + energia do aquecimento (ADR 0007) | — | 403 |
| Painéis do armazenamento criogênico no cruzeiro (só MAV criogênico; descartados antes da entrada) | — | 0 |
| **Massa injetada** | | **3 996** |

Massa de entrada 3 866 kg; massa pousada 1 968 kg.

MAV O4: ε 0,230, Δv de subida com margem 5,764 km/s; mav_1: Isp 310 s, Δv 2,772 km/s, massa inicial 384,0 kg, propelente 229,7 kg; mav_2: Isp 310 s, Δv 2,991 km/s, massa inicial 85,7 kg, propelente 53,6 kg.

## Lançadores (forma a): pior margem nas quatro janelas

| Veículo | Lançador | Pior margem |
| :- | :- | -: |
| orbitador | Falcon Heavy (descartável) | +56 % |
| orbitador | Vulcan VC6 | +15 % |
| lander | Falcon Heavy (recuperação) | +17 % |
| lander | Falcon Heavy (descartável) | +181 % |
| lander | Vulcan VC2 | +8 % |
| lander | Vulcan VC4 | +62 % |
| lander | Vulcan VC6 | +108 % |

## Cronograma da missão de referência (datas em TDB)

| Evento | Data |
| :- | :- |
| Lançamentos do orbitador e do lander (injeção direta, lançamentos separados) | 2028-11-24 |
| Chegada a Marte: captura do orbitador; entrada direta e pouso do lander | 2029-09-20 |
| Estada em Marte (414 d): recuperação dos tubos, coleta de reserva, subida do MAV, encontro | 2029-09-20 a 2030-11-08 |
| Partida de Marte (injeção trans-Terra) | 2030-11-08 |
| Chegada à Terra (reentrada a 12,34 km/s) | 2031-09-23 |

## Sensibilidade (uma premissa por vez; órbita de encontro de base)

| Caso | Premissa | Orbitador injetado | Lander injetado | Orb.: Falcon Heavy (descartável) | Orb.: Vulcan VC6 | Lander: Falcon Heavy (recuperação) | Lander: Falcon Heavy (descartável) | Lander: Vulcan VC2 | Lander: Vulcan VC4 | Lander: Vulcan VC6 |
| :- | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| Base | — | 7 205 | 3 996 | +56 % | +15 % | +17 % | +181 % | +8 % | +62 % | +108 % |
| Margem de massa GSFC (+15 % da básica) nas duas plataformas | P-033 | 7 563 | 4 463 | +48 % | +10 % | +5 % | +151 % | −3 % | +45 % | +86 % |
| Margem de massa ESA (20 % × 20 %) nas duas plataformas | P-033 | 7 666 | 5 304 | +46 % | +8 % | −12 % | +112 % | −18 % | +22 % | +56 % |
| Plataforma do lander no limite inferior (L1; sem os helicópteros, como definido na Etapa 2.3) | P-017, P-035 | 7 205 | 1 892 | +56 % | +15 % | +147 % | +493 % | +129 % | +243 % | +338 % |
| Plataforma do lander no limite superior (SRL 2024 − MAV) | P-017, P-035 | 7 205 | 5 895 | +56 % | +15 % | −21 % | +90 % | −27 % | +10 % | +41 % |
| Razão pousada/entrada 0,624 (Viking, a partir de órbita) em vez de 0,509 | P-018 | 7 205 | 3 259 | +56 % | +15 % | +44 % | +244 % | +33 % | +99 % | +154 % |
| Margem de Δv 5 % (base 10 %) | P-014 | 6 549 | 3 839 | +71 % | +27 % | +22 % | +192 % | +13 % | +69 % | +116 % |
| Margem de Δv 20 % (base 10 %) | P-014 | 8 778 | 4 476 | +28 % | −6 % | +5 % | +151 % | −3 % | +45 % | +85 % |
| Sem penalidade de DLA (multiplicador 1) | P-036 | 7 205 | 3 996 | +69 % | +25 % | +26 % | +205 % | +17 % | +76 % | +126 % |
| ε do MAV 0,238 (MAV com turbobomba, Bowles Tab. 5 [F46]) em vez de 0,230 | — | 7 205 | 4 066 | +56 % | +15 % | +15 % | +176 % | +6 % | +60 % | +104 % |
| ε do MAV 0,176 (só a massa seca, Bowles Tab. 11 [F46]) em vez de 0,230 | — | 7 205 | 3 701 | +56 % | +15 % | +26 % | +203 % | +17 % | +75 % | +124 % |
| ε do MAV 0,300 (sem fonte, ilustração do risco) em vez de 0,230 | P-045 | 7 205 | 5 368 | +56 % | +15 % | −13 % | +109 % | −19 % | +21 % | +54 % |
