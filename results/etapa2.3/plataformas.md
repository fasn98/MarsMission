# Plataformas por subsistema (gerado por tools/plataformas.py)

Órbita de encontro 300 × 24 992 km (regra dos 5 % do ADR 0005 reaplicada; antes 26 950 km); MAV O4 com energia solar. Massas em kg.

## Orbitador (base: E1 médio)

| Subsistema | Básica | Categoria E1 | MGA (médio) | Prevista |
| :- | -: | :- | -: | -: |
| estrutura | 81,7 | estrutura_primaria | 21,5 % | 99,3 |
| termico | 20,3 | controle_termico | 40,0 % | 28,4 |
| comunicacao | 23,9 | eletronica_0_5kg | 27,5 % | 30,5 |
| comando_e_dados | 11,1 | eletronica_5_15kg | 20,0 % | 13,3 |
| gnc | 23,4 | eletronica_5_15kg | 20,0 % | 28,1 |
| mecanismos | 24,2 | mecanismos | 21,5 % | 29,4 |
| rss_nac | 29,0 | eletronica_5_15kg | 20,0 % | 34,8 |
| rss_lidar | 13,0 | eletronica_5_15kg | 20,0 % | 15,6 |
| painel_solar | 29,5 | painel_solar | 27,5 % | 37,6 |
| bateria | 55,0 | baterias | 22,5 % | 67,4 |
| energia_restante | 67,2 | eletronica_acima_15kg | 15,0 % | 77,3 |
| cabeamento | 19,9 | cabeamento | 75,0 % | 34,8 |
| **Total** | **398,3** | | | **496,5** |

Energia: pior eclipse 3,24 h num período de 17,14 h; carga 510 W; painel 658 W no afélio (1,666 UA, 22,3 W/kg); bateria 5 500 Wh nominais para 1 650 Wh no eclipse.

## Lander

**Base:** L3 (lander do MSR sem MAV e sem rover de busca) 1 470 kg, sem MGA adicional, + braço de coleta (P-034) + helicópteros (ADR 0009), com MGA E1 = 1 564,9 kg (GSFC: 1 795,0; ESA: 2 209,0). Faixa: L1 (abaixo) até SRL 2024 − MAV = 2 500 kg (comparabilidade não confirmada); L2 só como referência.

### Limite inferior L1

| Subsistema | Básica | Categoria E1 | MGA (médio) | Prevista |
| :- | -: | :- | -: | -: |
| nucleo | 257,8 | estrutura_primaria | 21,5 % | 313,2 |
| uhf | 6,5 | eletronica_0_5kg | 27,5 % | 8,3 |
| banda_x_cruzeiro | 14,7 | eletronica_0_5kg | 27,5 % | 18,7 |
| radar | 5,0 | eletronica_0_5kg | 27,5 % | 6,4 |
| amostras | 59,0 | instrumentacao | 50,0 % | 88,5 |
| painel_solar | 17,3 | painel_solar | 27,5 % | 22,1 |
| bateria | 58,3 | baterias | 22,5 % | 71,5 |
| **Total** | **418,7** | | | **528,7** |

### Referência L2

| Subsistema | Básica | Categoria E1 | MGA (médio) | Prevista |
| :- | -: | :- | -: | -: |
| nucleo | 1 723,4 | estrutura_primaria | 21,5 % | 2 093,9 |
| uhf | 6,5 | eletronica_0_5kg | 27,5 % | 8,3 |
| banda_x_cruzeiro | 14,7 | eletronica_0_5kg | 27,5 % | 18,7 |
| radar | 5,0 | eletronica_0_5kg | 27,5 % | 6,4 |
| amostras | 59,0 | instrumentacao | 50,0 % | 88,5 |
| painel_solar | 17,3 | painel_solar | 27,5 % | 22,1 |
| bateria | 58,3 | baterias | 22,5 % | 71,5 |
| **Total** | **1 884,3** | | | **2 309,4** |

## Massa total na órbita baixa da Terra

| Caso | Orbitador | Lander | Total (iii) em 26 950 km | Total (A) em 26 950 km | Apoapse pela regra dos 5 % | Total (iii) nele | Total (A) nele |
| :- | -: | -: | -: | -: | -: | -: | -: |
| Antes (P-016 = P-017 = 850 kg) | 850 | 850 | 35 412 | 23 580 | 26 950 | 35 412 | 23 580 |
| **Base: orbitador E1 médio + L3 + braço + helicópteros** | 497 | 1 565 | 33 547 | 24 400 | 24 992 | 34 003 | 24 603 |
| GSFC: E1 médio + 15 % nos dois | 556 | 1 795 | 36 025 | 26 424 | 24 992 | 36 505 | 26 640 |
| ESA: 20 % × 20 % nos dois | 574 | 2 209 | 38 882 | 29 151 | 24 992 | 39 370 | 29 370 |
| Orbitador E1 mínimo + lander de base | 473 | 1 565 | 33 134 | 24 163 | 24 992 | 33 580 | 24 362 |
| Orbitador E1 máximo + lander de base | 520 | 1 565 | 33 960 | 24 636 | 25 952 | 34 188 | 24 738 |
| Limite inferior do lander: L1 (E1 médio) | 497 | 529 | 27 160 | 18 013 | 26 950 | 27 160 | 18 013 |
| Limite superior do lander: SRL 2024 − MAV (comparabilidade não confirmada) | 497 | 2 500 | 39 311 | 30 164 | 24 067 | 40 010 | 30 476 |
| Referência: L2 (E1 médio), antigo limite superior | 497 | 2 309 | 38 136 | 28 989 | 24 992 | 38 592 | 29 192 |

Nos casos de sensibilidade, a plataforma do orbitador é a calculada no apoapse do caso de base.
