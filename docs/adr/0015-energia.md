# ADR 0015 — Energia: lander solar com sobrevivência, carga do orbitador por modo e captura com 10 × R-4D-11

Status: Proposed. Itens 1 a 4 decididos pelo Fabio no portão da Etapa 4.1 (2026-10-31); item 5 é proposta para o
mesmo portão, pendente de decisão.
Data: 2026-10-31

## Contexto
A Etapa 4.1 (`docs/etapa4.1_energia.md`, `results/etapa4.1/energia.md`) comparou as fontes de energia do lander em
Jezero (solar e MMRTG) com bases iguais e dimensionou a carga do orbitador por modo (P-053). No primeiro portão o Fabio
escolheu as 2 MMRTG e adotou os 1.022 W. Depois, com os fatos levantados sobre o Pu-238 (ADR 0016), trocou a linha de
base para a opção C, solar com sobrevivência.

A carga de 1.022 W aumenta a plataforma do orbitador. Com ela, a 1ª queima da captura com 8 × R-4D-11 (C2, ADR 0011)
passou de 2.000 s, o limite de queima única do catálogo. Esse limite é requisito da missão Artemis I, não vida
qualificada do motor (`config/motores.yaml`, [F107] p. 6, Tab. 3: "Max Firing Time 2000 seconds"). O Fabio decidiu não
relaxar esse limite e pediu a avaliação de mais motores em arranjo simétrico.

## Decisão
1. **Energia do lander, linha de base: C, solar com sobrevivência.**
   - O painel e a bateria servem a dois casos: operação normal com céu claro e sobrevivência na tempestade global. Fica
     a maior área e a maior bateria dos dois.
   - Na sobrevivência entram o aquecimento do MAV, os aquecedores do próprio lander e uma eletrônica mínima (P-056,
     análogo do Spirit no inverno de 2008 [F141]). O calor das 8 RHUs do MER [F142] entra como aquecimento elétrico:
     a conta supõe um lander sem RHU (caso conservador). Usar RHUs é opção não decidida (Fabio).
2. **Alternativa A (2 × MMRTG): condicionada à disponibilidade de Pu-238** (ADR 0016).
3. **Carga do orbitador: 1.022 W por modo (P-053) é o novo valor-base da P-028**, no lugar de 510 W.
   - Com o Vulcan VC6 a poucos pontos percentuais de margem, o orbitador depende na prática do Falcon Heavy
     descartável.
   - Isso será reavaliado na Etapa 4.5.
4. **Premissas P-050 a P-054:** aprovadas, NÃO VALIDADAS. **P-056 a P-058:** novas, NÃO VALIDADAS.
5. **Proposta, pendente:** captura com **C4, 10 × R-4D-11** em arranjo simétrico (P-055), no lugar da C2.

## Números
- **Captura** (`results/etapa3.1/queima_finita.md`): pior janela (2031), 4 queimas. As três combinações foram calculadas
  nas massas do ponto fixo convergido com a C4.

| Combinação | Motores (kg) | 1ª queima (s) | Propelente da captura (kg) |
| :- | -: | -: | -: |
| C2: 8 × R-4D-11 | 34,5 | 2.037 (acima do limite de 2.000) | 2.851 |
| C4: 10 × R-4D-11 | 43,1 | 1.605 | 2.813 |
| C5: 12 × R-4D-11 | 51,7 | 1.324 | 2.789 |

- **Antes e depois** (antes: fim da Fase 3, `docs/fase3_relatorio.md`, com 510 W e C2; depois: `results/` atuais, com
  1.022 W e C4):
  - perda de captura do ponto fixo: 72,6 m/s passa a 57,6 m/s (`results/etapa3.1/perdas_calculadas.md`);
  - plataforma do orbitador: 496,5 kg passa a 614,0 kg (P-016, `results/etapa2.3/plataformas.md`);
  - apoapse de encontro: 24.992 km passa a 25.952 km;
  - orbitador injetado: 7.205 kg passa a 7.796 kg (`results/etapa2.4/lancamento.md`);
  - margens na pior janela: Falcon Heavy descartável +56 % passa a +44 %; Vulcan VC6 +15 % passa a +6 %.
  - A linha "Anterior (510 W)" de `results/etapa4.1/energia.md` é outra base: é uma sensibilidade com 510 W, mas com as
    perdas e o apoapse atuais.
- **Lander, opção C** (`results/etapa4.1/energia.md`):
  - massa: 318 kg;
  - área: 41,7 m², dimensionada pela sobrevivência;
  - carga de sobrevivência: 2.547 Wh/sol;
  - sensibilidade com a escala linear da P-056: 431 kg.

## Motivos
- **Solar como base:** a disponibilidade de Pu-238 para duas MMRTG não está garantida pelas fontes oficiais (ADR 0016).
- **Mais motores em vez de relaxar o limite:** mudar a regra no momento em que ela é violada não é aceitável (Fabio).
- **C4 e C5, lado a lado (decisão do Fabio):**
  - **C4:** menos motores (10) e uma 1ª queima de 1.605 s, abaixo de 2.000 s.
  - **C5:** a 1ª queima é mais curta (1.324 s). Pela tabela, a soma de motores e propelente da captura é a menor das
    três, porque a redução do propelente supera o acréscimo de motores.
  - **Contra a C5:** 12 motores, mais distante dos 8 do arranjo voado do Orion ESM [F107].
  - **As duas:** sem arranjo voado (P-055).
  - O config e os `results/` estão com a C4. Se a escolha for a C5, tudo é regenerado.

## Consequências
- **Tempestade acima de τ = 6:** a opção C não cobre a sobrevivência (P-057). Com a razão medida pelo Opportunity em
  τ = 10,8 [F140], o painel da opção C produz 13 % da energia de sobrevivência no pior sol da estada.
  - A sobrevivência nessa condição exigiria 313 m².
  - O dado de voo usado é o do próprio Opportunity: ele "tripped a low-power fault and gone silent", e até 20/12/2018
    não houve sinal [F140]. A pesquisa não achou outro dado publicado de energia acima de τ = 6.
  - A duração da fase com τ > 6 e a ponte pela bateria não foram avaliadas.
  - **Isso fica registrado como limitação e como RISCO.**
- **Modelo de insolação contra o Opportunity em τ = 2,1:** o modelo dá uma razão de energia 26 % maior que a medida.
  - Isso indica que as áreas da tempestade podem estar subdimensionadas.
  - A comparação não separa a poeira depositada durante a tempestade, a inclinação do painel nem a latitude.
- **Não há arranjo voado com 10 R-4D-11.** Montagem, desalinhamento e plumas não foram estudados (P-055).
- **Resultados das Fases 2 e 3 regenerados**, com errata em `docs/fase3_relatorio.md`.

## Nota (2026-10-31): decisões do portão da Etapa 4.1
O Fabio decidiu, depois do merge do PR #30:
1. **Captura: C4 (10 × R-4D-11).** O item 5 deixa de ser proposta.
2. **RHUs:** antes de decidir, pediu a variante C + RHU calculada (ver abaixo). A decisão fica para o próximo portão.
3. **P-055 a P-058:** aprovadas, NÃO VALIDADAS.
4. **Risco acima de τ = 6:** aceito como registrado, com a probabilidade de tempestade e a sensibilidade ao fator do
   Opportunity acrescentadas.
5. **Lançador do orbitador:** fica registrado que o orbitador depende, na prática, do Falcon Heavy descartável.

Números (`results/etapa4.1/energia.md`, `results/etapa2.5/arquitetura.md`):
- **Variante C + RHU:**
  - 35 RHUs de 1 W, no lugar dos aquecedores que repõem o calor das RHUs do MER;
  - 61,6 g de Pu-238 e 39,1 TBq, ou 0,391 do limite do Tier I: **Tier I pelo critério de quantidade** (análise de
    segurança não feita);
  - sobrevivência de 1.694 Wh/sol, 853 Wh/sol a menos;
  - 27,7 m² e 245 kg: 14,0 m² e 73 kg a menos que a C.
  - Com RHUs de 0,8 W (o inventário atual [F153]) seriam 44 unidades; com 1,1 W (produção nova [F152]), 32.
- **Tempestade global na estada:**
  - a estada (Ls 190° a 58°) contém 96 % da estação de início das tempestades globais observadas (Ls 185° a 315° [F149]);
  - 8 dos 10 inícios do catálogo caem dentro da estada; os outros 2 (2001 e 2018) começaram pouco antes da chegada e
    estariam em curso;
  - probabilidade de cerca de 25 % por ano marciano [F149] (P-061).
- **Sensibilidade (P-059):** com a energia da tempestade dividida por 1,258, a opção C vai a 52,5 m² e 375 kg, e a C + RHU
  a 34,9 m² e 282 kg.
- **Dependência de lançador:** dos escolhidos para o orbitador, só o Falcon Heavy descartável tem margem ≥ 0 em todos os
  casos da sensibilidade. O Vulcan VC6 fica negativo com a margem de massa ESA e com a margem de Δv de 20 %.

## Nota (2026-10-31): decisões do 2º portão da Etapa 4.1
O Fabio decidiu, depois do merge do PR #31:
1. **Energia do lander: C + RHU** é a nova linha de base (`results/etapa4.1/energia.md`). São 35 RHUs de 1 W, 61,6 g de
   Pu-238, Tier I do NSPM-20 pelo critério de quantidade; 27,7 m² e 245 kg. A opção C sem RHU fica como alternativa.
2. **P-059 a P-061:** aprovadas, NÃO VALIDADAS.
3. **RISCO de disponibilidade de RHUs:**
   - as 35 RHUs da linha de base ficam acima das alocações recentes de 20 (AO do New Frontiers [F144]) e de 24 (Dragonfly
     e Rosalind Franklin, 2026 [F156]);
   - só a de até 40 (Rosalind Franklin, 2024 [F153]) comporta essa quantidade;
   - o inventário atual tem cerca de 0,8 W por unidade [F153], o que pediria 44 RHUs.
4. **Para a Etapa 4.2:** o calor das RHUs no cruzeiro, dentro do aeroshell.
5. **Para a Etapa 4.4** (escolha aprovada pelo Fabio):
   - **Mitigação operacional da tempestade:** o lander só precisa sobreviver até o lançamento do MAV. Estimar a linha do
     tempo mínima da superfície: pouso, busca dos tubos pelos helicópteros (alcance e ritmo do Ingenuity como
     referência), transferência e lançamento do MAV, com fonte ou premissa.
   - Com essa linha do tempo, calcular a probabilidade acumulada de início de tempestade global até o lançamento do MAV,
     pela distribuição de Ls dos inícios do catálogo, e comparar com os 25 % da estada inteira.
   - **Chegada em Ls ~190°**, no início da estação de tempestades: avaliar o efeito na entrada, descida e pouso.
