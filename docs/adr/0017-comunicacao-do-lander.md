# ADR 0017 — Comunicação do lander: relé por orbitadores existentes, com reserva própria para o mínimo crítico

Status: Accepted (Fabio, 2026-10-31, portão da Etapa 4.3)
Data: 2026-10-31

## Contexto
A Etapa 4.3 (`docs/etapa4.3_comunicacao.md`, `results/etapa4.3/comunicacao.md`) comparou três saídas para a comunicação
do lander:
- (a) orbitadores de relé existentes;
- (b) enlace direto maior;
- (c) relé pelo nosso orbitador na órbita de encontro.

Com Friis, o relé pelo nosso orbitador cobre só de 1 % a 3 % da demanda total. O enlace direto do análogo do MSL cobre
1,6 % da demanda do lander.

## Decisão
1. **Requisito:** o MAV é lançado antes do início da conjunção solar (SEP ≤ 5°, 2030-05-06), com folga a definir na Etapa
   4.4.
2. **Primário: relé pelos orbitadores existentes.** O TGO é o principal. O MRO entra enquanto estiver disponível.
3. **Reserva própria:**
   - relé pelo nosso orbitador;
   - um enlace direto dimensionado para o mínimo crítico: estado, comandos de segurança e confirmação do lançamento
     do MAV (P-070).
4. **Premissas P-063 a P-069:** aprovadas, NÃO VALIDADAS. **P-070 a P-072:** novas, NÃO VALIDADAS.

## Números (`results/etapa4.3/comunicacao.md`, seção da decisão)
**Capacidade por caminho, contra a demanda:**

| Caminho | Capacidade | Helicópteros, só Navcam | Lander + helicópteros (só Navcam) |
| :- | -: | :- | :- |
| TGO | 60 a 2.000 Mbit/sol | depende | depende |
| MRO | 100 a 1.150 Mbit/sol | depende | não cobre |
| Reserva própria | 12 a 35 Mbit/sol | não cobre | não cobre; só o mínimo crítico |

- **TGO:** o limite superior é o da taxa máxima de 2.048 kbps, "over 1 Gbit during a 15-minute overflight" [F177]. O inferior
  vem da P-071. O TGO é compartilhado com outros usuários.
- **Demanda:**
  - lander: 250 Mbit por sol (P-063);
  - helicópteros, pela média do Ingenuity por câmera (P-072, sem compressão, com imagens em solo nas contagens):
    953 Mbit por sol só com a Navcam e 2.709 com a RTE;
  - a envoltória da P-068 dá 983 Mbit por sol;
  - **com a RTE, nenhum caminho cobre os helicópteros** (`results/etapa4.3/comunicacao.md`).
- **Enlace direto mínimo (P-070):**
  - HGA de 0,297 m e SSPA de 15 W, para os 160 bps do requisito de superfície do MSL na distância máxima;
  - comando de emergência a 7,8125 bps pela RLGA [F137];
  - massa de todos os itens do "Rover X-band" do MSL: 17,6 kg básica e 22,4 kg com margem;
  - 345 Wh por sol, com o receptor ligado o sol inteiro; a área de operação vai a 20,5 m², abaixo da linha de base de
    32,8 m².
- **Efeito no lander (sensibilidade; a P-017 não muda):**
  - lander injetado de 4.012 para 4.057 kg;
  - margens: Falcon Heavy com recuperação de +17 % para +15 %; Vulcan VC2 de +8 % para +7 %; as demais em
    `results/etapa4.3/comunicacao.md`.
  - **Proposta de encaminhamento:** incorporar o conjunto na lista de massas da Etapa 4.5.
- **Limitação:** se o receptor tiver de ficar ligado também na tempestade, ele soma à carga de sobrevivência, e isso não
  foi calculado.

## Riscos
- **Dependência de ativo externo.** O TGO é praticamente ponto único de falha.
  - Fonte: "health is nominal and appears consistent with operation well into the 2030s" [F183].
  - A extensão da ESA até a missão não foi conferida.
- **MRO:**
  - o TWTA de banda X está em fim de vida e é "a single-string failure point for the communication system" [F182];
  - isso ameaça o caminho de volta à Terra dos dados retransmitidos pelo MRO.
- **Reserva própria limitada:** com ela só passa o mínimo crítico. Sem o TGO e sem o MRO, a operação dos helicópteros fica
  muito reduzida.

## Oportunidade
- **Orbitador comercial de telecomunicações** da PL 119-21, com entrega "not later than December 31, 2028" [F185].
- É uma oportunidade, mas não conta na arquitetura.
