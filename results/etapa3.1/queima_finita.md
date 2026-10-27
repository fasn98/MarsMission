# Etapa 3.1 — motores reais e queima finita (gerado por tools/queima_finita.py)

Modelo: plano, dois corpos (Marte pontual), empuxo constante tangente à velocidade, vazão T/(Isp g0). Perda = Δv entregue pelo motor − Δv impulsivo no periapse. Rótulo: calculado (não verificado contra caso publicado).

Massa no início de cada queima e propelente dimensionado: dimensionamento atual (regra iii, Isp de 321 s, perdas da P-015 e margem de Δv da P-014), sem refazer com o Isp de cada combinação. "Cabe?" compara o propelente da queima finita com o dimensionado para aquela queima; o caso de referência usa o mesmo veículo.

Perdas do DRA usadas hoje (P-015, NÃO VALIDADA): captura 18 m/s; saída de Marte 11 m/s.

## Captura em Marte (órbita de 1 sol)

| Combinação | Empuxo (N) | Isp (s) | Caso | v∞ (km/s) | m0 (kg) | Queima (s) | Propelente (kg) | Δv impulsivo (m/s) | Perda (m/s) | Perda (% do Δv) | Perda / P-015 | Periapse de chegada (km) | Altitude mínima (km) | Propelente dimensionado (kg) | Cabe? | Queima única máx. (s) | Excede? |
| :- | -: | -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- |
| C1: 2 × S400-15 | 850 | 321,0 | projeto (pior janela) (2031-conjuncao) | 3,484 | 6 169 | 9 901 | 2 674 | 1 344 | 444,5 | 33,1 | 24,7× | 1 471 | 454 | 2 336 | **não** | 6 660 | **sim** |
| C1: 2 × S400-15 | 850 | 321,0 | referência (2028-conjuncao) | 2,971 | 6 169 | 8 151 | 2 201 | 1 059 | 329,7 | 31,1 | 18,3× | 1 210 | 449 | 2 336 | sim | 6 660 | **sim** |
| C2: 8 × R-4D-11 | 3 914 | 315,0 | projeto (pior janela) (2031-conjuncao) | 3,484 | 6 169 | 1 794 | 2 274 | 1 344 | 76,4 | 5,7 | 4,2× | 412 | 302 | 2 336 | sim | 12 000 | não |
| C2: 8 × R-4D-11 | 3 914 | 315,0 | referência (2028-conjuncao) | 2,971 | 6 169 | 1 461 | 1 851 | 1 059 | 43,0 | 4,1 | 2,4× | 348 | 286 | 2 336 | sim | 12 000 | não |
| C3: 1 × OMS-E | 26 700 | 315,1 | projeto (pior janela) (2031-conjuncao) | 3,484 | 6 169 | 252 | 2 178 | 1 344 | 2,1 | 0,2 | 0,1× | 254 | 252 | 2 336 | sim | 1 030 | não |
| C3: 1 × OMS-E | 26 700 | 315,1 | referência (2028-conjuncao) | 2,971 | 6 169 | 207 | 1 792 | 1 059 | 1,1 | 0,1 | 0,1× | 252 | 251 | 2 336 | sim | 1 030 | não |

## Saída de Marte (injeção trans-Terra)

| Combinação | Empuxo (N) | Isp (s) | Caso | v∞ (km/s) | Órbita inicial | m0 (kg) | Queima (s) | Propelente (kg) | Δv impulsivo (m/s) | Perda (m/s) | Perda (% do Δv) | Perda / P-015 | Propelente dimensionado (kg) | Cabe? | Queima única máx. (s) | Excede? |
| :- | -: | -: | :- | -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- |
| R1: 1 × S400-15 | 425 | 321,0 | projeto (pior janela) (2035-conjuncao) | 3,543 | órbita de 1 sol | 2 769 | 9 188 | 1 241 | 1 378 | 492,5 | 35,7 | 44,8× | 1 065 | **não** | 6 660 | **sim** |
| R1: 1 × S400-15 | 425 | 321,0 | referência (2028-conjuncao) | 2,330 | órbita de 1 sol | 2 769 | 5 233 | 707 | 753 | 174,9 | 23,2 | 15,9× | 1 065 | sim | 6 660 | não |
| R2: 2 × S400-15 | 850 | 321,0 | projeto (pior janela) (2035-conjuncao) | 3,543 | órbita de 1 sol | 2 769 | 4 126 | 1 114 | 1 378 | 242,2 | 17,6 | 22,0× | 1 065 | **não** | 6 660 | não |
| R2: 2 × S400-15 | 850 | 321,0 | referência (2028-conjuncao) | 2,330 | órbita de 1 sol | 2 769 | 2 341 | 632 | 753 | 63,2 | 8,4 | 5,7× | 1 065 | sim | 6 660 | não |
| R3: 4 × R-4D-11 | 1 957 | 315,0 | projeto (pior janela) (2035-conjuncao) | 3,543 | órbita de 1 sol | 2 769 | 1 637 | 1 037 | 1 378 | 71,4 | 5,2 | 6,5× | 1 065 | sim | 12 000 | não |
| R3: 4 × R-4D-11 | 1 957 | 315,0 | referência (2028-conjuncao) | 2,330 | órbita de 1 sol | 2 769 | 960 | 609 | 753 | 14,1 | 1,9 | 1,3× | 1 065 | sim | 12 000 | não |

## Cruzeiro do lander (todas as correções da ida, somadas)

Perda de queima finita não calculada: Δv pequeno, longe de qualquer planeta.

| Combinação | Empuxo (N) | Isp (s) | m0 (kg) | Δv total (m/s) | Tempo total de queima (s) | Queima única máx. (s) |
| :- | -: | -: | -: | -: | -: | -: |
| Z1: 4 × 10N | 40 | 292 | 3 740 | 71,5 | 6 602 | 28 800 |
| Z2: 8 × 10N | 80 | 292 | 3 740 | 71,5 | 3 301 | 28 800 |

## MAV (dois estágios)

Empuxo/peso na superfície de Marte, g = 3,713 m/s². Perda de subida já incluída no Δv (Etapa 2.1); não recalculada. O dimensionamento usa Isp de 343 s (Bowles et al. 2013, motor com turbobomba). O estágio 2 acende em voo: o empuxo/peso dele em Marte é só referência.

| Estágio | Combinação | Empuxo (N) | Isp (s) | m0 (kg) | Δv (m/s) | Queima (s) | Empuxo/peso em Marte | Aceleração inicial (m/s²) | Queima única máx. (s) | Excede? |
| :- | :- | -: | -: | -: | -: | -: | -: | -: | -: | :- |
| mav_1 | M1: 2 × R-42 | 1 779 | 305 | 267,8 | 2 772 | 272 | 1,79 | 6,64 | 3 940 | não |
| mav_1 | M2: 4 × R-4D-11 | 1 957 | 315 | 267,8 | 2 772 | 250 | 1,97 | 7,31 | 12 000 | não |
| mav_1 | M3: 1 × R-40B | 4 003 | 296 | 267,8 | 2 772 | 119 | 4,03 | 14,95 | 500 | não |
| mav_2 | N1: 1 × S400-15 | 425 | 321 | 70,5 | 2 991 | 320 | 1,62 | 6,03 | 6 660 | não |
| mav_2 | N2: 1 × R-4D-11 | 489 | 315 | 70,5 | 2 991 | 276 | 1,87 | 6,94 | 12 000 | não |
