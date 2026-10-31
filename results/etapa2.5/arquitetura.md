# Arquitetura integrada (gerado por tools/arquitetura.py)

Missão de referência 2028-conjuncao; órbita de encontro 300 × 25 952 km; envelope de Δv 5,912 km/s; injeção direta (ADR 0008); 2 lançamentos. Massas em kg.

## Orbitador (regra iii)

| Item | Propelente | Inerte / massa |
| :- | -: | -: |
| Estágio de inserção em Marte (MMH/MON) | 3 210 | 1 014 |
| Estágio de retorno (MMH/MON) | 1 709 | 540 |
| Carga útil CU-2: CCRS (captura + montagem + proteção contra micrometeoroides) | — | 620 |
| Carga útil CU-2: EEV com COS (valor máximo esperado) | — | 90 |
| Plataforma (P-016, lista por subsistema + sensores de encontro) | — | 614 |
| **Massa injetada** | | **7 796** |

## Lander

| Item | Propelente | Inerte / massa |
| :- | -: | -: |
| Estágio de cruzeiro (correções de trajetória) | 99 | 31 |
| Sistema de entrada, descida e pouso (aeroshell, paraquedas, propelente de descida; P-018) | — | 1 901 |
| Plataforma de superfície L3 (lander do MSR sem MAV e sem rover de busca) | — | 1 470 |
| Braço de coleta de reserva (P-034, com margem) | — | 88 |
| Helicópteros de recuperação (ADR 0009, com margem) | — | 6 |
| MAV hipergólico + energia do aquecimento (ADR 0007) | — | 406 |
| Painéis do armazenamento criogênico no cruzeiro (só MAV criogênico; descartados antes da entrada) | — | 0 |
| **Massa injetada** | | **4 002** |

Massa de entrada 3 872 kg; massa pousada 1 971 kg.

MAV O4: ε 0,230, Δv de subida com margem 5,772 km/s; mav_1: Isp 310 s, Δv 2,777 km/s, massa inicial 386,8 kg, propelente 231,6 kg; mav_2: Isp 310 s, Δv 2,996 km/s, massa inicial 86,0 kg, propelente 53,9 kg.

## Lançadores (forma a): pior margem nas quatro janelas

| Veículo | Lançador | Pior margem |
| :- | :- | -: |
| orbitador | Falcon Heavy (descartável) | +44 % |
| orbitador | Vulcan VC6 | +6 % |
| lander | Falcon Heavy (recuperação) | +17 % |
| lander | Falcon Heavy (descartável) | +180 % |
| lander | Vulcan VC2 | +8 % |
| lander | Vulcan VC4 | +62 % |
| lander | Vulcan VC6 | +107 % |

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
| Base | — | 7 796 | 4 002 | +44 % | +6 % | +17 % | +180 % | +8 % | +62 % | +107 % |
| Margem de massa GSFC (+15 % da básica) nas duas plataformas | P-033 | 8 231 | 4 469 | +36 % | +1 % | +5 % | +151 % | −3 % | +45 % | +86 % |
| Margem de massa ESA (20 % × 20 %) nas duas plataformas | P-033 | 8 345 | 5 310 | +35 % | −1 % | −12 % | +111 % | −19 % | +22 % | +56 % |
| Plataforma do lander no limite inferior (L1; sem os helicópteros, como definido na Etapa 2.3) | P-017, P-035 | 7 796 | 1 898 | +44 % | +6 % | +147 % | +491 % | +128 % | +242 % | +337 % |
| Plataforma do lander no limite superior (SRL 2024 − MAV) | P-017, P-035 | 7 796 | 5 900 | +44 % | +6 % | −21 % | +90 % | −27 % | +10 % | +41 % |
| Razão pousada/entrada 0,624 (Viking, a partir de órbita) em vez de 0,509 | P-018 | 7 796 | 3 264 | +44 % | +6 % | +43 % | +244 % | +32 % | +99 % | +154 % |
| Margem de Δv 5 % (base 10 %) | P-014 | 7 093 | 3 844 | +58 % | +17 % | +22 % | +192 % | +13 % | +69 % | +116 % |
| Margem de Δv 20 % (base 10 %) | P-014 | 9 479 | 4 488 | +18 % | −13 % | +4 % | +150 % | −4 % | +45 % | +85 % |
| Sem penalidade de DLA (multiplicador 1) | P-036 | 7 796 | 4 002 | +56 % | +16 % | +26 % | +204 % | +17 % | +76 % | +125 % |
| ε do MAV 0,238 (MAV com turbobomba, Bowles Tab. 5 [F46]) em vez de 0,230 | — | 7 796 | 4 073 | +44 % | +6 % | +15 % | +176 % | +6 % | +59 % | +104 % |
| ε do MAV 0,176 (só a massa seca, Bowles Tab. 11 [F46]) em vez de 0,230 | — | 7 796 | 3 703 | +44 % | +6 % | +26 % | +203 % | +17 % | +75 % | +124 % |
| ε do MAV 0,300 (sem fonte, ilustração do risco) em vez de 0,230 | P-045 | 7 796 | 5 397 | +44 % | +6 % | −13 % | +108 % | −20 % | +20 % | +54 % |

## Dependência de lançador (escolhidos com margem ≥ 0 na base e em todos os casos da sensibilidade)

- **orbitador:** Falcon Heavy (descartável). Vulcan VC6 fica negativo em: Margem de massa ESA (20 % × 20 %) nas duas plataformas; Margem de Δv 20 % (base 10 %).
- **lander:** Falcon Heavy (descartável), Vulcan VC4, Vulcan VC6. Falcon Heavy (recuperação) fica negativo em: Margem de massa ESA (20 % × 20 %) nas duas plataformas; Plataforma do lander no limite superior (SRL 2024 − MAV); ε do MAV 0,300 (sem fonte, ilustração do risco) em vez de 0,230. Vulcan VC2 fica negativo em: Margem de massa GSFC (+15 % da básica) nas duas plataformas; Margem de massa ESA (20 % × 20 %) nas duas plataformas; Plataforma do lander no limite superior (SRL 2024 − MAV); Margem de Δv 20 % (base 10 %); ε do MAV 0,300 (sem fonte, ilustração do risco) em vez de 0,230.
