# Etapa 4.3: comunicação

Fase 4, subsistemas. Os números vêm de `results/etapa4.3/comunicacao.md` e `.yaml`, gerados por `tools/comunicacao.py`.
As entradas são `config/comunicacao.yaml`, a efeméride DE440 com o pck00011 (`config/kernels.yaml`) e a missão de
referência (`results/etapa1.3/missoes.yaml`).

## 1. Pergunta
- Enlaces com a DSN em banda X ao longo da missão (distância máxima Terra–Marte), volumes de dados, relé UHF
  lander–orbitador e atraso de comunicação.
- Conjunção solar: as datas em que Marte fica atrás do Sol durante a missão de referência e o impacto nas operações
  (busca dos tubos, transferência, lançamento do MAV e encontro).
- Pedido do Fabio para o portão:
  - registrar como requisito proposto o lançamento do MAV antes da conjunção;
  - comparar as saídas para a comunicação do lander;
  - dizer o volume de dados dos helicópteros.

## 2. Conjunção solar na estada (`results/etapa4.3/comunicacao.md`)
- **Como foi calculado:** o ângulo Sol–Terra–Marte (SEP) é calculado pela efeméride (baricentro de Marte visto da Terra),
  um ponto por dia à meia-noite TDB. As datas têm resolução de ±1 dia.
- **Mínimo:** 0,30° em 2030-05-25, 247 dias depois da chegada, a 376,5 milhões de km. Na amostragem diária o mínimo real
  fica um pouco abaixo disso.
- **Estada:** de 2029-09-20 a 2030-11-08.

| Critério (fonte) | SEP até | Janela | Dias |
| :- | -: | :- | -: |
| Período de conjunção (MRO [F173], "5 deg or less") | 5° | 2030-05-06 a 2030-06-13 | 39 |
| Sem depender de telemetria (MER [F174]) | 3° | 2030-05-14 a 2030-06-06 | 24 |
| Abaixo do ângulo em que a DSN 810-005 cobre o retorno BPSK padrão [F175] | 2,3° | 2030-05-17 a 2030-06-03 | 18 |
| Sem comandos (MER [F174]); a banda X degrada (MRO [F173]) | 2° | 2030-05-18 a 2030-06-02 | 16 |

- A janela de 2° tem a ordem de grandeza da moratória de 2021, de 2 a 16 de outubro.
- Depois da moratória de 2021, a NASA reservou "about a week" para baixar os dados [F176].
- O relé lander–orbitador não é afetado diretamente pela conjunção [F173].
- Nos arcos de cruzeiro o SEP mínimo é de 60,6° (ida) e 44,2° (volta).

## 3. Requisito proposto: lançamento do MAV antes da conjunção
**Requisito proposto (pedido do Fabio no portão da 4.3):** o MAV é lançado antes do início do período de conjunção
(SEP ≤ 5°, a partir de 2030-05-06), com folga.
- O tamanho da folga fica para a Etapa 4.4, junto com a mitigação da tempestade. Pela decisão do Fabio no 2º portão da
  4.1, o lander só precisa sobreviver até o lançamento do MAV.
- Da chegada ao início da janela há 228 dias.
- Se o lançamento for antes da conjunção, o encontro também pode ficar todo antes dela. As fases do encontro do ERO,
  da subida do MAV à selagem (T0 + 22 d) mais a fase de RAAN (T0 + 46 d) [F121], somam 46 dias.
- Se o encontro passar da conjunção, ele cabe depois da janela e dos 7 dias de recuperação, com 95 dias de folga até a
  partida.

## 4. Distância e tempo de luz
- **Distância Terra–espaçonave máxima:** 380,7 milhões de km na estada, 246,8 na ida e 306,5 na volta. O máximo da missão é
  2,545 UA. O análogo (MRO) foi projetado para até 400 milhões de km [F173].
- **Tempo de luz (uma via):** até 21,2 min; o mínimo na estada é de 13,7 min.

## 5. Volume de dados
- **Lander:** 250 Mbit por sol (P-063), que é o requisito do MSL [F137].
- **Helicópteros:** 983 Mbit por sol, que é uma envoltória (P-068).
  - Não há volume por voo publicado.
  - O Ingenuity guardava no máximo 200 imagens por voo [F179]. Pela Navcam de 640 × 480 e 8 bits [F179, F180], sem
    compressão, isso dá 492 Mbit por voo. Com 2 voos por sol (P-054), 983 Mbit por sol.
  - O enlace helicóptero–base, a 250 kbps [F180], leva 33 min por voo. O press kit diz "250 kilobytes per second" [F136],
    e essa divergência de unidade fica registrada.
- **Demanda total:** 1.233 Mbit por sol.

## 6. Comparação das saídas para a comunicação do lander
**Enlace direto atual** (análogo do MSL, 160 bps a 2,4 UA [F137], escalado com 1/d², P-064):
- 142 bps na distância máxima da estada;
- 4,1 Mbit num passe de 8 h (P-065);
- 1,6 % da demanda do lander, sem os helicópteros.

### (a) Orbitadores de relé existentes (estado em 2026-10-31)
| Orbitador | Estado | Fonte |
| :- | :- | :- |
| MAVEN | perdido; missão encerrada em 03/06/2026 | [F181] |
| MRO | operando; propelente para "well beyond another three years" (2025); TWTA de banda X perto do fim da vida e ponto único de falha; linha de orçamento até o FY2031 | [F182, F146] |
| Odyssey | propelente baixo; financiamento eliminado no pedido do FY2026; fora da tabela do FY2027 | [F182, F126] |
| TGO | saúde nominal "well into the 2030s"; extensão da ESA até 2030 não conferida; até 2.048 kbps, "over 1 Gbit during a 15-minute overflight"; pelo menos dois passes bons por sol | [F183, F177, F184] |
| Mars Express | financiado até o fim de 2026; extensão pedida até o fim de 2029; capacidade de relé não quantificada | [F183] |
| Orbitador comercial (PL 119-21) | US$ 700 milhões; entrega até 31/12/2028; contrato não conferido | [F185] |

- **Prós:** sem massa nem energia novas no nosso orbitador. O TGO retorna "over 1 Gbit during a 15-minute overflight"
  [F177], e a demanda total é de 1.233 Mbit por sol.
- **Contras:**
  - nenhuma fonte confirma relé até 2030–2031;
  - o MRO tem o TWTA em fim de vida;
  - o TGO depende de extensão da ESA;
  - o orbitador comercial ainda não existe.
- **É um risco de programa, não de engenharia.**

### (b) Enlace direto maior (P-069)
- **Taxa e antena:** para a demanda total num passe de 8 h, a taxa precisa ser de 42.814 bps, 301 vezes o MSL (24,8 dB).
  Isso pede uma HGA de 4,86 m com 15 W, ou de 1,86 m com o TWTA de 100 W do MRO.
- **Massa:** com 100 W, o conjunto (refletor, gimbal, TWTA e conversor) fica em cerca de 29,6 kg, contra 9,4 kg do MSL.
- **Energia:** 1.376 Wh por passe.
  - A área de operação vai a 24,5 m², ainda abaixo dos 32,8 m² da linha de base: a área continua dada pela sobrevivência.
  - A energia por sol e a bateria crescem.
- **Contras:**
  - uma antena de quase 2 m apontada da superfície (vento, poeira, gimbal) não tem análogo no estudo;
  - a escala supõe o mesmo erro de apontamento do MSL (5°). Uma HGA desse tamanho tem feixe mais estreito e pede
    apontamento melhor;
  - a massa e a potência do TWTA foram lidas da linha "X-band TWTAs (2)" da Tab. 2-1 do MRO [F173], e podem ser do par;
  - na conjunção, o enlace direto também para.

### (c) Relé pelo nosso orbitador na órbita de encontro (P-066, P-067)
A simulação considera:
- uma órbita kepleriana de 300 × 25.952 km com inclinação de 30° (sem J2);
- Marte girando à taxa do pck00011;
- o sítio em Jezero [F172];
- elevação mínima de 10° [F137];
- perda de espaço livre por Friis a 401,6 MHz [F137, F31];
- limiares do Electra [F178];
- 5 W, 0 dBi e 3 dB de margem;
- 60 sóis.

A fórmula de perda de percurso do [F177] (62 + 20·log10 R) fica uns 22,5 dB abaixo de Friis e não é usada.

| Caso | Passes por sol (com enlace) | Duração média | Mbit por passe com enlace (médio / máximo) | Mbit por sol | Cobertura da demanda total | Energia transmitindo |
| :- | -: | -: | -: | -: | -: | -: |
| Periapse na latitude do sítio | 1,52 (1,18) | 325 min | 29 / 115 | 34 | 3 % | 62 Wh/sol |
| Apoapse na latitude do sítio | 1,00 (0,92) | 582 min | 12 / 36 | 11 | 1 % | 68 Wh/sol |

- **Alcance do enlace:** com P-066 ele fecha a 1.024 kbps até 290 km e a 32 kbps até 1.840 km. Na órbita de encontro, o
  orbitador passa quase todo o tempo além disso.
  - Isso concorda com a descrição do MAVEN no apoapse: "slant ranges exceeding 8000 km ... much lower instantaneous data
    rates" [F178].
- **Comparação com dado publicado:** o mesmo modelo numa órbita circular de 250 km [F177] dá 99 Mbit por passe em média
  (máximo de 211) e 207 Mbit por sol. A faixa publicada do MRO com o MSL é de 30 a 600 Mbit por passe e de 100 a
  1.150 Mbit por sol [F137].
  - O resultado fica dentro da faixa.
  - O resultado baixo da opção (c) vem da órbita de encontro, e não de um modelo de enlace pessimista.
- **Prós:** independente de orbitadores de terceiros.
- **Contras:**
  - cobre 1 % a 3 % da demanda total, ou de 4 % a 14 % só da demanda do lander;
  - sem J2, o periapse migra ao longo da simulação, e os dois casos são extremos, não médias;
  - a orientação da órbita não está definida (P-067).
- **Variante não avaliada:** usar como relé uma órbita mais baixa durante a superfície exigiria Δv do orbitador.

## 7. Para decidir (Fabio)
1. **Requisito proposto:** lançamento do MAV antes do início do período de conjunção (2030-05-06), com folga a definir na
   Etapa 4.4.
2. **Comunicação do lander:**
   - (a) orbitadores existentes;
   - (b) enlace direto maior;
   - (c) relé pelo nosso orbitador;
   - ou uma combinação delas.
3. **Premissas novas** (NÃO VALIDADAS):
   - P-063: demanda do lander;
   - P-064: escala 1/d²;
   - P-065: passe direto de 8 h;
   - P-066: enlace UHF;
   - P-067: geometria dos passes;
   - P-068: volume dos helicópteros;
   - P-069: escala do enlace direto maior.

## 8. Limitações
- **Taxas por análogo:** não há orçamento de enlace próprio em banda X; as taxas do orbitador e do lander vêm de
  análogos escalados com 1/d². Os parâmetros da DSN (ganho, temperatura de ruído e EIRP, nos módulos 101 e 104 da
  810-005) foram levantados e ficam para um orçamento detalhado.
- **Banda X no cruzeiro:** a taxa nos arcos de cruzeiro não foi calculada; só a distância e o tempo de luz.
- **Volume do orbitador:** o volume de dados do orbitador (câmeras e sensores de encontro) não foi estimado. Em banda X,
  ele tem 15.900 Mbit por passe de 8 h na distância máxima.
- **Moratória:** a moratória real depende do projeto. O critério de 2° e 3° é o do MER [F174], e a NASA não publica um
  limite único [F176].
- **Helicópteros:** o volume é uma envoltória sem compressão (P-068).
