# Famílias de arquitetura para o portão do MAV (gerado por tools/opcoes_arquitetura.py)

Pedido do Fabio (2026-11-07): sem cálculo novo, só resultados existentes e fontes com página. Não é recomendação. A opinião do agente está separada e rotulada no fim.

## Para onde a NASA convergiu no MSR

A NASA não chegou a escolher uma arquitetura. Em 2024, apontou o MAV como o fator principal de complexidade, custo e risco; em janeiro de 2025, as duas opções de pouso levavam "a smaller version of the Mars Ascent Vehicle"; a proposta de orçamento de 2026 propõe encerrar o programa por custo. O plano de gastos de julho de 2026 ainda tem uma linha do MSR, sem dizer o uso; a situação depois disso não foi conferida.

| Quando | O que a fonte diz |
| :- | :- |
| set/2023 | [F255] PDF p. 17: "Technical issues, risks, and performance-to-date indicate a near zero probability of ERO/CCRS or SRL/MAV meeting the 2027/2028 Launch Readiness Dates (LRDs)"; PDF p. 37: "the mass and volume of the OS drives the size of the Mars Ascent Vehicle"; PDF p. 42: "The current MSR architecture is highly constrained and is not sufficiently robust or resilient to delays" |
| abr/2024 | [F256] PDF p. 25: "the MAV is the primary driver of architecture complexity, cost and risk"; "Significantly smaller and lower-mass MAV designs enable substantially different SRL architectures."; PDF p. 8: "launch Sample Retrieval Lander(SRL)/Mars Ascent Vehicle (MAV) from Earth in 2035" |
| jan/2025 | [F257]: "The first option will leverage previously flown entry, descent, and landing system designs, namely the sky crane method"; "the mission's landed platform will carry a smaller version of the Mars Ascent Vehicle"; "NASA is expected to confirm the program – and its design – in the second half of 2026" |
| mai/2025 | [F258] PDF p. 242: "NASA plans to terminate the Mars Sample Return Program given that current architecture options remain unaffordable" |
| jul/2026 | [F259] PDF p. 2, plano de gastos do FY2026 para a P.L. 119-74: linha "Mars Sample Return 35.0" (milhões de dólares); o documento não diz o uso |

## Família 1: estada longa e orbitador elétrico

- **O que muda:** a missão de referência passa a ter estada longa em Marte, como a do ERO; o orbitador usa propulsão elétrica para espiralar até uma órbita baixa de encontro, e o MAV sobe só até ela.
- **ADRs que reabre:** 0003 (missão de referência), 0005 (órbita de encontro), 0013 (propulsão do orbitador), e 0008/0020 (lançadores) se a massa mudar. O ADR 0013 já registra: "Uma missão de estada longa, como a do ERO, poderia mudar isso".
- **Ordem de grandeza (rota B, results/etapa7.2/rotas_mav.md):** o MAV vai a 4 606 a 4 801 m/s de Δv com margem, contra 5 772 m/s no vigente, e a GLOM de 167 a 189 kg. Mesmo assim, a folga sem deck fica em +0,032 m e +0,000 m, abaixo do alvo de +0,05 m. O orbitador só elétrico (calculado, NÃO verificado, só com o XIPS-25, sem vida conhecida) fecha a massa (7 947 a 9 420 kg, margem de +18,7 a +40,7 % no Falcon Heavy) e a estada de 414 dias (folga de 4,4 a 11,2 dias), mas fica pronto no encontro em 2030-07-02 e 2030-07-18, depois do último lançamento do MAV na referência (2030-03-06); rotas_mav.md registra isso como ordem de grandeza, que não decide.
- **ERO, a estada longa de referência:** [F260]: "It would take ERO about two years to reach its operational orbit around Mars, a year to perform its Mars mission and another two years to leave Mars and return to Earth."; [F260]: "While ERO would use chemical propulsion to enter Mars orbit, it would rely on solar electric propulsion for the cruise to and from Mars, and for placing itself in operational orbit."; [F260]: "Launch vehicle: Ariane 64"; "325 km above Mars surface"; "Mass: 7 tonnes".
- **Riscos:** missão mais longa (o ERO leva cerca de cinco anos na volta completa, pela fonte); propulsão elétrica de alta potência; o MAV ainda precisa de embalagem que caiba.
- **Para decidir, calcular:** a missão de referência com estada longa, a guiagem elétrica otimizada e o MAV para a órbita baixa com o empuxo/peso real (a subida de results/etapa7.2/subida_mav.md com o alvo da órbita baixa).

## Família 2: aeroshell maior que 4,65 m, com outro lançador

- **O que muda:** a cápsula cresce, o MAV deitado ganha comprimento, e o lançador precisa de coifa com envelope maior.
- **ADRs que reabre:** 0022 (arranjo e aeroshell), 0008 e 0020 (lançadores), e o portão da Etapa 7.3 (entrada).
- **Ordem de grandeza:** no Vulcan, com o adaptador da P-097 (0,127 m), o lander de 4,65 m tem folga radial de +0,042 m (contorno reto) e −0,016 m (Ø menor) (results/etapa7.2/rota_a.md, seção 5). A massa por área da rota A fica de 287 a 291 kg/m², contra 211 do Mars 2020 (risco aberto na 7.3); um diâmetro maior reduz esse número, mas sai da herança de voo de 4,5 m ([F251] PDF p. 6).
- **Fontes do MSR:** [F254] PDF p. 13: "Capsule diameter (m)" de 4.65 e >5.4 nas duas colunas do SRL.
- **Lançadores com coifa maior (voos e situação de operação não conferidos em fonte oficial nesta etapa):**
  - **New Glenn (Blue Origin):** coifa de 7 m e envelope dinâmico de 6,228 a 6,350 m ([F264] PDF p. 57: "standard offering PLF measures 7 m (23 ft) in diameter"; PDF p. 58: "A cylindrical volume with a diameter of between 6,228.1 and 6,350 mm"); o guia é de 2018, anterior ao primeiro voo (PDF p. 24: "design targets"), e é cópia de terceiros, não conferida contra o original; voos e situação atual não conferidos em fonte oficial.
  - **Vulcan (ULA), coifa de 21,3 m:** envelope estático de 4,877 m na interface de 1575 mm, 4,826 m e 4,661 m mais acima ([F80] PDF p. 45, Fig. 4.3.1-2, leitura de figura); PDF p. 44: "The 21.3-m (70-ft.) long PLF is available as a mission unique offering", "Some increases in diameter may also be allowed on a mission unique basis, but must be analyzed.".
  - **Ariane 6 (Arianespace), coifa longa:** coifa de 5,4 m ([F81] PDF p. 88: "This nose fairing has an external diameter of 5.4 m."); volume útil de Ø 4,6 m embaixo e 4,7 m no trecho superior do cilindro, com extensão a 4,9 m "Subject to specific analysis" ([F81] PDF p. 85, Fig. 5.3.1b, leitura de figura).
  - **Falcon Heavy (SpaceX), coifa estendida:** [F82] PDF p. 27: "The extended fairing has the same diameter as the standard faring (5.2 m, 17.2 ft)"; "The payload static envelope for the extended fairing is available upon request.".
  - **SLS e Starship:** sem coifa de carga operacional; não avaliados com fonte oficial nesta etapa.
- **O que muda na entrada (fontes da NASA):**
  - [F254] PDF p. 12: "A capsule diameter > 4.65-m may lead to a new launch vehicle fairing, re-thinking facility processing, and new transportation challenges".
  - [F254] PDF p. 13: "Capsule ballistic coefficient (kg/m2)", com efeitos da massa maior: "Less time/altitude margin".
  - [F254] PDF p. 15: "There are small windows to increase the SRL capsule and parachute diameters beyond Mars 2020 (4.5-m and 21.5-m, respectively), but new testing may be required".
  - [F265] PDF p. 17: "a larger supersonic parachute (30 m vs. 21.5 m MSL DGB) combined with one other technology is necessary to make any significant increase in landed payload mass and/or altitude".
  - [F227] PDF p. 3: "MSL will enter the largest entry mass, fly the largest diameter aeroshell".
- **Riscos:** entrada fora da herança de voo (paraquedas, aquecimento, guiagem); só o New Glenn tem envelope publicado bem acima de 4,65 m, com guia anterior ao primeiro voo; o MAV continua com o mesmo Δv.
- **Para decidir, calcular:** o envelope do lançador candidato com a cápsula maior, o MAV deitado na cápsula maior e a entrada (massa por área, abertura do paraquedas).

## Família 3: MAV hipergólico com motor de estágio 1 de 1 a 4 kN

- **O que muda:** o empuxo/peso do MAV sobe e a perda gravitacional cai. Indício, sem cálculo dos candidatos: a base com empuxo/peso maior convergiu, e a rota A, perto de 1, não.
- **ADRs que reabre:** 0011 (motores) e 0023 (rota do MAV).
- **Ordem de grandeza (results/etapa7.2/bocais_alternativas.md):** um R-40B sozinho cabe em Ø 0,57 m com parede, com empuxo/peso de 2,79 em Marte, mas o motor passa a P-086 em 0,111 m, o MAV fica com folga deitado de −0,244 m no aeroshell de 4,5 m e −0,039 m no de 4,65 m, e o Isp usado é 296 s (de [F106]; [F228] dá 293 s); dois R-42 dão empuxo/peso de 1,24, mas não cabem em Ø 0,57 m. Na subida simulada, a base com empuxo/peso de 1,48 converge (results/etapa7.2/subida_mav.md).
- **Candidatos com fonte** (motores de 1 a 4 kN, e, como referência de voo, o de 800 N do Chandrayaan-3, abaixo da faixa; o R-42, de 890 N e em produção por [F228] PDF p. 25, entra só na ordem de grandeza, porque dois não cabem em Ø 0,57 m):
  - **R-40B (folha da Aerojet Rocketdyne, [F228])** (voou; fora de produção): [F228] PDF p. 30: "Expansion Ratio 60:1"; "293 sec"; "10.5 kg (23.0 lbm)"; "Not in Production; Requires component obsolescence update" (dados em results/etapa7.2/bocais_alternativas.md, alternativa F)
  - **LEROS 4 (Nammo)** (em desenvolvimento, TRL 6): [F110] PDF p. 2: "Thrust, nominal inlet pressure 1000 N [225 lbf]"; "Specific Impulse 321 seconds minimum"; "Technology Readiness Level In development, TRL6"
  - **Motor de 800 N do Chandrayaan-3 (ISRO)** (voou; abaixo de 1 kN; sem folha de dados pública): [F261]: "Bi-Propellant Propulsion System (MMH + MON3), 4 nos. of 800 N Throttleable engines"
  - **Motor de 3000 N do Tianwen-1 (China)** (voou; sem folha de dados pública (só empuxo)): [F262]: "A 3000N engine was ignited at 7:52 p.m. (Beijing time) to decelerate Tianwen-1"
  - Não conferidos: LEROS 4-ET e ISE-900: sem folha de dados primária reaberta nesta etapa.
- **Riscos:** pelas fontes, nenhum candidato de 1 a 4 kN tem produção confirmada (R-40B "Not in Production"; LEROS 4 "In development, TRL6", ficha de 2021, situação atual não conferida; os motores da ISRO e do Tianwen-1 sem dado de produção); o R-40B exige atualização de componentes obsoletos pela própria folha; o Isp do R-40B é menor que o do R-4D-11.
- **Para decidir, calcular:** a subida e o comprimento com cada candidato (o mesmo método de results/etapa7.2/subida_mav.md e rota_a.md).

## Família 4: três lançamentos, com o orbitador à parte, como no MSR original

- **Nota sobre o título:** o título é o do pedido. Nas fontes deste PR, dois landers mais o orbitador foram estudados pelo MSR (2021 e 2023) e rejeitados uma vez; nenhuma delas dá três lançamentos como linha de base do MSR.
- **O que muda:** o lander se divide em dois (um com o MAV e outro com a coleta), além do orbitador. O MAV ganha um lander próprio.
- **ADRs que reabre:** 0005 e 0008 (lançamentos separados), 0009 (coleta), 0020 (lançadores) e 0022 (arranjo).
- **Ordem de grandeza:** o Δv do MAV não muda, então o problema de embalagem só muda se o lander dedicado permitir outro arranjo do MAV (por exemplo, sem a carga de coleta ao lado). Não há cálculo disso no estudo.
- **Fontes do MSR:** [F254] PDF p. 8: "The project currently is considering whether to deliver the Sample Fetch Rover (SFR) and Mars Ascent Vehicle (MAV) in one or two launches", "Two launches: Entry system heavier than MSL and Mars 2020, probably no new technologies needed, but more costly"; PDF p. 13: cápsula de 4.65 m no SRL de dois lançamentos, contra >5.4 m no de um lançamento; [F255] PDF p. 7: o segundo lander foi "eventually rejected because of added complexity/cost"; PDF p. 45: "MSR MAV Lander (MML), which includes the MAV and a MAV landing/launch system using a scaled-up Skycrane EDL".
- **Riscos:** custo e complexidade de um terceiro lançamento e de um segundo pouso (a razão da rejeição no MSR); dependência entre os pousos.
- **Para decidir, calcular:** a massa e o arranjo do lander só com o MAV, e as margens dos três lançamentos.

## Decisão do Fabio (2026-11-09): família 1 calculada; 2, 3 e 4 em reserva

| Família em reserva | Motivo |
| :- | :- |
| 2 (aeroshell maior que 4,65 m, outro lançador) | só o New Glenn publica envelope bem acima de 4,65 m, num guia anterior ao primeiro voo, e a entrada sai da herança de 4,5 m |
| 3 (motor de estágio 1 de 1 a 4 kN) | nenhum motor hipergólico de 1 a 4 kN com produção confirmada pelas fontes achadas |
| 4 (três lançamentos) | o Δv do MAV não muda, e o MSR rejeitou o segundo lander por custo e complexidade ([F255] PDF p. 7) |

Resultados da família 1: results/familia1/missao.md e results/familia1/mavs.md.

## Opinião do agente (separada dos dados; não é fato nem recomendação como fato)

- A causa comum é o Δv. A família 1 é a única que ataca o Δv do MAV diretamente; as famílias 2 e 4 tratam a embalagem, e a 3 trata a perda na subida.
- Os dados sugerem que uma combinação pode ser necessária: a rota B sozinha chega perto de caber sem deck, e mais empuxo no estágio 1 reduziria o MAV.
- O próprio MSR terminou apontando o MAV como o fator principal; isso é coerente com o que este estudo achou.
