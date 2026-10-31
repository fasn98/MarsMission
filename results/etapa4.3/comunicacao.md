# Comunicação (gerado por tools/comunicacao.py)

## Conjunção solar na estada

Estada 2029-09-20 a 2030-11-08; amostragem diária à meia-noite TDB (datas com ±1 dia de resolução). Ângulo Sol–Terra–Marte mínimo: 0,30° em 2030-05-25, 247 dias depois da chegada (distância 376,5 milhões de km).

| Critério | SEP até | Início | Fim | Dias | Dias desde a chegada | Dias até a partida |
| :- | -: | :- | :- | -: | -: | -: |
| período de conjunção (MRO) | 5,0° | 2030-05-06 | 2030-06-13 | 39 | 228 | 148 |
| sem depender de telemetria (MER) | 3,0° | 2030-05-14 | 2030-06-06 | 24 | 236 | 155 |
| sem comandos (MER) | 2,0° | 2030-05-18 | 2030-06-02 | 16 | 240 | 159 |
| degradação da banda X (MRO) | 2,0° | 2030-05-18 | 2030-06-02 | 16 | 240 | 159 |
| abaixo do ângulo em que a DSN 810-005 106 cobre o retorno BPSK padrão | 2,3° | 2030-05-17 | 2030-06-03 | 18 | 239 | 158 |

Moratória de comandos de referência: [F176]: "most missions will stop sending commands between Oct. 2 and Oct. 16"; "Engineers will spend about a week downloading the information before normal spacecraft operations resume".

Relé de proximidade: [F173] PDF p. 18 (impr. 5): "Proximity communications with surface vehicles would not be directly affected".

SEP mínimo nos arcos de cruzeiro: ida 60,6°, volta 44,2°.

## Distância e tempo de luz

Distância Terra–espaçonave máxima: estada 380,7, ida 246,8, volta 306,5 milhões de km; na missão, 2,545 UA. Tempo de luz (uma via): até 21,2 min; mínimo na estada 13,7 min. Referência do análogo (MRO): distância máxima de 400 milhões de km [F173].

## Folgas em torno da conjunção (período de conjunção, SEP ≤ 5°)

Da chegada ao início da janela: 228 dias. Do fim da janela à partida, menos 7 dias de recuperação dos dados [F176]: 141 dias. As fases do encontro do ERO somam 46 dias (da subida do MAV à selagem do contêiner, T0 + 22 d, mais a fase de RAAN, T0 + 46 d [F121]): cabem depois da janela, com folga de 95 dias.

## Enlaces

- Orbitador em banda X (análogo do MRO, 1/d², P-064): 552 kbps na distância máxima da estada e 1 314 kbps na mínima; 15 900 Mbit por passe de 8 h na distância máxima. Conferência da escala: a 100 milhões de km ela dá 8 000 kbps, contra 3 a 4 Mbps publicados [F173] (a escala superestima perto da Terra).
- Lander direto à Terra (análogo do MSL: 160 bps a 2,4 UA [F137], mesma escala da P-064): 142 bps na distância máxima da estada; 4,1 Mbit num passe de 8 h (P-065), 1,6 % da demanda de 250 Mbit por sol (P-063).
- Relé UHF: até 2 048 kbps [F137]; o MSL com orbitadores em órbita baixa tinha de 100 a 1 150 Mbit por sol [F137]. A órbita de encontro vai de 300 a 25 952 km de altitude: no apoapse, 38,7 dB a mais de perda de espaço livre que no periapse (só pela distância).

## Comparação das saídas para a comunicação do lander

Demanda: lander 250 Mbit/sol (P-063) + helicópteros 983 Mbit/sol (492 Mbit por voo, 2 voos/sol, P-068; 33 min de enlace helicóptero–base por voo a 250 kbps [F180]) = 1 233 Mbit/sol.

### (a) Orbitadores de relé existentes

| Orbitador | Estado | Fonte |
| :- | :- | :- |
| MAVEN | perdido; missão encerrada em 03/06/2026 | [F181] |
| MRO | operando; propelente além de três anos (2025); TWTA de banda X perto do fim da vida, ponto único de falha; linha de orçamento até o FY2031 | [F182] |
| Odyssey | propelente baixo; financiamento eliminado no pedido do FY2026; fora da tabela do FY2027 | [F182] |
| TGO | saúde nominal "well into the 2030s"; extensão da ESA até 2030 não conferida; até 2048 kbps; pelo menos dois passes bons por sol | [F183] |
| Mars Express | financiado até o fim de 2026; extensão pedida até o fim de 2029; capacidade de relé não quantificada | [F183] |
| Mars Telecommunications Orbiter (comercial) | US$ 700 milhões na PL 119-21, entrega até 31/12/2028; contrato e vencedor não conferidos | [F185] |
| MAVEN (desempenho no apoapse, referência) | passes longos a taxas baixas | [F178] |

### (c) Relé pelo nosso orbitador na órbita de encontro (simulação dos passes, P-066 e P-067)

| Caso | Passes por sol | Duração média (min) | Mbit por passe (médio / máximo) | Mbit por sol | Cobertura da demanda total | Energia transmitindo (Wh/sol) |
| :- | -: | -: | -: | -: | -: | -: |
| periapse na latitude do sítio | 1,52 | 325 | 1 559 / 3 564 | 2 365 | 192 % | 568 |
| apoapse na latitude do sítio | 1,00 | 582 | 2 336 / 4 842 | 2 336 | 189 % | 669 |

Conferência do modelo de enlace: numa órbita baixa de 250 km ele dá 1 024 kbps (o topo da tabela do Electra); referência publicada: [F177] p. 26: "a 15-minute relay session at 256 kbps will return approximately 230 Mbit of data. In comparison, TGO supports adaptive data rates up to 2048 kbps, and can therefore return over 1 Gbit during a 15-minute overflight". A energia supõe transmissão em todo o tempo visível (envoltória).

### (b) Enlace direto maior (P-069)

Taxa necessária para a demanda total num passe de 8 h: 42 814 bps, 301 vezes o análogo do MSL (24,8 dB). HGA de 4,86 m com 15 W, ou de 1,86 m com o TWTA de 100 W do MRO; massa do conjunto com 100 W de cerca de 29,6 kg, contra 9,4 kg do MSL; 1 376 Wh por passe. Área de operação com esse consumo: 24,5 m², abaixo dos 32,8 m² da linha de base (a área continua dada pela sobrevivência). Na conjunção, o enlace direto também para.
