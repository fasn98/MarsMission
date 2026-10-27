# Etapa 2.1: arquitetura de superfície (pouso, subida e encontro)

Estado: **aguardando o portão do Fabio**, que escolhe a arquitetura de superfície e a órbita de
encontro. Nenhuma arquitetura foi escolhida aqui. Resultados: `results/etapa2.1/arquiteturas.md` e
`.yaml`, gerados por `tools/superficie.py`.

## 1. O que as fontes primárias do MSR mostram

- **MAV:** sólido de dois estágios.
  - Versão de 2019: 394 kg na decolagem, 16 kg de carga útil, Isp médio de 293 e 282 s [F34].
  - Versão de 2022: alocação de 400 kg; injeção a 380 km, com inclinação de 27,3° [F35].
  - Nenhum documento da campanha 2019–2024 publica o Δv do MAV. O Δv de subida publicado é o de
    Bowles et al. 2013 [F37], para lançamento equatorial rumo leste.
- **Lander do MSR (SRL):** **entrada direta** a partir da trajetória hiperbólica em todas as versões.
  A versão de 2024 tem 5700 kg de entrada a 5,4 km/s e capacidade pousada de ~2900 kg [F41].
  **Nenhuma fonte primária publica um estudo de troca "entrada direta × a partir de órbita"** para o
  SRL. A propulsão de descida do SRL não é publicada.
- **Encontro:** o orbitador do MSR desce até uma órbita baixa (305 a 450 km) **com propulsão
  elétrica** (Martin-Mur et al. 2024 [F32]). O estudo de 2017 da ESA/Airbus avaliou alternativas
  químicas com aerofrenagem [F44].

## 2. Comparação com MSL, Perseverance, Phoenix e Viking

| Missão | Entrada | Massa de entrada | Massa pousada | Razão pousada/entrada | Fonte |
| :- | :- | -: | -: | -: | :- |
| Viking | a partir de órbita, ~4,61 km/s | 980 kg | 612 kg | 0,624 | [F42] Tab. 1; [F43] |
| Phoenix | direta | 603 kg | 364 kg | 0,604 | [F42] Tab. 1 |
| MSL (projeto) | direta, 5,85 km/s em voo | 3257 kg | 850 kg | 0,261 (sky crane: o estágio de descida não pousa) | [F42] Tab. 1 |
| Perseverance | direta, 5,33 km/s | — | rover de 1025 kg | — | [F45], [F38] |
| SRL (MSR, 2024) | direta, 5,4 km/s | 5700 kg | ~2900 kg (capacidade) | 0,509 | [F41] |

**Descida propulsiva.**
- O MSL de projeto teve Δv ideal de 336,2 m/s, dos quais 161,2 m/s de perda gravitacional [F42,
  Tab. 10].
- Aqui: 82,14 m/s na separação do backshell + g·61,2 s = **0,309 km/s**, com o tempo do voo do
  Perseverance [F38].
- A perda gravitacional vem da equação do movimento ao longo da trajetória, dv/dt = T/m − D/m − g·sen θ
  (Luidens, NASA TM X-52396, Eq. 28 [F39]). **g·t é exato para descida vertical; numa trajetória
  inclinada a perda é ∫g·sen γ dt, menor. A forma vertical foi usada como escolha conservadora.**
- A forma t = Isp·g0/g·ln(m0/m1) e a vazão ṁ = F/(Isp·g0) são **método reaproveitado de projeto
  anterior** (DroneSimulator, modelo `lunar_hopper_tcc`, só leitura). Esse projeto não é fonte, e
  nenhum número dele foi usado.

## 3. Método

- **Subida do MAV** (`src/orbital/superficie.py`):
  - Δv publicado até 100 × 100 km (4027,9 m/s [F37]), mais a transferência coaxial ideal até a órbita
    de encontro, mais o déficit de rotação por lançar na inclinação de 27,3° [F35]. Esse déficit vale
    v_eq·(1 − cos i) = 0,027 km/s, com v_eq da rotação de Marte [F17].
  - **A composição foi verificada contra a própria Tabela 1 de Bowles et al.:** fica de 1,5 a 6 m/s
    acima dos valores publicados para 100 × 500, 500 × 500 e fuga (`tests/test_superficie.py`).
- **MAV:** dois estágios sólidos, com a equação do foguete verificada na Fase 1. Isp de 293 e 282 s
  [F34]; fração estrutural e divisão do Δv derivadas do MAV de 2019 (P-019).
- **Lander:** massa pousada = MAV + plataforma de superfície (P-017, 850 kg). Massa de entrada =
  massa pousada ÷ razão pousada/entrada (P-018: 0,509 para entrada direta, do SRL; 0,624 a partir de
  órbita, do Viking).
- **Arquitetura S3:** o lander se captura em 1 sol e sai de órbita com propulsão bipropelente (321 s,
  ε = 0,24, como na Fase 1).
- **Orbitador:** o Δv extra para descer até a órbita de encontro e o custo extra da injeção trans-Terra
  (o menor entre partir direto da órbita baixa ou subir de volta para 1 sol) entram na queima de
  encontro do estágio de retorno. A massa na órbita baixa da Terra é recalculada pela regra (iii) do
  ADR 0004.
- Margem de 10 % (P-014) nos trechos propulsivos.

## 4. Arquiteturas

| | **S1**: entrada direta + encontro em órbita baixa (como o MSR) | **S2**: entrada direta + encontro na órbita de 1 sol | **S3**: pouso a partir de 1 sol + encontro em órbita baixa | **S4**: como S1, orbitador desce por aerofrenagem |
| :- | :- | :- | :- | :- |
| Órbita de encontro | 380 km circular, 27,3° [F35] | 250 × 33.793 km [F18] | 380 km circular | 380 km circular |
| Δv de subida do MAV (com perdas) | 4,187 km/s | 5,296 km/s | 4,187 km/s | 4,187 km/s |
| Δv da descida propulsiva (orçamento) | 0,309 km/s | 0,309 | 0,309 | 0,309 |
| Δv do lander: captura / saída de órbita | — | — | 1,077 / 0,007 km/s | — |
| Velocidade de entrada: missão A / envelope | 5,76 / 6,04 km/s | 5,76 / 6,04 | 4,71 / 4,71 | 5,76 / 6,04 |
| Δv extra do orbitador (descer + saída de Marte) | 2,375 km/s | 0 | 2,375 km/s | 1,267 km/s (aerofrenagem de ~205 d) |
| MAV na decolagem | 341 kg | 1821 kg | 341 kg | 341 kg |
| Massa pousada | 1191 kg | 2671 kg | 1191 kg | 1191 kg |
| Lander na chegada a Marte (missão A) | 2341 kg | 5248 kg | 3264 kg | 2341 kg |
| **Orbitador na órbita baixa da Terra: missão A / regra (iii)** | **92,9 t / 1109 t** | **13,6 t / 22,8 t** | **92,9 t / 1109 t** | **29,6 t / 60,3 t** |

Referência da Fase 1, sem superfície: orbitador de 13,6 t (missão A) e 22,8 t (regra iii).

Leitura (fatos do modelo, sem recomendação):

- **Descer o orbitador químico da órbita de 1 sol até a órbita baixa custa ~1,2 km/s, e a injeção
  trans-Terra a partir de lá custa outros ~1,2 km/s.** Com propulsão química, isso torna S1 e S3
  inviáveis na prática: pela regra (iii) a massa vai à ordem de 1000 t, perto da assíntota da equação
  do foguete. Capturar direto na órbita baixa não ajuda (2,245 km/s contra 1,059 + 1,198 km/s). É
  coerente com o MSR, cujo orbitador desce com propulsão elétrica.
- **S2** mantém o orbitador da Fase 1, mas o MAV precisa de 5,3 km/s (perto da fuga) e vai a 1,8 t.
  O lander chega a 5,2 t, ordem de grandeza do SRL de 2024 (5,7 t). O encontro acontece numa órbita
  muito elíptica, o que é operacionalmente mais difícil (não modelado).
- **S3** reduz a velocidade de entrada (4,7 km/s) e permite escolher o momento do pouso. Em troca, o
  lander precisa se capturar (+0,9 t na chegada a Marte) e o orbitador ainda tem de descer.
- **S4** usa aerofrenagem, técnica já usada em Marte [F44], e reduz a descida do orbitador para
  0,09 km/s. A injeção trans-Terra a partir da órbita baixa continua cara, e a massa fica em 60 t pela
  regra (iii). A aerofrenagem de ~205 dias cabe na estada da missão A (414 d), mas ocupa metade dela.
- **Velocidade de entrada no envelope:** 6,04 km/s, acima do requisito de 6 km/s do SRL de 2028
  [F32]. A missão A fica em 5,76 km/s.
- **Comparação com o MSR, ordem de grandeza:** o MAV de S1, S3 e S4 (341 kg com margem de 10 %)
  fica na faixa dos MAVs publicados (394 a 400 kg [F34, F35]).

## 5. Premissas novas (NÃO VALIDADAS)

- P-017: plataforma de superfície de 850 kg (faixa de 284 a 2500 kg).
- P-018: razão pousada/entrada (0,509 para entrada direta; 0,624 a partir de órbita).
- P-019: fração estrutural e divisão do Δv entre os estágios do MAV.
- P-020: aerofrenagem (walk-out de 90 m/s, 205 dias).

## 6. Limitações

- A massa do sistema de entrada vem de razões de missões análogas, não de um dimensionamento de
  aeroshell e paraquedas.
- Sem divert na descida (o SRL tinha 4 km de capacidade [F24]); o divert fica coberto só pela margem.
- Órbitas de encontro supostas coplanares com o sítio e com o orbitador; sem fase de encontro nem
  deriva de RAAN.
- O lançamento do lander (estágio de saída da Terra próprio) entra na Etapa 2.4.
- Fonte de projeto anterior: DroneSimulator só como método.
