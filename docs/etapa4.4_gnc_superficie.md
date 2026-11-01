# Etapa 4.4: GNC e operação de superfície

Fase 4, subsistemas. Os números vêm de `results/etapa4.4/operacao_superficie.md` e `.yaml`, gerados por
`tools/operacao_superficie.py`. As entradas são:
- `config/operacao_superficie.yaml`;
- o catálogo de tempestades de `config/energia.yaml`;
- os caminhos de comunicação de `results/etapa4.3/comunicacao.yaml`;
- a missão de referência.

## 1. Pergunta (escopo consolidado pelo Fabio)
1. **Pouso:** a elipse com navegação relativa ao terreno, contra a distância até o depósito Three Forks e o alcance dos
   helicópteros.
2. **Chegada em Ls ~190°:** o efeito do início da estação de tempestades na entrada, descida e pouso.
3. **Linha do tempo mínima da superfície:** pouso, busca dos tubos, transferência tardia ao MAV e lançamento. Com ela:
   - a probabilidade de tempestade global até o lançamento;
   - a folga até a conjunção (06/05/2030), para fixar o requisito aprovado na 4.3.
4. **Dados dos helicópteros:** volume contra capacidade, e as opções (a) mais autonomia, (b) operação mais lenta e (c) mais
   comunicação.
5. **Navegação de cruzeiro e sensores de encontro.**

## 2. Pouso e alcance
- **Elipse e TRN:**
  - a elipse do Mars 2020 é de 7,7 × 6,6 km [F187];
  - a navegação relativa ao terreno (TRN) desvia o ponto de toque em até 600 m [F188];
  - o rover pousou a 5 m do alvo escolhido pelo TRN [F189];
  - a entrada guiada entregou o rover a 1,7 km do ponto esperado [F190].
- **O TRN acerta o alvo que escolhe, mas não leva o pouso a um ponto fixo do mapa a km de distância.** O lander do MSR
  previa pousar perto do depósito com pouso de precisão: "Pin Point Landing (PPL) accu-racy may be required" [F192]. O
  conceito do helicóptero de recuperação punha o lander a ~200 m do depósito (P-075, leitura da figura de [F191]).
- **Alcance dos helicópteros:**
  - SRH: cerca de 700 m por carga diária [F194];
  - Ingenuity: 300 m de projeto [F196] e 705 m no maior voo [F195].
- **Depósito:** 10 tubos, de 5 a 15 m entre si, com um tubo por vez por helicóptero [F193].
- **Três casos de distância do lander ao depósito**, para a linha do tempo:
  - 200 m, com pouso de precisão (P-075);
  - 1,7 km, o erro de entrega do Mars 2020 [F190];
  - 3,85 km, o semieixo maior da elipse [F187].

## 3. Chegada em Ls ~190°
- **Data e estação:** a chegada é em 2029-09-20, Ls 189,5°.
- **Tempestade na chegada:** dois inícios do catálogo (2001 e 2018) caem na estação antes da chegada. A probabilidade de
  haver uma tempestade global em curso na chegada é de 5 % (P-061), contra 25 % na estada inteira.
- **EDL na estação de tempestades:**
  - o InSight foi "the first Mars mission to land during the Mars dust storm season", com um modelo de atmosfera para
    poeira de fundo, tempestade regional, tempestade em declínio e tempestade global, em densidade e ventos [F199];
  - o efeito no EDL deste lander (densidade, ventos, paraquedas) **não foi quantificado aqui**;
  - o conceito do SRL planejava a superfície de Ls 40° a Ls 150°, fora da estação [F191].

## 4. Linha do tempo mínima da superfície (`results/etapa4.4/operacao_superficie.md`)
Fases:
- saída do lander: 6 sóis;
- mapeamento: 7 sóis [F191];
- busca de 10 tubos;
- transferência tardia e preparação do lançamento: 10 sóis (P-074).

Na busca, o ritmo do SRH é de 4 sóis por tubo por helicóptero [F191, F98], ganhando 1 sol por perna a cada 700 m (P-073).
No ritmo real do Ingenuity, o intervalo mediano entre voos é de 10 sóis [F195], com voos de até 300 m.

| Distância | Ritmo | Helicópteros em paralelo | Total (sóis) | Lançamento do MAV | Ls | Tempestade até o lançamento | Folga até a conjunção | Antes da conjunção? |
| -: | :- | -: | -: | :- | -: | -: | -: | :- |
| 200 m | SRH | 2 | 43 | 2029-11-03 | 215,8° | 10,0 % | 184 d | sim |
| 200 m | SRH | 1 | 63 | 2029-11-23 | 228,2° | 10,0 % | 164 d | sim |
| 200 m | Ingenuity | 2 | 123 | 2030-01-24 | 267,4° | 20,0 % | 102 d | sim |
| 200 m | Ingenuity | 1 | 223 | 2030-05-07 | 328,9° | 25,0 % | −1 d | **não** |
| 1,7 km | SRH | 2 | 63 | 2029-11-23 | 228,2° | 10,0 % | 164 d | sim |
| 1,7 km | SRH | 1 | 103 | 2030-01-03 | 254,1° | 15,0 % | 123 d | sim |
| 1,7 km | Ingenuity | 2 | 623 | 2031-06-22 | — | — | — | **não** (depois da partida) |
| 3,85 km | SRH | 2 | 93 | 2029-12-24 | 247,7° | 10,0 % | 133 d | sim |
| 3,85 km | SRH | 1 | 163 | 2030-03-06 | 292,8° | 20,0 % | 61 d | sim |
| 3,85 km | Ingenuity | 2 | 1.323 | 2033-06-10 | — | — | — | **não** (depois da partida) |

- **Tempestade:** pela distribuição de Ls do catálogo (P-061), a probabilidade de início de tempestade global até o
  lançamento vai de 10 % (lançamento em Ls 215° a 248°) a 20 %, contra 25 % na estada inteira.
- **Folga até a conjunção:**
  - no ritmo do SRH, todos os casos lançam antes da conjunção, com folga de 61 a 184 dias;
  - no ritmo do Ingenuity, só o caso de 200 m com dois helicópteros cabe, com 102 dias.
- **A estada termina em 2030-11-08** (partida do orbitador). Os casos lentos de 1,7 km e 3,85 km passam da partida e são
  inviáveis.

## 5. Dados dos helicópteros contra a capacidade dos caminhos
- **Capacidade (Mbit/sol, results/etapa4.3):** TGO de 60 a 2.000; MRO de 100 a 1.150; reserva própria de 12 a 35.
- **Lander:** 250 Mbit/sol (P-063).
- **Compressão:** a câmera colorida RTE usa JPEG de qualidade 85, com razão de 1,73 a 8,63 [F198] (P-076). A Navcam é sem
  perdas, com razão não publicada, e fica sem compressão.

| Ritmo (200 m, 2 helicópteros) | Volume por voo | Voos por sol | Helicópteros (Mbit/sol) | Com o lander (Mbit/sol) | Superfície (sóis) | Folga até a conjunção |
| :- | :- | -: | -: | -: | -: | -: |
| SRH | Navcam + RTE, sem compressão | 1,00 | 1.355 | 1.605 | 43 | 184 d |
| SRH | Navcam sem compressão + RTE em JPEG | 1,00 | 578 a 984 | 828 a 1.234 | 43 | 184 d |
| SRH | **(a)** só a RTE em JPEG; a Navcam fica a bordo | 1,00 | 102 a 508 | 352 a 758 | 43 | 184 d |
| **(b)** ritmo do Ingenuity | Navcam + RTE, sem compressão | 0,20 | 271 | 521 | 123 | 102 d |
| **(b)** ritmo do Ingenuity | Navcam sem compressão + RTE em JPEG | 0,20 | 116 a 197 | 366 a 447 | 123 | 102 d |
| **(b)** ritmo do Ingenuity | (a) + (b) | 0,20 | 20 a 102 | 270 a 352 | 123 | 102 d |

- **(a) Mais autonomia.** O que o Ingenuity já fazia sozinho:
  - voo por pontos de passagem, com navegação visual-inercial (IMU, altímetro, câmera) e sem desvio de perigos no pouso
    [F197];
  - mais tarde, ganhou a escolha autônoma do local de pouso [F186];
  - a Navcam rodava a 30 Hz para navegar, mas no máximo 200 imagens por voo eram guardadas para descer [F179].

  Se a Navcam ficar a bordo e descerem só as imagens RTE em JPEG, o volume cai para 102 a 508 Mbit/sol. Com o lander, isso
  fica dentro da faixa do TGO e do MRO.
  - Contra: a seleção e a autonomia além do que o Ingenuity voou não foram avaliadas.
- **(b) Operação mais lenta.** No ritmo do Ingenuity, os helicópteros fazem 0,20 voo por sol, e o volume cai na mesma
  proporção.
  - Com 200 m e dois helicópteros, a superfície dura 123 sóis e o MAV ainda lança antes da conjunção, com 102 dias de folga.
  - A tempestade sobe de 10 % para 20 %.
  - Com um helicóptero, ou com o lander mais longe, a operação lenta não cabe.
- **(c) Mais comunicação.** Um enlace direto para o caso mais pesado (1.605 Mbit/sol) pede:
  - uma HGA de 2,12 m com 100 W (P-069), cerca de 37,0 kg e 1.376 Wh por passe;
  - lander injetado de 4.012 para 4.087 kg;
  - Falcon Heavy com recuperação de +17 % para +14 %; Vulcan VC2 de +8 % para +6 % (sensibilidade).

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
  - a análise de navegação do encontro fica fora desta etapa.

## 7. Para decidir (Fabio)
1. **Folga do requisito do MAV antes da conjunção.** Os números estão na tabela da seção 4.
   - Com o ritmo do SRH, a folga vai de 61 a 184 dias.
   - Com o ritmo do Ingenuity, é de 102 dias no único caso que cabe.
   - Opção (i): fixar a folga no pior caso do ritmo do SRH que cabe (61 dias, a 3,85 km com um helicóptero).
   - Opção (ii): exigir pouso de precisão (200 m, P-075) e fixar a folga pelo ritmo do Ingenuity (102 dias).
   - Opção (iii): outro valor, que define até onde a operação pode atrasar.
2. **Dados dos helicópteros:** (a), (b), (c) ou uma combinação.
3. **Premissas novas** (NÃO VALIDADAS):
   - P-073: ritmo da busca;
   - P-074: transferência e preparação do lançamento;
   - P-075: 200 m do depósito;
   - P-076: compressão das imagens.
4. **Divergência a registrar:** a P-062 (aprovada na 4.2) fixou o depósito completo em 15/02/2023. A fonte [F99] dá o último
   tubo em 28/01/2023. A diferença muda o tempo no depósito em menos de um mês. Mudar o valor-base é decisão do Fabio.

## 8. Limitações
- **A linha do tempo é de conceito:** o ritmo do SRH é de um projeto não voado, e a transferência e a preparação do
  lançamento não têm fonte (P-074).
- **EDL:** o efeito da poeira no EDL não foi quantificado.
- **Volumes:** sem compressão da Navcam; a razão do JPEG da RTE vem de quatro rótulos.
- **Opção (c):** usa a escala da Etapa 4.3 (P-069), com o mesmo erro de apontamento do MSL.
- **Navegação de cruzeiro e encontro:** só análogos, sem análise própria.
