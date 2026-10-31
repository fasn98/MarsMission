# ADR 0016 — Alternativa A para o lander: 2 × MMRTG, condicionada à disponibilidade de Pu-238

Status: Accepted (Fabio, 2026-10-31, portão da Etapa 4.1). É uma alternativa registrada, não a linha de base
(ADR 0015).
Data: 2026-10-31

## Contexto
Com bases iguais à das opções solares (margem de crescimento e bateria dos picos, P-054), a opção A é a mais leve
(`results/etapa4.1/energia.md`):
- 2 MMRTG e 118 kg;
- 6.956 g de Pu-238 [F135];
- não depende da profundidade óptica.

O Fabio pediu os fatos de disponibilidade gravados com fonte, a conta da atividade pela ferramenta e o enquadramento
no NSPM-20.

## Decisão
1. **A opção A fica como alternativa CONDICIONADA à disponibilidade de Pu-238.** Ela volta a ser candidata se o DOE e
   a NASA indicarem inventário para duas MMRTG na janela da missão.
2. **Riscos de programa**, registrados se a alternativa for retomada:
   - disponibilidade de cerca de 7 kg de Pu-238;
   - processo de autorização de lançamento do NSPM-20 [F128].

## Fatos de disponibilidade (literais, `config/energia.yaml`, `lander.pu238.disponibilidade`)
- **[F143] NASA OIG IG-23-010:**
  - p. 27 do PDF: "although DOE planned to produce a total of 1.5 kg from 2018 through 2021, they produced only 0.77 kg";
  - p. 28 do PDF: "the Dragonfly rotorcraft is being designed with one MMRTG requiring 32 fueled clads"; "DOE can only
    produce about 187 fueled clads over that time period—101 fewer than needed";
  - p. 13 do PDF: "a fueled clad containing 150 grams of Pu-238".
- **[F144] NASA FY 2025 Congressional Justification, p. PS-104:** "DoE continues to increase annual production,
  producing approximately 700 grams per year".
- **[F145] NASA 2026 GAO-IG Act Report, p. 32 do PDF:** "In July 2025, DOE informed NASA that DOE did not have
  sufficient thermal inventory to provide an in-spec multi-mission radioisotope thermoelectric generator for a
  baselined mission".
- **[F146] NASA FY 2027 Budget Request, p. PS-56:** "The budget assumes a pause in the development of additional units
  after completion of the MMRTG for the Dragonfly mission".

O relatório GAO-17-673 não pôde ser baixado (o endereço devolveu HTML, não PDF) e não foi usado.

## Atividade e NSPM-20 (`tools/energia.py`, `results/etapa4.1/energia.md`)
- **Atividade:** A = (ln 2 / T½) · (m / M) · N_A.
  - T½ = 87,7 anos [F148];
  - N_A [F31];
  - M = 238 g/mol e ano de 365,25 dias (P-058).
- **Resultado:** 4.408 TBq, ou 4,41 × 10⁶ vezes o A2 do Pu-238 (10⁻³ TBq, SSR-6 Tab. 2 [F147]). É 44,1 vezes o
  limite do Tier I (100.000 × A2 [F128]).
- **Enquadramento:** acima do Tier I. É Tier II, ou Tier III se a análise de segurança der probabilidade de 1 em
  1.000.000 ou mais de exposição acima de 25 rem [F128].
  - Essa análise não foi feita.
  - No Tier II e no Tier III, o chefe da agência pede ao administrador da NASA a revisão do INSRB [F128].

## Consequências
- A linha de base fica sem material nuclear (ADR 0015). O preço é a sobrevivência acima de τ = 6, que não está coberta
  (P-057).
- Se a alternativa A for retomada, os 3.950 W térmicos das duas MMRTG podem aquecer o MAV. Isso não foi modelado.
