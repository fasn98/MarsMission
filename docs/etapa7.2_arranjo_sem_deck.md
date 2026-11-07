# Portão da rota A: viabilidade do arranjo sem deck (fontes)

Pedido do Fabio (2026-11-07): onde ficam, no MSL, no Mars 2020 e no lander do MSR (SRL), a estrutura de descida, o deck e a
carga dentro da casca traseira. A P-094 (deck de 0,30 m) e a P-092 (ombro otimista) seguem como estão. Aqui só há fontes,
sem cálculo. Os números do nosso MAV vêm de `results/etapa7.2/rota_a.md` e `results/etapa7.2/subida_mav.md`.

## Resposta curta

- **Não achei nenhuma cota interna** nas três missões: altura do estágio de descida, do deck ou da plataforma, folga até a
  casca ou até o escudo, nem corte com escala. A viabilidade do arranjo sem deck **não fica provada** pelas fontes.
- **MSL e Mars 2020:** a carga (o rover) é presa **diretamente** ao estágio de descida, sem deck intermediário citado, e o
  conjunto fica dentro da casca traseira com o escudo embaixo.
- **SRL:** o MAV vai **deitado** sobre a plataforma do lander, dentro de um recinto térmico, e há uma estrutura de ligação
  (LAS) entre a casca traseira e o lander, só desenhada, sem cota.
- **Comparação de envelope:** o MAV do MSR tinha de caber em 2,8 m no SRL de 2019 e em 3,0 m no de 2020, com cápsula de
  4,65 m. O nosso limite sem deck, em cápsula de 4,5 m, é maior que esses dois. É um indício de que o limite sem deck é
  otimista, não uma prova.

## MSL (Curiosity)

| O que a fonte diz | Citação | Fonte |
| :- | :- | :- |
| Rover preso diretamente ao estágio de descida | "While the rover is fastened to the descent stage, the two components together are called the powered descent vehicle. The fastenings are pyrotechnic bolts." | [F251] PDF p. 37 |
| Rover e estágio de descida no aeroshell | "The 4.5 m aeroshell is composed of a heatshield and backshell, and contains the DS and rover." | [F244] PDF p. 1 |
| Estágio de descida aninhado na casca | "with the PDV nested inside the backshell" | [F244] PDF p. 9 |
| O que é o estágio de descida | "The Descent Stage contains fuel and rocket engines to provide a powered descent to the surface with a deployed Rover" | [F252] PDF p. 253 |
| Única cota | "Cruise vehicle dimensions (cruise stage and aeroshell with rover and descent stage inside): Diameter: 14 feet, 9 inches (4.5 meters); height: 9 feet, 8 inches (3 meters)" | [F251] PDF p. 6 |

**Leitura de figura:** [F252] PDF p. 254, Fig. 1, vista explodida, de cima para baixo: estágio de cruzeiro, casca traseira,
estágio de descida, rover, escudo. Nenhum deck aparece entre o estágio de descida e o rover. Sem cotas.

## Mars 2020 (Perseverance)

| O que a fonte diz | Citação | Fonte |
| :- | :- | :- |
| Rover e estágio de descida no aeroshell | "the Perseverance rover and its descent stage are protected inside a capsule known as an aeroshell" | [F253] PDF p. 25 |
| O conjunto que sai da casca | "the powered descent vehicle – the combination of the descent stage and the rover – separates from the back shell" | [F45] PDF p. 22 |
| Semelhança com o MSL | "Perseverance is traveling to Mars in an almost identical way to NASA's Curiosity rover" | [F45] PDF p. 37 |

Sem cotas internas.

## Lander do MSR (SRL)

| O que a fonte diz | Citação | Fonte |
| :- | :- | :- |
| MAV deitado no lançamento e na entrada | "This requires it to be stored in a lateral position during major loads events such as Earth launch and Martian Entry, Descent, and Landing (EDL). The primary load path of the vehicle during these times passes directly through SRM1 and the interstage." | [F35] PDF p. 4 |
| Plataforma de pouso com o MAV como carga | "deploy the Mobile Lander Platform (MLP), with the MAV as its payload" | [F35] PDF p. 2 |
| Fixação no lander | "attach directly to the SRL via four attach hard points on the VECTOR" | [F57] PDF p. 4 |
| Recinto térmico | "the MAV is stored in a thermal enclosure known as the igloo" | [F249] PDF p. 3 |
| Envelope para caber no SRL (2019) | "a maximum length of 2.8m and a maximum diameter of 0.57m was needed to fit within the SRL" | [F249] PDF p. 2 |
| Envelope (DAC-0.0, 2020) | "a geometric length not to exceed 3.0m and a diameter not to exceed 0.57m (excluding aft aerodynamic ramp)" | [F57] PDF p. 2 |
| Diâmetro da cápsula | Tabela "Capsule diameter (m)": 4.5 (MSL), 4.5 (Mars 2020), 4.65 e >5.4 (duas colunas do SRL) | [F254] PDF p. 13 |
| Alternativa de 2023 | "MSR MAV Lander (MML), which includes the MAV and a MAV landing/launch system using a scaled-up Skycrane EDL" | [F255] PDF p. 45 |

**Leitura de figuras (sem cotas nem escala):**
- [F254] PDF p. 9, "SRL Baseline Entry System", vista explodida de cima para baixo: casca traseira (BS), "LAS (Lander Attach
  Struct.)", lander (MLV), escudo (HS). A LAS é uma estrutura de ligação entre a casca e o lander, que o MSL não mostra.
- [F249] PDF p. 3, Fig. 2 "MAV Stowed on SRL", com o escudo translúcido: o igloo, uma caixa horizontal com o MAV, atravessa o
  lander quase de borda a borda, entre tanques esféricos e pernas, com um anel estrutural em cima. A fonte não nomeia o anel.
- [F57] PDF p. 8, Fig. 16 "SRL with MAV Stowed Within Igloo": MAV horizontal dentro do igloo, sobre o berço, apoiado no corpo
  do lander.

## O que isso diz sobre o nosso "sem deck"

- **A favor:** nenhuma das três missões põe um deck entre a estrutura de descida e a carga. No MSL e no Mars 2020, a carga
  pende do estágio de descida. No SRL, o MAV deitado ocupa quase todo o diâmetro do lander. Um arranjo em que a carga vai até
  perto do plano mais largo não contraria nenhuma das fontes.
- **Contra:** o SRL tem uma estrutura de ligação (LAS) entre a casca e o lander, e um recinto térmico em volta do MAV. As duas
  ocupam o espaço que o nosso "sem deck" dá ao MAV. O MSR limitou o MAV a 2,8 m (2019) e a 3,0 m (2020) numa cápsula de
  4,65 m. O nosso limite sem deck, 3,184 m em 4,5 m (`results/etapa7.2/rota_a.yaml`, `alvo.limite_sem_deck_m`), passa dos dois.
- **Conclusão:** as fontes não provam nem descartam o arranjo sem deck. O indício do SRL é de que o espaço real é menor que
  o nosso limite sem deck. Para provar, faltaria uma cota do SRL ou do MSL: altura da LAS, do igloo ou do estágio de descida,
  ou a folga até a casca. Não achei nenhuma.

## Não achado ou não conferido

- Cotas internas de qualquer uma das três missões.
- Altura da plataforma do SRL, da LAS e do igloo; só "two layers of CO2, each layer being 5-cm thick" ([F34] PDF p. 5).
- Trabalhos do NTRS sem PDF aberto (por exemplo, a visão geral do SRL de 2021, NTRS 20210012062, e a arquitetura térmica do
  lander do MSR, NTRS 20220001440), e o trabalho do IEEE de 2008 sobre a placa de interface da casca do MSL (só o resumo).
