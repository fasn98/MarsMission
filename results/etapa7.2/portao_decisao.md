# Portão da Etapa 7.2: dados para a decisão de aeroshell e MAV (gerado por tools/portao_7_2.py)

Esta página não escolhe. A decisão é do Fabio.

## 1. Comparação

Folga do MAV no aeroshell com a folga interna de 0,25 m (P-087) e a base em cada estação (ombro, ombro + meio deck, ombro + deck (P-094)). A massa por área do lander é comparada com 211 kg/m² do Mars 2020 (3.360 kg de entrada em 4,5 m, [F202] p. 13; calculado).

| Aeroshell | Folga no Vulcan, contorno reto entre as cotas | Folga no Vulcan, Ø menor desde o PAF | Massa por área (kg/m²) | Ø do MAV | Comprimento | Deitado, ombro | Deitado, ombro + meio deck | Deitado, ombro + deck (P-094) | Em pé, ombro | Em pé, ombro + meio deck | Em pé, ombro + deck (P-094) |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| 4,5 m (forma MSL/M2020) | +0,143 | +0,065 | 279 | 0,57 | 3,56 | −0,19 | −0,30 | −0,41 | −1,78 | −1,93 | −2,08 |
| 4,65 m (forma SRL-A) | +0,047 | −0,014 | 261 | 0,57 | 3,56 | +0,02 | −0,06 | −0,14 | −0,77 | −0,92 | −1,07 |
| 4,5 m (forma MSL/M2020) | +0,143 | +0,065 | 279 | 0,60 | 3,49 | −0,18 | −0,29 | −0,40 | −1,74 | −1,89 | −2,04 |
| 4,65 m (forma SRL-A) | +0,047 | −0,014 | 261 | 0,60 | 3,49 | +0,04 | −0,04 | −0,12 | −0,73 | −0,87 | −1,02 |
| 4,5 m (forma MSL/M2020) | +0,143 | +0,065 | 279 | 0,63 | 3,48 | −0,19 | −0,30 | −0,41 | −1,75 | −1,90 | −2,05 |
| 4,65 m (forma SRL-A) | +0,047 | −0,014 | 261 | 0,63 | 3,48 | +0,03 | −0,05 | −0,13 | −0,73 | −0,88 | −1,03 |
| 4,5 m (forma MSL/M2020) | +0,143 | +0,065 | 279 | 0,66 | 3,48 | −0,21 | −0,32 | −0,43 | −1,78 | −1,93 | −2,08 |
| 4,65 m (forma SRL-A) | +0,047 | −0,014 | 261 | 0,66 | 3,48 | +0,01 | −0,06 | −0,14 | −0,76 | −0,91 | −1,06 |
| 4,5 m (forma MSL/M2020) | +0,143 | +0,065 | 279 | 0,69 | 3,48 | −0,23 | −0,34 | −0,45 | −1,81 | −1,96 | −2,11 |
| 4,65 m (forma SRL-A) | +0,047 | −0,014 | 261 | 0,69 | 3,48 | +0,00 | −0,08 | −0,16 | −0,78 | −0,93 | −1,08 |
| 4,5 m (forma MSL/M2020) | +0,143 | +0,065 | 279 | 0,72 | 3,48 | −0,26 | −0,37 | −0,48 | −1,83 | −1,98 | −2,13 |
| 4,65 m (forma SRL-A) | +0,047 | −0,014 | 261 | 0,72 | 3,48 | −0,02 | −0,09 | −0,17 | −0,80 | −0,95 | −1,10 |
| 4,5 m (forma MSL/M2020) | +0,143 | +0,065 | 279 | 0,75 | 3,48 | −0,28 | −0,39 | −0,50 | −1,86 | −2,01 | −2,16 |
| 4,65 m (forma SRL-A) | +0,047 | −0,014 | 261 | 0,75 | 3,48 | −0,03 | −0,11 | −0,19 | −0,83 | −0,98 | −1,13 |

Duas leituras do envelope do Vulcan, [F80] Fig. 4.3.1-1 ("Simplified"), p. 4-8: a primeira interpola em linha reta entre Ø 4.877 mm e Ø 4.648 mm; a segunda usa Ø 4.648 mm desde o plano do PAF. Com a forma SRL-C, as folgas são +0,032 e −0,034 m. A massa por área usa os diâmetros nominais. Comprimentos e folgas em m; folga positiva = cabe.

## 2. Piso do comprimento do MAV

**Confirmado:** com o arranjo atual (P-085), o comprimento para de cair em 3,48 m a partir de Ø 0,61 m.

**A origem é só em parte a P-086:** 1,50 m (43 %) vêm da P-086, sem fonte. Os outros 1,98 m vêm dos tanques em série, cujo volume sai das massas de propelente e das densidades (P-078, [F211]) com a ullage da P-081, na geometria da P-085.

## 3. Opções que dependem da P-086

Para cada caso, o maior comprimento fora dos tanques que ainda caberia, contra os 1,50 m da P-086.

| Aeroshell | Orientação | Cabe hoje | Depende da P-086 | Bloqueada pelos tanques (não cabe nem com zero fora dos tanques) |
| :- | :- | -: | -: | -: |
| 4,5 m (forma MSL/M2020) | deitado | 0 | 21 | 0 |
| 4,5 m (forma MSL/M2020) | em pé | 0 | 0 | 21 |
| 4,65 m (forma SRL-A) | deitado | 4 | 17 | 0 |
| 4,65 m (forma SRL-A) | em pé | 0 | 21 | 0 |

Maior comprimento fora dos tanques que caberia (m), por estação da base:

| Aeroshell | Ø do MAV | Orientação | ombro | ombro + meio deck | ombro + deck (P-094) |
| :- | -: | :- | -: | -: | -: |
| 4,5 m (forma MSL/M2020) | 0,57 | deitado | 1,12 | 0,90 | 0,68 |
| 4,5 m (forma MSL/M2020) | 0,57 | em pé | −0,28 | −0,43 | −0,58 |
| 4,65 m (forma SRL-A) | 0,57 | deitado | 1,53 | 1,38 | 1,23 |
| 4,65 m (forma SRL-A) | 0,57 | em pé | 0,73 | 0,58 | 0,43 |
| 4,5 m (forma MSL/M2020) | 0,60 | deitado | 1,15 | 0,93 | 0,71 |
| 4,5 m (forma MSL/M2020) | 0,60 | em pé | −0,24 | −0,39 | −0,54 |
| 4,65 m (forma SRL-A) | 0,60 | deitado | 1,57 | 1,42 | 1,27 |
| 4,65 m (forma SRL-A) | 0,60 | em pé | 0,77 | 0,63 | 0,48 |
| 4,5 m (forma MSL/M2020) | 0,63 | deitado | 1,12 | 0,90 | 0,68 |
| 4,5 m (forma MSL/M2020) | 0,63 | em pé | −0,25 | −0,40 | −0,55 |
| 4,65 m (forma SRL-A) | 0,63 | deitado | 1,56 | 1,40 | 1,25 |
| 4,65 m (forma SRL-A) | 0,63 | em pé | 0,77 | 0,62 | 0,47 |
| 4,5 m (forma MSL/M2020) | 0,66 | deitado | 1,08 | 0,86 | 0,64 |
| 4,5 m (forma MSL/M2020) | 0,66 | em pé | −0,28 | −0,43 | −0,58 |
| 4,65 m (forma SRL-A) | 0,66 | deitado | 1,53 | 1,37 | 1,22 |
| 4,65 m (forma SRL-A) | 0,66 | em pé | 0,74 | 0,59 | 0,44 |
| 4,5 m (forma MSL/M2020) | 0,69 | deitado | 1,03 | 0,81 | 0,59 |
| 4,5 m (forma MSL/M2020) | 0,69 | em pé | −0,31 | −0,46 | −0,61 |
| 4,65 m (forma SRL-A) | 0,69 | deitado | 1,50 | 1,34 | 1,19 |
| 4,65 m (forma SRL-A) | 0,69 | em pé | 0,72 | 0,57 | 0,42 |
| 4,5 m (forma MSL/M2020) | 0,72 | deitado | 0,99 | 0,77 | 0,55 |
| 4,5 m (forma MSL/M2020) | 0,72 | em pé | −0,33 | −0,48 | −0,63 |
| 4,65 m (forma SRL-A) | 0,72 | deitado | 1,46 | 1,31 | 1,16 |
| 4,65 m (forma SRL-A) | 0,72 | em pé | 0,70 | 0,55 | 0,40 |
| 4,5 m (forma MSL/M2020) | 0,75 | deitado | 0,94 | 0,72 | 0,50 |
| 4,5 m (forma MSL/M2020) | 0,75 | em pé | −0,36 | −0,51 | −0,66 |
| 4,65 m (forma SRL-A) | 0,75 | deitado | 1,43 | 1,28 | 1,13 |
| 4,65 m (forma SRL-A) | 0,75 | em pé | 0,67 | 0,52 | 0,37 |

## 4. O que as fontes dizem sobre a P-086

| Item | O que foi achado | Fonte |
| :- | :- | :- |
| Divisão do comprimento de um MAV por elemento | **não achada** em nenhuma fonte primária consultada (Yaghoubi 2022, McCollum 2019, Yaghoubi e Schnell, Bowles 2013, Desai 1998): só envelopes totais e figuras sem cotas (não conferido além dessas) | [F35], [F216], [F230], [F46], [F229] |
| Única cota por elemento achada | "a length margin of 10cm on SRM1" (margem, não comprimento) | [F230] PDF p. 6 |
| Motor R-4D-11 | dimensões publicadas; ver a conta acima | [F228] PDF p. 22 |
| Interestágio | sem cota; no MSR, o bocal do 2º estágio fica dentro do interestágio ("the nested SRM2 nozzle") | [F35] PDF p. 15 |
| Carga (contêiner de amostras) | não conferido em fonte com página: a página do MSR da NASA daria cerca de 0,24 m × 0,23 m, lida só por resumo, sem cópia local | não conferido |
| Arranjo sem empilhar | MAV pressurizado de dois estágios com o 2º dentro do 1º, cerca de 1,2 m × 1,7 m; cabe em outro envelope, com outro diâmetro | [F229] PDF p. 3 |
| Conceito líquido no envelope do MSR | "Liquid propulsion vehicle found to not be feasible" | [F231] PDF p. 3 |
| Fonte que poderia resolver | desenho cotado do MAV do MSR, ou o estudo líquido de dois estágios (Trinidad et al. 2012, IEEE, não obtido; não conferido) | não conferido |

**R-4D-11, bocal 164:1 (a variante do Isp que usamos), conta a partir de [F228]:** 0,554 m de comprimento total, contra 0,60 m (estágio 1) e 0,45 m (estágio 2) da P-086; saída de Ø 0,279 m. Quatro saídas em quadrado pedem um círculo de Ø 0,675 m (conta geométrica, saídas encostadas), contra o Ø 0,57 m do ADR 0022. Bocais podem ficar fora do diâmetro do veículo ou aninhados; isso não está modelado.

**Achado à parte, sem mudança aqui:** a mesma folha dá 3,76 kg para o bocal 164:1, e o catálogo (config/motores.yaml) usa 4,31 kg, a massa do bocal 300:1, junto com o Isp do 164:1.

**Análogos publicados, só pela geometria (não são o nosso MAV):**

| MAV | Comprimento × Ø | Aeroshell | Base | Folga deitado | Fonte |
| :- | :- | :- | :- | -: | :- |
| Bowles, hipergólico pressurizado de um estágio, 393 kg | 2,74 × 0,56 | 4,5 m (forma MSL/M2020) | ombro | +0,23 | [F46] Tab. 11, p. 40 impressa: "Overall length/Diameter, m 2.74 / 0.56" |
| Bowles, hipergólico pressurizado de um estágio, 393 kg | 2,74 × 0,56 | 4,5 m (forma MSL/M2020) | ombro + deck (P-094) | +0,01 | [F46] Tab. 11, p. 40 impressa: "Overall length/Diameter, m 2.74 / 0.56" |
| Bowles, hipergólico pressurizado de um estágio, 393 kg | 2,74 × 0,56 | 4,65 m (forma SRL-A) | ombro | +0,43 | [F46] Tab. 11, p. 40 impressa: "Overall length/Diameter, m 2.74 / 0.56" |
| Bowles, hipergólico pressurizado de um estágio, 393 kg | 2,74 × 0,56 | 4,65 m (forma SRL-A) | ombro + deck (P-094) | +0,28 | [F46] Tab. 11, p. 40 impressa: "Overall length/Diameter, m 2.74 / 0.56" |
| MAV do MSR, SRC (sólido, dois estágios), limite | 2,99 × 0,50 | 4,5 m (forma MSL/M2020) | ombro | +0,15 | [F35] p. 3 |
| MAV do MSR, SRC (sólido, dois estágios), limite | 2,99 × 0,50 | 4,5 m (forma MSL/M2020) | ombro + deck (P-094) | −0,07 | [F35] p. 3 |
| MAV do MSR, SRC (sólido, dois estágios), limite | 2,99 × 0,50 | 4,65 m (forma SRL-A) | ombro | +0,34 | [F35] p. 3 |
| MAV do MSR, SRC (sólido, dois estágios), limite | 2,99 × 0,50 | 4,65 m (forma SRL-A) | ombro + deck (P-094) | +0,18 | [F35] p. 3 |

## 5. Opinião do agente (separada dos dados; não é fato nem recomendação como fato)

Opinião: com o que está calculado, nenhuma combinação com base realista cabe sem mexer na P-086 ou no arranjo dos tanques, e o que mais pesa na decisão é essa premissa sem fonte, não o diâmetro. Eu calcularia um arranjo sem tanques em série antes de escolher o aeroshell, porque alargar o MAV não o encurta. A decisão é do Fabio.
