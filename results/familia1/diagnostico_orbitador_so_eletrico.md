# Diagnóstico do orbitador só elétrico da família 1 (gerado por tools/orbitador_so_eletrico.py)

Fora da comparação do CI (regra 6): soluções de otimização (mínimos locais). Calculado, NÃO validado.

## (b) Caso publicado: Joffre 2018 [F121] com massa e empuxo de Yau 2021 [F22]

### Fig. 4, esquerda: empuxo constante, chegada com v infinito (captura química), só com os módulos de v infinito publicados

Δv publicado 2,59 km/s; Isp 3 900 s; o Δv publicado não fica entre dois empuxos convergidos da varredura.

| Empuxo (N) | Convergiu | Critério | Δv (km/s) | Δv dos arcos (km/s) | δ partida (°) | δ chegada, equador de Marte (°) | Erro contínuo (km; km/s) |
| -: | :- | :- | -: | :- | -: | -: | :- |
| 1,50 | sim | Optimization terminated successfully | 1,986 | 1,103, 0,542, 0,341 | 34,21 | −13,82 | 34; 4,3e−06 |
| 1,25 | sim | Optimization terminated successfully | 1,987 | 1,123, 0,505, 0,359 | 34,28 | −13,75 | 31; 3,6e−06 |
| 1,20 | sim | Optimization terminated successfully | 1,987 | 1,128, 0,496, 0,363 | 34,29 | −13,72 | 31; 3,4e−06 |
| 1,15 | sim | Optimization terminated successfully | 1,987 | 1,136, 0,486, 0,364 | 34,31 | −13,70 | 30; 3,2e−06 |
| 1,10 | sim | Optimization terminated successfully | 1,987 | 1,141, 0,480, 0,366 | 34,31 | −13,68 | 30; 3,1e−06 |
| 1,05 | sim | Optimization terminated successfully | 1,988 | 1,146, 0,474, 0,368 | 34,30 | −13,66 | 30; 3,1e−06 |
| 1,00 | sim | Optimization terminated successfully | 1,988 | 1,144, 0,479, 0,365 | 34,20 | −13,67 | 30; 3,1e−06 |
| 0,75 | sim | Optimization terminated successfully | 1,990 | 1,222, 0,305, 0,463 | 34,21 | −13,37 | 29; 2,7e−06 |

### Fig. 4, esquerda: empuxo constante, chegada com v infinito (captura química), com as declinações publicadas impostas

Δv publicado 2,59 km/s; Isp 3 900 s; o Δv publicado não fica entre dois empuxos convergidos da varredura.

| Empuxo (N) | Convergiu | Critério | Δv (km/s) | Δv dos arcos (km/s) | δ partida (°) | δ chegada, equador de Marte (°) | Erro contínuo (km; km/s) |
| -: | :- | :- | -: | :- | -: | -: | :- |
| 1,50 | sim | Optimization terminated successfully | 2,376 | 0,787, 1,404, 0,185 | 4,97 | −11,90 | 202; 2,1e−05 |
| 1,25 | sim | Optimization terminated successfully | 2,379 | 0,787, 1,417, 0,175 | 4,97 | −11,90 | 200; 2,0e−05 |
| 1,20 | sim | Optimization terminated successfully | 2,380 | 0,786, 1,415, 0,179 | 4,97 | −11,90 | 198; 2,0e−05 |
| 1,15 | sim | Optimization terminated successfully | 2,381 | 0,785, 1,412, 0,183 | 4,97 | −11,90 | 195; 2,0e−05 |
| 1,10 | sim | Optimization terminated successfully | 2,382 | 0,787, 1,423, 0,172 | 4,97 | −11,90 | 188; 1,9e−05 |
| 1,05 | sim | Optimization terminated successfully | 2,383 | 0,785, 1,429, 0,169 | 4,97 | −11,90 | 179; 1,8e−05 |
| 1,00 | sim | Optimization terminated successfully | 2,385 | 0,784, 1,436, 0,165 | 4,97 | −11,90 | 172; 1,8e−05 |
| 0,75 | sim | Optimization terminated successfully | 2,398 | 0,776, 1,489, 0,133 | 4,97 | −11,90 | 160; 1,6e−05 |

### Fig. 4, direita: chegada com v infinito = 0, arco de voo livre entre dois arcos de empuxo, só com os módulos de v infinito publicados

Δv publicado 5,94 km/s; Isp 3 900 s; empuxo em que o Δv calculado iguala o publicado: 1,176 N (1,8e−04 m/s² com 6 500 kg), contra o máximo de 0,75 N de [F22].

| Empuxo (N) | Convergiu | Critério | Δv (km/s) | Δv dos arcos (km/s) | δ partida (°) | δ chegada, equador de Marte (°) | Erro contínuo (km; km/s) |
| -: | :- | :- | -: | :- | -: | -: | :- |
| 1,50 | sim | Optimization terminated successfully | 5,384 | 2,876, 2,508 | 14,71 | — | 1 238; 1,2e−04 |
| 1,25 | sim | Optimization terminated successfully | 5,730 | 3,069, 2,661 | 13,50 | — | 1 110; 1,1e−04 |
| 1,20 | sim | Optimization terminated successfully | 5,860 | 3,180, 2,680 | 13,15 | — | 955; 9,5e−05 |
| 1,15 | sim | Optimization terminated successfully | 6,029 | 3,283, 2,745 | 13,36 | — | 857; 8,6e−05 |
| 1,10 | sim | Optimization terminated successfully | 6,250 | 3,466, 2,783 | 13,50 | — | 669; 6,9e−05 |
| 1,05 | sim | Optimization terminated successfully | 6,599 | 3,623, 2,975 | 13,82 | — | 571; 6,0e−05 |
| 1,00 | não | Iteration limit reached | — | — | — | — | — |
| 0,75 | não | Iteration limit reached | — | — | — | — | — |

### Fig. 4, direita: chegada com v infinito = 0, arco de voo livre entre dois arcos de empuxo, com as declinações publicadas impostas

Δv publicado 5,94 km/s; Isp 3 900 s; empuxo em que o Δv calculado iguala o publicado: 1,200 N (1,8e−04 m/s² com 6 500 kg), contra o máximo de 0,75 N de [F22].

| Empuxo (N) | Convergiu | Critério | Δv (km/s) | Δv dos arcos (km/s) | δ partida (°) | δ chegada, equador de Marte (°) | Erro contínuo (km; km/s) |
| -: | :- | :- | -: | :- | -: | -: | :- |
| 1,50 | sim | Optimization terminated successfully | 5,463 | 2,961, 2,502 | −0,06 | — | 1 259; 1,3e−04 |
| 1,25 | sim | Optimization terminated successfully | 5,812 | 3,159, 2,653 | −0,06 | — | 1 086; 1,1e−04 |
| 1,20 | sim | Optimization terminated successfully | 5,940 | 3,250, 2,690 | −0,06 | — | 935; 9,3e−05 |
| 1,15 | sim | Optimization terminated successfully | 6,118 | 3,381, 2,737 | −0,06 | — | 781; 7,9e−05 |
| 1,10 | sim | Optimization terminated successfully | 6,346 | 3,575, 2,771 | −0,06 | — | 628; 6,5e−05 |
| 1,05 | sim | Optimization terminated successfully | 6,772 | 3,731, 3,041 | −0,06 | — | 549; 5,8e−05 |
| 1,00 | não | Positive directional derivative for linesearch | — | — | — | — | — |
| 0,75 | não | Positive directional derivative for linesearch | — | — | — | — | — |

## (a) e (c) Família 1

| Propulsor | Ativos | Encontro (km) | Instalados | Potência (kW) | Xe (kg) | Xe por propulsor (kg) | Vida (kg) | Propulsores + PPU (kg) | Orbitador (kg) | Margem no Falcon Heavy | C3 (km²/s²) | DLA (°) | Partida da Terra | Ida (d) | Chegada a Marte | Descida (d) | Pronto no encontro | Último lançamento do MAV | Lançamento do MAV | Subida (d) | Partida de Marte | Volta (d) | Chegada à Terra | Descida cruza conjunção | Encontro e subida cruzam conjunção | Fecha? |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- | -: | :- | :- | :- | -: | :- | -: | :- | :- | :- | :- |
| XIPS-25 | 6 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 1.50e-09** |
| XIPS-25 | 7 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 5.71e-09** |
| XIPS-25 | 8 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 2.81e-10** |
| XIPS-25 | 9 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 5.42e-11** |
| XIPS-25 | 10 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 8.03e-09** |
| XIPS-25 | 11 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 1.38e-08** |
| XIPS-25 | 12 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 4.07e-06** |
| NEXT-C | 3 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 1.18e-09** |
| NEXT-C | 4 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 1.23e-09** |
| NEXT-C | 5 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 1.37e-08** |
| NEXT-C | 6 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 1.63e-09** |
| NEXT-C | 7 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 9.83e-10** |
| XIPS-25 | 6 | 814 | 15 | 27,0 | 2 171 | 155 | 158 | 525 | 6 438 | 129,9 % | 0,60 | 28,5 | 2028-09-18 | 603 | 2030-05-14 | 237 | 2031-01-07 | 2032-04-26 | 2031-01-07 | 206 | 2032-01-17 | 650 | 2033-10-28 | sim | não | **sim** |
| XIPS-25 | 7 | 814 | 16 | 31,5 | 2 362 | 157 | 158 | 560 | 7 001 | 111,5 % | 0,57 | 28,5 | 2028-09-18 | 602 | 2030-05-13 | 221 | 2030-12-21 | 2032-04-26 | 2030-12-21 | 192 | 2032-01-17 | 650 | 2033-10-28 | sim | não | **sim** |
| XIPS-25 | 8 | 814 | 18 | 36,0 | 2 583 | 152 | 158 | 630 | 7 659 | 93,3 % | 0,58 | 28,5 | 2028-09-18 | 601 | 2030-05-12 | 212 | 2030-12-10 | 2032-04-26 | 2030-12-10 | 184 | 2032-01-18 | 650 | 2033-10-29 | sim | não | **sim** |
| XIPS-25 | 9 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 1.24e-09; segunda passada, a partir de n = 10: NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 5.00e-08** |
| XIPS-25 | 10 | 814 | 20 | 45,0 | 2 959 | 156 | 158 | 700 | 8 777 | 68,7 % | 0,57 | 28,5 | 2028-09-18 | 601 | 2030-05-12 | 194 | 2030-11-23 | 2032-04-26 | 2030-11-23 | 168 | 2032-01-18 | 650 | 2033-10-29 | sim | não | **sim** |
| XIPS-25 | 11 | 814 | 21 | 49,5 | 3 146 | 157 | 158 | 735 | 9 335 | 58,6 % | 0,58 | 28,5 | 2028-09-18 | 601 | 2030-05-12 | 188 | 2030-11-16 | 2032-04-26 | 2030-11-16 | 163 | 2032-01-18 | 651 | 2033-10-30 | sim | não | **sim** |
| XIPS-25 | 12 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 7.33e-10** |
| NEXT-C | 3 | 814 | 4 | 22,0 | 1 378 | 459 | 918 | 196 | 4 616 | 221,5 % | 0,45 | 28,5 | 2028-09-17 | 601 | 2030-05-11 | 246 | 2031-01-12 | 2032-04-26 | 2031-01-12 | 216 | 2032-01-24 | 595 | 2033-09-10 | sim | não | **sim** |
| NEXT-C | 4 | 814 | 5 | 29,3 | 1 622 | 406 | 918 | 245 | 5 434 | 173,2 % | 0,43 | 28,5 | 2028-09-18 | 602 | 2030-05-13 | 217 | 2030-12-16 | 2032-04-26 | 2030-12-16 | 190 | 2032-01-22 | 594 | 2033-09-07 | sim | não | **sim** |
| NEXT-C | 5 | 814 | 6 | 36,6 | 1 865 | 373 | 918 | 294 | 6 252 | 137,5 % | 0,42 | 28,5 | 2028-09-18 | 601 | 2030-05-11 | 200 | 2030-11-27 | 2032-04-26 | 2030-11-27 | 175 | 2032-01-22 | 594 | 2033-09-07 | sim | não | **sim** |
| NEXT-C | 6 | 814 | 7 | 44,0 | 2 110 | 352 | 918 | 343 | 7 070 | 110,0 % | 0,42 | 28,5 | 2028-09-18 | 600 | 2030-05-12 | 188 | 2030-11-17 | 2032-04-26 | 2030-11-17 | 165 | 2032-01-22 | 593 | 2033-09-06 | sim | não | **sim** |
| NEXT-C | 7 | 814 | 8 | 51,3 | 2 355 | 336 | 918 | 392 | 7 890 | 88,3 % | 0,41 | 28,5 | 2028-09-18 | 600 | 2030-05-11 | 180 | 2030-11-07 | 2032-04-26 | 2030-11-07 | 158 | 2032-01-22 | 593 | 2033-09-06 | sim | não | **sim** |

### Convergência

| Propulsor | Ativos | Encontro (km) | Δv ida (km/s) | Δv volta (km/s) | v infinito na Terra (km/s) | Mudança do orbitador na última iteração do fecho | Erro contínuo da ida (km; km/s) | Erro contínuo da volta (km; km/s) | Otimizador (ida; volta) | Nota |
| :- | -: | -: | -: | -: | -: | -: | :- | :- | :- | :- |
| XIPS-25 | 6 | 814 | 4,907 | 2,429 | 4,51 | 2,8e−06 | 2 239; 2,4e−04 | 71; 1,3e−05 | Optimization terminated successfully, 193 it.; Optimization terminated successfully, 662 it. | — |
| XIPS-25 | 7 | 814 | 4,918 | 2,428 | 4,55 | 1,8e−08 | 2 352; 2,6e−04 | 73; 1,3e−05 | Optimization terminated successfully, 235 it.; Optimization terminated successfully, 124 it. | — |
| XIPS-25 | 8 | 814 | 4,913 | 2,427 | 4,58 | 3,0e−05 | 2 403; 2,6e−04 | 75; 1,3e−05 | Optimization terminated successfully, 226 it.; Optimization terminated successfully, 66 it. | — |
| XIPS-25 | 10 | 814 | 4,908 | 2,425 | 4,64 | 2,8e−06 | 2 547; 2,8e−04 | 81; 1,4e−05 | Optimization terminated successfully, 467 it.; Optimization terminated successfully, 237 it. | — |
| XIPS-25 | 11 | 814 | 4,902 | 2,424 | 4,66 | 3,7e−05 | 2 561; 2,8e−04 | 84; 1,4e−05 | Optimization terminated successfully, 494 it.; Optimization terminated successfully, 283 it. | — |
| NEXT-C | 3 | 814 | 5,015 | 2,438 | 3,68 | 9,5e−07 | 2 328; 2,5e−04 | 133; 2,0e−05 | Optimization terminated successfully, 184 it.; Optimization terminated successfully, 220 it. | convergiu na segunda passada, a partir de n = 4 |
| NEXT-C | 4 | 814 | 5,023 | 2,427 | 3,79 | 4,0e−05 | 2 539; 2,8e−04 | 163; 2,5e−05 | Optimization terminated successfully, 443 it.; Optimization terminated successfully, 127 it. | — |
| NEXT-C | 5 | 814 | 5,019 | 2,424 | 3,82 | 1,7e−06 | 2 606; 2,8e−04 | 168; 2,6e−05 | Optimization terminated successfully, 387 it.; Optimization terminated successfully, 336 it. | — |
| NEXT-C | 6 | 814 | 5,021 | 2,421 | 3,84 | 5,4e−06 | 2 683; 2,9e−04 | 175; 2,7e−05 | Optimization terminated successfully, 359 it.; Optimization terminated successfully, 327 it. | — |
| NEXT-C | 7 | 814 | 5,025 | 2,419 | 3,85 | 7,5e−06 | 2 784; 3,1e−04 | 182; 2,8e−05 | Optimization terminated successfully, 290 it.; Optimization terminated successfully, 465 it. | — |
