# ADR 0004 — Envelope de Δv para dimensionamento

Status: Accepted quanto à regra (Fabio, 2026-10-27). **O valor depende de confirmação: ver "Pendência".**
Data: 2026-10-27

## Contexto
O veículo deve servir em qualquer janela de conjunção de 2028 a 2035, não só na missão de
referência (ADR 0003).

## Decisão
- Δv de projeto = maior Δv propulsivo total entre as conjunções das janelas de ida 2028, 2031,
  2033 e 2035, com órbita de 1 sol, captura propulsiva e respeitando o limite de reentrada P-011.
- A regra fica em `config/missao_referencia.yaml`. O valor é calculado por `tools/missoes.py` e
  gravado em `results/etapa1.3/missoes.yaml` (`envelope_dimensionamento`), sem ser digitado à mão.

## Pendência
No portão, o Fabio citou "hoje a D, 6,17 km/s". Com a regra aplicada a todas as conjunções
calculadas e com o limite de reentrada aplicado **dentro** da busca, o valor é **6,64 km/s**,
definido por `2028-conjuncao_transito_curto`. A D era a pior só entre as cinco candidatas
apresentadas. Falta o Fabio confirmar uma de três leituras:
(a) as duas classes de conjunção: 6,64 km/s, como configurado agora;
(b) só a classe `conjuncao`, sem limite de trânsito: 5,91 km/s (2035);
(c) só as candidatas apresentadas: 6,17 km/s (D).

## Consequências
O envelope não inclui margem. A margem é premissa da Etapa 1.4.
