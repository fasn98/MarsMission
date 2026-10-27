# Arquitetura integrada (gerado por tools/arquitetura.py)

Missão de referência 2028-conjuncao; órbita de encontro 300 × 24 992 km; envelope de Δv 5,912 km/s; injeção direta (ADR 0008); 2 lançamentos. Massas em kg.

## Orbitador (regra iii)

| Item | Propelente | Inerte / massa |
| :- | -: | -: |
| Estágio de inserção em Marte (MMH/MON) | 2 478 | 782 |
| Estágio de retorno (MMH/MON) | 1 401 | 443 |
| Carga útil CU-2: CCRS (captura + montagem + proteção contra micrometeoroides) | — | 620 |
| Carga útil CU-2: EEV com COS (valor máximo esperado) | — | 90 |
| Plataforma (P-016, lista por subsistema + sensores de encontro) | — | 496 |
| **Massa injetada** | | **6 310** |

## Lander

| Item | Propelente | Inerte / massa |
| :- | -: | -: |
| Estágio de cruzeiro (correções de trajetória) | 84 | 27 |
| Sistema de entrada, descida e pouso (aeroshell, paraquedas, propelente de descida; P-018) | — | 1 782 |
| Plataforma de superfície L3 (lander do MSR sem MAV e sem rover de busca) | — | 1 470 |
| Braço de coleta de reserva (P-034, com margem) | — | 88 |
| Helicópteros de recuperação (ADR 0009, com margem) | — | 6 |
| MAV hipergólico + energia do aquecimento (ADR 0007) | — | 282 |
| **Massa injetada** | | **3 740** |

Massa de entrada 3 629 kg; massa pousada 1 847 kg.

## Lançadores (forma a): pior margem nas quatro janelas

| Veículo | Lançador | Pior margem |
| :- | :- | -: |
| orbitador | Falcon Heavy (descartável) | +78 % |
| orbitador | Vulcan VC6 | +31 % |
| lander | Falcon Heavy (recuperação) | +25 % |
| lander | Falcon Heavy (descartável) | +200 % |
| lander | Vulcan VC2 | +16 % |
| lander | Vulcan VC4 | +73 % |
| lander | Vulcan VC6 | +122 % |

## Cronograma da missão de referência (datas em TDB)

| Evento | Data |
| :- | :- |
| Lançamentos do orbitador e do lander (injeção direta, lançamentos separados) | 2028-11-24 |
| Chegada a Marte: captura do orbitador; entrada direta e pouso do lander | 2029-09-20 |
| Estada em Marte (414 d): recuperação dos tubos, coleta de reserva, subida do MAV, encontro | 2029-09-20 a 2030-11-08 |
| Partida de Marte (injeção trans-Terra) | 2030-11-08 |
| Chegada à Terra (reentrada a 12,34 km/s) | 2031-09-23 |

## Sensibilidade (uma premissa por vez; órbita de encontro de base)

| Caso | Premissa | Orbitador injetado | Lander injetado | Orb.: Falcon Heavy (descartável) | Orb.: Vulcan VC6 | Lander: menor margem |
| :- | :- | -: | -: | -: | -: | -: |
| Base | — | 6 310 | 3 740 | +78 % | +31 % | +16 % (Vulcan VC2) |
| Margem de massa GSFC (+15 % da básica) nas duas plataformas | P-033 | 6 623 | 4 206 | +69 % | +25 % | +3 % (Vulcan VC2) |
| Margem de massa ESA (20 % × 20 %) nas duas plataformas | P-033 | 6 714 | 5 044 | +67 % | +24 % | −14 % (Vulcan VC2) |
| Plataforma do lander no limite inferior (L1) | P-017, P-035 | 6 310 | 1 642 | +78 % | +31 % | +163 % (Vulcan VC2) |
| Plataforma do lander no limite superior (SRL 2024 − MAV) | P-017, P-035 | 6 310 | 5 633 | +78 % | +31 % | −23 % (Vulcan VC2) |
| Razão pousada/entrada 0,624 (Viking, a partir de órbita) em vez de 0,509 | P-018 | 6 310 | 3 051 | +78 % | +31 % | +42 % (Vulcan VC2) |
| Margem de Δv 5 % (base 10 %) | P-014 | 5 785 | 3 645 | +94 % | +43 % | +19 % (Vulcan VC2) |
| Margem de Δv 20 % (base 10 %) | P-014 | 7 548 | 4 007 | +49 % | +10 % | +8 % (Vulcan VC2) |
| Sem penalidade de DLA (multiplicador 1) | P-036 | 6 310 | 3 740 | +93 % | +43 % | +25 % (Vulcan VC2) |
