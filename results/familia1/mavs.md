# Família 1: dois MAVs para o encontro em órbita baixa (gerado por tools/mav_familia1.py)

**NÃO VALIDADO.** Premissas P-108, P-110 e as do PR #55 (P-104 a P-107).

## Verificação do modelo do sólido com o MAV do MSR de 2019

Massas, empuxos e Isp publicados ([F34] PDF p. 4; [F249] PDF p. 5); alvo de 350 km ([F34] PDF p. 4). A divisão do inerte entre os estágios não é publicada: varrida (P-110).

| Fração do inerte no estágio 2 | Inertes (kg) | Chega à órbita | Costa (s) |
| -: | -: | :- | -: |
| 0,30 | 75,3 e 32,3 | não | — |
| 0,34 | 71,0 e 36,6 | não | — |
| 0,38 | 66,7 e 40,9 | sim | 483 |
| 0,40 | 64,6 e 43,0 | sim | 488 |
| 0,42 | 62,4 e 45,2 | não | — |
| 0,46 | 58,1 e 49,5 | não | — |
| 0,50 | 53,8 e 53,8 | não | — |

**Base: fração 0,40** (o meio das que chegam). Costa de 488 s, contra 446 s publicados ([F34] PDF p. 7): o tempo de costa não foi ajustado e é a conferência independente. É uma conferência parcial, não uma verificação completa, porque a divisão do inerte foi escolhida para fechar.

## Comparação lado a lado

| Grandeza | Sólido, 380 km, sem margem (o menor que chega) | Sólido, 380 km, com a margem da P-014 na capacidade | Sólido, 814 km | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | Hipergólico 4 × 164:1, 380 km, sem margem | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | Hipergólico 4 × 164:1, 814 km, sem margem |
| :- | -: | -: | -: | -: | -: | -: | -: |
| Fecha | sim | sim | não | sim | sim | sim | sim |
| Δv (m/s) | 4 087 (capacidade ideal) | 4 496 (capacidade ideal) | — | 4 553 (de projeto) | 4 139 (de projeto) | 4 715 (de projeto) | 4 287 (de projeto) |
| GLOM (kg) | 392,3 | 1 332,1 | — | 161,0 | 124,4 | 178,9 | 136,2 |
| Empuxo/peso na decolagem | 6,73 | 6,94 | — | 3,27 | 4,24 | 2,95 | 3,87 |
| Comprimento (m) | 2,69 a 2,69 | 5,68 a 9,40 | — | 3,059 | 2,935 | 3,111 | 2,978 |
| Folga deitado sem deck (m) | +0,245 a +0,248 | −3,108 a −1,247 | — | −0,047 | +0,014 | −0,074 | −0,007 |
| Folga deitado com deck (m) | +0,025 a +0,028 | −3,328 a −1,467 | — | −0,267 | −0,206 | −0,294 | −0,227 |
| Massa por área (kg/m²) | 278 | 394 | — | 249 | 245 | 252 | 246 |
| Dias na superfície | 285 | 285 | — | 285 | 285 | 301 | 301 |
| Temperatura mantida (°C) | −40 | −40 | — | 15 | 15 | 15 | 15 |
| Aquecimento (W) | 17,0 | 39,1 | — | 32,5 | 26,8 | 35,2 | 28,7 |
| Energia na superfície (kWh) | 116 | 268 | — | 222 | 183 | 254 | 207 |
| RHUs equivalentes | 19 (de 43 no inventário) | 44 (de 43 no inventário) | — | 37 (de 43 no inventário) | 30 (de 43 no inventário) | 40 (de 43 no inventário) | 32 (de 43 no inventário) |

Alvo de folga: +0,05 m. Limites deitado: sólido em Ø 0,57 m, 3,184 m sem deck e 2,744 m com deck; hipergólico em Ø 0,72 m, 2,964 m e 2,524 m. O comprimento do sólido varia com a parte fixa da P-108.

**A margem no sólido:** com o inerte proporcional ao propelente (P-110), o sólido está perto da assíntota da equação do foguete: somar a margem de 10 % da P-014 à capacidade multiplica a escala do veículo. Por isso a tabela mostra o sólido sem e com margem, e o hipergólico também.

**Como cada Δv foi obtido:** o sólido é dimensionado pela simulação da subida (queima até esgotar, costa e 2º estágio) até a circular de encontro, e a margem da P-014 entra sobre a capacidade ideal; o hipergólico usa o Δv de 100 × 100 km da simulação do PR #55 com o empuxo/peso dele, mais a transferência e o déficit de rotação, com a margem da P-014. A massa por área do sólido troca no lander o GLOM do hipergólico pelo do sólido, dividido pela razão pousada/entrada (P-018); a energia do aquecimento e o seu hardware não entram nessa troca.

## Térmico e estocagem

O aquecimento segue o modelo da Etapa 4.2 (P-027, [F57]): a potência escala com a diferença de temperatura até o ambiente do igloo e com a massa de propelente elevada a 2/3. O sólido fica no mínimo fora de operação de [F57]; o hipergólico, a 15 °C (P-027). Os RHUs são o número de unidades de [F155] que dariam a mesma potência.

**Envelhecimento do propelente sólido, nas fontes:**
- [F263] PDF p. 1: "The test plan includes propellant aging first at high vacuum conditions, representative of the Mars transit, followed by an additional year at simulated Mars surface conditions."
- [F263] PDF p. 2: "The project has also completed the first of three phases of propellant aging"
- [F263] PDF p. 1: "the flight heritage is limited and outside the environments, the MAV must endure"
- [F250] PDF p. 2: "concerns exist with long duration aging associated with baseline CTPB (cold temperature capable) propellant"
- [F248] PDF p. 3: "The SRL is expected to keep the MAV between -40 °C and +40 °C, enabling the use of propellant that has already been qualified for that temperature range."
- [F248] PDF p. 13: "Current qualification minimum temperatures are -50 °C"; PDF p. 14: "Data from the analog samples showed cracking at approximately -70 °C"

**Tempo do MAV em Marte no MSR, para comparar:**
- [F266] (slides do IAC-19) PDF p. 3: "MAV dwell time in SRL on Mars ~9 months"
- [F35] PDF p. 1: "After residing on the surface for another year"
