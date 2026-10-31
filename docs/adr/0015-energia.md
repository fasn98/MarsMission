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
     análogo do Spirit no inverno de 2008 [F141]).
2. **Alternativa A (2 × MMRTG): condicionada à disponibilidade de Pu-238** (ADR 0016).
3. **Carga do orbitador: 1.022 W por modo (P-053) é o novo valor-base da P-028**, no lugar de 510 W.
   - Com o Vulcan VC6 a poucos pontos percentuais de margem, o orbitador depende na prática do Falcon Heavy
     descartável.
   - Isso será reavaliado na Etapa 4.5.
4. **Premissas P-050 a P-054:** aprovadas, NÃO VALIDADAS. **P-056 a P-058:** novas, NÃO VALIDADAS.
5. **Proposta, pendente:** captura com **C4, 10 × R-4D-11** em arranjo simétrico (P-055), no lugar da C2.

## Números (de `results/`)
- **Captura** (`results/etapa3.1/queima_finita.md` e `perdas_calculadas.md`): pior janela (2031), 4 queimas, massas
  do ponto fixo convergido.
  - 1ª queima: C2, 2.037 s, acima de 2.000 s; C4, 1.605 s; C5 (12 × R-4D-11), 1.324 s.
  - Massa dos motores: C2, 34,5 kg; C4, 43,1 kg; C5, 51,7 kg.
  - Propelente da captura: C2, 2.851 kg; C4, 2.813 kg.
  - Perda de captura do ponto fixo: 72,6 m/s com a C2 e 510 W; 57,6 m/s com a C4 e 1.022 W.
- **Orbitador** (`results/etapa2.3/plataformas.md`, `results/etapa2.4/lancamento.md`):
  - plataforma: 496,5 kg passa a 614,0 kg (P-016);
  - apoapse de encontro: 24.992 km passa a 25.952 km;
  - orbitador injetado: 7.205 kg passa a 7.796 kg;
  - margens na pior janela: Falcon Heavy descartável +56 % passa a +44 %; Vulcan VC6 +15 % passa a +6 %.
- **Lander, opção C** (`results/etapa4.1/energia.md`):
  - massa: 245 kg;
  - área: 27,7 m², dimensionada pela sobrevivência;
  - carga de sobrevivência: 1.694 Wh/sol;
  - sensibilidade com a escala linear da P-056: 278 kg.

## Motivos
- **Solar como base:** a disponibilidade de Pu-238 para duas MMRTG não está garantida pelas fontes oficiais (ADR 0016).
- **C4 em vez de relaxar o limite:** mudar a regra no momento em que ela é violada não é aceitável (Fabio). A C4 traz
  a 1ª queima abaixo de 2.000 s, com 395 s de folga, por 8,6 kg a mais de motores. Parte disso volta em propelente,
  porque a perda é menor.
- **C4 em vez de C5:** a C4 já fecha com folga; a C5 custa mais 8,6 kg.

## Consequências
- **Tempestade acima de τ = 6:** a opção C não cobre a sobrevivência (P-057). Com a razão medida pelo Opportunity em
  τ = 10,8 [F140], o painel da opção C produz 13 % da energia de sobrevivência no pior sol da estada.
  - A sobrevivência nessa condição exigiria 208 m².
  - O único dado de voo nessa condição é o próprio Opportunity: ele entrou em falha de baixa energia e não foi mais
    ouvido [F140].
  - A duração da fase com τ > 6 e a ponte pela bateria não foram avaliadas.
  - **Isso fica registrado como limitação e como RISCO.**
- **Modelo de insolação contra o Opportunity em τ = 2,1:** o modelo dá uma razão de energia 26 % maior que a medida.
  - Isso indica que as áreas da tempestade podem estar subdimensionadas.
  - A comparação não separa a poeira depositada durante a tempestade, a inclinação do painel nem a latitude.
- **Não há arranjo voado com 10 R-4D-11.** Montagem, desalinhamento e plumas não foram estudados (P-055).
- **Resultados das Fases 2 e 3 regenerados**, com errata em `docs/fase3_relatorio.md`.
