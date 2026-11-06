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

Colunas: a geometria do estágio 2 (seção 4), que é uma escolha do Fabio. **recesso_hemisferio**: esfera em recesso de outra, recesso de até um hemisfério; **recesso_livre**: esfera em recesso de outra, sem limite de recesso (um recesso além do hemisfério prende a esfera); **antepara_assimetrica**: esfera de volume somado, dividida no equador por antepara de calota (lente e tigela); **lente_mesmo_raio**: esfera de volume somado, com antepara do mesmo raio e borda fora do equador (lente e crescente, com canto vivo na borda).

Limite otimista, sem tanques dimensionados: 310,6 s.

| Vão (m) | Fator de flambagem (NÃO VALIDADO) | recesso_hemisferio | recesso_livre | antepara_assimetrica | lente_mesmo_raio |
| -: | -: | -: | -: | -: | -: |
| 0,020 | 1,00 | 316,13 | 313,73 | 313,46 | 313,46 |
| 0,020 | 0,50 | 316,15 | 313,76 | 313,50 | 313,50 |
| 0,020 | 0,25 | 316,21 | 313,86 | 313,59 | 313,59 |
| 0,020 | 0,14 | 316,27 | 313,98 | 313,70 | 313,70 |
| 0,005 | 0,14 | 315,11 | 311,92 | 311,79 | 311,79 |
| 0,050 | 0,14 | 318,97 | 318,25 | 317,81 | 317,81 |

Os valores de Isp conhecidos são só análogos (results/etapa7.2/rotas_mav.md). O Isp do 44:1 do R-4D-11 segue sem fonte. Os análogos de 306 a 314 s têm câmara de irídio e rênio, ou, em [F240], só o resumo cita essa tecnologia. Na faixa de 306 a 314 s: esfera em recesso de outra, recesso de até um hemisfério: 0 de 6 linhas dentro da faixa; esfera em recesso de outra, sem limite de recesso (um recesso além do hemisfério prende a esfera): 5 de 6 linhas dentro da faixa; esfera de volume somado, dividida no equador por antepara de calota (lente e tigela): 5 de 6 linhas dentro da faixa; esfera de volume somado, com antepara do mesmo raio e borda fora do equador (lente e crescente, com canto vivo na borda): 5 de 6 linhas dentro da faixa.

**Fixada a geometria, estes valores são um piso quanto à massa.** O MAV redimensionado usa a fração estrutural fixa e não recebe a massa dos tanques da seção 4; se o inerte estourar, o MAV cresce e o Isp mínimo sobe. A geometria muda em que lado da faixa dos análogos o valor cai, e por isso a conclusão depende dela.

## 4. Tanques aninhados dimensionados

Ti-6Al-4V recozido, base A: Ftu 924 MPa, Fty 869 MPa ([F219]). Fator de 2,0: [F46] PDF p. 9: "A factor of safety of 2.0 was used for tank internal pressure." (tanque compósito; ANSI/AIAA S-080 não aberta). Tensão admissível: 462 MPa. Na flambagem, fator de 2,0: sem fonte, NÃO VALIDADO: a citação de [F46] PDF p. 9 é só para pressão interna; aqui se repete o mesmo valor na pressão externa da cúpula invertida; t varia com a raiz do fator. Raio interno 0,275 m. A P-093 usa 1,5 mm. **fórmula clássica da casca esférica sob pressão externa, p = 2 E (t/R)² / √(3(1 − ν²)); NASA SP-8032 não pôde ser aberta. Fórmula e fatores NÃO VALIDADOS.**

**Pressão e espessura mínima (mm):**

| Pressão | MPa | Cilindro | Cúpula normal | Cúpula invertida, fator 1,00 | Cúpula invertida, fator 0,50 | Cúpula invertida, fator 0,25 | Cúpula invertida, fator 0,14 | Fonte |
| :- | -: | -: | -: | -: | -: | -: | -: | :- |
| entrada_piso_r4d11 | 1,40 | 0,83 | 0,42 | 1,23 | 1,75 | 2,47 | 3,30 | [F228] PDF p. 22: "Inlet Pressure* ... >14 bar (>205 psia)" (piso de entrada do motor; o tanque precisa de mais, com as perdas da linha) |
| camara_mais_25_pct | 0,93 | 0,55 | 0,28 | 1,01 | 1,42 | 2,01 | 2,69 | [F228] PDF p. 22: "Chamber Pressure* ... 7.45 bar (108 psia)" × 1,25; [F46] PDF p. 9: "tank pressure was 25% higher than the thrust chamber pressure" (fica abaixo do piso de entrada do motor) |
| bowles_20_kg | 1,30 | 0,77 | 0,39 | 1,19 | 1,68 | 2,38 | 3,18 | [F46] Tab. 5, PDF p. 34: "Tank Pressure ... 1.30 MPa (188 psi)" |
| entrada_maxima_r4d11 | 2,93 | 1,74 | 0,87 | 1,79 | 2,53 | 3,57 | 4,77 | [F228] PDF p. 22: "Inlet Pressure Range ... 4.1 – 29.3 bar (60 – 425 psia)" |

**Comprimento e massa,** em Ø 0,57 m, com o piso de entrada do motor, vão de 0,02 m (NÃO VALIDADO: [F46] §5.4, PDF p. 17: "with a purge gap between the two tanks"; a fonte não dá o valor: varredura sem fonte, NÃO VALIDADO) e fator de flambagem 0,14. O estágio 1 soma ao limite o vão e as duas paredes da antepara. No estágio 2, o volume cabe numa esfera menor que o diâmetro interno: uma antepara do mesmo raio dessa esfera, com a borda no equador, não deixa volume para o segundo tanque, e por isso há quatro geometrias, sem fonte e NÃO VALIDADAS.

| Isp (s) | Geometria do estágio 2 | Só 44:1 (m) | Limite otimista (m) | Real (m) | Redução no limite (m) | Redução real (m) | Sobra da redução | Folga, com deck (m) | Folga, sem deck (m) | Tanques (kg) |
| -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| 304 | recesso_hemisferio | 3,260 | 2,763 | 2,854 | 0,496 | 0,406 | 82 % | −0,055 | +0,165 | 33,8 |
| 304 | recesso_livre | 3,260 | 2,763 | 2,817 | 0,496 | 0,442 | 89 % | −0,037 | +0,183 | 36,7 |
| 304 | antepara_assimetrica | 3,260 | 2,763 | 2,813 | 0,496 | 0,447 | 90 % | −0,035 | +0,185 | 31,7 |
| 304 | lente_mesmo_raio | 3,260 | 2,763 | 2,813 | 0,496 | 0,447 | 90 % | −0,035 | +0,185 | 32,8 |
| 308 | recesso_hemisferio | 3,181 | 2,688 | 2,778 | 0,492 | 0,403 | 82 % | −0,017 | +0,203 | 32,8 |
| 308 | recesso_livre | 3,181 | 2,688 | 2,742 | 0,492 | 0,439 | 89 % | +0,001 | +0,221 | 35,6 |
| 308 | antepara_assimetrica | 3,181 | 2,688 | 2,738 | 0,492 | 0,443 | 90 % | +0,003 | +0,223 | 30,7 |
| 308 | lente_mesmo_raio | 3,181 | 2,688 | 2,738 | 0,492 | 0,443 | 90 % | +0,003 | +0,223 | 31,7 |
| 309 | recesso_hemisferio | 3,162 | 2,671 | 2,760 | 0,492 | 0,402 | 82 % | −0,008 | +0,212 | 32,5 |
| 309 | recesso_livre | 3,162 | 2,671 | 2,725 | 0,492 | 0,438 | 89 % | +0,010 | +0,230 | 35,3 |
| 309 | antepara_assimetrica | 3,162 | 2,671 | 2,721 | 0,492 | 0,442 | 90 % | +0,012 | +0,232 | 30,4 |
| 309 | lente_mesmo_raio | 3,162 | 2,671 | 2,721 | 0,492 | 0,442 | 90 % | +0,012 | +0,232 | 31,5 |
| 314 | recesso_hemisferio | 3,077 | 2,590 | 2,678 | 0,487 | 0,399 | 82 % | +0,033 | +0,253 | 31,4 |
| 314 | recesso_livre | 3,077 | 2,590 | 2,644 | 0,487 | 0,433 | 89 % | +0,050 | +0,270 | 34,0 |
| 314 | antepara_assimetrica | 3,077 | 2,590 | 2,639 | 0,487 | 0,437 | 90 % | +0,052 | +0,272 | 29,3 |
| 314 | lente_mesmo_raio | 3,077 | 2,590 | 2,639 | 0,487 | 0,437 | 90 % | +0,052 | +0,272 | 30,3 |

Massa dos tanques em série hoje: 19,9 kg, na espessura da P-093. A massa do orçamento do MAV vem da fração estrutural, então esta conta não muda o GLOM; por isso o confronto abaixo.

**Tanques contra o inerte, por estágio.** A sobra é o que resta no inerte para estrutura, pressurização e o resto. O motor é o de 164:1, porque o 44:1 não tem massa com fonte. O estágio 1 não depende da geometria.

| Isp (s) | Estágio | Geometria | Inerte (kg) | Tanques (kg) | Parcela | Motores 164:1 (kg) | Sobra (kg) |
| -: | -: | :- | -: | -: | -: | -: | -: |
| 304 | 1 | todas | 76,9 | 23,6 | 31 % | 15,0 | +38,3 |
| 304 | 2 | recesso_hemisferio | 17,1 | 10,3 | 60 % | 3,8 | +3,1 |
| 304 | 2 | recesso_livre | 17,1 | 13,2 | 77 % | 3,8 | +0,2 |
| 304 | 2 | antepara_assimetrica | 17,1 | 8,1 | 47 % | 3,8 | +5,3 |
| 304 | 2 | lente_mesmo_raio | 17,1 | 9,2 | 54 % | 3,8 | +4,2 |
| 308 | 1 | todas | 71,6 | 22,8 | 32 % | 15,0 | +33,8 |
| 308 | 2 | recesso_hemisferio | 16,4 | 10,0 | 61 % | 3,8 | +2,7 |
| 308 | 2 | recesso_livre | 16,4 | 12,8 | 78 % | 3,8 | −0,1 |
| 308 | 2 | antepara_assimetrica | 16,4 | 7,9 | 48 % | 3,8 | +4,8 |
| 308 | 2 | lente_mesmo_raio | 16,4 | 8,9 | 54 % | 3,8 | +3,7 |
| 309 | 1 | todas | 70,4 | 22,6 | 32 % | 15,0 | +32,7 |
| 309 | 2 | recesso_hemisferio | 16,3 | 9,9 | 61 % | 3,8 | +2,6 |
| 309 | 2 | recesso_livre | 16,3 | 12,7 | 78 % | 3,8 | −0,2 |
| 309 | 2 | antepara_assimetrica | 16,3 | 7,8 | 48 % | 3,8 | +4,7 |
| 309 | 2 | lente_mesmo_raio | 16,3 | 8,9 | 55 % | 3,8 | +3,6 |
| 314 | 1 | todas | 64,7 | 21,8 | 34 % | 15,0 | +27,9 |
| 314 | 2 | recesso_hemisferio | 15,5 | 9,6 | 62 % | 3,8 | +2,1 |
| 314 | 2 | recesso_livre | 15,5 | 12,3 | 79 % | 3,8 | −0,6 |
| 314 | 2 | antepara_assimetrica | 15,5 | 7,6 | 49 % | 3,8 | +4,1 |
| 314 | 2 | lente_mesmo_raio | 15,5 | 8,6 | 56 % | 3,8 | +3,1 |

**As quatro geometrias do estágio 2.** **recesso_hemisferio**: esfera em recesso de outra, recesso de até um hemisfério; **recesso_livre**: esfera em recesso de outra, sem limite de recesso (um recesso além do hemisfério prende a esfera); **antepara_assimetrica**: esfera de volume somado, dividida no equador por antepara de calota (lente e tigela); **lente_mesmo_raio**: esfera de volume somado, com antepara do mesmo raio e borda fora do equador (lente e crescente, com canto vivo na borda). As espessuras seguem as do raio interno, e nenhuma é um dimensionamento. Com recesso, o fundo do recesso não foi analisado. Em **antepara_assimetrica**, a calota fica quase plana, com o vão praticamente constante: a espessura de flambagem no raio da calota, na tabela, está fora do domínio da fórmula da casca esférica, uma calota tão rasa trabalha como placa, e a flexão de placa não foi calculada. O comprimento e a massa dessa coluna usam a espessura do raio interno, então são otimistas. Em **lente_mesmo_raio**, a antepara tem o raio da esfera e o canto vivo na borda não foi analisado.

| Isp (s) | Tanque único (m) | recesso_hemisferio (m) | recesso_livre (m) | antepara_assimetrica (m) | lente_mesmo_raio (m) | Raio da calota, antepara (m) | Flambagem nesse raio, fora do domínio (mm) | Raio da esfera e raio da borda, lente (m) |
| -: | -: | -: | -: | -: | -: | -: | -: | -: |
| 304 | 0,465 | 0,530 | 0,494 | 0,489 | 0,489 | 87,57 | 1 050,7 | 0,232 e 0,218 |
| 308 | 0,458 | 0,523 | 0,487 | 0,483 | 0,483 | 86,35 | 1 035,9 | 0,229 e 0,215 |
| 309 | 0,457 | 0,521 | 0,486 | 0,481 | 0,481 | 86,05 | 1 032,4 | 0,228 e 0,214 |
| 314 | 0,449 | 0,513 | 0,478 | 0,474 | 0,474 | 84,62 | 1 015,3 | 0,224 e 0,210 |

**Sensibilidade do comprimento real (m) ao vão de purga:**

| Isp (s) | Geometria | 0,005 m | 0,010 m | 0,020 m | 0,050 m |
| -: | :- | -: | -: | -: | -: |
| 304 | recesso_hemisferio | 2,837 | 2,842 | 2,854 | 2,892 |
| 304 | recesso_livre | 2,785 | 2,796 | 2,817 | 2,879 |
| 304 | antepara_assimetrica | 2,783 | 2,793 | 2,813 | 2,873 |
| 304 | lente_mesmo_raio | 2,783 | 2,793 | 2,813 | 2,873 |
| 308 | recesso_hemisferio | 2,761 | 2,766 | 2,778 | 2,816 |
| 308 | recesso_livre | 2,710 | 2,721 | 2,742 | 2,804 |
| 308 | antepara_assimetrica | 2,708 | 2,718 | 2,738 | 2,798 |
| 308 | lente_mesmo_raio | 2,708 | 2,718 | 2,738 | 2,798 |
| 309 | recesso_hemisferio | 2,743 | 2,749 | 2,760 | 2,798 |
| 309 | recesso_livre | 2,693 | 2,704 | 2,725 | 2,787 |
| 309 | antepara_assimetrica | 2,691 | 2,701 | 2,721 | 2,781 |
| 309 | lente_mesmo_raio | 2,691 | 2,701 | 2,721 | 2,781 |
| 314 | recesso_hemisferio | 2,661 | 2,666 | 2,678 | 2,716 |
| 314 | recesso_livre | 2,612 | 2,622 | 2,644 | 2,706 |
| 314 | antepara_assimetrica | 2,609 | 2,619 | 2,639 | 2,699 |
| 314 | lente_mesmo_raio | 2,609 | 2,619 | 2,639 | 2,699 |

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
