# Etapa 2.2: estudo de troca do ISRU

Estado: **aguardando o portão do Fabio**, que decide se o ISRU entra na arquitetura. Resultados:
`results/etapa2.2/isru.md` e `.yaml`, gerados por `tools/isru.py`.

## 1. O que se compara

Três opções para a **mesma subida**: órbita de encontro de 300 × 18.483 km (ADR 0005), Δv de
5,685 km/s com margem, carga útil de 16 kg.

| Opção | MAV | Propelente |
| :- | :- | :- |
| **O1** | sólido de dois estágios (Etapa 2.1) | todo da Terra |
| **O2** | LOX/CH4 de dois estágios | todo da Terra |
| **O3** | LOX/CH4 de dois estágios | **O2 produzido em Marte** (MOXIE escalado); **CH4 da Terra** |

**Critério: massa total na órbita baixa da Terra pela regra (iii).** É o orbitador na órbita de
encontro do ADR 0005 (27,3 t) mais o lander com o seu estágio de saída da Terra (lançamentos
separados). Na missão A, o orbitador tem 15,9 t.

Entram na massa pousada do lander:
- o MAV (em O3, com os tanques de O2 vazios);
- a plataforma de superfície (P-017);
- em O2 e O3, o armazenamento criogênico e a fonte de energia;
- em O3, também a planta de O2 e a liquefação.

## 2. Pontos pedidos no portão

1. **Só O2 é produzido; o metano vem da Terra.** Razão de mistura **O/F = 3,5**, a do MAV LOX/CH4 do DRA
   5.0 ("mixture ratio of 3.5:1", Addendum p. 105 [F18]). O O2 é **77,8 %** da massa de propelente,
   coerente com "78%" de Hecht et al. [F48].
   - No MAV LOX/CH4 de base: 189 kg de propelente = 147 kg de O2 + 42 kg de CH4.
   - **O ISRU economiza 147 kg, ou 52 % da massa de decolagem do MAV (281 kg).**
2. **Energia.**
   - A planta é extrapolada linearmente do MOXIE (17,8 kg; ~300 W; 6 g/h [F48]; P-022). Para 147 kg de O2
     em 300 sols (DRA, p. 109 [F18]), a taxa é ~20 g/h, ou **~3,3 vezes o MOXIE**: uma extrapolação
     pequena. A planta sai com ~59 kg e ~1000 W.
   - Duas fontes de energia, cada uma somada ao custo:
     - **MMRTG:** 110 W no início da vida, 45 kg [F52], degradação de 4,8 %/ano [F53] até o fim da estada (1,95 ano).
     - **Solar:** módulo do DRA, 1980 kg por 5 kWe contínuos com armazenamento noturno [F18], escalado
       linearmente (P-025).
3. **Armazenamento criogênico na superfície durante toda a estada.**
   - Usa armazenamento **sem evaporação** (resfriadores ativos), escalado da Tabela 4-31 do DRA
     Addendum #2 [F51] com expoente 2/3 sobre a massa (P-024).
   - Em O3 entra também a **liquefação em linha**, escalada de Johnson et al. [F49] (P-023).
   - **O armazenamento no cruzeiro Terra–Marte (~300 dias) não está modelado.** Esse custo pesa mais em
     O2 (LOX e CH4) do que em O3 (só CH4).

## 3. Resultado (massas em kg)

| Opção | Energia | MAV | Planta + liquefação + armazenamento | Potência | Fonte de energia | Massa pousada | Lander na órbita baixa | **Total (iii)** | Total (missão A) |
| :- | :- | -: | -: | -: | -: | -: | -: | -: | -: |
| O1, sólido | — | 1.404 | — | — | — | 2.254 | 13.854 | **41.168** | 29.709 |
| O2, LOX/CH4 da Terra | 2 MMRTG | 281 | 22 | 180 W | 90 | 1.242 | 7.634 | **34.948** | 23.488 |
| O2, LOX/CH4 da Terra | solar | 281 | 22 | 180 W | 71 | 1.224 | 7.520 | **34.834** | 23.374 |
| O3, ISRU | 13 MMRTG | 281 | 82 | 1.206 W | 585 | 1.650 | 10.141 | **37.455** | 25.995 |
| O3, ISRU | solar | 281 | 82 | 1.206 W | 477 | 1.543 | 9.480 | **36.794** | 25.334 |

Sensibilidade, total pela regra (iii):

| Caso | MMRTG | Solar |
| :- | -: | -: |
| O3 com a planta na escala do DRA (~10× mais leve por kg/h que o MOXIE linear) | 34.638 | 34.424 |
| O2 com ε = 0,114 no MAV LOX/CH4 (Bowles, veículo de ~2 t) | 33.823 | 33.518 |
| O3 com ε = 0,114 | 34.701 | 34.354 |

## 4. Leitura (sem decisão)

1. **O maior efeito não é o ISRU, é a propulsão do MAV.**
   - Trocar o MAV sólido por LOX/CH4, com todo o propelente da Terra (O1 → O2), reduz o total pela regra
     (iii) de 41,2 t para 34,8–34,9 t (−15 %). O MAV cai de 1404 kg para 281 kg.
   - O motivo é o Δv de ~5,7 km/s até a órbita elíptica: com Isp de 282–293 s, o 2º estágio sólido
     trabalha perto do limite da equação do foguete (k·(R−1) ≈ 0,76). Com 370 s fica longe dele (0,50).
   - Essa troca é decisão de arquitetura e deve ser tomada à parte. O MSR escolheu o sólido; o motivo
     não foi analisado aqui.
2. **Nesta escala, o ISRU não compensa no caso de base.** O3 pesa 2,0 a 2,5 t a mais que O2. O O2
   economizado (147 kg) é menor que o que a produção exige:
   - planta + liquefação + armazenamento: 82 kg;
   - fonte de energia: 477 a 585 kg para ~1,2 kW contínuos.
3. **Só no limite otimista** (planta na escala do DRA) o O3 empata ou fica um pouco abaixo do O2:
   34,4–34,6 t contra 34,8–34,9 t, ou seja, −0,3 a −0,4 t. A diferença está dentro da incerteza das
   premissas.
4. **MMRTG × solar:** as massas ficam parecidas (para ~1,2 kW, 13 MMRTG contra ~480 kg de painéis). O
   MMRTG depende de plutônio-238; a disponibilidade para 13 unidades não foi avaliada. O solar
   não inclui tempestade de poeira longa: o DRA estima +7800 kg para 50 dias na sua escala (p. 123).
   Nenhum dos dois pontos foi quantificado aqui.

## 5. Premissas novas (NÃO VALIDADAS)

- **P-021:** ε do MAV LOX/CH4 = 0,286, igual ao do MAV sólido (conservador; faixa até 0,114). Não usa
  média geométrica.
- **P-022:** escala linear da planta a partir do MOXIE.
- **P-023:** escala linear da liquefação. **Atenção:** de 2,2 kg/h para ~0,02 kg/h ela vai a ~1 kg e
  ~32 W, provavelmente abaixo do mínimo real de um resfriador criogênico.
- **P-024:** armazenamento sem evaporação escalado com expoente 2/3.
- **P-025:** escala linear da energia solar.

## 6. Limitações

- Armazenamento criogênico no cruzeiro e o seu custo de energia: não modelados.
- MAV LOX/CH4 com a mesma divisão de Δv e a mesma fração estrutural nos dois estágios; sem isolamento
  específico além do ε. Bowles mostra que o LOX/CH4 tem massa seca maior que o hipergólico.
- Pureza do O2 do MOXIE: requisito > 98 % [F48]. Hoffman et al. 2022 recomendam > 99,6 % para propelente [F54];
  não confirmei se o MOXIE atingiu isso. Não modelado.
- A produção depende de a planta funcionar por 300 sols. O MOXIE fez ciclos curtos (horas); não há
  demonstração de operação contínua.
- Sem estudo de lançador nem de Pu-238 disponível.
