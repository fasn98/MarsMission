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

Os resultados de `results/etapa7.2` não foram alterados: corrigir esses números e registrar a errata é decisão do Fabio.

**Orbitador:** a Etapa 7.2 dá +0,356 m (Tanques de inserção), porque trata cada conjunto como um cilindro no raio máximo. Aqui as esferas têm a forma real, e a folga é maior. As duas contas respondem a perguntas diferentes, e a da 7.2 fica do lado seguro.

## O que os arquivos têm

| Arquivo | Veículo | Corpos | Massa (kg) | CG x, y, z (m) | Mate connector preso a |
| :- | :- | -: | -: | :- | :- |
| lander_4_65.fs | lander_4_65 | 33 | 3 190,406 | 0,0256, −0,0263, 3,0032 | Circuito de fluido de cruzeiro (P-077) |
| lander_4_5.fs | lander_4_5 | 33 | 3 154,718 | 0,0259, −0,0266, 2,0985 | Circuito de fluido de cruzeiro (P-077) |
| orbitador.fs | orbitador | 20 | 6 506,245 | 0,0000, 0,0000, 1,3928 | Cilindro central |

**O que mudou em relação a `results/etapa7.2/orbitador.fs` e `lander.fs`:** a versão do cabeçalho, de 2737 para 3112; a constante `DONO_INTERFACE`; e o bloco `opMateConnector` no fim da feature. A lista CORPOS é a mesma (`tests/test_cad.py` confere), então massa e CG não mudam. O `mav.fs` não muda: o MAV não tem interface com o adaptador.

**`lander_4_5.fs` é um modelo novo:** cápsula MSL/M2020 e o resto do arranjo igual, com a massa acima. O MAV deitado não cabe nesta cápsula (folga de −0,188 m com a base na estação 0,85 m), então ele atravessa a casca traseira no modelo. Isso é o conflito do aeroshell, visível no Onshape, e não um erro do arquivo.

## Planos da interface

- **Vulcan, com fonte:** [F80] Fig. 4.3.1-1, p. 4-8: "LV STA 2596.66 (1575 Interface)".
- **Falcon, sem fonte direta:** [F82] PDF p. 26: "The origin of the payload coordinate system is fixed at the center of the separation plane"; o arquivo STEP não declara que usa esse sistema (P-096 proposta).
- **Veículos, sem fonte:** z = 0 do modelo. Um adaptador real subiria o veículo; não há altura com fonte para ele. Na primeira leitura do Vulcan, cada metro de altura tira 0,0173 m de folga radial.

## Premissas propostas (não entraram em config/premissas.yaml; pendentes do Fabio)

| Id | Texto | Evidência |
| :- | :- | :- |
| P-096 | A origem do STEP de keep-in do Falcon é o plano da interface de 1575 mm, com o eixo x axial. | [F82] PDF p. 26 define a origem do sistema da carga útil no plano de separação; o topo do arquivo, em 446,76 pol, é coerente com o guia. O arquivo não declara o sistema, e separação e interface podem não coincidir. |
| P-097 | A base dos veículos (z = 0 do modelo) fica no plano da interface, sem altura de adaptador nem de sistema de separação. | Convenção do modelo desde a Etapa 7.1, sem fonte; a P-091 não trata disso. Um adaptador real sobe o veículo, e o envelope afunila com a altura. |

A espessura de 0,01 m da casca é escolha de construção, sem efeito nas folgas. Os arquivos .fs não foram compilados nesta máquina: a compilação é o primeiro passo do roteiro.
