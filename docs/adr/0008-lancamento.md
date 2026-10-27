# ADR 0008 — Chegada à trajetória para Marte: injeção direta pelo lançador

Status: Accepted (Fabio, 2026-10-27, portão da Etapa 2.4)
Data: 2026-10-27

## Contexto
Na Etapa 2.4 foram comparadas duas formas de pôr orbitador e lander na trajetória para Marte, com os dois em
lançamentos separados (ADR 0005), em cada janela do envelope (2028–2035), com o C3 e a DLA de cada uma
(`docs/etapa2.4_lancamento.md`):
- (a) **injeção direta**: o lançador entrega o veículo no C3 da janela;
- (b) **órbita baixa + estágio criogênico próprio** (o modelo das Etapas 1.4 a 2.3).

## Decisão
1. **Forma (a), injeção direta pelo lançador.**
2. **Orbitador:** Falcon Heavy descartável ou Vulcan VC6.
3. **Lander:** os lançadores que servem por injeção direta em todas as janelas: Falcon Heavy (recuperação ou
   descartável) e Vulcan VC2, VC4 ou VC6. New Glenn e SLS ficam como "desempenho anunciado, não demonstrado".
   O Falcon 9 serve o lander só na forma (b) e fica fora.
4. **Janela de 2033 limitada a |DLA| ≤ 50°.** A regra do envelope (ADR 0004) foi reaplicada.
5. **A forma (b) fica documentada como alternativa.** Ressalva: exige estágio criogênico (LOX/LH2) próprio,
   com armazenamento na órbita baixa antes da queima de saída, que não foi modelado.

## Resultado no momento da decisão (`results/etapa2.4/lancamento.yaml`)
- **Massas injetadas:** orbitador da regra (iii) 6.027 kg; lander 3.727 kg.
- **Pior margem do orbitador em (a)**, nas quatro janelas:

| Lançador | Pior margem | Janela | Condição |
| :- | -: | :- | :- |
| Falcon Heavy descartável | +86 % | 2033 | DLA −49,7°, multiplicador de 0,902 (P-036) |
| Vulcan VC6 | +38 % | 2033 | idem |

- **Lançamentos da arquitetura:** 2, um por veículo.

## Ressalvas
- **"Lançador em operação"** vale na data do guia ou da consulta citada (ELVPerf consultado em 2026-10-27;
  guias de 2021 a 2025). A disponibilidade desses lançadores em 2028 e depois **não foi avaliada**.
- **Penalidade de DLA:** vem de uma tabela aproximada de Atlas V e Delta IV [F83], aplicada aos demais
  lançadores (P-036, NÃO VALIDADA).
- **Não avaliados:** coifa (diâmetro), período de lançamento e janela finita.

## Consequências
- **Massa na órbita baixa da Terra:** a soma da Etapa 2.3 (29,6 t pela regra iii) deixa de ser a medida
  de lançamento. Com (a), o orbitador não leva estágio de saída próprio. A Etapa 2.5 consolida a arquitetura
  com essa escolha.

## Atualização (Etapa 2.5, 2026-10-27): sensores de encontro no orbitador
Com os sensores de encontro alocados (Etapa 2.5), o orbitador da regra (iii) passa de 6.027 para **6.310 kg**
injetados. Pior margem na forma (a) (`results/etapa2.4/lancamento.yaml`):

| Lançador | Antes | Depois |
| :- | -: | -: |
| Falcon Heavy descartável | +86 % | **+78 %** |
| Vulcan VC6 | +38 % | **+31 %** |

Os dois continuam servindo. O lander não muda. Os números das seções acima são os de antes desta atualização.

## Atualização (Etapa 2.5, 2026-10-27): helicópteros de coleta no lander (ADR 0009)
Com os helicópteros de recuperação (ADR 0009), o lander passa de 3.727 para **3.740 kg** injetados e a nota
anterior ("O lander não muda") deixa de valer.

| Lançador | Pior margem antes | Pior margem depois |
| :- | -: | -: |
| Falcon Heavy, recuperação | +26 % | **+25 %** |
| Falcon Heavy, descartável | +201 % | **+200 %** |
| Vulcan VC2 | +16 % | **+16 %** |
| Vulcan VC4 | +74 % | **+73 %** |
| Vulcan VC6 | +123 % | **+122 %** |

Fonte: `results/etapa2.4/lancamento.md`.

