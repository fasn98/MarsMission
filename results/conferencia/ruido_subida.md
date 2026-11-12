# Piso de ruído da subida (gerado por tools/ruido_subida.py)

**Diagnóstico (P-116, NÃO VALIDADA); não muda nenhum resultado.** Os tempos de execução não ficam aqui (mudam de máquina para máquina); saem no log.

## Sólido (`voa_solido`), MAV do MSR na divisão de base, guiamento da verificação

Rugosidade: desvio rms do ajuste quadrático da órbita final em 21 passos de 1,0e-04 s na antecedência e de 1,0e-07 rad em θ0. "Apses": maior entre periapse e apoapse, que têm uma quina em e = 0 (a órbita da verificação é quase circular). "Suave": maior entre o semieixo e as componentes do vetor excentricidade vezes o raio-alvo.

| Integrador | rtol | atol | Passo máx. queima / costa (s) | Erro contra a referência: periapse / apoapse / semieixo / excentricidade (m) | Rugosidade apses: antecedência / θ0 (m) | Rugosidade suave: antecedência / θ0 (m) |
| :- | -: | -: | -: | -: | -: | -: |
| atual | 1,0e-09 | 1,0e-06 | 1,00 / 5,00 | 5,2e-02 / 2,3e+00 / 1,2e+00 / 1,1e+00 | 1,1e-07 / 3,2e-01 | 1,6e-09 / 1,7e-01 |
| a | 1,0e-10 | 1,0e-07 | 0,50 / 2,50 | 1,1e-02 / 1,1e-01 / 5,9e-02 / 4,8e-02 | 9,3e-08 / 1,5e-02 | 2,6e-09 / 8,3e-03 |
| b | 1,0e-11 | 1,0e-08 | 0,25 / 1,00 | 3,6e-05 / 4,2e-04 / 1,9e-04 / 2,3e-04 | 1,2e-07 / 9,4e-03 | 4,3e-09 / 5,1e-03 |
| c | 1,0e-12 | 1,0e-09 | 0,10 / 0,50 | 6,5e-05 / 3,8e-04 / 2,2e-04 / 1,6e-04 | 1,1e-07 / 8,3e-04 | 5,6e-09 / 4,5e-04 |

Em grandezas suaves, a rugosidade cai de 1,7e-01 m (integrador atual) para 4,5e-04 m (integrador c): o ruído do integrador existe e cai ao apertá-lo. Em periapse e apoapse, ela fica entre 8,3e-04 e 3,2e-01 m porque mede a quina, não o integrador.

**Errata (2026-11-11):** a primeira versão deste diagnóstico (commit 5729b00, não publicado) media a rugosidade só em periapse e apoapse e concluía que "o ruído do sólido não vem do integrador". Essa conclusão não se sustenta: aquela medida via a quina em e = 0. Vale a medida em grandezas suaves acima. O diagnóstico do ajuste (a quina no resíduo espalhava o custo, tabela abaixo) continua valendo.

## Sólido: menor custo do ajuste, P-111 a 380 km (tolerância da P-110: 1,0e-06, ~14 m)

| Escala | Custo, apses, atual | Erro da órbita (m), apses, atual | Fecha? apses, atual | Custo, suave, atual | Erro da órbita (m), suave, atual | Fecha? suave, atual |
| -: | -: | -: | :- | -: | -: | :- |
| 0,97 | 3,0e+01 | 77 858,8 | não | 1,5e+01 | 55 260,5 | não |
| 0,98 | 2,6e+01 | 72 637,2 | não | 1,3e+01 | 51 542,9 | não |
| 0,99 | 2,3e+01 | 67 554,8 | não | 1,1e+01 | 47 924,6 | não |
| 1,00 | 2,0e+01 | 62 597,1 | não | 9,9e+00 | 44 398,7 | não |
| 1,02 | 1,4e+01 | 53 048,1 | não | 7,1e+00 | 37 608,2 | não |
| 1,03 | 1,2e+01 | 48 444,3 | não | 5,9e+00 | 34 337,3 | não |

## Reprodutibilidade da escala mínima do sólido (P-117), P-111

A escala mínima é a raiz de (maior semieixo de uma circular alcançável) − (raio-alvo). A raiz do caso atual é a de results/familia1/mavs.yaml; nas duas perturbações do tamanho do ruído de ponto flutuante, a raiz é refeita por brentq num intervalo estreito em torno dela (sinais do déficit conferidos); nas variantes do integrador, a estimativa de primeira ordem (déficit na raiz atual dividido pela inclinação do déficit no intervalo).

| Encontro (km) | Variante | Método | Escala | Diferença relativa da escala | GLOM (kg) | Diferença relativa do GLOM | Déficit na raiz (m) |
| -: | :- | :- | -: | -: | -: | -: | -: |
| 380 | atual | raiz de results/familia1/mavs.yaml | 1,1513144255 | 0,0e+00 | 451,196853 | 0,0e+00 | -1,3e-07 |
| 380 | escala + 4,0e-16 no déficit | raiz por brentq em torno da atual | 1,1513144255 | 4,2e-13 | 451,196853 | 4,1e-13 | -1,4e-07 |
| 380 | carga útil × (1 + 1,0e-13) | raiz por brentq em torno da atual | 1,1513144255 | 4,7e-13 | 451,196853 | 4,6e-13 | -3,7e-07 |
| 380 | rtol e atol × 0,5 | primeira ordem (déficit na raiz ÷ inclinação do intervalo) | 1,1513144511 | 2,2e-08 | 451,196863 | 2,2e-08 | -7,5e-03 |
| 380 | rtol e atol × 2,0 | primeira ordem (déficit na raiz ÷ inclinação do intervalo) | 1,1513141575 | -2,3e-07 | 451,196752 | -2,2e-07 | 7,8e-02 |

**As variantes do integrador ficam fora da P-039** (2,2e-08 e -2,3e-07 na escala): a parte do critério que pedia perturbar as tolerâncias do integrador dentro da P-039 **não foi atendida**. Essas variantes mudam o modelo (o erro de truncamento do integrador atual no semieixo é 1,2e+00 m contra a referência), e foram estimadas em primeira ordem, em dois pontos, sem refazer a raiz: não demonstram continuidade.

**Risco residual entre CPUs.** As perturbações de 4,0e-16 na escala e de 1,0e-13 na carga mudam a escala em ~1e-12, porque não viram nenhuma decisão discreta do integrador (aceitar ou rejeitar um passo). Se outra CPU virar uma dessas decisões, o salto pode ter a ordem da rugosidade do integrador atual em grandezas suaves (1,7e-01 m), ~5,2e-07 relativo na escala pela inclinação do déficit, acima da P-039. A prova é a regeneração do CI em outra CPU. A decisão sobre esse risco é do Fabio.

## Hipergólico (`voa`), veículo de referência da subida, guiamento ótimo do integrador atual (tolerâncias da P-107: 1,0 m e 0,1 m/s)

| Integrador | rtol | atol | Passo máx. (s) | Erro contra a referência: altitude (m) / v radial (m/s) / Δv (m/s) | Rugosidade em θ0: altitude (m) / v radial (m/s) / Δv (m/s) |
| :- | -: | -: | -: | -: | -: |
| atual | 1,0e-08 | 1,0e-06 | 2,00 | 6,3e-03 / 1,8e-03 / 2,1e-03 | 2,0e-09 / 1,6e-11 / 1,6e-11 |
| a | 1,0e-10 | 1,0e-08 | 1,00 | 2,5e-04 / 2,3e-05 / 2,7e-05 | 2,4e-04 / 1,3e-05 / 1,5e-05 |
| b | 1,0e-11 | 1,0e-09 | 0,50 | 1,1e-04 / 5,7e-07 / 1,4e-07 | 4,8e-05 / 1,6e-06 / 1,7e-06 |
| c | 1,0e-12 | 1,0e-10 | 0,25 | 6,3e-06 / 1,4e-07 / 1,4e-07 | 4,5e-06 / 1,6e-07 / 1,8e-07 |

As tolerâncias da P-107 ficam acima da rugosidade do hipergólico em todos os integradores: não há proposta de mudança.
