# ADR 0003 — Missão de referência da Fase 1

Status: Accepted (Fabio, 2026-10-27, portão da Etapa 1.3)
Data: 2026-10-27

## Contexto
A Etapa 1.3 apresentou cinco candidatas, sem escolha (docs/etapa1.3_missoes.md).

## Decisão
- Missão de referência: **candidata A, 2028, classe conjunção** (`2028-conjuncao`):
  - partida da Terra em 2028-11-23, chegada a Marte em 2029-09-19;
  - partida de Marte em 2030-11-07, chegada à Terra em 2031-09-22.
- Órbita em Marte: elíptica de 1 sol, 250 × 33.793 km (DRA 5.0 [F18]).
- Captura em Marte **propulsiva** como linha de base. A aerocaptura fica como opção comparada,
  com a ressalva de que nunca foi feita em voo: "Aerocapture has never been performed"
  (NASA/TM-2002-211386 [F21]); "aerocapture has never been demonstrated at any planetary
  destination" (Dutta et al., NASA, 2025, NTRS 20250006035 [F21]).
- Registro em `config/missao_referencia.yaml`.

## Consequências
- Δv propulsivo da missão: 5,40 km/s, impulsivo ideal (`results/etapa1.3/missoes.yaml`).
- A reentrada a 12,34 km/s fica abaixo do limite da P-011 (12,9 km/s).
- A órbita de 1 sol barateia captura e saída, mas aumenta o Δv da subida a partir da superfície.
  Essa troca será fechada na Fase 2.
