# Portão da 7.2: rotas para o alvo de aeroshell de 4,5 m (gerado por tools/rotas_mav.py)

Dados para o portão. Nenhuma premissa nem ADR muda, e a decisão é do Fabio. O que usa análogo ou leitura está marcado NÃO VALIDADO.

**Alvo:** aeroshell de 4,5 m, MAV deitado, Ø que contenha as saídas dos bocais com parede. Coifa do Vulcan com 4,5 m: +0,139 e +0,064 m, nas duas leituras da figura. Comprimento máximo deitado por Ø, com a base no ombro: Ø 0,57 m, 3,18 m; Ø 0,60 m, 3,14 m; Ø 0,63 m, 3,10 m; Ø 0,66 m, 3,05 m; Ø 0,69 m, 3,01 m; Ø 0,72 m, 2,96 m; Ø 0,75 m, 2,92 m. Com o deck (P-094) sob o MAV, o limite em Ø 0,57 m cai 0,44 m; por isso as duas folgas aparecem. A folga é por extremidade: (disponível − comprimento) / 2. "Motor real" é a P-086 só com o motor de [F228] nos dois estágios, sem estrutura de empuxo: um limite inferior do comprimento.

## Rota A: MAV melhorado, arquitetura atual

R-4D-11 44:1 nos dois estágios; a P-086 segue o motor do [F228]; o MAV é redimensionado para cada Isp. **Tanques aninhados:** [F46] §5.4, PDF p. 17: "Similar to a common bulkhead design, the forward tank aft dome is accommodated within a recessed aft tank forward dome but with a purge gap between the two tanks. The inter-tank section is eliminated". Ressalva: a conta não desconta o vão de purga nem muda a massa dos tanques. Massa e empuxo do 44:1 são os do catálogo (NÃO VALIDADO). Isp NÃO VALIDADO: análogos.

| Caso | GLOM (kg) | Comprimento (m) | Folga deitado, ombro (m) | Folga deitado, ombro + deck (m) | Círculo das saídas (m) | Folga radial dos bocais, com parede (m) | Empuxo/peso em Marte | Massa por área (kg/m²) | Margem no Vulcan VC4 |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| Base: 4 × 164:1, Ø atual | 386,8 | 3,561 | −0,188 | −0,408 | 0,675 | −0,062 | 1,36 | 279 | +39,6 % |
| Base com a P-086 só pelo motor 164:1 [F228], sem estrutura de empuxo (a P-086 não muda) | 386,8 | 3,619 | −0,218 | −0,438 | 0,675 | −0,062 | 1,36 | 279 | +39,6 % |
| 44:1, Isp 304 s | 425,0 | 3,260 | −0,038 | −0,258 | 0,369 | +0,091 | 1,24 | 283 | +37,2 % |
| 44:1, Isp 308 s | 398,8 | 3,181 | +0,002 | −0,218 | 0,369 | +0,091 | 1,32 | 280 | +38,9 % |
| 44:1, Isp 309 s | 392,7 | 3,162 | +0,011 | −0,209 | 0,369 | +0,091 | 1,34 | 279 | +39,3 % |
| 44:1, Isp 314 s | 364,5 | 3,077 | +0,054 | −0,166 | 0,369 | +0,091 | 1,45 | 276 | +41,1 % |
| 44:1 e aninhados, Isp 304 s | 425,0 | 2,763 | +0,210 | −0,010 | 0,369 | +0,091 | 1,24 | 283 | +37,2 % |
| 44:1 e aninhados, Isp 308 s | 398,8 | 2,688 | +0,248 | +0,028 | 0,369 | +0,091 | 1,32 | 280 | +38,9 % |
| 44:1 e aninhados, Isp 309 s | 392,7 | 2,671 | +0,257 | +0,037 | 0,369 | +0,091 | 1,34 | 279 | +39,3 % |
| 44:1 e aninhados, Isp 314 s | 364,5 | 2,590 | +0,297 | +0,077 | 0,369 | +0,091 | 1,45 | 276 | +41,1 % |
| Referência, Isp 297 s: só 44:1 | 478,5 | 3,420 | −0,118 | −0,338 | 0,369 | +0,091 | 1,10 | 290 | +34,0 % |
| Referência, Isp 297 s: 44:1 e aninhados | 478,5 | 2,916 | +0,134 | −0,086 | 0,369 | +0,091 | 1,10 | 290 | +34,0 % |

**Ressalva sobre a faixa:** Os análogos de 306 a 314 s têm câmara de irídio e rênio, ou, em [F240], só o resumo cita essa tecnologia. Os motores convencionais de 110 lbf são outros: [F241] PDF p. 18: "Conventional 110 lbf engines use up to ~40% fuel film cooling"; "may produce a performance loss of up to 25 sec"; "10 sec higher than conventional 110 lbf silicide coated Cb chambers now in use", a 286:1. Aplicar isso ao R-4D-11 e ao 44:1 é inferência (NÃO VALIDADO): nenhuma fonte lida diz a construção da câmara do R-4D-11. O caso de referência usa o R-4D do Apollo ([F242] PDF p. 15: "This prototype engine demonstrated good performance Isp's of 295 and 297"; "maximum performance" de pouco mais de 310 s, em outra razão de mistura; câmara inicial "with an expansion ratio equal to 40"), fora da faixa pedida, para mostrar o efeito de um Isp menor. Isp 314 s fica acima do 164:1 do mesmo motor, por isso o GLOM dele sai menor que o da base.

O Δv de subida vem de [F46], calculado com empuxo/peso de 2,5 na decolagem ([F46] PDF p. 9: "a liftoff thrust-to-weight ratio of 2.5 was used"). Todos os casos aqui têm empuxo/peso menor, e a perda gravitacional maior disso não está modelada, nem na base.

## Rota B: orbitador elétrico e encontro em órbita baixa

### MAV

2 × R-4D-11 164:1, Ø 0,60 m, o menor da varredura que contém as saídas com parede. Comprimento com o motor real nos dois estágios, a mesma base da rota A. **Esta é a configuração da opção C, descartada pelo Fabio** por empuxo/peso de 0,68 no GLOM atual. Ela só passa de 1 aqui porque o GLOM cai, o que depende de reabrir o ADR 0013. Além disso, a altitude da segunda órbita depende da grade de diâmetros; com um Ø menor que 0,60 m que ainda contenha as saídas, ela seria mais alta.

| Caso | GLOM (kg) | Comprimento (m) | Folga deitado, ombro (m) | Folga deitado, ombro + deck (m) | Círculo das saídas (m) | Folga radial dos bocais, com parede (m) | Empuxo/peso em Marte | Massa por área (kg/m²) | Margem no Vulcan VC4 |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| 2 × 164:1, Ø 0,60 m, 380 × 380 km | 166,6 | 3,075 | +0,032 | −0,188 | 0,559 | +0,011 | 1,58 | 250 | +55,5 % |
| Idem, com a P-086 atual | 166,6 | 3,017 | +0,061 | −0,159 | 0,559 | +0,011 | 1,58 | 250 | +55,5 % |
| 2 × 164:1, Ø 0,60 m, 814 × 814 km | 189,4 | 3,140 | +0,000 | −0,220 | 0,559 | +0,011 | 1,39 | 253 | +53,6 % |
| Idem, com a P-086 atual | 189,4 | 3,081 | +0,029 | −0,191 | 0,559 | +0,011 | 1,39 | 253 | +53,6 % |

| Órbita | Altitude (km) | Δv do MAV, com margem (m/s) | Por que esta órbita |
| :- | -: | -: | :- |
| Órbita do MSR | 380 | 4 606 | [F35] p. 3: "nominal injection orbit of 380km" |
| Maior que cumpre o alvo | 814 | 4 801 | a maior altitude circular em que o MAV com 2 motores R-4D-11 164:1, com o motor real, ainda cabe deitado no aeroshell de 4,5 m: o menor Δv do orbitador que cumpre o alvo |

### Orbitador híbrido (c2 do ADR 0013): captura e saída químicas, espiral elétrica verificada

O mais leve que cabe na menor estada das quatro janelas, varrendo a altitude de captura e o número de propulsores. Massa e margem pela regra (iii). A folga não inclui a fase de RAAN de 24 d (ADR 0013, item 6). Conferência com a Etapa 3.3, na altitude dela: 47 447 e 47 447 kg.

| Órbita (km) | Propulsor | Ativos | Potência (kW) | Captura (km) | Orbitador (kg) | Xenônio (kg) | Descida (d) | Subida (d) | Folga na estada (d) | Margem no Falcon Heavy | Em órbita de encontro | Chega antes do último lançamento? | Subida cruza a conjunção? |
| -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | :- | :- |
| 380 | NSTAR | 3 | 7,7 | 1 000 | 63 466 | 207 | 201 | 189 | 2 | −82,4 % | 2030-04-09 | **não** (-34 d) | sim |
| 380 | XIPS-25 | 2 | 9,0 | 1 099 | 65 793 | 219 | 200 | 188 | 4 | −83,0 % | 2030-04-09 | **não** (-34 d) | sim |
| 814 | NSTAR | 1 | 2,6 | 1 099 | 48 853 | 67 | 186 | 176 | 30 | −77,1 % | 2030-03-26 | **não** (-20 d) | sim |
| 814 | XIPS-25 | 1 | 4,5 | 1 328 | 53 207 | 114 | 197 | 186 | 9 | −79,0 % | 2030-04-06 | **não** (-31 d) | sim |

### Orbitador só elétrico (opção b do ADR 0013): calculado, NÃO verificado

Massas fechadas aqui, sem estágio químico de captura. Trecho heliocêntrico quase circular, com a margem de Δv: não é trajetória otimizada nem traz janela nova. **A conta é de ordem de grandeza e o sentido do erro é desconhecido:** a margem cobra os C3 das janelas atuais, mas o Δv não dá crédito a esse v∞ (o que piora o tempo), e não há fasagem, ciclo de trabalho nem correções (o que melhora). As datas valem para crédito zero de C3 e partida em 2028-11-24, e não decidem o trade. A folga conta a estada de outra chegada, então pode não bater com as datas, e não inclui a fase de RAAN. Primeiro número de propulsores que fecha estada e lançador, e o maior da varredura. Vida do XIPS-25 não achada: conta como não limitante.

| Órbita (km) | Propulsor | Caso | Ativos | Potência (kW) | Orbitador (kg) | Xenônio por propulsor (kg) | Vida (kg) | Empuxo na ida (d) | Empuxo na volta (d) | Descida (d) | Subida (d) | Folga na estada (d) | Margem no Falcon Heavy | Em órbita de encontro, partindo em 2028-11-24 | Chega antes do último lançamento? |
| -: | :- | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | :- |
| 380 | NSTAR | nenhum fecha; o maior | 12 | 30,7 | 8 198 | 311 | 135 | 479 | 297 | 260 | 222 | −90 | +36,4 % | 2030-12-04 | **não** |
| 380 | XIPS-25 | primeiro que fecha | 10 | 45,0 | 9 420 | 394 | não achada | 376 | 245 | 208 | 180 | 4 | +18,7 % | 2030-07-02 | **não** |
| 380 | XIPS-25 | o maior | 12 | 54,0 | 10 754 | 375 | não achada | 358 | 233 | 198 | 171 | 23 | +4,0 % | 2030-06-03 | **não** |
| 814 | NSTAR | nenhum fecha; o maior | 12 | 30,7 | 8 039 | 301 | 135 | 470 | 295 | 237 | 204 | −49 | +39,1 % | 2030-11-02 | **não** |
| 814 | XIPS-25 | primeiro que fecha | 8 | 36,0 | 7 947 | 409 | não achada | 397 | 261 | 204 | 177 | 11 | +40,7 % | 2030-07-18 | **não** |
| 814 | XIPS-25 | o maior | 12 | 54,0 | 10 577 | 363 | não achada | 352 | 231 | 181 | 157 | 54 | +5,7 % | 2030-05-12 | **não** |

### Linha do tempo da missão de referência

Chegada 2029-09-20; partida 2030-11-08; viagens de 300 e 319 d; encontro de 22 d. Conjunção de 2030-05-06 a 2030-06-13. Lançamento do MAV, dentro da folga mínima de 60 d do ADR 0018: de 2029-11-03 a 2030-03-06. O orbitador precisa estar em órbita antes desse lançamento. Hoje, com o químico, ele já chega pronto. Cruzar a conjunção significa operar a espiral sem o enlace normal com a Terra no período.

### Por que o ADR 0013 rejeitou o elétrico, e se ainda vale

**Conclusão do ADR:** "Na missão de referência (414 dias em Marte) e com as leis de guiagem verificadas, nenhuma opção elétrica fecha massa e tempo. Uma missão de estada longa, como a do ERO, poderia mudar isso, mas exigiria outra missão de referência e uma guiagem otimizada, não estudadas."

- **Híbrido c2:** continua valendo. A captura química em órbita baixa custa caro, e o orbitador fica muitas vezes acima do lançador.
- **Só elétrico:** o ADR só o estimou em ordem de grandeza. Com as massas fechadas, a massa pode caber, mas pede dezenas de kW, xenônio além da vida conhecida no NSTAR e sem vida publicada no XIPS-25. Nesta conta não chega a tempo do lançamento do MAV, com crédito zero de C3 e a partida atual; isso é ordem de grandeza e não decide. O que continua de pé é a outra parte do ADR: exigiria outra missão de referência e outra guiagem, não estudadas.

## Tabela final: A × B × base

| Grandeza | Base | A: 44:1 e aninhados, 304 a 314 s | B: híbrido c2, 380 a 814 km | B: só elétrico, só XIPS-25, sem vida conhecida, NÃO verificado |
| :- | :- | :- | :- | :- |
| Δv do MAV (m/s) | 5 772 | 5 772 | 4 606 a 4 801 | a mesma do híbrido |
| GLOM (kg) | 386,8 | 364,5 a 425,0 | 166,6 a 189,4 | a mesma do híbrido |
| Comprimento, com o motor real (m) | 3,619 | 2,590 a 2,763 | 3,075 a 3,140 | a mesma do híbrido |
| Folga deitado, ombro, com o motor real (m) | −0,218 | +0,210 a +0,297 | +0,000 a +0,032 | a mesma do híbrido |
| Folga deitado, ombro + deck, com o motor real (m) | −0,438 | −0,010 a +0,077 | −0,220 a −0,188 | a mesma do híbrido |
| Folga radial dos bocais, com parede (m) | −0,062 | +0,091 | +0,011 | a mesma do híbrido |
| Empuxo/peso em Marte | 1,36 | 1,24 a 1,45 | 1,39 a 1,58 | a mesma do híbrido |
| Massa por área, 4,5 m (kg/m²; Mars 2020: 211) | 279 | 276 a 283 | 250 a 253 | a mesma do híbrido |
| Orbitador (kg) | 7 796 | 7 796 | 48 853 a 65 793 | 7 947 a 9 420 |
| Potência elétrica (kW) | — | — | 2,6 a 9,0 | 36,0 a 45,0 |
| Margem no Falcon Heavy | +43,4 % | +43,4 % | −83,0 a −77,1 % | +18,7 a +40,7 % |
| Espiral de descida e de subida (d) | — | — | 186 a 201 e 176 a 189 | 204 a 208 e 177 a 180 |
| Efeito na linha do tempo | nenhum | nenhum | em órbita em 2030-03-26 a 2030-04-09, depois do último lançamento do MAV (2030-03-06); a subida cruza a conjunção | outra missão de referência |
| Muda o quê | — | motor sem Isp e massa de fonte, e arranjo dos tanques | reabre os ADRs 0005 e 0013 e usa a opção C | reabre os ADRs 0003, 0005 e 0013 e usa a opção C |

## Opinião do agente (separada dos dados; não é fato nem recomendação como fato)

Opinião: a rota A é a única que cumpre o alvo sem mudar a arquitetura: no ombro, cabe com +0,21 m no pior Isp da faixa e com +0,13 m no caso de referência, mas com o deck sob o MAV ela fica entre −0,09 e +0,08 m. Só o 44:1, sem aninhar, cabe no ombro de 308 s para cima, com pouca folga, e não cabe com o deck. O que sustenta a rota não está verificado: Isp e massa do 44:1 e o tanque aninhado na pressão real. A rota B reduz bem o MAV e a massa por área, mas o híbrido pede de 4,4 a 5,9 vezes a capacidade do Falcon Heavy, e, com o deck, o MAV dela não cabe em nenhuma das duas órbitas. Os motivos de massa do ADR 0013 continuam. O só elétrico merece no máximo uma conta melhor, se a missão de referência mudar. Meu próximo passo seria fechar os dados do 44:1 e dimensionar o tanque aninhado. A decisão é do Fabio.
