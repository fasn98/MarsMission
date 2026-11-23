# Orbitador só elétrico da família 1: trajetória de baixo empuxo e fecho de massa (gerado por tools/orbitador_so_eletrico.py)

Etapa 2 do plano (issue #68). Plano aprovado pelo Fabio em 2026-11-20. **Calculado, NÃO validado.**

**Os números estão em `results/familia1/diagnostico_orbitador_so_eletrico.md`**, fora da comparação do CI: as trajetórias otimizadas são mínimos locais (CLAUDE.md, regra 6). Este arquivo traz o método e as entradas.

## Método

- **(a) Trechos heliocêntricos:** transcrição de Sims–Flanagan de ordem 4 (`orbital.sims_flanagan`) com as efemérides DE440s, 30 segmentos por trecho, otimizada com SLSQP (P-118). Conferências em `tests/test_sims_flanagan.py`: empuxo zero contra Kepler e Lambert, aceleração tangencial constante contra [F113] p. 31.
- **Ida:** partida da Terra com o v∞ do lançador (variável), chegada ao raio de Hill de Marte com v∞ = 0; objetivo: a maior margem no Falcon Heavy (descartável) pela curva C3 × massa e pela declinação ([F79]). Restrições: DLA ≤ 28,5° (formulação "restricao", P-118) e o orbitador pronto no encontro até o último lançamento do MAV da família 1 (`results/familia1/missao.yaml`); se a tentativa com o prazo falha, tenta-se sem ele, e o prazo entra só na conclusão.
- **Marte:** espirais de descida e de subida como na rota B (`orbital.hibrido`, verificadas na Etapa 3.2), com o motor desligado no eclipse; MAV lançado pela regra da família 1 (conjunções, recuperação, folga de 60 d).
- **Volta:** partida do raio de Hill com v∞ = 0 a partir da partida mais cedo; objetivo: a maior massa final.
- **Fecho de massa:** o da rota B (`tools/rotas_mav.py`), com a razão de massas de cada trecho heliocêntrico otimizado no lugar do Δv quase circular; a margem de Δv (P-014) multiplica o logaritmo da razão. 4 iterações entre a ida e o fecho (P-122).
- **Ciclo de trabalho:** 95 % (P-120, valor do Dawn [F279] p. 611).
- **(c) Vida e rodízio:** propulsores além dos ativos até o xenônio por propulsor ficar abaixo da vida demonstrada, cada um com a sua PPU (P-121).

## Propulsores

| Propulsor | No catálogo (ADR 0013) | Vida usada (kg de Xe por propulsor) | Fonte da vida | Voo |
| :- | :- | -: | :- | :- |
| XIPS-25 | sim | 158 | [F274] p. 4, Tab. 3: "Xe throughput (kG) 4 40 114 158" (teste de vida de 16 250 h, perfil de GEO); [F275] p. 1 dá "about 170 kg" para o mesmo teste | [F119] p. 1 |
| XIPS-25 (87 kg) | sim (o mesmo propulsor) | 87 | [F275] p. 10: "the thruster should be rated at full power for about 87 kg" (modelo CEX-2D a 4,3 kW: "operate for 7270 hours and process 134 kg of xenon", com 50 % de margem) | [F119] p. 1 |
| NEXT-C | não (avaliação em paralelo, decisão do Fabio em 2026-11-20) | 918 | [F277] p. 2: "processed 918 kg of xenon propellant" (NEXT, teste de longa duração, propulsor de engenharia; a análise do NEXT-C em [F276] p. 7 dá "a conservative minimum" de 700 kg) | [F278] p. 2: "On December 18, 2021, the NEXT-C system underwent its first activation in flight" (DART; cerca de 2 h de operação) |

- **XIPS-25, vida a ~4,5 kW:** o teste de vida [F274] processou 4 + 40 kg em alta potência e 114 kg a 2 kW (Tab. 3, p. 4). A plena potência, [F275] p. 10 avalia por modelo (não por teste) o limite em 134 kg e recomenda 87 kg com a margem de 50 %; e diz (p. 1) que vazões maiores são possíveis em trajetórias com muito tempo em baixa potência. Por isso a base de 158 kg (P-121) é carregada ao lado da variante de 87 kg; a aplicação de cada uma a 4,5 kW é premissa NÃO VALIDADA (P-121).
- **NEXT-C, herança de voo limitada:** no DART, o sistema foi ativado em 18/12/2021 e operou cerca de 2 h, com 21 reciclagens; um aumento de corrente na eletrônica de potência da nave, atribuído à interferência de um arco, mostrou teste elétrico insuficiente entre propulsor e nave antes do lançamento e levou à suspensão das operações do NEXT-C ([F278] p. 2). A vida usada é a do NEXT de engenharia em solo ([F277] p. 2).

## Conclusões

Três estados (P-123): "sim" e "não" só fora da banda; dentro dela, "indeterminado". Os números estão no diagnóstico. Xe por propulsor ≤ vida: por construção do rodízio (P-121), quando converge. Uma configuração que não converge é classificada pelo menor resíduo de continuidade alcançado (P-118): acima do aceito, "nenhuma solução viável encontrada" (o que não demonstra inviabilidade); abaixo, "sem convergência do otimizador"; sem resíduo (fecho de massa, vida ou erro), "falha fora do otimizador".

### Conclusão principal: o orbitador só elétrico fecha a 380 km?

Na família 1, o MAV sólido só fecha com encontro a 380 km (decisão do Fabio, 2026-11-22). Fecha, para um propulsor: "sim" se alguma configuração dá "sim" nas quatro colunas; senão, "indeterminado" se alguma convergida tem "indeterminado" e nenhum "não"; "não" se todas convergiram e nenhuma fecha; "não demonstrado" nos outros casos (alguma não convergiu).

| Propulsor | Fecha? | Ativos que fecham |
| :- | :- | :- |
| XIPS-25 | sim | 4, 5, 6, 7, 8, 9, 10, 11, 12 |
| XIPS-25 (87 kg) | indeterminado | — |
| NEXT-C | sim | 3, 4, 5, 6, 7 |

### Por configuração, encontro a 380 km

| Propulsor | Ativos | Encontro (km) | Converge | Margem no Falcon Heavy ≥ 0 % (banda ± 5 pontos) | Pronto até o último lançamento do MAV (banda ± 30 d) | Xe por propulsor ≤ vida |
| :- | -: | -: | :- | :- | :- | :- |
| XIPS-25 | 1 | 380 | não (nenhuma solução viável encontrada) | — | — | — |
| XIPS-25 | 2 | 380 | sim | sim | não | sim |
| XIPS-25 | 3 | 380 | sim | sim | indeterminado | sim |
| XIPS-25 | 4 | 380 | sim | sim | sim | sim |
| XIPS-25 | 5 | 380 | sim | sim | sim | sim |
| XIPS-25 | 6 | 380 | sim | sim | sim | sim |
| XIPS-25 | 7 | 380 | sim | sim | sim | sim |
| XIPS-25 | 8 | 380 | sim | sim | sim | sim |
| XIPS-25 | 9 | 380 | sim | sim | sim | sim |
| XIPS-25 | 10 | 380 | sim | sim | sim | sim |
| XIPS-25 | 11 | 380 | sim | sim | sim | sim |
| XIPS-25 | 12 | 380 | sim | sim | sim | sim |
| XIPS-25 (87 kg) | 1 | 380 | não (nenhuma solução viável encontrada) | — | — | — |
| XIPS-25 (87 kg) | 2 | 380 | não (nenhuma solução viável encontrada) | — | — | — |
| XIPS-25 (87 kg) | 3 | 380 | sim | sim | indeterminado | sim |
| XIPS-25 (87 kg) | 4 | 380 | sim | sim | indeterminado | sim |
| XIPS-25 (87 kg) | 5 | 380 | sim | sim | indeterminado | sim |
| XIPS-25 (87 kg) | 6 | 380 | não (sem convergência do otimizador) | — | — | — |
| XIPS-25 (87 kg) | 7 | 380 | não (sem convergência do otimizador) | — | — | — |
| XIPS-25 (87 kg) | 8 | 380 | não (nenhuma solução viável encontrada) | — | — | — |
| XIPS-25 (87 kg) | 9 | 380 | não (nenhuma solução viável encontrada) | — | — | — |
| XIPS-25 (87 kg) | 10 | 380 | não (nenhuma solução viável encontrada) | — | — | — |
| XIPS-25 (87 kg) | 11 | 380 | sim | não | sim | sim |
| XIPS-25 (87 kg) | 12 | 380 | sim | não | sim | sim |
| NEXT-C | 1 | 380 | sim | sim | não | sim |
| NEXT-C | 2 | 380 | não (nenhuma solução viável encontrada) | — | — | — |
| NEXT-C | 3 | 380 | sim | sim | sim | sim |
| NEXT-C | 4 | 380 | sim | sim | sim | sim |
| NEXT-C | 5 | 380 | sim | sim | sim | sim |
| NEXT-C | 6 | 380 | sim | sim | sim | sim |
| NEXT-C | 7 | 380 | sim | sim | sim | sim |

### Sensibilidade: as outras órbitas de encontro

| Propulsor | Ativos | Encontro (km) | Converge | Margem no Falcon Heavy ≥ 0 % (banda ± 5 pontos) | Pronto até o último lançamento do MAV (banda ± 30 d) | Xe por propulsor ≤ vida |
| :- | -: | -: | :- | :- | :- | :- |
| XIPS-25 | 1 | 814 | não (nenhuma solução viável encontrada) | — | — | — |
| XIPS-25 | 2 | 814 | não (nenhuma solução viável encontrada) | — | — | — |
| XIPS-25 | 3 | 814 | sim | sim | indeterminado | sim |
| XIPS-25 | 4 | 814 | sim | sim | sim | sim |
| XIPS-25 | 5 | 814 | sim | sim | sim | sim |
| XIPS-25 | 6 | 814 | sim | sim | sim | sim |
| XIPS-25 | 7 | 814 | sim | sim | sim | sim |
| XIPS-25 | 8 | 814 | sim | sim | sim | sim |
| XIPS-25 | 9 | 814 | sim | sim | sim | sim |
| XIPS-25 | 10 | 814 | sim | sim | sim | sim |
| XIPS-25 | 11 | 814 | sim | sim | sim | sim |
| XIPS-25 | 12 | 814 | sim | sim | sim | sim |
| XIPS-25 (87 kg) | 1 | 814 | não (nenhuma solução viável encontrada) | — | — | — |
| XIPS-25 (87 kg) | 2 | 814 | não (nenhuma solução viável encontrada) | — | — | — |
| XIPS-25 (87 kg) | 3 | 814 | não (nenhuma solução viável encontrada) | — | — | — |
| XIPS-25 (87 kg) | 4 | 814 | não (nenhuma solução viável encontrada) | — | — | — |
| XIPS-25 (87 kg) | 5 | 814 | sim | sim | sim | sim |
| XIPS-25 (87 kg) | 6 | 814 | sim | sim | sim | sim |
| XIPS-25 (87 kg) | 7 | 814 | sim | sim | sim | sim |
| XIPS-25 (87 kg) | 8 | 814 | sim | sim | sim | sim |
| XIPS-25 (87 kg) | 9 | 814 | sim | sim | sim | sim |
| XIPS-25 (87 kg) | 10 | 814 | sim | sim | sim | sim |
| XIPS-25 (87 kg) | 11 | 814 | sim | sim | sim | sim |
| XIPS-25 (87 kg) | 12 | 814 | sim | sim | sim | sim |
| NEXT-C | 1 | 814 | sim | sim | não | sim |
| NEXT-C | 2 | 814 | sim | sim | sim | sim |
| NEXT-C | 3 | 814 | sim | sim | sim | sim |
| NEXT-C | 4 | 814 | sim | sim | sim | sim |
| NEXT-C | 5 | 814 | sim | sim | sim | sim |
| NEXT-C | 6 | 814 | sim | sim | sim | sim |
| NEXT-C | 7 | 814 | sim | sim | sim | sim |

## (b) Caso publicado

Joffre et al. 2018 [F121], Fig. 4, p. 5: dois exemplos de ida do ERO. Massa inicial e empuxo de Yau 2021 [F22] (outra versão do projeto). O ERO não é comparável na captura: ela é química ([F280] p. 6).

| Exemplo | Partida | Chegada | v∞ de partida (km/s) | v∞ de chegada (km/s) | Δv publicado (km/s) |
| :- | :- | :- | -: | -: | -: |
| Fig. 4, esquerda: empuxo constante, chegada com v infinito (captura química) | 2026-10-02 | 2027-10-14 | 2,23 | 1,47 | 2,59 |
| Fig. 4, direita: chegada com v infinito = 0, arco de voo livre entre dois arcos de empuxo | 2026-06-16 | 2027-10-08 | 2,08 | 0,00 | 5,94 |

Configurações da família 1 avaliadas: XIPS-25: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ativos; XIPS-25 (87 kg): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ativos; NEXT-C: 1, 2, 3, 4, 5, 6, 7 ativos; encontro a 380 e 814 km.

