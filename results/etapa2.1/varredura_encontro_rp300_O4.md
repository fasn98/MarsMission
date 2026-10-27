# Varredura da órbita de encontro, periapse 300 km (gerado por tools/varredura_encontro.py)

Apoapse de 380 a 33793 km, 120 pontos. Massa total na órbita baixa da Terra = orbitador + lander (lançamentos separados). Massas em kg.

| Versão do orbitador | Caso | Apoapse do mínimo | Massa total no mínimo | MAV no mínimo | No extremo? |
| :- | :- | -: | -: | -: | :- |
| quimico | missão A | 33 793 km | 20 664 | 295 | sim |
| quimico | regra (iii) | 33 793 km | 29 948 | 295 | sim |

**Regra de escolha (ADR 0005):** menor apoapse com total_regra_iii_kg ≤ (1 + 0.05) × mínimo. Resultado: apoapse de **26 950 km**, total de 31 233 kg pela regra (iii) (4,3 % acima do mínimo de 29 948 kg) e 21 298 kg na missão A; MAV de 286 kg.

Pontos selecionados:

| Apoapse (km) | Δv MAV | MAV (kg) | Lander | Total quimico: A / (iii) |
| -: | -: | -: | -: | -: |
| 380 | 4,169 | 138 | 6 074 | 95 660 / 856 242 |
| 514 | 4,198 | 141 | 6 089 | 88 186 / 540 451 |
| 695 | 4,236 | 144 | 6 109 | 80 071 / 365 060 |
| 939 | 4,283 | 148 | 6 136 | 71 637 / 257 526 |
| 1 270 | 4,342 | 154 | 6 169 | 63 262 / 187 569 |
| 1 718 | 4,412 | 161 | 6 212 | 55 316 / 140 299 |
| 2 322 | 4,495 | 170 | 6 266 | 48 100 / 107 547 |
| 3 140 | 4,589 | 180 | 6 331 | 41 806 / 84 468 |
| 4 246 | 4,691 | 193 | 6 407 | 36 513 / 68 021 |
| 5 742 | 4,797 | 207 | 6 494 | 32 198 / 56 214 |
| 7 764 | 4,903 | 222 | 6 590 | 28 774 / 47 699 |
| 10 498 | 5,004 | 238 | 6 689 | 26 116 / 41 540 |
| 14 194 | 5,096 | 255 | 6 788 | 24 086 / 37 075 |
| 19 193 | 5,178 | 270 | 6 883 | 22 558 / 33 835 |
| 25 952 | 5,248 | 284 | 6 970 | 21 418 / 31 479 |
| 33 793 | 5,298 | 295 | 7 037 | 20 664 / 29 948 |
