# Diagnóstico do orbitador só elétrico da família 1 (gerado por tools/orbitador_so_eletrico.py)

Fora da comparação do CI (regra 6): soluções de otimização (mínimos locais). Calculado, NÃO validado.

## (b) Caso publicado: Joffre 2018 [F121] com massa e empuxo de Yau 2021 [F22]

### Fig. 4, esquerda: empuxo constante, chegada com v infinito (captura química), só com os módulos de v infinito publicados

Δv publicado 2,59 km/s; Isp 3 900 s; o Δv publicado não fica entre dois empuxos convergidos da varredura.

| Empuxo (N) | Convergiu | Critério | Δv (km/s) | Δv dos arcos (km/s) | δ partida (°) | δ chegada, equador de Marte (°) | Erro contínuo (km; km/s) |
| -: | :- | :- | -: | :- | -: | -: | :- |
| 1,50 | sim | Optimization terminated successfully | 1,986 | 1,103, 0,541, 0,341 | 34,21 | −13,82 | 34; 4,3e−06 |
| 1,25 | sim | Optimization terminated successfully | 1,987 | 1,121, 0,505, 0,361 | 34,27 | −13,74 | 31; 3,6e−06 |
| 1,20 | sim | Optimization terminated successfully | 1,987 | 1,129, 0,496, 0,362 | 34,30 | −13,72 | 31; 3,4e−06 |
| 1,15 | sim | Optimization terminated successfully | 1,987 | 1,134, 0,487, 0,366 | 34,30 | −13,69 | 30; 3,2e−06 |
| 1,10 | sim | Optimization terminated successfully | 1,987 | 1,141, 0,479, 0,367 | 34,31 | −13,68 | 30; 3,1e−06 |
| 1,05 | sim | Optimization terminated successfully | 1,988 | 1,147, 0,473, 0,368 | 34,31 | −13,66 | 30; 3,1e−06 |
| 1,00 | sim | Optimization terminated successfully | 1,988 | 1,144, 0,478, 0,365 | 34,20 | −13,67 | 30; 3,1e−06 |
| 0,75 | sim | Optimization terminated successfully | 1,990 | 1,224, 0,302, 0,465 | 34,22 | −13,36 | 29; 2,7e−06 |

### Fig. 4, esquerda: empuxo constante, chegada com v infinito (captura química), com as declinações publicadas impostas

Δv publicado 2,59 km/s; Isp 3 900 s; o Δv publicado não fica entre dois empuxos convergidos da varredura.

| Empuxo (N) | Convergiu | Critério | Δv (km/s) | Δv dos arcos (km/s) | δ partida (°) | δ chegada, equador de Marte (°) | Erro contínuo (km; km/s) |
| -: | :- | :- | -: | :- | -: | -: | :- |
| 1,50 | sim | Optimization terminated successfully | 2,376 | 0,787, 1,404, 0,185 | 4,97 | −11,90 | 202; 2,1e−05 |
| 1,25 | sim | Optimization terminated successfully | 2,379 | 0,787, 1,416, 0,176 | 4,97 | −11,90 | 200; 2,0e−05 |
| 1,20 | sim | Optimization terminated successfully | 2,380 | 0,786, 1,415, 0,179 | 4,97 | −11,90 | 198; 2,0e−05 |
| 1,15 | sim | Optimization terminated successfully | 2,381 | 0,785, 1,412, 0,183 | 4,97 | −11,90 | 195; 2,0e−05 |
| 1,10 | sim | Optimization terminated successfully | 2,382 | 0,787, 1,423, 0,172 | 4,97 | −11,90 | 188; 1,9e−05 |
| 1,05 | sim | Optimization terminated successfully | 2,383 | 0,785, 1,430, 0,169 | 4,97 | −11,90 | 179; 1,8e−05 |
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
| 1,00 | não | Positive directional derivative for linesearch | — | — | — | — | — |
| 0,75 | não | Positive directional derivative for linesearch | — | — | — | — | — |

### Fig. 4, direita: chegada com v infinito = 0, arco de voo livre entre dois arcos de empuxo, com as declinações publicadas impostas

Δv publicado 5,94 km/s; Isp 3 900 s; empuxo em que o Δv calculado iguala o publicado: 1,200 N (1,8e−04 m/s² com 6 500 kg), contra o máximo de 0,75 N de [F22].

| Empuxo (N) | Convergiu | Critério | Δv (km/s) | Δv dos arcos (km/s) | δ partida (°) | δ chegada, equador de Marte (°) | Erro contínuo (km; km/s) |
| -: | :- | :- | -: | :- | -: | -: | :- |
| 1,50 | sim | Optimization terminated successfully | 5,463 | 2,961, 2,502 | −0,06 | — | 1 259; 1,3e−04 |
| 1,25 | sim | Optimization terminated successfully | 5,812 | 3,159, 2,653 | −0,06 | — | 1 086; 1,1e−04 |
| 1,20 | sim | Optimization terminated successfully | 5,940 | 3,250, 2,691 | −0,06 | — | 935; 9,3e−05 |
| 1,15 | sim | Optimization terminated successfully | 6,118 | 3,381, 2,736 | −0,06 | — | 781; 7,9e−05 |
| 1,10 | sim | Optimization terminated successfully | 6,346 | 3,575, 2,771 | −0,06 | — | 628; 6,5e−05 |
| 1,05 | sim | Optimization terminated successfully | 6,772 | 3,731, 3,041 | −0,06 | — | 549; 5,8e−05 |
| 1,00 | não | Positive directional derivative for linesearch | — | — | — | — | — |
| 0,75 | não | Positive directional derivative for linesearch | — | — | — | — | — |

## (a) e (c) Família 1

| Propulsor | Ativos | Encontro (km) | Instalados | Potência (kW) | Xe (kg) | Xe por propulsor (kg) | Vida (kg) | Propulsores + PPU (kg) | Orbitador (kg) | Margem no Falcon Heavy | C3 (km²/s²) | DLA (°) | Partida da Terra | Ida (d) | Chegada a Marte | Descida (d) | Pronto no encontro | Último lançamento do MAV | Lançamento do MAV | Subida (d) | Partida de Marte | Volta (d) | Chegada à Terra | Descida cruza conjunção | Encontro e subida cruzam conjunção | Fecha? |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- | -: | :- | :- | :- | -: | :- | -: | :- | :- | :- | :- |
| XIPS-25 | 1 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução viável encontrada** (menor resíduo 2,0e−01; NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.36e-02; segunda passada, a partir de n = 2: NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.36e-02) |
| XIPS-25 | 2 | 380 | 11 | 9,0 | 1 507 | 151 | 158 | 385 | 4 320 | 232,7 % | 2,13 | 23,5 | 2028-09-01 | 956 | 2031-04-15 | 520 | 2032-09-17 | 2032-04-26 | 2032-09-17 | 452 | 2034-01-05 | 889 | 2036-06-12 | sim | não | não |
| XIPS-25 | 3 | 380 | 12 | 13,5 | 1 676 | 152 | 158 | 420 | 4 856 | 199,4 % | 1,53 | 23,7 | 2028-09-01 | 864 | 2031-01-12 | 469 | 2032-04-26 | 2032-04-26 | 2032-08-03 | 336 | 2033-11-07 | 705 | 2035-10-13 | não | não | **sim** |
| XIPS-25 | 4 | 380 | 13 | 18,0 | 1 851 | 154 | 158 | 455 | 5 397 | 173,4 % | 0,76 | 28,5 | 2028-09-18 | 561 | 2030-04-02 | 322 | 2031-02-18 | 2032-04-26 | 2031-02-18 | 278 | 2032-01-06 | 657 | 2033-10-24 | sim | não | **sim** |
| XIPS-25 | 5 | 380 | 14 | 22,5 | 2 020 | 155 | 158 | 490 | 5 934 | 147,5 % | 1,01 | 28,5 | 2028-10-14 | 487 | 2030-02-12 | 284 | 2030-11-24 | 2032-04-26 | 2030-11-24 | 246 | 2031-10-08 | 703 | 2033-09-10 | sim | não | **sim** |
| XIPS-25 | 6 | 380 | 16 | 27,0 | 2 248 | 150 | 158 | 560 | 6 600 | 122,7 % | 0,96 | 28,5 | 2028-10-14 | 507 | 2030-03-05 | 263 | 2030-11-24 | 2032-04-26 | 2030-11-24 | 227 | 2031-10-03 | 707 | 2033-09-09 | sim | não | **sim** |
| XIPS-25 | 7 | 380 | 17 | 31,5 | 2 446 | 153 | 158 | 595 | 7 171 | 105,2 % | 0,90 | 28,5 | 2028-10-15 | 566 | 2030-05-04 | 245 | 2031-01-05 | 2032-04-26 | 2031-01-05 | 212 | 2031-09-17 | 722 | 2033-09-08 | sim | não | **sim** |
| XIPS-25 | 8 | 380 | 18 | 36,0 | 2 642 | 155 | 158 | 630 | 7 740 | 90,3 % | 0,86 | 28,5 | 2028-10-15 | 569 | 2030-05-06 | 231 | 2030-12-24 | 2032-04-26 | 2030-12-24 | 200 | 2031-09-10 | 728 | 2033-09-07 | sim | não | **sim** |
| XIPS-25 | 9 | 380 | 19 | 40,5 | 2 834 | 157 | 158 | 665 | 8 303 | 77,4 % | 0,85 | 28,5 | 2028-10-15 | 586 | 2030-05-24 | 221 | 2030-12-31 | 2032-04-26 | 2030-12-31 | 191 | 2031-09-10 | 728 | 2033-09-07 | sim | não | **sim** |
| XIPS-25 | 10 | 380 | 21 | 45,0 | 3 063 | 153 | 158 | 735 | 8 971 | 64,3 % | 0,82 | 28,5 | 2028-10-15 | 597 | 2030-06-05 | 214 | 2031-01-06 | 2032-04-26 | 2031-01-06 | 185 | 2031-09-10 | 727 | 2033-09-06 | sim | não | **sim** |
| XIPS-25 | 11 | 380 | 22 | 49,5 | 3 260 | 155 | 158 | 770 | 9 541 | 54,6 % | 0,79 | 28,5 | 2028-10-16 | 598 | 2030-06-05 | 207 | 2030-12-30 | 2032-04-26 | 2030-12-30 | 179 | 2031-09-09 | 727 | 2033-09-06 | sim | não | **sim** |
| XIPS-25 | 12 | 380 | 23 | 54,0 | 3 455 | 157 | 158 | 805 | 10 108 | 45,9 % | 0,78 | 28,5 | 2028-10-16 | 598 | 2030-06-06 | 201 | 2030-12-25 | 2032-04-26 | 2030-12-25 | 174 | 2031-09-09 | 727 | 2033-09-05 | sim | não | **sim** |
| XIPS-25 (87 kg) | 1 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução viável encontrada** (menor resíduo 1,7e+00; NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 2.80e-01; segunda passada, a partir de n = 3: NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 2.80e-01) |
| XIPS-25 (87 kg) | 2 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução viável encontrada** (menor resíduo 1,8e+00; NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.93e+00; segunda passada, a partir de n = 3: NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.93e+00) |
| XIPS-25 (87 kg) | 3 | 380 | 29 | 13,5 | 2 390 | 85 | 87 | 1 015 | 6 709 | 112,8 % | 2,46 | 24,0 | 2028-09-01 | 792 | 2030-11-01 | 541 | 2032-04-26 | 2032-04-26 | 2032-08-03 | 467 | 2034-04-16 | 900 | 2036-10-02 | não | não | **sim** |
| XIPS-25 (87 kg) | 4 | 380 | 33 | 18,0 | 2 736 | 86 | 87 | 1 155 | 7 630 | 91,3 % | 1,33 | 24,0 | 2028-09-01 | 881 | 2031-01-30 | 452 | 2032-04-26 | 2032-04-26 | 2032-08-03 | 395 | 2034-04-10 | 900 | 2036-09-26 | não | não | **sim** |
| XIPS-25 (87 kg) | 5 | 380 | 37 | 22,5 | 3 099 | 86 | 87 | 1 295 | 8 571 | 71,8 % | 0,86 | 24,9 | 2028-09-01 | 951 | 2031-04-09 | 408 | 2032-05-21 | 2032-04-26 | 2032-08-03 | 353 | 2034-04-06 | 900 | 2036-09-22 | não | não | não |
| XIPS-25 (87 kg) | 6 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **sem convergência do otimizador** (menor resíduo 2,7e−10; NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 1.47e-08; segunda passada, a partir de n = 5: NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 2.40e-09) |
| XIPS-25 (87 kg) | 7 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **sem convergência do otimizador** (menor resíduo 6,2e−09; NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 2.52e-09; segunda passada, a partir de n = 11: NaoConverge: otimizador não convergiu: Iteration limit reached; resíduo 2.52e-09) |
| XIPS-25 (87 kg) | 8 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução viável encontrada** (menor resíduo 6,8e−01; NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 4.27e+00; segunda passada, a partir de n = 11: NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 4.27e+00) |
| XIPS-25 (87 kg) | 9 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução viável encontrada** (menor resíduo 1,3e−01; NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 2.22e-01; segunda passada, a partir de n = 11: NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 2.22e-01) |
| XIPS-25 (87 kg) | 10 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução viável encontrada** (menor resíduo 6,4e−02; NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 3.12e-02; segunda passada, a partir de n = 11: NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 3.12e-02) |
| XIPS-25 (87 kg) | 11 | 380 | 76 | 49,5 | 6 482 | 86 | 87 | 2 660 | 16 559 | −11,1 % | 0,88 | 25,0 | 2028-09-01 | 828 | 2030-12-07 | 411 | 2032-01-23 | 2032-04-26 | 2032-01-23 | 310 | 2032-12-20 | 900 | 2035-06-08 | não | sim | não |
| XIPS-25 (87 kg) | 12 | 380 | 100 | 54,0 | 8 600 | 87 | 87 | 3 500 | 20 776 | −29,1 % | 0,88 | 25,3 | 2028-09-01 | 710 | 2030-08-12 | 413 | 2031-09-30 | 2032-04-26 | 2031-09-30 | 357 | 2032-10-13 | 807 | 2034-12-29 | não | sim | não |
| NEXT-C | 1 | 380 | 3 | 7,3 | 1 000 | 500 | 918 | 147 | 3 200 | 346,5 % | 2,42 | 22,7 | 2028-09-01 | 953 | 2031-04-11 | 561 | 2032-10-24 | 2032-04-26 | 2032-10-24 | 491 | 2034-04-13 | 900 | 2036-09-29 | sim | não | não |
| NEXT-C | 2 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução viável encontrada** (menor resíduo 2,7e+01; NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.19e+00; segunda passada, a partir de n = 3: NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.19e+00) |
| NEXT-C | 3 | 380 | 4 | 22,0 | 1 420 | 473 | 918 | 196 | 4 676 | 216,8 % | 0,55 | 28,5 | 2028-09-18 | 568 | 2030-04-08 | 268 | 2031-01-02 | 2032-04-26 | 2031-01-02 | 235 | 2031-11-06 | 721 | 2033-10-27 | sim | não | **sim** |
| NEXT-C | 4 | 380 | 5 | 29,3 | 1 673 | 418 | 918 | 245 | 5 505 | 169,3 % | 0,51 | 28,5 | 2028-09-18 | 573 | 2030-04-14 | 237 | 2030-12-07 | 2032-04-26 | 2030-12-07 | 207 | 2031-09-11 | 728 | 2033-09-08 | sim | não | **sim** |
| NEXT-C | 5 | 380 | 6 | 36,6 | 1 908 | 382 | 918 | 294 | 6 313 | 134,1 % | 0,67 | 28,5 | 2028-10-14 | 535 | 2030-04-02 | 218 | 2030-11-06 | 2032-04-26 | 2030-11-06 | 191 | 2031-09-10 | 728 | 2033-09-07 | sim | não | **sim** |
| NEXT-C | 6 | 380 | 7 | 44,0 | 2 160 | 360 | 918 | 343 | 7 141 | 107,1 % | 0,63 | 28,5 | 2028-10-14 | 576 | 2030-05-13 | 205 | 2030-12-05 | 2032-04-26 | 2030-12-05 | 180 | 2031-09-10 | 727 | 2033-09-06 | sim | não | **sim** |
| NEXT-C | 7 | 380 | 8 | 51,3 | 2 413 | 345 | 918 | 392 | 7 970 | 85,7 % | 0,59 | 28,5 | 2028-10-15 | 590 | 2030-05-28 | 196 | 2030-12-11 | 2032-04-26 | 2030-12-11 | 172 | 2031-09-09 | 727 | 2033-09-05 | sim | não | **sim** |
| XIPS-25 | 1 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução viável encontrada** (menor resíduo 7,7e−01; NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 9.10e-02; segunda passada, a partir de n = 3: NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 9.10e-02) |
| XIPS-25 | 2 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução viável encontrada** (menor resíduo 1,3e+00; NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.07e+00; segunda passada, a partir de n = 3: NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.07e+00) |
| XIPS-25 | 3 | 814 | 11 | 13,5 | 1 566 | 157 | 158 | 385 | 4 656 | 210,7 % | 1,79 | 23,3 | 2028-09-01 | 876 | 2031-01-24 | 457 | 2032-04-26 | 2032-04-26 | 2032-08-03 | 302 | 2033-09-28 | 749 | 2035-10-18 | não | não | **sim** |
| XIPS-25 | 4 | 814 | 13 | 18,0 | 1 782 | 149 | 158 | 455 | 5 305 | 178,2 % | 0,74 | 28,5 | 2028-09-18 | 560 | 2030-04-01 | 294 | 2031-01-21 | 2032-04-26 | 2031-01-21 | 255 | 2031-11-24 | 700 | 2033-10-24 | sim | não | **sim** |
| XIPS-25 | 5 | 814 | 14 | 22,5 | 1 943 | 149 | 158 | 490 | 5 833 | 151,8 % | 1,00 | 28,5 | 2028-10-14 | 468 | 2030-01-25 | 260 | 2030-10-12 | 2032-04-26 | 2030-10-12 | 225 | 2031-09-15 | 726 | 2033-09-10 | sim | não | **sim** |
| XIPS-25 | 6 | 814 | 15 | 27,0 | 2 134 | 152 | 158 | 525 | 6 396 | 130,0 % | 0,92 | 28,5 | 2028-10-14 | 473 | 2030-01-30 | 237 | 2030-09-25 | 2032-04-26 | 2030-09-25 | 206 | 2031-09-14 | 725 | 2033-09-09 | sim | não | **sim** |
| XIPS-25 | 7 | 814 | 16 | 31,5 | 2 323 | 155 | 158 | 560 | 6 956 | 111,7 % | 0,87 | 28,5 | 2028-10-15 | 473 | 2030-01-31 | 221 | 2030-09-09 | 2032-04-26 | 2030-09-09 | 192 | 2031-09-14 | 725 | 2033-09-08 | sim | não | **sim** |
| XIPS-25 | 8 | 814 | 17 | 36,0 | 2 514 | 157 | 158 | 595 | 7 519 | 96,0 % | 0,82 | 28,5 | 2028-10-15 | 469 | 2030-01-28 | 209 | 2030-08-25 | 2032-04-26 | 2030-08-25 | 181 | 2031-09-13 | 725 | 2033-09-07 | sim | não | **sim** |
| XIPS-25 | 9 | 814 | 19 | 40,5 | 2 729 | 152 | 158 | 665 | 8 170 | 80,4 % | 0,83 | 28,5 | 2028-10-15 | 487 | 2030-02-14 | 202 | 2030-09-04 | 2032-04-26 | 2030-09-04 | 175 | 2031-09-13 | 724 | 2033-09-07 | sim | não | **sim** |
| XIPS-25 | 10 | 814 | 20 | 45,0 | 2 919 | 154 | 158 | 700 | 8 731 | 68,9 % | 0,80 | 28,5 | 2028-10-15 | 511 | 2030-03-10 | 194 | 2030-09-20 | 2032-04-26 | 2030-09-20 | 168 | 2031-09-13 | 724 | 2033-09-06 | sim | não | **sim** |
| XIPS-25 | 11 | 814 | 21 | 49,5 | 3 104 | 155 | 158 | 735 | 9 287 | 58,8 % | 0,80 | 28,5 | 2028-10-16 | 557 | 2030-04-26 | 188 | 2030-10-31 | 2032-04-26 | 2030-10-31 | 163 | 2031-09-13 | 724 | 2033-09-06 | sim | não | **sim** |
| XIPS-25 | 12 | 814 | 22 | 54,0 | 3 296 | 157 | 158 | 770 | 9 851 | 49,8 % | 0,77 | 28,5 | 2028-10-16 | 584 | 2030-05-23 | 182 | 2030-11-22 | 2032-04-26 | 2030-11-22 | 158 | 2031-09-12 | 724 | 2033-09-05 | sim | não | **sim** |
| XIPS-25 (87 kg) | 1 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução viável encontrada** (menor resíduo 2,0e+00; NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.82e-01; segunda passada, a partir de n = 5: NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.82e-01) |
| XIPS-25 (87 kg) | 2 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução viável encontrada** (menor resíduo 9,5e−01; NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 9.75e-02; segunda passada, a partir de n = 5: NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 9.75e-02) |
| XIPS-25 (87 kg) | 3 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução viável encontrada** (menor resíduo 2,0e+00; NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.13e+00; segunda passada, a partir de n = 5: NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.13e+00) |
| XIPS-25 (87 kg) | 4 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução viável encontrada** (menor resíduo 1,8e+00; NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.23e+00; segunda passada, a partir de n = 5: NaoConverge: otimizador não convergiu: Positive directional derivative for linesearch; resíduo 1.23e+00) |
| XIPS-25 (87 kg) | 5 | 814 | 30 | 22,5 | 2 508 | 86 | 87 | 1 050 | 7 445 | 98,3 % | 0,74 | 25,2 | 2028-09-01 | 608 | 2030-05-01 | 330 | 2031-03-27 | 2032-04-26 | 2031-03-27 | 286 | 2032-04-16 | 553 | 2033-10-21 | sim | não | **sim** |
| XIPS-25 (87 kg) | 6 | 814 | 33 | 27,0 | 2 764 | 86 | 87 | 1 155 | 8 202 | 80,1 % | 0,71 | 25,1 | 2028-09-01 | 614 | 2030-05-07 | 303 | 2031-03-06 | 2032-04-26 | 2031-03-06 | 263 | 2032-04-17 | 555 | 2033-10-23 | sim | não | **sim** |
| XIPS-25 (87 kg) | 7 | 814 | 36 | 31,5 | 3 021 | 86 | 87 | 1 260 | 8 961 | 64,9 % | 0,67 | 25,1 | 2028-09-01 | 619 | 2030-05-13 | 283 | 2031-02-21 | 2032-04-26 | 2031-02-21 | 246 | 2032-04-18 | 555 | 2033-10-25 | sim | não | **sim** |
| XIPS-25 (87 kg) | 8 | 814 | 39 | 36,0 | 3 269 | 86 | 87 | 1 365 | 9 710 | 52,1 % | 0,70 | 25,1 | 2028-09-01 | 629 | 2030-05-22 | 269 | 2031-02-15 | 2032-04-26 | 2031-02-15 | 233 | 2032-04-16 | 558 | 2033-10-26 | sim | não | **sim** |
| XIPS-25 (87 kg) | 9 | 814 | 42 | 40,5 | 3 525 | 86 | 87 | 1 470 | 10 467 | 41,2 % | 0,68 | 25,0 | 2028-09-01 | 631 | 2030-05-25 | 258 | 2031-02-07 | 2032-04-26 | 2031-02-07 | 223 | 2032-04-17 | 558 | 2033-10-26 | sim | não | **sim** |
| XIPS-25 (87 kg) | 10 | 814 | 45 | 45,0 | 3 781 | 86 | 87 | 1 575 | 11 225 | 31,7 % | 0,67 | 25,3 | 2028-09-01 | 638 | 2030-06-01 | 249 | 2031-02-05 | 2032-04-26 | 2031-02-05 | 216 | 2032-04-17 | 558 | 2033-10-27 | sim | não | **sim** |
| XIPS-25 (87 kg) | 11 | 814 | 47 | 49,5 | 4 001 | 87 | 87 | 1 645 | 11 881 | 24,4 % | 0,67 | 25,2 | 2028-09-01 | 640 | 2030-06-03 | 239 | 2031-01-29 | 2032-04-26 | 2031-01-29 | 207 | 2032-04-17 | 558 | 2033-10-27 | sim | não | **sim** |
| XIPS-25 (87 kg) | 12 | 814 | 50 | 54,0 | 4 256 | 87 | 87 | 1 750 | 12 638 | 17,0 % | 0,67 | 25,0 | 2028-09-01 | 640 | 2030-06-03 | 233 | 2031-01-23 | 2032-04-26 | 2031-01-23 | 202 | 2032-04-17 | 559 | 2033-10-28 | sim | não | **sim** |
| NEXT-C | 1 | 814 | 2 | 7,3 | 885 | 885 | 918 | 98 | 2 975 | 384,2 % | 2,01 | 23,0 | 2028-09-01 | 955 | 2031-04-14 | 486 | 2032-08-12 | 2032-04-26 | 2032-08-12 | 424 | 2033-12-06 | 900 | 2036-05-24 | sim | não | não |
| NEXT-C | 2 | 814 | 3 | 14,7 | 1 163 | 582 | 918 | 147 | 3 833 | 285,8 % | 0,64 | 28,5 | 2028-09-17 | 546 | 2030-03-16 | 307 | 2031-01-17 | 2032-04-26 | 2031-01-17 | 270 | 2031-12-17 | 894 | 2034-05-29 | sim | não | **sim** |
| NEXT-C | 3 | 814 | 4 | 22,0 | 1 414 | 471 | 918 | 196 | 4 660 | 217,9 % | 0,54 | 28,5 | 2028-09-18 | 566 | 2030-04-06 | 248 | 2030-12-11 | 2032-04-26 | 2030-12-11 | 218 | 2031-12-31 | 876 | 2034-05-25 | sim | não | **sim** |
| NEXT-C | 4 | 814 | 5 | 29,3 | 2 782 | 695 | 918 | 245 | 6 827 | 117,0 % | 0,55 | 28,5 | 2028-09-18 | 550 | 2030-03-22 | 270 | 2030-12-17 | 2032-04-26 | 2030-12-17 | 240 | 2031-09-05 | 823 | 2033-12-05 | sim | não | **sim** |
| NEXT-C | 5 | 814 | 6 | 36,6 | 2 869 | 574 | 918 | 294 | 7 457 | 98,7 % | 0,52 | 28,5 | 2028-09-18 | 566 | 2030-04-07 | 238 | 2030-12-02 | 2032-04-26 | 2030-12-02 | 209 | 2031-07-22 | 847 | 2033-11-14 | sim | não | **sim** |
| NEXT-C | 6 | 814 | 7 | 44,0 | 3 184 | 531 | 918 | 343 | 8 361 | 77,2 % | 0,53 | 28,5 | 2028-09-18 | 585 | 2030-04-26 | 224 | 2030-12-06 | 2032-04-26 | 2030-12-06 | 196 | 2031-07-12 | 838 | 2033-10-27 | sim | não | **sim** |
| NEXT-C | 7 | 814 | 8 | 51,3 | 3 680 | 526 | 918 | 392 | 9 482 | 56,3 % | 0,51 | 28,5 | 2028-09-18 | 612 | 2030-05-23 | 220 | 2030-12-30 | 2032-04-26 | 2030-12-30 | 190 | 2031-07-31 | 816 | 2033-10-24 | sim | não | **sim** |

### Convergência

| Propulsor | Ativos | Encontro (km) | Δv ida (km/s) | Δv volta (km/s) | v infinito na Terra (km/s) | Mudança do orbitador na última iteração do fecho | Erro contínuo da ida (km; km/s) | Erro contínuo da volta (km; km/s) | Otimizador (ida; volta) | Nota |
| :- | -: | -: | -: | -: | -: | -: | :- | :- | :- | :- |
| XIPS-25 | 2 | 380 | 4,328 | 3,021 | 3,97 | 1,1e−02 | 11 369; 1,2e−03 | 629; 1,5e−04 | Optimization terminated successfully, 813 it.; Optimization terminated successfully, 981 it. | sem a restrição de prazo (com ela: NaoConverge) |
| XIPS-25 | 3 | 380 | 4,565 | 2,802 | 3,63 | 2,0e−01 | 6 695; 6,8e−04 | 341; 6,1e−05 | Optimization terminated successfully, 1699 it.; Optimization terminated successfully, 1936 it. | — |
| XIPS-25 | 4 | 380 | 4,832 | 2,438 | 4,24 | 1,3e−04 | 1 393; 1,5e−04 | 63; 1,2e−05 | Optimization terminated successfully, 439 it.; Optimization terminated successfully, 246 it. | — |
| XIPS-25 | 5 | 380 | 4,698 | 2,443 | 3,66 | 7,5e−07 | 916; 9,8e−05 | 244; 3,7e−05 | Optimization terminated successfully, 53 it.; Optimization terminated successfully, 117 it. | — |
| XIPS-25 | 6 | 380 | 4,716 | 2,436 | 3,73 | 1,3e−06 | 1 200; 1,3e−04 | 278; 4,2e−05 | Optimization terminated successfully, 70 it.; Optimization terminated successfully, 261 it. | sem a restrição de prazo (com ela: NaoConverge) |
| XIPS-25 | 7 | 380 | 4,744 | 2,432 | 3,76 | 2,5e−06 | 2 048; 2,1e−04 | 313; 4,8e−05 | Optimization terminated successfully, 449 it.; Optimization terminated successfully, 207 it. | — |
| XIPS-25 | 8 | 380 | 4,761 | 2,428 | 3,79 | 4,0e−07 | 2 154; 2,2e−04 | 349; 5,4e−05 | Optimization terminated successfully, 319 it.; Optimization terminated successfully, 1252 it. | — |
| XIPS-25 | 9 | 380 | 4,760 | 2,424 | 3,82 | 1,7e−07 | 2 476; 2,5e−04 | 375; 5,8e−05 | Optimization terminated successfully, 176 it.; Optimization terminated successfully, 223 it. | — |
| XIPS-25 | 10 | 380 | 4,772 | 2,422 | 3,84 | 1,1e−07 | 2 737; 2,8e−04 | 393; 6,1e−05 | Optimization terminated successfully, 170 it.; Optimization terminated successfully, 286 it. | — |
| XIPS-25 | 11 | 380 | 4,787 | 2,419 | 3,86 | 5,0e−08 | 2 779; 2,9e−04 | 418; 6,5e−05 | Optimization terminated successfully, 244 it.; Optimization terminated successfully, 210 it. | — |
| XIPS-25 | 12 | 380 | 4,790 | 2,417 | 3,88 | 1,3e−05 | 2 798; 2,9e−04 | 442; 6,9e−05 | Optimization terminated successfully, 477 it.; Optimization terminated successfully, 1395 it. | sem a restrição de prazo (com ela: NaoConverge) |
| XIPS-25 (87 kg) | 3 | 380 | 4,374 | 3,615 | 3,91 | 1,6e−05 | 2 643; 3,1e−04 | 8 154; 1,6e−03 | Optimization terminated successfully, 197 it.; Optimization terminated successfully, 276 it. | — |
| XIPS-25 (87 kg) | 4 | 380 | 4,639 | 3,465 | 4,23 | 1,4e−02 | 7 989; 8,1e−04 | 8 777; 1,8e−03 | Optimization terminated successfully, 2389 it.; Optimization terminated successfully, 1722 it. | — |
| XIPS-25 (87 kg) | 5 | 380 | 4,861 | 3,373 | 4,47 | 1,5e−03 | 14 452; 1,5e−03 | 8 256; 1,7e−03 | Optimization terminated successfully, 283 it.; Optimization terminated successfully, 2213 it. | sem a restrição de prazo (com ela: NaoConverge) |
| XIPS-25 (87 kg) | 11 | 380 | 4,847 | 6,076 | 2,57 | 1,5e−01 | 6 067; 6,2e−04 | 17 357; 3,4e−03 | Optimization terminated successfully, 2352 it.; Optimization terminated successfully, 270 it. | — |
| XIPS-25 (87 kg) | 12 | 380 | 4,841 | 5,064 | 4,55 | 1,5e−05 | 2 708; 2,9e−04 | 9 278; 2,0e−03 | Optimization terminated successfully, 944 it.; Optimization terminated successfully, 627 it. | sem a restrição de prazo (com ela: NaoConverge); segunda passada, a partir de n = 11 |
| NEXT-C | 1 | 380 | 4,249 | 3,671 | 3,65 | 1,1e−03 | 10 693; 1,1e−03 | 7 319; 1,4e−03 | Optimization terminated successfully, 953 it.; Optimization terminated successfully, 296 it. | sem a restrição de prazo (com ela: NaoConverge) |
| NEXT-C | 3 | 380 | 4,944 | 2,432 | 4,45 | 7,0e−07 | 1 826; 2,0e−04 | 103; 1,8e−05 | Optimization terminated successfully, 390 it.; Optimization terminated successfully, 249 it. | — |
| NEXT-C | 4 | 380 | 4,957 | 2,432 | 3,76 | 1,5e−06 | 2 042; 2,2e−04 | 334; 5,1e−05 | Optimization terminated successfully, 308 it.; Optimization terminated successfully, 186 it. | — |
| NEXT-C | 5 | 380 | 4,872 | 2,426 | 3,81 | 8,0e−08 | 1 922; 2,0e−04 | 374; 5,8e−05 | Optimization terminated successfully, 300 it.; Optimization terminated successfully, 1428 it. | — |
| NEXT-C | 6 | 380 | 4,891 | 2,421 | 3,85 | 1,1e−06 | 2 603; 2,7e−04 | 413; 6,4e−05 | Optimization terminated successfully, 1045 it.; Optimization terminated successfully, 142 it. | — |
| NEXT-C | 7 | 380 | 4,911 | 2,417 | 3,88 | 3,4e−04 | 2 967; 3,1e−04 | 449; 7,0e−05 | Optimization terminated successfully, 679 it.; Optimization terminated successfully, 411 it. | — |
| XIPS-25 | 3 | 814 | 4,469 | 2,799 | 3,70 | 3,2e−01 | 6 829; 7,0e−04 | 426; 7,7e−05 | Optimization terminated successfully, 614 it.; Optimization terminated successfully, 1132 it. | — |
| XIPS-25 | 4 | 814 | 4,839 | 2,439 | 4,25 | 1,6e−07 | 1 405; 1,5e−04 | 83; 1,5e−05 | Optimization terminated successfully, 82 it.; Optimization terminated successfully, 1191 it. | — |
| XIPS-25 | 5 | 814 | 4,699 | 2,441 | 3,68 | 7,0e−08 | 773; 8,3e−05 | 284; 4,4e−05 | Optimization terminated successfully, 32 it.; Optimization terminated successfully, 322 it. | — |
| XIPS-25 | 6 | 814 | 4,732 | 2,436 | 3,73 | 1,4e−07 | 896; 9,6e−05 | 302; 4,6e−05 | Optimization terminated successfully, 29 it.; Optimization terminated successfully, 380 it. | — |
| XIPS-25 | 7 | 814 | 4,750 | 2,431 | 3,77 | 3,7e−07 | 977; 1,0e−04 | 325; 5,0e−05 | Optimization terminated successfully, 80 it.; Optimization terminated successfully, 229 it. | — |
| XIPS-25 | 8 | 814 | 4,774 | 2,427 | 3,80 | 5,5e−06 | 990; 1,1e−04 | 351; 5,4e−05 | Optimization terminated successfully, 210 it.; Optimization terminated successfully, 262 it. | — |
| XIPS-25 | 9 | 814 | 4,762 | 2,424 | 3,82 | 1,5e−07 | 1 200; 1,3e−04 | 370; 5,7e−05 | Optimization terminated successfully, 434 it.; Optimization terminated successfully, 1645 it. | — |
| XIPS-25 | 10 | 814 | 4,778 | 2,421 | 3,85 | 2,8e−06 | 1 529; 1,6e−04 | 395; 6,1e−05 | Optimization terminated successfully, 411 it.; Optimization terminated successfully, 227 it. | — |
| XIPS-25 | 11 | 814 | 4,777 | 2,418 | 3,87 | 8,7e−07 | 2 202; 2,3e−04 | 421; 6,5e−05 | Optimization terminated successfully, 510 it.; Optimization terminated successfully, 232 it. | — |
| XIPS-25 | 12 | 814 | 4,794 | 2,416 | 3,89 | 1,4e−05 | 2 623; 2,7e−04 | 442; 6,9e−05 | Optimization terminated successfully, 298 it.; Optimization terminated successfully, 489 it. | — |
| XIPS-25 (87 kg) | 5 | 814 | 4,880 | 2,443 | 4,08 | 5,1e−08 | 1 641; 1,8e−04 | 30; 5,7e−06 | Optimization terminated successfully, 25 it.; Optimization terminated successfully, 122 it. | — |
| XIPS-25 (87 kg) | 6 | 814 | 4,888 | 2,438 | 4,21 | 2,9e−08 | 1 816; 2,0e−04 | 32; 5,9e−06 | Optimization terminated successfully, 34 it.; Optimization terminated successfully, 146 it. | — |
| XIPS-25 (87 kg) | 7 | 814 | 4,899 | 2,434 | 4,33 | 4,5e−07 | 2 006; 2,2e−04 | 34; 6,2e−06 | Optimization terminated successfully, 204 it.; Optimization terminated successfully, 156 it. | — |
| XIPS-25 (87 kg) | 8 | 814 | 4,879 | 2,432 | 4,38 | 1,7e−08 | 2 186; 2,5e−04 | 35; 6,3e−06 | Optimization terminated successfully, 309 it.; Optimization terminated successfully, 123 it. | — |
| XIPS-25 (87 kg) | 9 | 814 | 4,884 | 2,431 | 4,42 | 1,5e−07 | 2 293; 2,6e−04 | 36; 6,4e−06 | Optimization terminated successfully, 413 it.; Optimization terminated successfully, 80 it. | — |
| XIPS-25 (87 kg) | 10 | 814 | 4,888 | 2,430 | 4,45 | 5,8e−08 | 2 472; 2,8e−04 | 37; 6,6e−06 | Optimization terminated successfully, 103 it.; Optimization terminated successfully, 125 it. | — |
| XIPS-25 (87 kg) | 11 | 814 | 4,885 | 2,429 | 4,49 | 4,5e−06 | 2 551; 2,9e−04 | 38; 6,7e−06 | Optimization terminated successfully, 557 it.; Optimization terminated successfully, 285 it. | — |
| XIPS-25 (87 kg) | 12 | 814 | 4,886 | 2,428 | 4,52 | 1,6e−05 | 2 594; 2,9e−04 | 39; 6,9e−06 | Optimization terminated successfully, 222 it.; Optimization terminated successfully, 175 it. | — |
| NEXT-C | 1 | 814 | 4,379 | 2,917 | 4,02 | 2,0e−03 | 11 808; 1,2e−03 | 2 340; 4,0e−04 | Optimization terminated successfully, 593 it.; Optimization terminated successfully, 298 it. | sem a restrição de prazo (com ela: NaoConverge) |
| NEXT-C | 2 | 814 | 4,914 | 2,825 | 3,18 | 1,1e−04 | 1 276; 1,4e−04 | 546; 1,0e−04 | Optimization terminated successfully, 226 it.; Optimization terminated successfully, 360 it. | — |
| NEXT-C | 3 | 814 | 4,946 | 2,791 | 3,20 | 1,0e−04 | 1 801; 1,9e−04 | 1 065; 1,9e−04 | Optimization terminated successfully, 268 it.; Optimization terminated successfully, 217 it. | — |
| NEXT-C | 4 | 814 | 4,950 | 9,305 | 3,81 | 1,2e−02 | 1 510; 1,6e−04 | 11 641; 2,3e−03 | Optimization terminated successfully, 574 it.; Optimization terminated successfully, 2395 it. | — |
| NEXT-C | 5 | 814 | 4,958 | 7,669 | 2,25 | 2,8e−04 | 1 845; 2,0e−04 | 17 605; 3,4e−03 | Optimization terminated successfully, 504 it.; Optimization terminated successfully, 571 it. | — |
| NEXT-C | 6 | 814 | 4,946 | 7,316 | 1,92 | 3,3e−03 | 2 193; 2,4e−04 | 20 537; 3,9e−03 | Optimization terminated successfully, 475 it.; Optimization terminated successfully, 743 it. | — |
| NEXT-C | 7 | 814 | 4,961 | 7,427 | 2,24 | 1,7e−02 | 2 545; 2,8e−04 | 19 178; 3,6e−03 | Optimization terminated successfully, 2229 it.; Optimization terminated successfully, 1090 it. | — |

## Estocagem do MAV na superfície

Pouso do lander em 2029-09-20 (Ls 189,5°). Aquecimento de results/familia1/mavs.yaml (modelo da P-027); RHU com a potência do ano do lançamento do MAV ([F155] p. 1: 0,90 W em 2014, menos 0,01 W por ano). Teto oferecido ao New Frontiers: 43 RHUs ([F155] p. 2).
Temporadas de tempestade global (Ls 180° a 340°, P-124) tocadas entre o pouso e o lançamento do MAV; na missão de referência (MAV no lançamento mais cedo, 2029-11-03): 1.
Envelhecimento do propelente sólido: só há resultado publicado da fase de vácuo ([F263] PDF p. 1, perda de massa abaixo de 0,1 %); a fase de um ano em condições de superfície de Marte estava planejada ([F263] PDF p. 1) e não há resultado publicado achado; o projeto do MSR previa cerca de um ano na superfície ([F35] PDF p. 1).

| Propulsor | Ativos | Encontro (km) | Lançamento do MAV | Dias na superfície | Ls no lançamento (°) | Temporadas de tempestade | MAV | Temperatura mantida (°C) | Aquecimento (W) | Energia (kWh) | RHUs |
| :- | -: | -: | :- | -: | -: | -: | :- | -: | -: | -: | -: |
| XIPS-25 | 2 | 380 | 2032-09-17 | 1093 | 54,6 | 2 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 491 | 26 |
| XIPS-25 | 2 | 380 | 2032-09-17 | 1093 | 54,6 | 2 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 1 773 | 94 |
| XIPS-25 | 2 | 380 | 2032-09-17 | 1093 | 54,6 | 2 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 853 | 46 |
| XIPS-25 | 2 | 380 | 2032-09-17 | 1093 | 54,6 | 2 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 703 | 38 |
| XIPS-25 | 3 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 471 | 26 |
| XIPS-25 | 3 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 1 700 | 94 |
| XIPS-25 | 3 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 818 | 46 |
| XIPS-25 | 3 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 674 | 38 |
| XIPS-25 | 4 | 380 | 2031-02-18 | 516 | 103,0 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 232 | 26 |
| XIPS-25 | 4 | 380 | 2031-02-18 | 516 | 103,0 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 837 | 93 |
| XIPS-25 | 4 | 380 | 2031-02-18 | 516 | 103,0 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 403 | 45 |
| XIPS-25 | 4 | 380 | 2031-02-18 | 516 | 103,0 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 332 | 37 |
| XIPS-25 | 5 | 380 | 2030-11-24 | 430 | 65,1 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 193 | 26 |
| XIPS-25 | 5 | 380 | 2030-11-24 | 430 | 65,1 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 698 | 92 |
| XIPS-25 | 5 | 380 | 2030-11-24 | 430 | 65,1 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 336 | 44 |
| XIPS-25 | 5 | 380 | 2030-11-24 | 430 | 65,1 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 277 | 37 |
| XIPS-25 | 6 | 380 | 2030-11-24 | 430 | 65,1 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 193 | 26 |
| XIPS-25 | 6 | 380 | 2030-11-24 | 430 | 65,1 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 698 | 92 |
| XIPS-25 | 6 | 380 | 2030-11-24 | 430 | 65,1 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 336 | 44 |
| XIPS-25 | 6 | 380 | 2030-11-24 | 430 | 65,1 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 277 | 37 |
| XIPS-25 | 7 | 380 | 2031-01-05 | 472 | 83,5 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 212 | 26 |
| XIPS-25 | 7 | 380 | 2031-01-05 | 472 | 83,5 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 766 | 93 |
| XIPS-25 | 7 | 380 | 2031-01-05 | 472 | 83,5 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 368 | 45 |
| XIPS-25 | 7 | 380 | 2031-01-05 | 472 | 83,5 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 304 | 37 |
| XIPS-25 | 8 | 380 | 2030-12-24 | 460 | 78,2 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 207 | 26 |
| XIPS-25 | 8 | 380 | 2030-12-24 | 460 | 78,2 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 746 | 92 |
| XIPS-25 | 8 | 380 | 2030-12-24 | 460 | 78,2 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 359 | 44 |
| XIPS-25 | 8 | 380 | 2030-12-24 | 460 | 78,2 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 296 | 37 |
| XIPS-25 | 9 | 380 | 2030-12-31 | 467 | 81,3 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 210 | 26 |
| XIPS-25 | 9 | 380 | 2030-12-31 | 467 | 81,3 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 758 | 92 |
| XIPS-25 | 9 | 380 | 2030-12-31 | 467 | 81,3 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 365 | 44 |
| XIPS-25 | 9 | 380 | 2030-12-31 | 467 | 81,3 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 300 | 37 |
| XIPS-25 | 10 | 380 | 2031-01-06 | 473 | 83,9 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 212 | 26 |
| XIPS-25 | 10 | 380 | 2031-01-06 | 473 | 83,9 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 767 | 93 |
| XIPS-25 | 10 | 380 | 2031-01-06 | 473 | 83,9 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 369 | 45 |
| XIPS-25 | 10 | 380 | 2031-01-06 | 473 | 83,9 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 304 | 37 |
| XIPS-25 | 11 | 380 | 2030-12-30 | 466 | 80,9 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 209 | 26 |
| XIPS-25 | 11 | 380 | 2030-12-30 | 466 | 80,9 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 756 | 92 |
| XIPS-25 | 11 | 380 | 2030-12-30 | 466 | 80,9 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 364 | 44 |
| XIPS-25 | 11 | 380 | 2030-12-30 | 466 | 80,9 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 300 | 37 |
| XIPS-25 | 12 | 380 | 2030-12-25 | 461 | 78,7 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 207 | 26 |
| XIPS-25 | 12 | 380 | 2030-12-25 | 461 | 78,7 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 748 | 92 |
| XIPS-25 | 12 | 380 | 2030-12-25 | 461 | 78,7 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 360 | 44 |
| XIPS-25 | 12 | 380 | 2030-12-25 | 461 | 78,7 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 297 | 37 |
| XIPS-25 (87 kg) | 3 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 471 | 26 |
| XIPS-25 (87 kg) | 3 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 1 700 | 94 |
| XIPS-25 (87 kg) | 3 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 818 | 46 |
| XIPS-25 (87 kg) | 3 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 674 | 38 |
| XIPS-25 (87 kg) | 4 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 471 | 26 |
| XIPS-25 (87 kg) | 4 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 1 700 | 94 |
| XIPS-25 (87 kg) | 4 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 818 | 46 |
| XIPS-25 (87 kg) | 4 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 674 | 38 |
| XIPS-25 (87 kg) | 5 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 471 | 26 |
| XIPS-25 (87 kg) | 5 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 1 700 | 94 |
| XIPS-25 (87 kg) | 5 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 818 | 46 |
| XIPS-25 (87 kg) | 5 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 674 | 38 |
| XIPS-25 (87 kg) | 11 | 380 | 2032-01-23 | 855 | 293,5 | 2 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 384 | 26 |
| XIPS-25 (87 kg) | 11 | 380 | 2032-01-23 | 855 | 293,5 | 2 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 1 387 | 94 |
| XIPS-25 (87 kg) | 11 | 380 | 2032-01-23 | 855 | 293,5 | 2 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 667 | 46 |
| XIPS-25 (87 kg) | 11 | 380 | 2032-01-23 | 855 | 293,5 | 2 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 550 | 38 |
| XIPS-25 (87 kg) | 12 | 380 | 2031-09-30 | 740 | 221,3 | 2 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 332 | 26 |
| XIPS-25 (87 kg) | 12 | 380 | 2031-09-30 | 740 | 221,3 | 2 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 1 201 | 93 |
| XIPS-25 (87 kg) | 12 | 380 | 2031-09-30 | 740 | 221,3 | 2 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 578 | 45 |
| XIPS-25 (87 kg) | 12 | 380 | 2031-09-30 | 740 | 221,3 | 2 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 476 | 37 |
| NEXT-C | 1 | 380 | 2032-10-24 | 1130 | 70,8 | 2 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 507 | 26 |
| NEXT-C | 1 | 380 | 2032-10-24 | 1130 | 70,8 | 2 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 1 833 | 94 |
| NEXT-C | 1 | 380 | 2032-10-24 | 1130 | 70,8 | 2 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 882 | 46 |
| NEXT-C | 1 | 380 | 2032-10-24 | 1130 | 70,8 | 2 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 727 | 38 |
| NEXT-C | 3 | 380 | 2031-01-02 | 469 | 82,2 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 211 | 26 |
| NEXT-C | 3 | 380 | 2031-01-02 | 469 | 82,2 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 761 | 93 |
| NEXT-C | 3 | 380 | 2031-01-02 | 469 | 82,2 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 366 | 45 |
| NEXT-C | 3 | 380 | 2031-01-02 | 469 | 82,2 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 302 | 37 |
| NEXT-C | 4 | 380 | 2030-12-07 | 443 | 70,8 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 199 | 26 |
| NEXT-C | 4 | 380 | 2030-12-07 | 443 | 70,8 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 719 | 92 |
| NEXT-C | 4 | 380 | 2030-12-07 | 443 | 70,8 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 346 | 44 |
| NEXT-C | 4 | 380 | 2030-12-07 | 443 | 70,8 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 285 | 37 |
| NEXT-C | 5 | 380 | 2030-11-06 | 412 | 57,2 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 185 | 26 |
| NEXT-C | 5 | 380 | 2030-11-06 | 412 | 57,2 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 668 | 92 |
| NEXT-C | 5 | 380 | 2030-11-06 | 412 | 57,2 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 322 | 44 |
| NEXT-C | 5 | 380 | 2030-11-06 | 412 | 57,2 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 265 | 37 |
| NEXT-C | 6 | 380 | 2030-12-05 | 441 | 69,9 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 198 | 26 |
| NEXT-C | 6 | 380 | 2030-12-05 | 441 | 69,9 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 715 | 92 |
| NEXT-C | 6 | 380 | 2030-12-05 | 441 | 69,9 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 344 | 44 |
| NEXT-C | 6 | 380 | 2030-12-05 | 441 | 69,9 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 284 | 37 |
| NEXT-C | 7 | 380 | 2030-12-11 | 447 | 72,6 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 201 | 26 |
| NEXT-C | 7 | 380 | 2030-12-11 | 447 | 72,6 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 725 | 92 |
| NEXT-C | 7 | 380 | 2030-12-11 | 447 | 72,6 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 349 | 44 |
| NEXT-C | 7 | 380 | 2030-12-11 | 447 | 72,6 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 288 | 37 |
| XIPS-25 | 3 | 814 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 884 | 49 |
| XIPS-25 | 3 | 814 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 722 | 40 |
| XIPS-25 | 4 | 814 | 2031-01-21 | 488 | 90,5 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 412 | 49 |
| XIPS-25 | 4 | 814 | 2031-01-21 | 488 | 90,5 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 336 | 40 |
| XIPS-25 | 5 | 814 | 2030-10-12 | 387 | 46,2 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 327 | 48 |
| XIPS-25 | 5 | 814 | 2030-10-12 | 387 | 46,2 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 267 | 39 |
| XIPS-25 | 6 | 814 | 2030-09-25 | 370 | 38,6 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 312 | 48 |
| XIPS-25 | 6 | 814 | 2030-09-25 | 370 | 38,6 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 255 | 39 |
| XIPS-25 | 7 | 814 | 2030-09-09 | 354 | 31,3 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 299 | 48 |
| XIPS-25 | 7 | 814 | 2030-09-09 | 354 | 31,3 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 244 | 39 |
| XIPS-25 | 8 | 814 | 2030-08-25 | 339 | 24,4 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 286 | 48 |
| XIPS-25 | 8 | 814 | 2030-08-25 | 339 | 24,4 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 234 | 39 |
| XIPS-25 | 9 | 814 | 2030-09-04 | 349 | 29,0 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 295 | 48 |
| XIPS-25 | 9 | 814 | 2030-09-04 | 349 | 29,0 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 240 | 39 |
| XIPS-25 | 10 | 814 | 2030-09-20 | 365 | 36,3 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 308 | 48 |
| XIPS-25 | 10 | 814 | 2030-09-20 | 365 | 36,3 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 251 | 39 |
| XIPS-25 | 11 | 814 | 2030-10-31 | 406 | 54,6 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 343 | 48 |
| XIPS-25 | 11 | 814 | 2030-10-31 | 406 | 54,6 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 280 | 39 |
| XIPS-25 | 12 | 814 | 2030-11-22 | 428 | 64,3 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 361 | 48 |
| XIPS-25 | 12 | 814 | 2030-11-22 | 428 | 64,3 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 295 | 39 |
| XIPS-25 (87 kg) | 5 | 814 | 2031-03-27 | 553 | 119,9 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 467 | 49 |
| XIPS-25 (87 kg) | 5 | 814 | 2031-03-27 | 553 | 119,9 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 381 | 40 |
| XIPS-25 (87 kg) | 6 | 814 | 2031-03-06 | 532 | 110,2 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 449 | 49 |
| XIPS-25 (87 kg) | 6 | 814 | 2031-03-06 | 532 | 110,2 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 366 | 40 |
| XIPS-25 (87 kg) | 7 | 814 | 2031-02-21 | 519 | 104,3 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 438 | 49 |
| XIPS-25 (87 kg) | 7 | 814 | 2031-02-21 | 519 | 104,3 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 358 | 40 |
| XIPS-25 (87 kg) | 8 | 814 | 2031-02-15 | 513 | 101,6 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 433 | 49 |
| XIPS-25 (87 kg) | 8 | 814 | 2031-02-15 | 513 | 101,6 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 353 | 40 |
| XIPS-25 (87 kg) | 9 | 814 | 2031-02-07 | 505 | 98,1 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 426 | 49 |
| XIPS-25 (87 kg) | 9 | 814 | 2031-02-07 | 505 | 98,1 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 348 | 40 |
| XIPS-25 (87 kg) | 10 | 814 | 2031-02-05 | 503 | 97,2 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 424 | 49 |
| XIPS-25 (87 kg) | 10 | 814 | 2031-02-05 | 503 | 97,2 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 347 | 40 |
| XIPS-25 (87 kg) | 11 | 814 | 2031-01-29 | 496 | 94,1 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 419 | 49 |
| XIPS-25 (87 kg) | 11 | 814 | 2031-01-29 | 496 | 94,1 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 342 | 40 |
| XIPS-25 (87 kg) | 12 | 814 | 2031-01-23 | 490 | 91,4 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 413 | 49 |
| XIPS-25 (87 kg) | 12 | 814 | 2031-01-23 | 490 | 91,4 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 338 | 40 |
| NEXT-C | 1 | 814 | 2032-08-12 | 1057 | 38,6 | 2 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 892 | 49 |
| NEXT-C | 1 | 814 | 2032-08-12 | 1057 | 38,6 | 2 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 728 | 40 |
| NEXT-C | 2 | 814 | 2031-01-17 | 484 | 88,8 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 408 | 49 |
| NEXT-C | 2 | 814 | 2031-01-17 | 484 | 88,8 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 333 | 40 |
| NEXT-C | 3 | 814 | 2030-12-11 | 447 | 72,6 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 377 | 48 |
| NEXT-C | 3 | 814 | 2030-12-11 | 447 | 72,6 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 308 | 39 |
| NEXT-C | 4 | 814 | 2030-12-17 | 453 | 75,2 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 382 | 48 |
| NEXT-C | 4 | 814 | 2030-12-17 | 453 | 75,2 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 312 | 39 |
| NEXT-C | 5 | 814 | 2030-12-02 | 438 | 68,6 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 370 | 48 |
| NEXT-C | 5 | 814 | 2030-12-02 | 438 | 68,6 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 302 | 39 |
| NEXT-C | 6 | 814 | 2030-12-06 | 442 | 70,4 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 373 | 48 |
| NEXT-C | 6 | 814 | 2030-12-06 | 442 | 70,4 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 304 | 39 |
| NEXT-C | 7 | 814 | 2030-12-30 | 466 | 80,9 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 393 | 48 |
| NEXT-C | 7 | 814 | 2030-12-30 | 466 | 80,9 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 321 | 39 |
