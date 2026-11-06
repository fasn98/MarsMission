# Portão da 7.2: rotas para o alvo de aeroshell de 4,5 m (gerado por tools/rotas_mav.py)

Dados para o portão. Nenhuma premissa nem ADR muda, e a decisão é do Fabio. O que usa análogo ou leitura está marcado NÃO VALIDADO.

**Alvo:** aeroshell de 4,5 m, MAV deitado, Ø que contenha as saídas dos bocais com parede. Coifa do Vulcan com 4,5 m: +0,141 e +0,064 m, nas duas leituras da figura. Comprimento máximo deitado por Ø, com a base no ombro: Ø 0,57 m, 3,18 m; Ø 0,60 m, 3,14 m; Ø 0,63 m, 3,10 m; Ø 0,66 m, 3,05 m; Ø 0,69 m, 3,01 m; Ø 0,72 m, 2,96 m; Ø 0,75 m, 2,92 m. Com o deck (P-094) sob o MAV, o limite em Ø 0,57 m cai 0,44 m; por isso as duas folgas aparecem.

## Rota A: MAV melhorado, arquitetura atual

R-4D-11 44:1 nos dois estágios; a P-086 segue o motor do [F228]; o MAV é redimensionado para cada Isp. **Tanques aninhados:** [F46] §5.4, PDF p. 17: "Similar to a common bulkhead design, the forward tank aft dome is accommodated within a recessed aft tank forward dome but with a purge gap between the two tanks. The inter-tank section is eliminated". Ressalva: a conta não desconta o vão de purga nem muda a massa dos tanques. Massa e empuxo do 44:1 são os do catálogo (NÃO VALIDADO). Isp NÃO VALIDADO: análogos.

| Caso | GLOM (kg) | Comprimento (m) | Folga deitado, ombro (m) | Folga deitado, ombro + deck (m) | Círculo das saídas (m) | Folga radial dos bocais, com parede (m) | Empuxo/peso em Marte | Massa por área (kg/m²) | Margem no Vulcan VC4 |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| Base: 4 × 164:1, Ø atual | 386,8 | 3,561 | −0,188 | −0,408 | 0,675 | −0,062 | 1,36 | 279 | +40,6 % |
| 44:1, Isp 304 s | 425,0 | 3,260 | −0,038 | −0,258 | 0,369 | +0,091 | 1,24 | 283 | +38,2 % |
| 44:1, Isp 308 s | 398,8 | 3,181 | +0,002 | −0,218 | 0,369 | +0,091 | 1,32 | 280 | +39,8 % |
| 44:1, Isp 309 s | 392,7 | 3,162 | +0,011 | −0,209 | 0,369 | +0,091 | 1,34 | 279 | +40,2 % |
| 44:1, Isp 314 s | 364,5 | 3,077 | +0,054 | −0,166 | 0,369 | +0,091 | 1,45 | 276 | +42,0 % |
| 44:1 e aninhados, Isp 304 s | 425,0 | 2,763 | +0,210 | −0,010 | 0,369 | +0,091 | 1,24 | 283 | +38,2 % |
| 44:1 e aninhados, Isp 308 s | 398,8 | 2,688 | +0,248 | +0,028 | 0,369 | +0,091 | 1,32 | 280 | +39,8 % |
| 44:1 e aninhados, Isp 309 s | 392,7 | 2,671 | +0,257 | +0,037 | 0,369 | +0,091 | 1,34 | 279 | +40,2 % |
| 44:1 e aninhados, Isp 314 s | 364,5 | 2,590 | +0,297 | +0,077 | 0,369 | +0,091 | 1,45 | 276 | +42,0 % |

O Δv de subida vem de [F46], calculado com empuxo/peso de 2,5 na decolagem ([F46] PDF p. 9: "a liftoff thrust-to-weight ratio of 2.5 was used"). Todos os casos aqui têm empuxo/peso menor, e a perda gravitacional maior disso não está modelada, nem na base.

## Rota B: orbitador elétrico e encontro em órbita baixa

### MAV

2 × R-4D-11 164:1, Ø 0,60 m, o menor da varredura que contém as saídas com parede. Comprimento com a P-086 atual.

| Caso | GLOM (kg) | Comprimento (m) | Folga deitado, ombro (m) | Folga deitado, ombro + deck (m) | Círculo das saídas (m) | Folga radial dos bocais, com parede (m) | Empuxo/peso em Marte | Massa por área (kg/m²) | Margem no Vulcan VC4 |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| 2 × 164:1, Ø 0,60 m, 380 × 380 km | 166,6 | 3,017 | +0,061 | −0,159 | 0,559 | +0,011 | 1,58 | 250 | +56,5 % |
| 2 × 164:1, Ø 0,60 m, 1 252 × 1 252 km | 212,2 | 3,140 | +0,000 | −0,220 | 0,559 | +0,011 | 1,24 | 256 | +52,9 % |

| Órbita | Altitude (km) | Δv do MAV, com margem (m/s) | Por que esta órbita |
| :- | -: | -: | :- |
| Órbita do MSR | 380 | 4 606 | [F35] p. 3: "nominal injection orbit of 380km" |
| Maior que cumpre o alvo | 1 252 | 4 969 | a maior altitude circular em que o MAV com 2 motores R-4D-11 164:1, em Ø 0,60 m, ainda cabe deitado no aeroshell de 4,5 m: o menor Δv do orbitador que cumpre o alvo |

### Orbitador híbrido (c2 do ADR 0013): captura e saída químicas, espiral elétrica verificada

O mais leve que cabe na menor estada das quatro janelas, varrendo a altitude de captura e o número de propulsores. Massa e margem pela regra (iii).

| Órbita (km) | Propulsor | Ativos | Potência (kW) | Captura (km) | Orbitador (kg) | Xenônio (kg) | Descida (d) | Subida (d) | Folga na estada (d) | Margem no Falcon Heavy | Em órbita de encontro | Chega antes do último lançamento? | Subida cruza a conjunção? |
| -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | :- | :- |
| 380 | NSTAR | 3 | 7,7 | 1 000 | 63 466 | 207 | 201 | 189 | 2 | −82,3 % | 2030-04-09 | **não** (-34 d) | sim |
| 380 | XIPS-25 | 2 | 9,0 | 1 099 | 65 793 | 219 | 200 | 188 | 4 | −82,9 % | 2030-04-09 | **não** (-34 d) | sim |
| 1 252 | NSTAR | 1 | 2,6 | 1 605 | 47 298 | 70 | 184 | 174 | 33 | −76,3 % | 2030-03-24 | **não** (-18 d) | sim |
| 1 252 | XIPS-25 | 1 | 4,5 | 1 764 | 51 753 | 97 | 161 | 152 | 80 | −78,3 % | 2030-02-28 | sim (6 d) | sim |

### Orbitador só elétrico (opção b do ADR 0013): calculado, NÃO verificado

Massas fechadas aqui, sem estágio químico de captura. Trecho heliocêntrico quase circular, com a margem de Δv, e motor de potência constante: não é trajetória otimizada nem traz janela nova. A margem usa os C3 das janelas atuais. Primeiro número de propulsores que fecha estada, lançador e vida, e o maior da varredura.

| Órbita (km) | Propulsor | Caso | Ativos | Potência (kW) | Orbitador (kg) | Xenônio por propulsor (kg) | Vida (kg) | Empuxo na ida (d) | Empuxo na volta (d) | Descida (d) | Subida (d) | Folga na estada (d) | Margem no Falcon Heavy | Em órbita de encontro, partindo em 2028-11-24 | Chega antes do último lançamento? |
| -: | :- | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | :- |
| 380 | NSTAR | nenhum fecha; o maior | 12 | 30,7 | 8 198 | 311 | 135 | 479 | 297 | 260 | 222 | −90 | +36,9 % | 2030-12-04 | **não** |
| 380 | XIPS-25 | primeiro que fecha | 10 | 45,0 | 9 420 | 394 | não achada | 376 | 245 | 208 | 180 | 4 | +19,2 % | 2030-07-02 | **não** |
| 380 | XIPS-25 | o maior | 12 | 54,0 | 10 754 | 375 | não achada | 358 | 233 | 198 | 171 | 23 | +4,4 % | 2030-06-03 | **não** |
| 1 252 | NSTAR | nenhum fecha; o maior | 12 | 30,7 | 7 912 | 292 | 135 | 462 | 294 | 219 | 189 | −16 | +41,9 % | 2030-10-07 | **não** |
| 1 252 | XIPS-25 | primeiro que fecha | 7 | 31,5 | 7 187 | 417 | não achada | 410 | 272 | 198 | 172 | 22 | +56,2 % | 2030-07-26 | **não** |
| 1 252 | XIPS-25 | o maior | 12 | 54,0 | 10 434 | 353 | não achada | 347 | 230 | 168 | 146 | 78 | +7,6 % | 2030-04-24 | **não** |

### Linha do tempo da missão de referência

Chegada 2029-09-20; partida 2030-11-08; viagens de 300 e 319 d; encontro de 22 d. Conjunção de 2030-05-06 a 2030-06-13. Lançamento do MAV, dentro da folga mínima de 60 d do ADR 0018: de 2029-11-03 a 2030-03-06. O orbitador precisa estar em órbita antes desse lançamento. Hoje, com o químico, ele já chega pronto.

### Por que o ADR 0013 rejeitou o elétrico, e se ainda vale

**Conclusão do ADR:** "Na missão de referência (414 dias em Marte) e com as leis de guiagem verificadas, nenhuma opção elétrica fecha massa e tempo. Uma missão de estada longa, como a do ERO, poderia mudar isso, mas exigiria outra missão de referência e uma guiagem otimizada, não estudadas."

- **Híbrido c2:** continua valendo. A captura química em órbita baixa custa caro, e o orbitador fica muitas vezes acima do lançador.
- **Só elétrico:** o ADR só o estimou em ordem de grandeza. Com as massas fechadas, a massa pode caber, mas pede dezenas de kW, xenônio além da vida conhecida no NSTAR e sem vida publicada no XIPS-25, e não chega a tempo do lançamento do MAV na missão de referência. A outra parte da conclusão do ADR continua: exigiria outra missão de referência e outra guiagem.

## Tabela final: A × B × base

| Grandeza | Base | A: 44:1 e aninhados, 304 a 314 s | B: híbrido c2, 380 a 1 252 km | B: só elétrico, NÃO verificado |
| :- | :- | :- | :- | :- |
| Δv do MAV (m/s) | 5 772 | 5 772 | 4 606 a 4 969 | a mesma do híbrido |
| GLOM (kg) | 386,8 | 364,5 a 425,0 | 166,6 a 212,2 | a mesma do híbrido |
| Comprimento (m) | 3,561 | 2,590 a 2,763 | 3,017 a 3,140 | a mesma do híbrido |
| Folga deitado, ombro (m) | −0,188 | +0,210 a +0,297 | +0,000 a +0,061 | a mesma do híbrido |
| Folga deitado, ombro + deck (m) | −0,408 | −0,010 a +0,077 | −0,220 a −0,159 | a mesma do híbrido |
| Folga radial dos bocais, com parede (m) | −0,062 | +0,091 | +0,011 | a mesma do híbrido |
| Empuxo/peso em Marte | 1,36 | 1,24 a 1,45 | 1,24 a 1,58 | a mesma do híbrido |
| Massa por área, 4,5 m (kg/m²; Mars 2020: 211) | 279 | 276 a 283 | 250 a 256 | a mesma do híbrido |
| Orbitador (kg) | 7 796 | 7 796 | 47 298 a 65 793 | 7 187 a 9 420 |
| Potência elétrica (kW) | — | — | 2,6 a 9,0 | 31,5 a 45,0 |
| Margem no Falcon Heavy | +44,0 % | +44,0 % | −82,9 a −76,3 % | +19,2 a +56,2 % |
| Espiral de descida e de subida (d) | — | — | 161 a 201 e 152 a 189 | 198 a 208 e 172 a 180 |
| Efeito na linha do tempo | nenhum | nenhum | pede o lançamento do MAV perto do limite do ADR 0018, ou depois | outra missão de referência |
| Muda o quê | — | motor sem Isp e massa de fonte, e arranjo dos tanques | reabre o ADR 0013 | reabre os ADRs 0003 e 0013 |

## Opinião do agente (separada dos dados; não é fato nem recomendação como fato)

Opinião: a rota A é a única que cumpre o alvo sem mudar a arquitetura: mesmo no pior Isp ela cabe no ombro com +0,21 m, e a massa por área fica na mesma faixa da base. O que a sustenta é ainda não verificado: Isp e massa do 44:1 e a soma das duas mudanças no arranjo. A rota B reduz bem o MAV e a massa por área, mas o híbrido fica 76 a 83 % acima do Falcon Heavy, então os motivos do ADR 0013 continuam, e o só elétrico pede outra missão. Se eu fosse testar um próximo passo, seria fechar os dados do 44:1 e dimensionar o tanque aninhado na pressão real. A decisão é do Fabio.
