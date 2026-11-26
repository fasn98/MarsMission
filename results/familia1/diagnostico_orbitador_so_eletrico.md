# Diagnóstico do orbitador só elétrico da família 1 (gerado por tools/orbitador_so_eletrico.py)

Fora da comparação do CI (regra 6): soluções de otimização (mínimos locais), verificadas sem reotimizar. Calculado, NÃO validado.

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

## (a) e (c) Família 1: a melhor solução verificada de cada configuração

| Propulsor | Ativos | Encontro (km) | Instalados | Potência (kW) | Xe (kg) | Xe por propulsor (kg) | Vida (kg) | Propulsores + PPU (kg) | Orbitador (kg) | Margem no Falcon Heavy | C3 (km²/s²) | DLA (°) | Partida da Terra | Ida (d) | Chegada a Marte | Descida (d) | Pronto no encontro | Último lançamento do MAV | Lançamento do MAV | Subida (d) | Partida de Marte | Volta (d) | Chegada à Terra | Descida cruza conjunção | Encontro e subida cruzam conjunção | Fecha? |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- | -: | :- | :- | :- | -: | :- | -: | :- | :- | :- | :- |
| XIPS-25 | 1 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 | 2 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 | 3 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 | 4 | 380 | 13 | 18,0 | 1 851 | 154 | 158 | 455 | 5 397 | 173,4 % | 0,76 | 28,5 | 2028-09-18 | 562 | 2030-04-02 | 322 | 2031-02-18 | 2032-04-26 | 2031-02-18 | 278 | 2032-01-07 | 656 | 2033-10-24 | sim | não | **sim** |
| XIPS-25 | 5 | 380 | 14 | 22,5 | 2 019 | 155 | 158 | 490 | 5 933 | 147,5 % | 1,02 | 28,5 | 2028-10-14 | 472 | 2030-01-28 | 284 | 2030-11-09 | 2032-04-26 | 2030-11-09 | 246 | 2031-09-12 | 729 | 2033-09-10 | sim | não | **sim** |
| XIPS-25 | 6 | 380 | 16 | 27,0 | 2 248 | 150 | 158 | 560 | 6 600 | 122,7 % | 0,96 | 28,5 | 2028-10-14 | 507 | 2030-03-05 | 263 | 2030-11-24 | 2032-04-26 | 2030-11-24 | 227 | 2031-10-03 | 707 | 2033-09-09 | sim | não | **sim** |
| XIPS-25 | 7 | 380 | 17 | 31,5 | 2 446 | 153 | 158 | 595 | 7 171 | 105,2 % | 0,89 | 28,5 | 2028-10-14 | 521 | 2030-03-20 | 245 | 2030-11-21 | 2032-04-26 | 2030-11-21 | 212 | 2031-09-11 | 728 | 2033-09-08 | sim | não | **sim** |
| XIPS-25 | 8 | 380 | 18 | 36,0 | 2 638 | 155 | 158 | 630 | 7 735 | 90,3 % | 0,88 | 28,5 | 2028-10-15 | 529 | 2030-03-27 | 231 | 2030-11-14 | 2032-04-26 | 2030-11-14 | 200 | 2031-09-10 | 728 | 2033-09-07 | sim | não | **sim** |
| XIPS-25 | 9 | 380 | 19 | 40,5 | 2 834 | 157 | 158 | 665 | 8 303 | 77,4 % | 0,85 | 28,5 | 2028-10-15 | 586 | 2030-05-24 | 221 | 2030-12-31 | 2032-04-26 | 2030-12-31 | 191 | 2031-09-10 | 728 | 2033-09-07 | sim | não | **sim** |
| XIPS-25 | 10 | 380 | 21 | 45,0 | 3 064 | 153 | 158 | 735 | 8 972 | 64,3 % | 0,81 | 28,5 | 2028-10-15 | 530 | 2030-03-29 | 214 | 2030-10-30 | 2032-04-26 | 2030-10-30 | 185 | 2031-09-10 | 727 | 2033-09-06 | sim | não | **sim** |
| XIPS-25 | 11 | 380 | 22 | 49,5 | 3 255 | 155 | 158 | 770 | 9 535 | 54,6 % | 0,81 | 28,5 | 2028-10-15 | 548 | 2030-04-16 | 207 | 2030-11-10 | 2032-04-26 | 2030-11-10 | 179 | 2031-09-10 | 727 | 2033-09-06 | sim | não | **sim** |
| XIPS-25 | 12 | 380 | 23 | 54,0 | 3 450 | 157 | 158 | 805 | 10 102 | 46,0 % | 0,80 | 28,5 | 2028-10-16 | 559 | 2030-04-28 | 201 | 2030-11-16 | 2032-04-26 | 2030-11-16 | 174 | 2031-09-09 | 727 | 2033-09-05 | sim | não | **sim** |
| XIPS-25 (87 kg) | 1 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 2 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 3 | 380 | 29 | 13,5 | 2 390 | 85 | 87 | 1 015 | 6 709 | 112,8 % | 2,46 | 24,0 | 2028-09-01 | 792 | 2030-11-01 | 541 | 2032-04-26 | 2032-04-26 | 2032-08-03 | 467 | 2034-04-16 | 900 | 2036-10-02 | não | não | **sim** |
| XIPS-25 (87 kg) | 4 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 5 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 6 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 7 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 8 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 9 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 10 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 11 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 12 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| NEXT-C | 1 | 380 | 3 | 7,3 | 1 000 | 500 | 918 | 147 | 3 200 | 346,6 % | 2,42 | 22,7 | 2028-09-01 | 953 | 2031-04-11 | 561 | 2032-10-24 | 2032-04-26 | 2032-10-24 | 491 | 2034-04-13 | 900 | 2036-09-29 | sim | não | não |
| NEXT-C | 2 | 380 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| NEXT-C | 3 | 380 | 4 | 22,0 | 1 420 | 473 | 918 | 196 | 4 676 | 216,8 % | 0,55 | 28,5 | 2028-09-18 | 568 | 2030-04-08 | 268 | 2031-01-02 | 2032-04-26 | 2031-01-02 | 235 | 2031-11-06 | 721 | 2033-10-27 | sim | não | **sim** |
| NEXT-C | 4 | 380 | 5 | 29,3 | 1 673 | 418 | 918 | 245 | 5 505 | 169,3 % | 0,51 | 28,5 | 2028-09-18 | 573 | 2030-04-14 | 237 | 2030-12-07 | 2032-04-26 | 2030-12-07 | 207 | 2031-09-11 | 728 | 2033-09-08 | sim | não | **sim** |
| NEXT-C | 5 | 380 | 6 | 36,6 | 1 908 | 382 | 918 | 294 | 6 313 | 134,1 % | 0,67 | 28,5 | 2028-10-14 | 535 | 2030-04-02 | 218 | 2030-11-06 | 2032-04-26 | 2030-11-06 | 191 | 2031-09-10 | 728 | 2033-09-07 | sim | não | **sim** |
| NEXT-C | 6 | 380 | 7 | 44,0 | 2 160 | 360 | 918 | 343 | 7 141 | 107,1 % | 0,63 | 28,5 | 2028-10-14 | 576 | 2030-05-13 | 205 | 2030-12-05 | 2032-04-26 | 2030-12-05 | 180 | 2031-09-10 | 727 | 2033-09-06 | sim | não | **sim** |
| NEXT-C | 7 | 380 | 8 | 51,3 | 2 413 | 345 | 918 | 392 | 7 970 | 85,7 % | 0,59 | 28,5 | 2028-10-15 | 590 | 2030-05-28 | 196 | 2030-12-11 | 2032-04-26 | 2030-12-11 | 172 | 2031-09-09 | 727 | 2033-09-05 | sim | não | **sim** |
| XIPS-25 | 1 | 814 | 8 | 4,5 | 1 087 | 155 | 158 | 280 | 3 360 | 304,3 % | 4,96 | 22,3 | 2028-09-01 | 1 032 | 2031-06-29 | 775 | 2033-08-12 | 2032-04-26 | 2033-08-12 | 672 | 2035-12-20 | 900 | 2038-06-07 | sim | sim | não |
| XIPS-25 | 2 | 814 | 10 | 9,0 | 1 372 | 152 | 158 | 350 | 4 090 | 253,4 % | 1,84 | 23,7 | 2028-09-01 | 952 | 2031-04-11 | 460 | 2032-07-14 | 2032-04-26 | 2032-08-03 | 398 | 2033-12-08 | 900 | 2036-05-26 | sim | não | não |
| XIPS-25 | 3 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 | 4 | 814 | 13 | 18,0 | 1 782 | 148 | 158 | 455 | 5 304 | 178,2 % | 0,75 | 28,5 | 2028-09-18 | 563 | 2030-04-04 | 294 | 2031-01-24 | 2032-04-26 | 2031-01-24 | 255 | 2031-11-14 | 710 | 2033-10-24 | sim | não | **sim** |
| XIPS-25 | 5 | 814 | 14 | 22,5 | 1 943 | 149 | 158 | 490 | 5 833 | 151,8 % | 1,01 | 28,5 | 2028-10-14 | 473 | 2030-01-29 | 260 | 2030-10-16 | 2032-04-26 | 2030-10-16 | 225 | 2031-09-15 | 726 | 2033-09-10 | sim | não | **sim** |
| XIPS-25 | 6 | 814 | 15 | 27,0 | 2 134 | 152 | 158 | 525 | 6 396 | 130,0 % | 0,92 | 28,5 | 2028-10-14 | 473 | 2030-01-30 | 237 | 2030-09-25 | 2032-04-26 | 2030-09-25 | 206 | 2031-09-14 | 725 | 2033-09-09 | sim | não | **sim** |
| XIPS-25 | 7 | 814 | 16 | 31,5 | 2 323 | 155 | 158 | 560 | 6 956 | 111,7 % | 0,87 | 28,5 | 2028-10-15 | 473 | 2030-01-31 | 221 | 2030-09-09 | 2032-04-26 | 2030-09-09 | 192 | 2031-09-14 | 725 | 2033-09-08 | sim | não | **sim** |
| XIPS-25 | 8 | 814 | 17 | 36,0 | 2 514 | 157 | 158 | 595 | 7 519 | 96,0 % | 0,82 | 28,5 | 2028-10-15 | 469 | 2030-01-28 | 209 | 2030-08-25 | 2032-04-26 | 2030-08-25 | 181 | 2031-09-13 | 725 | 2033-09-07 | sim | não | **sim** |
| XIPS-25 | 9 | 814 | 19 | 40,5 | 2 729 | 152 | 158 | 665 | 8 170 | 80,4 % | 0,83 | 28,5 | 2028-10-15 | 487 | 2030-02-14 | 202 | 2030-09-04 | 2032-04-26 | 2030-09-04 | 175 | 2031-09-13 | 724 | 2033-09-07 | sim | não | **sim** |
| XIPS-25 | 10 | 814 | 20 | 45,0 | 2 919 | 154 | 158 | 700 | 8 731 | 68,9 % | 0,80 | 28,5 | 2028-10-15 | 511 | 2030-03-10 | 194 | 2030-09-20 | 2032-04-26 | 2030-09-20 | 168 | 2031-09-13 | 724 | 2033-09-06 | sim | não | **sim** |
| XIPS-25 | 11 | 814 | 21 | 49,5 | 3 104 | 155 | 158 | 735 | 9 287 | 58,8 % | 0,80 | 28,5 | 2028-10-16 | 557 | 2030-04-26 | 188 | 2030-10-31 | 2032-04-26 | 2030-10-31 | 163 | 2031-09-13 | 724 | 2033-09-06 | sim | não | **sim** |
| XIPS-25 | 12 | 814 | 22 | 54,0 | 3 294 | 157 | 158 | 770 | 9 849 | 49,8 % | 0,78 | 28,5 | 2028-10-16 | 600 | 2030-06-08 | 182 | 2030-12-08 | 2032-04-26 | 2030-12-08 | 158 | 2031-09-12 | 724 | 2033-09-05 | sim | não | **sim** |
| XIPS-25 (87 kg) | 1 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 2 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 3 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 4 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| XIPS-25 (87 kg) | 5 | 814 | 30 | 22,5 | 2 508 | 86 | 87 | 1 050 | 7 444 | 98,3 % | 0,74 | 25,4 | 2028-09-01 | 616 | 2030-05-10 | 330 | 2031-04-05 | 2032-04-26 | 2031-04-05 | 286 | 2032-04-16 | 553 | 2033-10-21 | sim | não | **sim** |
| XIPS-25 (87 kg) | 6 | 814 | 33 | 27,0 | 2 763 | 86 | 87 | 1 155 | 8 201 | 80,1 % | 0,71 | 25,2 | 2028-09-01 | 617 | 2030-05-10 | 303 | 2031-03-09 | 2032-04-26 | 2031-03-09 | 263 | 2032-04-17 | 555 | 2033-10-23 | sim | não | **sim** |
| XIPS-25 (87 kg) | 7 | 814 | 36 | 31,5 | 3 021 | 86 | 87 | 1 260 | 8 961 | 64,9 % | 0,67 | 25,1 | 2028-09-01 | 619 | 2030-05-13 | 283 | 2031-02-21 | 2032-04-26 | 2031-02-21 | 246 | 2032-04-18 | 555 | 2033-10-25 | sim | não | **sim** |
| XIPS-25 (87 kg) | 8 | 814 | 39 | 36,0 | 3 269 | 86 | 87 | 1 365 | 9 710 | 52,1 % | 0,70 | 25,1 | 2028-09-01 | 629 | 2030-05-22 | 269 | 2031-02-15 | 2032-04-26 | 2031-02-15 | 233 | 2032-04-16 | 558 | 2033-10-26 | sim | não | **sim** |
| XIPS-25 (87 kg) | 9 | 814 | 42 | 40,5 | 3 525 | 86 | 87 | 1 470 | 10 467 | 41,2 % | 0,68 | 25,0 | 2028-09-01 | 631 | 2030-05-25 | 258 | 2031-02-07 | 2032-04-26 | 2031-02-07 | 223 | 2032-04-17 | 558 | 2033-10-26 | sim | não | **sim** |
| XIPS-25 (87 kg) | 10 | 814 | 45 | 45,0 | 3 781 | 86 | 87 | 1 575 | 11 225 | 31,7 % | 0,67 | 25,3 | 2028-09-01 | 638 | 2030-06-01 | 249 | 2031-02-05 | 2032-04-26 | 2031-02-05 | 216 | 2032-04-17 | 558 | 2033-10-27 | sim | não | **sim** |
| XIPS-25 (87 kg) | 11 | 814 | 47 | 49,5 | 4 001 | 87 | 87 | 1 645 | 11 881 | 24,4 % | 0,67 | 25,2 | 2028-09-01 | 640 | 2030-06-03 | 239 | 2031-01-29 | 2032-04-26 | 2031-01-29 | 207 | 2032-04-17 | 558 | 2033-10-27 | sim | não | **sim** |
| XIPS-25 (87 kg) | 12 | 814 | 50 | 54,0 | 4 256 | 87 | 87 | 1 750 | 12 638 | 17,0 % | 0,67 | 25,0 | 2028-09-01 | 640 | 2030-06-03 | 233 | 2031-01-23 | 2032-04-26 | 2031-01-23 | 202 | 2032-04-17 | 559 | 2033-10-28 | sim | não | **sim** |
| NEXT-C | 1 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| NEXT-C | 2 | 814 | 3 | 14,7 | 1 168 | 584 | 918 | 147 | 3 838 | 285,9 % | 0,56 | 25,7 | 2028-09-01 | 779 | 2030-10-20 | 306 | 2031-08-23 | 2032-04-26 | 2031-08-23 | 269 | 2033-07-15 | 821 | 2035-10-13 | não | sim | **sim** |
| NEXT-C | 3 | 814 | 4 | 22,0 | 1 414 | 471 | 918 | 196 | 4 660 | 217,9 % | 0,54 | 28,5 | 2028-09-18 | 566 | 2030-04-06 | 248 | 2030-12-11 | 2032-04-26 | 2030-12-11 | 218 | 2031-12-31 | 876 | 2034-05-25 | sim | não | **sim** |
| NEXT-C | 4 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| NEXT-C | 5 | 814 | 6 | 36,6 | 2 867 | 573 | 918 | 294 | 7 455 | 98,8 % | 0,52 | 28,5 | 2028-09-18 | 566 | 2030-04-07 | 238 | 2030-12-02 | 2032-04-26 | 2030-12-02 | 209 | 2031-07-22 | 847 | 2033-11-14 | sim | não | **sim** |
| NEXT-C | 6 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |
| NEXT-C | 7 | 814 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | **nenhuma solução verificada** |

### Verificação das soluções gravadas

Todas as tentativas de cada configuração, por origem. Pior: o maior entre os resíduos de continuidade, as violações das desigualdades e as dos limites, contra o aceito (1,0e−08, P-118). Descasamento: massa do fecho menos a massa gravada no trecho (m0 da volta; chegada a Marte), de o fecho por razões de massas (método da Etapa 2) não ter fechado por completo nas iterações da otimização; o relativo (o maior dos dois) contra a P-125 (1,0e−03).

| Propulsor | Ativos | Encontro (km) | Origem | Situação | Pior | Resíduo ida; volta | Descasamento m0 da volta (kg) | Descasamento chegada a Marte (kg) | Descasamento relativo | Margem no Falcon Heavy | Pronto no encontro | Escolhida |
| :- | -: | -: | :- | :- | -: | :- | -: | -: | -: | -: | :- | :- |
| XIPS-25 | 1 | 380 | notebook | otimizador: nenhuma solução viável encontrada (menor resíduo 2,0e−01) | — | — | — | — | — | — | — | — |
| XIPS-25 | 1 | 380 | CI | não verificada | 1,3e−11 | 3,2e−12; 1,3e−11 | −25,943 | −23,768 | 1,0e−02 | 282,95 % | 2033-11-04 | — |
| XIPS-25 | 2 | 380 | notebook | não verificada | 2,7e−11 | 7,3e−12; 2,7e−11 | −28,835 | −12,775 | 9,9e−03 | 235,98 % | 2032-09-17 | — |
| XIPS-25 | 2 | 380 | CI | não verificada | 2,1e−11 | 2,1e−11; 8,0e−12 | −28,876 | −10,710 | 9,9e−03 | 235,80 % | 2032-09-19 | — |
| XIPS-25 | 3 | 380 | notebook | não verificada | 1,6e−11 | 1,4e−11; 6,7e−12 | −4,388 | −864,912 | 1,7e−01 | 199,82 % | 2032-04-26 | — |
| XIPS-25 | 3 | 380 | CI | não verificada | 9,1e−11 | 9,1e−11; 6,3e−11 | −4,420 | −867,977 | 1,7e−01 | 199,81 % | 2032-04-26 | — |
| XIPS-25 | 4 | 380 | notebook | verificada | 4,1e−11 | 4,9e−12; 4,1e−11 | 0,000 | −0,114 | 2,5e−05 | 173,37 % | 2031-02-18 | — |
| XIPS-25 | 4 | 380 | CI | verificada | 1,4e−11 | 1,4e−11; 9,7e−12 | 0,000 | 0,000 | 3,7e−08 | 173,37 % | 2031-02-18 | **sim** |
| XIPS-25 | 5 | 380 | notebook | verificada | 2,4e−11 | 1,4e−11; 2,4e−11 | 0,000 | −0,001 | 1,4e−07 | 147,45 % | 2030-11-24 | — |
| XIPS-25 | 5 | 380 | CI | verificada | 3,2e−11 | 3,2e−11; 8,7e−13 | 0,000 | 0,000 | 4,3e−08 | 147,48 % | 2030-11-09 | **sim** |
| XIPS-25 | 6 | 380 | notebook | verificada | 2,7e−11 | 1,0e−11; 2,7e−11 | 0,000 | −0,001 | 1,8e−07 | 122,72 % | 2030-11-24 | **sim** |
| XIPS-25 | 6 | 380 | CI | verificada | 3,4e−11 | 3,4e−11; 3,4e−11 | 0,000 | −0,002 | 3,6e−07 | 122,68 % | 2030-10-14 | — |
| XIPS-25 | 7 | 380 | notebook | verificada | 6,6e−11 | 1,7e−11; 6,6e−11 | 0,000 | 0,003 | 4,8e−07 | 105,22 % | 2031-01-05 | — |
| XIPS-25 | 7 | 380 | CI | verificada | 1,8e−11 | 1,8e−11; 4,1e−12 | 0,000 | −0,001 | 2,0e−07 | 105,23 % | 2030-11-21 | **sim** |
| XIPS-25 | 8 | 380 | notebook | verificada | 5,4e−11 | 5,4e−11; 1,8e−11 | 0,000 | −0,001 | 7,8e−08 | 90,29 % | 2030-12-24 | — |
| XIPS-25 | 8 | 380 | CI | verificada | 4,9e−11 | 4,9e−11; 3,3e−11 | 0,000 | 0,004 | 5,5e−07 | 90,33 % | 2030-11-14 | **sim** |
| XIPS-25 | 9 | 380 | notebook | verificada | 4,9e−11 | 4,9e−11; 1,9e−11 | 0,000 | 0,000 | 3,3e−08 | 77,40 % | 2030-12-31 | **sim** |
| XIPS-25 | 9 | 380 | CI | verificada | 3,5e−11 | 3,5e−11; 1,3e−11 | 0,000 | 0,000 | 9,3e−09 | 77,39 % | 2030-11-04 | — |
| XIPS-25 | 10 | 380 | notebook | verificada | 8,2e−11 | 6,1e−12; 8,2e−11 | 0,000 | 0,000 | 2,2e−08 | 64,28 % | 2031-01-06 | — |
| XIPS-25 | 10 | 380 | CI | verificada | 5,1e−11 | 1,4e−11; 5,1e−11 | 0,000 | 0,063 | 8,1e−06 | 64,29 % | 2030-10-30 | **sim** |
| XIPS-25 | 11 | 380 | notebook | verificada | 1,9e−11 | 1,9e−11; 1,9e−11 | 0,000 | 0,000 | 9,8e−09 | 54,56 % | 2030-12-30 | — |
| XIPS-25 | 11 | 380 | CI | verificada | 2,8e−11 | 2,8e−11; 6,5e−12 | 0,000 | 0,001 | 1,3e−07 | 54,59 % | 2030-11-10 | **sim** |
| XIPS-25 | 12 | 380 | notebook | verificada | 3,8e−11 | 3,8e−11; 5,4e−12 | −0,864 | −1,106 | 1,3e−04 | 45,93 % | 2030-12-25 | — |
| XIPS-25 | 12 | 380 | CI | verificada | 7,3e−11 | 7,3e−11; 5,8e−12 | −0,001 | −0,217 | 2,5e−05 | 45,96 % | 2030-11-16 | **sim** |
| XIPS-25 (87 kg) | 1 | 380 | notebook | otimizador: nenhuma solução viável encontrada (menor resíduo 1,7e+00) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 2 | 380 | notebook | otimizador: nenhuma solução viável encontrada (menor resíduo 1,8e+00) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 3 | 380 | notebook | verificada | 8,1e−11 | 1,1e−11; 8,1e−11 | 0,004 | 0,148 | 2,5e−05 | 112,85 % | 2032-04-26 | **sim** |
| XIPS-25 (87 kg) | 4 | 380 | notebook | não verificada | 5,9e−11 | 5,9e−11; 3,0e−11 | 2,372 | 90,105 | 1,4e−02 | 91,19 % | 2032-04-26 | — |
| XIPS-25 (87 kg) | 5 | 380 | notebook | não verificada | 3,6e−11 | 3,6e−11; 3,0e−11 | 0,319 | 13,748 | 1,9e−03 | 71,83 % | 2032-05-21 | — |
| XIPS-25 (87 kg) | 6 | 380 | notebook | otimizador: sem convergência do otimizador (menor resíduo 2,7e−10) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 7 | 380 | notebook | otimizador: sem convergência do otimizador (menor resíduo 6,2e−09) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 8 | 380 | notebook | otimizador: nenhuma solução viável encontrada (menor resíduo 6,8e−01) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 9 | 380 | notebook | otimizador: nenhuma solução viável encontrada (menor resíduo 1,3e−01) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 10 | 380 | notebook | otimizador: nenhuma solução viável encontrada (menor resíduo 6,4e−02) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 11 | 380 | notebook | não verificada | 4,7e+01 | 7,0e−11; 2,6e−11 | 1 641,751 | 34,550 | 1,5e−01 | −22,60 % | 2032-01-23 | — |
| XIPS-25 (87 kg) | 12 | 380 | notebook | não verificada | 2,0e−01 | 9,0e−12; 7,4e−11 | −2 074,089 | −2 685,861 | 1,5e−01 | −16,66 % | 2031-09-30 | — |
| NEXT-C | 1 | 380 | notebook | verificada | 5,9e−11 | 1,1e−11; 5,9e−11 | −0,048 | −2,025 | 7,1e−04 | 346,55 % | 2032-10-24 | **sim** |
| NEXT-C | 1 | 380 | CI | verificada | 5,9e−11 | 1,1e−11; 5,9e−11 | −0,048 | −2,025 | 7,1e−04 | 346,55 % | 2032-10-24 | — |
| NEXT-C | 2 | 380 | notebook | otimizador: nenhuma solução viável encontrada (menor resíduo 2,7e+01) | — | — | — | — | — | — | — | — |
| NEXT-C | 2 | 380 | CI | otimizador: nenhuma solução viável encontrada (menor resíduo 2,7e+01) | — | — | — | — | — | — | — | — |
| NEXT-C | 3 | 380 | notebook | verificada | 7,0e−11 | 1,0e−11; 7,0e−11 | 0,000 | 0,001 | 1,3e−07 | 216,82 % | 2031-01-02 | **sim** |
| NEXT-C | 3 | 380 | CI | verificada | 7,0e−11 | 1,0e−11; 7,0e−11 | 0,000 | 0,001 | 1,3e−07 | 216,82 % | 2031-01-02 | — |
| NEXT-C | 4 | 380 | notebook | verificada | 4,2e−11 | 4,2e−11; 5,7e−12 | 0,000 | 0,001 | 2,7e−07 | 169,28 % | 2030-12-07 | **sim** |
| NEXT-C | 4 | 380 | CI | verificada | 4,2e−11 | 4,2e−11; 5,7e−12 | 0,000 | 0,001 | 2,7e−07 | 169,28 % | 2030-12-07 | — |
| NEXT-C | 5 | 380 | notebook | verificada | 6,7e−11 | 2,6e−11; 6,7e−11 | 0,000 | 0,000 | 1,6e−08 | 134,14 % | 2030-11-06 | **sim** |
| NEXT-C | 5 | 380 | CI | verificada | 6,7e−11 | 2,6e−11; 6,7e−11 | 0,000 | 0,000 | 1,6e−08 | 134,14 % | 2030-11-06 | — |
| NEXT-C | 6 | 380 | notebook | verificada | 2,5e−11 | 5,1e−12; 2,5e−11 | 0,000 | −0,001 | 1,8e−07 | 107,13 % | 2030-12-05 | **sim** |
| NEXT-C | 6 | 380 | CI | verificada | 2,5e−11 | 5,1e−12; 2,5e−11 | 0,000 | −0,001 | 1,8e−07 | 107,13 % | 2030-12-05 | — |
| NEXT-C | 7 | 380 | notebook | verificada | 2,9e−11 | 2,9e−12; 2,9e−11 | 0,000 | 0,253 | 3,6e−05 | 85,71 % | 2030-12-11 | **sim** |
| NEXT-C | 7 | 380 | CI | verificada | 2,9e−11 | 2,9e−12; 2,9e−11 | 0,000 | 0,253 | 3,6e−05 | 85,71 % | 2030-12-11 | — |
| XIPS-25 | 1 | 814 | notebook | otimizador: nenhuma solução viável encontrada (menor resíduo 7,7e−01) | — | — | — | — | — | — | — | — |
| XIPS-25 | 1 | 814 | CI | verificada | 6,4e−11 | 1,9e−11; 6,4e−11 | 0,002 | 0,060 | 2,0e−05 | 304,31 % | 2033-08-12 | **sim** |
| XIPS-25 | 2 | 814 | notebook | otimizador: nenhuma solução viável encontrada (menor resíduo 1,3e+00) | — | — | — | — | — | — | — | — |
| XIPS-25 | 2 | 814 | CI | verificada | 6,2e−11 | 6,2e−11; 6,6e−12 | −0,078 | −3,158 | 8,9e−04 | 253,37 % | 2032-07-14 | **sim** |
| XIPS-25 | 3 | 814 | notebook | não verificada | 4,8e−11 | 4,8e−11; 3,0e−11 | −6,419 | −1 273,398 | 2,4e−01 | 211,32 % | 2032-04-26 | — |
| XIPS-25 | 3 | 814 | CI | não verificada | 3,2e−11 | 1,5e−11; 3,2e−11 | −0,162 | −7,392 | 1,6e−03 | 174,51 % | 2031-07-27 | — |
| XIPS-25 | 4 | 814 | notebook | verificada | 1,6e−11 | 1,6e−11; 1,4e−11 | 0,000 | 0,000 | 2,9e−08 | 178,21 % | 2031-01-21 | — |
| XIPS-25 | 4 | 814 | CI | verificada | 5,7e−11 | 5,7e−11; 3,3e−11 | 0,000 | 0,000 | 1,1e−07 | 178,22 % | 2031-01-24 | **sim** |
| XIPS-25 | 5 | 814 | notebook | verificada | 7,0e−11 | 7,0e−11; 4,7e−11 | 0,000 | 0,000 | 1,4e−08 | 151,79 % | 2030-10-12 | — |
| XIPS-25 | 5 | 814 | CI | verificada | 4,0e−11 | 2,3e−11; 4,0e−11 | −0,001 | 0,002 | 4,5e−07 | 151,79 % | 2030-10-16 | **sim** |
| XIPS-25 | 6 | 814 | notebook | verificada | 6,8e−11 | 6,8e−11; 3,6e−11 | 0,000 | 0,000 | 2,6e−08 | 129,99 % | 2030-09-25 | **sim** |
| XIPS-25 | 6 | 814 | CI | verificada | 3,3e−11 | 1,3e−11; 3,3e−11 | 0,000 | −0,132 | 2,4e−05 | 129,98 % | 2030-10-27 | — |
| XIPS-25 | 7 | 814 | notebook | verificada | 3,3e−11 | 3,3e−11; 8,4e−12 | 0,000 | 0,000 | 6,6e−08 | 111,66 % | 2030-09-09 | **sim** |
| XIPS-25 | 7 | 814 | CI | verificada | 6,5e−11 | 6,5e−11; 1,2e−11 | 0,000 | 0,005 | 8,8e−07 | 111,65 % | 2030-11-16 | — |
| XIPS-25 | 8 | 814 | notebook | verificada | 3,0e−11 | 1,2e−11; 3,0e−11 | 0,000 | 0,007 | 1,1e−06 | 96,00 % | 2030-08-25 | **sim** |
| XIPS-25 | 8 | 814 | CI | verificada | 9,5e−12 | 9,5e−12; 7,5e−12 | 0,000 | 0,004 | 6,8e−07 | 95,99 % | 2030-11-26 | — |
| XIPS-25 | 9 | 814 | notebook | verificada | 4,5e−11 | 2,8e−11; 4,5e−11 | 0,000 | 0,000 | 3,1e−08 | 80,35 % | 2030-09-04 | **sim** |
| XIPS-25 | 9 | 814 | CI | verificada | 6,1e−11 | 4,5e−11; 6,1e−11 | 0,000 | 0,008 | 1,1e−06 | 80,33 % | 2030-11-29 | — |
| XIPS-25 | 10 | 814 | notebook | verificada | 5,0e−11 | 3,1e−11; 5,0e−11 | 0,000 | 0,003 | 4,2e−07 | 68,85 % | 2030-09-20 | **sim** |
| XIPS-25 | 10 | 814 | CI | verificada | 7,3e−11 | 7,3e−11; 2,5e−12 | −0,002 | 0,005 | 7,2e−07 | 68,85 % | 2030-11-25 | — |
| XIPS-25 | 11 | 814 | notebook | verificada | 1,0e−11 | 1,0e−11; 6,2e−12 | 0,000 | −0,001 | 1,8e−07 | 58,75 % | 2030-10-31 | **sim** |
| XIPS-25 | 11 | 814 | CI | verificada | 3,1e−09 | 9,6e−12; 3,1e−09 | 0,000 | 0,000 | 2,0e−09 | 58,72 % | 2030-12-10 | — |
| XIPS-25 | 12 | 814 | notebook | verificada | 8,3e−11 | 3,5e−11; 8,3e−11 | 0,000 | −1,276 | 1,5e−04 | 49,75 % | 2030-11-22 | — |
| XIPS-25 | 12 | 814 | CI | verificada | 9,8e−11 | 9,8e−11; 1,3e−11 | −0,001 | −1,140 | 1,3e−04 | 49,76 % | 2030-12-08 | **sim** |
| XIPS-25 (87 kg) | 1 | 814 | notebook | otimizador: nenhuma solução viável encontrada (menor resíduo 2,0e+00) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 1 | 814 | CI | otimizador: nenhuma solução viável encontrada (menor resíduo 2,0e+00) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 2 | 814 | notebook | otimizador: nenhuma solução viável encontrada (menor resíduo 9,5e−01) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 2 | 814 | CI | otimizador: nenhuma solução viável encontrada (menor resíduo 2,0e+00) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 3 | 814 | notebook | otimizador: nenhuma solução viável encontrada (menor resíduo 2,0e+00) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 3 | 814 | CI | otimizador: nenhuma solução viável encontrada (menor resíduo 1,7e+00) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 4 | 814 | notebook | otimizador: nenhuma solução viável encontrada (menor resíduo 1,8e+00) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 4 | 814 | CI | otimizador: nenhuma solução viável encontrada (menor resíduo 1,8e+00) | — | — | — | — | — | — | — | — |
| XIPS-25 (87 kg) | 5 | 814 | notebook | verificada | 3,3e−11 | 3,3e−11; 2,0e−11 | 0,000 | 0,000 | 9,7e−09 | 98,26 % | 2031-03-27 | — |
| XIPS-25 (87 kg) | 5 | 814 | CI | verificada | 9,2e−11 | 9,2e−11; 3,0e−12 | 0,000 | 0,001 | 1,2e−07 | 98,26 % | 2031-04-05 | **sim** |
| XIPS-25 (87 kg) | 6 | 814 | notebook | verificada | 4,3e−11 | 4,0e−11; 4,3e−11 | 0,000 | 0,000 | 5,2e−09 | 80,07 % | 2031-03-06 | — |
| XIPS-25 (87 kg) | 6 | 814 | CI | verificada | 7,6e−11 | 5,7e−11; 7,6e−11 | 0,000 | 0,001 | 1,4e−07 | 80,08 % | 2031-03-09 | **sim** |
| XIPS-25 (87 kg) | 7 | 814 | notebook | verificada | 3,1e−11 | 3,1e−11; 1,8e−11 | 0,000 | 0,000 | 4,2e−08 | 64,92 % | 2031-02-21 | **sim** |
| XIPS-25 (87 kg) | 7 | 814 | CI | verificada | 3,1e−11 | 3,1e−11; 1,8e−11 | 0,000 | 0,000 | 4,2e−08 | 64,92 % | 2031-02-21 | — |
| XIPS-25 (87 kg) | 8 | 814 | notebook | verificada | 5,7e−11 | 1,4e−11; 5,7e−11 | 0,000 | 0,000 | 3,3e−09 | 52,14 % | 2031-02-15 | **sim** |
| XIPS-25 (87 kg) | 8 | 814 | CI | verificada | 5,7e−11 | 1,4e−11; 5,7e−11 | 0,000 | 0,000 | 3,3e−09 | 52,14 % | 2031-02-15 | — |
| XIPS-25 (87 kg) | 9 | 814 | notebook | verificada | 6,4e−11 | 3,6e−11; 6,4e−11 | 0,000 | 0,000 | 2,9e−08 | 41,16 % | 2031-02-07 | **sim** |
| XIPS-25 (87 kg) | 9 | 814 | CI | verificada | 6,4e−11 | 3,6e−11; 6,4e−11 | 0,000 | 0,000 | 2,9e−08 | 41,16 % | 2031-02-07 | — |
| XIPS-25 (87 kg) | 10 | 814 | notebook | verificada | 1,8e−11 | 1,5e−11; 1,8e−11 | 0,000 | 0,000 | 1,1e−08 | 31,66 % | 2031-02-05 | **sim** |
| XIPS-25 (87 kg) | 10 | 814 | CI | verificada | 1,8e−11 | 1,5e−11; 1,8e−11 | 0,000 | 0,000 | 1,1e−08 | 31,66 % | 2031-02-05 | — |
| XIPS-25 (87 kg) | 11 | 814 | notebook | verificada | 2,8e−11 | 2,8e−11; 1,6e−11 | 0,000 | −0,095 | 9,3e−06 | 24,39 % | 2031-01-29 | **sim** |
| XIPS-25 (87 kg) | 11 | 814 | CI | verificada | 2,8e−11 | 2,8e−11; 1,6e−11 | 0,000 | −0,095 | 9,3e−06 | 24,39 % | 2031-01-29 | — |
| XIPS-25 (87 kg) | 12 | 814 | notebook | verificada | 5,6e−11 | 5,6e−11; 5,2e−11 | −0,001 | −0,745 | 6,9e−05 | 16,96 % | 2031-01-23 | **sim** |
| XIPS-25 (87 kg) | 12 | 814 | CI | verificada | 5,6e−11 | 5,6e−11; 5,2e−11 | −0,001 | −0,745 | 6,9e−05 | 16,96 % | 2031-01-23 | — |
| NEXT-C | 1 | 814 | CI | otimizador: nenhuma solução viável encontrada (menor resíduo 3,7e−01) | — | — | — | — | — | — | — | — |
| NEXT-C | 1 | 814 | notebook | não verificada | 4,1e−11 | 1,3e−11; 4,1e−11 | −9,430 | −25,578 | 9,6e−03 | 386,33 % | 2032-08-12 | — |
| NEXT-C | 2 | 814 | notebook | verificada | 3,8e−11 | 2,3e−12; 3,8e−11 | −0,001 | −0,102 | 3,0e−05 | 285,84 % | 2031-01-17 | — |
| NEXT-C | 2 | 814 | CI | verificada | 4,9e−11 | 1,7e−11; 4,9e−11 | 0,000 | −0,003 | 7,9e−07 | 285,86 % | 2031-08-23 | **sim** |
| NEXT-C | 3 | 814 | notebook | verificada | 8,2e−11 | 8,2e−11; 5,4e−11 | 0,000 | 0,018 | 4,4e−06 | 217,95 % | 2030-12-11 | **sim** |
| NEXT-C | 3 | 814 | CI | verificada | 8,2e−11 | 8,2e−11; 2,7e−11 | 0,001 | 0,352 | 8,6e−05 | 217,79 % | 2031-10-17 | — |
| NEXT-C | 4 | 814 | CI | otimizador: nenhuma solução viável encontrada (menor resíduo 1,1e−01) | — | — | — | — | — | — | — | — |
| NEXT-C | 4 | 814 | notebook | não verificada | 1,0e+00 | 7,8e−11; 2,6e−11 | 20,635 | 93,958 | 1,6e−02 | 116,04 % | 2030-12-17 | — |
| NEXT-C | 5 | 814 | notebook | verificada | 3,2e−11 | 1,6e−11; 3,2e−11 | −1,715 | −0,504 | 3,3e−04 | 98,81 % | 2030-12-02 | **sim** |
| NEXT-C | 5 | 814 | CI | não verificada | 4,7e−11 | 1,3e−11; 4,7e−11 | 5,635 | 48,027 | 7,0e−03 | 87,72 % | 2031-02-05 | — |
| NEXT-C | 6 | 814 | notebook | não verificada | 3,1e−11 | 2,1e−11; 3,1e−11 | −24,713 | −53,945 | 7,4e−03 | 77,99 % | 2030-12-06 | — |
| NEXT-C | 6 | 814 | CI | não verificada | 5,8e−11 | 5,8e−11; 4,9e−11 | −43,917 | −67,237 | 8,9e−03 | 73,31 % | 2031-01-29 | — |
| NEXT-C | 7 | 814 | notebook | não verificada | 1,0e−11 | 7,6e−12; 1,0e−11 | −106,795 | −275,916 | 3,3e−02 | 58,88 % | 2030-12-30 | — |
| NEXT-C | 7 | 814 | CI | não verificada | 6,2e−12 | 6,2e−12; 6,1e−12 | −166,185 | −389,472 | 4,5e−02 | 55,47 % | 2031-02-12 | — |

## Estocagem do MAV na superfície

Pouso do lander em 2029-09-20 (Ls 189,5°). Aquecimento de results/familia1/mavs.yaml (modelo da P-027); RHU com a potência do ano do lançamento do MAV ([F155] p. 1: 0,90 W em 2014, menos 0,01 W por ano). Teto oferecido ao New Frontiers: 43 RHUs ([F155] p. 2).
Temporadas de tempestade global (Ls 180° a 340°, P-124) tocadas entre o pouso e o lançamento do MAV; na missão de referência (MAV no lançamento mais cedo, 2029-11-03): 1.
Envelhecimento do propelente sólido: só há resultado publicado da fase de vácuo ([F263] PDF p. 1, perda de massa abaixo de 0,1 %); a fase de um ano em condições de superfície de Marte estava planejada ([F263] PDF p. 1) e não há resultado publicado achado; o projeto do MSR previa cerca de um ano na superfície ([F35] PDF p. 1).

| Propulsor | Ativos | Encontro (km) | Lançamento do MAV | Dias na superfície | Ls no lançamento (°) | Temporadas de tempestade | MAV | Temperatura mantida (°C) | Aquecimento (W) | Energia (kWh) | RHUs |
| :- | -: | -: | :- | -: | -: | -: | :- | -: | -: | -: | -: |
| XIPS-25 | 4 | 380 | 2031-02-18 | 516 | 103,0 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 232 | 26 |
| XIPS-25 | 4 | 380 | 2031-02-18 | 516 | 103,0 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 837 | 93 |
| XIPS-25 | 4 | 380 | 2031-02-18 | 516 | 103,0 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 403 | 45 |
| XIPS-25 | 4 | 380 | 2031-02-18 | 516 | 103,0 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 332 | 37 |
| XIPS-25 | 5 | 380 | 2030-11-09 | 415 | 58,6 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 186 | 26 |
| XIPS-25 | 5 | 380 | 2030-11-09 | 415 | 58,6 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 673 | 92 |
| XIPS-25 | 5 | 380 | 2030-11-09 | 415 | 58,6 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 324 | 44 |
| XIPS-25 | 5 | 380 | 2030-11-09 | 415 | 58,6 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 267 | 37 |
| XIPS-25 | 6 | 380 | 2030-11-24 | 430 | 65,1 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 193 | 26 |
| XIPS-25 | 6 | 380 | 2030-11-24 | 430 | 65,1 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 698 | 92 |
| XIPS-25 | 6 | 380 | 2030-11-24 | 430 | 65,1 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 336 | 44 |
| XIPS-25 | 6 | 380 | 2030-11-24 | 430 | 65,1 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 277 | 37 |
| XIPS-25 | 7 | 380 | 2030-11-21 | 427 | 63,8 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 192 | 26 |
| XIPS-25 | 7 | 380 | 2030-11-21 | 427 | 63,8 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 693 | 92 |
| XIPS-25 | 7 | 380 | 2030-11-21 | 427 | 63,8 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 333 | 44 |
| XIPS-25 | 7 | 380 | 2030-11-21 | 427 | 63,8 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 275 | 37 |
| XIPS-25 | 8 | 380 | 2030-11-14 | 420 | 60,8 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 189 | 26 |
| XIPS-25 | 8 | 380 | 2030-11-14 | 420 | 60,8 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 681 | 92 |
| XIPS-25 | 8 | 380 | 2030-11-14 | 420 | 60,8 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 328 | 44 |
| XIPS-25 | 8 | 380 | 2030-11-14 | 420 | 60,8 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 270 | 37 |
| XIPS-25 | 9 | 380 | 2030-12-31 | 467 | 81,3 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 210 | 26 |
| XIPS-25 | 9 | 380 | 2030-12-31 | 467 | 81,3 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 758 | 92 |
| XIPS-25 | 9 | 380 | 2030-12-31 | 467 | 81,3 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 365 | 44 |
| XIPS-25 | 9 | 380 | 2030-12-31 | 467 | 81,3 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 300 | 37 |
| XIPS-25 | 10 | 380 | 2030-10-30 | 405 | 54,2 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 182 | 26 |
| XIPS-25 | 10 | 380 | 2030-10-30 | 405 | 54,2 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 657 | 92 |
| XIPS-25 | 10 | 380 | 2030-10-30 | 405 | 54,2 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 316 | 44 |
| XIPS-25 | 10 | 380 | 2030-10-30 | 405 | 54,2 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 261 | 37 |
| XIPS-25 | 11 | 380 | 2030-11-10 | 416 | 59,0 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 187 | 26 |
| XIPS-25 | 11 | 380 | 2030-11-10 | 416 | 59,0 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 675 | 92 |
| XIPS-25 | 11 | 380 | 2030-11-10 | 416 | 59,0 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 325 | 44 |
| XIPS-25 | 11 | 380 | 2030-11-10 | 416 | 59,0 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 268 | 37 |
| XIPS-25 | 12 | 380 | 2030-11-16 | 422 | 61,6 | 1 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 190 | 26 |
| XIPS-25 | 12 | 380 | 2030-11-16 | 422 | 61,6 | 1 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 685 | 92 |
| XIPS-25 | 12 | 380 | 2030-11-16 | 422 | 61,6 | 1 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 329 | 44 |
| XIPS-25 | 12 | 380 | 2030-11-16 | 422 | 61,6 | 1 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 271 | 37 |
| XIPS-25 (87 kg) | 3 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Sólido, 380 km, sem margem (o menor que chega) | −40 | 18,7 | 471 | 26 |
| XIPS-25 (87 kg) | 3 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | −40 | 67,6 | 1 700 | 94 |
| XIPS-25 (87 kg) | 3 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 15 | 32,5 | 818 | 46 |
| XIPS-25 (87 kg) | 3 | 380 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 380 km, sem margem | 15 | 26,8 | 674 | 38 |
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
| XIPS-25 | 1 | 814 | 2033-08-12 | 1422 | 218,3 | 3 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 1 200 | 50 |
| XIPS-25 | 1 | 814 | 2033-08-12 | 1422 | 218,3 | 3 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 980 | 41 |
| XIPS-25 | 2 | 814 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 884 | 49 |
| XIPS-25 | 2 | 814 | 2032-08-03 | 1048 | 34,5 | 2 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 722 | 40 |
| XIPS-25 | 4 | 814 | 2031-01-24 | 491 | 91,8 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 414 | 49 |
| XIPS-25 | 4 | 814 | 2031-01-24 | 491 | 91,8 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 338 | 40 |
| XIPS-25 | 5 | 814 | 2030-10-16 | 391 | 48,0 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 330 | 48 |
| XIPS-25 | 5 | 814 | 2030-10-16 | 391 | 48,0 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 269 | 39 |
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
| XIPS-25 | 12 | 814 | 2030-12-08 | 444 | 71,2 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 375 | 48 |
| XIPS-25 | 12 | 814 | 2030-12-08 | 444 | 71,2 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 306 | 39 |
| XIPS-25 (87 kg) | 5 | 814 | 2031-04-05 | 562 | 124,2 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 474 | 49 |
| XIPS-25 (87 kg) | 5 | 814 | 2031-04-05 | 562 | 124,2 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 387 | 40 |
| XIPS-25 (87 kg) | 6 | 814 | 2031-03-09 | 535 | 111,6 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 451 | 49 |
| XIPS-25 (87 kg) | 6 | 814 | 2031-03-09 | 535 | 111,6 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 369 | 40 |
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
| NEXT-C | 2 | 814 | 2031-08-23 | 702 | 198,3 | 2 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 592 | 49 |
| NEXT-C | 2 | 814 | 2031-08-23 | 702 | 198,3 | 2 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 484 | 40 |
| NEXT-C | 3 | 814 | 2030-12-11 | 447 | 72,6 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 377 | 48 |
| NEXT-C | 3 | 814 | 2030-12-11 | 447 | 72,6 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 308 | 39 |
| NEXT-C | 5 | 814 | 2030-12-02 | 438 | 68,6 | 1 | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 15 | 35,2 | 370 | 48 |
| NEXT-C | 5 | 814 | 2030-12-02 | 438 | 68,6 | 1 | Hipergólico 4 × 164:1, 814 km, sem margem | 15 | 28,7 | 302 | 39 |
