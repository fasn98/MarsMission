# Piso de ruído da subida (gerado por tools/ruido_subida.py)

**Diagnóstico (P-116, NÃO VALIDADA); não muda nenhum resultado.**

## Sólido (`voa_solido`), MAV do MSR na divisão de base, guiamento da verificação

Rugosidade: desvio rms do ajuste quadrático da órbita final em 21 passos de 1,0e-04 s na antecedência e de 1,0e-07 rad em θ0 (maior entre periapse e apoapse).

| Integrador | rtol | atol | Passo máx. queima / costa (s) | Erro contra a referência, periapse / apoapse (m) | Rugosidade na antecedência (m) | Rugosidade em θ0 (m) | Tempo por voo (s) |
| :- | -: | -: | -: | -: | -: | -: | -: |
| atual | 1,0e-09 | 1,0e-06 | 1,00 / 5,00 | 1,0e+00 / 4,2e-02 | 2,0e-01 | 5,4e-01 | 0,012 |
| a | 1,0e-10 | 1,0e-07 | 0,50 / 2,50 | 1,2e-01 / 9,9e-03 | 1,4e-01 | 5,2e-01 | 0,022 |
| b | 1,0e-11 | 1,0e-08 | 0,25 / 1,00 | 3,9e-03 / 7,7e-04 | 1,3e-01 | 5,3e-01 | 0,046 |
| c | 1,0e-12 | 1,0e-09 | 0,10 / 0,50 | 1,5e-05 / 1,5e-05 | 1,3e-01 | 5,3e-01 | 0,094 |

## Sólido: menor custo do ajuste, P-111 a 380 km (tolerância da P-110: 1,0e-06, ~14 m)

| Escala | Custo, apses, atual | Erro da órbita (m), apses, atual | Fecha? apses, atual | Tempo (s), apses, atual | Custo, suave, atual | Erro da órbita (m), suave, atual | Fecha? suave, atual | Tempo (s), suave, atual |
| -: | -: | -: | :- | -: | -: | -: | :- | -: |
| 0,97 | 3,8e-06 | 27,7 | não | 19 | 5,4e-20 | 0,0 | sim | 4 |
| 0,98 | 3,7e-09 | 0,9 | sim | 29 | 3,3e-23 | 0,0 | sim | 3 |
| 0,99 | 8,9e-05 | 133,4 | não | 27 | 2,7e-21 | 0,0 | sim | 2 |
| 1,00 | 1,3e-08 | 1,6 | sim | 27 | 1,6e-21 | 0,0 | sim | 2 |
| 1,02 | 3,9e-04 | 280,5 | não | 16 | 2,7e-25 | 0,0 | sim | 2 |
| 1,03 | 6,3e-05 | 112,5 | não | 16 | 4,3e-25 | 0,0 | sim | 2 |

## Reprodutibilidade da escala mínima do sólido (P-117), P-111

| Encontro (km) | Variante | Escala | GLOM (kg) | Custo | Costa (s) | Semieixo na maior escala que não fecha (km) | Tempo (s) |
| -: | :- | -: | -: | -: | -: | -: | -: |
| 380 | atual | 0,969336 | 382,409 | 3,1e-20 | 512,049 | 380,0 | 56 |
| 380 | rtol e atol × 0,5 | 0,969336 | 382,409 | 1,2e-19 | 512,049 | 380,0 | 53 |
| 380 | rtol e atol × 2,0 | 0,969336 | 382,409 | 2,0e-25 | 512,048 | 380,0 | 58 |
| 380 | carga útil × (1 + 1,0e-13) | 0,969336 | 382,409 | 5,3e-21 | 512,049 | 380,0 | 54 |

## Hipergólico (`voa`), veículo de referência da subida, guiamento ótimo do integrador atual (tolerâncias da P-107: 1,0 m e 0,1 m/s)

| Integrador | rtol | atol | Passo máx. (s) | Erro contra a referência: altitude (m) / v radial (m/s) / Δv (m/s) | Rugosidade em θ0: altitude (m) / v radial (m/s) / Δv (m/s) | Tempo por voo (s) |
| :- | -: | -: | -: | -: | -: | -: |
| atual | 1,0e-08 | 1,0e-06 | 2,00 | 6,3e-03 / 1,8e-03 / 2,1e-03 | 2,0e-09 / 1,6e-11 / 1,6e-11 | 0,009 |
| a | 1,0e-10 | 1,0e-08 | 1,00 | 2,5e-04 / 2,3e-05 / 2,7e-05 | 2,4e-04 / 1,3e-05 / 1,5e-05 | 0,016 |
| b | 1,0e-11 | 1,0e-09 | 0,50 | 1,1e-04 / 5,7e-07 / 1,4e-07 | 4,8e-05 / 1,6e-06 / 1,7e-06 | 0,029 |
| c | 1,0e-12 | 1,0e-10 | 0,25 | 6,3e-06 / 1,4e-07 / 1,4e-07 | 4,5e-06 / 1,6e-07 / 1,8e-07 | 0,053 |
