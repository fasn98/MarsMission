# ADR 0007 — Propulsão do MAV: hipergólica armazenável

Status: Accepted (Fabio, 2026-10-27, portão da propulsão do MAV na Etapa 2.2)
Data: 2026-10-27

## Contexto
Foram comparados o MAV sólido (O1, como o MSR), o LOX/CH4 com propelente da Terra (O2) e o hipergólico
armazenável (O4), todos sem ISRU (ADR 0006), pela massa total na órbita baixa da Terra pela regra (iii) e
por critérios operacionais (`docs/etapa2.2b_propulsao_mav.md`).

## Decisão
**Linha de base: O4, MAV hipergólico armazenável (MMH/NTO, Isp de 343 s [F46]).**

- **Por massa:** 34,2 a 34,4 t pela regra (iii), contra 41,3 a 41,4 t do sólido (−17 % com o aquecimento
  incluído; −21 % sem ele, como avaliado no portão) e 35,1 t do LOX/CH4. O aquecimento da superfície está
  incluído (P-027): 36 W para manter o NTO acima de −1 °C.
- **Por critério operacional:** dispensa armazenamento criogênico. O DRA 5.0 Addendum #2, p. 330 [F51],
  diz que "zero boil-off may be achieved using technology approaches under development but not yet
  demonstrated in space". O DRA 5.0 Addendum, p. 342 [F18], registra que "the longest flight of stored
  cyrogens is Titan Centaur-5, where the propellants were stored in orbit for 9 hours" (afirmação de 2009).
- **O2 (LOX/CH4)** empata em massa dentro da incerteza (+0,8 a 0,9 t) e perde nos critérios operacionais.
- **O1 (sólido)** fica documentado como alternativa de maior maturidade. Razões do MSR [F57, F58]:
  - "the most technologically ready";
  - "Simple design does not require moving parts";
  - "High TRL and reliability".
  Contras registrados pelo próprio MSR: não pode ser estrangulado nem desligado, Isp menor e
  "Potential issues with extremely cold environments".
- **Precedente:** o estágio de subida do módulo lunar da Apollo usou "hypergolic bipropellants and a
  pressure-fed ablatively cooled engine" de 3500 lbf, com "a single-engine concept" (NASA TN D-7082
  [F62]). O mesmo relatório registra uma falha do regulador primário de hélio no LM-3; não se afirma
  aqui ausência de falhas.

## Consequências
- Com O4, a varredura da órbita de encontro muda o apoapse escolhido pela regra dos 5 % de 18.483 para
  26.950 km (ADR 0005, atualizado).
- O aquecimento e a operação a baixa temperatura do hipergólico (NTO a −11 °C) são requisitos de projeto
  do lander para a Fase 4.

## Nota (2026-10-27): Isp de voo (ADR 0011)
- **Motores:** o MAV O4 passa a usar motores com voo comprovado, 4 × R-4D-11 no estágio 1 e 1 × R-4D-11 no estágio 2.
  O Isp é de **310 s** [F107, Tab. 3], no lugar dos 343 s do motor com turbobomba [F46].
- **Massas:** o MAV com a energia do aquecimento passa de 282 kg para 438 kg (`results/etapa2.5/arquitetura.md`).
- **A decisão O4 não foi reavaliada contra O1 e O2 com o Isp novo.** A comparação da Etapa 2.2 fica como registro da
  época.
- **Limitação:** a fração estrutural (0,238) continua a do MAV com turbobomba [F46]. Ver o ADR 0011.

## Nota (2026-10-28): fração estrutural do MAV pressurizado (decisão do Fabio)
- **Valor-base:** ε = **0,230**, do MAV hipergólico pressurizado de Bowles et al. [F46] (Tab. 5, p. 30, coluna "Pressure
  Feed"), com o mesmo método do 0,238. É coerente com os motores pressurizados escolhidos (R-4D-11, ADR 0011).
  Antes: 0,238, do MAV com turbobomba (mesma tabela).
- **A contingência está incluída:** p. 5, "A weight growth allowance of 30% was used for all dry mass elements". Os
  "% Dry" da Tab. 5 somam sobre 65,5/1,3 = 50,4 kg.
- **Por que o ε pressurizado não é maior:** a massa seca sobe 21 % (tanques e pressurização), mas a decolagem sobe 26 %
  (p. 27), e o propelente cresce mais que o seco. O Isp do caso pressurizado não é dado na fonte; pela Tab. 5 e o Δv de
  4.150 m/s, a conta feita aqui dá cerca de 322 s, contra 339 s do caso com turbobomba (publicado: 343 s). O custo
  aparece no Isp e na massa total, não no ε.
- **Massas** (`results/etapa2.5/arquitetura.md`): MAV com a energia do aquecimento de 438 para 403 kg; lander injetado
  de 4.066 para 3.996 kg. O orbitador não muda (7.205 kg).
- **Sensibilidade** (`results/etapa2.5/arquitetura.md`, órbita de encontro de base):

  | ε do MAV | Papel | Lander injetado | FH com recuperação | Vulcan VC2 |
  | :- | :- | -: | -: | -: |
  | 0,238 (turbobomba, Tab. 5) | pessimista | 4.066 | +15 % | +6 % |
  | **0,230 (pressurizado, Tab. 5)** | **base** | **3.996** | **+17 %** | **+8 %** |
  | 0,176 (só a massa seca, Tab. 11) | otimista | 3.701 | +26 % | +17 % |
  | 0,300 (P-045, sem fonte) | ilustração do risco | 5.368 | −13 % | −19 % |

- **Limitação:** o ε é de um MAV de **um estágio** (Bowles) e é aplicado aos **dois estágios** do nosso. Provavelmente é
  otimista para o 2º estágio: 85,7 kg, contra 394,1 kg do MAV de Bowles (`results/etapa2.5/arquitetura.md`). Outras:
  a massa de GN&C e de processamento de dados foi cobrada do ERV em Bowles (p. 5); o motor de Bowles não é o R-4D-11.

**RISCO de projeto (MAV perto da assíntota da equação do foguete).**
- Com Isp de 310 s e Δv de subida de 5,764 km/s (com margem), o MAV fica perto da assíntota da equação do foguete.
- Um ε só um pouco acima do de Bowles faz a massa crescer muito. Com ε = 0,300 (P-045, sem fonte, só ilustração), o
  lander vai a 5.368 kg e perde os dois lançadores escolhidos: Falcon Heavy com recuperação −13 % e Vulcan VC2 −19 %.
- Ligado à **Etapa 3.3**: uma órbita de encontro mais baixa, com orbitador elétrico, reduz o Δv do MAV.
