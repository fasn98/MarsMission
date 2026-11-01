# ADR 0019 — Massa do lander (caso B) e circuito de fluido no estágio de cruzeiro

Status: Accepted (Fabio, 2026-11-01, portão da Etapa 4.5)
Data: 2026-11-01

## Contexto
A Etapa 4.5 (`docs/etapa4.5_massas.md`, `results/etapa4.5/lista_massas.md`) tentou montar a lista de massas do lander de
baixo para cima.
- Nenhuma fonte primária pública dá a massa de um lander de Marte por subsistema. O núcleo (estrutura, pernas, propulsão de
  descida, térmico, aviônica, cabeamento, sistema de lançamento do MAV) fica de cima para baixo, no L3.
- As Etapas 4.1 a 4.4 acrescentaram itens com massa: energia C + RHU, RHUs, enlace direto mínimo e câmera do TRN.
- O lander dissipa no cruzeiro mais do que a perda passiva máxima do LAMP do SRL [F165]. A rejeição tem de ser ativa, com
  um circuito de fluido como no MSL e no Mars 2020 [F206, F207].

Opções apresentadas no portão:
- **Plataforma:** (A) manter o L3, supondo que ele comporta os itens novos; (B) somar os itens novos ao L3; (C) estágio de
  descida do Mars 2020 + todos os itens, só como limite inferior.
- **Radiador:** na plataforma, ou no estágio de cruzeiro.

## Decisão
1. **Plataforma de superfície: caso B, conservador.** A P-017 passa a ser L3 + braço + helicópteros + itens das Etapas 4.1
   a 4.4, menos a energia do aquecimento do MAV que o item do MAV já traz. O valor é calculado por
   `tools/lista_massas_lander.py` e conferido por `tests/test_lista_massas.py`.
2. **O caso A** (L3 + braço + helicópteros) fica como referência otimista.
3. **Circuito de fluido no estágio de cruzeiro**, descartado antes da entrada, como no MSL e no Mars 2020 [F206]. Massa pela
   P-077 (escala do MPF [F205]), em `config/superficie.yaml`.
4. **P-077:** aprovada, NÃO VALIDADA.

Os números (antes e depois) estão em `results/etapa4.5/lista_massas.md`, seção "Antes e depois das decisões do portão da 4.5".

## Consequências
- **Massa do lander:** o lander injetado e as margens mudam em toda a cadeia (Fases 2 a 4, regeneradas). As etapas
  anteriores à 2.3 regeneram sem o circuito (`antes_etapa_4_5` em `config/lista_massas.yaml`).
- **Composição:** `results/etapa2.5/arquitetura.md` lista os itens das Etapas 4.1 a 4.4 e o circuito à parte.
- **Opções de coleta:** em `results/etapa2.5/coleta.md`, as opções recebem os mesmos itens.
- **Enlace direto mínimo:** na Etapa 4.3, o efeito no lander passa a ser medido como P-017 sem e com o enlace.

## Limitações
- **Possível contagem dupla:** pode haver contagem dupla com a energia e as telecomunicações próprias do SRL dentro do L3. O
  caso B é conservador por construção.
- **Sem massa publicada:** o computador de visão do TRN (VCE) e o propelente do desvio não têm massa publicada.
- **Circuito de fluido:** a massa vem de uma escala linear a partir de um requisito do MPF (ordem de grandeza).
- **Margens misturadas:** nos casos de margem GSFC e ESA (`results/etapa2.5/arquitetura.md`), a margem GSFC ou ESA vale para
  L3 + braço + helicópteros, e os itens das Etapas 4.1 a 4.4 entram com a margem E1. Os casos L1 e SRL 2024 − MAV são
  plataformas inteiras e não recebem os itens.
- **Opção (c) da Etapa 4.4:** a HGA maior (`results/etapa4.4/operacao_superficie.md`) continua somada por cima da P-017, que
  agora já inclui o enlace direto mínimo. Há sobreposição parcial (HGA e gimbal); como é só sensibilidade, o resultado fica
  conservador.
