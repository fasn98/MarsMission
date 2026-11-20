# Orbitador só elétrico da família 1: verificação (gerado por tools/orbitador_so_eletrico.py)

Etapa 2 do plano (issue #68). Plano aprovado pelo Fabio em 2026-11-20. **Calculado, NÃO validado.**

**Os números estão em `results/familia1/diagnostico_orbitador_so_eletrico.md`**, fora da comparação do CI: as trajetórias otimizadas são mínimos locais (CLAUDE.md, regra 6). Este arquivo traz o método e as entradas.

## Método

- **(a) Trechos heliocêntricos:** transcrição de Sims–Flanagan de ordem 4 (`orbital.sims_flanagan`) com as efemérides DE440s, 30 segmentos por trecho, otimizada com SLSQP (P-118). Conferências em `tests/test_sims_flanagan.py`: empuxo zero contra Kepler e Lambert, aceleração tangencial constante contra [F113] p. 31.
- **Ida:** partida da Terra com o v∞ do lançador (variável), chegada ao raio de Hill de Marte com v∞ = 0; objetivo: a maior margem no Falcon Heavy (descartável) pela curva C3 × massa e pela declinação ([F79]). Restrição: o orbitador fica pronto no encontro até o último lançamento do MAV da família 1 (`results/familia1/missao.yaml`).
- **Marte:** espirais de descida e de subida como na rota B (`orbital.hibrido`, verificadas na Etapa 3.2), com o motor desligado no eclipse; MAV lançado pela regra da família 1 (conjunções, recuperação, folga de 60 d).
- **Volta:** partida do raio de Hill com v∞ = 0 a partir da partida mais cedo; objetivo: a maior massa final.
- **Fecho de massa:** o da rota B (`tools/rotas_mav.py`), com a razão de massas de cada trecho heliocêntrico otimizado no lugar do Δv quase circular; a margem de Δv (P-014) multiplica o logaritmo da razão. 4 iterações entre a ida e o fecho (P-122).
- **Ciclo de trabalho:** 95 % (P-120, valor do Dawn [F279] p. 611).
- **(c) Vida e rodízio:** propulsores além dos ativos até o xenônio por propulsor ficar abaixo da vida demonstrada, cada um com a sua PPU (P-121).

## Propulsores

| Propulsor | No catálogo (ADR 0013) | Vida demonstrada (kg de Xe) | Fonte da vida | Voo |
| :- | :- | -: | :- | :- |
| XIPS-25 | sim | 158 | [F274] p. 4, Tab. 3: "Xe throughput (kG) 4 40 114 158" (teste de vida de 16 250 h, perfil de GEO); [F275] p. 1 dá "about 170 kg" para o mesmo teste | [F119] p. 1 |
| NEXT-C | não (avaliação em paralelo, decisão do Fabio em 2026-11-20) | 918 | [F277] p. 2: "processed 918 kg of xenon propellant" (NEXT, teste de longa duração, propulsor de engenharia; a análise do NEXT-C em [F276] p. 7 dá "a conservative minimum" de 700 kg) | [F278] p. 2: "On December 18, 2021, the NEXT-C system underwent its first activation in flight" (DART; cerca de 2 h de operação) |

## (b) Caso publicado

Joffre et al. 2018 [F121], Fig. 4, p. 5: dois exemplos de ida do ERO. Massa inicial e empuxo de Yau 2021 [F22] (outra versão do projeto). O ERO não é comparável na captura: ela é química ([F280] p. 6).

| Exemplo | Partida | Chegada | v∞ de partida (km/s) | v∞ de chegada (km/s) | Δv publicado (km/s) |
| :- | :- | :- | -: | -: | -: |
| Fig. 4, esquerda: empuxo constante, chegada com v∞ (captura química) | 2026-10-02 | 2027-10-14 | 2,23 | 1,47 | 2,59 |
| Fig. 4, direita: chegada com v∞ = 0, arco de voo livre entre dois arcos de empuxo | 2026-06-16 | 2027-10-08 | 2,08 | 0,00 | 5,94 |

Configurações da família 1 avaliadas: XIPS-25: 6, 7, 8, 9, 10, 11, 12 ativos; NEXT-C: 3, 4, 5, 6, 7 ativos; encontro a 380 e 814 km.

