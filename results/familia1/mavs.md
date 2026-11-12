# Família 1: dois MAVs para o encontro em órbita baixa (gerado por tools/mav_familia1.py)

**NÃO VALIDADO.** Premissas P-014, P-018, P-019, P-027, P-104 a P-108, P-110, P-111 e P-117.

## Verificação do modelo do sólido com o MAV do MSR de 2019

Propelente, Isp, tempos de queima e empuxos médios publicados ([F34] PDF p. 4; [F249] PDF p. 5); alvo de 350 km ([F34] PDF p. 4). **Os dados publicados não fecham entre si:** empuxo médio × tempo de queima é maior que propelente × Isp × g0. A base usa o tempo de queima publicado e tira o empuxo dele; a alternativa usa o empuxo publicado e tira o tempo (P-111). A divisão do inerte entre os estágios não é publicada: varrida (P-110).

| Modelo de empuxo | Empuxos (N) | Fração do inerte no estágio 2 | Inertes (kg) | Chega à órbita | Queimas (s) | Costa (s) |
| :- | -: | -: | -: | :- | -: | -: |
| tempo publicado | 8 177 e 6 140 | 0,30 | 75,3 e 32,3 | não | — | — |
| tempo publicado | 8 177 e 6 140 | 0,34 | 71,0 e 36,6 | não | — | — |
| tempo publicado | 8 177 e 6 140 | 0,38 | 66,7 e 40,9 | sim | 75,9 e 24,5 | 475 |
| tempo publicado | 8 177 e 6 140 | 0,40 | 64,6 e 43,0 | sim | 75,9 e 24,5 | 481 |
| tempo publicado | 8 177 e 6 140 | 0,42 | 62,4 e 45,2 | sim | 75,9 e 24,5 | 487 |
| tempo publicado | 8 177 e 6 140 | 0,46 | 58,1 e 49,5 | não | — | — |
| tempo publicado | 8 177 e 6 140 | 0,50 | 53,8 e 53,8 | não | — | — |
| empuxo publicado | 9 854 e 6 937 | 0,30 | 75,3 e 32,3 | não | — | — |
| empuxo publicado | 9 854 e 6 937 | 0,34 | 71,0 e 36,6 | não | — | — |
| empuxo publicado | 9 854 e 6 937 | 0,38 | 66,7 e 40,9 | sim | 63,0 e 21,7 | 483 |
| empuxo publicado | 9 854 e 6 937 | 0,40 | 64,6 e 43,0 | sim | 63,0 e 21,7 | 488 |
| empuxo publicado | 9 854 e 6 937 | 0,42 | 62,4 e 45,2 | sim | 63,0 e 21,7 | 494 |
| empuxo publicado | 9 854 e 6 937 | 0,46 | 58,1 e 49,5 | não | — | — |
| empuxo publicado | 9 854 e 6 937 | 0,50 | 53,8 e 53,8 | não | — | — |

**Base: tempo de queima publicado, fração 0,40** (escolhida entre as que chegam, P-110). Costa de 481 s, contra 446 s publicados ([F34] PDF p. 7). O tempo de costa não foi ajustado, mas não há critério de aceitação definido para ele, e a divisão do inerte foi escolhida para fechar, com três parâmetros de guiamento para três resíduos (semieixo e vetor excentricidade; até 2026-11-11, dois: periapse e apoapse): **o modelo não fica verificado**; é uma conferência parcial.

## Comparação lado a lado

| Grandeza | Sólido, 380 km, sem margem (o menor que chega) | Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | Sólido, 814 km | Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | Hipergólico 4 × 164:1, 380 km, sem margem | Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | Hipergólico 4 × 164:1, 814 km, sem margem |
| :- | -: | -: | -: | -: | -: | -: | -: |
| Fecha | sim | não simulado | não | sim | sim | sim | sim |
| Δv (m/s) | 4 073 (capacidade ideal) | 4 481 (capacidade ideal) | — | 4 553 (de projeto) | 4 139 (de projeto) | 4 715 (de projeto) | 4 287 (de projeto) |
| GLOM (kg) | 382,3 | 1 234,2 | — | 161,0 | 124,4 | 178,9 | 136,2 |
| Empuxo/peso na decolagem | 5,58 | 5,75 | — | 3,27 | 4,24 | 2,95 | 3,87 |
| Comprimento (m) | 2,62 a 2,66 | 5,37 a 8,70 | — | 3,059 | 2,935 | 3,111 | 2,978 |
| Folga deitado sem deck (m) | +0,260 a +0,284 | −2,759 a −1,092 | — | −0,047 | +0,014 | −0,074 | −0,007 |
| Folga deitado com deck (m) | +0,040 a +0,064 | −2,979 a −1,312 | — | −0,267 | −0,206 | −0,294 | −0,227 |
| Massa por área (kg/m²) | 277 | 382 | — | 249 | 245 | 252 | 246 |
| Dias na superfície | 285 | 285 | — | 285 | 285 | 301 | 301 |
| Temperatura mantida (°C) | −40 | −40 | — | 15 | 15 | 15 | 15 |
| Aquecimento (W) | 16,7 | 37,2 | — | 32,5 | 26,8 | 35,2 | 28,7 |
| Energia na superfície (kWh) | 114 | 254 | — | 222 | 183 | 254 | 207 |
| RHUs equivalentes | 23 de 0,74 W em 2030 | 51 de 0,74 W em 2030 | — | 44 de 0,74 W em 2030 | 37 de 0,74 W em 2030 | 48 de 0,74 W em 2030 | 39 de 0,74 W em 2030 |

Alvo de folga: +0,05 m. Limites deitado: sólido em Ø 0,57 m, 3,184 m sem deck e 2,744 m com deck; hipergólico em Ø 0,72 m, 2,964 m e 2,524 m. O comprimento do sólido varia com a parte fixa da P-108.

**A margem no sólido:** com o inerte de cada estágio proporcional ao propelente (P-111), o sólido está perto da assíntota da equação do foguete: somar a margem de 10 % da P-014 à capacidade multiplica a escala do veículo. Essa coluna não foi simulada: um sólido sem corte com capacidade sobrando precisa de gestão de energia para chegar à circular. Com a fração 0,286 da P-019, o resultado seria outro. Por isso a tabela mostra o sólido sem e com margem, e o hipergólico também.

**Sólido a 814 km:** nenhuma escala da varredura (P-110) leva à circular, com a proporção de propelente entre estágios do MSR e o 2º estágio na horizontal. Causa provável, não demonstrada: a limitação do método. Não é uma conclusão sobre o sólido.

**Hipergólico:** Ø 0,72 m é o menor da grade de diâmetros que contém as quatro saídas com parede (results/etapa7.2/bocais_alternativas.md); o mínimo contínuo é menor. A versão sem margem tira a margem só do MAV: o Δv de 100 × 100 km é o do veículo com margem (empuxo/peso menor, conservador), e a massa de entrada desconta só a diferença do GLOM, sem a da energia de aquecimento. Os números diferem dos da rota B (results/etapa7.2/rotas_mav.md) porque aqui entra a perda gravitacional do PR #55, e porque a rota B usou 2 × 164:1 em Ø 0,60 m.

**Como cada Δv foi obtido:** o sólido é dimensionado pela simulação da subida (queima até esgotar, costa e 2º estágio) até a circular de encontro, e a margem da P-014 entra sobre a capacidade ideal; o hipergólico usa o Δv de 100 × 100 km da simulação do PR #55 com o empuxo/peso dele, mais a transferência e o déficit de rotação, com a margem da P-014. A massa por área do sólido troca no lander o GLOM do hipergólico pelo do sólido, dividido pela razão pousada/entrada (P-018); a energia do aquecimento e o seu hardware não entram nessa troca.

## Térmico e estocagem

O aquecimento segue o modelo da Etapa 4.2 (P-027, [F57]): a potência escala com a diferença de temperatura até o ambiente do igloo e com a massa de propelente elevada a 2/3. O sólido fica no mínimo fora de operação de [F57]; o hipergólico, a 15 °C (P-027). Os RHUs são o número de unidades de [F155] que dariam a mesma potência no ano do lançamento do MAV, com a potência de 2014 caindo 0,01 W por ano. Para comparar: [F155] p. 2 registra um teto de 43 RHUs oferecido a um edital do New Frontiers, não o tamanho do inventário.

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

## Errata (2026-11-11, decisão do Fabio)

O ajuste do sólido media o periapse e o apoapse, que têm uma quina em e = 0, exatamente no alvo circular; o custo parava em valores espalhados, a tolerância da P-110 caía no meio desse ruído, e a escala escolhida mudava com a CPU (CI do PR #60, run 42896102600; results/conferencia/ruido_subida.md). O ajuste passou a usar o semieixo e o vetor excentricidade, funções suaves, e a escala mínima do sólido passou a ser a raiz de (maior semieixo de uma circular alcançável) − (raio-alvo), por brentq (P-117, NÃO VALIDADA, para aprovação). Os valores publicados vêm de results/familia1/mavs.yaml no commit 8417131, o merge do PR #59; os antigos ficam como registro. O hipergólico não mudou.

| Sólido, 380 km | Escala | GLOM (kg) | Capacidade (m/s) | Empuxo/peso | Comprimento (m) | Folga sem deck (m) | Folga com deck (m) | Massa de entrada (kg) | Massa por área (kg/m²) | Aquecimento (W) | Energia (kWh) | RHUs |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| sem margem, publicado | 1,0289 | 404,9 | 4 103 | 5,60 | 2,73 a 2,78 | +0,203 a +0,225 | −0,017 a +0,005 | 4 443 | 279 | 17,4 | 119 | 24 |
| sem margem, vigente | 0,9692 | 382,3 | 4 073 | 5,58 | 2,62 a 2,66 | +0,260 a +0,284 | +0,040 a +0,064 | 4 399 | 277 | 16,7 | 114 | 23 |
| com a margem da P-014, publicado | 3,8512 | 1 471,7 | 4 514 | 5,76 | 6,12 a 10,40 | −3,607 a −1,469 | −3,827 a −1,689 | 6 539 | 411 | 41,9 | 286 | 57 |
| com a margem da P-014, vigente | 3,2228 | 1 234,2 | 4 481 | 5,75 | 5,37 a 8,70 | −2,759 a −1,092 | −2,979 a −1,312 | 6 072 | 382 | 37,2 | 254 | 51 |

Verificação, divisões que chegam à órbita publicada: tempo publicado: publicado 0,38, 0,40, 0,42, vigente 0,38, 0,40, 0,42; empuxo publicado: publicado 0,38, 0,40, vigente 0,38, 0,40, 0,42. A base continua em 0,40.
