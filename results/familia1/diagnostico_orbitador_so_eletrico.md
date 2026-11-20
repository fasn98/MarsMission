# Diagnóstico do orbitador só elétrico da família 1 (gerado por tools/orbitador_so_eletrico.py)

Fora da comparação do CI (regra 6): soluções de otimização (mínimos locais). Calculado, NÃO validado.

## (b) Caso publicado: Joffre 2018 [F121] com massa e empuxo de Yau 2021 [F22]

### Fig. 4, esquerda: empuxo constante, chegada com v∞ (captura química), só com os módulos de v∞ publicados

Δv publicado 2,59 km/s; Isp 3 900 s; o Δv publicado não fica entre dois empuxos convergidos da varredura.

| Empuxo (N) | Convergiu | Critério | Δv (km/s) | Δv dos arcos (km/s) | δ partida (°) | δ chegada, equador de Marte (°) | Erro contínuo (km; km/s) |
| -: | :- | :- | -: | :- | -: | -: | :- |
| 1,50 | sim | Optimization terminated successfully | 1,986 | 1,103, 0,542, 0,341 | 11,58 | −15,64 | 34; 4,3e−06 |
| 1,25 | sim | Optimization terminated successfully | 1,987 | 1,123, 0,505, 0,359 | 11,64 | −15,57 | 31; 3,6e−06 |
| 1,20 | sim | Optimization terminated successfully | 1,987 | 1,128, 0,496, 0,363 | 11,65 | −15,54 | 31; 3,4e−06 |
| 1,15 | sim | Optimization terminated successfully | 1,987 | 1,136, 0,486, 0,364 | 11,67 | −15,52 | 30; 3,2e−06 |
| 1,10 | sim | Optimization terminated successfully | 1,987 | 1,141, 0,480, 0,366 | 11,67 | −15,50 | 30; 3,1e−06 |
| 1,05 | sim | Optimization terminated successfully | 1,988 | 1,146, 0,474, 0,368 | 11,67 | −15,47 | 30; 3,1e−06 |
| 1,00 | sim | Optimization terminated successfully | 1,988 | 1,144, 0,479, 0,365 | 11,59 | −15,44 | 30; 3,1e−06 |
| 0,75 | sim | Optimization terminated successfully | 1,990 | 1,222, 0,305, 0,463 | 11,61 | −15,10 | 29; 2,7e−06 |

### Fig. 4, esquerda: empuxo constante, chegada com v∞ (captura química), com as declinações publicadas impostas

Δv publicado 2,59 km/s; Isp 3 900 s; o Δv publicado não fica entre dois empuxos convergidos da varredura.

| Empuxo (N) | Convergiu | Critério | Δv (km/s) | Δv dos arcos (km/s) | δ partida (°) | δ chegada, equador de Marte (°) | Erro contínuo (km; km/s) |
| -: | :- | :- | -: | :- | -: | -: | :- |
| 1,50 | sim | Optimization terminated successfully | 2,014 | 0,845, 0,839, 0,330 | 4,97 | −11,90 | 43; 5,6e−06 |
| 1,25 | sim | Optimization terminated successfully | 2,014 | 0,845, 0,828, 0,341 | 4,97 | −11,90 | 42; 5,3e−06 |
| 1,20 | sim | Optimization terminated successfully | 2,015 | 0,853, 0,815, 0,346 | 4,97 | −11,90 | 39; 4,9e−06 |
| 1,15 | sim | Optimization terminated successfully | 2,015 | 0,857, 0,807, 0,350 | 4,97 | −11,90 | 36; 4,6e−06 |
| 1,10 | sim | Optimization terminated successfully | 2,015 | 0,863, 0,803, 0,349 | 4,97 | −11,90 | 35; 4,3e−06 |
| 1,05 | sim | Optimization terminated successfully | 2,015 | 0,866, 0,800, 0,349 | 4,97 | −11,90 | 34; 4,2e−06 |
| 1,00 | sim | Optimization terminated successfully | 2,016 | 0,879, 0,797, 0,340 | 4,97 | −11,90 | 34; 4,1e−06 |
| 0,75 | sim | Optimization terminated successfully | 2,018 | 0,916, 0,726, 0,376 | 4,97 | −11,90 | 30; 3,3e−06 |

### Fig. 4, direita: chegada com v∞ = 0, arco de voo livre entre dois arcos de empuxo, só com os módulos de v∞ publicados

Δv publicado 5,94 km/s; Isp 3 900 s; empuxo em que o Δv calculado iguala o publicado: 1,176 N (1,8e−04 m/s² com 6 500 kg), contra o máximo de 0,75 N de [F22].

| Empuxo (N) | Convergiu | Critério | Δv (km/s) | Δv dos arcos (km/s) | δ partida (°) | δ chegada, equador de Marte (°) | Erro contínuo (km; km/s) |
| -: | :- | :- | -: | :- | -: | -: | :- |
| 1,50 | sim | Optimization terminated successfully | 5,384 | 2,876, 2,508 | −7,86 | — | 1 238; 1,2e−04 |
| 1,25 | sim | Optimization terminated successfully | 5,730 | 3,069, 2,661 | −9,64 | — | 1 110; 1,1e−04 |
| 1,20 | sim | Optimization terminated successfully | 5,860 | 3,180, 2,680 | −10,14 | — | 955; 9,5e−05 |
| 1,15 | sim | Optimization terminated successfully | 6,029 | 3,283, 2,745 | −9,98 | — | 857; 8,6e−05 |
| 1,10 | sim | Optimization terminated successfully | 6,250 | 3,466, 2,783 | −9,88 | — | 669; 6,9e−05 |
| 1,05 | sim | Optimization terminated successfully | 6,599 | 3,623, 2,975 | −9,55 | — | 571; 6,0e−05 |
| 1,00 | não | Iteration limit reached | — | — | — | — | — |
| 0,75 | não | Iteration limit reached | — | — | — | — | — |

### Fig. 4, direita: chegada com v∞ = 0, arco de voo livre entre dois arcos de empuxo, com as declinações publicadas impostas

Δv publicado 5,94 km/s; Isp 3 900 s; empuxo em que o Δv calculado iguala o publicado: 1,191 N (1,8e−04 m/s² com 6 500 kg), contra o máximo de 0,75 N de [F22].

| Empuxo (N) | Convergiu | Critério | Δv (km/s) | Δv dos arcos (km/s) | δ partida (°) | δ chegada, equador de Marte (°) | Erro contínuo (km; km/s) |
| -: | :- | :- | -: | :- | -: | -: | :- |
| 1,50 | sim | Optimization terminated successfully | 5,408 | 2,881, 2,527 | −0,06 | — | 1 241; 1,2e−04 |
| 1,25 | sim | Optimization terminated successfully | 5,773 | 3,092, 2,680 | −0,06 | — | 1 113; 1,1e−04 |
| 1,20 | sim | Optimization terminated successfully | 5,907 | 3,204, 2,703 | −0,06 | — | 942; 9,4e−05 |
| 1,15 | sim | Optimization terminated successfully | 6,079 | 3,320, 2,759 | −0,06 | — | 839; 8,5e−05 |
| 1,10 | sim | Optimization terminated successfully | 6,301 | 3,510, 2,791 | −0,06 | — | 656; 6,8e−05 |
| 1,05 | sim | Optimization terminated successfully | 6,679 | 3,666, 3,012 | −0,06 | — | 574; 6,0e−05 |
| 1,00 | não | Positive directional derivative for linesearch | — | — | — | — | — |
| 0,75 | não | Positive directional derivative for linesearch | — | — | — | — | — |

## (a) e (c) Família 1

| Propulsor | Ativos | Encontro (km) | Instalados | Potência (kW) | Xe (kg) | Xe por propulsor (kg) | Vida (kg) | Propulsores + PPU (kg) | Orbitador (kg) | Margem no Falcon Heavy | C3 (km²/s²) | DLA (°) | Partida da Terra | Ida (d) | Chegada a Marte | Descida (d) | Pronto no encontro | Último lançamento do MAV | Lançamento do MAV | Subida (d) | Partida de Marte | Volta (d) | Chegada à Terra | Fecha? |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- | -: | :- | :- | :- | -: | :- | -: | :- | :- |
| XIPS-25 | 6 | 380 | 26 | 27,0 | 2 632 | 105 | 158 | 910 | 7 643 | 93,4 % | 0,66 | 7,1 | 2028-09-17 | 590 | 2030-04-30 | 303 | 2031-02-28 | 2032-04-26 | 2031-02-28 | 262 | 2032-04-12 | 517 | 2033-09-11 | **sim** |
| XIPS-25 | 7 | 380 | 17 | 31,5 | 2 484 | 155 | 158 | 595 | 7 215 | 105,1 % | 0,59 | 6,4 | 2028-09-18 | 581 | 2030-04-22 | 245 | 2030-12-24 | 2032-04-26 | 2030-12-24 | 212 | 2032-04-06 | 520 | 2033-09-07 | **sim** |
| XIPS-25 | 8 | 380 | 19 | 36,0 | 2 716 | 151 | 158 | 665 | 7 885 | 87,8 % | 0,58 | 6,5 | 2028-09-18 | 587 | 2030-04-28 | 235 | 2030-12-19 | 2032-04-26 | 2030-12-19 | 203 | 2032-04-10 | 515 | 2033-09-07 | **sim** |
| XIPS-25 | 9 | 380 | 20 | 40,5 | 2 912 | 153 | 158 | 700 | 8 454 | 75,2 % | 0,57 | 6,3 | 2028-09-18 | 587 | 2030-04-28 | 223 | 2030-12-08 | 2032-04-26 | 2030-12-08 | 193 | 2032-04-14 | 510 | 2033-09-07 | **sim** |
| XIPS-25 | 10 | 380 | 21 | 45,0 | 3 108 | 155 | 158 | 735 | 9 022 | 64,2 % | 0,56 | 5,9 | 2028-09-19 | 587 | 2030-04-29 | 215 | 2030-11-30 | 2032-04-26 | 2030-11-30 | 185 | 2032-04-18 | 506 | 2033-09-06 | **sim** |
| XIPS-25 | 11 | 380 | 22 | 49,5 | 3 304 | 157 | 158 | 770 | 9 590 | 54,5 % | 0,55 | 5,5 | 2028-09-19 | 588 | 2030-04-29 | 207 | 2030-11-23 | 2032-04-26 | 2030-11-23 | 179 | 2032-04-21 | 503 | 2033-09-06 | **sim** |
| XIPS-25 | 12 | 380 | 24 | 54,0 | 3 534 | 154 | 158 | 840 | 10 258 | 44,4 % | 0,55 | 5,3 | 2028-09-19 | 588 | 2030-04-29 | 203 | 2030-11-19 | 2032-04-26 | 2030-11-19 | 176 | 2032-04-21 | 503 | 2033-09-06 | **sim** |
| NEXT-C | 3 | 380 | 4 | 22,0 | 1 428 | 476 | 918 | 196 | 4 686 | 216,6 % | 0,48 | 7,1 | 2028-09-17 | 702 | 2030-08-21 | 268 | 2031-05-17 | 2032-04-26 | 2031-05-17 | 235 | 2032-07-27 | 409 | 2033-09-09 | **sim** |
| NEXT-C | 4 | 380 | 5 | 29,3 | 1 682 | 420 | 918 | 245 | 5 515 | 169,1 % | 0,44 | 6,6 | 2028-09-18 | 702 | 2030-08-21 | 237 | 2031-04-15 | 2032-04-26 | 2031-04-15 | 207 | 2032-07-26 | 408 | 2033-09-08 | **sim** |
| NEXT-C | 5 | 380 | 6 | 36,6 | 1 936 | 387 | 918 | 294 | 6 345 | 134,0 % | 0,42 | 6,5 | 2028-09-18 | 702 | 2030-08-21 | 218 | 2031-03-27 | 2032-04-26 | 2031-03-27 | 191 | 2032-07-26 | 408 | 2033-09-06 | **sim** |
| NEXT-C | 6 | 380 | 7 | 44,0 | 2 187 | 365 | 918 | 343 | 7 173 | 107,0 % | 0,42 | 6,5 | 2028-09-18 | 702 | 2030-08-21 | 205 | 2031-03-15 | 2032-04-26 | 2031-03-15 | 180 | 2032-07-25 | 407 | 2033-09-06 | **sim** |
| NEXT-C | 7 | 380 | 8 | 51,3 | 2 439 | 348 | 918 | 392 | 8 000 | 85,6 % | 0,42 | 6,4 | 2028-09-18 | 694 | 2030-08-13 | 196 | 2031-02-26 | 2032-04-26 | 2031-02-26 | 172 | 2032-07-26 | 407 | 2033-09-06 | **sim** |
| XIPS-25 | 6 | 814 | 25 | 27,0 | 2 499 | 104 | 158 | 875 | 7 416 | 99,4 % | 0,65 | 7,0 | 2028-09-17 | 599 | 2030-05-10 | 274 | 2031-02-08 | 2032-04-26 | 2031-02-08 | 237 | 2032-04-15 | 558 | 2033-10-26 | **sim** |
| XIPS-25 | 7 | 814 | 16 | 31,5 | 2 361 | 157 | 158 | 560 | 7 000 | 111,5 % | 0,58 | 6,6 | 2028-09-18 | 589 | 2030-04-30 | 221 | 2030-12-08 | 2032-04-26 | 2030-12-08 | 192 | 2032-04-17 | 560 | 2033-10-29 | **sim** |
| XIPS-25 | 8 | 814 | 18 | 36,0 | 2 583 | 152 | 158 | 630 | 7 658 | 93,3 % | 0,57 | 6,5 | 2028-09-18 | 599 | 2030-05-11 | 212 | 2030-12-09 | 2032-04-26 | 2030-12-09 | 184 | 2032-04-17 | 560 | 2033-10-29 | **sim** |
| XIPS-25 | 9 | 814 | 19 | 40,5 | 2 771 | 154 | 158 | 665 | 8 218 | 80,2 % | 0,57 | 6,1 | 2028-09-18 | 599 | 2030-05-11 | 202 | 2030-11-30 | 2032-04-26 | 2030-11-30 | 175 | 2032-04-17 | 560 | 2033-10-29 | **sim** |
| XIPS-25 | 10 | 814 | 20 | 45,0 | 2 959 | 156 | 158 | 700 | 8 777 | 68,7 % | 0,57 | 6,0 | 2028-09-18 | 598 | 2030-05-10 | 194 | 2030-11-21 | 2032-04-26 | 2030-11-21 | 168 | 2032-04-16 | 562 | 2033-10-30 | **sim** |
| XIPS-25 | 11 | 814 | 21 | 49,5 | 3 152 | 158 | 158 | 735 | 9 343 | 58,6 % | 0,55 | 6,1 | 2028-09-18 | 598 | 2030-05-10 | 188 | 2030-11-14 | 2032-04-26 | 2030-11-14 | 163 | 2032-04-17 | 561 | 2033-10-30 | **sim** |
| XIPS-25 | 12 | 814 | 23 | 54,0 | 3 375 | 153 | 158 | 805 | 10 002 | 48,1 % | 0,55 | 6,0 | 2028-09-19 | 599 | 2030-05-10 | 184 | 2030-11-11 | 2032-04-26 | 2030-11-11 | 160 | 2032-04-17 | 561 | 2033-10-30 | **sim** |
| NEXT-C | 3 | 814 | 4 | 22,0 | 1 377 | 459 | 918 | 196 | 4 615 | 221,5 % | 0,46 | 7,3 | 2028-09-17 | 649 | 2030-06-29 | 246 | 2031-03-02 | 2032-04-26 | 2031-03-02 | 216 | 2032-01-22 | 597 | 2033-09-10 | **sim** |
| NEXT-C | 4 | 814 | 5 | 29,3 | 1 622 | 405 | 918 | 245 | 5 433 | 173,2 % | 0,43 | 6,9 | 2028-09-18 | 650 | 2030-06-30 | 217 | 2031-02-02 | 2032-04-26 | 2031-02-02 | 190 | 2032-01-20 | 596 | 2033-09-07 | **sim** |
| NEXT-C | 5 | 814 | 6 | 36,6 | 1 865 | 373 | 918 | 294 | 6 251 | 137,5 % | 0,43 | 6,3 | 2028-09-18 | 649 | 2030-06-29 | 200 | 2031-01-15 | 2032-04-26 | 2031-01-15 | 175 | 2032-01-20 | 596 | 2033-09-07 | **sim** |
| NEXT-C | 6 | 814 | 7 | 44,0 | 2 111 | 352 | 918 | 343 | 7 072 | 110,0 % | 0,41 | 6,5 | 2028-09-18 | 649 | 2030-06-29 | 188 | 2031-01-04 | 2032-04-26 | 2031-01-04 | 165 | 2032-01-20 | 595 | 2033-09-06 | **sim** |
| NEXT-C | 7 | 814 | 8 | 51,3 | 2 354 | 336 | 918 | 392 | 7 890 | 88,3 % | 0,41 | 6,6 | 2028-09-18 | 645 | 2030-06-25 | 180 | 2030-12-22 | 2032-04-26 | 2030-12-22 | 158 | 2032-01-20 | 595 | 2033-09-06 | **sim** |

### Convergência

| Propulsor | Ativos | Encontro (km) | Δv ida (km/s) | Δv volta (km/s) | v∞ na Terra (km/s) | Mudança do orbitador na última iteração do fecho | Erro contínuo da ida (km; km/s) | Erro contínuo da volta (km; km/s) | Otimizador (ida; volta) | Nota |
| :- | -: | -: | -: | -: | -: | -: | :- | :- | :- | :- |
| XIPS-25 | 6 | 380 | 4,890 | 2,446 | 3,61 | 4,3e−05 | 1 834; 2,0e−04 | 67; 1,0e−05 | Optimization terminated successfully, 774 it.; Optimization terminated successfully, 361 it. | — |
| XIPS-25 | 7 | 380 | 4,905 | 2,427 | 3,78 | 4,4e−08 | 2 051; 2,2e−04 | 92; 1,4e−05 | Optimization terminated successfully, 48 it.; Optimization terminated successfully, 248 it. | convergiu na segunda passada, a partir de n = 8 |
| XIPS-25 | 8 | 380 | 4,913 | 2,425 | 3,80 | 8,7e−06 | 2 207; 2,4e−04 | 91; 1,4e−05 | Optimization terminated successfully, 235 it.; Optimization terminated successfully, 276 it. | — |
| XIPS-25 | 9 | 380 | 4,918 | 2,422 | 3,82 | 8,6e−09 | 2 238; 2,4e−04 | 93; 1,4e−05 | Optimization terminated successfully, 171 it.; Optimization terminated successfully, 152 it. | — |
| XIPS-25 | 10 | 380 | 4,919 | 2,419 | 3,84 | 6,2e−07 | 2 279; 2,5e−04 | 95; 1,5e−05 | Optimization terminated successfully, 275 it.; Iteration limit reached, 800 it. | — |
| XIPS-25 | 11 | 380 | 4,921 | 2,417 | 3,86 | 1,1e−05 | 2 337; 2,6e−04 | 98; 1,5e−05 | Optimization terminated successfully, 324 it.; Optimization terminated successfully, 437 it. | — |
| XIPS-25 | 12 | 380 | 4,921 | 2,417 | 3,87 | 2,8e−08 | 2 377; 2,6e−04 | 98; 1,5e−05 | Optimization terminated successfully, 196 it.; Optimization terminated successfully, 6 it. | — |
| NEXT-C | 3 | 380 | 5,004 | 2,435 | 3,70 | 1,3e−05 | 4 044; 4,3e−04 | 31; 4,8e−06 | Optimization terminated successfully, 314 it.; Optimization terminated successfully, 186 it. | — |
| NEXT-C | 4 | 380 | 5,017 | 2,427 | 3,78 | 5,9e−08 | 4 245; 4,6e−04 | 35; 5,3e−06 | Optimization terminated successfully, 498 it.; Optimization terminated successfully, 183 it. | — |
| NEXT-C | 5 | 380 | 5,029 | 2,421 | 3,83 | 2,3e−07 | 4 446; 4,9e−04 | 40; 6,1e−06 | Optimization terminated successfully, 225 it.; Optimization terminated successfully, 402 it. | — |
| NEXT-C | 6 | 380 | 5,027 | 2,418 | 3,85 | 3,1e−09 | 4 553; 5,0e−04 | 40; 6,3e−06 | Optimization terminated successfully, 198 it.; Optimization terminated successfully, 113 it. | — |
| NEXT-C | 7 | 380 | 5,024 | 2,416 | 3,87 | 2,8e−05 | 4 460; 5,0e−04 | 42; 6,4e−06 | Optimization terminated successfully, 302 it.; Optimization terminated successfully, 280 it. | — |
| XIPS-25 | 6 | 814 | 4,891 | 2,433 | 4,36 | 1,2e−05 | 1 994; 2,1e−04 | 35; 6,3e−06 | Optimization terminated successfully, 274 it.; Optimization terminated successfully, 209 it. | — |
| XIPS-25 | 7 | 814 | 4,914 | 2,426 | 4,57 | 7,8e−07 | 2 222; 2,4e−04 | 41; 7,3e−06 | Optimization terminated successfully, 187 it.; Optimization terminated successfully, 180 it. | convergiu na segunda passada, a partir de n = 8 |
| XIPS-25 | 8 | 814 | 4,913 | 2,425 | 4,61 | 3,2e−06 | 2 391; 2,6e−04 | 44; 7,6e−06 | Optimization terminated successfully, 197 it.; Optimization terminated successfully, 118 it. | — |
| XIPS-25 | 9 | 814 | 4,911 | 2,424 | 4,63 | 4,4e−07 | 2 449; 2,7e−04 | 45; 7,7e−06 | Optimization terminated successfully, 134 it.; Optimization terminated successfully, 151 it. | — |
| XIPS-25 | 10 | 814 | 4,908 | 2,423 | 4,65 | 1,0e−04 | 2 510; 2,8e−04 | 46; 7,9e−06 | Optimization terminated successfully, 428 it.; Optimization terminated successfully, 275 it. | — |
| XIPS-25 | 11 | 814 | 4,923 | 2,423 | 4,67 | 5,7e−08 | 2 572; 2,8e−04 | 46; 8,0e−06 | Optimization terminated successfully, 199 it.; Optimization terminated successfully, 180 it. | convergiu na segunda passada, a partir de n = 12 |
| XIPS-25 | 12 | 814 | 4,924 | 2,423 | 4,67 | 1,2e−07 | 2 574; 2,8e−04 | 47; 8,0e−06 | Optimization terminated successfully, 355 it.; Iteration limit reached, 800 it. | — |
| NEXT-C | 3 | 814 | 5,009 | 2,438 | 3,69 | 9,0e−06 | 3 037; 3,3e−04 | 135; 2,1e−05 | Optimization terminated successfully, 179 it.; Optimization terminated successfully, 243 it. | convergiu na segunda passada, a partir de n = 4 |
| NEXT-C | 4 | 814 | 5,020 | 2,427 | 3,79 | 1,3e−04 | 3 258; 3,5e−04 | 165; 2,5e−05 | Optimization terminated successfully, 195 it.; Optimization terminated successfully, 370 it. | — |
| NEXT-C | 5 | 814 | 5,018 | 2,424 | 3,82 | 2,2e−06 | 3 382; 3,7e−04 | 170; 2,6e−05 | Optimization terminated successfully, 500 it.; Iteration limit reached, 800 it. | — |
| NEXT-C | 6 | 814 | 5,028 | 2,421 | 3,84 | 3,5e−07 | 3 468; 3,8e−04 | 177; 2,7e−05 | Optimization terminated successfully, 441 it.; Optimization terminated successfully, 127 it. | — |
| NEXT-C | 7 | 814 | 5,025 | 2,419 | 3,85 | 3,7e−06 | 3 467; 3,8e−04 | 185; 2,9e−05 | Optimization terminated successfully, 521 it.; Optimization terminated successfully, 173 it. | — |
