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
| Motor R-4D-11 | dimensões publicadas; ver a seção 7 | [F228] PDF p. 22 |
| Interestágio | sem cota; no MSR, o bocal do 2º estágio fica dentro do interestágio ("the nested SRM2 nozzle") | [F35] PDF p. 15 |
| Carga (contêiner de amostras) | não conferido em fonte com página: a página do MSR da NASA daria cerca de 0,24 m × 0,23 m, lida só por resumo, sem cópia local | não conferido |
| Arranjo sem empilhar | MAV pressurizado de dois estágios com o 2º dentro do 1º, cerca de 1,2 m × 1,7 m; cabe em outro envelope, com outro diâmetro | [F229] PDF p. 3 |
| Conceito líquido no envelope do MSR | "Liquid propulsion vehicle found to not be feasible" | [F231] PDF p. 3 |
| Fonte que poderia resolver | desenho cotado do MAV do MSR, ou o estudo líquido de dois estágios (Trinidad et al. 2012, IEEE, não obtido; não conferido) | não conferido |

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

## 5. Achado: o MAV de Bowles ao lado do nosso

| Grandeza | Bowles, conceito pressurizado de 20 kg | Fonte | Nosso MAV | Origem |
| :- | :- | :- | :- | :- |
| Estágios | 1 | [F46] PDF p. 44: "resulted in a single stage-to-orbit architecture" | 2 | results/etapa2.5/arquitetura.yaml |
| Δv | 4150 m/s | [F46] Tab. 11, PDF p. 44: "ΔVTOTAL/ERV Mass 4150 / 20 kg" | 5 772 m/s, com margem | results/etapa2.5/arquitetura.yaml |
| Carga útil | 20 kg | [F46] Tab. 11, PDF p. 44: "Payload, kg (%GLOW) 20 (5.1%)" | 16 kg | [F34] p. 4 |
| Propelente | 303,88 kg, MMH/NTO; inclui reservas e partida | [F46] Tab. 11, PDF p. 44: "Propellants, kg (%GLOW) 303.88"; PDF p. 42: "includes ascent propellant, reserves and engine start-up"; PDF p. 42: "All concepts utilize storable hypergolic propellants" | 285,5 kg, MMH/MON-3 | results/etapa2.5/arquitetura.yaml |
| Motores | a fonte diverge: 3 de 1210 N na tabela; "single engine" no texto; modelo não nomeado (referência de escala: XLR-132); não conferido se os 3 são bocais de uma cabeça comum | [F46] Tab. 11, PDF p. 44: "3 / 1210 nts"; §9.1, PDF p. 42: "a pressure-feed single engine concept"; PDF p. 46: "The reference engine selected was the Rocketdyne orbital-transfer XLR-132"; PDF p. 30: "multiple expansion nozzles with a common power head" | 4 + 1 R-4D-11 | config/motores.yaml (M2, N2) |
| Razão de expansão | não achada para este conceito (não conferido) | nos outros conceitos da Tab. 11: 200 ([F46] PDF p. 43) | 164:1 no Isp; ver a seção 7 | [F107] p. 5 |
| Alimentação | pressurizada | [F46] §9.1, PDF p. 42: "a pressure-feed single engine concept was selected" | pressurizada | ADR 0007, config/mav_propulsao.yaml |
| Tanques | aninhados no estudo; não confirmado para este conceito | [F46] PDF p. 17: "a nested tank configuration was selected"; PDF p. 44: "A nested tank design was chosen to eliminate the fuel/oxidizer inter-tank section, saving weight and reducing overall vehicle length" | em série | results/etapa7.2/mav_arranjo.md |
| Dimensões e massa | 2,74 m × 0,56 m; 392,6 kg | [F46] Tab. 11, PDF p. 44: "Overall length/Diameter, m 2.74 / 0.56"; "Gross Liftoff Mass, kg 392.6" | 3,56 m × 0,57 m; 386,8 kg no orçamento, 348,1 kg no CAD | results/etapa7.2 |

**A comparação não é de veículos equivalentes:**
- o de Bowles tem um estágio, então não tem interestágio nem segundo motor, que no nosso somam parte da P-086;
- o Δv dele é menor (4150 m/s contra 5 772 m/s, e não conferimos se as margens são iguais), embora a massa de propelente seja da mesma ordem;
- os tanques do estudo dele são aninhados, para encurtar o veículo, e os nossos estão em série;
- a carga, o motor e a origem dos números também diferem, e não achamos a razão de expansão dele.

**O que os dados permitem afirmar:** existe um conceito publicado, hipergólico e pressurizado, com massa de propelente da mesma ordem e 2,74 m. **O que não permitem:** dizer que o nosso MAV caberia nesse comprimento, ou que o piso de 3,48 m está errado. O piso é o resultado do nosso arranjo (dois estágios em série e a P-086).

## 6. Achado: bocais do estágio 1 no diâmetro do MAV

Saída do R-4D-11 de bocal 164:1: 0,279 m ([F228], 11,0 pol). Menor círculo que contém n saídas, contra o Ø 0,57 m do ADR 0022:

| Saídas | Fator sobre o diâmetro de saída | Círculo mínimo (m) | Cabe em Ø do MAV? |
| -: | :- | -: | :- |
| 1 | 1 = 1,000 | 0,279 | sim |
| 2 | 2 = 2,000 | 0,559 | sim |
| 3 | 1 + 2/√3 = 2,155 | 0,602 | não |
| 4 | 1 + √2 = 2,414 | 0,675 | não |

**Conta para 4 saídas, em qualquer arranjo:** se nenhum centro está no eixo, dois centros vizinhos ficam a no máximo 90° vistos do eixo, logo a no máximo R√2 um do outro, com R o raio em que estão os centros. Eles precisam estar a pelo menos d um do outro, então R ≥ d/√2, e o círculo total é 2R + d ≥ d(1 + √2). Com um centro no eixo, os outros três ficam a pelo menos d dele, e o círculo é ≥ 3d, pior.

**Resultado: 4 bocais de saída 164:1 não cabem em Ø 0,57 m em nenhum arranjo.** O mínimo é 0,675 m, sem folga entre eles e sem parede. Na varredura, o primeiro diâmetro que os contém é 0,69 m. Com outras variantes: 0,369 m (44:1) e 0,910 m (300:1).

**Hipótese da conta:** as saídas não se sobrepõem vistas ao longo do eixo e ficam dentro do diâmetro. Saídas escalonadas no eixo, ou bocais que passem do diâmetro do corpo, não foram calculadas; o R-4D-11 de 44:1 cabe na conta, mas a folha não dá o Isp nem a massa dele.

**Como o modelo compilado (32cb41d) representa os motores:**

| Peça | Forma | Ø (m) | Comprimento (m) | Densidade equivalente (kg/m³) |
| :- | :- | -: | -: | -: |
| MAV motores do estagio 1 (4 x R-4D-11) | cilindro maciço | 0,550 | 0,60 | 120,9 |
| MAV motor do estagio 2 (1 x R-4D-11) | cilindro maciço | 0,275 | 0,45 | 161,2 |

**A peça é um volume simplificado, não os bocais reais.** O cilindro cabe no diâmetro por construção. **O modelo do Onshape esconde essa interferência**: a compilação e a conferência de massa não a mostram. As folgas do MAV no aeroshell da seção 1 também não consideram os bocais, porque usam o Ø do corpo.

**Ligação com o MSR:** a fonte cita "the small clearances of the interstage hardware and the nested SRM2 nozzle" ([F35] PDF p. 15). O bocal de um 2º estágio aninhado reduz comprimento, e o nosso motor do estágio 2 só cabe nos 0,45 m da P-086 se entrar ao menos 0,104 m em outro elemento. Isso não resolve o diâmetro: o aninhamento é no 2º estágio, e o achado é no 1º (inferência, NÃO VALIDADO; o MSR usa motor sólido).

## 7. Achado: variantes do R-4D-11 misturadas no catálogo

| Variante | Isp (s) | Massa (kg) | Comprimento total (m) | Ø de saída (m) | Fonte |
| :- | -: | -: | -: | -: | :- |
| 44:1 | não dado | não dado | 0,317 | 0,153 | [F228] PDF p. 22, desenho: "44:1 = 9.97"; "44:1 = 6.01" (sem Isp nem massa na folha) |
| 164:1 | 311,0 | 3,76 | 0,554 | 0,279 | [F228] PDF p. 22: "164:1 = 19.32"; "164:1 = 11.0"; "164:1 = 311 sec"; "164:1 = 3.76 kg (8.3 lbm)" |
| 300:1 | 315,5 | 4,31 | 0,737 | 0,377 | [F228] PDF p. 22: "300:1 = 26.5"; "300:1 = 14.84"; "300:1 = 315.5 sec"; "300:1 = 4.31 kg (9.5 lbm)" |

| Grandeza | O que o estudo usa hoje | Variante | Fonte |
| :- | :- | :- | :- |
| Isp | 310 s | 164:1 (Orion, requisito do Artemis I) | [F107] p. 6, Tab. 3; variante em p. 5 |
| Massa | 4,31 kg | 300:1, pela massa e pelo Isp de 315 s da mesma ficha ([F228]); a ficha não diz a variante | [F106] p. 3, em lb |
| Comprimento | 0,60 m (estágio 1), 0,45 m (estágio 2) | nenhuma: premissa sem fonte; o 164:1 tem 0,554 m | P-086 |
| Diâmetro de saída | não entra no modelo | — | ver a seção 6 |

**Misturas:** o Isp é do 164:1, e a massa é do 300:1. A diferença é de 0,55 kg por motor, 10,4 kg nos 19 motores escolhidos (captura 10, retorno 4, MAV 4 + 1). A massa do catálogo só entra no CAD do MAV (2,7 kg de diferença) e como coluna informativa da queima finita (results/etapa3.1). Os estágios usam fração estrutural, então a cadeia de massa não depende dela (conferido por busca no código).

**Outras diferenças:** o motor 164:1 mede 0,554 m, mais que os 0,45 m do estágio 2 e 0,046 m menos que os 0,60 m do estágio 1. O Isp do 164:1 é 310 s como requisito do Orion [F107] e 311 s na folha [F228]. Não conferido: se o 164:1 da folha é o mesmo motor "modified" do Orion [F107].

**Para decidir (Fabio), sem nenhuma troca feita:**

| Opção | Massa e Isp | Prós | Contras |
| :- | :- | :- | :- |
| (a) 164:1 em tudo | 3,76 kg [F228], 310 s [F107] | variante única, a do Isp escolhido no ADR 0011; a cadeia de massa não muda | o CAD do MAV e a coluna da queima finita mudam; pede errata |
| (b) 300:1 em tudo | 4,31 kg, 315,5 s [F228] | variante única, com mais Isp | muda o Isp e reabre o ADR 0011; bocal maior (0,910 m para 4 saídas); sem o voo no Orion |
| (c) manter e registrar a limitação | sem mudança | nenhum resultado muda | a mistura continua, pequena na massa |

## 8. Opinião do agente (separada dos dados; não é fato nem recomendação como fato)

Opinião: com o que está calculado, nenhuma combinação com base realista cabe sem mexer na P-086 ou no arranjo dos tanques, e o que mais pesa na decisão é essa premissa sem fonte, não o diâmetro. Além disso, a seção 6 pesa contra o Ø 0,57 m com quatro motores no estágio 1. Eu calcularia um arranjo sem tanques em série antes de escolher o aeroshell. A decisão é do Fabio.
