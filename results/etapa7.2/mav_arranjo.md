# MAV na cápsula: deitado e em pé, por diâmetro (gerado por tools/mav_arranjo.py)

Mesmo propelente; comprimento pelos segmentos da Etapa 7.1 (P-085, P-086); folga interna de 0,25 m (P-087); altura do deck 0,30 m (P-094). Folga positiva = cabe. Comprimentos e folgas em m.

## Comprimento e massa dos tanques

| Diâmetro | Comprimento | Massa dos tanques (kg) | Variação sobre o diâmetro de 0,57 m (kg) |
| -: | -: | -: | -: |
| 0,57 | 3,56 | 19,9 | 0,0 |
| 0,60 | 3,49 | 19,8 | −0,1 |
| 0,63 | 3,48 | 19,8 | −0,1 |
| 0,66 | 3,48 | 19,8 | −0,1 |
| 0,69 | 3,48 | 19,8 | −0,1 |
| 0,72 | 3,48 | 19,8 | −0,1 |
| 0,75 | 3,48 | 19,8 | −0,1 |

**Por que o comprimento para de cair:** a partir de Ø 0,61 m, os quatro tanques (oxidante e combustível de cada estágio, em série) já cabem em esferas menores que o diâmetro interno; daí em diante o comprimento é a soma dessas esferas mais os 1,50 m fora dos tanques (P-086). Alargar o MAV só encurta mais com outro arranjo de tanques (lado a lado, antepara comum ou toroidal), que o modelo da P-085 não inclui. As esferas menores que o diâmetro interno são uma extensão da P-085.

**Massa:** cascas dos tanques em Ti-6Al-4V ([F219]) com a espessura da P-093, sem dimensionamento por pressão; a casca externa e a estrutura do MAV (que crescem com o diâmetro) não estão modeladas. O orçamento do MAV (386,8 kg, fração estrutural do ADR 0007) não depende do diâmetro.

## MSL/M2020 (Ø 4,52 m no perfil lido)

| Diâmetro | Comprimento | Deitado, base no ombro | Deitado, base no ombro + meio deck | Deitado, base no ombro + deck (P-094) | Em pé, base no ombro | Em pé, base no ombro + meio deck | Em pé, base no ombro + deck (P-094) |
| -: | -: | -: | -: | -: | -: | -: | -: |
| 0,57 | 3,56 | −0,19 | −0,30 | −0,41 | −1,78 (disp. 1,78) | −1,93 (disp. 1,63) | −2,08 (disp. 1,48) |
| 0,60 | 3,49 | −0,18 | −0,29 | −0,40 | −1,74 (disp. 1,75) | −1,89 (disp. 1,60) | −2,04 (disp. 1,45) |
| 0,63 | 3,48 | −0,19 | −0,30 | −0,41 | −1,75 (disp. 1,73) | −1,90 (disp. 1,58) | −2,05 (disp. 1,43) |
| 0,66 | 3,48 | −0,21 | −0,32 | −0,43 | −1,78 (disp. 1,70) | −1,93 (disp. 1,55) | −2,08 (disp. 1,40) |
| 0,69 | 3,48 | −0,23 | −0,34 | −0,45 | −1,81 (disp. 1,67) | −1,96 (disp. 1,52) | −2,11 (disp. 1,37) |
| 0,72 | 3,48 | −0,26 | −0,37 | −0,48 | −1,83 (disp. 1,64) | −1,98 (disp. 1,49) | −2,13 (disp. 1,34) |
| 0,75 | 3,48 | −0,28 | −0,39 | −0,50 | −1,86 (disp. 1,61) | −2,01 (disp. 1,47) | −2,16 (disp. 1,32) |

## SRL-A (Ø 4,68 m no perfil lido)

| Diâmetro | Comprimento | Deitado, base no ombro | Deitado, base no ombro + meio deck | Deitado, base no ombro + deck (P-094) | Em pé, base no ombro | Em pé, base no ombro + meio deck | Em pé, base no ombro + deck (P-094) |
| -: | -: | -: | -: | -: | -: | -: | -: |
| 0,57 | 3,56 | 0,02 | −0,06 | −0,14 | −0,77 (disp. 2,79) | −0,92 (disp. 2,64) | −1,07 (disp. 2,49) |
| 0,60 | 3,49 | 0,04 | −0,04 | −0,12 | −0,73 (disp. 2,77) | −0,87 (disp. 2,62) | −1,02 (disp. 2,47) |
| 0,63 | 3,48 | 0,03 | −0,05 | −0,13 | −0,73 (disp. 2,74) | −0,88 (disp. 2,59) | −1,03 (disp. 2,44) |
| 0,66 | 3,48 | 0,01 | −0,06 | −0,14 | −0,76 (disp. 2,72) | −0,91 (disp. 2,57) | −1,06 (disp. 2,42) |
| 0,69 | 3,48 | 0,00 | −0,08 | −0,16 | −0,78 (disp. 2,70) | −0,93 (disp. 2,55) | −1,08 (disp. 2,40) |
| 0,72 | 3,48 | −0,02 | −0,09 | −0,17 | −0,80 (disp. 2,67) | −0,95 (disp. 2,52) | −1,10 (disp. 2,37) |
| 0,75 | 3,48 | −0,03 | −0,11 | −0,19 | −0,83 (disp. 2,65) | −0,98 (disp. 2,50) | −1,13 (disp. 2,35) |

Faixa de diâmetros: pedido do Fabio no portão da 7.2 (0,57 a 0,75 m); estações da base derivadas do ombro do perfil e da altura do deck (P-094), como a varredura de estações da Etapa 7.1.
Estações da base (distância ao nariz): ombro = 0,85 m; ombro + meio deck = 1,00 m; ombro + deck (P-094) = 1,15 m.
Em pé: comprimento disponível da base até onde o raio interno (raio − folga) fica igual ao raio do MAV; a folga é esse comprimento menos o do MAV.
