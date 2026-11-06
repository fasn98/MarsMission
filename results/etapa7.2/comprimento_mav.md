# Portão da 7.2: o que define o comprimento do MAV (gerado por tools/comprimento_mav.py)

Investigação. Nenhuma premissa muda, a arquitetura não muda, e a decisão é do Fabio. O que é leitura de figura ou análogo está marcado NÃO VALIDADO.

## (a) P-086: o que as fontes dizem do MAV do MSR

| Item | O que foi achado | Fonte |
| :- | :- | :- |
| Comprimento total do MAV do MSR | limite de 2,99 m com Ø 0,5 m (SRC); 3,0 m com Ø 0,57 m (DAC-0.0); 2,8 m com Ø 0,57 m (2019). Nenhuma traz a divisão por elemento | [F35] p. 3; [F236] PDF p. 2; [F238] PDF p. 15 |
| Divisão por elemento | não há divisão completa em nenhuma das fontes consultadas; há uma figura sem cotas por trecho e cotas soltas, nas linhas abaixo | [F237] PDF p. 4; [F35]; [F236]; [F238] |
| Bocal aninhado | o 2º estágio tem o bocal dentro do interestágio, e isso aparece como risco na separação; a fonte não dá o comprimento aninhado | [F35] PDF p. 15: "the small clearances of the interstage hardware and the nested SRM2 nozzle"; [F236] PDF p. 13: "clearance of the nested second stage nozzle hardware" |
| Encurtar bocal e interestágio | o estudo troca Isp por comprimento no 2º estágio: cerca de 10 s a menos, num bocal de expansão 81 e Isp 293 s. A Fig. 10 tem o melhor ponto perto de −0,15 m no bocal, com GLOM cerca de 8 kg menor com o plano de separação na saída do bocal e 14 kg menor perto da flange, mas nesta segunda curva quase 12 kg já existem sem encurtar o bocal (leitura da figura, NÃO VALIDADO). Motor sólido, com o bocal aninhado desenhado no interestágio | [F238] PDF p. 10: "trading I sp for nozzle length"; "a significantly shorter inter-stage and nozzle"; Fig. 10, eixo "Nozzle Length change, m" |
| Motor do 1º estágio (MSR de 2019) | caixa do motor em três níveis de propelente, de 30,5 a 31,7 pol; é cota de um elemento, de motor sólido, sem o bocal completo, e não a divisão do veículo | [F238] PDF p. 12, Fig. 11: "525-lb prop, 31.7 inch case"; "475-lb prop, 30.5 inch case" |

**Não há fonte primária com a divisão por elemento.** A P-086 (1,50 m: motores_estagio_1 0,60, motor_estagio_2 0,45, interestagio 0,10, carga_os 0,35) continua sem fonte.

**Leitura proporcional da figura (NÃO VALIDADO):** [F237] PDF p. 4, figura "MAS Overview": "<3 m" (o rótulo "~0.5 m" é o diâmetro). A figura não declara escala; os trechos abaixo escalam a altura pelo limite de 2,99 m de [F35], que é um máximo. Motor sólido, Ø 0,50 m: outro veículo.

| Trecho | Fração da altura | Comprimento (m) |
| :- | -: | -: |
| Carga: coifa e carga útil (MPA) | 13,4 % | 0,40 |
| 2º estágio: motor sólido | 9,9 % | 0,30 |
| Interestágio, com o bocal do 2º estágio aninhado | 22,2 % | 0,66 |
| 1º estágio: motor sólido e rampa | 38,2 % | 1,14 |
| TVC e bocal do 1º estágio | 16,3 % | 0,49 |

**O que a leitura permite dizer:** o que fica fora do corpo dos motores no MSR (carga, interestágio com o bocal aninhado e aviônica, TVC e bocal do 1º estágio) soma cerca de 1,55 m, da mesma ordem da P-086. A diferença de comprimento entre os dois veículos está sobretudo na parte com propelente: cerca de 1,44 m de motores sólidos no MSR, contra 2,06 m de tanques no nosso. **O que não permite:** validar a P-086, porque os elementos não são equivalentes.

## (b) R-4D-11 44:1

**Não achado:** Isp, massa ou empuxo próprios do R-4D-11 44:1 em fonte primária. O comprimento sai do desenho de [F228]: 0,317 m, contra 0,554 m do 164:1.

**Onde se procurou:**
- [F228] PDF p. 22: 44:1 só nas cotas do desenho; sem Isp, massa ou empuxo próprios
- [F106] e [F107]: não citam 44:1 (conferido nas citações do repositório; [F106] sem cópia local)
- Busca no NTRS e na web por R-4D-11 com 44:1: [F239] e [F240] são os mais próximos e não nomeiam o R-4D-11
- Páginas de terceiros (Wikipedia, Astronautix e catálogos) não contam como fonte primária e não dão o 44:1

**Análogos da mesma classe e expansão (NÃO VALIDADO: não são o R-4D-11):**

| Motor | Isp (s) | Fonte |
| :- | -: | :- |
| 440 N, Re | 308 | [F239] PDF p. 7: "Performance of 308 seconds at 44:1 area ratio was achieved" |
| 440 N, Nb ("similar Nb engines", "the Nb engine") | 304 | [F239] PDF p. 7: "about 4 seconds higher than similar Nb engines" (308 − 4) e "about 10 seconds higher than the Nb engine" (314 − 10); calculado |
| 440 N, Re, injetor de programa anterior | 314 | [F239] PDF p. 7: "Performance of 314 seconds at an area ratio of 44:1 was measured. This performance is about 10 seconds higher than the Nb engine" |
| 490 N, três injetores | 309 | [F240] resumo no NTRS: "Three injectors with 44:1 area ratios are capable of nominal specific impulse values of 309 sec" (só o resumo; artigo não obtido) |

Sensibilidade, com o MAV redimensionado para o mesmo Isp nos dois estágios e o comprimento do motor 44:1 nos dois:

| Isp (s) | GLOM (kg) | Comprimento (m) | Sem mudar a P-086 (m) |
| -: | -: | -: | -: |
| 304 | 425,0 | 3,260 | 3,676 |
| 308 | 398,8 | 3,181 | 3,597 |
| 309 | 392,7 | 3,162 | 3,579 |
| 314 | 364,5 | 3,077 | 3,493 |

Massa do 44:1 sem fonte: fica a do catálogo.

## (c) De onde vêm os 5 772 m/s

| Parcela | m/s | Origem |
| :- | -: | :- |
| Subida a 100 × 100 km | 4 027,9 | [F37] Tab. 1, p. 17; 524,9 m/s acima da velocidade circular da mesma linha: inclui a subida a 100 km e as perdas, já líquidas do ganho de rotação, porque o caso sai do equador rumo leste |
| Transferência até 300 × 25 952 km | 1 192,9 | órbita do ADR 0005 (regra dos 5 %), coaxial ideal |
| Rotação perdida a 27,3° | 26,8 | inclinação de [F35] p. 3, v_eq·(1 − cos i) |
| Soma sem margem | 5 247,6 | |
| Margem de 10 % | 524,8 | P-014 |
| **Total** | **5 772,4** | results/etapa2.5/arquitetura.yaml |

**Bowles:** 4150 m/s em órbita baixa ([F46] PDF p. 10: "orbital at 4150 m/sec"). [F46] Tab. 1, PDF p. 21: "(100, 500) (3597,3227) 4115.5"; a fonte não diz de onde vem a diferença até o valor do texto (não conferido). O modelo do estudo dá 4 121,3 m/s para 100 × 500 km, sem rotação nem margem, contra 4 115,5 da tabela. Não conferido se o valor de Bowles tem margem. **A diferença de 1 622 m/s é principalmente a órbita-alvo e a margem**: as duas partem da mesma linha de 100 × 100 km.

### Trade da órbita de encontro

Cada linha roda `veiculos` do estudo com a órbita dada. O MAV é redimensionado, com a mesma carga e a mesma plataforma. Orbitador pela regra (iii). Descer vale de 1 sol até a órbita de encontro; "voltar" é o custo extra de voltar a 1 sol antes de partir para a Terra; "direto" é partir da órbita de encontro. O estudo soma o descer ao menor dos dois.

| Órbita (km) | Δv do MAV (m/s) | GLOM (kg) | Comprimento (m) | Empuxo/peso, 4 e 2 motores | Descer (m/s) | Direto, extra (m/s) | Voltar, extra (m/s) | Extra do orbitador (m/s) | Orbitador (kg) | Margem no Falcon Heavy | Lander (kg) | Margem no Vulcan VC4 |
| :- | -: | -: | -: | :- | -: | -: | -: | -: | -: | -: | -: | -: |
| 300 × 25 952 (base) | 5 772 | 386,8 | 3,561 | 1,36 e 0,68 | 58 | +62 | +57 | 115 | 7 796 | +44,0 % | 4 615 | +40,6 % |
| 300 × 10 824 (margem zero no Falcon Heavy) | 5 515 | 315,5 | 3,357 | 1,67 e 0,84 | 307 | +310 | +305 | 613 | 11 224 | +0,0 % | 4 464 | +45,3 % |
| 300 × 10 000 | 5 487 | 308,8 | 3,344 | 1,71 e 0,85 | 334 | +337 | +332 | 667 | 11 730 | −4,3 % | 4 449 | +45,8 % |
| 300 × 5 000 | 5 223 | 253,8 | 3,235 | 2,08 e 1,04 | 587 | +588 | +583 | 1 169 | 18 910 | −40,6 % | 4 332 | +49,7 % |
| 300 × 1 000 | 4 724 | 179,9 | 3,055 | 2,93 e 1,46 | 1 053 | +1 051 | +1 046 | 2 099 | 153 086 | −92,7 % | 4 174 | +55,4 % |
| 300 × 594 (limite em que o orbitador deixa de fechar) | 4 637 | 169,9 | 3,027 | 3,10 e 1,55 | 1 133 | +1 130 | +1 126 | 2 259 | diverge | — | 4 153 | +56,2 % |
| 380 × 380 | 4 606 | 166,6 | 3,017 | 3,16 e 1,58 | 1 198 | +1 190 | +1 177 | 2 375 | não fecha | — | 4 146 | +56,5 % |

**Limites, com periapse de 300 km:** o orbitador químico com um estágio de retorno deixa de fechar em 594 km de apoapse: abaixo disso, o Δv passa do que o estágio permite, e perto desse limite a massa diverge, então ele é só matemático. A margem no Falcon Heavy zera em 10 824 km. O Δv extra acima não depende do veículo fechar. O Vulcan VC6, a alternativa do orbitador no ADR 0008, parte de +6,4 % na órbita de base e zera bem antes.

**Não calculado:** aerofrenagem na descida (P-020): tiraria só o "descer", cerca de metade do extra, somando 90 m/s de saída e 205 dias, em valores de fonte para outra órbita; comunicação e relé, janela de encontro, sensores e o que muda na captura. A plataforma do orbitador não foi reiterada, e o MAV mais leve não mudou os motores.

## (d) O MAV em pé

**Sim, foi calculado:** results/etapa7.2/mav_arranjo.md tem o caso em pé, em todas as estações. Com a base no ombro, a mais favorável:

| Ø (m) | Disponível 4,5 m (m) | Folga em pé 4,5 m | Disponível 4,65 m (m) | Folga em pé 4,65 m |
| -: | -: | -: | -: | -: |
| 0,57 | 1,78 | −1,78 | 2,79 | −0,77 |
| 0,60 | 1,75 | −1,74 | 2,77 | −0,73 |
| 0,69 | 1,67 | −1,81 | 2,70 | −0,78 |

## Tabela final: o que cada alavanca faz

Folga em m, com a base no ombro, a estação mais favorável; positivo = cabe. Nas outras estações ela é menor (results/etapa7.2/mav_arranjo.md). A folga interna da P-087 já está descontada. A interferência dos bocais do estágio 1 (results/etapa7.2/bocais_alternativas.md) continua em todas as linhas com 164:1 até Ø 0,57 m e no diâmetro intermediário; o maior diâmetro da tabela só contém as saídas sem parede, e a linha de 44:1 as contém. "P-086 pelo motor" supõe nada além do motor: sem estrutura de empuxo e sem encaixe no tampo.

| Alavanca | Ø (m) | Comprimento (m) | Variação (m) | Deitado 4,5 m | Deitado 4,65 m | Em pé 4,5 m | Em pé 4,65 m | Extra do orbitador sobre a base (m/s) |
| :- | -: | -: | -: | -: | -: | -: | -: | -: |
| Base: Ø 0,57 m, P-086 de 1,5 m, órbita de base | 0,57 | 3,561 | +0,000 | −0,188 | +0,017 | −1,780 | −0,771 | — |
| P-086 pelo motor real 164:1 nos dois estágios ([F228]) | 0,57 | 3,619 | +0,058 | −0,218 | −0,012 | −1,838 | −0,830 | — |
| P-086 pela leitura da figura do MSR (NÃO VALIDADO) | 0,57 | 3,613 | +0,052 | −0,214 | −0,009 | −1,831 | −0,823 | — |
| Cada 0,1 m a menos na P-086, por qualquer meio, inclusive bocal aninhado (NÃO VALIDADO) | 0,57 | 3,461 | −0,100 | −0,138 | +0,067 | −1,680 | −0,671 | — |
| R-4D-11 44:1 nos dois estágios, P-086 pelo motor, Isp do 164:1 mantido (NÃO VALIDADO) | 0,57 | 3,144 | −0,417 | +0,020 | +0,225 | −1,363 | −0,355 | — |
| Idem, com o pior análogo (304 s; NÃO VALIDADO) | 0,57 | 3,260 | −0,301 | −0,038 | +0,168 | −1,478 | −0,470 | — |
| Tanques aninhados, antepara comum (limite otimista) | 0,57 | 3,070 | −0,491 | +0,057 | +0,262 | −1,289 | −0,281 | — |
| Ø 0,6 m | 0,60 | 3,491 | −0,070 | −0,176 | +0,037 | −1,737 | −0,725 | — |
| Ø 0,69 m | 0,69 | 3,477 | −0,084 | −0,234 | −0,002 | −1,806 | −0,781 | — |
| Órbita 300 × 10824 km (margem zero no Falcon Heavy) | 0,57 | 3,357 | −0,204 | −0,086 | +0,119 | −1,576 | −0,567 | +498 |
| Órbita 300 × 10000 km | 0,57 | 3,344 | −0,217 | −0,080 | +0,125 | −1,563 | −0,555 | +552 |
| Órbita 300 × 5000 km | 0,57 | 3,235 | −0,326 | −0,026 | +0,180 | −1,454 | −0,445 | +1 054 |
| Órbita 300 × 1000 km | 0,57 | 3,055 | −0,506 | +0,064 | +0,270 | −1,274 | −0,266 | +1 984 |
| Órbita 300 × 594 km (limite em que o orbitador deixa de fechar) | 0,57 | 3,027 | −0,534 | +0,079 | +0,284 | −1,246 | −0,237 | +2 144 (massa diverge) |
| Órbita 380 × 380 km | 0,57 | 3,017 | −0,544 | +0,083 | +0,289 | −1,236 | −0,227 | +2 260 (orbitador não fecha) |
| Órbita de margem zero + tanques aninhados (limite otimista) | 0,57 | 2,865 | −0,696 | +0,159 | +0,365 | −1,084 | −0,076 | +498 |

**Comprimento máximo com Ø 0,57 m:** deitado, 3,18 m no 4,5 m e 3,60 m no 4,65 m; em pé, 1,78 m e 2,79 m.

## Resolução da amostragem

Teste pedido pelo Fabio para aceitar os parâmetros de amostragem como tais, não como premissas: dobrar a resolução de cada um e olhar as conclusões, nas casas mostradas.

| Parâmetro | Como dobrei | Resultado | Muda nas casas mostradas? |
| :- | :- | :- | :- |
| passos_bissecao | 16 para 32 passos | margem zero em 10 824 e 10 824 km; deixa de fechar em 594 e 594 km | não |
| orbitas_amostra | ponto médio geométrico entre as órbitas: 2 236, 7 071, 10 404, 16 760 km | comprimentos novos 3,127, 3,289, 3,351, 3,457 m, em ordem entre os vizinhos; os pontos existentes são recalculados iguais | não |
| diametros_m, 4,5 m | 7 para 13 diâmetros | melhor folga deitado na grade: −0,176 m em Ø 0,600 m; na fina: −0,176 m em Ø 0,600 m | não |
| diametros_m, 4,65 m | 7 para 13 diâmetros | melhor folga deitado na grade: +0,037 m em Ø 0,600 m; na fina: +0,037 m em Ø 0,600 m | não |
| exemplo_p086_m | 0,10 para 0,05 m | folga por metro: 0,500 e 0,500 m/m | não |

**Nota sobre os diâmetros:** a tabela de alavancas mostra só os pontos da varredura, cujos valores não dependem da grade. O que a grade fina muda é onde cai o melhor diâmetro; a conclusão de que o diâmetro não faz o MAV caber no 4,5 m se mantém enquanto a folga máxima seguir negativa.

## Opinião do agente (separada dos dados; não é fato nem recomendação como fato)

Opinião: as duas maiores alavancas são tanques aninhados (−0,49 m, limite otimista) e R-4D-11 44:1 (−0,30 a −0,42 m, com Isp e massa sem fonte). A órbita de encontro dá −0,20 m até o limite do lançador. A órbita é a única que reduz o propelente, mas sozinha não basta: na margem zero do Falcon Heavy (300 × 10 824 km) a folga deitado é −0,09 m no 4,5 m e +0,12 m no 4,65 m, e margem zero não é ponto de projeto. Ela também não resolve os bocais: ali o empuxo/peso com dois motores é 0,84, abaixo de 1, o motivo por que a opção C foi descartada. O 44:1 é a única das três alavancas que também resolveria os bocais, então eu buscaria primeiro o Isp e a massa dele. Eu não gastaria mais esforço em órbita antes disso, e a P-086 pesa pelo motor, não pela busca de mais cotas do MSR. A decisão é do Fabio.
