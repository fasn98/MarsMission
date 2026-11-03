# Conferência do CAD no Onshape (gerado por tools/conferencia_onshape.py)

**VERIFICAÇÃO**: o CAD gerado no Onshape reproduz o modelo do script (mesma geometria e mesmas densidades). Não é validação do projeto nem comparação com o orçamento (Etapa 7.3).

Medição: Fabio, 2026-11-03, conta real do Onshape, FeatureScript versão 3112, arquivos do commit 32cb41d (cópias em tests/data/onshape/), Assign materials: sim. Unidades SI; inércias no centro de massa, nos eixos do Part Studio.

Documento no Onshape: "MarsMission Fase 7", gerado com os arquivos do commit 32cb41d e versionado no Onshape como "etapa7.2-32cb41d". Os arquivos atuais (results/etapa7.2/*.fs) diferem dos compilados: modelo atual menos compilado, Orbitador +0,6 g; Lander −0,027 kg; MAV sem diferença. Os previstos dos arquivos atuais estão em results/etapa7.2/parametros.yaml.

Previsto: tools/cad_parametros.py (volume, centro e inercia) sobre os dados do próprio arquivo compilado. O script calcula CG em x, y e z e o tensor de inércia completo; os produtos de inércia são comparados na forma de tensor (−∫ x y dm), com os sinais do Onshape.

Tolerância: meia unidade da última casa decimal mostrada em cada valor, lido manualmente na tela do Onshape (Mass properties, workspace units em SI). Cada linha mostra as casas decimais lidas; um CG mostrado como "0" usa as casas da coordenada z do mesmo veículo.

## Orbitador

Arquivo tests/data/onshape/compilados_32cb41d/orbitador.fs; compilou: sim; peças: 20 medidas, 20 corpos no arquivo.

| Grandeza | Medido no Onshape | Casas mostradas | Previsto pelo script | Desvio absoluto | Desvio relativo | Tolerância de leitura |
| :- | -: | -: | -: | -: | -: | :- |
| massa (kg) | 6506,2448 | 4 | 6506,2448 | +2,6e−05 | +4,1e−09 | ± 5,0e−05: dentro |
| CG x (m) | 0 | 4 | −2,986e−17 | +3,0e−17 | — | ± 5,0e−05: dentro |
| CG y (m) | 0 | 4 | 4,368e−17 | −4,4e−17 | — | ± 5,0e−05: dentro |
| CG z (m) | 1,3928 | 4 | 1,3928 | −2,5e−06 | −1,8e−06 | ± 5,0e−05: dentro |
| Ixx (kg·m²) | 12069,908 | 3 | 12069,9080 | +4,4e−05 | +3,6e−09 | ± 5,0e−04: dentro |
| Iyy (kg·m²) | 14890,7017 | 4 | 14890,7017 | −4,5e−05 | −3,0e−09 | ± 5,0e−05: dentro |
| Izz (kg·m²) | 11604,863 | 3 | 11604,8630 | +1,3e−05 | +1,1e−09 | ± 5,0e−04: dentro |
| volume (m³) | 10,8264 | 4 | 10,8264 | +3,4e−05 | +3,2e−06 | ± 5,0e−05: dentro |
| produtos de inércia | ~1e-13 (zero numérico) | — | maior valor absoluto +2,1e−13 | — | — | — |
| área (m²) | 142,922 | 3 | não calculada pelo script | — | — | — |

Modelo atual (results/etapa7.2/parametros.yaml) contra o arquivo compilado: massa +6,3e−04 kg; CG +2,9e−24, −4,2e−24, +3,2e−07 m.

## Lander

Arquivo tests/data/onshape/compilados_32cb41d/lander.fs; compilou: sim; peças: 33 medidas, 33 corpos no arquivo.

| Grandeza | Medido no Onshape | Casas mostradas | Previsto pelo script | Desvio absoluto | Desvio relativo | Tolerância de leitura |
| :- | -: | -: | -: | -: | -: | :- |
| massa (kg) | 3190,4337 | 4 | 3190,4337 | +1,4e−05 | +4,5e−09 | ± 5,0e−05: dentro |
| CG x (m) | 0,0256 | 4 | 0,0256 | −6,3e−06 | −2,5e−04 | ± 5,0e−05: dentro |
| CG y (m) | −0,0263 | 4 | −0,0263 | −4,3e−05 | +1,7e−03 | ± 5,0e−05: dentro |
| CG z (m) | 3,0032 | 4 | 3,0032 | +1,3e−05 | +4,4e−06 | ± 5,0e−05: dentro |
| Ixx (kg·m²) | 3648,0512 | 4 | 3648,0512 | +2,3e−05 | +6,3e−09 | ± 5,0e−05: dentro |
| Iyy (kg·m²) | 3639,2293 | 4 | 3639,2293 | −1,1e−05 | −3,0e−09 | ± 5,0e−05: dentro |
| Izz (kg·m²) | 4131,3508 | 4 | 4131,3508 | +2,3e−05 | +5,5e−09 | ± 5,0e−05: dentro |
| Ixy (kg·m²) | −2,145 | 3 | −2,1450 | +4,2e−05 | −2,0e−05 | ± 5,0e−04: dentro |
| Ixz (kg·m²) | 108,3561 | 4 | 108,3561 | +3,2e−05 | +3,0e−07 | ± 5,0e−05: dentro |
| Iyz (kg·m²) | −14,089 | 3 | −14,0890 | +2,6e−05 | −1,9e−06 | ± 5,0e−04: dentro |
| volume (m³) | 6,9993 | 4 | 6,9993 | −7,2e−06 | −1,0e−06 | ± 5,0e−05: dentro |
| área (m²) | 188,407 | 3 | não calculada pelo script | — | — | — |

Modelo atual (results/etapa7.2/parametros.yaml) contra o arquivo compilado: massa −2,7e−02 kg; CG +2,2e−07, −2,3e−07, +1,8e−06 m.

## MAV

Arquivo tests/data/onshape/compilados_32cb41d/mav.fs; compilou: sim; peças: 12 medidas, 12 corpos no arquivo.

| Grandeza | Medido no Onshape | Casas mostradas | Previsto pelo script | Desvio absoluto | Desvio relativo | Tolerância de leitura |
| :- | -: | -: | -: | -: | -: | :- |
| massa (kg) | 348,127 | 3 | 348,1270 | +3,5e−05 | +1,0e−07 | ± 5,0e−04: dentro |
| CG x (m) | 0 | 4 | 0,0000 | +0,0e+00 | — | ± 5,0e−05: dentro |
| CG y (m) | 0 | 4 | 0,0000 | +0,0e+00 | — | ± 5,0e−05: dentro |
| CG z (m) | 1,5399 | 4 | 1,5399 | +4,3e−05 | +2,8e−05 | ± 5,0e−05: dentro |
| Ixx (kg·m²) | 252,629 | 3 | 252,6290 | +4,7e−05 | +1,8e−07 | ± 5,0e−04: dentro |
| Iyy (kg·m²) | 252,629 | 3 | 252,6290 | +4,7e−05 | +1,8e−07 | ± 5,0e−04: dentro |
| Izz (kg·m²) | 13,8699 | 4 | 13,8699 | −3,6e−05 | −2,6e−06 | ± 5,0e−05: dentro |
| volume (m³) | 0,5065 | 4 | 0,5065 | +1,0e−05 | +2,0e−05 | ± 5,0e−05: dentro |
| produtos de inércia | ~1e-15 (zero numérico) | — | maior valor absoluto +0,0e+00 | — | — | — |
| área (m²) | 14,2848 | 4 | não calculada pelo script | — | — | — |

Modelo atual (results/etapa7.2/parametros.yaml) contra o arquivo compilado: massa +0,0e+00 kg; CG +0,0e+00, +0,0e+00, +0,0e+00 m.

