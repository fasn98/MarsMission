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

**Base L3** (lander do MSR sem MAV e sem rover de busca): 1 470 kg, sem MGA adicional (GSFC: 1 690; ESA: 2 117). Limites L1 e L2 abaixo.

### Limite L1

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

### Limite L2

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
| **Base: orbitador E1 médio + L3** | 442 | 1 470 | 28 699 | 21 364 | 24 992 | 29 063 | 21 539 |
| GSFC: orbitador E1 médio + 15 %; L3 + 15 % | 495 | 1 690 | 30 880 | 23 206 | 24 992 | 31 262 | 23 391 |
| ESA: 20 % × 20 % nos dois | 510 | 2 117 | 33 725 | 25 959 | 24 067 | 34 318 | 26 245 |
| Orbitador E1 mínimo + L3 | 422 | 1 470 | 28 378 | 21 174 | 24 992 | 28 735 | 21 346 |
| Orbitador E1 máximo + L3 | 463 | 1 470 | 29 020 | 21 553 | 24 992 | 29 391 | 21 732 |
| Limite inferior do lander: L1 (E1 médio) | 442 | 529 | 22 914 | 15 579 | 26 950 | 22 914 | 15 579 |
| Limite superior do lander: L2 (E1 médio) | 442 | 1 857 | 31 080 | 23 744 | 24 067 | 31 637 | 24 013 |

Nos casos de sensibilidade, a plataforma do orbitador é a calculada no apoapse do caso de base.
