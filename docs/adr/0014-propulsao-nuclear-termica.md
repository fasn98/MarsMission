# ADR 0014 — Propulsão nuclear térmica: fora desta missão robótica

Status: Proposto (para decisão do Fabio)
Data: 2026-10-28

## Contexto
O prompt da Fase 3 deixa a propulsão nuclear térmica (NTP) fora do escopo: "Nuclear térmica: não modelar". Ele pede para
verificar com fonte o estado atual da NTP (há motor qualificado em voo?) e registrar num ADR por que ela fica fora. No
portão da 3.3, o Fabio pediu este ADR em PR à parte.

## Estado atual (fontes primárias)
1. **Nenhum sistema NTP voou nem foi testado completo em configuração de voo:**
   - National Academies (2021), p. 2: "no in-space NTP system has ever been operated" [F124].
   - National Academies (2021), p. 15: "no complete NTP system has been assembled and tested in its flight configuration
     or flown in space" [F124].
2. **Só testes em solo, há mais de 50 anos (Rover/NERVA, 1955–1973):**
   - Pewee 1: "the highest peak equivalent ideal vacuum specific impulse, 901 seconds" [F125, p. 88 do PDF]. Para o
     "Pewee", a National Academies dá cerca de 875 s [F124, p. 14].
   - NRX-A6: "total run time of 62 minutes" [F125, p. 118 do PDF].
   - As fontes divergem no número de partidas do XE-Prime: 24 [F125] contra 28 [F124, p. 14]. Fica registrado, sem
     escolher.
3. **A demonstração em voo planejada (DRACO, DARPA/NASA) foi encerrada:**
   - NASA, FY 2026 Budget Technical Supplement, p. ST-8: "The request also reflects the decision by our partner to cancel
     the Demonstration Rocket for Agile Cislunar Operations (DRACO) project" [F126]. O parceiro é a DARPA, que conduzia o
     programa [F127].
   - DARPA: "This program is now complete" [F127].
4. **Desempenho de referência:** o DRA 5.0 dá "Isp 875–950 s" (NASA/SP-2009-566, p. 25) e um motor de 25 klbf com
   "Isp ~900–910 s" e razão empuxo/peso de "approximately 3.43" (Addendum, p. 195) [F18]. A massa do motor não é dada; não
   foi calculada aqui.
5. **Maturidade e prazo:** levar a NTP à missão tripulada de referência de 2039 exige "an aggressive research and
   development program". Entre os desafios, a National Academies aponta "the lack of adequate ground-based test
   facilities" [F124, p. 2].
6. **Lançamento de reator:** fissão com combustível diferente de urânio de baixo enriquecimento cai no Tier III, e "The
   President's authorization shall be required for Federal Government launches in Tier III" [F128, NSPM-20, p. 3].
7. **Ressalva, a pesquisa continua:** o Congresso destinou "not less than $110,000,000 and up to $120,000,000 for NTP"
   no FY2026 [F129, p. 55].

## Decisão (proposta)
A NTP fica **fora** desta missão robótica, sem modelagem.
- **Motivo principal (fato):** nenhum sistema NTP voou nem foi testado completo em configuração de voo [F124], e a única
  demonstração em voo planejada foi encerrada [F126, F127]. Pela prática da Fase 3 (motores com voo comprovado: ADR 0007,
  catálogo da Etapa 3.1, ADR 0013), a NTP já ficaria fora.
- **Motivo adicional (fato):** mesmo a missão tripulada de 2039 depende de um programa agressivo e de instalações de
  teste em solo que hoje não existem [F124].
- **Inferência deste estudo, não conferida em fonte:** não foi achada fonte primária que avalie a NTP para uma missão
  robótica de ida e volta como esta. O ganho de Isp (cerca de 900 s contra 310 s) teria de ser pesado contra a massa do
  reator e da blindagem, que não foi levantada.

## Consequências
- A propulsão do orbitador continua química (ADR 0013, no PR da Etapa 3.4).
- Reavaliar se surgir um motor NTP com voo ou com demonstração em voo programada.
