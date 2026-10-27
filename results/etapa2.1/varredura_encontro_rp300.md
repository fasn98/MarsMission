# Varredura da órbita de encontro, periapse 300 km (gerado por tools/varredura_encontro.py)

Apoapse de 380 a 33793 km, 120 pontos. Massa total na órbita baixa da Terra = orbitador + lander (lançamentos separados). Massas em kg.

| Versão do orbitador | Caso | Apoapse do mínimo | Massa total no mínimo | MAV no mínimo | No extremo? |
| :- | :- | -: | -: | -: | :- |
| quimico | missão A | 20 697 km | 29 677 | 1 484 | não |
| quimico | regra (iii) | 33 793 km | 39 398 | 1 833 | sim |

**Regra de escolha (ADR 0005):** menor apoapse com total_regra_iii_kg ≤ (1 + 0.05) × mínimo. Resultado: apoapse de **18 483 km**, total de 41 168 kg pela regra (iii) (4,5 % acima do mínimo de 39 398 kg) e 29 709 kg na missão A; MAV de 1 404 kg.

Pontos selecionados:

| Apoapse (km) | Δv MAV | MAV (kg) | Lander | Total quimico: A / (iii) |
| -: | -: | -: | -: | -: |
| 380 | 4,169 | 334 | 7 279 | 96 866 / 857 447 |
| 514 | 4,198 | 346 | 7 348 | 89 445 / 541 710 |
| 695 | 4,236 | 361 | 7 441 | 81 402 / 366 392 |
| 939 | 4,283 | 381 | 7 566 | 73 067 / 258 956 |
| 1 270 | 4,342 | 408 | 7 734 | 64 827 / 189 133 |
| 1 718 | 4,412 | 445 | 7 959 | 57 063 / 142 045 |
| 2 322 | 4,495 | 494 | 8 258 | 50 092 / 109 539 |
| 3 140 | 4,589 | 558 | 8 653 | 44 129 / 86 790 |
| 4 246 | 4,691 | 642 | 9 168 | 39 273 / 70 781 |
| 5 742 | 4,797 | 749 | 9 825 | 35 529 / 59 545 |
| 7 764 | 4,903 | 882 | 10 642 | 32 827 / 51 752 |
| 10 498 | 5,004 | 1 042 | 11 625 | 31 052 / 46 476 |
| 14 194 | 5,096 | 1 227 | 12 762 | 30 060 / 43 049 |
| 19 193 | 5,178 | 1 431 | 14 016 | 29 691 / 40 968 |
| 25 952 | 5,248 | 1 645 | 15 333 | 29 781 / 39 842 |
| 33 793 | 5,298 | 1 833 | 16 486 | 30 113 / 39 398 |
