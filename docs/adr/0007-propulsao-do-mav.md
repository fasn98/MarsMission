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
- **A contingência está incluída:**
  - p. 5: "A weight growth allowance of 30% was used for all dry mass elements";
  - cada "% Dry" da Tab. 5 é a massa do item dividida por 65,5/1,3 = 50,4 kg (calculado aqui);
  - a p. 38 (§9.0 e §9.1) diz que a coluna "Inert" da Tab. 11 é o projeto final do MAV pressurizado de 20 kg ("the
    pressure-feed 20kg inert payload mass MAV design"; 392,6 kg, contra 394,1 kg na Tab. 5), com (Tab. 11, p. 40) "Contingency 14.93
    (30%)" dentro dos 64,72 kg secos.
- **O 0,176 é o mesmo veículo, contado de outro jeito:** p. 38, "Total propellant mass fraction is 77.4%, which includes
  ascent propellant, reserves and engine start-up". Contar a reserva (5 %, p. 4) e a partida como propelente equivale a
  tirar a reserva do MAV. Por isso o 0,176 é só o limite otimista.
- **Por que o ε pressurizado não é maior:** a massa seca sobe 21 % (tanques e pressurização), mas a decolagem sobe 26 %
  (p. 27); o propelente útil cresce mais que o seco (calculado aqui com a Tab. 5). O Isp do caso pressurizado não é dado
  em número no texto nem nas tabelas; o custo da alimentação pressurizada aparece no propelente e na massa total, não
  no ε.
- **Massas** (`results/etapa2.5/arquitetura.md`): MAV com a energia do aquecimento de 438 para 403 kg; lander injetado
  de 4.066 para 3.996 kg. O orbitador não muda (7.205 kg).
- **Sensibilidade** (`results/etapa2.5/arquitetura.md`, órbita de encontro de base):

  | ε do MAV | Papel | Lander injetado | FH com recuperação | Vulcan VC2 |
  | :- | :- | -: | -: | -: |
  | 0,238 (turbobomba, Tab. 5) | pessimista | 4.066 | +15 % | +6 % |
  | **0,230 (pressurizado, Tab. 5)** | **base** | **3.996** | **+17 %** | **+8 %** |
  | 0,176 (só a massa seca, Tab. 11) | otimista | 3.701 | +26 % | +17 % |
  | 0,300 (P-045, sem fonte) | ilustração do risco | 5.368 | −13 % | −19 % |

- **Limitação:** o ε é de um MAV de **um estágio** (Bowles) e é aplicado aos **dois estágios** do nosso. Hipótese, sem
  fonte: provavelmente é otimista para o 2º estágio, que é muito menor: 85,7 kg, contra 394,1 kg do MAV de Bowles (`results/etapa2.5/arquitetura.md`). Outras:
  a massa de GN&C e de processamento de dados foi cobrada do ERV em Bowles (p. 5); o motor de Bowles não é o R-4D-11.

**RISCO de projeto (MAV perto da assíntota da equação do foguete).**
- Com Isp de 310 s e Δv de subida de 5,764 km/s (com margem), o MAV fica perto da assíntota da equação do foguete.
- Um ε só um pouco acima do de Bowles faz a massa crescer muito. Com ε = 0,300 (P-045, sem fonte, só ilustração), o
  lander vai a 5.368 kg e perde os dois lançadores escolhidos: Falcon Heavy com recuperação −13 % e Vulcan VC2 −19 %.
- Ligado à **Etapa 3.3**: uma órbita de encontro mais baixa, com orbitador elétrico, reduz o Δv do MAV.

## Nota (2026-10-28): risco do MAV depois da Etapa 3.3 (ADR 0013)
- **A mitigação prevista não se confirmou.** Ela era uma órbita de encontro mais baixa, com orbitador elétrico, para
  reduzir o Δv do MAV (nota anterior; Etapa 3.3). Na missão de referência, nenhuma opção elétrica fechou massa e tempo
  (ADR 0013), e o encontro continua em 300 × 24.992 km.
- **O risco continua aberto:** Isp de 310 s e Δv de subida de 5,764 km/s com margem (`results/etapa2.5/arquitetura.md`),
  perto da assíntota da equação do foguete.
- **Mitigações a avaliar nas próximas fases:**
  1. **Margem de lançador:** manter margem para o crescimento do lander. Hoje: Falcon Heavy com recuperação +17 % e
     Vulcan VC2 +8 % (`results/etapa2.5/arquitetura.md`).
  2. **Lançador maior para o lander:** por exemplo, os que já servem com folga na tabela do ADR 0008 (Falcon Heavy
     descartável, Vulcan VC4 e VC6).
  3. **MAV com Isp maior, se houver motor com voo comprovado:** o R-4D-11 tem 310 s [F107]. Um motor com voo e Isp
     maior reduziria a sensibilidade ao ε.
