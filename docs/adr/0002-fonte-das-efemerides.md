# ADR 0002 — Fonte das efemérides: DE440 (arquivo de440s.bsp) via SPICE, verificada contra o Horizons

Status: Accepted (Fabio, 2026-10-26, com ajuste: de440.bsp → de440s.bsp)
Data: 2026-10-26

## Contexto
A Fase 1 precisa de posições e velocidades heliocêntricas de Terra e Marte de 2028 até ~2040.

## Decisão
- Usar a solução **DE440** (Park et al., 2021, docs/fontes.md [F1]) no arquivo `de440s.bsp` do NAIF,
  via spiceypy, com `naif0012.tls`. O `de440s.bsp` contém a mesma solução DE440 num intervalo
  reduzido (1849-12-25 a 2150-01-21), que cobre a Fase 1 com folga. MD5 conferido contra o checksum
  publicado pelo NAIF (`spk/planets/aa_checksums.txt`).
- Alternativas consideradas: `de440.bsp` (120 MB, 1550–2650; usado na versão Proposed deste ADR) e
  `de441.bsp` (3 GB, −13200 a +17191).
- Marte = baricentro do sistema marciano (NAIF 4), único corpo marciano presente no arquivo.
- Frame J2000/ICRF, estados geométricos, tempo TDB.
- Verificação: vetores do JPL Horizons gravados em `tests/data/horizons/`.

## Consequências
- Download de kernels cai de ~120 MB para ~33 MB, localmente e no CI.
- Nas três épocas de teste, os estados de `de440s.bsp` e `de440.bsp` coincidem bit a bit
  (docs/etapa1.1_efemerides.md).
- Datas fora de 1849–2150 não são suportadas. O teste de cobertura falha se uma etapa futura
  precisar delas.
- A comparação com o Horizons verifica o pipeline, não a exatidão intrínseca da DE440.
