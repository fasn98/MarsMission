# ADR 0009 — Conceito de coleta de amostras: tubos do Perseverance + braço no lander

Status: Accepted (Fabio, 2026-10-27, portão do item 2 da Etapa 2.5)
Data: 2026-10-27

## Contexto
O lander de base (L3, lander do MSR sem MAV e sem rover de busca) não tinha quem coletasse amostras.
Foram comparadas três opções, com massa, energia, complexidade e objetivo científico
(`results/etapa2.5/coleta.md`, `config/coleta.yaml`):
- (a) braço no lander, regolito do sítio (análogo Phoenix);
- (b) rover próprio de busca (análogo do Sample Fetch Rover do MSR);
- (c) recuperar os tubos do Perseverance em Jezero.

## Decisão
**(c) + (a) combinados.**
1. **Primário:** dois helicópteros (2 × 2,5 kg [F98]) recuperam os tubos do depósito Three Forks e, se o
   Perseverance estiver operando, os tubos a bordo. Objetivo científico: amostras selecionadas e seladas pelo
   Perseverance.
2. **Reserva e complemento:** um braço no lander coleta solo/regolito do sítio, com a carga útil do Phoenix
   como análogo (59 kg [F40], P-034). Ele garante retorno de amostras se o depósito não estiver disponível.
3. **Dimensionamento:** o lander leva os dois itens. A plataforma (P-017) fica em L3 1470 + braço 88,5 +
   helicópteros 6,4 = **1564,9 kg**, com margem E1. A massa injetada passa a **3.740 kg**.
4. **Margens na forma (a)** (ADR 0008), pior caso nas quatro janelas (`results/etapa2.4/lancamento.yaml`):

| Lançador | Pior margem |
| :- | -: |
| Falcon Heavy, recuperação / descartável | +25 % / +200 % |
| Vulcan VC2 / VC4 / VC6 | +16 % / +73 % / +122 % |

## Riscos declarados (não avaliados quantitativamente)
- **Integridade atual do depósito:**
  - 10 tubos foram deixados entre 21/12/2022 e 28/01/2023 [F99].
  - Os 10 tubos do depósito são "the less desirable of the initial sample pairs" ([F97] p. 32).
  - Não foi encontrado relato primário posterior sobre o estado do depósito.
- **Perseverance ativo na data do pouso** (só para os tubos a bordo):
  - O rover está operando; última imagem consultada: Sol 2009, 14/10/2026 [F100].
  - O pedido de orçamento FY2027 reduz o ritmo das operações e põe a extensão da missão na Senior Review de
    2026 [F102]. O resultado da revisão não foi confirmado.
- **Pouso de precisão perto do depósito:** não avaliado. O lander do MSR previa "Pin-point landing (< 20 m
  from target)" ([F24] slide 10).
- **Situação do programa MSR:**
  - O pedido FY2026 (maio de 2025) propõe "terminate the Mars Sample Return Program" ([F101] p. 242).
  - A página do MSR (atualizada em 17/09/2026) fala do programa no passado [F103].
  - O pedido FY2027 (22/04/2026) diz que "Subsequent missions could retrieve the sealed samples collected
    by Perseverance" ([F102] p. 202).

## Consequências
- **Sítio de pouso:** Jezero, perto do depósito Three Forks. A latitude do modelo (18,85°) já é a de Jezero;
  a precisão de pouso fica como risco.
- **Massa do braço:** a massa da carga útil do Phoenix deixa de ser alocação provisória e passa a ser a
  coleta de reserva.
- **Twin (Fase 8):** os helicópteros são candidatos à simulação, reaproveitando o DroneSimulator
  (repositório só de leitura; método, não números).
