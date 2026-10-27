# Etapa 3.1: motores reais e queima finita

Fase 3, propulsão. Os números deste documento vêm de `results/etapa3.1/queima_finita.md` e `.yaml`, gerados por
`tools/queima_finita.py` a partir de `config/motores.yaml`, `config/queima_finita.yaml` e do dimensionamento atual
(`orbital.veiculos`). Rótulo de todos os resultados desta etapa: **calculado**. Nenhum foi comparado com um caso
publicado de queima finita; isso fica para a Etapa 3.2.

## 1. Pergunta
As Fases 1 e 2 trataram todas as manobras como impulsivas e somaram as perdas gravitacionais do DRA 5.0 (P-015:
captura 18 m/s, saída de Marte 11 m/s), que são de outro veículo. Com os motores reais que existem, quanto tempo duram as
queimas e quanto se perde?

## 2. Catálogo (`config/motores.yaml`)
Só motores com fonte primária. Cada valor traz a citação literal e a página; as fontes estão em `docs/fontes.md`
(F28, F105 a F112). Valores em lbf e lb foram convertidos pelos fatores do NIST SP 811 [F112].

| Motor | Propelentes | Empuxo | Isp | Massa | Queima única máx. | Voo |
| :- | :- | -: | -: | -: | -: | :- |
| S400-15 (ArianeGroup 400N) | MMH/MON | 425 N | 321 s | 4,30 kg | 1,85 h [F105] | Mars Express 2003, ExoMars Orbiter 2016 (lista do fabricante, sem separar S400-12 de -15) [F28] |
| R-4D-11 (L3Harris) | MON-3/MMH | 110 lbf | 315 s | 9,5 lb | 12.000 s | "F" na ficha [F106]; Orion ESM, 8 auxiliares no Artemis I [F107] |
| R-42 (L3Harris) | MON-3/MMH | 200 lbf | 305 s | 14,5 lb | 3.940 s | "F" na ficha, missão não nomeada [F106] |
| R-40B (L3Harris) | MON-3/MMH | 900 lbf | 296 s | 35 lb | 500 s | "F, NIP": fora de produção [F106] |
| OMS-E (Shuttle / Orion) | MMH/MON-3 | 26,7 kN | 315,1 s | 297 lb [F108] | 1.030 s | 19 missões do Shuttle e Artemis I [F107] |
| LEROS 1b (Nammo) | MON/**hidrazina** | 635 N | 317 s | 4,5 kg | 2.520 s | "18 off ... flown" [F109] |
| LEROS 4 (Nammo) | MON-3/MMH | 1000 N | 321 s | 8,41 kg | 3.600 s | **sem voo comprovado** da versão com ficha ("TRL6") [F110]; fora das combinações |
| 10N (ArianeGroup) | MMH/MON | 10 N | 292 s | 0,35 kg | 8 h | ExoMars Orbiter 2016 (lista do fabricante) [F28] |

Ressalvas registradas no config:
- **S400-15:** a vida acumulada (8,5 h) e os ciclos (135) estão como "planned" na página do fabricante. O S400-12 tem
  1,1 h de queima única qualificada.
- **R-4D-11 no Orion:** a variante que voou (bocal 164:1) dá "Thrust 489 N", "Specific Impulse 310 seconds",
  "Max Firing Time 2000 seconds" e "Number of Burns 40" [F107]. O catálogo e as combinações usam a ficha [F106]
  (315 s). Com a variante do Orion, a C2 e a R3 teriam ~1,6 % menos Δv por quilo de propelente (não recalculado).
- **OMS-E:** as unidades do Orion são motores do Shuttle reformados, a serem substituídos a partir do Artemis VII
  [F107]. A disponibilidade para esta missão **não foi conferida**.
- **Cruzeiro do MSL:** usou hidrazina monopropelente em blow-down, com ~4,35 N por propulsor [F111]. Sem Isp em fonte
  primária, fica só como referência.

## 3. Método
- **Captura e injeção trans-Terra:** `orbital.queima_finita` integra o movimento plano de dois corpos em torno de Marte,
  com empuxo constante tangente à velocidade, vazão T/(Isp·g0) e massa variável (DOP853).
  - **Captura:** periapse de chegada, início e duração da queima são ajustados para a órbita final ter o periapse e o
    apoapse da órbita de 1 sol; o início minimiza o propelente. Para empuxos baixos, a solução sai por continuação no
    empuxo, a partir de uma queima quase impulsiva.
  - **Saída:** a duração dá a energia de v∞²/2; o início minimiza o propelente. A direção da assíntota não é imposta.
  - **Perda de queima finita:** Δv entregue pelo motor (Isp·g0·ln m0/mf) − Δv impulsivo no periapse
    (`orbital.manobras.dv_hiperbole_orbita`, o mesmo das Fases 1 e 2).
- **Cruzeiro e MAV:** tempo de queima pela equação do foguete; empuxo/peso do MAV na superfície de Marte. A perda de
  subida do MAV já está no Δv da Etapa 2.1 e não é recalculada.
- **Casos:**
  - **Projeto:** a pior janela do envelope, como no dimensionamento (regra iii, ADR 0004); captura de 2031, saída de 2035.
  - **Referência:** a missão de 2028, com o mesmo veículo.
- **Massas e propelente:** a massa no início de cada queima e o propelente dimensionado para ela vêm do dimensionamento
  atual (Isp de 321 s, P-015, margem de Δv da P-014). O Isp de cada combinação é usado só na queima. **O dimensionamento
  não foi refeito** com os motores; isso fica para depois do portão.
- **Conferências internas (testes, não verificação):**
  - com empuxo muito alto, a perda tende a zero (< 1 cm/s);
  - a perda cresce quando o empuxo cai;
  - o propelente segue a equação do foguete;
  - trocar os parâmetros numéricos (P-041) muda a perda em menos de 1e-4 relativo.

## 4. Resultados (`results/etapa3.1/queima_finita.md`)

**Captura em Marte** (m0 = 6.169 kg; propelente dimensionado para a captura: 2.336 kg)

| Combinação | Empuxo | Caso | Queima | Perda | Perda / P-015 | Propelente | Cabe? | Passa da queima única qualificada? |
| :- | -: | :- | -: | -: | -: | -: | :- | :- |
| C1: 2 × S400-15 | 850 N | projeto | 9.901 s | 444,5 m/s | 24,7× | 2.674 kg | **não** | **sim** (máx. 6.660 s) |
| C1 | | referência | 8.151 s | 329,7 m/s | 18,3× | 2.201 kg | sim | **sim** |
| C2: 8 × R-4D-11 | 3.914 N | projeto | 1.794 s | 76,4 m/s | 4,2× | 2.274 kg | sim | não |
| C2 | | referência | 1.461 s | 43,0 m/s | 2,4× | 1.851 kg | sim | não |
| C3: 1 × OMS-E | 26,7 kN | projeto | 252 s | 2,1 m/s | 0,1× | 2.178 kg | sim | não |
| C3 | | referência | 207 s | 1,1 m/s | 0,1× | 1.792 kg | sim | não |

**Saída de Marte** (m0 = 2.769 kg, partindo da órbita de 1 sol como no dimensionamento; propelente dimensionado: 1.065 kg)

| Combinação | Empuxo | Caso | Queima | Perda | Perda / P-015 | Propelente | Cabe? | Passa da queima única qualificada? |
| :- | -: | :- | -: | -: | -: | -: | :- | :- |
| R1: 1 × S400-15 | 425 N | projeto | 9.188 s | 492,5 m/s | 44,8× | 1.241 kg | **não** | **sim** |
| R1 | | referência | 5.233 s | 174,9 m/s | 15,9× | 707 kg | sim | não |
| R2: 2 × S400-15 | 850 N | projeto | 4.126 s | 242,2 m/s | 22,0× | 1.114 kg | **não** | não |
| R2 | | referência | 2.341 s | 63,2 m/s | 5,7× | 632 kg | sim | não |
| R3: 4 × R-4D-11 | 1.957 N | projeto | 1.637 s | 71,4 m/s | 6,5× | 1.037 kg | sim | não |
| R3 | | referência | 960 s | 14,1 m/s | 1,3× | 609 kg | sim | não |

**Cruzeiro do lander** (todas as correções da ida, 71,5 m/s): Z1, 4 × 10N, 6.602 s no total; Z2, 8 × 10N, 3.301 s.

**MAV** (m0 de 267,8 kg no estágio 1 e 70,5 kg no estágio 2)

| Estágio | Combinação | Empuxo | Isp | Queima | Empuxo/peso em Marte |
| :- | :- | -: | -: | -: | -: |
| 1 | M1: 2 × R-42 | 1.779 N | 305 s | 272 s | 1,79 |
| 1 | M2: 4 × R-4D-11 | 1.957 N | 315 s | 250 s | 1,97 |
| 1 | M3: 1 × R-40B (fora de produção) | 4.003 N | 296 s | 119 s | 4,03 |
| 2 | N1: 1 × S400-15 | 425 N | 321 s | 320 s | (acende em voo) |
| 2 | N2: 1 × R-4D-11 | 489 N | 315 s | 276 s | (acende em voo) |

## 5. Achados
1. **A P-015 subestima a perda com os motores de baixo empuxo.**
   - Com 2 × 400 N, o arranjo do ERO, a captura perde 445 m/s no caso de projeto, 25 vezes os 18 m/s da P-015. O
     propelente não cabe no estágio dimensionado, e a queima (9.901 s) passa da queima única qualificada do S400-15.
   - Na saída, 1 ou 2 × 400 N também não cabem no caso de projeto.
   - Com 8 × R-4D-11 (captura) e 4 × R-4D-11 (saída), as queimas cabem, mas consomem a maior parte da margem: 2.274 de
     2.336 kg e 1.037 de 1.065 kg.
   - Só o OMS-E fica abaixo da P-015.
2. **O Isp de 321 s do estágio de cruzeiro do lander não corresponde a um propulsor pequeno.** É o do motor de 400 N
   [F28]. Os propulsores de 10 N da mesma família dão 292 s, e o MSL usou hidrazina [F111]. O propelente do cruzeiro
   foi dimensionado com 321 s.
3. **O Isp de 343 s do MAV é o de um motor com turbobomba (Bowles et al. 2013).** Os motores pressurizados com voo do
   catálogo dão 296 a 321 s. O MAV atual foi dimensionado com 343 s.
4. **Empuxo/peso do MAV:** as três combinações do estágio 1 passam de 1 em Marte (1,79 a 4,03). O R-40B está fora de
   produção, e o R-42 não tem missão nomeada em fonte primária.
5. **Massa dos motores:** 8,6 kg (C1), 34,5 kg (C2) e 134,7 kg (C3). No dimensionamento atual, o inerte de cada
   estágio é a fração estrutural de 0,24, que não separa os motores.

## 6. Limitações
- **Modelo da queima:** plano, Marte pontual, sem J2 nem atmosfera, empuxo tangente à velocidade (não é o
  direcionamento ótimo), **uma única queima**.
  - Uma captura dividida em várias passagens pelo periapse, ou outro direcionamento, deve perder menos. **Não modelado.**
  - A direção da assíntota na saída não é imposta.
- **Sem verificação:** nenhum resultado foi comparado com um caso publicado de queima finita (Etapa 3.2).
- **Dimensionamento não refeito** com o Isp, a massa e as perdas de cada combinação.
- **Herança de voo:** quase sempre vem da lista do fabricante. O R-42 e o R-40B não têm missão nomeada. A variante do
  LEROS 4 que teria voado (4-ET) não foi conferida em fonte primária.
- **LEROS 1b:** usa hidrazina, não o MMH dos estágios.
- **Disponibilidade** dos motores em 2028: não conferida.

## 7. Premissas
- **Nova: P-041**, os parâmetros numéricos da queima finita (`config/queima_finita.yaml`), NÃO VALIDADA.
- As demais seguem como estavam. A P-015 continua no dimensionamento até a decisão do portão; só o Fabio altera status.

## 8. Portão: escolha dos motores (decisão do Fabio)

| Estágio | Opções calculadas | O que pesa |
| :- | :- | :- |
| Captura | C1 2 × S400-15; C2 8 × R-4D-11; C3 1 × OMS-E | C1 não cabe e passa da queima única; C2 cabe com 76 m/s de perda; C3 perde 2 m/s, mas pesa 135 kg e tem disponibilidade não conferida |
| Retorno | R1 1 × S400-15; R2 2 × S400-15; R3 4 × R-4D-11 | só R3 cabe no caso de projeto (71 m/s de perda) |
| Cruzeiro do lander | Z1 4 × 10N; Z2 8 × 10N | Isp de 292 s, contra 321 s no dimensionamento |
| MAV, estágio 1 | M1 2 × R-42; M2 4 × R-4D-11; M3 1 × R-40B | M3 fora de produção; Isp de 296 a 315 s, contra 343 s no dimensionamento |
| MAV, estágio 2 | N1 1 × S400-15; N2 1 × R-4D-11 | Isp de 315 a 321 s, contra 343 s |

Depois da escolha:
- refazer o dimensionamento com o Isp, a massa e a perda dos motores escolhidos, no lugar da P-015;
- decidir o Isp do cruzeiro e do MAV.

Isso muda as massas da Fase 2 e entra com errata, no mesmo PR que aplicar a decisão.
