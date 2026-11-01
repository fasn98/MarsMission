# Etapa 4.5: estrutura e lista de massas

Fase 4, subsistemas. Os números vêm de `results/etapa4.5/lista_massas.md` e `.yaml`, gerados por
`tools/lista_massas_lander.py`. As entradas são:
- `config/lista_massas.yaml` e `config/plataformas.yaml`;
- os resultados das Etapas 4.1 a 4.3;
- o modelo de veículos (`orbital.veiculos`).

## 1. Pergunta (escopo consolidado pelo Fabio)
1. **Lista de massas do lander de baixo para cima,** por subsistema, para substituir ou confirmar o L3 (P-017). Inclui o que
   as Etapas 4.1 a 4.4 acrescentaram.
2. **Rejeição de calor no cruzeiro:** passiva ou ativa, com análogo publicado.
3. **Totais e margens dos lançadores,** e a dependência do orbitador em relação ao Falcon Heavy descartável.
4. **Risco do MAV:** as mitigações, com uma proposta.

## 2. Lista de massas: o que dá e o que não dá para fazer de baixo para cima
- **Nenhuma fonte primária pública publica a massa de um lander de Marte por subsistema.** A pesquisa cobriu o lander do MSR,
  o Phoenix, o InSight, o MSL e o Mars 2020; o Kazachok ficou bloqueado. Só há totais e partes grandes.
- O **núcleo** continua de cima para baixo, no L3: estrutura, pernas, propulsão de descida seca, térmico, aviônica,
  cabeamento e o sistema de lançamento do MAV.

Itens identificados (`results/etapa4.5/lista_massas.md`, margem E1 no ponto médio):

| Item | Prevista (kg) | Novo nas Etapas 4.1–4.4? | Fonte |
| :- | -: | :- | :- |
| Energia: painel e bateria da C + RHU | 277,5 | sim | Etapas 4.1 e 4.2 |
| RHUs (35 × 42 g) | 1,9 | sim | [F152] |
| Enlace direto mínimo | 22,4 | sim | Etapa 4.3 |
| Câmera do TRN (LCAM) | 1,1 | sim | [F203] |
| Circuito de fluido de cruzeiro | 37,4 | sim | P-077 |
| UHF | 8,3 | não | [F74] |
| Radar | 6,4 | não | [F74] |
| Braço de coleta | 88,5 | não | [F40] |
| Helicópteros | 6,4 | não | [F98] |

- **Somas:** os itens novos somam 340,3 kg; todos os itens, 449,8 kg.
- **Fora da lista:** o computador de visão do TRN (VCE) não tem massa publicada. O propelente do desvio do pouso de precisão
  também não ([F192], SRL).
- **Dupla contagem:** o item do MAV traz 24,1 kg de energia do aquecimento, que a energia C + RHU já cobre.

**O L3 comporta os itens?**
- O L3 tem 1.470 kg. Tirando os itens que estão dentro dele, sobram 1.115 kg para o núcleo.
- A descida seca do Mars 2020 tem 688,2 kg [F204]. Ela é de sky crane e não tem pernas nem plataforma de superfície.
- O L3 não é contradito pelos itens, mas também não é confirmado: o núcleo não tem lista publicada.

## 3. Rejeição de calor no cruzeiro
- **Lander:**
  - a dissipação é de 374 W: o lander do SRL, com 339 W [F165], mais as RHUs (Etapa 4.2). Isso passa do limite passivo do
    SRL, de 200 W [F165], então a rejeição tem de ser ativa;
  - o MSL e o Mars 2020 usaram circuito de fluido bombeado no cruzeiro [F206, F207];
  - a massa do circuito não é publicada para MSL, Mars 2020 e SRL. Pela escala do requisito do MPF (menos de 18 kg para
    180 W [F205]), fica em cerca de 37,4 kg (P-077, ordem de grandeza).
- **Orbitador:** os radiadores estão dentro da plataforma por subsistema (Etapa 2.3). A rejeição de calor de cruzeiro do
  orbitador não foi estudada à parte.

## 4. Totais e margens dos lançadores
| Caso de plataforma do lander | Plataforma | Lander injetado | Falcon Heavy (recuperação) | Falcon Heavy (descartável) | Vulcan VC2 | Vulcan VC4 | Vulcan VC6 |
| :- | -: | -: | -: | -: | -: | -: | -: |
| A: L3 vigente (P-017) | 1.565 kg | 4.012 kg | +17 % | +180 % | +8 % | +62 % | +107 % |
| B: L3 + itens novos, sem a dupla contagem | 1.881 kg | 4.654 kg | **+1 %** | +141 % | **−7 %** | +39 % | +78 % |
| C: núcleo = descida seca do Mars 2020 + todos os itens | 1.114 kg | 3.096 kg | +51 % | +263 % | +40 % | +110 % | +168 % |

- **Os três casos:**
  - B é o conservador: supõe que nenhum item novo cabe dentro do L3;
  - C não é crível como base, porque não tem pernas, plataforma de superfície, térmico de superfície nem sistema de
    lançamento do MAV. Fica só como limite inferior.
- **Orbitador:** não muda com a plataforma do lander (Falcon Heavy descartável +44 %; Vulcan VC6 +6 %). A dependência do
  Falcon Heavy descartável continua (ADR 0008).

## 5. Risco do MAV: mitigações
| Mitigação | Efeito no caso B | Prós | Contras |
| :- | :- | :- | :- |
| (a) margem de lançador | sem número de política com fonte | — | o JPL pede 30 % de margem de massa do **sistema** na Pré-Fase A [F210], que é outra grandeza; o "10 %/15 %" do lançador não foi conferido |
| (b) lançador maior para o lander | VC4 +39 %; VC6 +78 %; Falcon Heavy descartável +141 % | margem grande sem mudar o MAV | custo, não avaliado (Fase 6); com o Falcon Heavy descartável, os dois lançamentos dependem desse veículo |
| (c) Isp maior com motor que voou | 317 s (LEROS 1b): VC2 de −7 % para −5 %; 324 s (LEROS 1c): para −4 %; 321 s (S400-15): para −5 % | sem lançador novo | ganho de 1 a 3 pontos; os LEROS com voo usam MON/hidrazina [F208, F209] (troca de combustível; a hidrazina congela a +1,5 °C); o voo do S400-15 não foi conferido |

**Proposta do agente (o Fabio decide): (b), um lançador maior para o lander.**
- É a única mitigação que devolve margem ampla no caso conservador.
- A (c) melhora pouco e muda o combustível; a (a) não tem número de política com fonte.
- A escolha entre VC4, VC6 e Falcon Heavy descartável depende de custo e disponibilidade, que ficam fora desta etapa.

## 6. Para decidir (Fabio)
1. **Lista de massas:**
   - (A) manter o L3 (P-017), supondo que ele comporta os itens novos;
   - (B) somar os itens novos ao L3, que é mudança de valor-base da P-017;
   - (C) só como limite inferior.
2. **Rejeição de calor no cruzeiro:** circuito de fluido ativo no lander (~37,4 kg, P-077).
3. **Mitigação do MAV:** a proposta é (b), lançador maior para o lander, com o veículo a escolher.
4. **Premissa nova** (NÃO VALIDADA): P-077, massa do circuito de fluido.

## 7. Limitações
- **Núcleo do lander:** sem lista publicada; o L3 é uma alocação do SRL ("as much as 2100 kg").
- **Itens sem massa:** o VCE do TRN e o propelente do desvio não têm massa publicada.
- **Circuito de fluido:** a massa vem de uma escala linear a partir de um requisito do MPF.
- **Lançadores:** sem custo, e as curvas são as da Etapa 2.4.
