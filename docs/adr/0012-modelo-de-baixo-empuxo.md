# ADR 0012 — Modelo de baixo empuxo: critério da verificação e escopo de uso

Status: Accepted (Fabio, 2026-10-28, portão da Etapa 3.2)
Data: 2026-10-28

## Contexto
A Etapa 3.2 implementou:
- a espiral de baixo empuxo numérica, com empuxo tangencial;
- a solução analítica quase circular coplanar.

Ela verificou a espiral numérica contra a listagem publicada por Schwenzfeger (NASA TM X-64836, p. 31) [F113]. Pelo
critério declarado (1e-4 relativo por componente, P-046), a verificação não passa em u = r·ṙ
(`docs/etapa3.2_baixo_empuxo.md`, `results/etapa3.2/baixo_empuxo.md`).

## Decisão
1. **Critério da verificação: (B).**
   - Mantém-se o critério por componente (P-046, 1e-4).
   - Registro:
     - a espiral numérica concorda com [F113] em r, φ, v e h e nos vetores posição e velocidade (até 3,1e-5);
     - u fica fora, com até 3,2e-4;
     - a diferença é atribuída, provavelmente, à precisão da integração publicada. Isso **não foi confirmado**.
   - O erro vetorial é métrica **adicional** e não substitui o critério.
   - **Hipótese, não conferida:** u = r·ṙ é a parte radial, pequena e oscilante, do estado, e amplifica em termos
     relativos erros pequenos de r e da velocidade.
2. **Mudança de plano:** antes de buscar a fórmula de Edelbaum com mudança de plano, verificar se a Etapa 3.3 precisa
   dela. Se a captura puder ser feita já na inclinação da órbita de encontro (escolha do plano de aproximação na
   chegada), as espirais ficam coplanares. Se precisar, usar a fórmula de uma fonte aberta da NASA, com página citada.
3. **Trecho heliocêntrico:** fica com o rótulo "calculado, não verificado".
   - Na Etapa 3.3, prioridade para a opção (c), híbrida (captura química e espiral elétrica), que só usa o trecho
     verificado.
   - A opção (b), elétrica, leva o rótulo.
   - O Moeckel TR R-53 é opcional, de baixa prioridade.
4. **P-046:** aprovada, NÃO VALIDADA.

## Consequências
- A espiral planetocêntrica é usada na Etapa 3.3 com o registro do item 1.
- Resultados que dependam do trecho heliocêntrico elétrico levam "calculado, não verificado".
