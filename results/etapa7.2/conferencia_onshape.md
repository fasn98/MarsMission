# Conferência do CAD no Onshape (gerado por tools/conferencia_onshape.py)

**VERIFICAÇÃO**: o CAD gerado no Onshape reproduz o modelo do script (mesma geometria e mesmas densidades). Não é validação do projeto nem comparação com o orçamento (Etapa 7.3).

Medido: propriedades de massa lidas no Onshape (tests/data/onshape/medicoes.yaml), convertidas com 1 lb = 0.45359237 kg e 1 mm = 1e-3 m. Previsto: tools/cad_parametros.py (results/etapa7.2/parametros.yaml). Inércias no centro de massa, nos eixos do Part Studio.

## Orbitador

Aguardando medição. Previsto pelo script: massa 6 506,3 kg; CG z 1,393 m; Ixx, Iyy, Izz = 12 069,92, 14 890,73, 11 604,90 kg·m²; 20 corpos.

## Lander

Aguardando medição. Previsto pelo script: massa 3 190,4 kg; CG z 3,003 m; Ixx, Iyy, Izz = 3 648,02, 3 639,20, 4 131,30 kg·m²; 33 corpos.

## MAV

Medição: Fabio, 2026-11-03, FeatureScript versão 3112, results/etapa7.2/mav.fs; compilou: sim; Assign materials: sim.

| Grandeza | Medido no Onshape | Previsto pelo script | Desvio |
| :- | -: | -: | -: |
| Peças | 12 | 12 | 0 |
| Massa (kg) | 348,127 | 348,126 | +2,4e−06 (relativo) |
| CG x (m) | 0,0000 | 0,0000 | +0,0e+00 m |
| CG y (m) | 0,0000 | 0,0000 | +0,0e+00 m |
| CG z (m) | 1,5399 | 1,5399 | −6,5e−06 m |
| Ixx no CG (kg·m²) | 252,65 | 252,63 | +7,5e−05 (relativo) |
| Iyy no CG (kg·m²) | 252,65 | 252,63 | +7,5e−05 (relativo) |
| Izz no CG (kg·m²) | 13,87 | 13,87 | +6,8e−05 (relativo) |
| Volume (m³) | 0,5065 | 0,5065 | +1,9e−05 (relativo) |

As inércias e o volume medidos têm 4 algarismos significativos (como o Onshape os mostrou); os desvios abaixo de ~1e-4 estão dentro dessa precisão de leitura. Os dados do FeatureScript vão com 6 algarismos significativos (tools/cad_parametros.py), o que explica desvios da ordem de 1e-6 na massa e no CG.

