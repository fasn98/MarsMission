# Operação de superfície (gerado por tools/operacao_superficie.py)

## Pouso e alcance

Elipse do Mars 2020: 7,7 × 6,6 km [F187]; o TRN desvia até 600 m [F188] e pousou a 5 m do alvo escolhido [F189]; a entrega guiada ficou a 1 700 m do ponto esperado [F190]. Alcance: SRH 700 m por carga diária [F194]; Ingenuity 300 m de projeto [F196] e 705 m no maior voo [F195].

## Chegada e estação de tempestades

Chegada em 2029-09-20, Ls 189,5°. Inícios do catálogo na estação antes da chegada: 2 (tempestade possivelmente em curso na chegada: 5 %, P-061). Estada inteira: 25 %.

## Linha do tempo mínima da superfície

Ritmo real do Ingenuity [F195]: 72 voos entre os sóis 58 e 1035; intervalo entre voos: mediana 10 sóis, média 13,8, de 1 a 84.

| Distância ao depósito | Ritmo | Helicópteros em paralelo | Sóis por tubo | Busca (sóis) | Total (sóis) | Lançamento do MAV | Ls | Tempestade até o lançamento | Folga até a conjunção (dias) | Antes da conjunção? |
| -: | :- | -: | -: | -: | -: | :- | -: | -: | -: | :- |
| 200 m | SRH | 2 | 4 | 20 | 43 | 2029-11-03 | 215,8° | 10,0 % | 184 | sim |
| 200 m | SRH | 1 | 4 | 40 | 63 | 2029-11-23 | 228,2° | 10,0 % | 164 | sim |
| 200 m | Ingenuity | 2 | 20 | 100 | 123 | 2030-01-24 | 267,4° | 20,0 % | 102 | sim |
| 200 m | Ingenuity | 1 | 20 | 200 | 223 | 2030-05-07 | 328,9° | 25,0 % | -1 | **não** |
| 1 700 m | SRH | 2 | 8 | 40 | 63 | 2029-11-23 | 228,2° | 10,0 % | 164 | sim |
| 1 700 m | SRH | 1 | 8 | 80 | 103 | 2030-01-03 | 254,1° | 15,0 % | 123 | sim |
| 1 700 m | Ingenuity | 2 | 120 | 600 | 623 | 2031-06-22 | 163,3° | 25,0 % | -412 | **não** |
| 1 700 m | Ingenuity | 1 | 120 | 1 200 | 1 223 | 2033-02-27 | 127,5° | 25,0 % | -1028 | **não** |
| 3 850 m | SRH | 2 | 14 | 70 | 93 | 2029-12-24 | 247,7° | 10,0 % | 133 | sim |
| 3 850 m | SRH | 1 | 14 | 140 | 163 | 2030-03-06 | 292,8° | 20,0 % | 61 | sim |
| 3 850 m | Ingenuity | 2 | 260 | 1 300 | 1 323 | 2033-06-10 | 180,9° | 25,0 % | -1131 | **não** |
| 3 850 m | Ingenuity | 1 | 260 | 2 600 | 2 623 | 2037-02-05 | 160,1° | 25,0 % | -2467 | **não** |

Início da conjunção (SEP ≤ 5°): 2030-05-06 (results/etapa4.3). Tempestade: fração dos inícios do catálogo entre o começo da estação e o Ls do lançamento, vezes a probabilidade por ano marciano (P-061).

## Dados dos helicópteros contra a capacidade dos caminhos

Capacidade (Mbit/sol, results/etapa4.3): TGO 60 a 2 000; MRO 100 a 1 150; reserva própria (relé + DTE mínimo) 12 a 35. Lander: 250 Mbit/sol (P-063). RTE em JPEG com razão de 1,73 a 8,63 [F198] (P-076).

| Ritmo | Volume por voo | Voos por sol | Helicópteros (Mbit/sol) | Com o lander (Mbit/sol) | Superfície (sóis) | Folga até a conjunção (dias) |
| :- | :- | -: | -: | -: | -: | -: |
| SRH, 2 helicópteros, 200 m | Navcam + RTE, sem compressão (Etapa 4.3) | 1,00 | 1 355 a 1 355 | 1 605 a 1 605 | 43 | 184 |
| SRH, 2 helicópteros, 200 m | Navcam sem compressão + RTE em JPEG | 1,00 | 578 a 984 | 828 a 1 234 | 43 | 184 |
| SRH, 2 helicópteros, 200 m | (a) mais autonomia: só a RTE em JPEG (a Navcam fica a bordo) | 1,00 | 102 a 508 | 352 a 758 | 43 | 184 |
| (b) ritmo do Ingenuity, 2 helicópteros, 200 m | Navcam + RTE, sem compressão (Etapa 4.3) | 0,20 | 271 a 271 | 521 a 521 | 123 | 102 |
| (b) ritmo do Ingenuity, 2 helicópteros, 200 m | Navcam sem compressão + RTE em JPEG | 0,20 | 116 a 197 | 366 a 447 | 123 | 102 |
| (b) ritmo do Ingenuity, 2 helicópteros, 200 m | (a) mais autonomia: só a RTE em JPEG (a Navcam fica a bordo) | 0,20 | 20 a 102 | 270 a 352 | 123 | 102 |

### (c) Mais capacidade de comunicação

Enlace direto para 1 605 Mbit/sol num passe de 8 h (P-065): 55 717 bps, 391 vezes o análogo do MSL; HGA de 2,12 m com 100 W (P-069), cerca de 37,0 kg, 1 376 Wh por passe. Lander injetado 4 012 → 4 087 kg; margens do lander: Falcon Heavy (recuperação) +17 % → +14 %; Falcon Heavy (descartável) +180 % → +175 %; Vulcan VC2 +8 % → +6 %; Vulcan VC4 +62 % → +59 %; Vulcan VC6 +107 % → +103 % (sensibilidade). TGO + MRO no máximo somam 3 150 Mbit/sol, sem avaliar a sobreposição dos passes.
