# Etapa 3.3: orbitador químico × elétrico × híbrido

Fase 3, propulsão. Números de `results/etapa3.3/orbitador_eletrico.md` e `geometria_planos.md`, gerados por
`tools/orbitador_eletrico.py` e `tools/geometria_marte.py` a partir de `config/eletrica.yaml`, do dimensionamento
atual e dos modelos de baixo empuxo da Etapa 3.2 (ADR 0012).

## 1. Pergunta
O orbitador elétrico permite o encontro em órbita baixa (ADR 0005, item 1) e reduz a massa total?
- **Opções** (prompt da Fase 3):
  - (a) químico atual;
  - (b) elétrico, no cruzeiro e na espiral;
  - (c) híbrido: captura química e espiral elétrica até a órbita baixa. É a prioridade do ADR 0012.
- **Restrição de tempo:** a descida, o encontro e a subida cabem na estada em Marte. São 414 dias na missão de
  referência; nas outras janelas do envelope, 480 a 550.

## 2. Mudança de plano (ADR 0012, item 2)
`results/etapa3.3/geometria_planos.md` compara a declinação das assíntotas de chegada e de partida (equador de Marte,
pck00011.tpc) com a inclinação de 27,3° da órbita de encontro:
- Só a chegada de 2028 passa, e por 0,05° (−27,35°). Custear esse excesso no apoapse da órbita de 1 sol custa 0,40 m/s.
- **As espirais podem ser coplanares.** A fórmula de Edelbaum com mudança de plano não é necessária.
- Não tratado: a orientação do nodo na partida (precessão durante a estada).

## 3. Catálogo de propulsores elétricos (`config/eletrica.yaml`)
Entram no dimensionamento só os propulsores com voo e com empuxo, Isp, potência, massa do propulsor e massa da PPU em
fonte primária:

| Propulsor | Empuxo | Isp | Potência | Propulsor | PPU | Vida | Voo |
| :- | -: | -: | -: | -: | -: | :- | :- |
| NSTAR | 93 mN | 3160 s | 2,3 kW | < 8,2 kg | 13,7 kg | 235 kg de Xe no teste de vida em solo [F117] | Deep Space 1 [F122] |
| XIPS-25 | 165 mN | 3550 s | 4,5 kW (na fonte) | 13,7 kg | 21,3 kg | não encontrada | "more than 152 … in orbit" [F119] |

As fontes são F116, F117 e F119; os detalhes estão no config.

**Pesquisados e fora do dimensionamento:**
- **Sem massa do propulsor em fonte primária:** NEXT-C (DART), SPT-140 (Psyche), BPT-4000/XR-5, T6 (BepiColombo) e
  PPS-1350-G (SMART-1). A massa da PPU, quando há, vem de uma compilação.
- **PPS-5000:** voo não confirmado em fonte primária.
- **RIT-2X:** é o propulsor do ERO do MSR [F32, p. 5 do PDF], sem voo encontrado.

**Demais itens do sistema elétrico:**
- **Tanque:** S-XTA-60, voado, com 11,7 kg secos para 110 kg de xenônio [F120].
- **Resíduo:** 2,4 % [F118].
- **Alimentação:** 11,4 kg por propulsor, do NSTAR [F118]. No XIPS-25 o mesmo valor entra como premissa (P-047).
- **Painel:** 80 W/kg a 1 UA [F55], com o fator de perdas e no afélio, como na plataforma.
- **Tempo de encontro:** 22 dias, da detecção à captura, da arquitetura química do ERO de 2018 [F121].

## 4. Achado de física: a espiral tangencial não desce de uma órbita elíptica
- A espiral verificada (tangencial) parte de órbita circular.
- Partindo da elipse de captura de 1 sol, o empuxo tangencial contra a velocidade aumenta a excentricidade, e o
  periapse cai abaixo da superfície (visto na sessão; não gravado em `results/`).
- Daí as duas concepções do híbrido:
  - **(c2):** captura química direto numa órbita circular, depois espiral tangencial (verificada) até a circular de
    encontro, e o inverso na volta;
  - **(c1):** captura química na elipse de 1 sol, depois empuxo só em arcos de ±30° em torno do periapse, que baixam o
    apoapse quase sem mexer no periapse. Fora dos arcos o voo é livre (`orbital.baixo_empuxo.apoapse_por_arcos`, mesmo
    integrador).

## 5. Resultados (`results/etapa3.3/orbitador_eletrico.md`)
**(a) Químico atual:**
- orbitador de 7.205 kg e lander de 3.996 kg;
- MAV + aquecimento de 403 kg (Δv de subida de 5,240 km/s sem margem);
- total (iii) de 34.003 kg;
- órbita de encontro de 300 × 24.992 km.

**(c2) Captura em órbita circular.** Viável no tempo, mas a massa explode. Capturar numa órbita circular custa muito
mais Δv químico do que capturar na elipse de 1 sol, e o mesmo vale na saída. A varredura acaba escolhendo captura logo
acima do encontro, o que deixa à espiral quase nada.

| Propulsor | Ativos | Encontro | Captura | Orbitador | Total (iii) | Tempo em Marte |
| :- | -: | -: | -: | -: | -: | -: |
| NSTAR | 1 | 1.092 km | 1.460 km | 45.392 kg | 148.769 kg | 363 d |
| NSTAR | 12 | 1.216 km | 1.939 km | 107.211 kg | 336.467 kg | 140 d |
| XIPS-25 | 1 | 1.092 km | 1.764 km | 50.353 kg | 163.829 kg | 391 d |
| XIPS-25 | 12 | 1.092 km | 2.131 km | 164.043 kg | 508.944 kg | 168 d |

- O MAV cai para 216 kg, contra 403 kg no químico.
- Mesmo assim, o total fica 4 a 15 vezes acima do químico, e nenhum lançador leva o orbitador (margens de −61 a −91 %).
- A espiral quase circular confere com a numérica no ponto escolhido (diferença de ~1e-9).

**(c1) Captura na elipse de 1 sol e descida em arcos.** Só a descida já não cabe na estada. A conta usa a massa do
orbitador químico depois da captura (3.271 kg), que é menor que a do híbrido, porque este ainda leva o sistema
elétrico; não considera eclipse.

| Propulsor | Ativos (potência) | Δv | Tempo de empuxo | Tempo decorrido |
| :- | -: | -: | -: | -: |
| NSTAR | 1 (2,3 kW) | 1,205 km/s | 481 d | 10.964 d |
| NSTAR | 12 (27,6 kW) | 1,205 km/s | 40 d | 913 d |
| XIPS-25 | 4 (18 kW) | 1,205 km/s | 68 d | 1.546 d |
| XIPS-25 | 12 (54 kW) | 1,205 km/s | 23 d | 515 d |

- Quase todo o tempo é voo livre perto do apoapse.
- Arcos mais longos derrubam o periapse (visto na sessão; não gravado em `results/`).
- Outra lei de empuxo que mantenha o periapse seria uma lei de guiagem nova, não verificada.

**(b) Elétrico, trecho heliocêntrico (calculado, NÃO verificado).** Δv quase circular da órbita da Terra à de Marte:
5,655 km/s. Com a massa do orbitador químico (7.205 kg), só o empuxo da ida leva:
- de 4.635 d (1 NSTAR) a 386 d (12 NSTAR);
- de 2.635 d (1 XIPS-25) a 220 d (12 XIPS-25).

As viagens da missão de referência levam 300 d na ida e 319 d na volta.

**Comparação com o ERO** [F123, p. 3]: o ERO desce em "less than 1 year", fica 1 a 1,5 ano em órbita baixa e sobe em
"less than 1 year", com 5 RIT-2X e um painel de 144 m² [F32]. A missão de referência deste estudo fica 414 dias em Marte.

## 6. Conclusão para o portão
Com a missão de referência atual (classe conjunção, 414 dias em Marte), nenhuma opção elétrica cabe:
- **(c1):** não cabe no tempo, nem com 54 kW;
- **(c2):** não cabe em massa;
- **(b):** não cabe nos tempos de viagem.

Encontro em órbita baixa com orbitador elétrico, como no ERO, exige uma estada de anos em Marte. Isso muda a
missão de referência (ADR 0003).

## 7. Para decidir no portão (Fabio)
1. **Propulsão do orbitador:**
   - **(A)** Manter o químico (a) e registrar que o elétrico não cabe na missão de referência.
   - **(B)** Abrir o estudo de uma missão de estada longa, como a do ERO (nova missão de referência, ADR 0003), para
     reavaliar (c1). Exige a lei de guiagem da descida em arcos, ou outra, e a sua verificação.
   - **(C)** Estudar (c1) com potência maior, além de 54 kW, ainda na missão atual. É provavelmente inviável, pela
     escala dos números acima.
2. **Catálogo:** aceitar só NSTAR e XIPS-25, ou buscar as massas que faltam (NEXT-C, SPT-140, XR-5, T6).
3. **Premissas novas** (NÃO VALIDADAS):
   - **P-047:** operação do sistema elétrico (reserva, eclipse, alimentação do XIPS-25);
   - **P-048:** perdas químicas do híbrido iguais às da 3.1;
   - **P-049:** faixas da varredura e parâmetros do c1.
4. **ADR da propulsão nuclear térmica:** pendente, PR à parte.

## 8. Limitações
- **Concepções testadas:** o híbrido foi avaliado só em duas concepções (c2 e c1 com arcos de ±30°). Leis de guiagem
  ótimas para baixar o apoapse não foram implementadas.
- **(c1):** usa a massa do orbitador químico, sem o sistema elétrico, e não considera eclipse. O tempo real seria maior.
- **(b):** é só a ordem de grandeza do tempo de empuxo heliocêntrico, sem o dimensionamento completo.
- **Perdas químicas do híbrido:** são as da Etapa 3.1 (P-048), que subestimam as perdas nas capturas em órbita
  circular.
- **Órbita do nodo:** a orientação do nodo na partida não foi tratada.
