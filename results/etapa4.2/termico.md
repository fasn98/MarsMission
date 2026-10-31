# Controle térmico (gerado por tools/termico.py)

## Faixas de temperatura dos itens críticos (°C)

| Item | Tipo | Mínimo | Máximo | Fonte |
| :- | :- | -: | -: | :- |
| MMH (orbitador e MAV) | ponto de fusão | −52,4 | — | [F157] |
| NTO / MON-3 (orbitador e MAV) | ponto de fusão | −11,2 | — | [F158] |
| Sistemas MMH/NTO em operação (nominal) | faixa nominal | 15,0 | 27,0 | [F159] |
| Tanques de propelente (cruzeiro do MER) | AFT | 17,0 | 28,0 | [F160] |
| Linhas de propelente (cruzeiro do MER) | AFT | 17,0 | 50,0 | [F160] |
| Linhas de propelente à base de hidrazina (típico) | AFT | 15,0 | 50,0 | [F161] |
| Propulsão líquida (hidrazina) do MAV do SRL | AFT | 14,0 | 50,0 | [F164] |
| Bateria Li-ion do Perseverance (operação) | operação | −20,0 | 30,0 | [F162] |
| Bateria Li-ion do Phoenix e do MSL (operação) | operação | −20,0 | 30,0 | [F163] |
| Bateria Li-ion do SRL (cruzeiro, interface do HRS) | AFT | 0,0 | 30,0 | [F165] |
| Amostras (RSTA), fora de transientes | AFT | — | −20,0 | [F167] |
| Amostras (RSTA), transientes operacionais inevitáveis | AFT | — | 30,0 | [F167] |
| MAV O4 do estudo (aquecido) | alvo do aquecimento (P-027) | 15,0 | — | config/mav_propulsao.yaml, aquecimento.t_minima_c |

Ambiente do modelo de aquecimento do MAV: −62,5 °C (igloo do SRL [F57]); mínima noturna do solo em Jezero: cerca de −93 °C [F172].

## Aquecimento do MAV e efeito no orçamento de energia do lander (C + RHU)

O aquecimento escala com (T − T_ambiente) no modelo atual (P-027). A área da sobrevivência é linear na carga (mesmo cenário, tools/energia.py); a da opção é a maior entre ela e a de operação com céu claro.

| Alvo do MAV | T (°C) | Potência (W) | Wh/sol | Sobrevivência (Wh/sol) | Demanda em operação (Wh/sol) | Área da opção (m²) | Massa da opção (kg) |
| :- | -: | -: | -: | -: | -: | -: | -: |
| atual (P-027) | 15 | 60,8 | 1 500 | 2 004 | 5 000 | 32,8 | 278 |
| anterior_p027 | −1 | 48,3 | 1 191 | 1 694 | 4 691 | 27,7 | 245 |
| aft_tanques_mer | 17 | 62,4 | 1 539 | 2 042 | 5 039 | 33,4 | 282 |

## Amostras

AFT das amostras fora de transientes: −20 °C [F167]. O MAV do estudo é aquecido a 15 °C: 35 K acima da AFT das amostras; com os alvos alternativos, anterior_p027 19 K, aft_tanques_mer 37 K.

Decisão (portão da 4.2): transferência tardia para o MAV, tratada como transiente (+30 °C). Faixas de temperatura máxima estimadas por fase, no pior caso [F167], registro (d):

| Fase | Duração | Máxima estimada (°C) |
| :- | :- | :- |
| Antes da coleta | éons | −20 a 10 |
| No Perseverance (cache do rover) | anos | −65 a 10 |
| No depósito na superfície | anos | 5 a 53 |
| Transferência para o contêiner (OS) | meses | 30 a 53 |
| Lançamento do MAV | minutos | 30 |

No depósito desde 2023-02-15 (P-062) até a chegada da missão de referência em 2029-09-20: 6,6 anos, no mínimo (inferência da P-062: a coleta é depois da chegada); os tubos podem ser aquecidos repetidamente a até 300 K [F172]. Isolamento do contêiner (opção a): não avaliado: sem análogo com massa publicada (busca de 2026-10-31; só o limite de massa de todo o contêiner e as massas do veículo de entrada na Terra).

## Comparação com o projeto publicado do SRL (análise, não medida)

- Aquecedores de sobrevivência do LAMP e da bateria no caso frio: 1 540 Wh/sol; energia total do LAMP no caso frio: 2 300 Wh/sol [F166]. Aqui: aquecedores do lander 363 Wh/sol mais 34,6 W de RHUs (853 Wh/sol), total 1 217 Wh/sol, 79 % do SRL (P-056, ADR 0015). O SRL é outro veículo, no pior caso frio (Ls 72°), não na tempestade; a comparação não é verificação.
- MAV: sobrevivência da MAS do SRL (estágios sólidos e RCS líquido a +14 °C) de cerca de 30 W [F164]; operação de um MAV sólido a −20 °C de 60 a 70 W [F170]. Aqui: 60,8 W (MAV líquido).

## Cruzeiro: calor das RHUs dentro do aeroshell

35 RHUs, 35,0 W: 18 % da perda passiva máxima do LAMP do SRL (200 W [F165]); 28 % dos 125 W que o MER rejeitou por HRS ativo [F168]; 9 % dos 400 W da MMRTG que o projeto do MSL dissipava parasitamente no backshell e no escudo [F169]. No SRL, a dissipação máxima do LAMP no cruzeiro era de 322 W, acima dos 200 W da perda passiva [F165]. A dissipação das aviônicas do lander no cruzeiro não está no estudo.

## Orbitador

Os aquecedores estão dentro da potência da plataforma por modo (P-053): cruzeiro 745 W, captura 310 W, encontro 1 022 W, retorno 945 W. Referência: o MRO usa até 300 W em aquecedores [F171], sem divisão por modo.
