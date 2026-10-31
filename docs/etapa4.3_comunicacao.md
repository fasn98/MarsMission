# Etapa 4.3: comunicação

Fase 4, subsistemas. Os números vêm de `results/etapa4.3/comunicacao.md` e `.yaml`, gerados por `tools/comunicacao.py`.
As entradas são `config/comunicacao.yaml`, a efeméride DE440 (`config/kernels.yaml`) e a missão de referência
(`results/etapa1.3/missoes.yaml`).

## 1. Pergunta
- Enlaces com a DSN em banda X ao longo da missão (distância máxima Terra–Marte), volumes de dados, relé UHF
  lander–orbitador e atraso de comunicação.
- Conjunção solar: as datas em que Marte fica atrás do Sol durante a missão de referência e o impacto nas operações, em
  especial a busca dos tubos, a transferência, o lançamento do MAV e o encontro.

## 2. Conjunção solar na estada (`results/etapa4.3/comunicacao.md`)
O ângulo Sol–Terra–Marte (SEP) é calculado dia a dia pela efeméride (baricentro de Marte visto da Terra). O mínimo é de
**0,30° em 2030-05-25**, 247 dias depois da chegada, a 376,5 milhões de km. A estada vai de 2029-09-20 a 2030-11-08.

| Critério (fonte) | SEP abaixo de | Janela | Dias |
| :- | -: | :- | -: |
| Período de conjunção (MRO [F173]) | 5° | 2030-05-06 a 2030-06-13 | 39 |
| Sem depender de telemetria (MER [F174]) | 3° | 2030-05-14 a 2030-06-06 | 24 |
| Retorno BPSK padrão garantido (DSN 810-005 [F175]) | 2,3° | 2030-05-17 a 2030-06-03 | 18 |
| Sem comandos (MER [F174]); a banda X degrada (MRO [F173]) | 2° | 2030-05-18 a 2030-06-02 | 16 |

- A janela de 2° (16 dias) tem a ordem de grandeza da moratória de comandos de 2021, de 2 a 16 de outubro [F176].
- Depois da conjunção, a NASA reservou "about a week" para baixar os dados guardados [F176].
- O relé de proximidade (lander–orbitador) não é afetado diretamente pela conjunção [F173].
- Nos arcos de cruzeiro, o SEP mínimo é de 60,6° na ida e 44,2° na volta: não há conjunção fora da estada.

## 3. Impacto nas operações
| Trecho | Dias |
| :- | -: |
| Da chegada ao início do período de conjunção (SEP ≤ 5°) | 228 |
| Do fim do período de conjunção à partida, menos 7 dias de recuperação | 141 |
| Fases do encontro do ERO (captura em 22 dias + fase de RAAN em 24 dias [F121]) | 46 |

- **Superfície** (busca dos tubos, transferência, lançamento do MAV):
  - nenhum evento crítico deve cair dentro da janela, porque não há comando abaixo de 2° nem dependência de telemetria
    abaixo de 3°;
  - antes da conjunção há 228 dias, e a linha do tempo mínima da superfície é pendência da Etapa 4.4;
  - o lançamento do MAV pode ficar antes da conjunção ou depois dela.
- **Encontro:**
  - se o lançamento do MAV for depois da conjunção, as fases do encontro (46 dias) cabem antes da partida, com folga de
    95 dias;
  - se for antes, o encontro também pode ficar todo antes da conjunção, se a superfície terminar cedo.
- **A decisão de onde pôr o lançamento do MAV é do Fabio** (seção 6).

## 4. Distância e tempo de luz
- **Distância Terra–espaçonave máxima:** 380,7 milhões de km na estada, 246,8 na ida e 306,5 na volta. O máximo da missão é
  2,545 UA. O análogo (MRO) foi projetado para até 400 milhões de km [F173].
- **Tempo de luz (uma via):** até 21,2 min; o mínimo na estada é de 13,7 min.

## 5. Enlaces e volumes de dados
- **Orbitador em banda X** (análogo do MRO: HGA de 3 m e TWTA de 100 W [F173]; taxa escalada com 1/d², P-064):
  - 552 kbps na distância máxima da estada e 1.314 kbps na mínima;
  - 15.900 Mbit por passe de 8 h na distância máxima;
  - perto da Terra a escala superestima: a 100 milhões de km dá 8.000 kbps, contra os 3 a 4 Mbps publicados [F173];
  - os valores na estada ficam bem abaixo disso, mas são uma estimativa, não um orçamento de enlace.
- **Lander direto à Terra** (análogo do MSL: HGA de 0,28 m e 15 W [F137]):
  - 160 bps na distância máxima [F137], ou 4,6 Mbit num passe de 8 h;
  - isso é **1,8 % da demanda de 250 Mbit por sol** (P-063, o requisito do MSL [F137]);
  - o enlace direto não sustenta a operação de superfície e serve só como contingência e para comandos.
- **Relé UHF:**
  - o Electra chega a 2.048 kbps [F137];
  - o MSL, com orbitadores em órbita baixa, tinha de 100 a 1.150 Mbit por sol [F137];
  - a órbita de encontro do nosso orbitador vai de 300 a 25.952 km de altitude; no apoapse, a perda de espaço livre é
    38,7 dB maior que no periapse, só pela distância;
  - na prática, o relé pelo nosso orbitador só funciona perto do periapse.
  - O volume por sol depende da orientação da órbita e da visibilidade do sítio, e **não foi calculado**.
- **Volumes de dados do orbitador** (câmeras e sensores de encontro): não estimados. A capacidade de 15.900 Mbit por passe
  na distância máxima fica muito acima da demanda do lander.

## 6. Para decidir (Fabio)
1. **Onde fica o lançamento do MAV em relação à conjunção** (SEP ≤ 5° de 2030-05-06 a 2030-06-13):
   - (a) antes: a superfície tem até 228 dias desde a chegada;
   - (b) depois do fim da janela e dos 7 dias de recuperação, com o encontro em seguida e 95 dias de folga até a partida;
   - a escolha depende da linha do tempo mínima da superfície (Etapa 4.4).
2. **Relé do lander.** O enlace direto cobre só 1,8 % da demanda. Opções:
   - (a) nosso orbitador, só nos passes perto do periapse da órbita de encontro;
   - (b) orbitadores existentes (MRO, TGO), sem avaliar a disponibilidade deles em 2029–2030;
   - (c) uma fase do nosso orbitador em órbita mais baixa durante a superfície, sem avaliar o Δv;
   - nenhuma das três tem volume por sol calculado: isso exige a geometria dos passes (Etapa 4.4).
3. **Premissas novas** (NÃO VALIDADAS):
   - P-063: demanda do lander de 250 Mbit por sol (requisito do MSL);
   - P-064: taxa do orbitador escalada com 1/d² a partir do MRO.

## 7. Limitações
- Não há orçamento de enlace (link budget) próprio: as taxas vêm de análogos. Os parâmetros da DSN (ganho, temperatura de
  ruído, EIRP: 810-005, módulos 101 e 104) foram levantados e ficam para um orçamento detalhado.
- O SEP é o de Marte (baricentro), igual para o lander e para o orbitador na escala de graus.
- A moratória real depende do projeto. O critério de 2° e 3° é o do MER [F174]; a NASA não publica um limite único
  [F176].
