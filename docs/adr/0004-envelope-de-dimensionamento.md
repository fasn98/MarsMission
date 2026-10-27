# ADR 0004 — Envelope de Δv e regra de dimensionamento por estágio

Status: Accepted (Fabio, 2026-10-27; regra do Δv no 2º portão da Etapa 1.3; regra de estagiamento
no portão da Parte B da Etapa 1.4)
Data: 2026-10-27

## Contexto
O veículo deve servir em qualquer janela de ida de 2028 a 2035, não só na missão de referência
(ADR 0003). A forma de cobrir as janelas depende do estagiamento.

## Decisão
1. **Mínimo admissível por janela** (Etapa 1.3): para cada janela de ida 2028–2035, a missão de
   menor Δv propulsivo sob as restrições da missão robótica:
   - reentrada ≤ 12,9 km/s (P-011);
   - órbita de 1 sol e captura propulsiva (ADR 0003);
   - sem limite de trânsito.

   A classe "trânsitos ≤ 210 d" fica de fora porque é restrição de tripulação do DRA 5.0 (SP p. 47).
   Mínimos ideais: 2028 5,40; 2031 5,78; 2033 5,89; 2035 5,91 km/s.
2. **Regra de dimensionamento (variante iii)** (Etapa 1.4):
   - **estágio de saída da Terra:** dimensionado pela janela da missão A (2028). Esse estágio é
     montado para cada lançamento, então não precisa cobrir as outras janelas;
   - **estágio de captura em Marte:** dimensionado pelo pior caso do seu trecho entre as janelas, e
     **descartado em Marte** depois da captura, como o módulo de inserção do ERO [F22];
   - **estágio de retorno:** separado do de captura, dimensionado pelo pior caso do seu trecho;
   - o cálculo está em `tools/dimensionamento.py`, com `regra_projeto` em
     `config/dimensionamento.yaml`.
3. **Por que não (i) nem (ii):**
   - (i), um estágio único para captura e retorno, é frágil à fração estrutural: com ε × 1,5 a massa
     na órbita baixa vai a 41 t sem plataforma e a 90 t com a plataforma de 850 kg, porque o inerte
     da captura viaja até o fim;
   - (ii) dimensiona a saída da Terra por uma janela que não é a da missão de referência, e dá a
     maior massa das três.
4. **A DLA não entra nesta regra** e será avaliada na Fase 2 (afeta a janela de 2033, DLA −55,5°).

## Histórico
- No primeiro portão da 1.3 foram citados 6,17 km/s (candidata D, pior só entre as candidatas
  apresentadas); com a classe de trânsito curto seriam 6,64 km/s; a regra do item 1 dá 5,91 km/s.
- Na Etapa 1.4 foram comparadas as três regras de estagiamento (i), (ii) e (iii) com o mesmo
  propelente por trecho: `docs/etapa1.4_dimensionamento.md`.

## Consequências
- Massa na órbita baixa da Terra no caso base (CU-2, margem de 10 %, plataforma de 850 kg, P-016):
  22,8 t pela regra (iii). Valor em `results/etapa1.4/dimensionamento.yaml`.
- Se a avaliação de DLA da Fase 2 exigir mudança de plano em 2033, o pior caso da captura ou do
  retorno pode mudar, e o envelope deve ser recalculado.

## Atualização (Etapa 2.4, 2026-10-27): limite de DLA em 2033
Decisão do Fabio no portão da Etapa 2.4: na janela de 2033 a partida da Terra fica limitada a |DLA| ≤ 50°
(`config/missoes.yaml`). Sem o limite, a melhor conjunção tinha DLA de −55,5°, a 0,13° do limite de azimute
do Cabo [F13], com penalidade de lançamento aproximada de 0,76 (P-036).
- Regra do item 1 reaplicada (`results/etapa1.3/missoes.yaml`): mínimos por janela 2028 5,399; 2031 5,781;
  **2033 5,912**; 2035 5,911 km/s. **Envelope = 5,912 km/s, definido agora pela conjunção de 2033**
  (partida 2033-04-23, C3 9,60 km²/s², DLA −49,7°), contra 5,911 km/s (2035) antes.
- A regra (iii) usa o pior caso de cada estágio de Marte. Ele não muda, e as massas também não: os
  resultados da Etapa 2.3 foram regenerados sem diferença.
- O item de consequências acima ("se a avaliação de DLA da Fase 2 exigir mudança de plano em 2033…") fica
  atendido por esta atualização.

