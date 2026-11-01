# Fase 4: resumo integrado (gerado por tools/fase4.py)

Números das Etapas 4.1 a 4.5 (results/etapa4.*) e da arquitetura vigente (orbital.veiculos sobre config/). Massas em kg.

## Massas (ADR 0019)

| Item | Valor |
| :- | -: |
| Orbitador injetado (regra iii) | 7 796 |
| Lander injetado | 4 615 |
| Massa de entrada do lander | 4 429 |
| Massa pousada do lander | 2 255 |
| Plataforma de superfície (P-017, caso B) | 1 843,7 |
| MAV + energia do aquecimento | 411 |
| Circuito de fluido no estágio de cruzeiro (P-077) | 35,7 |
| Total na órbita baixa da Terra, regra (iii) (orbitador + lander) | 37 675 |

Referência otimista (A: L3 + braço + helicópteros (referência otimista)): plataforma 1 564,9, lander injetado 4 049.

## Lançadores de base (ADR 0020)

| Veículo | Lançador | Margem na base | Pior margem nas sensibilidades | Caso da pior margem |
| :- | :- | -: | -: | :- |
| Orbitador | Falcon Heavy (descartável) | +44 % | +18 % | Margem de Δv 20 % (base 10 %) |
| Lander | Vulcan VC4 | +41 % | +8 % | ε do MAV 0,300 (sem fonte, ilustração do risco) em vez de 0,230 |
| Lander (reserva) | Vulcan VC6 | +80 % | +38 % | ε do MAV 0,300 (sem fonte, ilustração do risco) em vez de 0,230 |

Margem na pior janela, injeção direta; sensibilidades de results/etapa2.5/arquitetura.md (uma premissa por vez).

## Energia (Etapa 4.1, ADR 0015)

- **Lander, C + RHU:** 32,8 m² de painel (172,5 kg) e bateria de 105,0 kg, total 277,5 kg; 35 RHUs (61,6 g de Pu-238).
- **Orbitador:** carga de 1 022 W; painel de 1 314 W no afélio; bateria de 11 367 Wh; plataforma de 614,0 kg.

## Térmico (Etapa 4.2) e rejeição de calor no cruzeiro (Etapa 4.5)

- **MAV a 15 °C (P-027):** 60,8 W, 1 500 Wh/sol.
- **Amostras:** transferência tardia para o MAV, tratada como transiente (+30 °C).
- **Cruzeiro do lander:** 357 W contra 200 W de perda passiva máxima: rejeição ativa, circuito de fluido de 35,7 kg no estágio de cruzeiro.

## Comunicação (Etapa 4.3, ADR 0017)

- **Conjunção solar (SEP ≤ 5°):** 2030-05-06 a 2030-06-13 (39 dias); sem comando de 2030-05-18 a 2030-06-02; SEP mínimo 0,30° em 2030-05-25.
- **Tempo-luz máximo:** 21,2 min.
- **Demanda do lander:** 250 Mbit/sol; helicópteros (envoltória) 983 Mbit/sol.
- **Capacidade dos caminhos (Mbit/sol):** TGO 60 a 2 000; MRO 100 a 1 150; reserva própria (relé + DTE mínimo) 12 a 35.
- **Enlace direto mínimo:** 22,4 kg.

## Operação de superfície (Etapa 4.4, ADR 0018)

Chegada 2029-09-20; início da conjunção 2030-05-06; probabilidade de tempestade global na estada 25 %. Requisitos: folga mínima de 60 dias, alvo de 100 a 180 dias; pouso de precisão obrigatório.

| Distância ao depósito (m) | Ritmo | Helicópteros | Sóis | Lançamento do MAV | Folga até a conjunção (d) | Folga mínima | Alvo |
| -: | :- | -: | -: | :- | -: | :- | :- |
| 200 | SRH | 2 | 43 | 2029-11-03 | 184 | sim | não |
| 200 | SRH | 1 | 63 | 2029-11-23 | 163 | sim | sim |
| 200 | Ingenuity | 2 | 123 | 2030-01-24 | 102 | sim | sim |
| 200 | Ingenuity | 1 | 223 | 2030-05-07 | −1 | não | não |
| 1 700 | SRH | 2 | 63 | 2029-11-23 | 163 | sim | sim |
| 1 700 | SRH | 1 | 103 | 2030-01-03 | 122 | sim | sim |
| 1 700 | Ingenuity | 2 | 623 | 2031-06-22 | — | não | não |
| 1 700 | Ingenuity | 1 | 1 223 | 2033-02-27 | — | não | não |
| 3 850 | SRH | 2 | 93 | 2029-12-24 | 132 | sim | sim |
| 3 850 | SRH | 1 | 163 | 2030-03-06 | 61 | sim | não |
| 3 850 | Ingenuity | 2 | 1 323 | 2033-06-10 | — | não | não |
| 3 850 | Ingenuity | 1 | 2 623 | 2037-02-05 | — | não | não |

Pouso: erro de entrega do Mars 2020 1 700 m; desvio máximo do TRN 600 m; alcance do SRH 700 m por carga; alcance de projeto do Ingenuity 300 m.

## Premissas

77 premissas, 77 NÃO VALIDADAS; 28 criadas na Fase 4 (P-050 a P-077); críticas: P-075. Lista em results/fase4/premissas_nao_validadas.md.
