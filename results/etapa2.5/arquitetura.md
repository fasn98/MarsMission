# Arquitetura integrada (gerado por tools/arquitetura.py)

Missão de referência 2028-conjuncao; órbita de encontro 300 × 25 952 km; envelope de Δv 5,912 km/s; injeção direta (ADR 0008); 2 lançamentos. Massas em kg.

## Orbitador (regra iii)

| Item | Propelente | Inerte / massa |
| :- | -: | -: |
| Estágio de inserção em Marte (MMH/MON) | 3 210 | 1 014 |
| Estágio de retorno (MMH/MON) | 1 709 | 540 |
| Carga útil CU-2: CCRS (captura + montagem + proteção contra micrometeoroides) | — | 620 |
| Carga útil CU-2: EEV com COS (valor máximo esperado) | — | 90 |
| Plataforma (P-016, lista por subsistema + sensores de encontro) | — | 614 |
| **Massa injetada** | | **7 796** |

## Lander

| Item | Propelente | Inerte / massa |
| :- | -: | -: |
| Estágio de cruzeiro (correções de trajetória) | 114 | 36 |
| Sistema de entrada, descida e pouso (aeroshell, paraquedas, propelente de descida; P-018) | — | 2 175 |
| Plataforma de superfície L3 (lander do MSR sem MAV e sem rover de busca) | — | 1 470 |
| Braço de coleta de reserva (P-034, com margem) | — | 88 |
| Helicópteros de recuperação (ADR 0009, com margem) | — | 6 |
| Itens das Etapas 4.1 a 4.4 (energia C + RHU, RHUs, enlace direto mínimo, câmera do TRN), sem a energia do aquecimento do MAV já no item do MAV (ADR 0019) | — | 279 |
| MAV hipergólico + energia do aquecimento (ADR 0007) | — | 411 |
| Painéis do armazenamento criogênico no cruzeiro (só MAV criogênico; descartados antes da entrada) | — | 0 |
| Circuito de fluido de rejeição de calor no estágio de cruzeiro (P-077; descartado antes da entrada) | — | 36 |
| **Massa injetada** | | **4 615** |

Massa de entrada 4 429 kg; massa pousada 2 255 kg.

MAV O4: ε 0,230, Δv de subida com margem 5,772 km/s; mav_1: Isp 310 s, Δv 2,777 km/s, massa inicial 386,8 kg, propelente 231,6 kg; mav_2: Isp 310 s, Δv 2,996 km/s, massa inicial 86,0 kg, propelente 53,9 kg.

## Lançadores (forma a): pior margem nas quatro janelas

| Veículo | Lançador | Pior margem |
| :- | :- | -: |
| orbitador | Falcon Heavy (descartável) | +44 % |
| orbitador | Vulcan VC6 | +6 % |
| lander | Falcon Heavy (recuperação) | +1 % |
| lander | Falcon Heavy (descartável) | +143 % |
| lander | Vulcan VC2 | −6 % |
| lander | Vulcan VC4 | +41 % |
| lander | Vulcan VC6 | +80 % |

## Cronograma da missão de referência (datas em TDB)

| Evento | Data |
| :- | :- |
| Lançamentos do orbitador e do lander (injeção direta, lançamentos separados) | 2028-11-24 |
| Chegada a Marte: captura do orbitador; entrada direta e pouso do lander | 2029-09-20 |
| Estada em Marte (414 d): recuperação dos tubos, coleta de reserva, subida do MAV, encontro | 2029-09-20 a 2030-11-08 |
| Partida de Marte (injeção trans-Terra) | 2030-11-08 |
| Chegada à Terra (reentrada a 12,34 km/s) | 2031-09-23 |

## Sensibilidade (uma premissa por vez; órbita de encontro de base)

| Caso | Premissa | Orbitador injetado | Lander injetado | Orb.: Falcon Heavy (descartável) | Orb.: Vulcan VC6 | Lander: Falcon Heavy (recuperação) | Lander: Falcon Heavy (descartável) | Lander: Vulcan VC2 | Lander: Vulcan VC4 | Lander: Vulcan VC6 |
| :- | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| Base | — | 7 796 | 4 615 | +44 % | +6 % | +1 % | +143 % | −6 % | +41 % | +80 % |
| Margem de massa GSFC (+15 % da básica) nas duas plataformas (lander: L3 + braço + helicópteros com GSFC + itens das Etapas 4.1 a 4.4) | P-033 | 8 231 | 5 082 | +36 % | +1 % | −8 % | +121 % | −15 % | +28 % | +63 % |
| Margem de massa ESA (20 % × 20 %) nas duas plataformas (lander: L3 + braço + helicópteros com ESA + itens das Etapas 4.1 a 4.4) | P-033 | 8 345 | 5 923 | +35 % | −1 % | −21 % | +90 % | −27 % | +10 % | +40 % |
| Plataforma do lander no limite inferior (L1; sem os helicópteros, como definido na Etapa 2.3) | P-017, P-035 | 7 796 | 1 945 | +44 % | +6 % | +141 % | +477 % | +122 % | +234 % | +326 % |
| Plataforma do lander no limite superior (SRL 2024 − MAV) | P-017, P-035 | 7 796 | 5 947 | +44 % | +6 % | −21 % | +89 % | −27 % | +9 % | +39 % |
| Razão pousada/entrada 0,624 (Viking, a partir de órbita) em vez de 0,509 | P-018 | 7 796 | 3 771 | +44 % | +6 % | +24 % | +198 % | +15 % | +72 % | +120 % |
| Margem de Δv 5 % (base 10 %) | P-014 | 7 093 | 4 454 | +58 % | +17 % | +5 % | +152 % | −3 % | +46 % | +86 % |
| Margem de Δv 20 % (base 10 %) | P-014 | 9 479 | 5 106 | +18 % | −13 % | −8 % | +120 % | −15 % | +27 % | +62 % |
| Sem penalidade de DLA (multiplicador 1) | P-036 | 7 796 | 4 615 | +56 % | +16 % | +9 % | +164 % | +1 % | +53 % | +95 % |
| ε do MAV 0,238 (MAV com turbobomba, Bowles Tab. 5 [F46]) em vez de 0,230 | — | 7 796 | 4 687 | +44 % | +6 % | −0 % | +139 % | −8 % | +38 % | +77 % |
| ε do MAV 0,176 (só a massa seca, Bowles Tab. 11 [F46]) em vez de 0,230 | — | 7 796 | 4 314 | +44 % | +6 % | +8 % | +160 % | +0 % | +50 % | +92 % |
| ε do MAV 0,300 (sem fonte, ilustração do risco) em vez de 0,230 | P-045 | 7 796 | 6 019 | +44 % | +6 % | −22 % | +86 % | −28 % | +8 % | +38 % |

## Dependência de lançador (escolhidos com margem ≥ 0 na base e em todos os casos da sensibilidade)

- **orbitador:** Falcon Heavy (descartável). Vulcan VC6 fica negativo em: Margem de massa ESA (20 % × 20 %) nas duas plataformas (lander: L3 + braço + helicópteros com ESA + itens das Etapas 4.1 a 4.4); Margem de Δv 20 % (base 10 %).
- **lander:** Falcon Heavy (descartável), Vulcan VC4, Vulcan VC6. Falcon Heavy (recuperação) fica negativo em: Margem de massa GSFC (+15 % da básica) nas duas plataformas (lander: L3 + braço + helicópteros com GSFC + itens das Etapas 4.1 a 4.4); Margem de massa ESA (20 % × 20 %) nas duas plataformas (lander: L3 + braço + helicópteros com ESA + itens das Etapas 4.1 a 4.4); Plataforma do lander no limite superior (SRL 2024 − MAV); Margem de Δv 20 % (base 10 %); ε do MAV 0,238 (MAV com turbobomba, Bowles Tab. 5 [F46]) em vez de 0,230; ε do MAV 0,300 (sem fonte, ilustração do risco) em vez de 0,230. Vulcan VC2 fica negativo em: Base; Margem de massa GSFC (+15 % da básica) nas duas plataformas (lander: L3 + braço + helicópteros com GSFC + itens das Etapas 4.1 a 4.4); Margem de massa ESA (20 % × 20 %) nas duas plataformas (lander: L3 + braço + helicópteros com ESA + itens das Etapas 4.1 a 4.4); Plataforma do lander no limite superior (SRL 2024 − MAV); Margem de Δv 5 % (base 10 %); Margem de Δv 20 % (base 10 %); ε do MAV 0,238 (MAV com turbobomba, Bowles Tab. 5 [F46]) em vez de 0,230; ε do MAV 0,300 (sem fonte, ilustração do risco) em vez de 0,230.
