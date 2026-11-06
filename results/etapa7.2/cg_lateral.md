# CG lateral e produtos de inércia do lander (gerado por tools/cg_lateral.py)

Modelo atual (results/etapa7.2/parametros.yaml). Diâmetro da cápsula no perfil lido: 4,68 m. Nenhuma peça foi movida.

## Configuração de lançamento

Massa 3 190,4 kg; CG (0,0256; −0,0263; 3,0032) m; deslocamento radial 0,0367 m = 0,0078 do diâmetro. Produtos de inércia: Ixy −2,15, Ixz 108,36, Iyz −14,09 kg·m².

| Conjunto | Massa (kg) | m·x (kg·m) | m·y (kg·m) | Contribuição ao CG x (m) | Contribuição ao CG y (m) | Ixy, Ixz, Iyz no eixo (kg·m²) | Ixy, Ixz, Iyz no CG (kg·m²) |
| :- | -: | -: | -: | -: | -: | -: | -: |
| Estágio de cruzeiro | 158,5 | 41,87 | 0,00 | 0,0131 | 0,0000 | 0,00; 111,02; 0,00 | −0,99; 99,99; 11,31 |
| Descida (3 tanques a 120°) | 576,2 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,00; 0,00; 0,00 | 0,39; 1,72; −1,77 |
| MAV (deitado ao longo de y) | 348,1 | 0,00 | −83,77 | 0,0000 | −0,0263 | 0,00; 0,00; −14,09 | −1,91; −1,50; −12,55 |
| Braço (guardado em x = +0,45 m) | 88,5 | 39,82 | 0,00 | 0,0125 | 0,0000 | 0,00; −2,66; 0,00 | −0,99; −2,51; −0,16 |
| Helicópteros | 6,4 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,00; 0,00; 0,00 | 0,00; −0,12; 0,13 |
| Núcleo do lander | 1 748,8 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,00; 0,00; 0,00 | 1,18; 11,95; −12,25 |
| Cápsula (escudo e casca) | 264,0 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,00; 0,00; 0,00 | 0,18; −1,17; 1,20 |

Produtos na forma de tensor (−∫ x y dm). "No eixo": em torno do ponto do eixo do veículo na altura do CG, (0, 0, z do CG), e mostra quem causa a assimetria (peças no eixo ou simétricas dão zero). "No CG": em torno do CG composto, e a soma dá o tensor total; aí até peças no eixo aparecem.

## Configuração de entrada (sem o estágio de cruzeiro)

Massa 3 031,9 kg; CG (0,0131; −0,0276; 3,1452) m; deslocamento radial 0,0306 m = 0,0065 do diâmetro. Produtos de inércia: Ixy −1,10, Ixz 3,00, Iyz −25,99 kg·m².

| Conjunto | Massa (kg) | m·x (kg·m) | m·y (kg·m) | Contribuição ao CG x (m) | Contribuição ao CG y (m) | Ixy, Ixz, Iyz no eixo (kg·m²) | Ixy, Ixz, Iyz no CG (kg·m²) |
| :- | -: | -: | -: | -: | -: | -: | -: |
| Descida (3 tanques a 120°) | 576,2 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,00; 0,00; 0,00 | 0,21; −0,19; 0,40 |
| MAV (deitado ao longo de y) | 348,1 | 0,00 | −83,77 | 0,0000 | −0,0276 | 0,00; 0,00; −25,99 | −0,97; −1,42; −23,01 |
| Braço (guardado em x = +0,45 m) | 88,5 | 39,82 | 0,00 | 0,0131 | 0,0000 | 0,00; 3,00; 0,00 | −1,07; 2,91; 0,18 |
| Helicópteros | 6,4 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,00; 0,00; 0,00 | 0,00; −0,07; 0,16 |
| Núcleo do lander | 1 748,8 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,00; 0,00; 0,00 | 0,63; 2,87; −6,03 |
| Cápsula (escudo e casca) | 264,0 | 0,00 | 0,00 | 0,0000 | 0,0000 | 0,00; 0,00; 0,00 | 0,10; −1,09; 2,30 |

Produtos na forma de tensor (−∫ x y dm). "No eixo": em torno do ponto do eixo do veículo na altura do CG, (0, 0, z do CG), e mostra quem causa a assimetria (peças no eixo ou simétricas dão zero). "No CG": em torno do CG composto, e a soma dá o tensor total; aí até peças no eixo aparecem.

## Consumo dos propelentes de cruzeiro no CG (NÃO VALIDADO)

Tanques em lados opostos, a 1,50 m do eixo (P-095): MON-3 com 70,9 kg em +x e MMH com 42,9 kg em −x. Consumo na razão de mistura constante (P-080), sem lei de consumo nem controle de CG modelados.

| Propelente de cruzeiro restante | Massa (kg) | CG x (m) | CG y (m) | CG z (m) | Deslocamento radial (m) |
| -: | -: | -: | -: | -: | -: |
| 100 % | 3 190,4 | 0,0256 | −0,0263 | 3,0032 | 0,0367 |
| 75 % | 3 162,0 | 0,0225 | −0,0265 | 3,0270 | 0,0348 |
| 50 % | 3 133,5 | 0,0194 | −0,0267 | 3,0513 | 0,0330 |
| 25 % | 3 105,1 | 0,0162 | −0,0270 | 3,0761 | 0,0315 |
| 0 % | 3 076,6 | 0,0129 | −0,0272 | 3,1013 | 0,0301 |

## Referência: MSL

- O MSL voou com deslocamento radial do CG intencional, zcg/d = −0,0215 sobre dref = 4,5 m ([F226]), isto é, 0,0967 m (calculado aqui), para trimar em cerca de −16° de ângulo de ataque hipersônico e gerar sustentação para a entrada guiada ([F226]), com L/D de projeto de 0,24 ([F227], configuração de base de 2006).
- O deslocamento vinha de massas de balanço: 2 de cerca de 75 kg no cruzeiro, ejetadas para criar o deslocamento, e 6 de cerca de 25 kg ejetadas antes do paraquedas para voltar o CG ao eixo ([F214]).
- A sensibilidade da trimagem ao deslocamento do CG (graus por cm) não foi achada em texto legível nas fontes (não conferido). Para o Mars 2020, a fonte consultada (reconstrução do MEADS) não dá valores de CG; o JPL Publication 22-1 não foi obtido (não conferido).

## Achado para o portão da 7.3

Na configuração de entrada, o deslocamento radial do CG do lander é 0,0065 do diâmetro da cápsula (perfil lido), contra 0,0215 do dref no MSL: 30 % do valor do MSL (diâmetros de referência diferentes: o do perfil lido e o dref do MSL). No MSL o deslocamento era intencional, para trimar e gerar sustentação; aqui ele sai do arranjo (braço e MAV), num azimute de −65° (atan2(y, x) nos eixos do Part Studio, de +x para +y) que não foi escolhido. Não é desprezível para a trimagem e o L/D da entrada; a ordem de grandeza da trimagem não foi calculada (aerodinâmica não modelada). Nenhuma peça foi movida.

## Errata (2026-11-06, decisão do Fabio): 13 algarismos nos arquivos .fs

Nas duas tabelas por conjunto, a massa da descida era 576,1 kg e a da cápsula era 263,9 kg, com 6 algarismos. Os valores vigentes são os das tabelas acima (results/etapa7.2b/folgas.md, comparação 6 × 13 algarismos).
