# Etapa 3.1 — motores reais e queima finita (gerado por tools/queima_finita.py)

Modelo: plano, dois corpos (Marte pontual), empuxo constante tangente à velocidade, vazão T/(Isp g0). Perda = Δv entregue pelo motor − Δv impulsivo no periapse. Rótulo: calculado (não verificado contra caso publicado).

O mínimo do propelente no início da queima é plano: o início, a altitude mínima durante a queima e o periapse de chegada são mal condicionados, e as apsides finais da captura carregam o resíduo do ajuste ao alvo; vão arredondados (config/queima_finita.yaml, P-041). A perda, a duração e o propelente não.

Massa no início de cada queima e propelente dimensionado: dimensionamento atual (regra iii, Isp de 321 s, perdas da P-015 e margem de Δv da P-014), sem refazer com o Isp de cada combinação. "Cabe?" compara o propelente da queima finita com o dimensionado para aquela queima; o caso de referência usa o mesmo veículo.

Perdas do DRA usadas hoje (P-015, NÃO VALIDADA): captura 18 m/s; saída de Marte 11 m/s.

## Captura em Marte (órbita de 1 sol)

| Combinação | Empuxo (N) | Isp (s) | Caso | v∞ (km/s) | m0 (kg) | Queima (s) | Propelente (kg) | Δv impulsivo (m/s) | Perda (m/s) | Perda (% do Δv) | Perda / P-015 | Periapse de chegada (km) | Altitude mínima durante a queima (km) | Propelente dimensionado (kg) | Cabe? | Queima única máx. (s) | Excede? |
| :- | -: | -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- |
| C1: 2 × S400-15 | 850 | 321,0 | projeto (pior janela) (2031-conjuncao) | 3,484 | 6 169 | 9 901 | 2 674 | 1 344 | 444,5 | 33,1 | 24,7× | 1 471 | 454 | 2 336 | **não** | 6 660 | **sim** |
| C1: 2 × S400-15 | 850 | 321,0 | referência (2028-conjuncao) | 2,971 | 6 169 | 8 151 | 2 201 | 1 059 | 329,7 | 31,1 | 18,3× | 1 210 | 449 | 2 336 | sim | 6 660 | **sim** |
| C2: 8 × R-4D-11 | 3 914 | 310,0 | projeto (pior janela) (2031-conjuncao) | 3,484 | 6 169 | 1 788 | 2 302 | 1 344 | 75,9 | 5,6 | 4,2× | 411 | 301 | 2 336 | sim | 2 000 | não |
| C2: 8 × R-4D-11 | 3 914 | 310,0 | referência (2028-conjuncao) | 2,971 | 6 169 | 1 457 | 1 876 | 1 059 | 42,8 | 4,0 | 2,4× | 347 | 285 | 2 336 | sim | 2 000 | não |
| C3: 1 × OMS-E | 26 700 | 315,1 | projeto (pior janela) (2031-conjuncao) | 3,484 | 6 169 | 252 | 2 178 | 1 344 | 2,1 | 0,2 | 0,1× | 254 | 252 | 2 336 | sim | 1 030 | não |
| C3: 1 × OMS-E | 26 700 | 315,1 | referência (2028-conjuncao) | 2,971 | 6 169 | 207 | 1 792 | 1 059 | 1,1 | 0,1 | 0,1× | 252 | 251 | 2 336 | sim | 1 030 | não |

## Saída de Marte (injeção trans-Terra)

| Combinação | Empuxo (N) | Isp (s) | Caso | v∞ (km/s) | Órbita inicial | m0 (kg) | Queima (s) | Propelente (kg) | Δv impulsivo (m/s) | Perda (m/s) | Perda (% do Δv) | Perda / P-015 | Propelente dimensionado (kg) | Cabe? | Queima única máx. (s) | Excede? |
| :- | -: | -: | :- | -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- |
| R1: 1 × S400-15 | 425 | 321,0 | projeto (pior janela) (2035-conjuncao) | 3,543 | órbita de 1 sol | 2 769 | 9 188 | 1 241 | 1 378 | 492,5 | 35,7 | 44,8× | 1 065 | **não** | 6 660 | **sim** |
| R1: 1 × S400-15 | 425 | 321,0 | referência (2028-conjuncao) | 2,330 | órbita de 1 sol | 2 769 | 5 233 | 707 | 753 | 174,9 | 23,2 | 15,9× | 1 065 | sim | 6 660 | não |
| R2: 2 × S400-15 | 850 | 321,0 | projeto (pior janela) (2035-conjuncao) | 3,543 | órbita de 1 sol | 2 769 | 4 126 | 1 114 | 1 378 | 242,2 | 17,6 | 22,0× | 1 065 | **não** | 6 660 | não |
| R2: 2 × S400-15 | 850 | 321,0 | referência (2028-conjuncao) | 2,330 | órbita de 1 sol | 2 769 | 2 341 | 632 | 753 | 63,2 | 8,4 | 5,7× | 1 065 | sim | 6 660 | não |
| R3: 4 × R-4D-11 | 1 957 | 310,0 | projeto (pior janela) (2035-conjuncao) | 3,543 | órbita de 1 sol | 2 769 | 1 631 | 1 050 | 1 378 | 71,0 | 5,1 | 6,5× | 1 065 | sim | 2 000 | não |
| R3: 4 × R-4D-11 | 1 957 | 310,0 | referência (2028-conjuncao) | 2,330 | órbita de 1 sol | 2 769 | 959 | 617 | 753 | 14,0 | 1,9 | 1,3× | 1 065 | sim | 2 000 | não |

## Várias queimas no periapse (P-042)

A 1ª queima da captura (a última da saída) leva o excesso hiperbólico numa única passagem, até uma órbita alta de apoapse = 0,333 × raio de Hill de Marte (1 084 065 km); as demais dividem o resto em partes iguais de velocidade no periapse. "Cabe?" compara com o propelente dimensionado; "Queima única", "Vida" e "Partidas" comparam com os limites do motor no catálogo (— = sem fonte); "Tempo" compara a duração da sequência com a estada em Marte da missão. N = 1 é a queima única das tabelas acima.

### Captura

| Combinação | Caso | N | Perda (m/s) | Propelente (kg) | Cabe? | Maior queima (s) | Queima única máx. (s) | Queima única | Vida | Partidas | Sequência (d) | Tempo |
| :- | :- | -: | -: | -: | :- | -: | -: | :- | :- | :- | -: | :- |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 1 | 444,5 | 2 674 | **não** | 9 901 | 6 660 | **não** | sim | sim | 0,0 | sim |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 2 | 346,0 | 2 562 | **não** | 8 613 | 6 660 | **não** | sim | sim | 27,4 | sim |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 3 | 343,8 | 2 560 | **não** | 8 613 | 6 660 | **não** | sim | sim | 29,8 | sim |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 4 | 343,4 | 2 559 | **não** | 8 613 | 6 660 | **não** | sim | sim | 33,0 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 1 | 329,7 | 2 201 | sim | 8 151 | 6 660 | **não** | sim | sim | 0,0 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 2 | 231,1 | 2 075 | sim | 6 684 | 6 660 | **não** | sim | sim | 27,4 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 3 | 228,3 | 2 071 | sim | 6 684 | 6 660 | **não** | sim | sim | 29,8 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 4 | 227,8 | 2 070 | sim | 6 684 | 6 660 | **não** | sim | sim | 33,0 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 1 | 75,9 | 2 302 | sim | 1 788 | 2 000 | sim | — | sim | 0,0 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 2 | 52,8 | 2 272 | sim | 1 562 | 2 000 | sim | — | sim | 27,4 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 3 | 52,7 | 2 272 | sim | 1 562 | 2 000 | sim | — | sim | 29,8 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 4 | 52,7 | 2 272 | sim | 1 562 | 2 000 | sim | — | sim | 33,0 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 1 | 42,8 | 1 876 | sim | 1 457 | 2 000 | sim | — | sim | 0,0 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 2 | 25,7 | 1 852 | sim | 1 213 | 2 000 | sim | — | sim | 27,4 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 3 | 25,6 | 1 852 | sim | 1 213 | 2 000 | sim | — | sim | 29,8 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 4 | 25,6 | 1 851 | sim | 1 213 | 2 000 | sim | — | sim | 33,0 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 1 | 2,1 | 2 178 | sim | 252 | 1 030 | sim | sim | sim | 0,0 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 2 | 1,4 | 2 177 | sim | 222 | 1 030 | sim | sim | sim | 27,4 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 3 | 1,4 | 2 177 | sim | 222 | 1 030 | sim | sim | sim | 29,8 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 4 | 1,4 | 2 177 | sim | 222 | 1 030 | sim | sim | sim | 33,0 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 1 | 1,1 | 1 792 | sim | 207 | 1 030 | sim | sim | sim | 0,0 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 2 | 0,6 | 1 791 | sim | 174 | 1 030 | sim | sim | sim | 27,4 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 3 | 0,6 | 1 791 | sim | 174 | 1 030 | sim | sim | sim | 29,8 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 4 | 0,6 | 1 791 | sim | 174 | 1 030 | sim | sim | sim | 33,0 | sim |

### Saída de Marte

| Combinação | Caso | N | Perda (m/s) | Propelente (kg) | Cabe? | Maior queima (s) | Queima única máx. (s) | Queima única | Vida | Partidas | Sequência (d) | Tempo |
| :- | :- | -: | -: | -: | :- | -: | -: | :- | :- | :- | -: | :- |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 1 | 492,5 | 1 241 | **não** | 9 188 | 6 660 | **não** | sim | sim | 0,0 | sim |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 2 | 352,4 | 1 171 | **não** | 7 395 | 6 660 | **não** | sim | sim | 27,4 | sim |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 3 | 348,2 | 1 169 | **não** | 7 404 | 6 660 | **não** | sim | sim | 29,8 | sim |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 4 | 347,4 | 1 168 | **não** | 7 405 | 6 660 | **não** | sim | sim | 33,0 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 1 | 174,9 | 707 | sim | 5 233 | 6 660 | sim | sim | sim | 0,0 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 2 | 85,9 | 647 | sim | 3 518 | 6 660 | sim | sim | sim | 27,4 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 3 | 81,5 | 644 | sim | 3 520 | 6 660 | sim | sim | sim | 29,8 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 4 | 80,7 | 644 | sim | 3 521 | 6 660 | sim | sim | sim | 33,0 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 1 | 242,2 | 1 114 | **não** | 4 126 | 6 660 | sim | sim | sim | 0,0 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 2 | 162,4 | 1 071 | **não** | 3 341 | 6 660 | sim | sim | sim | 27,4 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 3 | 161,2 | 1 071 | **não** | 3 342 | 6 660 | sim | sim | sim | 29,8 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 4 | 160,9 | 1 071 | **não** | 3 342 | 6 660 | sim | sim | sim | 33,0 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 1 | 63,2 | 632 | sim | 2 341 | 6 660 | sim | sim | sim | 0,0 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 2 | 27,6 | 608 | sim | 1 624 | 6 660 | sim | sim | sim | 27,4 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 3 | 26,4 | 607 | sim | 1 624 | 6 660 | sim | sim | sim | 29,8 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 4 | 26,2 | 607 | sim | 1 624 | 6 660 | sim | sim | sim | 33,0 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 1 | 71,0 | 1 050 | sim | 1 631 | 2 000 | sim | — | sim | 0,0 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 2 | 43,8 | 1 034 | sim | 1 336 | 2 000 | sim | — | sim | 27,4 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 3 | 43,6 | 1 034 | sim | 1 336 | 2 000 | sim | — | sim | 29,8 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 4 | 43,5 | 1 034 | sim | 1 336 | 2 000 | sim | — | sim | 33,0 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 1 | 14,0 | 617 | sim | 959 | 2 000 | sim | — | sim | 0,0 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 2 | 5,7 | 611 | sim | 679 | 2 000 | sim | — | sim | 27,4 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 3 | 5,5 | 611 | sim | 679 | 2 000 | sim | — | sim | 29,8 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 4 | 5,4 | 611 | sim | 679 | 2 000 | sim | — | sim | 33,0 | sim |

### Sensibilidade à fração do raio de Hill (C1, caso de projeto, maior N)

| Fração | Perda (m/s) | Maior queima (s) |
| -: | -: | -: |
| 0,10 | 371,0 | 8 984 |
| 0,50 | 339,4 | 8 559 |

## Conferência de coerência com o ERO da ESA (P-043; não é verificação)

ERO: massa úmida de ~6,5 t e 1.900 kg de propelente no módulo de inserção [F22], 2 × 400 N [F29]. Admitidos (P-043): a massa úmida como massa na captura e todo o propelente do módulo na captura; assim, Δv do motor = 1 088 m/s. As fontes não publicam v∞, órbita-alvo nem Δv da captura: a tabela varre o v∞ (o último é o da missão de referência) e mostra o melhor N.

| v∞ (km/s) | Órbita-alvo | N | Δv impulsivo (m/s) | Perda (m/s) | Propelente (kg) | Fecha com 1.900 kg? | Maior queima (s) | Dentro da queima única? |
| -: | :- | -: | -: | -: | -: | :- | -: | :- |
| 2,000 | órbita de 1 sol | 4 | 618 | 57 | 1 255 | sim | 3 387 | sim |
| 2,000 | órbita alta (f_H · raio de Hill) | 1 | 421 | 57 | 915 | sim | 3 387 | sim |
| 2,250 | órbita de 1 sol | 4 | 718 | 93 | 1 477 | sim | 4 263 | sim |
| 2,250 | órbita alta (f_H · raio de Hill) | 1 | 521 | 93 | 1 151 | sim | 4 263 | sim |
| 2,500 | órbita de 1 sol | 4 | 828 | 138 | 1 718 | sim | 5 216 | sim |
| 2,500 | órbita alta (f_H · raio de Hill) | 1 | 631 | 138 | 1 408 | sim | 5 216 | sim |
| 2,750 | órbita de 1 sol | 4 | 947 | 190 | 1 971 | **não** | 6 214 | sim |
| 2,750 | órbita alta (f_H · raio de Hill) | 1 | 750 | 190 | 1 678 | sim | 6 214 | sim |
| 2,971 | órbita de 1 sol | 4 | 1 059 | 240 | 2 198 | **não** | 7 108 | **não** |
| 2,971 | órbita alta (f_H · raio de Hill) | 1 | 862 | 239 | 1 919 | **não** | 7 108 | **não** |

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
| mav_1 | M2: 4 × R-4D-11 | 1 957 | 310 | 267,8 | 2 772 | 249 | 1,97 | 7,31 | 2 000 | não |
| mav_1 | M3: 1 × R-40B | 4 003 | 296 | 267,8 | 2 772 | 119 | 4,03 | 14,95 | 500 | não |
| mav_2 | N1: 1 × S400-15 | 425 | 321 | 70,5 | 2 991 | 320 | 1,62 | 6,03 | 6 660 | não |
| mav_2 | N2: 1 × R-4D-11 | 489 | 310 | 70,5 | 2 991 | 274 | 1,87 | 6,94 | 2 000 | não |
