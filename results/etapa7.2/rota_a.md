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

**CAD atual (forma SRL-A):** núcleo do lander entre 0,55 e 0,85 m do nariz, raio 1,33 m. Na frente do núcleo, a face externa da cápsula tem raio 1,58 m: sobram 0,25 m, com escudo de 0,032 m. **Cabe na geometria.**

| Item | O que a fonte diz | Fonte |
| :- | :- | :- |
| Ordem axial do MSL | de cima para baixo: estágio de cruzeiro, casca traseira, paraquedas, estágio de descida, BUD, rover, escudo | [F244] Fig. 1, PDF p. 2; [F214] PDF p. 35, vista expandida |
| Rover e estágio de descida no aeroshell | o aeroshell contém os dois | [F244] PDF p. 1: "The 4.5 m aeroshell is composed of a heatshield and backshell, and contains the DS and rover." |
| Separação do escudo | sem o escudo, rover e estágio de descida ficam expostos | [F244] PDF p. 2: "the heatshield is jettisoned to expose the both the DS and rover"; [F227] PDF p. 6: "exposes the stowed rover and descent stage to free-stream conditions" |
| Estágio de descida e casca | o estágio de descida fica aninhado na casca traseira | [F244] PDF p. 9: "with the PDV nested inside the backshell" |
| Mars 2020 | "quase idêntico" ao MSL na viagem, sem cotas nem corte; não prova o arranjo interno | [F245] PDF p. 37: "Perseverance is traveling to Mars in an almost identical way to NASA's Curiosity rover" |
| Cotas internas | não achadas: corte, altura da pilha, distância ao ombro, ou se o rover entra na parte cônica do escudo | procurado em [F244], [F214], [F245], [F227], [F226], [F215] e [F232] |

**O que dá para dizer:** no MSL, o que vai à superfície fica do lado do escudo, e o estágio de descida do lado da casca traseira, então ter o conjunto do lander à frente do ombro não contraria a ordem do MSL. **O que não dá:** confirmar a viabilidade. Não há cota interna nas fontes lidas, e o nosso arranjo é outro: o MAV deitado fica atrás do núcleo, e os tanques de descida atravessam a casca (results/etapa7.2b/folgas.md). Viabilidade funcional não conferida: abertura e separação do escudo, propulsão de descida e pernas.

## 3. Isp mínimo do 44:1, com deck e folga de ao menos +0,05 m

Comprimento máximo: 2,644 m, em Ø 0,57 m. MAV redimensionado para cada Isp, nos dois estágios.

| Comprimento usado | Isp mínimo (s) |
| :- | -: |
| Tanques aninhados, limite otimista | 310,6 |
| Tanques dimensionados, vão de 0,02 m, fator de flambagem 1,00 (NÃO VALIDADO) | 313,5 |
| Tanques dimensionados, vão de 0,02 m, fator de flambagem 0,50 (NÃO VALIDADO) | 313,5 |
| Tanques dimensionados, vão de 0,02 m, fator de flambagem 0,25 (NÃO VALIDADO) | 313,6 |
| Tanques dimensionados, vão de 0,02 m, fator de flambagem 0,14 (NÃO VALIDADO) | 313,7 |
| Tanques dimensionados, vão de 0,005 m, fator de flambagem 0,14 (NÃO VALIDADO) | 311,8 |

Os valores de Isp conhecidos são só análogos (results/etapa7.2/rotas_mav.md). O Isp do 44:1 do R-4D-11 segue sem fonte.

## 4. Tanques aninhados dimensionados

Ti-6Al-4V recozido, base A: Ftu 924 MPa, Fty 869 MPa ([F219]). Fator de 2,0: [F46] PDF p. 9: "A factor of safety of 2.0 was used for tank internal pressure." (tanque compósito; ANSI/AIAA S-080 não aberta). Tensão admissível: 462 MPa. Raio interno 0,275 m. A P-093 usa 1,5 mm. **fórmula clássica da casca esférica sob pressão externa, p = 2 E (t/R)² / √(3(1 − ν²)); NASA SP-8032 não pôde ser aberta. Fórmula e fatores NÃO VALIDADOS.**

**Pressão e espessura mínima (mm):**

| Pressão | MPa | Cilindro | Cúpula normal | Cúpula invertida, fator 1,00 | Cúpula invertida, fator 0,50 | Cúpula invertida, fator 0,25 | Cúpula invertida, fator 0,14 | Fonte |
| :- | -: | -: | -: | -: | -: | -: | -: | :- |
| entrada_nominal_r4d11 | 1,40 | 0,83 | 0,42 | 1,23 | 1,75 | 2,47 | 3,30 | [F228] PDF p. 22: "Inlet Pressure* ... >14 bar (>205 psia)" |
| bowles_20_kg | 1,30 | 0,77 | 0,39 | 1,19 | 1,68 | 2,38 | 3,18 | [F46] Tab. 5, PDF p. 34: "Tank Pressure ... 1.30 MPa (188 psi)" |
| entrada_maxima_r4d11 | 2,93 | 1,74 | 0,87 | 1,79 | 2,53 | 3,57 | 4,77 | [F228] PDF p. 22: "Inlet Pressure Range ... 4.1 – 29.3 bar (60 – 425 psia)" |

**Comprimento e massa,** em Ø 0,57 m, com a pressão nominal, vão de 0,02 m (NÃO VALIDADO: [F46] §5.4, PDF p. 17: "with a purge gap between the two tanks"; a fonte não dá o valor: varredura sem fonte, NÃO VALIDADO) e fator de flambagem 0,14. O comprimento real soma, por estágio, o vão e as duas paredes da antepara.

| Isp (s) | Só 44:1 (m) | Limite otimista (m) | Real (m) | Redução no limite (m) | Redução real (m) | Sobra da redução | Folga, com deck (m) | Folga, sem deck (m) | Tanques (kg) |
| -: | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| 304 | 3,260 | 2,763 | 2,813 | 0,496 | 0,447 | 90 % | −0,035 | +0,185 | 35,3 |
| 308 | 3,181 | 2,688 | 2,738 | 0,492 | 0,443 | 90 % | +0,003 | +0,223 | 34,2 |
| 309 | 3,162 | 2,671 | 2,721 | 0,492 | 0,442 | 90 % | +0,012 | +0,232 | 33,9 |
| 314 | 3,077 | 2,590 | 2,639 | 0,487 | 0,437 | 90 % | +0,052 | +0,272 | 32,7 |

Massa dos tanques em série hoje: 19,9 kg, na espessura da P-093. A massa do orçamento do MAV vem da fração estrutural, então esta conta não muda o GLOM.

**Sensibilidade do comprimento real (m) ao vão de purga:**

| Isp (s) | 0,005 m | 0,010 m | 0,020 m | 0,050 m |
| -: | -: | -: | -: | -: |
| 304 | 2,783 | 2,793 | 2,813 | 2,873 |
| 308 | 2,708 | 2,718 | 2,738 | 2,798 |
| 309 | 2,691 | 2,701 | 2,721 | 2,781 |
| 314 | 2,609 | 2,619 | 2,639 | 2,699 |

**Não dimensionado:** cargas de lançamento e de subida, fadiga e fratura, soldas, espessura mínima de fabricação, e o vão como peça. A fonte tem cúpula de excentricidade 0,707 em tanques de alta pressão ([F46] PDF p. 9), que encurtaria mais; aqui seguem os hemisférios da P-085.

## 5. P-097: folgas nas coifas com a altura do adaptador

Ressalvas: [F80] PDF p. 40: "should be used only as a guideline"; a tabela não dá capacidade por massa, e há envelope específico por adaptador (PDF p. 38-39: "Static payload envelopes specific to each payload adapter and separation system are available"). [F82] não publica altura de adaptador: PDF p. 27: "Any payload adapters required ... must also fit within the keep-in volumes"; aqui entra a mesma altura, por análogo. Limite do PAF de 1575 mm: PDF p. 28, "up to 10,885 kg".

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

**P-097 reformulada, para nova decisão:** Entre o plano da interface de 1575 mm e a base dos veículos há um adaptador com sistema de separação, de altura 0,127 m, e os veículos sobem essa altura em relação ao envelope. Fonte da altura: [F80] Tab. 4.2.2-1a. Falcon: sem altura publicada, mesma altura por análogo. A capacidade para as massas dos veículos não foi conferida, e os 43 kg do adaptador não estão no orçamento.
