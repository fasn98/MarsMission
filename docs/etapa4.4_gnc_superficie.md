# Etapa 4.4: GNC e operação de superfície

Fase 4, subsistemas. Os números vêm de `results/etapa4.4/operacao_superficie.md` e `.yaml`, gerados por
`tools/operacao_superficie.py`. As entradas são:
- `config/operacao_superficie.yaml`;
- o catálogo de tempestades de `config/energia.yaml`;
- os caminhos de comunicação de `results/etapa4.3/comunicacao.yaml`;
- a energia de `results/etapa4.1/energia.yaml`;
- a missão de referência.

## 1. Pergunta (escopo consolidado pelo Fabio)
1. **Pouso:** a elipse com navegação relativa ao terreno, contra a distância até o depósito Three Forks e o alcance dos
   helicópteros.
2. **Chegada em Ls ~190°:** o efeito do início da estação de tempestades na entrada, descida e pouso.
3. **Linha do tempo mínima da superfície:** pouso, busca dos tubos, transferência tardia ao MAV e lançamento. Com ela:
   - a probabilidade de tempestade global até o lançamento;
   - a folga até a conjunção (06/05/2030), para fixar o requisito aprovado na 4.3.
4. **Dados dos helicópteros:** volume contra capacidade de cada caminho, e as opções (a) mais autonomia, (b) operação mais
   lenta e (c) mais comunicação.
5. **Navegação de cruzeiro e sensores de encontro.**

## 2. Pouso e alcance
- **Elipse e TRN:**
  - a elipse do Mars 2020 é de 7,7 × 6,6 km [F187];
  - a navegação relativa ao terreno (TRN) desvia o ponto de toque em até 600 m [F188];
  - o rover pousou a 5 m do alvo escolhido pelo TRN [F189];
  - a entrada guiada entregou o rover a 1,7 km do ponto esperado [F190].
- **O TRN acerta o alvo que escolhe, mas não leva o pouso a um ponto fixo a km de distância.** O lander do MSR previa pouso
  de precisão perto das amostras: "Pin Point Landing (PPL) accu-racy may be required" [F192]. O conceito do helicóptero de
  recuperação punha o lander a ~200 m do depósito (P-075, leitura da figura de [F191]).
- **Alcance dos helicópteros:**
  - SRH: cerca de 700 m por carga diária [F194];
  - Ingenuity: 300 m de projeto [F196] e 705 m no maior voo [F195].
- **Depósito:** 10 tubos, de 5 a 15 m entre si, com um tubo por vez por helicóptero [F193].
- **Três casos de distância do lander ao depósito:**
  - 200 m, com pouso de precisão (P-075);
  - 1,7 km, o erro de entrega do Mars 2020 [F190];
  - 3,85 km, o semieixo maior da elipse [F187].
- **Lacunas:**
  - a posição de Three Forks em relação a um ponto de pouso não foi achada em fonte primária;
  - o caso de 1,7 km não desconta o desvio de até 600 m do TRN em direção ao depósito; com ele, esse caso seria mais curto.

## 3. Chegada em Ls ~190°
- **Data e estação:** a chegada é em 2029-09-20, Ls 189,5°.
- **Tempestade na chegada:** dois inícios do catálogo (2001 e 2018, Ls 185°) caem na estação antes da chegada. A
  probabilidade de haver uma tempestade global em curso na chegada é de 5 % (P-061), contra 25 % na estada inteira.
- **EDL na estação de tempestades:**
  - o InSight foi "the first Mars mission to land during the Mars dust storm season". O EDL dele exigiu um modelo de
    atmosfera para quatro condições de poeira, até a tempestade global, em densidade e ventos [F199];
  - o efeito no EDL deste lander **não foi quantificado**;
  - o conceito do SRL planejava a superfície de Ls 40° a Ls 150°, fora da estação [F191].

## 4. Linha do tempo mínima da superfície (`results/etapa4.4/operacao_superficie.md`)
Fases:
- saída do lander: 6 sóis;
- mapeamento: 7 sóis [F191];
- busca de 10 tubos;
- transferência tardia e preparação do lançamento: 10 sóis (P-074).

Na busca, o ritmo do SRH é de 4 sóis por tubo por helicóptero [F191, F98], ganhando 1 sol por perna a cada 700 m (P-073).
No ritmo real do Ingenuity, o intervalo mediano entre voos é de 10 sóis [F195], com voos de até 300 m.

| Distância | Ritmo | Helicópteros em paralelo | Total (sóis) | Lançamento do MAV | Ls | Tempestade desde Ls 185° até o lançamento | Folga até a conjunção (dias) | Antes da conjunção? |
| -: | :- | -: | -: | :- | -: | -: | -: | :- |
| 200 m | SRH | 2 | 43 | 2029-11-03 | 215,8° | 10,0 % | 183,8 | sim |
| 200 m | SRH | 1 | 63 | 2029-11-23 | 228,2° | 10,0 % | 163,3 | sim |
| 200 m | Ingenuity | 2 | 123 | 2030-01-24 | 267,4° | 20,0 % | 101,6 | sim |
| 200 m | Ingenuity | 1 | 223 | 2030-05-07 | 328,9° | 25,0 % | −1,1 | **não** (dentro de ±1 dia) |
| 1,7 km | SRH | 2 | 63 | 2029-11-23 | 228,2° | 10,0 % | 163,3 | sim |
| 1,7 km | SRH | 1 | 103 | 2030-01-03 | 254,1° | 15,0 % | 122,2 | sim |
| 1,7 km | Ingenuity | 2 | 623 | 2031-06-22 | — | — | — | **não** (depois da partida) |
| 1,7 km | Ingenuity | 1 | 1.223 | 2033-02-27 | — | — | — | **não** (depois da partida) |
| 3,85 km | SRH | 2 | 93 | 2029-12-24 | 247,7° | 10,0 % | 132,4 | sim |
| 3,85 km | SRH | 1 | 163 | 2030-03-06 | 292,8° | 20,0 % | 60,5 | sim |
| 3,85 km | Ingenuity | 2 | 1.323 | 2033-06-10 | — | — | — | **não** (depois da partida) |
| 3,85 km | Ingenuity | 1 | 2.623 | 2037-02-05 | — | — | — | **não** (depois da partida) |

- **Tempestade:** a probabilidade conta os inícios do catálogo desde o começo da estação (Ls 185°). Entram nela os de antes
  da chegada, que estariam em curso. Com 10 inícios, cada um vale 2,5 % (P-061).
  - Nos casos que cabem, ela vai de 10,0 % (lançamento entre Ls 215,8° e 247,7°) a 20,0 %, contra 25 % na estada inteira.
- **Folga até a conjunção:**
  - no ritmo do SRH, todos os casos lançam antes da conjunção, com folga de 60,5 a 183,8 dias;
  - no ritmo do Ingenuity, só o caso de 200 m com dois helicópteros cabe, com 101,6 dias;
  - o caso de 200 m com um helicóptero perde a conjunção por 1,1 dia, dentro da resolução de ±1 dia.
- **A estada termina em 2030-11-08** (partida do orbitador). Os casos lentos de 1,7 km e 3,85 km passam da partida.

## 5. Dados dos helicópteros contra a capacidade de cada caminho
- **Capacidade (Mbit/sol, results/etapa4.3):**
  - TGO: de 60 a 2.000;
  - MRO: de 100 a 1.150;
  - reserva própria: de 12 a 35.
- **Lander:** 250 Mbit/sol (P-063).
- **Volume por voo:** vem da Etapa 4.3. Os voos por sol são os de cada ritmo; a 4.3 usava 2 voos por sol (P-054), e por isso
  dava 2.709 Mbit/sol com a RTE.
- **Compressão:** a RTE usa JPEG de qualidade 85, com razão de 1,73 a 8,63 [F198] (P-076). A Navcam é sem perdas, com razão
  não publicada, e fica sem compressão.
- **Cobertura:**
  - "sim" quando o mínimo do caminho cobre o máximo da demanda;
  - "depende" quando só a parte alta da faixa cobre;
  - "não" quando nem o máximo do caminho cobre o mínimo da demanda.

| Ritmo (200 m, 2 helicópteros) | Volume por voo | Voos por sol | Com o lander (Mbit/sol) | TGO | MRO | Reserva própria | Superfície (sóis) | Folga (dias) |
| :- | :- | -: | -: | :- | :- | :- | -: | -: |
| SRH | Navcam + RTE, sem compressão | 1,00 | 1.605 | depende | **não** | não | 43 | 183,8 |
| SRH | Navcam sem compressão + RTE em JPEG | 1,00 | 828 a 1.234 | depende | depende | não | 43 | 183,8 |
| SRH | **(a)** só a RTE em JPEG; a Navcam fica a bordo | 1,00 | 352 a 758 | depende | depende | não | 43 | 183,8 |
| **(b)** Ingenuity | Navcam + RTE, sem compressão | 0,20 | 521 | depende | depende | não | 123 | 101,6 |
| **(b)** Ingenuity | Navcam sem compressão + RTE em JPEG | 0,20 | 366 a 447 | depende | depende | não | 123 | 101,6 |
| **(b)** Ingenuity | (a) + (b) | 0,20 | 270 a 352 | depende | depende | não | 123 | 101,6 |

- **Nenhum caminho cobre com certeza nenhum caso.** O mínimo dos caminhos (TGO 60, MRO 100) não cobre nem o lander sozinho
  (250). A reserva própria nunca cobre.
- **O que muda com cada opção:** (a) e (b) põem a demanda dentro da faixa dos dois caminhos primários. No caso sem compressão
  e no ritmo do SRH, o MRO não cobre nem no máximo.

### Comparação lado a lado
| Opção | O que é | Prós | Contras |
| :- | :- | :- | :- |
| (a) mais autonomia | a Navcam fica a bordo, só a RTE em JPEG desce | a demanda cai para 352 a 758 Mbit/sol com o lander; sem massa nova | a seleção a bordo vai além do que o Ingenuity voou, que já fazia voo por pontos de passagem com navegação visual-inercial [F197], escolha autônoma de local de pouso [F186] e guardava até 200 imagens por voo [F179]; não avaliada |
| (b) operação mais lenta | o ritmo real do Ingenuity, 0,20 voo por sol | a demanda cai para 270 a 521 Mbit/sol; sem massa nova | só cabe com pouso a 200 m e dois helicópteros; a superfície vai a 123 sóis, a folga cai para 101,6 dias e a tempestade sobe de 10 % para 20 % |
| (c) mais comunicação | enlace direto para 1.605 Mbit/sol num passe de 8 h | não depende de orbitador externo | HGA de 2,12 m com 100 W (P-069), cerca de 37,0 kg e 1.376 Wh por passe; lander injetado de 4.012 para 4.087 kg; VC2 de +8 % para +6 % e Falcon Heavy com recuperação de +17 % para +14 % (sensibilidade); a área de operação vai a 24,5 m², ainda abaixo dos 32,8 m² da linha de base; não foi achado análogo de uma antena de 2 m apontada da superfície; para na conjunção |

TGO e MRO no máximo somam 3.150 Mbit/sol, sem avaliar a sobreposição dos passes.

## 6. Navegação de cruzeiro e sensores de encontro
- **Cruzeiro:**
  - o delta-DOR da DSN tem erro aleatório abaixo de 0,06 ns, cerca de 281 m no plano do céu a 1 UA [F200];
  - o MSL usou Doppler de ~0,1 mm/s, distância de ~1 m e ΔDOR de ~400 m na chegada [F201];
  - o ângulo de entrada final do MSL ficou a 0,013° do alvo de −15,5° [F201].
  - Tomados como análogo, sem análise de navegação própria.
- **Sensores de encontro:**
  - a câmera de ângulo estreito do ERO consome menos de 12 W imageando [F138];
  - o alcance e a precisão do lidar **não foram conferidos**, porque a página da ESA recusou o acesso;
  - a navegação do encontro fica fora desta etapa.

## 7. Para decidir (Fabio)
1. **Folga do requisito do MAV antes da conjunção** (tabela da seção 4):

   | Opção | Folga | Prós | Contras |
   | :- | -: | :- | :- |
   | (i) pior caso do ritmo do SRH que cabe | 60,5 dias (3,85 km, um helicóptero) | cobre o pouso em qualquer ponto da elipse com o ritmo do SRH | depende do ritmo de um conceito não voado |
   | (ii) pouso de precisão e ritmo do Ingenuity | 101,6 dias (200 m, dois helicópteros) | usa o ritmo que voou | exige pouso de precisão (P-075), sem análogo voado nesta distância |
   | (iii) outro valor | — | define até onde a operação pode atrasar | — |

2. **Dados dos helicópteros:** (a), (b), (c) ou uma combinação (seção 5).
3. **Premissas novas** (NÃO VALIDADAS):
   - P-073: ritmo da busca;
   - P-074: transferência e preparação do lançamento;
   - P-075: 200 m do depósito;
   - P-076: compressão das imagens.
4. **Divergência a registrar:** a P-062 (aprovada na 4.2) fixou o depósito completo em 15/02/2023. A fonte [F99] dá o último
   tubo em 28/01/2023, menos de um mês antes. Mudar o valor-base é decisão do Fabio.

## 8. Limitações
- **A linha do tempo é de conceito:** o ritmo do SRH é de um projeto não voado, e a transferência e a preparação do
  lançamento não têm fonte (P-074).
- **EDL:** o efeito da poeira no EDL não foi quantificado.
- **Volumes:** a Navcam fica sem compressão; a razão do JPEG da RTE vem de três valores de rótulos.
- **Opção (c):** usa a escala da Etapa 4.3 (P-069), com o mesmo erro de apontamento do MSL.
- **Navegação de cruzeiro e encontro:** só análogos, sem análise própria.

## Nota (2026-11-01): decisões do portão da Etapa 4.4 (ADR 0018)
Decisões do Fabio. **Números vigentes:** `results/etapa4.4/operacao_superficie.md`.
1. **Helicópteros:** operação adaptativa (a) + (b). A autonomia fica no nível do Ingenuity e o ritmo se ajusta à capacidade
   dos passes de relé. A opção (c) fica só como sensibilidade.
2. **Pouso de precisão:** vira requisito, e a P-075 passa a crítica.
   - A precisão prevista para o lander do MSR, na sequência nocional de EDL, era de menos de 20 m do alvo [F202].
   - O Perseverance pousou a 5 m do alvo escolhido pelo TRN [F189], mas a entrega guiada ficou a 1,7 km [F190].
   - Os 200 m só se sustentam com pouso de precisão da classe do lander do MSR, não voado.
3. **Folga do MAV antes da conjunção:** mínimo de 60 dias; o plano mira de 100 a 180 dias. A tabela da linha do tempo mostra
   agora, para cada caso, se a folga atende o mínimo e se fica no alvo.
4. **P-062:** 28/01/2023 [F99]. O tempo no depósito até a chegada continua em 6,6 anos.
5. **Premissas:** P-073 a P-076 aprovadas, NÃO VALIDADAS; a P-075 é crítica.
6. **Conclusão registrada:** o plano de superfície só fecha com ritmo rápido OU pouso de precisão, e o ritmo rápido depende de
   dados que os relés existentes não garantem.

## Nota (2026-11-01): grandezas de precisão e conclusão principal (ADR 0018)
- **Grandezas:**
  - os 60 m e 5 m do Mars 2020 [F189] medem o erro até um alvo escolhido a bordo, e não se comparam à P-075;
  - os 1,7 km [F190] (demonstrado, distância ao "expected touchdown location", com o desvio do TRN embutido) e os < 20 m do
    lander do MSR [F202] (previsto, "from target") se comparam à parcela de erro da P-075;
  - os 200 m são um afastamento planejado e **não ficam do lado conservador**.
- **Faixa sem mudança:** a linha do tempo não muda até 300 m no ritmo do Ingenuity e até 700 m no ritmo do SRH
  (`results/etapa4.4/operacao_superficie.md`).
- **Conclusão principal e risco principal da Fase 4:** o plano de superfície depende de uma capacidade não demonstrada em voo
  em qualquer combinação. Com a precisão de pouso já voada (~1,7 km), só fecha com o ritmo do SRH, não voado. Com o ritmo
  voado do Ingenuity, só fecha com pouso de precisão abaixo de ~300 m, previsto e não voado.


## Errata (portão da Etapa 4.5, 2026-11-01): P-017 no caso B e circuito de fluido no estágio de cruzeiro
No portão da Etapa 4.5, o Fabio adotou o caso B da lista de massas como valor-base da P-017 (ADR 0019). A plataforma de
superfície passa a somar os itens das Etapas 4.1 a 4.4, menos a energia do aquecimento do MAV já contada no item do MAV.
O circuito de fluido de rejeição de calor (P-077) vai no estágio de cruzeiro, descartado antes da entrada. Os resultados
das Fases 2 a 4 foram regenerados; os das etapas anteriores à 2.3 ficam como estavam. O texto acima fica como estava.

Os números vigentes desta etapa estão em `results/etapa4.4/operacao_superficie.md`.

**Números vigentes** (`results/etapa2.5/arquitetura.md`, `results/etapa4.5/lista_massas.md`):

| Item | Antes | Vigente |
| :- | -: | -: |
| Plataforma de superfície do lander (P-017) | 1.564,9 kg | **1.843,7 kg** |
| Circuito de fluido no estágio de cruzeiro | — | **35,7 kg** |
| Massa de entrada do lander | 3.882 kg | **4.429 kg** |
| Lander injetado | 4.012 kg | **4.615 kg** |
| Lander: Falcon Heavy com recuperação | +17 % | **+1 %** |
| Lander: Falcon Heavy descartável | +180 % | **+143 %** |
| Lander: Vulcan VC2 | +8 % | **−6 %** |
| Lander: Vulcan VC4 | +62 % | **+41 %** |
| Lander: Vulcan VC6 | +107 % | **+80 %** |
| Orbitador injetado; Falcon Heavy descartável; Vulcan VC6 | 7.796 kg; +44 %; +6 % | sem mudança |

Lançadores de base (ADR 0020): lander no Vulcan VC4, com o VC6 de reserva; orbitador no Falcon Heavy descartável.
