# Etapa 7.2b: folgas nas coifas (gerado por tools/encaixe_coifas.py)

**VERIFICAÇÃO geométrica do modelo, não validação.** O envelope do Vulcan é leitura de uma figura "Simplified" do guia. O do Falcon é o STEP do fabricante amostrado em faixas de 500 mm. Nenhum deles é o CAD de interface do fabricante em voo.

## Folgas mínimas

Calculadas com todos os corpos de cada modelo, contra a face interna do envelope gravada no arquivo .fs. Em m.

| Configuração | Leitura do envelope | Folga radial | Onde | z (m) | Folga axial | Onde | Etapa 7.2 | Diferença |
| :- | :- | -: | :- | -: | -: | :- | -: | -: |
| Lander, aeroshell 4,5 m | Contorno reto entre as cotas | +0,141 | Escudo térmico (PICA) | 2,150 | +9,802 | Nariz do escudo (PICA) | +0,143 | −0,001 |
| Lander, aeroshell 4,5 m | Diametro menor desde o plano da interface | +0,064 | Escudo térmico (PICA) | 2,150 | +9,802 | Nariz do escudo (PICA) | +0,065 | −0,001 |
| Lander, aeroshell 4,65 m | Contorno reto entre as cotas | +0,044 | Escudo térmico (PICA) | 3,120 | +8,832 | Nariz do escudo (PICA) | +0,047 | −0,002 |
| Lander, aeroshell 4,65 m | Diametro menor desde o plano da interface | −0,016 | Escudo térmico (PICA) | 3,120 | +8,832 | Nariz do escudo (PICA) | −0,014 | −0,002 |
| Orbitador | Keep-in do fabricante, faixas de 500 mm | +0,361 | Tanque insercao MON-3 1 | 0,564 | +6,232 | EES com o contêiner de amostras | +0,356 | +0,005 |

## Por que as folgas do lander não batem com as da Etapa 7.2

**A diferença vem da amostragem da Etapa 7.2.** O `folga_vulcan` de `tools/cad_parametros.py` amostra o perfil da cápsula em 400 pontos, e nenhum cai no vértice do ombro, onde o raio é máximo. Por isso os valores publicados saem um pouco maiores que os da geometria que o Onshape constrói. A coluna abaixo repete a conta antiga, com o envelope lido do arquivo .fs:

| Configuração | Leitura | Conta da 7.2 repetida | Publicado na 7.2 | Geometria, no vértice |
| :- | :- | -: | -: | -: |
| Lander, aeroshell 4,5 m | Contorno reto entre as cotas | +0,1425 | +0,1425 | +0,1412 |
| Lander, aeroshell 4,5 m | Diametro menor desde o plano da interface | +0,0653 | +0,0653 | +0,0640 |
| Lander, aeroshell 4,65 m | Contorno reto entre as cotas | +0,0466 | +0,0466 | +0,0444 |
| Lander, aeroshell 4,65 m | Diametro menor desde o plano da interface | −0,0138 | −0,0138 | −0,0160 |

Com a SRL-C, a pior forma da P-089 e sem modelo próprio, os vértices dão +0,030 e −0,036 m, contra +0,032 e −0,034 m publicados.

A errata foi aprovada pelo Fabio (2026-11-04) e está em `results/etapa7.2/conferencias.md` e `portao_decisao.md`, com os valores antigos e os novos lado a lado.

**Orbitador:** a Etapa 7.2 dá +0,356 m (Tanques de inserção), porque trata cada conjunto como um cilindro no raio máximo. Aqui as esferas têm a forma real, e a folga é maior. As duas contas respondem a perguntas diferentes, e a da 7.2 fica do lado seguro.

## O que os arquivos têm

| Arquivo | Veículo | Corpos | Massa (kg) | CG x, y, z (m) | Mate connector preso a |
| :- | :- | -: | -: | :- | :- |
| lander_4_65.fs | lander_4_65 | 33 | 3 190,419 | 0,0256, −0,0263, 3,0032 | Circuito de fluido de cruzeiro (P-077) |
| lander_4_5.fs | lander_4_5 | 33 | 3 154,703 | 0,0259, −0,0266, 2,0985 | Circuito de fluido de cruzeiro (P-077) |
| orbitador.fs | orbitador | 20 | 6 506,252 | 0,0000, 0,0000, 1,3928 | Cilindro central |

**O que mudou em relação a `results/etapa7.2/orbitador.fs` e `lander.fs`:** a versão do cabeçalho, de 2737 para 3112; a linha de comentário com o rótulo de verificação; a constante `DONO_INTERFACE`; e o bloco `opMateConnector` no fim da feature. A lista CORPOS é a mesma (`tests/test_cad.py` confere), então massa e CG não mudam. O `mav.fs` não muda: o MAV não tem interface com o adaptador.

**`lander_4_5.fs` é um modelo novo:** cápsula MSL/M2020 e o resto do arranjo igual, com a massa acima. O MAV deitado viola a folga interna de 0,25 m da P-087 (folga de −0,188 m com a base na estação 0,85 m), mas não toca a casca. As peças que atravessam a face externa da cápsula são outras:

| Peça | Lander 4,5 m: folga até a face externa (m) | z (m) | Lander 4,65 m: folga até a face externa (m) | z (m) |
| :- | -: | -: | -: | -: |
| Tanque descida 1 | −0,079 | 2,481 | −0,031 | 3,453 |
| Tanque descida 2 | −0,079 | 2,481 | −0,031 | 3,453 |
| Tanque descida 3 | −0,079 | 2,481 | −0,031 | 3,453 |
| Helicóptero 1 | −0,060 | 1,040 | +0,321 | 2,010 |
| Helicóptero 2 | −0,060 | 1,040 | +0,321 | 2,010 |
| MAV (mais próximas: MAV carga (contêiner de amostras); MAV motores do estágio 1 (4 x R-4D-11)) | +0,069 | 1,590 | +0,272 | 2,560 |

Essas interferências entre peças não são corrigidas aqui (P-095): são o conflito do arranjo, e o Onshape vai mostrá-las.

## Grade alinhada e 13 algarismos: o que mudou

Antes: grade angular fixa e geometria com 6 algarismos, recalculadas aqui. Agora: grade alinhada à direção radial de cada peça, com 721 pontos, e 13 algarismos. A comparação junta os dois efeitos e cobre as folgas e posições do roteiro; a tabela de peças contra a cápsula não entra nela.

**Nas casas mostradas no roteiro (3):** nenhuma folga ou posição mudou. **Maiores diferenças nos valores completos:**

| Veículo | Leitura | Grandeza | Antes | Agora | Diferença (m) |
| :- | :- | :- | -: | -: | -: |
| orbitador | Keep-in do fabricante, faixas de 500 mm | folga axial | 6,231930000 | 6,231927774 | −2,23e−06 |
| orbitador | Keep-in do fabricante, faixas de 500 mm | z do topo | 5,115670000 | 5,115672226 | +2,23e−06 |
| orbitador | Keep-in do fabricante, faixas de 500 mm | raio do corpo | 1,958763685 | 1,958764291 | +6,05e−07 |
| orbitador | Keep-in do fabricante, faixas de 500 mm | distância no Measure | 0,360796924 | 0,360796320 | −6,04e−07 |
| orbitador | Keep-in do fabricante, faixas de 500 mm | folga radial | 0,360809054 | 0,360808450 | −6,04e−07 |
| orbitador | Keep-in do fabricante, faixas de 500 mm | z da folga radial | 0,564300109 | 0,564299910 | −1,99e−07 |

**Massa, CG e inércia (6 × 13 algarismos), contra a tolerância da P-039:**

| Veículo | Massa com 6 (kg) | Massa com 13 (kg) | Diferença (kg) | Maior diferença no CG (m) | Maior diferença na inércia (kg·m²) | Acima da P-039? |
| :- | -: | -: | -: | -: | -: | :- |
| lander | 3 190,4063 | 3 190,4187 | 1,24e−02 | 4,11e−06 | 4,59e−02 | sim |
| orbitador | 6 506,2454 | 6 506,2515 | 6,15e−03 | 2,64e−06 | 3,40e−02 | sim |
| mav | 348,1270 | 348,1263 | −6,33e−04 | 6,79e−06 | 2,93e−03 | sim |
| lander_4_5 | 3 154,7184 | 3 154,7032 | −1,52e−02 | 2,15e−06 | 4,05e−02 | sim |

**Tanques de descida:** distância do centro ao eixo: 1,400000000000000; 1,399999999999815; 1,399999999999815 m; maior diferença de 1,85e−13 m. z e raio iguais. Os tanques 2 e 3 são espelhos, bit a bit. O tanque 1 não fica igual a eles bit a bit: a coordenada y dos outros dois, 1,4 · sen 120°, é arredondada a 13 algarismos significativos em decimal.

## Parâmetros de desempate

`empate_m` = 1,00e−09 m; `casas_de_ordem` = 9, em casas decimais de metro. Valor e justificativa em config/cad.yaml.

| Item | Valor (m) | Limite (m) | Onde |
| :- | -: | -: | :- |
| (a) maior diferença entre peças exatamente simétricas | 1,85e−13 | ≤ 1,00e−12 | Propelente descida 1; Propelente descida 2 (lander_4_5, envelope_vulcan.fs, leitura 1, radial) |
| (b) menor diferença real entre peças distintas | 1,51e−04 | ≥ 1,00e−06 | Propelente cruzeiro MON-3; Propelente cruzeiro MMH (lander_4_5, envelope_vulcan.fs, leitura 1, axial) |
| (b'), só os pares que decidem texto gerado: o limitador contra o seguinte, e a lista de peças contra a cápsula | 1,10e−02 | ≥ 1,00e−06 | Tanque insercao MMH 1; Propelente insercao MON-3 1 (orbitador, envelope_falcon_heavy.fs, leitura 1, radial) |

**Resultado, com (a) e (b) literais: passa nos dois, aprovação registrada em config/cad.yaml.** Grupos de peças distintas com a mesma cota, até `empate_m`: Braço de coleta (guardado) × Casca traseira 1 (SLA-561V) × MAV interestágio; Casca traseira 1 (SLA-561V) × Escudo térmico (PICA); MAV Tanque de combustível do estágio 1 × MAV Tanque de combustível do estágio 2 × MAV Tanque de oxidante do estágio 1 × MAV Tanque de oxidante do estágio 2 × MAV carga (contêiner de amostras) × MAV motores do estágio 1 (4 x R-4D-11); MAV carga (contêiner de amostras) × MAV motores do estágio 1 (4 x R-4D-11); MAV propelente combustível do estágio 1 × MAV propelente combustível do estágio 2 × MAV propelente oxidante do estágio 1 × MAV propelente oxidante do estágio 2.

## Planos da interface

- **Vulcan, com fonte:** [F80] Fig. 4.3.1-1, p. 4-8: "LV STA 2596.66 (1575 Interface)".
- **Falcon, sem fonte direta:** [F82] PDF p. 26: "The origin of the payload coordinate system is fixed at the center of the separation plane"; o arquivo STEP não declara que usa esse sistema (P-096).
- **Veículos, sem fonte:** z = 0 do modelo. Um adaptador real subiria o veículo; não há altura com fonte para ele. Na primeira leitura do Vulcan, cada metro de altura tira 0,0173 m de folga radial.

## Premissas propostas (não entraram em config/premissas.yaml; pendentes do Fabio)

| Id | Texto | Evidência |
| :- | :- | :- |
| P-097 | A base dos veículos (z = 0 do modelo) fica no plano da interface, sem altura de adaptador nem de sistema de separação. | Convenção do modelo desde a Etapa 7.1, sem fonte; a P-091 não trata disso. Um adaptador real sobe o veículo, e o envelope afunila com a altura; [F82] PDF p. 27: "Any payload adapters required ... must also fit within the keep-in volumes". |

A espessura de 0,01 m da casca é escolha de construção, sem efeito nas folgas. Os arquivos .fs não foram compilados nesta máquina: a compilação é o primeiro passo do roteiro.
