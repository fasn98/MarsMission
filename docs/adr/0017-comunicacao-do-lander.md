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
1. **Requisito:** o MAV é lançado antes do início da conjunção solar (SEP ≤ 5°, a partir de 2030-05-06). A folga fica
   para a Etapa 4.4.
2. **Primário: relé pelos orbitadores existentes.** O TGO é o principal. O MRO entra enquanto estiver disponível.
3. **Reserva própria:**
   - relé pelo nosso orbitador;
   - um enlace direto dimensionado para o mínimo crítico: estado, comandos de segurança e confirmação do lançamento
     do MAV (P-070).
4. **Premissas P-063 a P-069:** aprovadas, NÃO VALIDADAS. **P-070:** nova, NÃO VALIDADA.

## Números (`results/etapa4.3/comunicacao.md`, seção da decisão)
**Capacidade por caminho, contra a demanda:**

| Caminho | Capacidade | Lander + helicópteros (média do Ingenuity) |
| :- | -: | :- |
| TGO (limite inferior) | 2.000 Mbit/sol | cobre |
| MRO | 100 a 1.150 Mbit/sol | não cobre a soma; os helicópteros, depende |
| Reserva própria | 12 a 35 Mbit/sol | não cobre; só o mínimo crítico |

- **Lander:** 250 Mbit por sol.
- **Helicópteros:** 994 Mbit por sol, pela média de 202 imagens por voo do Ingenuity [F179, F186]. A envoltória da P-068
  dá 983 Mbit por sol.
- **Enlace direto mínimo:**
  - HGA de 0,297 m e SSPA de 15 W, para os 160 bps do requisito de superfície do MSL na distância máxima;
  - comando de emergência a 7,8125 bps pela RLGA [F137];
  - 16,0 kg com margem e 62,9 Wh por sol. A área de operação vai a 19,5 m², abaixo da linha de base de 32,8 m².
- **Efeito no lander (sensibilidade; a P-017 não muda):** o lander injetado vai de 4.012 para 4.044 kg. As margens caem
  de 1 a 2 pontos; o Vulcan VC2 vai de +8 % para +7 %. A lista de massas da Etapa 4.5 incorpora o conjunto.

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
