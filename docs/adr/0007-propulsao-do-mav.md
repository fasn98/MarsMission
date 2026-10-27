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
