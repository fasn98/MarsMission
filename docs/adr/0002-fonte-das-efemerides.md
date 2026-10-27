# ADR 0002 — Fonte das efemérides: DE440 via SPICE, verificada contra o Horizons

Status: Proposed
Data: 2026-10-26

## Contexto
A Fase 1 precisa de posições e velocidades heliocêntricas de Terra e Marte de 2028 a ~2040.

## Decisão
- Usar `de440.bsp` completo (NAIF), via spiceypy, com `naif0012.tls`.
  Alternativas consideradas: `de440s.bsp` (33 MB, 1849–2150; mesma solução, intervalo menor) e
  `de441.bsp` (3 GB, −13200 a +17191). DE440 é a recomendada pelo JPL para trabalho atual e foi a
  especificada na tarefa.
- Marte = baricentro do sistema marciano (NAIF 4), único corpo marciano presente no `de440.bsp`.
- Frame J2000/ICRF, estados geométricos, tempo TDB.
- Verificação: vetores do JPL Horizons gravados em `tests/data/horizons/`.

## Consequências
- Ver docs/etapa1.1_efemerides.md. A comparação com o Horizons verifica o pipeline, não a exatidão
  intrínseca da DE440.
- Trocar para `de440s.bsp` reduziria o download do CI sem mudar os resultados no intervalo usado.
  Fica como opção.
