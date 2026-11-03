# CG lateral e produtos de inércia do lander (gerado por tools/cg_lateral.py)

Modelo atual (results/etapa7.2/parametros.yaml). Diâmetro da cápsula no perfil lido: 4,68 m. Nenhuma peça foi movida.

## Configuração de lançamento

Massa 3 190,4 kg; CG (0,0256; −0,0263; 3,0032) m; deslocamento radial 0,0367 m = 0,0078 do diâmetro. Produtos de inércia: Ixy −2,15, Ixz 108,36, Iyz −14,09 kg·m².

| Conjunto | Massa (kg) | m·x (kg·m) | m·y (kg·m) | Contribuição ao CG x (m) | Contribuição ao CG y (m) | Ixy | Ixz | Iyz (kg·m²) |
| :- | -: | -: | -: | -: | -: | -: | -: | -: |
| Estágio de cruzeiro | 158,5 | 41,87 | 0,00 | 0,0131 | 0,0000 | −0,99 | 99,99 | 11,31 |
| Descida (3 tanques a 120°) | 576,1 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,39 | 1,72 | −1,77 |
| MAV (deitado ao longo de y) | 348,1 | 0,00 | −83,77 | 0,0000 | −0,0263 | −1,91 | −1,50 | −12,55 |
| Braço (guardado em x = +0,45 m) | 88,5 | 39,83 | 0,00 | 0,0125 | 0,0000 | −0,99 | −2,51 | −0,16 |
| Helicópteros | 6,4 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,00 | −0,12 | 0,13 |
| Núcleo do lander | 1 748,8 | 0,00 | 0,00 | 0,0000 | 0,0000 | 1,18 | 11,95 | −12,25 |
| Cápsula (escudo e casca) | 263,9 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,18 | −1,17 | 1,20 |

## Configuração de entrada (sem o estágio de cruzeiro)

Massa 3 031,9 kg; CG (0,0131; −0,0276; 3,1452) m; deslocamento radial 0,0306 m = 0,0065 do diâmetro. Produtos de inércia: Ixy −1,10, Ixz 3,00, Iyz −25,99 kg·m².

| Conjunto | Massa (kg) | m·x (kg·m) | m·y (kg·m) | Contribuição ao CG x (m) | Contribuição ao CG y (m) | Ixy | Ixz | Iyz (kg·m²) |
| :- | -: | -: | -: | -: | -: | -: | -: | -: |
| Descida (3 tanques a 120°) | 576,1 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,21 | −0,19 | 0,40 |
| MAV (deitado ao longo de y) | 348,1 | 0,00 | −83,77 | 0,0000 | −0,0276 | −0,97 | −1,42 | −23,01 |
| Braço (guardado em x = +0,45 m) | 88,5 | 39,83 | 0,00 | 0,0131 | 0,0000 | −1,07 | 2,91 | 0,18 |
| Helicópteros | 6,4 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,00 | −0,07 | 0,16 |
| Núcleo do lander | 1 748,8 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,63 | 2,87 | −6,03 |
| Cápsula (escudo e casca) | 263,9 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,10 | −1,09 | 2,30 |

## Referência: MSL

- O MSL voou com deslocamento radial do CG intencional, zcg/d = −0,0215 sobre dref = 4,5 m ([F226]), isto é, 0,0967 m (calculado aqui), para trimar em cerca de −16° de ângulo de ataque hipersônico e gerar sustentação para a entrada guiada ([F226]), com L/D de 0,24 ([F227]).
- O deslocamento vinha de massas de balanço: 2 de cerca de 75 kg no cruzeiro, ejetadas para criar o deslocamento, e 6 de cerca de 25 kg ejetadas antes do paraquedas para voltar o CG ao eixo ([F214]).
- A sensibilidade da trimagem ao deslocamento do CG (graus por cm) não foi achada em texto legível nas fontes (não conferido); os valores do Mars 2020 também não (não conferido).

