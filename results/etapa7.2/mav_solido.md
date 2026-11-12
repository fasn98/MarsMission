# MAV de propelente sólido para o nosso encontro (gerado por tools/mav_solido.py)

**NÃO VALIDADO.** Reabre o ADR 0007 só como dado; o ADR não muda. Escala do MAV sólido do MSR de 2019; comprimento pela P-108 revista (2026-11-12; ver a errata no fim).

## Resposta

O MAV sólido fica entre **553 e 1 645 kg** (1,4 a 4,2 vezes o do MSR de 2019), com comprimento de 3,15 a 5,71 m em Ø 0,57 m. **Não cabe deitado, nem sem deck**, em nenhum caso: a melhor folga sem deck é +0,018 m.

**A perda gravitacional do item 2 não foi aplicada ao sólido.** A simulação de subida corta a queima quando chega à energia da órbita, como um motor que desliga; o sólido não desliga, e o MSR usa queima, costa longa e queima do 2º estágio ([F57] PDF p. 2), que o modelo não tem. No lugar, há dois limites para o Δv de 100 × 100 km: o de [F37], com as perdas do caso de [F37], e o ideal, sem perdas (src/orbital/subida.py, dv_ideal). O empuxo/peso maior do sólido tende a reduzir a perda gravitacional; o arrasto, a aumentar.

## MAV sólido do MSR de 2019 (fonte)

| Grandeza | Estágio 1 | Estágio 2 |
| :- | -: | -: |
| Propelente (kg) | 216,0 | 54,4 |
| Empuxo médio (N) | 9 854 | 6 937 |
| Tempo de queima (s) | 75,9 | 24,5 |
| Isp médio (s) | 293 | 282 |

GLOM 394 kg, comprimento 2,7 m, diâmetro máximo 0,57 m ([F34] PDF p. 4; [F247] PDF p. 2; [F248] PDF p. 4). O comprimento por estágio e a densidade do propelente não são publicados.

## O nosso MAV sólido

| Grandeza | Δv de [F37], com perdas | Δv ideal, sem perdas (limite inferior) |
| :- | -: | -: |
| Δv 100 × 100 km (m/s) | 4 027,9 | 3 361,6 |
| Δv de subida com margem (km/s) | 5,772 | 5,039 |
| GLOM (kg) | 1 645,0 | 552,6 |
| Propelente, estágios 1 e 2 (kg) | 1 019,1 e 144,0 | 314,9 e 68,2 |
| Empuxo, estágios 1 e 2 (N, P-108) | 46 492 e 18 365 | 14 366 e 8 702 |
| Empuxo/peso na decolagem | 7,61 | 7,00 |
| Lander injetado (kg) | 7 246 | 4 962 |

Fração estrutural 0,286 (P-019), a do veículo inteiro de 2019.

## Comprimento e folga deitado

Limites em Ø 0,57 m: 3,184 m sem deck e 2,744 m com deck.

| Δv | Comprimento (m, P-108 revista) | Folga sem deck (m) | Folga com deck (m) |
| :- | -: | -: | -: |
| Δv de [F37], com perdas | 5,71 | −1,263 | −1,483 |
| Δv ideal, sem perdas (limite inferior) | 3,15 | +0,018 | −0,202 |

## O que o ADR 0007 disse contra o sólido, e se ainda vale

| Item | ADR 0007 | Hoje, com as fontes do MSR |
| :- | :- | :- |
| Massa pela regra (iii) | 41,3 a 41,4 t do sólido, contra 34,2 a 34,4 t do hipergólico | o ADR registra que a comparação não foi refeita com o Isp de voo de 310 s; o GLOM do sólido para o nosso Δv está na tabela de cima |
| Frio extremo | [F58] p. 4: "Potential issues with extremely cold environments" | o MSR mantém o MAV num recinto térmico: [F249] PDF p. 3: "the MAV is stored in a thermal enclosure known as the igloo"; [F35] PDF p. 9: "the vehicle exterior will be maintained at -62.5°C by the SRL igloo. Most internal components will be kept at a non-operational AFT of -40°C". O grão trincou perto de −70 °C em ensaio: [F248] PDF p. 14: "Data from the analog samples showed cracking at approximately -70 °C"; PDF p. 13: "Current qualification minimum temperatures are -50 °C". O risco segue, com mitigação de projeto, não de voo |
| Aquecimento antes do voo | não tratado no ADR | [F34] PDF p. 5: "between 2 to 12 sols to warm the SRMs to flight temperatures"; [F249] PDF p. 4: "A solid motor temperature gradient of 10 oC/hr was desirable to minimize the risk of this solid motor grain cracking", "peak power ... 288W" |
| Estocagem longa | não tratado no ADR | [F250] PDF p. 2: "concerns exist with long duration aging associated with baseline CTPB (cold temperature capable) propellant" |
| Isp menor | [F58] p. 4: "Lower ISP than liquid/hybrid counterparts" | vale: [F34] PDF p. 4 dá 293 e 282 s médios, contra o Isp de requisito do R-4D-11 de 310 s ([F107] Tab. 3) |
| Não estrangula nem desliga | [F58] p. 4: "Cannot be actively throttled or shut down" | vale igual: o corte no alvo exige outro meio (o MSR usa costa longa e um 2º estágio dimensionado para a queima) |

**Limitações:** escala linear de um único projeto; a fração estrutural de 0,286 é do veículo inteiro (P-019); sem simulação de subida própria do sólido.

## Errata (2026-11-12, decisão do Fabio)

A P-108 foi revista (aprovada como NÃO VALIDADA): o comprimento passou a ser motor do estágio 1 + motor do estágio 2, pelo ajuste dos motores do catálogo [F270], mais um resto fixo sem fonte (results/familia1/comprimento_solido.md). Antes, o comprimento não fixo escalava com o propelente, com a parte fixa de 0 a 1,5 m. Valores publicados (results/etapa7.2/mav_solido.yaml no commit 9da6251 (main, merge do PR #64)), como registro:

| Δv | Parte fixa (m, P-108 original) | Comprimento (m) | Folga sem deck (m) | Folga com deck (m) |
| :- | -: | -: | -: | -: |
| Δv de [F37], com perdas | 0,0 | 11,61 | −4,215 | −4,435 |
| Δv de [F37], com perdas | 0,5 | 9,96 | −3,390 | −3,610 |
| Δv de [F37], com perdas | 1,0 | 8,31 | −2,564 | −2,784 |
| Δv de [F37], com perdas | 1,5 | 6,66 | −1,739 | −1,959 |
| Δv ideal, sem perdas (limite inferior) | 0,0 | 3,83 | −0,321 | −0,541 |
| Δv ideal, sem perdas (limite inferior) | 0,5 | 3,62 | −0,217 | −0,437 |
| Δv ideal, sem perdas (limite inferior) | 1,0 | 3,41 | −0,112 | −0,332 |
| Δv ideal, sem perdas (limite inferior) | 1,5 | 3,20 | −0,008 | −0,228 |
