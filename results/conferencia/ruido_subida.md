# Piso de ruído da subida (gerado por tools/ruido_subida.py)

**Diagnóstico (P-116, NÃO VALIDADA); não muda nenhum resultado.** Os tempos de execução não ficam aqui (mudam de máquina para máquina); saem no log.

## Sólido (`voa_solido`), MAV do MSR na divisão de base, guiamento da verificação

Rugosidade: desvio rms do ajuste quadrático da órbita final em 21 passos de 1,0e-04 s na antecedência e de 1,0e-07 rad em θ0. "Apses": maior entre periapse e apoapse, que têm uma quina em e = 0 (a órbita da verificação é quase circular). "Suave": maior entre o semieixo e as componentes do vetor excentricidade vezes o raio-alvo.

| Integrador | rtol | atol | Passo máx. queima / costa (s) | Erro contra a referência: periapse / apoapse / semieixo / excentricidade (m) | Rugosidade apses: antecedência / θ0 (m) | Rugosidade suave: antecedência / θ0 (m) |
| :- | -: | -: | -: | -: | -: | -: |
| atual | 1,0e-09 | 1,0e-06 | 1,00 / 5,00 | 1,0e+00 / 4,2e-02 / 5,4e-01 / 5,0e-01 | 2,0e-01 / 5,4e-01 | 2,2e-09 / 1,3e-01 |
| a | 1,0e-10 | 1,0e-07 | 0,50 / 2,50 | 1,2e-01 / 9,9e-03 / 6,7e-02 / 5,5e-02 | 1,4e-01 / 5,2e-01 | 3,7e-09 / 1,0e-02 |
| b | 1,0e-11 | 1,0e-08 | 0,25 / 1,00 | 3,9e-03 / 7,7e-04 / 2,3e-03 / 3,3e-03 | 1,3e-01 / 5,3e-01 | 3,9e-09 / 4,1e-03 |
| c | 1,0e-12 | 1,0e-09 | 0,10 / 0,50 | 1,5e-05 / 1,5e-05 / 1,5e-05 / 8,4e-06 | 1,3e-01 / 5,3e-01 | 5,5e-09 / 4,3e-04 |

Em grandezas suaves, a rugosidade cai de 1,3e-01 m (integrador atual) para 4,3e-04 m (integrador c): o ruído do integrador existe e cai ao apertá-lo. Em periapse e apoapse, ela fica em 5,4e-01 a 5,3e-01 m porque mede a quina, não o integrador.

**Errata (2026-11-11):** a primeira versão deste diagnóstico (commit 5729b00, não publicado) media a rugosidade só em periapse e apoapse e concluía que "o ruído do sólido não vem do integrador". Essa conclusão não se sustenta: aquela medida via a quina em e = 0. Vale a medida em grandezas suaves acima. O diagnóstico do ajuste (a quina no resíduo espalhava o custo, tabela abaixo) continua valendo.

## Sólido: menor custo do ajuste, P-111 a 380 km (tolerância da P-110: 1,0e-06, ~14 m)

| Escala | Custo, apses, atual | Erro da órbita (m), apses, atual | Fecha? apses, atual | Custo, suave, atual | Erro da órbita (m), suave, atual | Fecha? suave, atual |
| -: | -: | -: | :- | -: | -: | :- |
| 0,97 | 3,8e-06 | 27,7 | não | 5,4e-20 | 0,0 | sim |
| 0,98 | 3,7e-09 | 0,9 | sim | 3,3e-23 | 0,0 | sim |
| 0,99 | 8,9e-05 | 133,4 | não | 2,7e-21 | 0,0 | sim |
| 1,00 | 1,3e-08 | 1,6 | sim | 1,6e-21 | 0,0 | sim |
| 1,02 | 3,9e-04 | 280,5 | não | 2,7e-25 | 0,0 | sim |
| 1,03 | 6,3e-05 | 112,5 | não | 4,3e-25 | 0,0 | sim |

## Reprodutibilidade da escala mínima do sólido (P-117), P-111

A escala mínima é a raiz de (maior semieixo de uma circular alcançável) − (raio-alvo). A raiz do caso atual é a de results/familia1/mavs.yaml; nas duas perturbações do tamanho do ruído de ponto flutuante, a raiz é refeita por brentq num intervalo estreito em torno dela (sinais do déficit conferidos); nas variantes do integrador, a estimativa de primeira ordem (déficit na raiz atual dividido pela inclinação do déficit no intervalo).

| Encontro (km) | Variante | Método | Escala | Diferença relativa da escala | GLOM (kg) | Diferença relativa do GLOM | Déficit na raiz (m) |
| -: | :- | :- | -: | -: | -: | -: | -: |
| 380 | atual | raiz de results/familia1/mavs.yaml | 0,9691792458 | 0,0e+00 | 382,349755 | 0,0e+00 | 5,4e-08 |
| 380 | escala + 4,0e-16 no déficit | raiz por brentq em torno da atual | 0,9691792458 | -1,0e-12 | 382,349755 | -9,7e-13 | 4,4e-07 |
| 380 | carga útil × (1 + 1,0e-13) | raiz por brentq em torno da atual | 0,9691792458 | 1,0e-12 | 382,349755 | 9,9e-13 | 3,0e-07 |
| 380 | rtol e atol × 0,5 | primeira ordem (déficit na raiz ÷ inclinação do intervalo) | 0,9691798569 | 6,3e-07 | 382,349986 | 6,0e-07 | -2,6e-01 |
| 380 | rtol e atol × 2,0 | primeira ordem (déficit na raiz ÷ inclinação do intervalo) | 0,9691775168 | -1,8e-06 | 382,349101 | -1,7e-06 | 7,3e-01 |

As variantes do integrador mudam o modelo (o erro de truncamento), não só o ruído: a diferença delas é a ordem do erro do integrador atual no semieixo, contínua, sem saltos. O ruído de ponto flutuante entre CPUs é o das duas perturbações com a raiz refeita.

## Hipergólico (`voa`), veículo de referência da subida, guiamento ótimo do integrador atual (tolerâncias da P-107: 1,0 m e 0,1 m/s)

| Integrador | rtol | atol | Passo máx. (s) | Erro contra a referência: altitude (m) / v radial (m/s) / Δv (m/s) | Rugosidade em θ0: altitude (m) / v radial (m/s) / Δv (m/s) |
| :- | -: | -: | -: | -: | -: |
| atual | 1,0e-08 | 1,0e-06 | 2,00 | 6,3e-03 / 1,8e-03 / 2,1e-03 | 2,0e-09 / 1,6e-11 / 1,6e-11 |
| a | 1,0e-10 | 1,0e-08 | 1,00 | 2,5e-04 / 2,3e-05 / 2,7e-05 | 2,4e-04 / 1,3e-05 / 1,5e-05 |
| b | 1,0e-11 | 1,0e-09 | 0,50 | 1,1e-04 / 5,7e-07 / 1,4e-07 | 4,8e-05 / 1,6e-06 / 1,7e-06 |
| c | 1,0e-12 | 1,0e-10 | 0,25 | 6,3e-06 / 1,4e-07 / 1,4e-07 | 4,5e-06 / 1,6e-07 / 1,8e-07 |

As tolerâncias da P-107 ficam acima da rugosidade do hipergólico em todos os integradores: não há proposta de mudança.
