# Lista de massas do lander (gerado por tools/lista_massas_lander.py)

Nenhuma fonte primária pública publica a massa de um lander de Marte por subsistema: o núcleo (estrutura, pernas, propulsão de descida seca, térmico, aviônica, cabeamento, sistema de lançamento do MAV) fica de cima para baixo (L3).

P-017 vigente (decisão do portão da 4.5, caso B): 1 843,7 kg. Circuito de fluido no estágio de cruzeiro, descartado antes da entrada: 35,7 kg (config/superficie.yaml, P-077).

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
| Circuito de fluido de cruzeiro (rejeição ativa; no estágio de cruzeiro) | — | — | 35,7 | sim | P-077 ([F205], [F165]) |

Na plataforma de superfície (sem o circuito, que vai no estágio de cruzeiro): itens novos 302,9 kg; todos os itens 412,4 kg. A câmera do TRN entra; o computador de visão (VCE) não tem massa publicada e não está na lista.

Dupla contagem: o item do MAV traz 24,1 kg de energia do aquecimento, que a energia C + RHU também cobre.

## O L3 comporta os itens?

L3 = 1 470 kg (SRL seco − MAV − rover de busca). Tirando os itens que estão dentro do L3 (todos menos braço e helicópteros, que somam fora dele), sobram 1 177 kg para o núcleo, contra 688,2 kg da descida seca do Mars 2020 [F204] (descent stage de sky crane, sem pernas nem plataforma de superfície). A energia do aquecimento do MAV, que fica no item do MAV, não é descontada do L3.

## Rejeição de calor no cruzeiro (lander)

Dissipação: 357 W (máximo do LAMP do SRL [F165] + RHUs, Etapa 4.2), contra 200 W de perda passiva máxima do LAMP [F165]: rejeição ativa. Circuito de fluido, como no MSL e no Mars 2020 [F206, F207]: cerca de 35,7 kg (P-077, escala do MPF [F205], sem margem E1), no estágio de cruzeiro, descartado antes da entrada, como no MSL e no Mars 2020 [F206].

## Antes e depois das decisões do portão da 4.5

| Caso | Plataforma (kg) | Massa de entrada (kg) | Lander injetado (kg) | Falcon Heavy (recuperação) | Falcon Heavy (descartável) | Vulcan VC2 | Vulcan VC4 | Vulcan VC6 |
| :- | -: | -: | -: | -: | -: | -: | -: | -: |
| Antes: A, sem circuito (P-017 anterior) | 1 564,9 | 3 882 | 4 012 | +17 % | +180 % | +8 % | +62 % | +107 % |
| B com o circuito na plataforma | 1 879,4 | 4 499 | 4 650 | +1 % | +141 % | −7 % | +39 % | +78 % |
| Depois: B, circuito no estágio de cruzeiro (vigente) | 1 843,7 | 4 429 | 4 615 | +1 % | +143 % | −6 % | +41 % | +80 % |

Lançadores de base (ADR 0020): lander no Vulcan VC4 (reserva: Vulcan VC6); orbitador no Falcon Heavy (descartável).

## Totais e margens dos lançadores

| Caso | Plataforma (kg) | Lander injetado (kg) | Lander: Falcon Heavy (recuperação) | Lander: Falcon Heavy (descartável) | Lander: Vulcan VC2 | Lander: Vulcan VC4 | Lander: Vulcan VC6 | Orbitador: Falcon Heavy (descartável) | Orbitador: Vulcan VC6 |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| A: L3 + braço + helicópteros (referência otimista) | 1 565 | 4 049 | +16 % | +177 % | +7 % | +60 % | +105 % | +44 % | +6 % |
| B: A + itens novos, sem a dupla contagem (P-017 vigente) | 1 844 | 4 615 | +1 % | +143 % | −6 % | +41 % | +80 % | +44 % | +6 % |
| C: núcleo = descida seca do Mars 2020 + todos os itens | 1 077 | 3 057 | +53 % | +267 % | +41 % | +112 % | +171 % | +44 % | +6 % |

## MAV: Isp maior (caso B; só o Isp muda)

Empuxo, número e massa dos motores e o propelente ficam os do R-4D-11. Ganho em pontos sobre o motor de base entre parênteses.

| Motor | Isp (s) | Propelente | Voo | Lander injetado (kg) | Falcon Heavy (recuperação) | Falcon Heavy (descartável) | Vulcan VC2 | Vulcan VC4 | Vulcan VC6 |
| :- | -: | :- | :- | -: | -: | -: | -: | -: | -: |
| R-4D-11 (base, Orion) | 310 | MMH/MON-3 | Artemis I [F107] | 4 615 | +1 % (+0,0 pp) | +143 % (+0,0 pp) | −6 % (+0,0 pp) | +41 % (+0,0 pp) | +80 % (+0,0 pp) |
| LEROS 1b | 317 | MON/hidrazina | Juno, MESSENGER, Mars Global Surveyor [F208] | 4 535 | +3 % (+1,8 pp) | +148 % (+4,3 pp) | −5 % (+1,6 pp) | +43 % (+2,5 pp) | +83 % (+3,2 pp) |
| S400-15 | 321 | MMH/MON | não conferido para o S400-15 (a lista de herança não separa o S400-12) | 4 495 | +4 % (+2,7 pp) | +150 % (+6,5 pp) | −4 % (+2,5 pp) | +44 % (+3,7 pp) | +84 % (+4,8 pp) |
| LEROS 1c | 324 | MON/hidrazina | "more than 60 engines delivered" [F209]; entregues, voo não conferido | 4 468 | +5 % (+3,3 pp) | +151 % (+8,0 pp) | −3 % (+3,1 pp) | +45 % (+4,6 pp) | +86 % (+5,9 pp) |

Margem de sistema do JPL para um conceito nesta fase: 30 % [F210] (margem de massa do sistema, não margem do lançador).
