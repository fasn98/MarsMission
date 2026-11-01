# Operação de superfície (gerado por tools/operacao_superficie.py)

## Pouso e alcance

Elipse do Mars 2020: 7,7 × 6,6 km [F187]; o TRN desvia até 600 m [F188] e pousou a 5 m do alvo escolhido [F189]; a entrega guiada ficou a 1 700 m do ponto esperado [F190]. Alcance: SRH 700 m por carga diária [F194]; Ingenuity 300 m de projeto [F196] e 705 m no maior voo [F195].

## Chegada e estação de tempestades

Chegada em 2029-09-20, Ls 189,5°. Inícios do catálogo na estação antes da chegada: 2 (tempestade possivelmente em curso na chegada: 5 %, P-061). Estada inteira: 25 %.

## Linha do tempo mínima da superfície

Ritmo real do Ingenuity [F195]: 72 voos entre os sóis 58 e 1035; intervalo entre voos: mediana 10 sóis, média 13,8, de 1 a 84.

| Distância ao depósito | Ritmo | Helicópteros em paralelo | Sóis por tubo | Busca (sóis) | Total (sóis) | Lançamento do MAV | Ls | Tempestade desde Ls 185° até o lançamento | Folga até a conjunção (dias) | Antes da conjunção? |
| -: | :- | -: | -: | -: | -: | :- | -: | -: | -: | :- |
| 200 m | SRH | 2 | 4 | 20 | 43 | 2029-11-03 | 215,8° | 10,0 % | 183,8 | sim |
| 200 m | SRH | 1 | 4 | 40 | 63 | 2029-11-23 | 228,2° | 10,0 % | 163,3 | sim |
| 200 m | Ingenuity | 2 | 20 | 100 | 123 | 2030-01-24 | 267,4° | 20,0 % | 101,6 | sim |
| 200 m | Ingenuity | 1 | 20 | 200 | 223 | 2030-05-07 | 328,9° | 25,0 % | −1,1 | **não** |
| 1 700 m | SRH | 2 | 8 | 40 | 63 | 2029-11-23 | 228,2° | 10,0 % | 163,3 | sim |
| 1 700 m | SRH | 1 | 8 | 80 | 103 | 2030-01-03 | 254,1° | 15,0 % | 122,2 | sim |
| 1 700 m | Ingenuity | 2 | 120 | 600 | 623 | 2031-06-22 | — | — | — | **não** (depois da partida do orbitador) |
| 1 700 m | Ingenuity | 1 | 120 | 1 200 | 1 223 | 2033-02-27 | — | — | — | **não** (depois da partida do orbitador) |
| 3 850 m | SRH | 2 | 14 | 70 | 93 | 2029-12-24 | 247,7° | 10,0 % | 132,4 | sim |
| 3 850 m | SRH | 1 | 14 | 140 | 163 | 2030-03-06 | 292,8° | 20,0 % | 60,5 | sim |
| 3 850 m | Ingenuity | 2 | 260 | 1 300 | 1 323 | 2033-06-10 | — | — | — | **não** (depois da partida do orbitador) |
| 3 850 m | Ingenuity | 1 | 260 | 2 600 | 2 623 | 2037-02-05 | — | — | — | **não** (depois da partida do orbitador) |

Início da conjunção (SEP ≤ 5°): 2030-05-06 (results/etapa4.3). Tempestade: fração dos inícios do catálogo entre o começo da estação (Ls 185°, inclusive os inícios antes da chegada, que estariam em curso) e o Ls do lançamento, vezes a probabilidade por ano marciano (P-061); com 10 inícios no catálogo, cada um vale 2,5 %. Datas com resolução de ±1 dia (a conjunção é amostrada dia a dia).

## Dados dos helicópteros contra a capacidade dos caminhos

Capacidade (Mbit/sol, results/etapa4.3): TGO 60 a 2 000; MRO 100 a 1 150; reserva própria (relé + DTE mínimo) 12 a 35. Lander: 250 Mbit/sol (P-063). RTE em JPEG com razão de 1,73 a 8,63 [F198] (P-076).

O volume por voo vem da Etapa 4.3; o número de voos por sol é o do ritmo de cada linha (a Etapa 4.3 usava 2 voos por sol, P-054).

| Ritmo | Volume por voo | Voos por sol | Helicópteros (Mbit/sol) | Com o lander (Mbit/sol) | TGO | MRO | reserva própria (relé + DTE mínimo) | Superfície (sóis) | Folga até a conjunção (dias) |
| :- | :- | -: | -: | -: |  :- | :- | :- | -: | -: |
| SRH, 2 helicópteros, 200 m | Navcam + RTE, sem compressão (Etapa 4.3) | 1,00 | 1 355 a 1 355 | 1 605 a 1 605 | depende | não | não | 43 | 183,8 |
| SRH, 2 helicópteros, 200 m | Navcam sem compressão + RTE em JPEG | 1,00 | 578 a 984 | 828 a 1 234 | depende | depende | não | 43 | 183,8 |
| SRH, 2 helicópteros, 200 m | (a) mais autonomia: só a RTE em JPEG (a Navcam fica a bordo) | 1,00 | 102 a 508 | 352 a 758 | depende | depende | não | 43 | 183,8 |
| (b) ritmo do Ingenuity, 2 helicópteros, 200 m | Navcam + RTE, sem compressão (Etapa 4.3) | 0,20 | 271 a 271 | 521 a 521 | depende | depende | não | 123 | 101,6 |
| (b) ritmo do Ingenuity, 2 helicópteros, 200 m | Navcam sem compressão + RTE em JPEG | 0,20 | 116 a 197 | 366 a 447 | depende | depende | não | 123 | 101,6 |
| (b) ritmo do Ingenuity, 2 helicópteros, 200 m | (a) mais autonomia: só a RTE em JPEG (a Navcam fica a bordo) | 0,20 | 20 a 102 | 270 a 352 | depende | depende | não | 123 | 101,6 |

Cobertura: "sim" quando o mínimo do caminho cobre o máximo da demanda; "depende" quando só a parte alta da faixa cobre; "não" quando nem o máximo do caminho cobre o mínimo da demanda.

### (c) Mais capacidade de comunicação

Enlace direto para 1 605 Mbit/sol num passe de 8 h (P-065): 55 717 bps, 391 vezes o análogo do MSL; HGA de 2,12 m com 100 W (P-069), cerca de 37,0 kg, 1 376 Wh por passe. Energia: área de operação 24,5 m² com esse consumo (demanda de 5 000 Wh/sol), abaixo dos 32,8 m² da linha de base. Lander injetado 4 012 → 4 087 kg; margens do lander: Falcon Heavy (recuperação) +17 % → +14 %; Falcon Heavy (descartável) +180 % → +175 %; Vulcan VC2 +8 % → +6 %; Vulcan VC4 +62 % → +59 %; Vulcan VC6 +107 % → +103 % (sensibilidade). TGO + MRO no máximo somam 3 150 Mbit/sol, sem avaliar a sobreposição dos passes.
