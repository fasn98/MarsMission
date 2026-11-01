# Lista de massas do lander (gerado por tools/lista_massas_lander.py)

Nenhuma fonte primária pública publica a massa de um lander de Marte por subsistema: o núcleo (estrutura, pernas, propulsão de descida seca, térmico, aviônica, cabeamento, sistema de lançamento do MAV) fica de cima para baixo (L3, P-017).

## Itens identificados

| Item | Básica (kg) | Margem E1 | Prevista (kg) | Novo nas Etapas 4.1–4.4? | Fonte |
| :- | -: | -: | -: | :- | :- |
| Energia: painel e bateria da C + RHU (Etapas 4.1 e 4.2) | — | — | 277,5 | sim | results/etapa4.1/energia.yaml (já com margem) |
| RHUs (35 × 42 g, máximo por unidade) | 1,47 | 27,5 % | 1,9 | sim | [F152] |
| Enlace direto mínimo (Etapa 4.3) | — | — | 22,4 | sim | results/etapa4.3/comunicacao.yaml (já com margem) |
| Câmera do TRN (LCAM do Mars 2020) | 0,86 | 27,5 % | 1,1 | sim | [F203] |
| UHF (Phoenix) | 6,50 | 27,5 % | 8,3 | não | [F74] |
| Radar (Phoenix) | 5,00 | 27,5 % | 6,4 | não | [F74] |
| Braço de coleta (reserva) | 59,00 | 50,0 % | 88,5 | não | [F40] |
| Helicópteros (2) | 5,00 | 27,5 % | 6,4 | não | [F98] |
| Circuito de fluido de cruzeiro (rejeição ativa) | — | — | 35,7 | sim | P-077 ([F205], [F165]) |

Itens novos: 338,6 kg; todos os itens: 448,1 kg. A câmera do TRN entra; o computador de visão (VCE) não tem massa publicada e não está na lista.

Dupla contagem: o item do MAV traz 24,1 kg de energia do aquecimento, que a energia C + RHU também cobre.

## O L3 comporta os itens?

L3 = 1 470 kg (SRL seco − MAV − rover de busca). Tirando os itens que estão dentro do L3 (todos menos braço e helicópteros, que somam fora dele), sobram 1 141 kg para o núcleo, contra 688,2 kg da descida seca do Mars 2020 [F204] (descent stage de sky crane, sem pernas nem plataforma de superfície). A energia do aquecimento do MAV, que fica no item do MAV, não é descontada do L3.

## Rejeição de calor no cruzeiro (lander)

Dissipação: 357 W (máximo do LAMP do SRL [F165] + RHUs, Etapa 4.2), contra 200 W de perda passiva máxima do LAMP [F165]: rejeição ativa. Circuito de fluido, como no MSL e no Mars 2020 [F206, F207]: cerca de 35,7 kg (P-077, escala do MPF [F205], sem margem E1). Conservador: o circuito entra na plataforma de superfície; no MSL e no Mars 2020 o radiador fica no estágio de cruzeiro, descartado antes da entrada [F206].

## Totais e margens dos lançadores

| Caso | Plataforma (kg) | Lander injetado (kg) | Lander: Falcon Heavy (recuperação) | Lander: Falcon Heavy (descartável) | Lander: Vulcan VC2 | Lander: Vulcan VC4 | Lander: Vulcan VC6 | Orbitador: Falcon Heavy (descartável) | Orbitador: Vulcan VC6 |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| A: L3 vigente (P-017) | 1 565 | 4 012 | +17 % | +180 % | +8 % | +62 % | +107 % | +44 % | +6 % |
| B: L3 + itens novos, sem a dupla contagem | 1 879 | 4 650 | +1 % | +141 % | −7 % | +39 % | +78 % | +44 % | +6 % |
| C: núcleo = descida seca do Mars 2020 + todos os itens | 1 112 | 3 093 | +51 % | +263 % | +40 % | +110 % | +168 % | +44 % | +6 % |

## MAV: Isp maior (caso B; só o Isp muda)

Empuxo, número e massa dos motores e o propelente ficam os do R-4D-11. Ganho em pontos sobre o motor de base entre parênteses.

| Motor | Isp (s) | Propelente | Voo | Lander injetado (kg) | Falcon Heavy (recuperação) | Falcon Heavy (descartável) | Vulcan VC2 | Vulcan VC4 | Vulcan VC6 |
| :- | -: | :- | :- | -: | -: | -: | -: | -: | -: |
| R-4D-11 (base, Orion) | 310 | MMH/MON-3 | Artemis I [F107] | 4 650 | +1 % (0,0 pp) | +141 % (0,0 pp) | −7 % (0,0 pp) | +39 % (0,0 pp) | +78 % (0,0 pp) |
| LEROS 1b | 317 | MON/hidrazina | Juno, MESSENGER, Mars Global Surveyor [F208] | 4 571 | +2 % (1,8 pp) | +146 % (4,2 pp) | −5 % (1,6 pp) | +42 % (2,4 pp) | +81 % (3,1 pp) |
| S400-15 | 321 | MMH/MON | não conferido para o S400-15 (a lista de herança não separa o S400-12) | 4 531 | +3 % (2,7 pp) | +148 % (6,4 pp) | −5 % (2,5 pp) | +43 % (3,7 pp) | +83 % (4,7 pp) |
| LEROS 1c | 324 | MON/hidrazina | "more than 60 engines delivered" [F209]; entregues, voo não conferido | 4 503 | +4 % (3,3 pp) | +149 % (7,9 pp) | −4 % (3,0 pp) | +44 % (4,6 pp) | +84 % (5,8 pp) |

Margem de sistema do JPL para um conceito nesta fase: 30 % [F210] (margem de massa do sistema, não margem do lançador).
