# Plataformas por subsistema (gerado por tools/plataformas.py)

Órbita de encontro 300 × 25 952 km (regra dos 5 % do ADR 0005 reaplicada; antes 26 950 km); MAV O4 com energia solar. Massas em kg.

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
| painel_solar | 58,9 | painel_solar | 27,5 % | 75,1 |
| bateria | 113,7 | baterias | 22,5 % | 139,2 |
| energia_restante | 67,2 | eletronica_acima_15kg | 15,0 % | 77,3 |
| cabeamento | 24,5 | cabeamento | 75,0 % | 43,0 |
| **Total** | **491,0** | | | **614,0** |

Energia: pior eclipse 3,34 h num período de 17,91 h; carga 1 022 W; painel 1 314 W no afélio (1,666 UA, 22,3 W/kg); bateria 11 367 Wh nominais para 3 410 Wh no eclipse.

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
| Antes (P-016 = P-017 = 850 kg) | 850 | 850 | 35 337 | 23 531 | 26 950 | 35 337 | 23 531 |
| **Base: orbitador E1 médio + L3 + braço + helicópteros** | 614 | 1 565 | 35 568 | 25 550 | 25 952 | 35 814 | 25 662 |
| GSFC: E1 médio + 15 % nos dois | 688 | 1 795 | 38 289 | 27 714 | 25 952 | 38 551 | 27 832 |
| ESA: 20 % × 20 % nos dois | 707 | 2 209 | 41 183 | 30 461 | 24 992 | 41 725 | 30 706 |
| Orbitador E1 mínimo + lander de base | 586 | 1 565 | 35 070 | 25 266 | 25 952 | 35 311 | 25 374 |
| Orbitador E1 máximo + lander de base | 642 | 1 565 | 36 065 | 25 835 | 25 952 | 36 318 | 25 949 |
| Limite inferior do lander: L1 (E1 médio) | 614 | 529 | 29 181 | 19 164 | 26 950 | 29 181 | 19 164 |
| Limite superior do lander: SRL 2024 − MAV (comparabilidade não confirmada) | 614 | 2 500 | 41 332 | 31 314 | 24 992 | 41 836 | 31 541 |
| Referência: L2 (E1 médio), antigo limite superior | 614 | 2 309 | 40 157 | 30 140 | 24 992 | 40 661 | 30 366 |

Nos casos de sensibilidade, a plataforma do orbitador é a calculada no apoapse do caso de base.
