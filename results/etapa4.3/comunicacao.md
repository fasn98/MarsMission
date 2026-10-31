# Comunicação (gerado por tools/comunicacao.py)

## Conjunção solar na estada

Estada 2029-09-20 a 2030-11-08. Ângulo Sol–Terra–Marte mínimo: 0,30° em 2030-05-25, 247 dias depois da chegada (distância 376,5 milhões de km).

| Critério | SEP abaixo de | Início | Fim | Dias | Dias desde a chegada | Dias até a partida |
| :- | -: | :- | :- | -: | -: | -: |
| período de conjunção (MRO) | 5,0° | 2030-05-06 | 2030-06-13 | 39 | 228 | 148 |
| sem depender de telemetria (MER) | 3,0° | 2030-05-14 | 2030-06-06 | 24 | 236 | 155 |
| sem comandos (MER) | 2,0° | 2030-05-18 | 2030-06-02 | 16 | 240 | 159 |
| degradação da banda X (MRO) | 2,0° | 2030-05-18 | 2030-06-02 | 16 | 240 | 159 |
| retorno BPSK padrão garantido (DSN 810-005 106) | 2,3° | 2030-05-17 | 2030-06-03 | 18 | 239 | 158 |

Moratória de comandos de referência: [F176]: "most missions will stop sending commands between Oct. 2 and Oct. 16"; "Engineers will spend about a week downloading the information before normal spacecraft operations resume".

Relé de proximidade: [F173] PDF p. 18 (impr. 5): "Proximity communications with surface vehicles would not be directly affected".

SEP mínimo nos arcos de cruzeiro: ida 60,6°, volta 44,2°.

## Distância e tempo de luz

Distância Terra–espaçonave máxima: estada 380,7, ida 246,8, volta 306,5 milhões de km; na missão, 2,545 UA. Tempo de luz (uma via): até 21,2 min; mínimo na estada 13,7 min. Referência do análogo (MRO): distância máxima de 400 milhões de km [F173].

## Folgas em torno da conjunção (período de conjunção, SEP ≤ 5°)

Da chegada ao início da janela: 228 dias. Do fim da janela à partida, menos 7 dias de recuperação dos dados [F176]: 141 dias. As fases do encontro do ERO somam 46 dias (captura e fase de RAAN [F121]): cabem depois da janela, com folga de 95 dias.

## Enlaces

- Orbitador em banda X (análogo do MRO, 1/d², P-064): 552 kbps na distância máxima da estada e 1 314 kbps na mínima; 15 900 Mbit por passe de 8 h na distância máxima. Conferência da escala: a 100 milhões de km ela dá 8 000 kbps, contra 3 a 4 Mbps publicados [F173] (a escala superestima perto da Terra).
- Lander direto à Terra (análogo do MSL): 160 bps na distância máxima; 4,6 Mbit num passe de 8 h, 1,8 % da demanda de 250 Mbit por sol (P-063).
- Relé UHF: até 2 048 kbps [F137]; o MSL com orbitadores em órbita baixa tinha de 100 a 1 150 Mbit por sol [F137]. A órbita de encontro vai de 300 a 25 952 km de altitude: no apoapse, 38,7 dB a mais de perda de espaço livre que no periapse (só pela distância, sem a geometria do passe).
