# Etapa 7.2: parâmetros do CAD e conferências (gerado por tools/cad_parametros.py)

Escolhas (ADR 0022): aeroshell srl_duplo, MAV restricao_2019, 2 pares de tanques por estágio.

## Lander no Vulcan com o perfil real da cápsula (sem a P-083)

Perfis lidos de [F41] Fig. 2 (P-089); frente para cima e estágio de cruzeiro de 0,12 m além da cápsula (P-091).

| Forma | Raio máximo | Comprimento | Menor folga radial ao envelope do Vulcan | Sem o afunilamento linear entre as cotas |
| :- | -: | -: | -: | -: |
| MSL/M2020 (Ø 4,5 m) | 2,26 | 2,88 | 0,143 | 0,065 |
| SRL-A | 2,34 | 3,85 | 0,047 | −0,014 |
| SRL-C | 2,36 | 3,55 | 0,032 | −0,034 |

Envelope do Vulcan: [F80] Fig. 4.3.1-1 ("Simplified"), cotas de diâmetro nas estações; entre elas o contorno desenhado é reto, e a interpolação é linear. A última coluna supõe o diâmetro menor (o da estação de cima) desde o plano do PAF.

Forma usada no CAD: SRL-A.

## MAV deitado contra a casca traseira (Ø 0,57 m, 3,56 m; folga interna de 0,25 m, P-087)

Comprimento máximo do MAV deitado com a base na estação dada (distância ao nariz), pelo raio interno no topo do MAV.

| Estação da base | MSL/M2020 (Ø 4,5 m) | SRL-A | SRL-C |
| -: | -: | -: | -: |
| 0,85 | 3,18 (não cabe) | 3,60 (cabe) | 3,62 (cabe) |
| 0,95 | 3,04 (não cabe) | 3,49 (não cabe) | 3,51 (não cabe) |
| 1,05 | 2,89 (não cabe) | 3,39 (não cabe) | 3,40 (não cabe) |
| 1,15 | 2,74 (não cabe) | 3,29 (não cabe) | 3,30 (não cabe) |
| 1,25 | 2,60 (não cabe) | 3,18 (não cabe) | 3,19 (não cabe) |
| 1,35 | 2,41 (não cabe) | 3,08 (não cabe) | 3,08 (não cabe) |
| 1,45 | 2,08 (não cabe) | 2,96 (não cabe) | 2,97 (não cabe) |

## Errata (2026-11-04, aprovada pelo Fabio): folgas do lander no Vulcan

**O que muda:** as folgas da primeira tabela valem menos do que está escrito. **Causa:** o cálculo amostra o perfil da cápsula em 400 pontos, e nenhum cai no vértice do ombro, onde o raio é máximo. Os valores vigentes são os da coluna "Vigente", calculados nos vértices do perfil. Os antigos ficam como registro.

| Forma | Leitura do envelope | Publicado (grade de 400 pontos) | Vigente (vértices) | Diferença (mm) |
| :- | :- | -: | -: | -: |
| MSL/M2020 (Ø 4,5 m) | contorno reto | 0,1425 | 0,1412 | −1,3 |
| MSL/M2020 (Ø 4,5 m) | Ø menor desde o PAF | 0,0653 | 0,0640 | −1,3 |
| SRL-A | contorno reto | 0,0466 | 0,0444 | −2,2 |
| SRL-A | Ø menor desde o PAF | −0,0138 | −0,0160 | −2,2 |
| SRL-C | contorno reto | 0,0319 | 0,0296 | −2,3 |
| SRL-C | Ø menor desde o PAF | −0,0338 | −0,0360 | −2,2 |

## Errata (2026-11-06, decisão do Fabio): 12 algarismos nos arquivos .fs

**O que muda:** toda a geometria e as densidades vão para os .fs com 12 algarismos significativos, antes 6. Massa, CG e inércia desta página mudam por isso; os valores vigentes são os mostrados aqui, e a comparação 6 × 12 algarismos está em results/etapa7.2b/folgas.md. A conferência no Onshape continua valendo para o commit 32cb41d: ela lê as cópias em tests/data/onshape/, que não mudam.

## Orbitador no Falcon (com a plataforma e o EES no arranjo do CAD)

| Conjunto | Base | Topo | Raio | Folga radial |
| :- | -: | -: | -: | -: |
| Tanques de inserção | 0,00 | 1,12 | 1,96 | 0,36 |
| Tanques de retorno | 1,22 | 2,13 | 1,75 | 0,56 |
| Plataforma | 2,23 | 2,53 | 1,74 | 0,56 |
| CCRS | 2,63 | 4,63 | 1,72 | 0,57 |
| EES | 4,63 | 5,12 | 0,64 | 1,65 |

## Massa e CG esperados do CAD (pelos volumes dos primitivos; para conferir o Onshape)

| Veículo | Corpos | Massa do CAD | Geometria modelada | Propelente | Densidade equivalente (orçamento) | CG (x, y, z) |
| :- | -: | -: | -: | -: | -: | :- |
| orbitador | 20 | 6 506,3 | 263,3 | 4 919,1 | 1 323,9 | 0,000, 0,000, 1,393 |
| lander | 33 | 3 190,4 | 330,0 | 943,5 | 1 916,9 | 0,026, −0,026, 3,003 |
| mav | 12 | 348,1 | 25,1 | 285,5 | 37,5 | 0,000, 0,000, 1,540 |

Geometria modelada: tanques, cilindro central, escudo térmico (PICA [F223]) e casca traseira (SLA-561V, densidade da P-090), com espessuras das fontes [F215, F225] ou da P-093.

Orçamento (results/etapa2.5/arquitetura.yaml): orbitador 7 796 kg, lander 4 615 kg, MAV 386,8 kg. A diferença (estrutura, motores e peças sem geometria nesta etapa) é assunto da Etapa 7.3; nada é ajustado.

Arquivos para o Onshape: orbitador.fs, lander.fs e mav.fs (instruções em docs/etapa7.2_featurescript.md).
