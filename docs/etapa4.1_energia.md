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
  insolação calculada difere da publicada no máximo 1,8 %. **Verificado** dentro do erro máximo que a fonte declara para
  o próprio ajuste (7 %).
- **Painel:**
  - Horizontal, calibrado no 1º sol do InSight [F131, F132]: 4,6 kWh com 5,14 m² e τ ≈ 0,7, o que dá η = 0,247.
  - Poeira acumulada nos painéis: 0,28 %/sol [F131], sem limpeza (P-051).
- **Massas:**
  - Painel de superfície: 330 W/m² ÷ 80 W/kg [F55].
  - Bateria: 100 Wh/kg e profundidade de descarga de 30 % [F73].
  - Margens de crescimento E1, no ponto médio.
- **MMRTG:**
  - 110 W no início, 45 kg [F52], degradação de 4,8 %/ano [F53], contada desde o lançamento.
  - 1.975 W térmicos [F135].

## 3. Lander em Jezero (`results/etapa4.1/energia.md`)
- **Estada:** de 2029-09-20 a 2030-11-08, Ls 190° a 58°. **Ela cobre toda a estação de tempestades de poeira.** A
  tempestade global de 2018 começou em Ls ≈ 188° [F134].
- **Demanda por sol, 4.685 Wh/sol:**
  - plataforma: 3.500 Wh/sol (P-032);
  - aquecimento do MAV: 48,0 W, ou 1.185 Wh/sol.
- **Poeira acumulada:** no fim da estada, o fator é 0,324 (sem limpeza).

| Fonte | Cenário | Área (m²) | Massa (kg) |
| :- | :- | -: | -: |
| Solar | Céu claro em Jezero, τ = 0,4 [F133] | 16,0 | 180 |
| Solar | Tempestade regional de Jezero, τ = 2 [F133] | 25,5 | 230 |
| Solar | Tempestade global de 2018, τ = 8,5 [F134], calculada com τ = 6 (limite do modelo; otimista) | 68,2 | 454 |
| Solar | Global, só o aquecimento do MAV (sobrevivência) | 17,2 | 115 |
| Solar | Céu claro, sem poeira acumulada (sensibilidade) | 6,3 | 129 |
| **MMRTG** | 2 unidades; 99,9 W cada no fim da estada, para 190,0 W médios | — | **90** |

Leitura:
- **A área solar fica muito além da dos landers que voaram.** Mesmo com céu claro, são 16 m², contra 5,14 m² do InSight
  [F131] e 4,2 m² do Phoenix [F40].
- **A poeira acumulada domina.** Sem ela, a área cai para 6,3 m².
- **Numa tempestade global, a operação normal exige 68 m²,** e isso ainda é otimista, porque o modelo vai só até τ = 6.
- **O MMRTG:**
  - dá energia constante, sem depender de poeira nem de tempestade;
  - fornece 3.950 W térmicos, que podem aquecer o MAV;
  - essa transferência de calor não foi modelada.
- **Massas fora do lander:** as linhas acima não incluem a energia que já está no análogo L3 da plataforma (painéis do
  Phoenix; ver P-017 e P-032). A lista de massas da Etapa 4.5 vai consolidar isso.
- **Helicópteros:** têm energia própria (P-052). Um voo do Ingenuity gasta cerca de 350 W por até 90 s [F136].
- **Rádio UHF:** 69 W transmitindo e 21 W em espera [F137]. Essa carga já está no análogo da P-032 (Phoenix).

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
  510 W da P-028. O lidar de encontro não tem potência em fonte de agência e ficou de fora.

| | Carga | Plataforma | Bateria | Orbitador injetado | Falcon Heavy descartável | Vulcan VC6 |
| :- | -: | -: | -: | -: | -: | -: |
| Atual (P-028) | 510 W | 496,5 kg | 5.500 Wh | 7.205 kg | +56 % | +15 % |
| Proposta (P-053) | 1.022 W | 609,8 kg | 11.021 Wh | 7.882 kg | +42 % | +5 % |

As margens são de injeção direta, na pior janela, com a órbita de encontro fixa.

- **Sensibilidade da bateria:** com a profundidade de descarga do MRO, 40 % [F139], a bateria cai para 4.125 Wh (atual)
  e 8.266 Wh (proposta).

## 5. Para decidir no portão (Fabio)
1. **Fonte de energia do lander:**

| Opção | Massa | Prós | Contras |
| :- | -: | :- | :- |
| **A. MMRTG × 2** | 90 kg | Energia constante, sem poeira nem tempestade; 3.950 W térmicos que podem aquecer o MAV | Pu-238 e processo de autorização do lançamento (NSPM-20 [F128]); disponibilidade de unidades não conferida |
| **B. Solar, céu claro** | 180 kg, 16 m² | Sem material nuclear | 16 m² contra 5,14 m² do InSight; não atravessa uma tempestade |
| **C. Solar com sobrevivência na tempestade global** | 115 a 454 kg, 17 a 68 m² | Sem material nuclear | Na tempestade, só o aquecimento do MAV (a plataforma desliga); risco de perder o MAV se τ passar de 6 |

2. **Carga do orbitador:** adotar a proposta por modo (P-053) no lugar dos 510 W da P-028? Isso muda o valor-base de uma
   premissa: o orbitador injetado passa de 7.205 para 7.882 kg, e a margem do Vulcan VC6 cai de +15 para +5 %.
3. **Premissas novas** (NÃO VALIDADAS):
   - **P-050:** modelo solar (albedo 0,1, data de calibração, painel horizontal, τ constante);
   - **P-051:** sem limpeza;
   - **P-052:** helicópteros com energia própria;
   - **P-053:** carga do orbitador por modo.

## 6. Limitações
- **Cenários de τ:** cada um é constante na estada inteira, como envoltória. Somado à poeira acumulada, o pior sol cai
  sempre no fim da estada (Ls 58°), quando na realidade as tempestades globais acontecem entre Ls 180° e 330°. Por isso
  a conta é conservadora no cruzamento entre tempestade e poeira.
- **Limite do modelo:** τ acima de 6 fica fora do ajuste de Appelbaum, e o pico de 2018 foi 8,5.
- **Painel:** horizontal; inclinação e rastreamento não foram estudados.
- **Calor do MMRTG:** não foi modelado o uso dele para o MAV.
- **Orbitador:** o eclipse é o pior caso geométrico (Sol no plano da órbita), e a carga do CCRS por fase não é publicada
  (P-053).
- **Plataforma do lander:** a energia ainda é um análogo (P-032). A lista de baixo para cima fica para a Etapa 4.5.
