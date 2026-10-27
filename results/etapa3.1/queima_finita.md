# Etapa 3.1 — motores reais e queima finita (gerado por tools/queima_finita.py)

Modelo: plano, dois corpos (Marte pontual), empuxo constante tangente à velocidade, vazão T/(Isp g0). Perda = Δv entregue pelo motor − Δv impulsivo no periapse. Rótulo: calculado (não verificado contra caso publicado).

O mínimo do propelente no início da queima é plano: o início, a altitude mínima durante a queima e o periapse de chegada são mal condicionados, e as apsides finais da captura carregam o resíduo do ajuste ao alvo; vão arredondados (config/queima_finita.yaml, P-041). A perda, a duração e o propelente não.

Massa no início de cada queima e propelente dimensionado: dimensionamento atual (regra iii; desde o ADR 0011, Isp dos motores escolhidos e perdas calculadas por tools/redimensiona.py; margem de Δv da P-014), sem refazer com o Isp de cada combinação. "Cabe?" compara o propelente da queima finita com o dimensionado para aquela queima; o caso de referência usa o mesmo veículo.

Perdas do DRA usadas até o redimensionamento do ADR 0011 (P-015, NÃO VALIDADA): captura 18 m/s; saída de Marte 11 m/s.

## Captura em Marte (órbita de 1 sol)

| Combinação | Empuxo (N) | Isp (s) | Caso | v∞ (km/s) | m0 (kg) | Queima (s) | Propelente (kg) | Δv impulsivo (m/s) | Perda (m/s) | Perda (% do Δv) | Perda / P-015 | Periapse de chegada (km) | Altitude mínima durante a queima (km) | Propelente dimensionado (kg) | Cabe? | Queima única máx. (s) | Excede? |
| :- | -: | -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- |
| C1: 2 × S400-15 | 850 | 321,0 | projeto (pior janela) (2031-conjuncao) | 3,484 | 7 038 | 11 510 | 3 108 | 1 344 | 490,3 | 36,5 | 27,2× | 1 639 | 470 | 2 822 | **não** | 6 660 | **sim** |
| C1: 2 × S400-15 | 850 | 321,0 | referência (2028-conjuncao) | 2,971 | 7 038 | 9 516 | 2 569 | 1 059 | 370,6 | 35,0 | 20,6× | 1 365 | 467 | 2 822 | sim | 6 660 | **sim** |
| C2: 8 × R-4D-11 | 3 914 | 310,0 | projeto (pior janela) (2031-conjuncao) | 3,484 | 7 038 | 2 059 | 2 651 | 1 344 | 93,1 | 6,9 | 5,2× | 450 | 311 | 2 822 | sim | 2 000 | **sim** |
| C2: 8 × R-4D-11 | 3 914 | 310,0 | referência (2028-conjuncao) | 2,971 | 7 038 | 1 676 | 2 158 | 1 059 | 53,6 | 5,1 | 3,0× | 373 | 294 | 2 822 | sim | 2 000 | não |
| C3: 1 × OMS-E | 26 700 | 315,1 | projeto (pior janela) (2031-conjuncao) | 3,484 | 7 038 | 288 | 2 486 | 1 344 | 2,8 | 0,2 | 0,2× | 256 | 252 | 2 822 | sim | 1 030 | não |
| C3: 1 × OMS-E | 26 700 | 315,1 | referência (2028-conjuncao) | 2,971 | 7 038 | 237 | 2 045 | 1 059 | 1,4 | 0,1 | 0,1× | 253 | 251 | 2 822 | sim | 1 030 | não |

## Saída de Marte (injeção trans-Terra)

| Combinação | Empuxo (N) | Isp (s) | Caso | v∞ (km/s) | Órbita inicial | m0 (kg) | Queima (s) | Propelente (kg) | Δv impulsivo (m/s) | Perda (m/s) | Perda (% do Δv) | Perda / P-015 | Propelente dimensionado (kg) | Cabe? | Queima única máx. (s) | Excede? |
| :- | -: | -: | :- | -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- |
| R1: 1 × S400-15 | 425 | 321,0 | projeto (pior janela) (2035-conjuncao) | 3,543 | órbita de 1 sol | 2 959 | 9 927 | 1 340 | 1 378 | 520,7 | 37,8 | 47,3× | 1 198 | **não** | 6 660 | **sim** |
| R1: 1 × S400-15 | 425 | 321,0 | referência (2028-conjuncao) | 2,330 | órbita de 1 sol | 2 959 | 5 672 | 766 | 753 | 190,2 | 25,3 | 17,3× | 1 198 | sim | 6 660 | não |
| R2: 2 × S400-15 | 850 | 321,0 | projeto (pior janela) (2035-conjuncao) | 3,543 | órbita de 1 sol | 2 959 | 4 451 | 1 202 | 1 378 | 262,2 | 19,0 | 23,8× | 1 198 | **não** | 6 660 | não |
| R2: 2 × S400-15 | 850 | 321,0 | referência (2028-conjuncao) | 2,330 | órbita de 1 sol | 2 959 | 2 521 | 681 | 753 | 70,5 | 9,4 | 6,4× | 1 198 | sim | 6 660 | não |
| R3: 4 × R-4D-11 | 1 957 | 310,0 | projeto (pior janela) (2035-conjuncao) | 3,543 | órbita de 1 sol | 2 959 | 1 750 | 1 127 | 1 378 | 79,3 | 5,8 | 7,2× | 1 198 | sim | 2 000 | não |
| R3: 4 × R-4D-11 | 1 957 | 310,0 | referência (2028-conjuncao) | 2,330 | órbita de 1 sol | 2 959 | 1 027 | 661 | 753 | 15,9 | 2,1 | 1,4× | 1 198 | sim | 2 000 | não |

## Várias queimas no periapse (P-042)

A 1ª queima da captura (a última da saída) leva o excesso hiperbólico numa única passagem, até uma órbita alta de apoapse = 0,100 × raio de Hill de Marte (1 084 065 km); as demais dividem o resto em partes iguais de velocidade no periapse. "Cabe?" compara com o propelente dimensionado; "Queima única", "Vida" e "Partidas" comparam com os limites do motor no catálogo (— = sem fonte); "Tempo" compara a duração da sequência com a estada em Marte da missão. N = 1 é a queima única das tabelas acima.

### Captura

| Combinação | Caso | N | Perda (m/s) | Propelente (kg) | Cabe? | Maior queima (s) | Queima única máx. (s) | Queima única | Vida | Partidas | Sequência (d) | Tempo |
| :- | :- | -: | -: | -: | :- | -: | -: | :- | :- | :- | -: | :- |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 1 | 490,3 | 3 108 | **não** | 11 510 | 6 660 | **não** | sim | sim | 0,0 | sim |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 2 | 411,7 | 3 008 | **não** | 10 447 | 6 660 | **não** | sim | sim | 4,7 | sim |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 3 | 410,7 | 3 007 | **não** | 10 447 | 6 660 | **não** | sim | sim | 6,5 | sim |
| C1: 2 × S400-15 | projeto (pior janela) (2031-conjuncao) | 4 | 410,5 | 3 007 | **não** | 10 447 | 6 660 | **não** | sim | sim | 8,4 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 1 | 370,6 | 2 569 | sim | 9 516 | 6 660 | **não** | sim | sim | 0,0 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 2 | 290,2 | 2 454 | sim | 8 295 | 6 660 | **não** | sim | sim | 4,7 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 3 | 288,9 | 2 452 | sim | 8 295 | 6 660 | **não** | sim | sim | 6,5 | sim |
| C1: 2 × S400-15 | referência (2028-conjuncao) | 4 | 288,7 | 2 452 | sim | 8 295 | 6 660 | **não** | sim | sim | 8,4 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 1 | 93,1 | 2 651 | sim | 2 059 | 2 000 | **não** | — | sim | 0,0 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 2 | 72,7 | 2 621 | sim | 1 872 | 2 000 | sim | — | sim | 4,7 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 3 | 72,6 | 2 621 | sim | 1 872 | 2 000 | sim | — | sim | 6,5 | sim |
| C2: 8 × R-4D-11 | projeto (pior janela) (2031-conjuncao) | 4 | 72,6 | 2 621 | sim | 1 872 | 2 000 | sim | — | sim | 8,4 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 1 | 53,6 | 2 158 | sim | 1 676 | 2 000 | sim | — | sim | 0,0 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 2 | 37,8 | 2 132 | sim | 1 474 | 2 000 | sim | — | sim | 4,7 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 3 | 37,7 | 2 132 | sim | 1 474 | 2 000 | sim | — | sim | 6,5 | sim |
| C2: 8 × R-4D-11 | referência (2028-conjuncao) | 4 | 37,7 | 2 132 | sim | 1 474 | 2 000 | sim | — | sim | 8,4 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 1 | 2,8 | 2 486 | sim | 288 | 1 030 | sim | sim | sim | 0,0 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 2 | 2,1 | 2 485 | sim | 263 | 1 030 | sim | sim | sim | 4,7 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 3 | 2,1 | 2 485 | sim | 263 | 1 030 | sim | sim | sim | 6,5 | sim |
| C3: 1 × OMS-E | projeto (pior janela) (2031-conjuncao) | 4 | 2,1 | 2 485 | sim | 263 | 1 030 | sim | sim | sim | 8,4 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 1 | 1,4 | 2 045 | sim | 237 | 1 030 | sim | sim | sim | 0,0 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 2 | 0,9 | 2 044 | sim | 209 | 1 030 | sim | sim | sim | 4,7 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 3 | 0,9 | 2 044 | sim | 209 | 1 030 | sim | sim | sim | 6,5 | sim |
| C3: 1 × OMS-E | referência (2028-conjuncao) | 4 | 0,9 | 2 044 | sim | 209 | 1 030 | sim | sim | sim | 8,4 | sim |

### Saída de Marte

| Combinação | Caso | N | Perda (m/s) | Propelente (kg) | Cabe? | Maior queima (s) | Queima única máx. (s) | Queima única | Vida | Partidas | Sequência (d) | Tempo |
| :- | :- | -: | -: | -: | :- | -: | -: | :- | :- | :- | -: | :- |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 1 | 520,7 | 1 340 | **não** | 9 927 | 6 660 | **não** | sim | sim | 0,0 | sim |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 2 | 410,3 | 1 283 | **não** | 8 518 | 6 660 | **não** | sim | sim | 4,7 | sim |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 3 | 408,5 | 1 282 | **não** | 8 522 | 6 660 | **não** | sim | sim | 6,5 | sim |
| R1: 1 × S400-15 | projeto (pior janela) (2035-conjuncao) | 4 | 408,2 | 1 281 | **não** | 8 523 | 6 660 | **não** | sim | sim | 8,4 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 1 | 190,2 | 766 | sim | 5 672 | 6 660 | sim | sim | sim | 0,0 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 2 | 114,8 | 713 | sim | 4 297 | 6 660 | sim | sim | sim | 4,7 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 3 | 113,0 | 711 | sim | 4 299 | 6 660 | sim | sim | sim | 6,5 | sim |
| R1: 1 × S400-15 | referência (2028-conjuncao) | 4 | 112,6 | 711 | sim | 4 299 | 6 660 | sim | sim | sim | 8,4 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 1 | 262,2 | 1 202 | **não** | 4 451 | 6 660 | sim | sim | sim | 0,0 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 2 | 198,2 | 1 166 | sim | 3 832 | 6 660 | sim | sim | sim | 4,7 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 3 | 197,7 | 1 165 | sim | 3 832 | 6 660 | sim | sim | sim | 6,5 | sim |
| R2: 2 × S400-15 | projeto (pior janela) (2035-conjuncao) | 4 | 197,6 | 1 165 | sim | 3 832 | 6 660 | sim | sim | sim | 8,4 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 1 | 70,5 | 681 | sim | 2 521 | 6 660 | sim | sim | sim | 0,0 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 2 | 39,2 | 658 | sim | 1 952 | 6 660 | sim | sim | sim | 4,7 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 3 | 38,7 | 658 | sim | 1 952 | 6 660 | sim | sim | sim | 6,5 | sim |
| R2: 2 × S400-15 | referência (2028-conjuncao) | 4 | 38,6 | 658 | sim | 1 952 | 6 660 | sim | sim | sim | 8,4 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 1 | 79,3 | 1 127 | sim | 1 750 | 2 000 | sim | — | sim | 0,0 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 2 | 56,5 | 1 113 | sim | 1 519 | 2 000 | sim | — | sim | 4,7 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 3 | 56,4 | 1 113 | sim | 1 519 | 2 000 | sim | — | sim | 6,5 | sim |
| R3: 4 × R-4D-11 | projeto (pior janela) (2035-conjuncao) | 4 | 56,4 | 1 113 | sim | 1 519 | 2 000 | sim | — | sim | 8,4 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 1 | 15,9 | 661 | sim | 1 027 | 2 000 | sim | — | sim | 0,0 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 2 | 8,4 | 655 | sim | 808 | 2 000 | sim | — | sim | 4,7 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 3 | 8,3 | 655 | sim | 808 | 2 000 | sim | — | sim | 6,5 | sim |
| R3: 4 × R-4D-11 | referência (2028-conjuncao) | 4 | 8,3 | 655 | sim | 808 | 2 000 | sim | — | sim | 8,4 | sim |

Natureza dos limites: S400-15, queima única qualificada de 1,85 h; vida acumulada e partidas "planned" [F105]. R-4D-11, 2000 s e 40 queimas são requisitos da missão Artemis I, não vida qualificada do motor [F107]. OMS-E, 1030 s e 10 partidas são requisitos do Orion; 15 h acumuladas, do Shuttle [F107, F108]. Captura e retorno usam estágios e motores diferentes: as vidas não se somam.

### Sensibilidade à fração do raio de Hill (caso de projeto, maior N)

Com 1/3, a perturbação solar (não modelada) muda o periapse em centenas a milhares de km por volta (estimativa da revisão independente, não conferida em fonte): fora da validade do modelo de dois corpos.

| Fração | Combinação | Perda (m/s) | Propelente (kg) | Maior queima (s) |
| -: | :- | -: | -: | -: |
| 0,100 | C1 (captura) | 410,5 | 3 007 | 10 447 |
| 0,100 | C2 (captura) | 72,6 | 2 621 | 1 872 |
| 0,100 | R3 (saída) | 56,4 | 1 113 | 1 519 |
| 0,050 | C1 (captura) | 452,6 | 3 061 | 11 021 |
| 0,050 | C2 (captura) | 83,3 | 2 637 | 1 972 |
| 0,050 | R3 (saída) | 67,9 | 1 120 | 1 641 |
| 0,333 | C1 (captura) | 380,6 | 2 968 | 10 017 |
| 0,333 | C2 (captura) | 65,3 | 2 611 | 1 797 |
| 0,333 | R3 (saída) | 48,9 | 1 109 | 1 433 |

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
| Z1: 4 × 10N | 40 | 292 | 4 066 | 71,5 | 7 178 | 28 800 |
| Z2: 8 × 10N | 80 | 292 | 4 066 | 71,5 | 3 589 | 28 800 |

## MAV (dois estágios)

Empuxo/peso na superfície de Marte, g = 3,713 m/s². Perda de subida já incluída no Δv (Etapa 2.1); não recalculada. O dimensionamento usa Isp de 343 s (Bowles et al. 2013, motor com turbobomba). O estágio 2 acende em voo: o empuxo/peso dele em Marte é só referência.

| Estágio | Combinação | Empuxo (N) | Isp (s) | m0 (kg) | Δv (m/s) | Queima (s) | Empuxo/peso em Marte | Aceleração inicial (m/s²) | Queima única máx. (s) | Excede? |
| :- | :- | -: | -: | -: | -: | -: | -: | -: | -: | :- |
| mav_1 | M1: 2 × R-42 | 1 779 | 305 | 417,7 | 2 772 | 424 | 1,15 | 4,26 | 3 940 | não |
| mav_1 | M2: 4 × R-4D-11 | 1 957 | 310 | 417,7 | 2 772 | 388 | 1,26 | 4,69 | 2 000 | não |
| mav_1 | M3: 1 × R-40B | 4 003 | 296 | 417,7 | 2 772 | 186 | 2,58 | 9,59 | 500 | não |
| mav_2 | N1: 1 × S400-15 | 425 | 321 | 89,8 | 2 991 | 408 | 1,28 | 4,73 | 6 660 | não |
| mav_2 | N2: 1 × R-4D-11 | 489 | 310 | 89,8 | 2 991 | 349 | 1,47 | 5,45 | 2 000 | não |
