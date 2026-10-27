# Plataformas por subsistema (gerado por tools/plataformas.py)

Órbita de encontro 300 × 26 950 km (ADR 0005); MAV O4 com energia solar. Massas em kg.

## Orbitador

| Subsistema | Básica | Categoria E1 | MGA (médio) | Prevista |
| :- | -: | :- | -: | -: |
| estrutura | 81,7 | estrutura_primaria | 21,5 % | 99,3 |
| termico | 20,3 | controle_termico | 40,0 % | 28,4 |
| comunicacao | 23,9 | eletronica_0_5kg | 27,5 % | 30,5 |
| comando_e_dados | 11,1 | eletronica_5_15kg | 20,0 % | 13,3 |
| gnc | 23,4 | eletronica_5_15kg | 20,0 % | 28,1 |
| mecanismos | 24,2 | mecanismos | 21,5 % | 29,4 |
| painel_solar | 29,3 | painel_solar | 27,5 % | 37,4 |
| bateria | 58,5 | baterias | 22,5 % | 71,7 |
| energia_restante | 67,2 | eletronica_acima_15kg | 15,0 % | 77,3 |
| cabeamento | 55,2 | cabeamento | 75,0 % | 96,7 |
| **Total** | **394,9** | | | **512,0** |

Energia: pior eclipse 3,44 h num período de 18,73 h; carga 510 W; painel 654 W no afélio (1,666 UA, 22,3 W/kg); bateria 5 851 Wh nominais para 1 755 Wh no eclipse.

## Lander, opção L1

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

## Lander, opção L2

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

Energia do lander: 3 500 Wh/sol (142 W médios); painel 4,20 m²; bateria 5 833 Wh nominais para 1 750 Wh na noite.

## Plataformas por critério de margem

| Critério | Orbitador | Lander L1 | Lander L2 |
| :- | -: | -: | -: |
| S-120A E1, ponto médio (base) | 512 | 529 | 1 857 |
| S-120A E1, mínimo | 482 | 500 | 1 791 |
| S-120A E1, máximo | 542 | 557 | 1 924 |
| E1 médio + 15 % da básica (GSFC pré-A) | 571 | 591 | 2 084 |
| ESA: 20 % equipamento × 20 % sistema | 569 | 603 | 2 178 |

## Massa total na órbita baixa da Terra

| Caso | Orbitador | Lander | Total (iii) em 26 950 km | Total (A) em 26 950 km | Apoapse pela regra dos 5 % | Total (iii) nele | Total (A) nele |
| :- | -: | -: | -: | -: | -: | -: | -: |
| Antes (P-016 = P-017 = 850 kg) | 850 | 850 | 31 233 | 21 298 | 26 950 | 31 233 | 21 298 |
| L1, S-120A E1, ponto médio (base) | 512 | 529 | 23 999 | 16 219 | 26 950 | 23 999 | 16 219 |
| L1, S-120A E1, mínimo | 482 | 500 | 23 356 | 15 768 | 26 950 | 23 356 | 15 768 |
| L1, S-120A E1, máximo | 542 | 557 | 24 642 | 16 670 | 26 950 | 24 642 | 16 670 |
| L1, E1 médio + 15 % da básica (GSFC pré-A) | 571 | 591 | 25 307 | 17 149 | 26 950 | 25 307 | 17 149 |
| L1, ESA: 20 % equipamento × 20 % sistema | 569 | 603 | 25 337 | 17 195 | 26 950 | 25 337 | 17 195 |
| L2, S-120A E1, ponto médio (base) | 512 | 1 857 | 32 165 | 24 385 | 24 992 | 32 552 | 24 572 |
| L2, S-120A E1, mínimo | 482 | 1 791 | 31 286 | 23 698 | 24 992 | 31 664 | 23 880 |
| L2, S-120A E1, máximo | 542 | 1 924 | 33 043 | 25 071 | 24 992 | 33 441 | 25 264 |
| L2, E1 médio + 15 % da básica (GSFC pré-A) | 571 | 2 084 | 34 480 | 26 323 | 24 067 | 35 104 | 26 624 |
| L2, ESA: 20 % equipamento × 20 % sistema | 569 | 2 178 | 35 014 | 26 873 | 24 067 | 35 637 | 27 174 |
