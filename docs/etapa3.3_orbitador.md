# Etapa 3.3: orbitador químico × elétrico × híbrido

Fase 3, propulsão. Números de `results/etapa3.3/orbitador_eletrico.md` e `geometria_planos.md`, gerados por
`tools/orbitador_eletrico.py` e `tools/geometria_marte.py` a partir de `config/eletrica.yaml`, do dimensionamento
atual e dos modelos de baixo empuxo da Etapa 3.2 (ADR 0012).

## 1. Pergunta
O orbitador elétrico permite o encontro em órbita baixa (ADR 0005, item 1) e reduz a massa total?

As opções (prompt da Fase 3) são:
- (a) químico atual;
- (b) elétrico, no cruzeiro e na espiral;
- (c) híbrido: captura química e espiral elétrica até a órbita baixa. É a prioridade do ADR 0012.

Restrição de tempo: descida, encontro e subida cabem na estada em Marte. São 414 dias na missão de referência e de
480 a 550 nas outras janelas do envelope.

## 2. Mudança de plano (ADR 0012, item 2)
`results/etapa3.3/geometria_planos.md` compara a declinação das assíntotas de chegada e de partida (equador de Marte,
pck00011.tpc [F17]) com a inclinação de 27,3° da órbita de encontro.
- Só a chegada de 2028 passa do limite, e por 0,05° (−27,35°). Custear esse excesso no apoapse da órbita de 1 sol custa
  0,40 m/s.
- **As espirais podem ser coplanares.** A fórmula de Edelbaum com mudança de plano não é necessária.
- Não tratado: a orientação do nodo na partida (precessão durante a estada).

## 3. Catálogo de propulsores elétricos (`config/eletrica.yaml`)
Entram no dimensionamento só os propulsores com voo e com empuxo, Isp, potência, massa do propulsor e massa da PPU em
fonte primária.

| Propulsor | Empuxo | Isp | Potência do painel (entrada da PPU) | Propulsor | PPU | Throughput | Voo |
| :- | -: | -: | -: | -: | -: | :- | :- |
| NSTAR | 93 mN | 3160 s | 2,56 kW (2,3 kW de saída / 0,90) [F116] | < 8,2 kg | 13,7 kg | 135 kg [F118] | Deep Space 1 [F122] |
| XIPS-25 | 165 mN | 3550 s | 4,5 kW [F119] | 13,7 kg | 21,3 kg | não encontrado | "more than 152 … in orbit" [F119] |

**Fora do dimensionamento:**
- NEXT-C (DART), SPT-140 (Psyche), BPT-4000/XR-5, T6 (BepiColombo) e PPS-1350-G (SMART-1): sem massa do propulsor em
  fonte primária.
- PPS-5000: voo não confirmado.
- RIT-2X, o propulsor do ERO do MSR [F32]: sem voo encontrado.

**Demais itens do sistema elétrico:**
- **Vida do NSTAR:** o teste de vida em solo processou 235 kg [F117], mas o config usa os 135 kg da tabela da NASA
  [F118].
- **Tanque:** massa seca do S-XTA-60 voado (11,7 kg), com a capacidade de xenônio do membro de 60 l da mesma família
  (110 kg), que está em desenvolvimento [F120].
- **Resíduo:** 2,4 % [F118].
- **Alimentação:** 11,4 kg por propulsor, do NSTAR [F118]. No XIPS-25 o mesmo valor é premissa (P-047).
- **Painel:** 80 W/kg a 1 UA [F55], com o fator de perdas e no afélio, como na plataforma.
- **Margens de crescimento:** propulsão de fluidos para o propulsor e a alimentação; eletrônica, pela massa, para a PPU;
  painel solar para o painel. O tanque não leva margem, como o ε dos estágios.
- **Tempo de encontro:** 22 dias, da detecção à captura, da arquitetura química do ERO de 2018 [F121].

## 4. Achado de física: a espiral tangencial não desce de uma órbita elíptica
**A espiral verificada parte de órbita circular.** Partindo da elipse de 300 × 33.793 km, empuxo tangencial contra a
velocidade o tempo todo, com 1 N, não chega à circular do encontro. O periapse cai abaixo da superfície (até −170 km)
em 2 dias (`results/etapa3.3/orbitador_eletrico.md`, "Demonstração").

Daí as duas concepções do híbrido:
- **(c2):** captura química direto numa órbita circular; espiral tangencial verificada até a circular de encontro; o
  inverso na volta.
- **(c1):** captura química numa elipse com o apoapse da órbita de 1 sol e o periapse no encontro (300 × 33.793 km).
  Empuxo só em arcos de ±30° em torno do periapse e voo livre no resto, para baixar o apoapse
  (`orbital.baixo_empuxo.apoapse_por_arcos`, mesmo integrador).

## 5. Resultados (`results/etapa3.3/orbitador_eletrico.md`)
**(a) Químico atual:**
- orbitador de 7.205 kg;
- lander de 3.996 kg;
- MAV + aquecimento de 403 kg (Δv de subida de 5,240 km/s, sem margem);
- total (iii) de 34.003 kg;
- órbita de encontro de 300 × 24.992 km.

**(c2) Captura em órbita circular: cabe no tempo, mas não cabe em massa.**

| Propulsor | Ativos | Encontro | Captura | Δv captura / saída químicas | Descida / subida | Orbitador | Total (iii) | Menor folga |
| :- | -: | -: | -: | -: | -: | -: | -: | -: |
| NSTAR | 1 | 1.092 km | 1.460 km | 2,816 / 2,839 km/s | 195 / 184 d | 45.878 kg | 150.244 kg | 13 d |
| NSTAR | 12 | 1.216 km | 1.939 km | 2,804 / 2,829 km/s | 71 / 66 d | 112.994 kg | 354.021 kg | 255 d |
| XIPS-25 | 1 | 1.092 km | 1.605 km | 2,812 / 2,836 km/s | 164 / 155 d | 50.357 kg | 163.840 kg | 73 d |
| XIPS-25 | 12 | 1.092 km | 2.131 km | 2,801 / 2,826 km/s | 82 / 77 d | 163.585 kg | 507.555 kg | 232 d |

- **Por que a massa explode:** a captura e a saída químicas partem de órbita circular (cerca de 2,8 km/s cada, com a
  margem), e não de uma elipse.
- **Lado do lander:** o MAV cai para 216 a 223 kg, contra 403 kg no químico.
- **Saldo:** o total fica 4 a 15 vezes o do químico.
- **Lançadores:** nenhum leva o orbitador; as margens vão de −61 a −91 %.
- **Conferência:** a espiral quase circular confere com a numérica no ponto escolhido (diferença de ~1e-9 relativo).

**(c1) Elipse e descida em arcos: não cabe no tempo.** A tabela é só a descida. A conta usa a massa do orbitador químico
depois da captura (3.271 kg), menor que a do híbrido, que ainda leva o sistema elétrico, e não considera eclipse.

| Propulsor | Ativos (potência) | Δv | Tempo de empuxo | Tempo decorrido | Periapse final |
| :- | -: | -: | -: | -: | -: |
| NSTAR | 1 (2,6 kW) | 1,205 km/s | 481 d | 10.964 d | 223 km |
| NSTAR | 12 (30,7 kW) | 1,205 km/s | 40 d | 913 d | 223 km |
| XIPS-25 | 4 (18 kW) | 1,205 km/s | 68 d | 1.546 d | 223 km |
| XIPS-25 | 12 (54 kW) | 1,205 km/s | 23 d | 515 d | 223 km |

- Quase todo o tempo é voo livre perto do apoapse.
- O periapse cai de 300 para 223 km, abaixo dos 300 km pedidos para o contêiner [F32]. Seria preciso corrigi-lo.

**(b) Elétrico, trecho heliocêntrico (calculado, NÃO verificado).**
- Δv quase circular da órbita da Terra à de Marte: 5,655 km/s.
- Com a massa do orbitador químico (7.205 kg), só o empuxo da ida leva:
  - de 4.635 d (1 NSTAR) a 386 d (12 NSTAR);
  - de 2.638 d (1 XIPS-25) a 220 d (12 XIPS-25, 54 kW).
- As viagens da missão de referência levam 300 d na ida e 319 d na volta.
- **Com 12 XIPS-25, o empuxo da ida (220 d) cabe nos 300 d da viagem.**
- **Não foi feito para (b):** a trajetória elétrica, as espirais em Marte e na Terra, o dimensionamento, a varredura, o
  MAV e as margens. Só há esta ordem de grandeza, e ela não decide a opção.

**Referência do ERO** [F123, p. 3]:
- desce em "less than 1 year", fica 1 a 1,5 ano em órbita baixa e sobe em "less than 1 year";
- usa 5 RIT-2X e um painel de 144 m² [F32].

## 6. Leitura para o portão
Com a missão de referência atual (classe conjunção, 414 dias em Marte) e as concepções avaliadas:
- **(c2):** cabe no tempo, mas não cabe em massa;
- **(c1):** não cabe no tempo, nem com 54 kW, e o periapse desce abaixo do mínimo;
- **(b):** não foi dimensionado. Com cerca de 54 kW, o empuxo da ida cabe na viagem, mas falta o resto.

Nenhuma opção elétrica avaliada fecha massa e tempo ao mesmo tempo nesta missão.

## 7. Para decidir no portão (Fabio)

| Opção | O que significa | Prós | Contras | Base |
| :- | :- | :- | :- | :- |
| **A. Manter o químico (a)** | Fecha a Fase 3 com o orbitador químico; o elétrico fica registrado como não aplicável à missão de referência | Total de 34.003 kg e lançadores que já servem; sem dependência de propulsão elétrica | Encontro continua na elipse de 300 × 24.992 km, e o MAV continua com Δv de 5,24 km/s (risco do ADR 0007) | §5, (a) e (c2) |
| **B. Estudar uma missão de estada longa** | Nova missão de referência (ADR 0003) com estada de anos, como o ERO | Abre espaço para a descida em arcos (c1) e para o encontro em órbita baixa, como no MSR | Muda a missão de referência; exige uma lei de guiagem da descida (a de ±30° baixa o periapse) e a sua verificação; a etapa fica maior | §5 (c1); ERO [F123] |
| **C. Dimensionar (b) por inteiro** | Trajetória heliocêntrica elétrica, espirais em Marte e na Terra, massas e margens | Única opção ainda sem número completo; a ida cabe com cerca de 54 kW | Trecho heliocêntrico "calculado, não verificado" (ADR 0012); espirais a partir de v∞ ≈ 0 e cronograma novo | §5 (b) |

Outros pontos:
1. **Catálogo:** aceitar só NSTAR e XIPS-25, ou buscar as massas que faltam (NEXT-C, SPT-140, XR-5, T6).
2. **Premissas novas** (NÃO VALIDADAS):
   - **P-047:** operação do sistema elétrico (reserva, eclipse, alimentação do XIPS-25);
   - **P-048:** perdas químicas do híbrido iguais às da 3.1;
   - **P-049:** faixas, parâmetros do c1 e da ordem de grandeza da (b), demonstração, convergência e arredondamentos.
3. **ADR da propulsão nuclear térmica:** pendente, em PR à parte.

## 8. Limitações
- **Concepções testadas:** o híbrido foi avaliado só em duas concepções (c2, e c1 com arcos de ±30°). Leis de guiagem
  ótimas para baixar o apoapse não foram implementadas.
- **(c1):** usa a massa do orbitador químico, sem o sistema elétrico, e não considera eclipse. O tempo real seria maior.
- **(b):** é só a ordem de grandeza do tempo de empuxo heliocêntrico, sem dimensionamento.
- **Perdas químicas do híbrido:** são as da Etapa 3.1 (P-048), que subestimam as perdas de capturas em órbita circular.
- **Tempo de encontro e nodo:**
  - O tempo de encontro (22 d) não inclui a fase de RAAN de 24 d da mesma tabela [F121].
  - A orientação do nodo na partida não foi tratada.
  - Com os 24 d, o c2 com 1 NSTAR (folga de 13 d) deixa de caber.
- **Tempo da espiral com margem:** usa o Δv com a margem (como o xenônio), com a mesma fração média de eclipse da
  espiral sem margem.
