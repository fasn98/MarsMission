# ADR 0011 — Propulsão química: motores escolhidos e perdas de queima finita calculadas

Status: Accepted (Fabio, 2026-10-27, portões da Etapa 3.1)
Data: 2026-10-27

## Contexto
As Fases 1 e 2 dimensionaram os estágios com manobras impulsivas e somaram as perdas gravitacionais do DRA 5.0 (P-015:
captura 18 m/s, saída de Marte 11 m/s), que são de outro veículo. A Etapa 3.1 montou um catálogo de motores com fonte
primária e calculou a queima finita com o empuxo real, em uma e em várias queimas no periapse
(`docs/etapa3.1_motores.md`, `results/etapa3.1/queima_finita.md`).

## Decisão
1. **Motores** (`config/motores.yaml`, "escolha"):
   - Captura em Marte: **C2, 8 × R-4D-11**.
   - Retorno (injeção trans-Terra): **R3, 4 × R-4D-11**.
   - MAV: estágio 1 **M2, 4 × R-4D-11**; estágio 2 **N2, 1 × R-4D-11**.
   - Cruzeiro do lander: **Z1, 4 × 10N ArianeGroup**.
2. **Isp de voo:**
   - R-4D-11 com a variante que voou no Orion, Isp de 310 s [F107, Tab. 3], na inserção, no retorno e no MAV. Antes eram 321 s
     do motor de 400 N [F28] e 343 s do motor com turbobomba de Bowles et al. [F46].
   - Cruzeiro com 292 s, do 10N [F28 p. 4]. Antes, 321 s.
3. **Limites do R-4D-11:** os 2000 s de queima única e as 40 queimas da Tab. 3 da F107 são **requisitos da missão
   Artemis I, não vida qualificada do motor**. São usados como limite conservador, declarado como tal.
4. **Perdas:** captura e saída de Marte usam a perda de queima finita calculada com C2 e R3, no lugar da P-015.
   - O cálculo usa várias queimas no periapse (P-042, fração do raio de Hill de 0,1, aprovada pelo Fabio).
   - Há um ponto fixo com as massas e a órbita de encontro (`tools/redimensiona.py`, P-044).
   - Valores vigentes em `results/etapa3.1/perdas_calculadas.md`.
   - A P-015 fica para a saída da Terra e para as etapas anteriores.

## Motivos
- **C2 e R3:** cabem no propelente dimensionado e respeitam a queima única e as partidas no caso de projeto, com uma ou
  várias queimas. As combinações de 400 N não cabem, e a 1ª queima delas passa da vida qualificada com qualquer N. O
  OMS-E (C3) perde menos, mas tem 135 kg de motor e disponibilidade não conferida.
- **Um único tipo de motor (R-4D-11)** na captura, no retorno e no MAV (motivo dado pelo Fabio).
- **Isp de voo:** os motores pressurizados de 400 N ou mais que voaram dão 296 a 321 s (o 10N dá 292 s). Os 343 s eram
  de um motor com turbobomba.

## Consequências
- Massas, órbita de encontro (regra dos 5 %, ADR 0005), MAV e margens dos lançadores (ADR 0008) foram refeitos:
  - errata em `docs/fase2_relatorio.md`;
  - notas com data nos ADRs 0005, 0007 e 0008.
- As Etapas 1.4, 2.1 e 2.2 ficam como registro da época. `tools/confere_regeneracao.py` e `tools/confere_2033.py` as
  regeneram com a propulsão de antes (`config/motores.yaml`, "antes_etapa_3_1").
- **Limitação a decidir:** a fração estrutural do MAV (0,238) vem do MAV com turbobomba de Bowles et al. [F46]. Com
  motores pressurizados, os tanques tendem a pesar mais, e isso não foi refeito.
- **Fora desta ADR:** a propulsão nuclear térmica (ADR à parte).

## Nota (2026-10-28): fração estrutural do MAV decidida
A "limitação a decidir" acima foi decidida pelo Fabio: ε = 0,230, do MAV pressurizado de Bowles et al. [F46], com 0,238 e
0,176 como limites. Ver a nota de 2026-10-28 no ADR 0007.
