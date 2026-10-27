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

A 1ª queima da captura (a última da saída) leva o excesso hiperbólico numa única passagem, até uma órbita alta de apoapse = 0,100 × raio de Hill de Marte (1 084 065 km); as demais dividem o resto em partes iguais de velocidade no periapse. "Cabe?" compara com o propelente dimensionado; "Queima única", "Vida" e "Partidas" comparam com os limites do motor no catálogo (— = sem fonte); "Tempo" compara a duração da sequência com a estada em Marte da missão. N = 1 é a queima única das tabelas acima.

### Captura

| Combinação | Caso | N | Perda (m/s) | Propelente (kg) | Cabe? | Maior queima (s) | Queima única máx. (s) | Queima única | Vida | Partidas | Sequência (d) | Tempo |
| :- | :- | -: | -: | -: | :- | -: | -: | :- | :- | :- | -: | :- |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 1 | 444,5 | 2 674 | **não** | 9 901 | 6 660 | **não** | sim | sim | 0,0 | sim |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 2 | 371,9 | 2 592 | **não** | 8 984 | 6 660 | **não** | sim | sim | 4,7 | sim |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 3 | 371,2 | 2 591 | **não** | 8 984 | 6 660 | **não** | sim | sim | 6,5 | sim |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 4 | 371,0 | 2 591 | **não** | 8 984 | 6 660 | **não** | sim | sim | 8,4 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 1 | 329,7 | 2 201 | sim | 8 151 | 6 660 | **não** | sim | sim | 0,0 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 2 | 256,4 | 2 107 | sim | 7 104 | 6 660 | **não** | sim | sim | 4,7 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 3 | 255,4 | 2 106 | sim | 7 104 | 6 660 | **não** | sim | sim | 6,5 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 4 | 255,2 | 2 106 | sim | 7 104 | 6 660 | **não** | sim | sim | 8,4 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 1 | 75,9 | 2 302 | sim | 1 788 | 2 000 | sim | — | sim | 0,0 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 2 | 58,9 | 2 280 | sim | 1 626 | 2 000 | sim | — | sim | 4,7 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 3 | 58,8 | 2 280 | sim | 1 626 | 2 000 | sim | — | sim | 6,5 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 4 | 58,8 | 2 280 | sim | 1 626 | 2 000 | sim | — | sim | 8,4 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 1 | 42,8 | 1 876 | sim | 1 457 | 2 000 | sim | — | sim | 0,0 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 2 | 30,0 | 1 858 | sim | 1 283 | 2 000 | sim | — | sim | 4,7 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 3 | 29,9 | 1 858 | sim | 1 283 | 2 000 | sim | — | sim | 6,5 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 4 | 29,9 | 1 858 | sim | 1 283 | 2 000 | sim | — | sim | 8,4 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 1 | 2,1 | 2 178 | sim | 252 | 1 030 | sim | sim | sim | 0,0 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 2 | 1,6 | 2 178 | sim | 230 | 1 030 | sim | sim | sim | 4,7 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 3 | 1,6 | 2 178 | sim | 230 | 1 030 | sim | sim | sim | 6,5 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 4 | 1,6 | 2 178 | sim | 230 | 1 030 | sim | sim | sim | 8,4 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 1 | 1,1 | 1 792 | sim | 207 | 1 030 | sim | sim | sim | 0,0 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 2 | 0,7 | 1 791 | sim | 184 | 1 030 | sim | sim | sim | 4,7 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 3 | 0,7 | 1 791 | sim | 184 | 1 030 | sim | sim | sim | 6,5 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 4 | 0,7 | 1 791 | sim | 184 | 1 030 | sim | sim | sim | 8,4 | sim |

### Saída de Marte

| Combinação | Caso | N | Perda (m/s) | Propelente (kg) | Cabe? | Maior queima (s) | Queima única máx. (s) | Queima única | Vida | Partidas | Sequência (d) | Tempo |
| :- | :- | -: | -: | -: | :- | -: | -: | :- | :- | :- | -: | :- |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 1 | 492,5 | 1 241 | **não** | 9 188 | 6 660 | **não** | sim | sim | 0,0 | sim |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 2 | 386,9 | 1 188 | **não** | 7 885 | 6 660 | **não** | sim | sim | 4,7 | sim |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 3 | 385,3 | 1 188 | **não** | 7 889 | 6 660 | **não** | sim | sim | 6,5 | sim |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 4 | 385,0 | 1 187 | **não** | 7 889 | 6 660 | **não** | sim | sim | 8,4 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 1 | 174,9 | 707 | sim | 5 233 | 6 660 | sim | sim | sim | 0,0 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 2 | 104,7 | 660 | sim | 3 972 | 6 660 | sim | sim | sim | 4,7 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 3 | 103,1 | 659 | sim | 3 974 | 6 660 | sim | sim | sim | 6,5 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 4 | 102,8 | 659 | sim | 3 974 | 6 660 | sim | sim | sim | 8,4 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 1 | 242,2 | 1 114 | **não** | 4 126 | 6 660 | sim | sim | sim | 0,0 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 2 | 182,2 | 1 082 | **não** | 3 554 | 6 660 | sim | sim | sim | 4,7 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 3 | 181,8 | 1 082 | **não** | 3 554 | 6 660 | sim | sim | sim | 6,5 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 4 | 181,7 | 1 082 | **não** | 3 554 | 6 660 | sim | sim | sim | 8,4 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 1 | 63,2 | 632 | sim | 2 341 | 6 660 | sim | sim | sim | 0,0 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 2 | 35,0 | 613 | sim | 1 816 | 6 660 | sim | sim | sim | 4,7 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 3 | 34,5 | 613 | sim | 1 816 | 6 660 | sim | sim | sim | 6,5 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 4 | 34,4 | 612 | sim | 1 816 | 6 660 | sim | sim | sim | 8,4 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 1 | 71,0 | 1 050 | sim | 1 631 | 2 000 | sim | — | sim | 0,0 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 2 | 50,4 | 1 038 | sim | 1 416 | 2 000 | sim | — | sim | 4,7 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 3 | 50,3 | 1 038 | sim | 1 416 | 2 000 | sim | — | sim | 6,5 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 4 | 50,3 | 1 038 | sim | 1 416 | 2 000 | sim | — | sim | 8,4 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 1 | 14,0 | 617 | sim | 959 | 2 000 | sim | — | sim | 0,0 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 2 | 7,4 | 612 | sim | 755 | 2 000 | sim | — | sim | 4,7 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 3 | 7,3 | 612 | sim | 755 | 2 000 | sim | — | sim | 6,5 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 4 | 7,3 | 612 | sim | 755 | 2 000 | sim | — | sim | 8,4 | sim |

Natureza dos limites: S400-15, queima única qualificada de 1,85 h; vida acumulada e partidas "planned" [F105]. R-4D-11, 2000 s e 40 queimas são requisitos da missão Artemis I, não vida qualificada do motor [F107]. OMS-E, 1030 s e 10 partidas são requisitos do Orion; 15 h acumuladas, do Shuttle [F107, F108]. Captura e retorno usam estágios e motores diferentes: as vidas não se somam.

### Sensibilidade à fração do raio de Hill (caso de projeto, maior N)

Com 1/3, a perturbação solar (não modelada) muda o periapse em centenas a milhares de km por volta (estimativa da revisão independente, não conferida em fonte): fora da validade do modelo de dois corpos.

| Fração | Combinação | Perda (m/s) | Propelente (kg) | Maior queima (s) |
| -: | :- | -: | -: | -: |
| 0,100 | C1 (captura) | 371,0 | 2 591 | 8 984 |
| 0,100 | C2 (captura) | 58,8 | 2 280 | 1 626 |
| 0,100 | R3 (saída) | 50,3 | 1 038 | 1 416 |
| 0,050 | C1 (captura) | 409,8 | 2 635 | 9 480 |
| 0,050 | C2 (captura) | 67,7 | 2 291 | 1 713 |
| 0,050 | R3 (saída) | 60,7 | 1 044 | 1 529 |
| 0,333 | C1 (captura) | 343,4 | 2 559 | 8 613 |
| 0,333 | C2 (captura) | 52,7 | 2 272 | 1 562 |
| 0,333 | R3 (saída) | 43,5 | 1 034 | 1 336 |

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
