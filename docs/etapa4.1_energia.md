# Etapa 4.1: energia

Fase 4, subsistemas. Os números vêm de `results/etapa4.1/energia.md` e `.yaml`, gerados por `tools/energia.py` a partir
de `config/energia.yaml`, de `config/plataformas.yaml` e do modelo atual do MAV.

## 1. Pergunta
Esta etapa responde a duas perguntas:
- **Lander em Jezero:** energia solar (irradiância de Marte com fonte, poeira, tempestades) ou gerador a radioisótopo
  (MMRTG), para as cargas da superfície?
- **Orbitador:** painéis e baterias para a distância ao Sol ao longo da missão e para os eclipses da órbita de encontro,
  com carga por modo (cruzeiro, captura, encontro, retorno), incluindo os sensores de encontro.

O portão é a escolha da fonte de energia do lander, pelo Fabio.

## 2. Modelo (`src/orbital/energia.py`)
- **Geometria (SPICE, DE440 + pck00011):**
  - Ls, declinação do Sol e distância Marte–Sol.
  - Conferência: os testes conferem que a declinação máxima (a obliquidade) cai perto de Ls = 90°.
- **Insolação diária na superfície:**
  - Modelo de Appelbaum & Landis [F130]: G_h = G_ob cos z f(z,τ,al)/(1 − al).
  - f é o ajuste polinomial da Eq. (20), com os coeficientes da Tab. V, conferidos na imagem.
  - A integral é feita do nascer ao pôr do Sol.
  - O ajuste vale para τ ≤ 6.
- **Verificação contra a tabela publicada do VL1, a 22,3° N** [F56, Tab. IV]: em cinco pontos, com τ de 0,40 a 3,25, a
  insolação calculada difere da publicada no máximo 1,8 %.
  - **Verificado** dentro do erro máximo que a fonte declara para o próprio ajuste (7 %).
  - A tabela é cálculo publicado (modelo de Appelbaum & Flood), não medida: a comparação verifica a implementação, não a
    física contra Marte.
  - A única âncora medida é a calibração no InSight.
- **Painel:**
  - Horizontal, calibrado no 1º sol do InSight [F131, F132]: 4,6 kWh com 5,14 m² e τ ≈ 0,7, o que dá η = 0,247.
  - Poeira acumulada nos painéis: 0,28 %/sol [F131], sem limpeza (P-051).
- **Massas:**
  - Painel de superfície: 330 W/m² ÷ 80 W/kg [F55].
  - Bateria: 100 Wh/kg e profundidade de descarga de 30 % [F73]. A energia da noite passa pela bateria, com a
    eficiência de recarga da P-029: a produção necessária é 1,125 vez a demanda.
  - Margens de crescimento E1, no ponto médio.
- **MMRTG:**
  - 110 W no início, 45 kg [F52], degradação de 4,8 %/ano [F53], contada desde o lançamento. Na sensibilidade,
    soma-se um ano entre o abastecimento e o lançamento (P-050).
  - A massa é a da unidade voada, sem margem de crescimento e sem bateria de pico.
  - 1.975 W térmicos [F135].

## 3. Lander em Jezero (`results/etapa4.1/energia.md`)
- **Estada:** de 2029-09-20 a 2030-11-08, Ls 190° a 58°. **A estada atravessa a estação de tempestades de poeira.** A
  tempestade global de 2018 começou em Ls ≈ 188° [F134].
- **Demanda por sol, 4.685 Wh/sol:**
  - plataforma: 3.500 Wh/sol (P-032);
  - aquecimento do MAV: 48,0 W, ou 1.185 Wh/sol.
- **Poeira acumulada:** no fim da estada, o fator é 0,324 (sem limpeza).

Picos por sol, colocados na bateria das duas opções pelo mesmo critério (P-054), somando 72,0 Wh:
- braço: 20,0 Wh;
- recarga dos helicópteros: 17,5 Wh;
- transmissões UHF: 34,5 Wh.

O aquecimento, que o pedido também lista entre os picos, entra como carga contínua (MAV 48,0 W e o aquecimento da
plataforma, já na P-032). Ele está na demanda média, não na bateria de picos.

| Fonte | Cenário | Área (m²) | Massa (kg) |
| :- | :- | -: | -: |
| Solar | Céu claro em Jezero, τ = 0,4 [F133] | 18,0 | 193 |
| Solar | Tempestade regional de Jezero, τ = 2 [F133] | 28,7 | 250 |
| Solar | Tempestade global de 2018, τ = 8,5 [F134], calculada com τ = 6 (limite do modelo; otimista) | 76,7 | 502 |
| Solar | Global, só o aquecimento do MAV (o caso que dimensiona a área na sobrevivência) | 19,4 | 129 |
| Solar | **Com sobrevivência:** operação normal com céu claro e só o MAV na tempestade global (maior área e maior bateria) | 19,4 | **201** |
| Solar | Céu claro, sem poeira acumulada (sensibilidade) | 7,1 | 136 |
| **MMRTG** | 2 unidades: 90 kg + margem de 27,5 % + bateria dos picos de 2,9 kg. No fim da estada, 99,9 W cada (90,8 % da inicial), para 190,0 W médios, com sobra de 243 Wh/sol. Com abastecimento um ano antes do lançamento: 95,1 W cada, ainda 2 unidades | — | **118** |

As bases são iguais: as duas fontes levam margem de crescimento e bateria dos picos, com profundidade de descarga de
30 %. O MMRTG usa a margem da geração solar (categoria "painel_solar", P-054).

Leitura:
- **A área solar fica muito além da dos landers que voaram.** Mesmo com céu claro, são 18,0 m², contra 5,14 m² do
  InSight [F131] e 4,2 m² do Phoenix [F40].
- **A poeira acumulada domina.** Sem ela, a área cai para 7,1 m².
- **Numa tempestade global, a operação normal exige 76,7 m²,** e isso ainda é otimista, porque o modelo vai só até τ = 6.
- **Sobrevivência:** o caso considera só o aquecimento do MAV. Os aquecedores de sobrevivência do próprio lander não
  foram incluídos.
- **O MMRTG:**
  - dá energia constante, sem depender de poeira nem de tempestade;
  - fornece 3.950 W térmicos, que podem aquecer o MAV;
  - essa transferência de calor não foi modelada.
- **Cargas da superfície pedidas e onde estão:**
  - **aquecimento do MAV:** calculado acima;
  - **braço:** o do análogo (Phoenix) já está na P-032. O braço do MarsFAST consome 10 W em média [F93], só como
    referência;
  - **comunicação:** o rádio UHF consome 69 W transmitindo e 21 W em espera [F137]. Também já está no análogo da P-032;
  - **recarga dos helicópteros:** não há, porque eles têm energia própria (P-052). Um voo do Ingenuity gasta cerca de
    350 W por até 90 s [F136].
- **O que já está na massa vigente do lander:**
  - a energia da plataforma, no análogo L3 (painéis do Phoenix; P-017 e P-032);
  - a energia do aquecimento do MAV, dimensionada pelo módulo solar do DRA (P-025).
  - Esta etapa mostra que a energia solar real em Jezero é bem maior. A lista de massas da Etapa 4.5 vai consolidar
    isso.

## 4. Orbitador
- **Distância máxima ao Sol** (janelas do envelope e referência): ida 1,507 UA, Marte 1,666 UA, volta 1,665 UA. O
  afélio de Marte é 1,666 UA, e é nele que o painel atual já é dimensionado.
- **Eclipse máximo (pior caso geométrico):** 3,24 h na órbita de encontro e 4,19 h na órbita de 1 sol.
- **Proposta de carga por modo (P-053, lado a lado com a P-028, que continua o valor-base):**

| Modo | Carga | Composição |
| :- | -: | :- |
| Cruzeiro | 745 W | plataforma 445 + CCRS 300 |
| Captura | 310 W | plataforma 310 |
| **Encontro** | **1.022 W** | plataforma 445 + CCRS 500 + Electra 65 + NAC 12 |
| Retorno | 945 W | plataforma 445 + CCRS 500 |

- **O modo dominante é o encontro.** O CCRS sozinho consome tipicamente de 300 a 500 W [F23], e isso não estava nos
  510 W da P-028.
- **O lidar de encontro ficou de fora:** não tem potência em fonte de agência. Por isso a carga do encontro está
  subestimada.

| | Carga | Plataforma | Bateria | Orbitador injetado | Falcon Heavy descartável | Vulcan VC6 |
| :- | -: | -: | -: | -: | -: | -: |
| Atual (P-028) | 510 W | 496,5 kg | 5.500 Wh | 7.205 kg | +56 % | +15 % |
| Proposta (P-053) | 1.022 W | 609,8 kg | 11.021 Wh | 7.882 kg | +42 % | +5 % |

As margens são de injeção direta, na pior janela, com a órbita de encontro fixa.

- **Sensibilidade da bateria:** com a profundidade de descarga do MRO, 40 % [F139], a bateria cai para 4.125 Wh (atual)
  e 8.266 Wh (proposta).

## 5. Para decidir no portão (Fabio)
1. **Fonte de energia do lander:**

Comparação com bases iguais (`results/etapa4.1/energia.md`):

| Opção | Massa | Área | Pu-238 | Tempestade global (inclusive τ > 6) | Degradação na estada |
| :- | -: | -: | :- | :- | :- |
| **A. MMRTG × 2** | 118 kg | — | 6.956 g; **disponibilidade não avaliada**. Em 2016, a produção nos EUA tinha sido retomada, com cerca de 50 g [F53] | não depende de τ | potência no fim: 90,8 % da inicial |
| **B. Solar, céu claro** | 193 kg | 18,0 m² | — | não atravessa: com τ = 6 a energia cai a 23,5 % da de céu claro; τ > 6 não avaliado | poeira: fator 0,324 no fim, sem limpeza |
| **C. Solar com sobrevivência** | 201 kg | 19,4 m² | — | só o aquecimento do MAV até τ = 6 (os aquecedores do lander não foram contados); τ > 6 não avaliado | poeira: fator 0,324 |
| **D. Solar operando na tempestade** | 502 kg | 76,7 m² | — | opera até τ = 6; τ > 6 não avaliado (o pico de 2018 foi 8,5 [F134]) | poeira: fator 0,324 |

Outros pontos:
- **MMRTG:** fornece 3.950 W térmicos, que podem aquecer o MAV (não modelado). O lançamento depende do processo do
  NSPM-20 [F128].
- **Solar:** sem material nuclear. As áreas se comparam com os 5,14 m² do InSight [F131] e os 4,2 m² do Phoenix [F40].

2. **Carga do orbitador:** adotar a proposta por modo (P-053) no lugar dos 510 W da P-028? Isso muda o valor-base de uma
   premissa: o orbitador injetado passa de 7.205 para 7.882 kg, e a margem do Vulcan VC6 cai de +15 para +5 %.
3. **Premissas novas** (NÃO VALIDADAS):
   - **P-054:** cargas de pico e margem do MMRTG;
   - **P-050:** modelo solar (albedo 0,1, data de calibração, painel horizontal, τ constante);
   - **P-051:** sem limpeza;
   - **P-052:** helicópteros com energia própria. Ressalva: a recarga deles entra nos picos da P-054, de forma
     conservadora;
   - **P-053:** carga do orbitador por modo.

## 6. Limitações
- **Cenários de τ:** cada um é constante na estada inteira, como envoltória. Somado à poeira acumulada, o pior sol cai
  sempre no fim da estada (Ls 58°), quando a poeira já acumulou mais. As tempestades não duram a estada inteira (a de
  2018 começou em Ls ≈ 188° e decaiu em escala de 43 sóis [F134]). Por isso a conta é conservadora no cruzamento entre
  tempestade e poeira.
- **Limite do modelo:** τ acima de 6 fica fora do ajuste de Appelbaum, e o pico de 2018 foi 8,5.
- **Painel:** horizontal; inclinação e rastreamento não foram estudados.
- **Calor do MMRTG:** não foi modelado o uso dele para o MAV.
- **MMRTG:** a bateria cobre só os picos (P-054). A sobra de 243 Wh/sol recarrega essa bateria.
- **Orbitador:** o eclipse é o pior caso geométrico (Sol no plano da órbita), e a carga do CCRS por fase não é publicada
  (P-053).
- **Plataforma do lander:** a energia ainda é um análogo (P-032). A lista de baixo para cima fica para a Etapa 4.5.

## Nota (2026-10-31): decisões do portão, opção C completa e captura

O Fabio decidiu no portão (ADR 0015):
- energia do lander com linha de base C, solar com sobrevivência;
- A, 2 × MMRTG, como alternativa condicionada ao Pu-238 (ADR 0016);
- 1.022 W como valor-base da P-028;
- P-050 a P-054 aprovadas, NÃO VALIDADAS.

O texto acima fica como estava no primeiro portão. **Números vigentes: `results/etapa4.1/energia.md`.** Com o ponto
fixo refeito, a demanda do lander passou a 4.691 Wh/sol: o aquecimento do MAV foi a 48,3 W, porque o Δv de subida mudou
com a órbita de encontro.

### Captura (o limite de 2.000 s não foi relaxado)
Com 1.022 W, a 1ª queima da C2 (8 × R-4D-11) passa de 2.000 s. O Fabio pediu a variante com mais motores em arranjo
simétrico (P-055). Os números abaixo são da pior janela (2031), com 4 queimas e as massas do ponto fixo convergido
(`results/etapa3.1/queima_finita.md` e `perdas_calculadas.md`):

| Combinação | Motores (kg) | 1ª queima (s) | Propelente da captura (kg) | Perda (m/s), 1.022 W |
| :- | -: | -: | -: | -: |
| C2: 8 × R-4D-11 | 34,5 | **2.037** (acima de 2.000) | 2.851 | 82 |
| **C4: 10 × R-4D-11 (proposta)** | 43,1 | **1.605** | 2.813 | 58 |
| C5: 12 × R-4D-11 | 51,7 | 1.324 | 2.789 | 42 |

- As três foram calculadas nas massas do ponto fixo com a C4. A perda de 72,6 m/s do fim da Fase 3 era com a C2 e 510 W.
- A C4 e a C5 ficam abaixo de 2.000 s.
- **C5:** a soma de motores e propelente é a menor das três, mas usa 12 motores.
- **Nenhuma das duas** tem arranjo voado (P-055). A escolha é do Fabio (ADR 0015).
- A opção (a), aceitar a queima acima de 2.000 s, não foi preciso avaliar.

### Opção C: sobrevivência do próprio lander e tempestade acima de τ = 6
- **Aquecedores do lander (P-056):** o análogo é o Spirit no inverno de 2008, com 84 Wh/sol de aquecedores e 140 Wh/sol
  para o resto [F141], num rover de 174 kg [F142].
  - O calor do MER também vinha de 8 RHUs de cerca de 1 W [F142], 197 Wh/sol. Sem material nuclear, o lander repõe esse
    calor com aquecedores elétricos.
  - Os aquecedores escalam com a massa da plataforma do lander elevada a 2/3.
  - Na sobrevivência, o total fica em 2.547 Wh/sol: MAV 1.191, aquecedores 1.217 e eletrônica 140.
  - Com escala linear (sensibilidade), 3.860 Wh/sol.
- **Opção C:** 41,7 m² e 318 kg. A área agora sai da sobrevivência, não da operação normal. Na sensibilidade com escala
  linear, 63,2 m² e 431 kg.
- **Dados de voo na tempestade global de 2018 (Opportunity, [F140]):**
  - 652 Wh com τ = 0,64 (sol 5100);
  - 345 Wh com τ = 2,1 (sol 5106);
  - cerca de 22 Wh com τ = 10,8 (sol 5111): "tripped a low-power fault and gone silent".
  - Até 20/12/2018, nenhum sinal desde o sol 5111.
- **Modelo contra o voo:** em τ = 2,1, a razão de energia do modelo é 0,666, contra 0,529 medida (+26 %).
  - O modelo é otimista nesse ponto.
  - A comparação não separa a poeira depositada durante a tempestade, a inclinação do painel nem a geometria.
  - **Não é uma verificação:** fica como comparação com dado publicado, com essas ressalvas.
- **Acima de τ = 6 (P-057):** a razão medida entre τ = 10,8 e τ = 0,64 é 3,4 %. Aplicada ao painel da opção C, no pior
  sol da estada:
  - o painel dá 382 Wh/sol contra 2.865 Wh/sol necessários, ou 13 %;
  - a sobrevivência exigiria 313 m²;
  - na sensibilidade, 13 % e 474 m².
- **Limite declarado:** os dados publicados não bastam para afirmar a sobrevivência da opção C acima de τ = 6.
  - O dado de voo usado, o único que a pesquisa achou acima de τ = 6, termina com o rover sem sinal até 20/12/2018.
  - A duração da fase com τ > 6 e a ponte pela bateria não foram avaliadas.
  - É limitação e RISCO (ADR 0015).

Tabela completa, com bases iguais (`results/etapa4.1/energia.md`):

| Opção | Massa | Área | Pu-238 | Tempestade global (inclusive τ > 6) | Degradação na estada |
| :- | -: | -: | :- | :- | :- |
| **C. Solar com sobrevivência (linha de base)** | 318 kg | 41,7 m² | — | sobrevive (MAV + lander, P-056) até τ = 6; com τ = 10,8, 13 % da energia de sobrevivência (P-057) | poeira: fator 0,324 no fim, sem limpeza |
| A. 2 × MMRTG (alternativa condicionada) | 118 kg | — | 6.956 g; condicionada à disponibilidade (ADR 0016); acima do Tier I do NSPM-20 | não depende de τ | potência no fim: 90,8 % da inicial |
| B. Solar, céu claro | 194 kg | 18,0 m² | — | não atravessa: com τ = 6, a energia cai a 23,5 % da de céu claro | poeira: fator 0,324 |
| D. Solar operando na tempestade | 502 kg | 76,8 m² | — | opera até τ = 6; acima disso, ver a razão do Opportunity | poeira: fator 0,324 |

### Alternativa A: atividade e NSPM-20
- **Atividade:** 4.408 TBq, ou 4,41 × 10⁶ A2. É 44,1 vezes o limite do Tier I.
- **Enquadramento:** Tier II, ou Tier III, dependendo da análise de segurança, que não foi feita.
- Os fatos de disponibilidade, com fonte, estão no ADR 0016.

### Orbitador com 1.022 W (vigente)
Estes números substituem a linha "Proposta (P-053)" da seção 4, que foi calculada antes do ponto fixo com a C4:

| | Plataforma | Orbitador injetado | Falcon Heavy descartável | Vulcan VC6 |
| :- | -: | -: | -: | -: |
| Antes (510 W, C2) | 496,5 kg | 7.205 kg | +56 % | +15 % |
| **Vigente (1.022 W, C4)** | 614,0 kg | 7.796 kg | +44 % | +6 % |

- Com a margem de massa da ESA, o VC6 fica em −1 % (`results/etapa2.5/arquitetura.md`). O orbitador depende na
  prática do Falcon Heavy descartável. A reavaliação fica para a Etapa 4.5.

### Premissas novas (NÃO VALIDADAS)
- **P-055:** arranjo simétrico de 10 e 12 R-4D-11.
- **P-056:** sobrevivência do lander pelo Spirit.
- **P-057:** razão de energia do Opportunity acima de τ = 6.
- **P-058:** atividade do Pu-238.

## Nota (2026-10-31): variante C + RHU, probabilidade de tempestade e sensibilidade ao fator do Opportunity
Decisões do Fabio no segundo portão (ADR 0015, nota): captura C4; P-055 a P-058 aprovadas; risco acima de τ = 6 aceito,
com a probabilidade acrescentada; dependência do Falcon Heavy descartável registrada (ADR 0008). As RHUs ficam para
decidir com a variante abaixo. Números de `results/etapa4.1/energia.md`.

### Variante C + RHU
- **Quantidade:** 35 RHUs de 1 W no lugar dos aquecedores que repõem o calor das RHUs do MER (34,6 W, mesma escala da P-056).
- **Pu-238:**
  - 61,6 g, pela potência específica do Pu-238 calculada pela física (meia-vida [F148], Q do alfa [F154], N_A e e [F31]);
  - essa potência específica coincide com a da MMRTG publicada [F135], a 0,0 %, o que **verifica** a conta contra dado
    publicado.
- **Atividade:** 39,1 TBq, ou 39.056 A2: 0,391 do limite do Tier I, logo **Tier I do NSPM-20 pelo critério de
  quantidade**. Nele, o chefe da agência é a autoridade de lançamento [F128]. A análise de segurança não foi feita: com
  probabilidade de 1 em 1.000.000 ou mais de exposição de 5 a 25 rem, o lançamento passaria ao Tier II [F128].
- **Sua estimativa:** ~20 g e ~12 TBq. O enquadramento em Tier I, pelo critério de quantidade, se confirma, mas a quantidade calculada é maior (61,6 g e
  39,1 TBq), porque o calor do MER escalado pede 35 RHUs.
- **Potência por unidade:**

| Potência por RHU | RHUs | Pu-238 |
| :- | -: | -: |
| 1,0 W (MER, base) | 35 | 61,6 g |
| 0,8 W (inventário atual [F153]) | 44 | 62,0 g |
| 1,1 W (produção nova [F152]) | 32 | 62,0 g |

- **Ganho:**
  - sobrevivência de 1.694 Wh/sol, 853 Wh/sol a menos;
  - opção C + RHU: 27,7 m² e 245 kg, ou 14,0 m² e 73 kg a menos que a C;
  - acima de τ = 6 continua sem cobertura: 13 % da sobrevivência, 208 m² necessários.
- **Disponibilidade, com fonte:**
  - existem LWRHUs da era Cassini, com cerca de 0,8 W, e o DOE reconstitui a produção, com campanha dedicada prevista para
    2027 [F153];
  - a potência do inventário cai cerca de 0,01 W por ano [F155];
  - alocações recentes:
    - até 20 LWRHUs no AO do New Frontiers [F144];
    - 24 no Dragonfly [F156];
    - no Rosalind Franklin, "Up to 40" em 2024 [F153] e 24 em 2026 [F156].
  - A variante pede 32 RHUs (1,1 W), 35 (1 W) ou 44 (0,8 W). As três passam de 20 e de 24; as de 32 e 35 ficam dentro
    do "up to 40" de 2024. A disponibilidade para esta missão não foi confirmada.
  - A quantidade usa a potência nominal: não se desconta o decaimento até a estada (cerca de 0,01 W por ano no
    inventário [F155]).

### Tempestade global na estada
- **Estação:** as tempestades globais observadas começaram entre Ls 185° e 315° [F149]. A estada vai de Ls 190° a 58° e
  contém 96 % dessa estação.
- **Catálogo:** 8 dos 10 inícios caem dentro da estada [F150, F151]. Os de 2001 e 2018 começaram em Ls 185°, pouco
  antes da chegada, e estariam em curso ("persist for weeks to months" [F134]).
- **Probabilidade:** cerca de 25 % por ano marciano [F149]. A estada atravessa uma única estação; o trecho de antes da
  chegada conta como exposição, porque tempestades que começam ali ainda estariam em curso. Por isso a probabilidade na
  missão é cerca de 25 % (P-061).
- **Limitações:** a estatística vem de 11 tempestades registradas, com observação incompleta antes de 1997. A fração com
  τ acima de 6 no sítio não foi avaliada: a de 2018 chegou a 8,5 em Gale [F134] e a 10,8 no Opportunity [F140].

### Sensibilidade ao fator do Opportunity (P-059)
A energia dos cenários de tempestade é dividida por 1,258, a razão do modelo sobre a razão medida em τ = 2,1:

| Cenário | Área | Área com o fator | Massa | Massa com o fator |
| :- | -: | -: | -: | -: |
| Tempestade regional, τ = 2 | 28,7 m² | 36,2 m² | 250 kg | 289 kg |
| Tempestade global, operação normal | 76,8 m² | 96,6 m² | 502 kg | 607 kg |
| **Opção C** | 41,7 m² | **52,5 m²** | 318 kg | **375 kg** |
| **Opção C + RHU** | 27,7 m² | **34,9 m²** | 245 kg | **282 kg** |

### Premissas novas (NÃO VALIDADAS)
- **P-059:** fator do Opportunity nas tempestades.
- **P-060:** tolerância do teste da potência específica.
- **P-061:** probabilidade de tempestade global na estada.

## Nota (2026-10-31): fechamento da etapa (ADR 0015)
- **Linha de base do lander: C + RHU**, com 27,7 m² e 245 kg. A C sem RHU fica como alternativa
  (`results/etapa4.1/energia.md`).
- **P-059 a P-061:** aprovadas, NÃO VALIDADAS.
- **Risco registrado:** as 35 RHUs passam das alocações recentes de 20 e de 24. Só a de até 40 comporta.
- **Pendências** (ADR 0015, nota do 2º portão):
  - **Etapa 4.2:** o calor das RHUs no cruzeiro, dentro do aeroshell.
  - **Etapa 4.4:** a linha do tempo mínima da superfície até o lançamento do MAV, a probabilidade acumulada de tempestade
    até esse lançamento (contra os 25 % da estada) e o efeito da chegada em Ls ~190° na entrada, descida e pouso.
