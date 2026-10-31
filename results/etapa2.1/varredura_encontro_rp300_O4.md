# Varredura da órbita de encontro, periapse 300 km (gerado por tools/varredura_encontro.py)

Apoapse de 380 a 33793 km, 120 pontos. Massa total na órbita baixa da Terra = orbitador + lander (lançamentos separados). Massas em kg.

| Versão do orbitador | Caso | Apoapse do mínimo | Massa total no mínimo | MAV no mínimo | No extremo? |
| :- | :- | -: | -: | -: | :- |
| quimico | missão A | 33 793 km | 20 689 | 299 | sim |
| quimico | regra (iii) | 33 793 km | 29 973 | 299 | sim |

**Regra de escolha (ADR 0005):** menor apoapse com total_regra_iii_kg ≤ (1 + 0.05) × mínimo. Resultado: apoapse de **26 950 km**, total de 31 257 kg pela regra (iii) (4,3 % acima do mínimo de 29 973 kg) e 21 321 kg na missão A; MAV de 290 kg.

Pontos selecionados:

| Apoapse (km) | Δv MAV | MAV (kg) | Lander | Total quimico: A / (iii) |
| -: | -: | -: | -: | -: |
| 380 | 4,169 | 141 | 6 088 | 95 674 / 856 255 |
| 514 | 4,198 | 143 | 6 103 | 88 200 / 540 465 |
| 695 | 4,236 | 146 | 6 124 | 80 085 / 365 075 |
| 939 | 4,283 | 151 | 6 150 | 71 652 / 257 541 |
| 1 270 | 4,342 | 156 | 6 184 | 63 277 / 187 584 |
| 1 718 | 4,412 | 163 | 6 228 | 55 332 / 140 315 |
| 2 322 | 4,495 | 172 | 6 282 | 48 116 / 107 563 |
| 3 140 | 4,589 | 183 | 6 348 | 41 823 / 84 484 |
| 4 246 | 4,691 | 196 | 6 425 | 36 531 / 68 039 |
| 5 742 | 4,797 | 210 | 6 513 | 32 217 / 56 233 |
| 7 764 | 4,903 | 226 | 6 609 | 28 794 / 47 719 |
| 10 498 | 5,004 | 242 | 6 710 | 26 136 / 41 560 |
| 14 194 | 5,096 | 258 | 6 810 | 24 108 / 37 097 |
| 19 193 | 5,178 | 274 | 6 906 | 22 581 / 33 858 |
| 25 952 | 5,248 | 288 | 6 993 | 21 441 / 31 502 |
| 33 793 | 5,298 | 299 | 7 061 | 20 689 / 29 973 |
