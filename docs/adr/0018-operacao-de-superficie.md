# ADR 0018 — Operação de superfície: helicópteros adaptativos, pouso de precisão e folga antes da conjunção

Status: Accepted (Fabio, 2026-11-01, portão da Etapa 4.4)
Data: 2026-11-01

## Contexto
A Etapa 4.4 (`docs/etapa4.4_gnc_superficie.md`, `results/etapa4.4/operacao_superficie.md`) montou a linha do tempo da
superfície: pouso, busca dos 10 tubos, transferência tardia ao MAV e lançamento. Ela foi calculada em três distâncias até o
depósito e em dois ritmos (SRH e o ritmo real do Ingenuity). A etapa também comparou o volume de dados dos helicópteros com
a capacidade de cada caminho de comunicação.

## Decisão
1. **Helicópteros em operação adaptativa: (a) + (b).**
   - A autonomia fica no nível que o Ingenuity demonstrou: pontos de passagem, escolha do local de pouso e armazenamento a
     bordo [F197, F186, F179].
   - O ritmo de voo se ajusta à capacidade dos passes de relé, do ritmo do SRH ao do Ingenuity.
   - A opção (c), o enlace direto maior, fica só como sensibilidade, porque não foi achado análogo.
2. **Pouso de precisão é requisito.** A P-075 (200 m do depósito) passa a **crítica**.
3. **Folga do MAV antes da conjunção:** mínimo de **60 dias**, o pior caso que cabe no ritmo do SRH em qualquer ponto da
   elipse. O plano de referência mira de 100 a 180 dias.
4. **P-062:** corrigida para 28/01/2023, alinhada à fonte [F99].
5. **P-073 a P-076:** aprovadas, NÃO VALIDADAS. A P-075 é crítica.

## A P-075 é sustentável? (`config/premissas.yaml`, P-075)
- O Perseverance pousou a 5 m do alvo que o TRN escolheu [F189]. Mas a entrada guiada o entregou a 1,7 km do ponto esperado
  [F190], e o TRN desvia no máximo 600 m [F188].
- A precisão prevista para o lander do MSR, na sequência nocional de EDL, era "Pin-point landing (< 20 m from target)" [F202].
  - Um artigo de 2024 da AIAA citaria 60 m para o lander do MSR; não foi conferido, porque o texto completo está atrás de
    paywall.
  - O "60m touchdown error requirement" de [F189] é do Mars 2020, não do lander do MSR.
- **Conclusão:** 200 m só se sustentam com pouso de precisão da classe do lander do MSR, que não voou. Com a capacidade
  demonstrada pelo Perseverance, a distância até o depósito tende à ordem do erro de entrega, 1,7 km. Essa leitura é do
  agente: a fonte dá o erro, não a distância a um depósito.

## Conclusão registrada
**O plano de superfície só fecha com ritmo rápido OU pouso de precisão, e o ritmo rápido depende de dados que os relés
existentes não garantem.**
- No ritmo do SRH, todos os casos lançam antes da conjunção, com folga de 60,5 a 183,8 dias.
  - Mas o volume dos helicópteros, de 352 a 1.605 Mbit por sol com o lander, só cabe nos relés existentes na parte alta da
    faixa: TGO de 60 a 2.000 e MRO de 100 a 1.150 Mbit por sol.
- No ritmo do Ingenuity, o volume cai, mas só o caso de 200 m com dois helicópteros cabe (101,6 dias de folga), e esse caso
  exige pouso de precisão.

## Consequências
- **Proposta, a confirmar pelo Fabio:** o pouso de precisão entra na lista de massas e na EDL (Etapa 4.5 em diante), como
  capacidade a demonstrar.
- O risco de dependência do TGO (ADR 0017) se soma ao ritmo da busca: com menos capacidade de relé, a operação desacelera,
  e a folga cai na direção do mínimo de 60 dias.

## Grandezas de precisão de pouso (pedido do Fabio, portão da 4.4)
| Número | O que mede | Fonte | Comparável com a P-075? |
| :- | :- | :- | :- |
| 60 m (requisito) e 5 m (alcançado), Mars 2020 | erro até o alvo escolhido a bordo durante a descida, entre os pontos seguros ao alcance do desvio do TRN | [F189], [F188] | não |
| 1,7 km, Mars 2020 | distância entre o ponto de toque real e o ponto de toque esperado antes do voo (demonstrado) | [F190] | sim, com a parcela de erro |
| < 20 m, lander do MSR | erro previsto até o alvo pré-selecionado, na sequência nocional de EDL (não voado) | [F202], [F192] | sim, com a parcela de erro |

- **A P-075 é uma distância:** o afastamento planejado do ponto-alvo ao depósito mais o erro de pouso em relação a esse ponto.
- **Os 200 m de [F191] são um afastamento planejado.** Se a seta da figura vai até a borda do círculo de 60 m, a distância
  iria de 200 a 320 m (leitura do agente).
- **Os 200 m não ficam do lado conservador:**
  - com o erro demonstrado (1,7 km), ficam muito do lado otimista;
  - com o erro previsto do lander do MSR (< 20 m), só seriam conservadores com um afastamento planejado menor que cerca de
    180 m.
- **Faixa sem mudança:** pela regra da P-073, a linha do tempo é a mesma do caso de 200 m até 300 m no ritmo do Ingenuity e
  até 700 m no ritmo do SRH (`results/etapa4.4/operacao_superficie.md`).

## Conclusão principal da Etapa 4.4 (Fabio)
**"O plano de superfície depende de uma capacidade não demonstrada em voo em qualquer combinação: com a precisão de pouso já
voada (~1,7 km, Mars 2020), só fecha com o ritmo do SRH (não voado); com o ritmo voado do Ingenuity, só fecha com pouso de
precisão < ~300 m (previsto, não voado)."**

Conferência nos resultados:
- a 1,7 km, o ritmo do SRH lança antes da conjunção (63 e 103 sóis), e o do Ingenuity passa da partida;
- no ritmo do Ingenuity, só o caso de 200 m com dois helicópteros cabe, e a faixa sem mudança vai até 300 m.

## Risco principal da Fase 4
**Risco principal da Fase 4 (decisão do Fabio): o plano de superfície depende de uma capacidade não demonstrada em voo.**
- Ou o ritmo de busca do SRH, ou o pouso de precisão abaixo de ~300 m do depósito.
- O ritmo rápido ainda depende de capacidade de relé que os orbitadores existentes não garantem (ADR 0017).
- O risco entra no relatório da Fase 4 (Etapa 4.6).
