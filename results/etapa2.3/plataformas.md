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
| painel_solar | 29,5 | painel_solar | 27,5 % | 37,6 |
| bateria | 55,0 | baterias | 22,5 % | 67,4 |
| energia_restante | 67,2 | eletronica_acima_15kg | 15,0 % | 77,3 |
| cabeamento | 17,7 | cabeamento | 75,0 % | 31,0 |
| **Total** | **354,1** | | | **442,3** |

Energia: pior eclipse 3,24 h num período de 17,14 h; carga 510 W; painel 658 W no afélio (1,666 UA, 22,3 W/kg); bateria 5 500 Wh nominais para 1 650 Wh no eclipse.

## Lander

**Base:** L3 (lander do MSR sem MAV e sem rover de busca) 1 470 kg, sem MGA adicional, + amostras (P-034, provisório) com MGA E1 = 1 558,5 kg (GSFC: 1 787,8; ESA: 2 201,8). Faixa: L1 (abaixo) até SRL 2024 − MAV = 2 500 kg (comparabilidade não confirmada); L2 só como referência.

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
| nucleo | 1 351,4 | estrutura_primaria | 21,5 % | 1 642,0 |
| uhf | 6,5 | eletronica_0_5kg | 27,5 % | 8,3 |
| banda_x_cruzeiro | 14,7 | eletronica_0_5kg | 27,5 % | 18,7 |
| radar | 5,0 | eletronica_0_5kg | 27,5 % | 6,4 |
| amostras | 59,0 | instrumentacao | 50,0 % | 88,5 |
| painel_solar | 17,3 | painel_solar | 27,5 % | 22,1 |
| bateria | 58,3 | baterias | 22,5 % | 71,5 |
| **Total** | **1 512,3** | | | **1 857,4** |

## Massa total na órbita baixa da Terra

| Caso | Orbitador | Lander | Total (iii) em 26 950 km | Total (A) em 26 950 km | Apoapse pela regra dos 5 % | Total (iii) nele | Total (A) nele |
| :- | -: | -: | -: | -: | -: | -: | -: |
| Antes (P-016 = P-017 = 850 kg) | 850 | 850 | 31 233 | 21 298 | 26 950 | 31 233 | 21 298 |
| **Base: orbitador E1 médio + L3 + amostras** | 442 | 1 558 | 29 243 | 21 907 | 24 992 | 29 607 | 22 083 |
| GSFC: E1 médio + 15 % nos dois | 495 | 1 788 | 31 479 | 23 804 | 24 992 | 31 861 | 23 989 |
| ESA: 20 % × 20 % nos dois | 510 | 2 202 | 34 247 | 26 481 | 24 067 | 34 840 | 26 767 |
| Orbitador E1 mínimo + lander de base | 422 | 1 558 | 28 922 | 21 718 | 24 992 | 29 279 | 21 890 |
| Orbitador E1 máximo + lander de base | 463 | 1 558 | 29 564 | 22 097 | 24 992 | 29 935 | 22 276 |
| Limite inferior do lander: L1 (E1 médio) | 442 | 529 | 22 914 | 15 579 | 26 950 | 22 914 | 15 579 |
| Limite superior do lander: SRL 2024 − MAV (comparabilidade não confirmada) | 442 | 2 500 | 35 029 | 27 693 | 23 176 | 35 788 | 28 058 |
| Referência: L2 (E1 médio), antigo limite superior | 442 | 1 857 | 31 080 | 23 744 | 24 067 | 31 637 | 24 013 |

Nos casos de sensibilidade, a plataforma do orbitador é a calculada no apoapse do caso de base.
