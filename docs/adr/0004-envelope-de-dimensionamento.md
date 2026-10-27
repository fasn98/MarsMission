# ADR 0004 — Envelope de Δv para dimensionamento

Status: Accepted (Fabio, 2026-10-27; regra explicitada no segundo portão da Etapa 1.3)
Data: 2026-10-27

## Contexto
O veículo deve servir em qualquer janela de ida de 2028 a 2035, não só na missão de referência
(ADR 0003).

## Decisão
- **Regra:** para cada janela de ida (2028, 2031, 2033, 2035), toma-se o **menor Δv propulsivo
  admissível** sob as restrições da missão **robótica**. O **envelope é o maior desses mínimos**.
- Restrições da missão robótica:
  - velocidade de reentrada ≤ 12,9 km/s (P-011, NÃO VALIDADA), aplicada dentro da busca;
  - órbita de Marte elíptica de 1 sol e captura propulsiva (ADR 0003);
  - **sem limite de tempo de trânsito.**
- **Classes consideradas:** conjunção e oposição. A classe `conjuncao_transito_curto` (trânsitos
  ≤ 210 d) **fica de fora**: o limite de 210 d vem do DRA 5.0 ("relatively short transits … less
  than 180 to 210 days", SP p. 47 [F18]) e é uma restrição de tripulação. A missão deste estudo é
  robótica.
- **Valor:** 5,91 km/s, definido por `2035-conjuncao` (impulsivo ideal, sem margem). É calculado
  por `tools/missoes.py` a partir de `config/missao_referencia.yaml` e gravado em
  `results/etapa1.3/missoes.yaml`. Mínimos por janela: 2028 5,40; 2031 5,78; 2033 5,89; 2035 5,91 km/s.
- **A DLA não entra nesta regra.** Ela será avaliada na Fase 2. Afeta principalmente a janela de
  2033, cujo mínimo tem DLA de −55,5°: partir no plano da órbita de estacionamento exigiria
  inclinação ≥ 55,5° ou mudança de plano, e nenhuma das duas está no Δv acima.

## Histórico
No primeiro portão foram citados 6,17 km/s (candidata D). Esse era o pior valor só entre as cinco
candidatas apresentadas. Com a regra aplicada a todas as conjunções e a classe de trânsito curto
incluída, o valor seria 6,64 km/s. O Fabio escolheu a regra acima.

## Consequências
- O envelope não inclui margem; a margem é premissa da Etapa 1.4.
- Se a avaliação de DLA da Fase 2 exigir mudança de plano em 2033, o mínimo dessa janela sobe, e o
  envelope deve ser recalculado.
