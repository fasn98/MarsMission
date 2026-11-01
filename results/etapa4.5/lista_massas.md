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
| Circuito de fluido de cruzeiro (rejeição ativa) | — | — | 37,4 | sim | P-077 ([F205], [F165]) |

Itens novos: 340,3 kg; todos os itens: 449,8 kg. A câmera do TRN entra; o computador de visão (VCE) não tem massa publicada e não está na lista.

Dupla contagem: o item do MAV traz 24,1 kg de energia do aquecimento, que a energia C + RHU também cobre.

## O L3 comporta os itens?

L3 = 1 470 kg (SRL seco − MAV − rover de busca). Tirando os itens que estão dentro do L3 (todos menos braço e helicópteros, que somam fora dele), sobram 1 115 kg para o núcleo, contra 688,2 kg da descida seca do Mars 2020 [F204] (sky crane: propulsão, estrutura e aviônica de descida, sem pernas nem plataforma de superfície).

## Rejeição de calor no cruzeiro (lander)

Dissipação: 374 W (lander do SRL [F165] + RHUs, Etapa 4.2), contra 200 W de limite passivo do SRL [F165]: rejeição ativa. Circuito de fluido, como no MSL e no Mars 2020 [F206, F207]: cerca de 37,4 kg (P-077, escala do MPF [F205]).

## Totais e margens dos lançadores

| Caso | Plataforma (kg) | Lander injetado (kg) | Lander: Falcon Heavy (recuperação) | Lander: Falcon Heavy (descartável) | Lander: Vulcan VC2 | Lander: Vulcan VC4 | Lander: Vulcan VC6 | Orbitador: Falcon Heavy (descartável) | Orbitador: Vulcan VC6 |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| A: L3 vigente (P-017) | 1 565 | 4 012 | +17 % | +180 % | +8 % | +62 % | +107 % | +44 % | +6 % |
| B: L3 + itens novos, sem a dupla contagem | 1 881 | 4 654 | +1 % | +141 % | −7 % | +39 % | +78 % | +44 % | +6 % |
| C: núcleo = descida seca do Mars 2020 + todos os itens | 1 114 | 3 096 | +51 % | +263 % | +40 % | +110 % | +168 % | +44 % | +6 % |

## MAV: Isp maior com motor que voou (caso B)

| Motor | Isp (s) | Propelente | Voo | Lander injetado (kg) | Falcon Heavy (recuperação) | Falcon Heavy (descartável) | Vulcan VC2 | Vulcan VC4 | Vulcan VC6 |
| :- | -: | :- | :- | -: | -: | -: | -: | -: | -: |
| R-4D-11 (base, Orion) | 310 | MMH/MON-3 | Artemis I [F107] | 4 654 | +1 % | +141 % | −7 % | +39 % | +78 % |
| LEROS 1b | 317 | MON/hidrazina | Juno, MESSENGER, Mars Global Surveyor [F208] | 4 574 | +2 % | +145 % | −5 % | +42 % | +81 % |
| S400-15 | 321 | MMH/MON | não conferido para o S400-15 (a lista de herança não separa o S400-12) | 4 534 | +3 % | +148 % | −5 % | +43 % | +83 % |
| LEROS 1c | 324 | MON/hidrazina | "more than 60 engines delivered", missões não nomeadas [F209] | 4 507 | +4 % | +149 % | −4 % | +44 % | +84 % |

Margem de sistema do JPL para um conceito nesta fase: 30 % [F210] (margem de massa do sistema, não margem do lançador).
