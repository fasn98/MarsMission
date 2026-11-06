# Portão do comprimento do MAV: rota A provisória (gerado por tools/rota_a_dimensiona.py)

Dados para decisão do Fabio (ADR 0023). A rota A não está aplicada ao CAD nem às premissas. O que não tem fonte fica em varredura e está marcado NÃO VALIDADO.

## 1. Alvo com deck

Com as 4 saídas de 44:1 (0,369 m, com parede de 0,01 m de cada lado), o menor Ø da varredura é 0,57 m: limite de 2,74 m com deck; 3,18 m sem deck, que fica como limite otimista. Com 164:1 (0,675 m), o Ø cresce e o limite cai.

| Ø (m) | Limite com deck (m) | Limite sem deck (m) |
| -: | -: | -: |
| 0,57 | 2,74 | 3,18 |
| 0,60 | 2,70 | 3,14 |
| 0,63 | 2,66 | 3,10 |
| 0,66 | 2,61 | 3,05 |
| 0,69 | 2,57 | 3,01 |
| 0,72 | 2,52 | 2,96 |
| 0,75 | 2,48 | 2,92 |

## 2. O arranjo atual do CAD é viável? Comparação com o MSL e o Mars 2020

**CAD atual:** núcleo do lander na forma SRL-A, entre 0,55 e 0,85 m do nariz, raio 1,33 m, com face externa de raio 1,58 m na frente dele: sobram 0,25 m; na forma MSL/Mars 2020 (o alvo de 4,5 m), entre 0,55 e 0,85 m do nariz, raio 1,28 m, com face externa de raio 1,53 m na frente dele: sobram 0,25 m, com escudo de 0,032 m. **Cabe na geometria, mas por construção:** o raio do núcleo é o da cápsula menos a folga interna (tools/cad_parametros.py), então essa sobra não é uma verificação independente.

| Item | O que a fonte diz | Fonte |
| :- | :- | :- |
| Ordem axial do MSL | de cima para baixo: estágio de cruzeiro, casca traseira, paraquedas, estágio de descida, BUD, rover, escudo | [F244] Fig. 1, PDF p. 2; [F214] PDF p. 35, vista expandida |
| Rover e estágio de descida no aeroshell | o aeroshell contém os dois | [F244] PDF p. 1: "The 4.5 m aeroshell is composed of a heatshield and backshell, and contains the DS and rover." |
| Separação do escudo | sem o escudo, rover e estágio de descida ficam expostos | [F244] PDF p. 2: "the heatshield is jettisoned to expose the both the DS and rover"; [F227] PDF p. 6: "exposes the stowed rover and descent stage to free-stream conditions" |
| Estágio de descida e casca | o estágio de descida fica aninhado na casca traseira | [F244] PDF p. 9: "with the PDV nested inside the backshell" |
| Mars 2020 | "quase idêntico" ao MSL na viagem, sem cotas nem corte; não prova o arranjo interno | [F45] PDF p. 37: "Perseverance is traveling to Mars in an almost identical way to NASA's Curiosity rover" |
| Cotas internas | não achadas: corte, altura da pilha, distância ao ombro, ou se o rover entra na parte cônica do escudo | procurado em [F244], [F214], [F45], [F227], [F226], [F215] e [F232] |

**O que dá para dizer:** no MSL, o que vai à superfície fica do lado do escudo, e o estágio de descida do lado da casca traseira, então ter o conjunto do lander à frente do ombro não contraria a ordem do MSL. **O que não dá:** confirmar a viabilidade. Não há cota interna nas fontes lidas, e o nosso arranjo é outro: o MAV deitado fica atrás do núcleo, e os tanques de descida atravessam a casca (results/etapa7.2b/folgas.md). Viabilidade funcional não conferida: abertura e separação do escudo, propulsão de descida e pernas.

## 3. Isp mínimo do 44:1, com deck e folga de ao menos +0,05 m

Comprimento máximo: 2,644 m, em Ø 0,57 m. MAV redimensionado para cada Isp, nos dois estágios.

| Comprimento usado | Isp mínimo (s) |
| :- | -: |
| Tanques aninhados, limite otimista | 310,6 |
| Tanques dimensionados, vão de 0,02 m, fator de flambagem 1,00 (NÃO VALIDADO) | 316,2 |
| Tanques dimensionados, vão de 0,02 m, fator de flambagem 0,50 (NÃO VALIDADO) | 316,2 |
| Tanques dimensionados, vão de 0,02 m, fator de flambagem 0,25 (NÃO VALIDADO) | 316,2 |
| Tanques dimensionados, vão de 0,02 m, fator de flambagem 0,14 (NÃO VALIDADO) | 316,3 |
| Tanques dimensionados, vão de 0,005 m, fator de flambagem 0,14 (NÃO VALIDADO) | 315,2 |
| Tanques dimensionados, vão de 0,050 m, fator de flambagem 0,14 (NÃO VALIDADO) | 319,0 |

Os valores de Isp conhecidos são só análogos (results/etapa7.2/rotas_mav.md). O Isp do 44:1 do R-4D-11 segue sem fonte. Os análogos de 306 a 314 s têm câmara de irídio e rênio, ou, em [F240], só o resumo cita essa tecnologia. Com os tanques dimensionados, todos os valores da tabela ficam acima do topo dessa faixa; só o limite otimista fica dentro.

**Estes valores são um piso.** O MAV redimensionado usa a fração estrutural fixa e não recebe a massa dos tanques da seção 4; se o inerte estourar, o MAV cresce e o Isp mínimo sobe.

## 4. Tanques aninhados dimensionados

Ti-6Al-4V recozido, base A: Ftu 924 MPa, Fty 869 MPa ([F219]). Fator de 2,0: [F46] PDF p. 9: "A factor of safety of 2.0 was used for tank internal pressure." (tanque compósito; ANSI/AIAA S-080 não aberta). Tensão admissível: 462 MPa. Na flambagem, fator de 2,0: sem fonte, NÃO VALIDADO: a citação de [F46] PDF p. 9 é só para pressão interna; aqui se repete o mesmo valor na pressão externa da cúpula invertida; t varia com a raiz do fator. Raio interno 0,275 m. A P-093 usa 1,5 mm. **fórmula clássica da casca esférica sob pressão externa, p = 2 E (t/R)² / √(3(1 − ν²)); NASA SP-8032 não pôde ser aberta. Fórmula e fatores NÃO VALIDADOS.**

**Pressão e espessura mínima (mm):**

| Pressão | MPa | Cilindro | Cúpula normal | Cúpula invertida, fator 1,00 | Cúpula invertida, fator 0,50 | Cúpula invertida, fator 0,25 | Cúpula invertida, fator 0,14 | Fonte |
| :- | -: | -: | -: | -: | -: | -: | -: | :- |
| entrada_piso_r4d11 | 1,40 | 0,83 | 0,42 | 1,23 | 1,75 | 2,47 | 3,30 | [F228] PDF p. 22: "Inlet Pressure* ... >14 bar (>205 psia)" (piso de entrada do motor; o tanque precisa de mais, com as perdas da linha) |
| camara_mais_25_pct | 0,93 | 0,55 | 0,28 | 1,01 | 1,42 | 2,01 | 2,69 | [F228] PDF p. 22: "Chamber Pressure* ... 7.45 bar (108 psia)" × 1,25; [F46] PDF p. 9: "tank pressure was 25% higher than the thrust chamber pressure" (fica abaixo do piso de entrada do motor) |
| bowles_20_kg | 1,30 | 0,77 | 0,39 | 1,19 | 1,68 | 2,38 | 3,18 | [F46] Tab. 5, PDF p. 34: "Tank Pressure ... 1.30 MPa (188 psi)" |
| entrada_maxima_r4d11 | 2,93 | 1,74 | 0,87 | 1,79 | 2,53 | 3,57 | 4,77 | [F228] PDF p. 22: "Inlet Pressure Range ... 4.1 – 29.3 bar (60 – 425 psia)" |

**Comprimento e massa,** em Ø 0,57 m, com o piso de entrada do motor, vão de 0,02 m (NÃO VALIDADO: [F46] §5.4, PDF p. 17: "with a purge gap between the two tanks"; a fonte não dá o valor: varredura sem fonte, NÃO VALIDADO) e fator de flambagem 0,14. O comprimento real soma, no estágio 1, o vão e as duas paredes da antepara, e usa o esboço abaixo no estágio 2.

| Isp (s) | Só 44:1 (m) | Limite otimista (m) | Real (m) | Redução no limite (m) | Redução real (m) | Sobra da redução | Folga, com deck (m) | Folga, sem deck (m) | Tanques (kg) |
| -: | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| 304 | 3,260 | 2,763 | 2,855 | 0,496 | 0,405 | 82 % | −0,055 | +0,165 | 33,8 |
| 308 | 3,181 | 2,688 | 2,779 | 0,492 | 0,402 | 82 % | −0,017 | +0,203 | 32,7 |
| 309 | 3,162 | 2,671 | 2,761 | 0,492 | 0,402 | 82 % | −0,008 | +0,212 | 32,5 |
| 314 | 3,077 | 2,590 | 2,678 | 0,487 | 0,399 | 82 % | +0,033 | +0,253 | 31,4 |

Massa dos tanques em série hoje: 19,9 kg, na espessura da P-093. A massa do orçamento do MAV vem da fração estrutural, então esta conta não muda o GLOM; por isso o confronto abaixo.

**Tanques contra o inerte, por estágio.** A sobra é o que resta no inerte para estrutura, pressurização e o resto. O motor é o de 164:1, porque o 44:1 não tem massa com fonte.

| Isp (s) | Estágio | Inerte (kg) | Tanques (kg) | Parcela | Motores 164:1 (kg) | Sobra (kg) |
| -: | -: | -: | -: | -: | -: | -: |
| 304 | 1 | 76,9 | 23,6 | 31 % | 15,0 | +38,3 |
| 304 | 2 | 17,1 | 10,2 | 60 % | 3,8 | +3,2 |
| 308 | 1 | 71,6 | 22,8 | 32 % | 15,0 | +33,8 |
| 308 | 2 | 16,4 | 9,9 | 61 % | 3,8 | +2,7 |
| 309 | 1 | 70,4 | 22,6 | 32 % | 15,0 | +32,7 |
| 309 | 2 | 16,3 | 9,9 | 61 % | 3,8 | +2,6 |
| 314 | 1 | 64,7 | 21,8 | 34 % | 15,0 | +27,9 |
| 314 | 2 | 15,5 | 9,6 | 62 % | 3,8 | +2,1 |

**O estágio 2 usa um esboço, NÃO VALIDADO.** O volume somado cabe numa esfera menor que o diâmetro interno. Tanque único com antepara do mesmo raio não deixaria volume para o segundo tanque, então essa geometria não é realizável. O real põe uma esfera num recesso da outra, com o mesmo vão e as mesmas paredes, com recesso de, no máximo, um hemisfério (escolha do esboço, sem fonte; relaxá-la só pode encurtar, mas um recesso mais fundo prende a esfera), e procura o menor comprimento. Não é um dimensionamento: as espessuras seguem calculadas com o raio interno, e o fundo do recesso não foi analisado.

| Isp (s) | Esfera equivalente, irrealizável (m) | Esboço (m) | Raios: tanque ao redor e esfera (m) |
| -: | -: | -: | -: |
| 304 | 0,489 | 0,531 | 0,236 e 0,184 |
| 308 | 0,483 | 0,524 | 0,233 e 0,182 |
| 309 | 0,481 | 0,522 | 0,232 e 0,181 |
| 314 | 0,474 | 0,513 | 0,229 e 0,178 |

**Sensibilidade do comprimento real (m) ao vão de purga:**

| Isp (s) | 0,005 m | 0,010 m | 0,020 m | 0,050 m |
| -: | -: | -: | -: | -: |
| 304 | 2,838 | 2,843 | 2,855 | 2,892 |
| 308 | 2,761 | 2,767 | 2,779 | 2,816 |
| 309 | 2,743 | 2,750 | 2,761 | 2,798 |
| 314 | 2,661 | 2,667 | 2,678 | 2,717 |

**Não dimensionado:** cargas de lançamento e de subida, fadiga e fratura, soldas, espessura mínima de fabricação, e o vão como peça. A fonte tem cúpula de excentricidade 0,707 em tanques de alta pressão ([F46] PDF p. 9), que encurtaria mais; aqui seguem os hemisférios da P-085.

## 5. P-097: folgas nas coifas com a altura do adaptador

Ressalvas: [F80] PDF p. 40: "should be used only as a guideline"; a tabela não dá capacidade por massa, e há envelope específico por adaptador (PDF p. 38-39: "Static payload envelopes specific to each payload adapter and separation system are available"). [F82] não publica altura de adaptador. PDF p. 27: "Any payload adapters required (e.g., to achieve a 937-mm or 1,194-mm or 1,666-mm (36.89 in. or 47.01 or 65.59 in.) interface) must also fit within the keep-in volumes": a fonte não pede adaptador para um veículo com a própria interface de 1575 mm, então a mesma altura, por análogo, fica do lado seguro. Limite do PAF de 1575 mm: PDF p. 28, "up to 10,885 kg".

| Adaptador | Altura (m) | Massa (kg) | Fonte |
| :- | -: | -: | :- |
| 1575 mm, clampband | 0,127 | 43,0 | [F80] Tab. 4.2.2-1a, PDF p. 41: "1575 mm Payload Adapter and Separation System", "43 kg", "Height: 127 mm (5.00 in.)" |
| 1194 mm, clampband | 0,254 | 38,1 | [F80] Tab. 4.2.2-1a, PDF p. 41: "Height: 254.0 mm (10.00 in.)", "38.1 kg" |
| 1666 mm, clampband | 0,330 | 48,7 | [F80] Tab. 4.2.2-1a, PDF p. 41: "Height: 330.2 mm (13.00 in.)", "48.7 kg" |
| 937 mm, clampband | 0,406 | 46,4 | [F80] Tab. 4.2.2-1a, PDF p. 41: "Height: 406.4 mm (16.00 in.)", "46.4 kg" |
| 1663 mm, parafusos | 0,562 | 89,6 | [F80] Tab. 4.2.2-1a, PDF p. 41: "Height: 562 mm (22.126 in)", "89.6 kg" |

Folga radial mínima (m):

| Configuração | Leitura | Sem adaptador | 0,127 m | 0,254 m | 0,330 m | 0,406 m | 0,562 m |
| :- | :- | -: | -: | -: | -: | -: | -: |
| Lander 4,5 m | contorno reto | +0,141 | +0,139 | +0,137 | +0,135 | +0,134 | +0,131 |
| Lander 4,5 m | Ø menor | +0,064 | +0,064 | +0,064 | +0,064 | +0,064 | +0,064 |
| Lander 4,65 m | contorno reto | +0,044 | +0,042 | +0,040 | +0,039 | +0,037 | +0,035 |
| Lander 4,65 m | Ø menor | −0,016 | −0,016 | −0,016 | −0,016 | −0,016 | −0,016 |
| Orbitador no Falcon Heavy | keep-in | +0,361 | +0,360 | +0,359 | +0,358 | +0,357 | +0,356 |

Folga axial mínima (m):

| Configuração | Leitura | Sem adaptador | 0,127 m | 0,254 m | 0,330 m | 0,406 m | 0,562 m |
| :- | :- | -: | -: | -: | -: | -: | -: |
| Lander 4,5 m | contorno reto | +9,802 | +9,675 | +9,548 | +9,471 | +9,395 | +9,240 |
| Lander 4,5 m | Ø menor | +9,802 | +9,675 | +9,548 | +9,471 | +9,395 | +9,240 |
| Lander 4,65 m | contorno reto | +8,832 | +8,705 | +8,578 | +8,501 | +8,425 | +8,270 |
| Lander 4,65 m | Ø menor | +8,832 | +8,705 | +8,578 | +8,501 | +8,425 | +8,270 |
| Orbitador no Falcon Heavy | keep-in | +6,232 | +6,105 | +5,978 | +5,902 | +5,826 | +5,670 |

**P-097 reformulada, para nova decisão:** Entre o plano da interface de 1575 mm e a base dos veículos há um adaptador com sistema de separação, de altura 0,127 m, e os veículos sobem essa altura em relação ao envelope. Fonte da altura: [F80] Tab. 4.2.2-1a. Falcon: sem altura publicada, mesma altura por análogo, do lado seguro. A capacidade para as massas dos veículos não foi conferida, e os 43 kg do adaptador não estão no orçamento.
