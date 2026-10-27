# Varredura da órbita de encontro, periapse 300 km (gerado por tools/varredura_encontro.py)

Apoapse de 380 a 33793 km, 120 pontos. Massa total na órbita baixa da Terra = orbitador + lander (lançamentos separados). Massas em kg.

| Versão do orbitador | Caso | Apoapse do mínimo | Massa total no mínimo | MAV no mínimo | No extremo? |
| :- | :- | -: | -: | -: | :- |
| quimico | missão A | 33 793 km | 20 571 | 280 | sim |
| quimico | regra (iii) | 33 793 km | 29 856 | 280 | sim |

**Regra de escolha (ADR 0005):** menor apoapse com total_regra_iii_kg ≤ (1 + 0.05) × mínimo. Resultado: apoapse de **26 950 km**, total de 31 142 kg pela regra (iii) (4,3 % acima do mínimo de 29 856 kg) e 21 207 kg na missão A; MAV de 271 kg.

Pontos selecionados:

| Apoapse (km) | Δv MAV | MAV (kg) | Lander | Total quimico: A / (iii) |
| -: | -: | -: | -: | -: |
| 380 | 4,169 | 130 | 6 021 | 95 607 / 856 189 |
| 514 | 4,198 | 132 | 6 035 | 88 132 / 540 398 |
| 695 | 4,236 | 135 | 6 054 | 80 016 / 365 006 |
| 939 | 4,283 | 139 | 6 080 | 71 581 / 257 470 |
| 1 270 | 4,342 | 144 | 6 112 | 63 205 / 187 512 |
| 1 718 | 4,412 | 151 | 6 153 | 55 257 / 140 240 |
| 2 322 | 4,495 | 160 | 6 204 | 48 038 / 107 485 |
| 3 140 | 4,589 | 170 | 6 266 | 41 742 / 84 403 |
| 4 246 | 4,691 | 182 | 6 339 | 36 445 / 67 953 |
| 5 742 | 4,797 | 195 | 6 423 | 32 127 / 56 142 |
| 7 764 | 4,903 | 210 | 6 514 | 28 699 / 47 623 |
| 10 498 | 5,004 | 226 | 6 609 | 26 036 / 41 460 |
| 14 194 | 5,096 | 241 | 6 705 | 24 003 / 36 992 |
| 19 193 | 5,178 | 256 | 6 796 | 22 471 / 33 748 |
| 25 952 | 5,248 | 269 | 6 879 | 21 327 / 31 388 |
| 33 793 | 5,298 | 280 | 6 944 | 20 571 / 29 856 |
