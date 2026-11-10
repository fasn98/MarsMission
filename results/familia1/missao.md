# Família 1: missão de estada longa (gerado por tools/missao_familia1.py)

**Calculado, NÃO verificado.** O orbitador só elétrico usa os tempos da rota B (results/etapa7.2/rotas_mav.md), com o trecho heliocêntrico quase circular e a margem de Δv, sem trajetória otimizada.

## Conjunções solares (Sol–Terra–Marte ≤ 5°)

| Início | Fim | Dias |
| :- | :- | -: |
| 2030-05-06 | 2030-06-13 | 39 |
| 2032-06-25 | 2032-07-27 | 33 |
| 2034-08-05 | 2034-09-03 | 30 |

## Menor estada

**A menor estada é condicional:** a partida da Terra fica a da referência e os tempos são os da rota B, com crédito zero de C3. Premissa numérica P-109.

Referência: chegada do lander em 2029-09-20, partida em 2030-11-08; lançamento do MAV de 2029-11-03 a 2030-03-06. O MAV lança no primeiro dia em que o orbitador está pronto, fora da conjunção, da recuperação de 7 dias e da folga de 60 dias antes da conjunção seguinte (ADR 0018).

| Encontro (km) | Propulsores | Orbitador (kg) | Pronto no encontro | Lançamento do MAV | Último lançamento possível | Partida de Marte | Estada (d) | Estada da referência (d) | C3 na partida (km²/s²) | C3 na partida da referência | Chegada à Terra (tempo de voo balístico) | Missão total, com o voo balístico (d) | MAV na superfície (d) |
| -: | -: | -: | :- | :- | :- | :- | -: | -: | -: | -: | :- | -: | -: |
| 380 | 10 × XIPS-25, 45,0 kW | 9 420 | 2030-07-02 | 2030-07-02 | 2032-04-26 | 2031-01-20 | 487 | 414 | 7,23 | 5,44 | 2031-11-01 | 1072 | 285 |
| 814 | 8 × XIPS-25, 36,0 kW | 7 947 | 2030-07-18 | 2030-07-18 | 2032-04-26 | 2031-02-02 | 500 | 414 | 7,99 | 5,44 | 2031-11-04 | 1075 | 301 |

**Conjunção solar:** na referência, o MAV lança antes da conjunção de 2030. Aqui, o MAV lança depois dela, no intervalo até a seguinte, e o lander com o MAV fica na superfície durante a conjunção de 2030.
- Encontro a 380 km: a descida em espiral começa em 2029-12-06 e cruza a conjunção (pede operação autônoma do orbitador); o encontro e a subida em espiral ficam fora das conjunções.
- Encontro a 814 km: a descida em espiral começa em 2029-12-26 e cruza a conjunção (pede operação autônoma do orbitador); o encontro e a subida em espiral ficam fora das conjunções.

**O que falta para verificar o orbitador só elétrico:** (1) uma trajetória heliocêntrica de baixo empuxo com efemérides, nas datas de cada caso, no lugar do trecho quase circular com margem; (2) comparação dessa trajetória com um caso publicado de baixo empuxo Terra–Marte (por exemplo o ERO, [F260], ou um estudo com massas e tempos publicados); (3) a vida dos propulsores XIPS-25 com fonte ("não achada" em results/etapa7.2/rotas_mav.md); (4) a fase de RAAN e o plano até a órbita do encontro (results/etapa7.2/rotas_mav.md não a inclui); (5) o ciclo de trabalho e a potência dos painéis na distância de Marte. A espiral em Marte usa as leis da Etapa 3.2, cuja verificação tem ressalva em results/etapa3.2/baixo_empuxo.md.

**Retorno:** C3 balístico de 7,23 e 7,99 km²/s² nas partidas calculadas, contra 5,44 km²/s² na partida da referência e 5,43 km²/s² no mínimo da janela de 2030 (results/etapa1.2/minimos_marte_terra.yaml); não há critério de janela definido. A volta do elétrico usa o tempo de empuxo da rota B, não esse C3; a chegada à Terra usa o tempo de voo balístico, como ordem de grandeza.
