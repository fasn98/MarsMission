# Conferência do CAD no Onshape (gerado por tools/conferencia_onshape.py)

**VERIFICAÇÃO**: o CAD gerado no Onshape reproduz o modelo do script (mesma geometria e mesmas densidades). Não é validação do projeto nem comparação com o orçamento (Etapa 7.3).

Medido: propriedades de massa lidas no Onshape (tests/data/onshape/medicoes.yaml), convertidas com 1 lb = 0.45359237 kg e 1 mm = 1e-3 m. Previsto: tools/cad_parametros.py (results/etapa7.2/parametros.yaml). Inércias no centro de massa, nos eixos do Part Studio.

## Orbitador

Aguardando medição. Previsto pelo script: massa 6 506,3 kg; CG z 1,393 m; Ixx, Iyy, Izz = 12 069,92, 14 890,73, 11 604,90 kg·m²; 20 corpos.

## Lander

Aguardando medição. Previsto pelo script: massa 3 190,4 kg; CG z 3,003 m; Ixx, Iyy, Izz = 3 648,02, 3 639,20, 4 131,30 kg·m²; 33 corpos.

## MAV

Medição: Fabio, 2026-11-03, FeatureScript versão 3112, results/etapa7.2/mav.fs; compilou: sim; Assign materials: sim.

| Grandeza | Medido no Onshape | Previsto pelo script | Desvio | Precisão de leitura |
| :- | -: | -: | -: | :- |
| Peças | 12 | 12 | 0 | — |
| Massa (kg) | 348,127 | 348,126 | +2,4e−06 (relativo) | dentro |
| CG x (m) | 0,0000 | 0,0000 | +0,0e+00 m | dentro |
| CG y (m) | 0,0000 | 0,0000 | +0,0e+00 m | dentro |
| CG z (m) | 1,5399 | 1,5399 | −6,5e−06 m | dentro |
| Ixx no CG (kg·m²) | 252,65 | 252,63 | +7,5e−05 (relativo) | dentro |
| Iyy no CG (kg·m²) | 252,65 | 252,63 | +7,5e−05 (relativo) | dentro |
| Izz no CG (kg·m²) | 13,87 | 13,87 | +6,8e−05 (relativo) | dentro |
| Volume (m³) | 0,5065 | 0,5065 | +1,9e−05 (relativo) | dentro |
| Produtos de inércia | da ordem de 1e-8 (ruído numérico) | maior valor absoluto +0,0e+00 kg·m² | — | — |
| Área (m²) | 14,28 | não calculada pelo script | — | — |

Precisão de leitura: meia unidade do último algarismo que o Onshape mostrou (tests/data/onshape/medicoes.yaml, resolucao) mais o arredondamento dos dados do FeatureScript a 6 algarismos significativos (tools/cad_parametros.py).

