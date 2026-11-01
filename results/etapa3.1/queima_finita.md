# Etapa 3.1 — motores reais e queima finita (gerado por tools/queima_finita.py)

Modelo: plano, dois corpos (Marte pontual), empuxo constante tangente à velocidade, vazão T/(Isp g0). Perda = Δv entregue pelo motor − Δv impulsivo no periapse. Rótulo: calculado (não verificado contra caso publicado).

O mínimo do propelente no início da queima é plano: o início, a altitude mínima durante a queima e o periapse de chegada são mal condicionados, e as apsides finais da captura carregam o resíduo do ajuste ao alvo; vão arredondados (config/queima_finita.yaml, P-041). A perda, a duração e o propelente não.

Massa no início de cada queima e propelente dimensionado: dimensionamento atual (regra iii; desde o ADR 0011, Isp dos motores escolhidos e perdas calculadas por tools/redimensiona.py; margem de Δv da P-014), sem refazer com o Isp de cada combinação. "Cabe?" compara o propelente da queima finita com o dimensionado para aquela queima; o caso de referência usa o mesmo veículo.

Perdas do DRA usadas até o redimensionamento do ADR 0011 (P-015, NÃO VALIDADA): captura 18 m/s; saída de Marte 11 m/s.

## Captura em Marte (órbita de 1 sol)

| Combinação | Empuxo (N) | Isp (s) | Caso | v∞ (km/s) | m0 (kg) | Queima (s) | Propelente (kg) | Δv impulsivo (m/s) | Perda (m/s) | Perda (% do Δv) | Perda / P-015 | Periapse de chegada (km) | Altitude mínima durante a queima (km) | Propelente dimensionado (kg) | Cabe? | Queima única máx. (s) | Excede? |
| :- | -: | -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- |
| C1: 2 × S400-15 | 850 | 321,0 | projeto (pior janela) (2031-conjuncao) | 3,484 | 7 615 | 12 594 | 3 401 | 1 344 | 518,4 | 38,6 | 28,8× | 1 747 | 479 | 3 029 | **não** | 6 660 | **sim** |
| C1: 2 × S400-15 | 850 | 321,0 | referência (2028-conjuncao) | 2,971 | 7 615 | 10 440 | 2 819 | 1 059 | 395,9 | 37,4 | 22,0× | 1 466 | 478 | 3 029 | sim | 6 660 | **sim** |
| C2: 8 × R-4D-11 | 3 914 | 310,0 | projeto (pior janela) (2031-conjuncao) | 3,484 | 7 615 | 2 242 | 2 886 | 1 344 | 104,6 | 7,8 | 5,8× | 477 | 318 | 3 029 | sim | 2 000 | **sim** |
| C2: 8 × R-4D-11 | 3 914 | 310,0 | referência (2028-conjuncao) | 2,971 | 7 615 | 1 823 | 2 348 | 1 059 | 61,1 | 5,8 | 3,4× | 391 | 299 | 3 029 | sim | 2 000 | não |
| C3: 1 × OMS-E | 26 700 | 315,1 | projeto (pior janela) (2031-conjuncao) | 3,484 | 7 615 | 311 | 2 691 | 1 344 | 3,2 | 0,2 | 0,2× | 256 | 252 | 3 029 | sim | 1 030 | não |
| C3: 1 × OMS-E | 26 700 | 315,1 | referência (2028-conjuncao) | 2,971 | 7 615 | 256 | 2 213 | 1 059 | 1,6 | 0,2 | 0,1× | 254 | 251 | 3 029 | sim | 1 030 | não |
| C4: 10 × R-4D-11 | 4 893 | 310,0 | projeto (pior janela) (2031-conjuncao) | 3,484 | 7 615 | 1 764 | 2 839 | 1 344 | 74,4 | 5,5 | 4,1× | 408 | 301 | 3 029 | sim | 2 000 | não |
| C4: 10 × R-4D-11 | 4 893 | 310,0 | referência (2028-conjuncao) | 2,971 | 7 615 | 1 438 | 2 314 | 1 059 | 41,9 | 4,0 | 2,3× | 345 | 285 | 3 029 | sim | 2 000 | não |
| C5: 12 × R-4D-11 | 5 872 | 310,0 | projeto (pior janela) (2031-conjuncao) | 3,484 | 7 615 | 1 454 | 2 809 | 1 344 | 55,3 | 4,1 | 3,1× | 365 | 289 | 3 029 | sim | 2 000 | não |
| C5: 12 × R-4D-11 | 5 872 | 310,0 | referência (2028-conjuncao) | 2,971 | 7 615 | 1 188 | 2 294 | 1 059 | 30,3 | 2,9 | 1,7× | 318 | 276 | 3 029 | sim | 2 000 | não |

## Saída de Marte (injeção trans-Terra)

| Combinação | Empuxo (N) | Isp (s) | Caso | v∞ (km/s) | Órbita inicial | m0 (kg) | Queima (s) | Propelente (kg) | Δv impulsivo (m/s) | Perda (m/s) | Perda (% do Δv) | Perda / P-015 | Propelente dimensionado (kg) | Cabe? | Queima única máx. (s) | Excede? |
| :- | -: | -: | :- | -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- |
| R1: 1 × S400-15 | 425 | 321,0 | projeto (pior janela) (2035-conjuncao) | 3,543 | órbita de 1 sol | 3 252 | 11 078 | 1 496 | 1 378 | 561,5 | 40,7 | 51,0× | 1 323 | **não** | 6 660 | **sim** |
| R1: 1 × S400-15 | 425 | 321,0 | referência (2028-conjuncao) | 2,330 | órbita de 1 sol | 3 252 | 6 364 | 859 | 753 | 213,3 | 28,3 | 19,4× | 1 323 | sim | 6 660 | não |
| R2: 2 × S400-15 | 850 | 321,0 | projeto (pior janela) (2035-conjuncao) | 3,543 | órbita de 1 sol | 3 252 | 4 958 | 1 339 | 1 378 | 292,2 | 21,2 | 26,6× | 1 323 | **não** | 6 660 | não |
| R2: 2 × S400-15 | 850 | 321,0 | referência (2028-conjuncao) | 2,330 | órbita de 1 sol | 3 252 | 2 804 | 757 | 753 | 81,8 | 10,9 | 7,4× | 1 323 | sim | 6 660 | não |
| R3: 4 × R-4D-11 | 1 957 | 310,0 | projeto (pior janela) (2035-conjuncao) | 3,543 | órbita de 1 sol | 3 252 | 1 937 | 1 247 | 1 378 | 92,4 | 6,7 | 8,4× | 1 323 | sim | 2 000 | não |
| R3: 4 × R-4D-11 | 1 957 | 310,0 | referência (2028-conjuncao) | 2,330 | órbita de 1 sol | 3 252 | 1 132 | 729 | 753 | 19,0 | 2,5 | 1,7× | 1 323 | sim | 2 000 | não |

## Várias queimas no periapse (P-042)

A 1ª queima da captura (a última da saída) leva o excesso hiperbólico numa única passagem, até uma órbita alta de apoapse = 0,100 × raio de Hill de Marte (1 084 065 km); as demais dividem o resto em partes iguais de velocidade no periapse. "Cabe?" compara com o propelente dimensionado; "Queima única", "Vida" e "Partidas" comparam com os limites do motor no catálogo (— = sem fonte); "Tempo" compara a duração da sequência com a estada em Marte da missão. N = 1 é a queima única das tabelas acima.

### Captura

| Combinação | Caso | N | Perda (m/s) | Propelente (kg) | Cabe? | Maior queima (s) | Queima única máx. (s) | Queima única | Vida | Partidas | Sequência (d) | Tempo |
| :- | :- | -: | -: | -: | :- | -: | -: | :- | :- | :- | -: | :- |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 1 | 518,4 | 3 401 | **não** | 12 594 | 6 660 | **não** | sim | sim | 0,0 | sim |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 2 | 436,1 | 3 289 | **não** | 11 433 | 6 660 | **não** | sim | sim | 4,7 | sim |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 3 | 435,0 | 3 287 | **não** | 11 433 | 6 660 | **não** | sim | sim | 6,5 | sim |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 4 | 434,8 | 3 287 | **não** | 11 433 | 6 660 | **não** | sim | sim | 8,4 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 1 | 395,9 | 2 819 | sim | 10 440 | 6 660 | **não** | sim | sim | 0,0 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 2 | 311,4 | 2 688 | sim | 9 103 | 6 660 | **não** | sim | sim | 4,7 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 3 | 309,9 | 2 686 | sim | 9 103 | 6 660 | **não** | sim | sim | 6,5 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 4 | 309,6 | 2 686 | sim | 9 103 | 6 660 | **não** | sim | sim | 8,4 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 1 | 104,6 | 2 886 | sim | 2 242 | 2 000 | **não** | — | sim | 0,0 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 2 | 82,1 | 2 851 | sim | 2 037 | 2 000 | **não** | — | sim | 4,7 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 3 | 82,0 | 2 851 | sim | 2 037 | 2 000 | **não** | — | sim | 6,5 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 4 | 82,0 | 2 851 | sim | 2 037 | 2 000 | **não** | — | sim | 8,4 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 1 | 61,1 | 2 348 | sim | 1 823 | 2 000 | sim | — | sim | 0,0 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 2 | 43,3 | 2 317 | sim | 1 602 | 2 000 | sim | — | sim | 4,7 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 3 | 43,2 | 2 317 | sim | 1 602 | 2 000 | sim | — | sim | 6,5 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 4 | 43,2 | 2 316 | sim | 1 602 | 2 000 | sim | — | sim | 8,4 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 1 | 3,2 | 2 691 | sim | 311 | 1 030 | sim | sim | sim | 0,0 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 2 | 2,4 | 2 689 | sim | 284 | 1 030 | sim | sim | sim | 4,7 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 3 | 2,4 | 2 689 | sim | 284 | 1 030 | sim | sim | sim | 6,5 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 4 | 2,4 | 2 689 | sim | 284 | 1 030 | sim | sim | sim | 8,4 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 1 | 1,6 | 2 213 | sim | 256 | 1 030 | sim | sim | sim | 0,0 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 2 | 1,1 | 2 212 | sim | 227 | 1 030 | sim | sim | sim | 4,7 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 3 | 1,1 | 2 212 | sim | 227 | 1 030 | sim | sim | sim | 6,5 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 4 | 1,1 | 2 212 | sim | 227 | 1 030 | sim | sim | sim | 8,4 | sim |
| C4: 10 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 1 | 74,4 | 2 839 | sim | 1 764 | 2 000 | sim | — | sim | 0,0 | sim |
| C4: 10 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 2 | 57,7 | 2 813 | sim | 1 605 | 2 000 | sim | — | sim | 4,7 | sim |
| C4: 10 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 3 | 57,6 | 2 813 | sim | 1 605 | 2 000 | sim | — | sim | 6,5 | sim |
| C4: 10 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 4 | 57,6 | 2 813 | sim | 1 605 | 2 000 | sim | — | sim | 8,4 | sim |
| C4: 10 × R-4D-11 | referência (2028-conjuncao) | 1 | 41,9 | 2 314 | sim | 1 438 | 2 000 | sim | — | sim | 0,0 | sim |
| C4: 10 × R-4D-11 | referência (2028-conjuncao) | 2 | 29,3 | 2 292 | sim | 1 266 | 2 000 | sim | — | sim | 4,7 | sim |
| C4: 10 × R-4D-11 | referência (2028-conjuncao) | 3 | 29,3 | 2 292 | sim | 1 266 | 2 000 | sim | — | sim | 6,5 | sim |
| C4: 10 × R-4D-11 | referência (2028-conjuncao) | 4 | 29,3 | 2 292 | sim | 1 266 | 2 000 | sim | — | sim | 8,4 | sim |
| C5: 12 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 1 | 55,3 | 2 809 | sim | 1 454 | 2 000 | sim | — | sim | 0,0 | sim |
| C5: 12 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 2 | 42,5 | 2 789 | sim | 1 324 | 2 000 | sim | — | sim | 4,7 | sim |
| C5: 12 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 3 | 42,4 | 2 789 | sim | 1 324 | 2 000 | sim | — | sim | 6,5 | sim |
| C5: 12 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 4 | 42,4 | 2 789 | sim | 1 324 | 2 000 | sim | — | sim | 8,4 | sim |
| C5: 12 × R-4D-11 | referência (2028-conjuncao) | 1 | 30,3 | 2 294 | sim | 1 188 | 2 000 | sim | — | sim | 0,0 | sim |
| C5: 12 × R-4D-11 | referência (2028-conjuncao) | 2 | 21,1 | 2 278 | sim | 1 047 | 2 000 | sim | — | sim | 4,7 | sim |
| C5: 12 × R-4D-11 | referência (2028-conjuncao) | 3 | 21,0 | 2 278 | sim | 1 047 | 2 000 | sim | — | sim | 6,5 | sim |
| C5: 12 × R-4D-11 | referência (2028-conjuncao) | 4 | 21,0 | 2 278 | sim | 1 047 | 2 000 | sim | — | sim | 8,4 | sim |

### Saída de Marte

| Combinação | Caso | N | Perda (m/s) | Propelente (kg) | Cabe? | Maior queima (s) | Queima única máx. (s) | Queima única | Vida | Partidas | Sequência (d) | Tempo |
| :- | :- | -: | -: | -: | :- | -: | -: | :- | :- | :- | -: | :- |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 1 | 561,5 | 1 496 | **não** | 11 078 | 6 660 | **não** | sim | sim | 0,0 | sim |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 2 | 444,4 | 1 429 | **não** | 9 503 | 6 660 | **não** | sim | sim | 4,7 | sim |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 3 | 442,3 | 1 428 | **não** | 9 509 | 6 660 | **não** | sim | sim | 6,5 | sim |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 4 | 441,9 | 1 428 | **não** | 9 511 | 6 660 | **não** | sim | sim | 8,4 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 1 | 213,3 | 859 | sim | 6 364 | 6 660 | sim | sim | sim | 0,0 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 2 | 130,3 | 795 | sim | 4 808 | 6 660 | sim | sim | sim | 4,7 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 3 | 128,1 | 794 | sim | 4 811 | 6 660 | sim | sim | sim | 6,5 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 4 | 127,7 | 793 | sim | 4 811 | 6 660 | sim | sim | sim | 8,4 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 1 | 292,2 | 1 339 | **não** | 4 958 | 6 660 | sim | sim | sim | 0,0 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 2 | 222,4 | 1 296 | sim | 4 266 | 6 660 | sim | sim | sim | 4,7 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 3 | 221,8 | 1 296 | sim | 4 267 | 6 660 | sim | sim | sim | 6,5 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 4 | 221,6 | 1 296 | sim | 4 267 | 6 660 | sim | sim | sim | 8,4 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 1 | 81,8 | 757 | sim | 2 804 | 6 660 | sim | sim | sim | 0,0 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 2 | 46,0 | 729 | sim | 2 165 | 6 660 | sim | sim | sim | 4,7 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 3 | 45,4 | 728 | sim | 2 165 | 6 660 | sim | sim | sim | 6,5 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 4 | 45,3 | 728 | sim | 2 165 | 6 660 | sim | sim | sim | 8,4 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 1 | 92,4 | 1 247 | sim | 1 937 | 2 000 | sim | — | sim | 0,0 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 2 | 66,3 | 1 230 | sim | 1 679 | 2 000 | sim | — | sim | 4,7 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 3 | 66,1 | 1 230 | sim | 1 679 | 2 000 | sim | — | sim | 6,5 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 4 | 66,1 | 1 230 | sim | 1 679 | 2 000 | sim | — | sim | 8,4 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 1 | 19,0 | 729 | sim | 1 132 | 2 000 | sim | — | sim | 0,0 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 2 | 10,0 | 721 | sim | 890 | 2 000 | sim | — | sim | 4,7 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 3 | 9,9 | 721 | sim | 890 | 2 000 | sim | — | sim | 6,5 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 4 | 9,9 | 721 | sim | 890 | 2 000 | sim | — | sim | 8,4 | sim |

Natureza dos limites: S400-15, queima única qualificada de 1,85 h; vida acumulada e partidas "planned" [F105]. R-4D-11, 2000 s e 40 queimas são requisitos da missão Artemis I, não vida qualificada do motor [F107]. OMS-E, 1030 s e 10 partidas são requisitos do Orion; 15 h acumuladas, do Shuttle [F107, F108]. Captura e retorno usam estágios e motores diferentes: as vidas não se somam.

### Sensibilidade à fração do raio de Hill (caso de projeto, maior N)

Com 1/3, a perturbação solar (não modelada) muda o periapse em centenas a milhares de km por volta (estimativa da revisão independente, não conferida em fonte): fora da validade do modelo de dois corpos.

| Fração | Combinação | Perda (m/s) | Propelente (kg) | Maior queima (s) |
| -: | :- | -: | -: | -: |
| 0,100 | C1 (captura) | 434,8 | 3 287 | 11 433 |
| 0,100 | C2 (captura) | 82,0 | 2 851 | 2 037 |
| 0,100 | R3 (saída) | 66,1 | 1 230 | 1 679 |
| 0,050 | C1 (captura) | 478,9 | 3 347 | 12 061 |
| 0,050 | C2 (captura) | 93,8 | 2 870 | 2 147 |
| 0,050 | R3 (saída) | 79,4 | 1 238 | 1 815 |
| 0,333 | C1 (captura) | 403,4 | 3 244 | 10 964 |
| 0,333 | C2 (captura) | 73,8 | 2 838 | 1 956 |
| 0,333 | R3 (saída) | 57,4 | 1 224 | 1 584 |

## Conferência de coerência com o ERO da ESA (P-043; não é verificação)

ERO: massa úmida de ~6,5 t [F22] ou massa de lançamento de 7,2 t [F29]; 1.900 kg de propelente no módulo de inserção [F22]; 2 × 400 N [F29]. Admitidos (P-043): essa massa na captura, todo o propelente do módulo na captura, o motor como S400-15 e o periapse da órbita de 1 sol. Δv do motor com todo o propelente: 1 088 m/s com 6 500 kg; 964 m/s com 7 200 kg. As fontes não publicam v∞, órbita-alvo nem Δv da captura: a tabela varre o v∞ (o último é o da missão de referência) e mostra o melhor N.

| Massa (kg) | v∞ (km/s) | Órbita-alvo | N | Δv impulsivo (m/s) | Perda (m/s) | Propelente (kg) | Fecha com 1.900 kg? | Maior queima (s) | Dentro da queima única? |
| -: | -: | :- | -: | -: | -: | -: | :- | -: | :- |
| 6 500 | 2,000 | órbita de 1 sol | 4 | 618 | 76 | 1 286 | sim | 3 871 | sim |
| 6 500 | 2,000 | órbita alta (f_H · raio de Hill) | 1 | 476 | 76 | 1 045 | sim | 3 871 | sim |
| 6 500 | 2,250 | órbita de 1 sol | 4 | 718 | 116 | 1 513 | sim | 4 750 | sim |
| 6 500 | 2,250 | órbita alta (f_H · raio de Hill) | 1 | 576 | 116 | 1 283 | sim | 4 750 | sim |
| 6 500 | 2,500 | órbita de 1 sol | 4 | 828 | 164 | 1 757 | sim | 5 696 | sim |
| 6 500 | 2,500 | órbita alta (f_H · raio de Hill) | 1 | 686 | 164 | 1 538 | sim | 5 696 | sim |
| 6 500 | 2,750 | órbita de 1 sol | 4 | 947 | 218 | 2 011 | **não** | 6 679 | **não** |
| 6 500 | 2,750 | órbita alta (f_H · raio de Hill) | 1 | 805 | 218 | 1 803 | sim | 6 679 | **não** |
| 6 500 | 2,971 | órbita de 1 sol | 4 | 1 059 | 268 | 2 237 | **não** | 7 554 | **não** |
| 6 500 | 2,971 | órbita alta (f_H · raio de Hill) | 1 | 917 | 268 | 2 040 | **não** | 7 554 | **não** |
| 7 200 | 2,000 | órbita de 1 sol | 4 | 618 | 88 | 1 446 | sim | 4 370 | sim |
| 7 200 | 2,000 | órbita alta (f_H · raio de Hill) | 1 | 476 | 88 | 1 180 | sim | 4 370 | sim |
| 7 200 | 2,250 | órbita de 1 sol | 4 | 718 | 132 | 1 704 | sim | 5 370 | sim |
| 7 200 | 2,250 | órbita alta (f_H · raio de Hill) | 1 | 576 | 132 | 1 450 | sim | 5 370 | sim |
| 7 200 | 2,500 | órbita de 1 sol | 4 | 828 | 184 | 1 980 | **não** | 6 439 | sim |
| 7 200 | 2,500 | órbita alta (f_H · raio de Hill) | 1 | 686 | 184 | 1 739 | sim | 6 439 | sim |
| 7 200 | 2,750 | órbita de 1 sol | 4 | 947 | 242 | 2 265 | **não** | 7 543 | **não** |
| 7 200 | 2,750 | órbita alta (f_H · raio de Hill) | 1 | 805 | 241 | 2 037 | **não** | 7 543 | **não** |
| 7 200 | 2,971 | órbita de 1 sol | 4 | 1 059 | 295 | 2 517 | **não** | 8 521 | **não** |
| 7 200 | 2,971 | órbita alta (f_H · raio de Hill) | 1 | 917 | 294 | 2 301 | **não** | 8 521 | **não** |

## Cruzeiro do lander (todas as correções da ida, somadas)

Perda de queima finita não calculada: Δv pequeno, longe de qualquer planeta.

| Combinação | Empuxo (N) | Isp (s) | m0 (kg) | Δv total (m/s) | Tempo total de queima (s) | Queima única máx. (s) |
| :- | -: | -: | -: | -: | -: | -: |
| Z1: 4 × 10N | 40 | 292 | 4 615 | 71,5 | 8 147 | 28 800 |
| Z2: 8 × 10N | 80 | 292 | 4 615 | 71,5 | 4 073 | 28 800 |

## MAV (dois estágios)

Empuxo/peso na superfície de Marte, g = 3,713 m/s². Perda de subida já incluída no Δv (Etapa 2.1); não recalculada. O dimensionamento usa Isp de 343 s (Bowles et al. 2013, motor com turbobomba). O estágio 2 acende em voo: o empuxo/peso dele em Marte é só referência.

| Estágio | Combinação | Empuxo (N) | Isp (s) | m0 (kg) | Δv (m/s) | Queima (s) | Empuxo/peso em Marte | Aceleração inicial (m/s²) | Queima única máx. (s) | Excede? |
| :- | :- | -: | -: | -: | -: | -: | -: | -: | -: | :- |
| mav_1 | M1: 2 × R-42 | 1 779 | 305 | 386,8 | 2 777 | 393 | 1,24 | 4,60 | 3 940 | não |
| mav_1 | M2: 4 × R-4D-11 | 1 957 | 310 | 386,8 | 2 777 | 360 | 1,36 | 5,06 | 2 000 | não |
| mav_1 | M3: 1 × R-40B | 4 003 | 296 | 386,8 | 2 777 | 173 | 2,79 | 10,35 | 500 | não |
| mav_2 | N1: 1 × S400-15 | 425 | 321 | 86,0 | 2 996 | 391 | 1,33 | 4,94 | 6 660 | não |
| mav_2 | N2: 1 × R-4D-11 | 489 | 310 | 86,0 | 2 996 | 335 | 1,53 | 5,69 | 2 000 | não |
