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
| Circuito de fluido de cruzeiro (sem margem E1) | 35,7 | sim | P-077 |
| UHF | 8,3 | não | [F74] |
| Radar | 6,4 | não | [F74] |
| Braço de coleta | 88,5 | não | [F40] |
| Helicópteros | 6,4 | não | [F98] |

- **Somas:** os itens novos somam 338,6 kg; todos os itens, 448,1 kg.
- **Fora da lista:** o computador de visão do TRN (VCE) não tem massa publicada. O propelente do desvio do pouso de precisão
  também não ([F192], SRL).
- **Dupla contagem:** o item do MAV traz 24,1 kg de energia do aquecimento, que a energia C + RHU já cobre.

**O L3 comporta os itens?**
- O L3 tem 1.470 kg. Tirando os itens que estão dentro dele, sobram 1.141 kg para o núcleo. A energia do aquecimento do MAV,
  que fica no item do MAV, não é descontada do L3.
- A descida seca do Mars 2020 tem 688,2 kg [F204]. É o descent stage de um sky crane, sem pernas nem plataforma de superfície.
- O L3 não é contradito pelos itens, mas também não é confirmado: o núcleo não tem lista publicada.

## 3. Rejeição de calor no cruzeiro
- **Lander:**
  - a dissipação é de 357 W: a dissipação máxima do LAMP do SRL, 322 W [F165], mais as RHUs (Etapa 4.2). Isso passa da
    perda passiva máxima do LAMP, de 200 W [F165], então a rejeição tem de ser ativa. As duas grandezas são do LAMP;
  - o MSL e o Mars 2020 usaram circuito de fluido bombeado no cruzeiro [F206, F207];
  - a massa do circuito não é publicada para MSL, Mars 2020 e SRL. Pela escala do requisito do MPF (menos de 18 kg para
    180 W [F205]), fica em cerca de 35,7 kg (P-077, ordem de grandeza). Não leva margem E1, porque o valor do MPF é um máximo;
  - **é conservador:** o circuito entra aqui na plataforma de superfície. No MSL e no Mars 2020, o radiador fica no estágio
    de cruzeiro, descartado antes da entrada [F206]. Levá-lo para o estágio de cruzeiro tiraria esse peso da massa pousada,
    que é a que pesa mais no lander injetado. Fica como opção para a Etapa 4.6.
- **Orbitador:** os radiadores estão dentro da plataforma por subsistema (Etapa 2.3). A rejeição de calor de cruzeiro do
  orbitador não foi estudada à parte.

## 4. Totais e margens dos lançadores
| Caso de plataforma do lander | Plataforma | Lander injetado | Falcon Heavy (recuperação) | Falcon Heavy (descartável) | Vulcan VC2 | Vulcan VC4 | Vulcan VC6 |
| :- | -: | -: | -: | -: | -: | -: | -: |
| A: L3 vigente (P-017) | 1.565 kg | 4.012 kg | +17 % | +180 % | +8 % | +62 % | +107 % |
| B: L3 + itens novos, sem a dupla contagem | 1.879 kg | 4.650 kg | **+1 %** | +141 % | **−7 %** | +39 % | +78 % |
| C: núcleo = descida seca do Mars 2020 + todos os itens | 1.112 kg | 3.093 kg | +51 % | +263 % | +40 % | +110 % | +168 % |

- **Os três casos:**
  - B é o conservador: supõe que nenhum item novo cabe dentro do L3. Nele, o Falcon Heavy com recuperação fica com +1 % e o
    Vulcan VC2 perde a margem (−7 %);
  - C não é crível como base, porque não tem pernas, plataforma de superfície, térmico de superfície nem sistema de
    lançamento do MAV. Fica só como limite inferior.
- **Orbitador:** não muda com a plataforma do lander (Falcon Heavy descartável +44 %; Vulcan VC6 +6 %). A dependência do
  Falcon Heavy descartável continua (ADR 0008).

## 5. Risco do MAV: mitigações
| Mitigação | Efeito no caso B | Prós | Contras |
| :- | :- | :- | :- |
| (a) margem de lançador | sem número de política com fonte | — | o JPL pede 30 % de margem de massa do **sistema** "for a concept at this stage of development" [F210] (outro estudo; aplicar à Pré-Fase A é inferência), que é outra grandeza; o "10 %/15 %" do lançador não foi conferido |
| (b) lançador maior para o lander | VC4 +39 %; VC6 +78 %; Falcon Heavy descartável +141 % | margem grande sem mudar o MAV | custo, não avaliado (Fase 6); com o Falcon Heavy descartável, os dois lançamentos dependem desse veículo |
| (c) Isp maior | 317 s (LEROS 1b, voou): VC2 de −7 % para −5 %; 321 s (S400-15): para −5 %; 324 s (LEROS 1c): para −4 % | sem lançador novo | ganho no VC2 de 1,6 a 3,0 pontos; os dois LEROS usam MON/hidrazina [F208, F209] (troca de combustível, que reabre o ADR 0011); o LEROS 1c foi entregue, mas o voo não foi conferido; o voo do S400-15 também não; a sensibilidade troca só o Isp (empuxo, número e massa dos motores e propelente ficam os do R-4D-11) |

**Proposta do agente (o Fabio decide): (b), um lançador maior para o lander.**
- É a única mitigação que devolve margem ampla no caso conservador.
- A (c) melhora pouco e, com os LEROS, muda o combustível; a (a) não tem número de política com fonte.
- A escolha entre VC4, VC6 e Falcon Heavy descartável depende de custo e disponibilidade, que ficam fora desta etapa.

## 6. Para decidir (Fabio)
1. **Lista de massas:**
   - (A) manter o L3 (P-017), supondo que ele comporta os itens novos;
   - (B) somar os itens novos ao L3, que é mudança de valor-base da P-017;
   - (C) só como limite inferior.
2. **Rejeição de calor no cruzeiro:** circuito de fluido ativo no lander (~35,7 kg, P-077); radiador na plataforma (como
   está) ou no estágio de cruzeiro (como no MSL e no Mars 2020).
3. **Mitigação do MAV:** a proposta é (b), lançador maior para o lander, com o veículo a escolher.
4. **Premissa nova** (NÃO VALIDADA): P-077, massa do circuito de fluido.

## 7. Limitações
- **Núcleo do lander:** sem lista publicada; o L3 é uma alocação do SRL ("as much as 2100 kg").
- **Itens sem massa:** o VCE do TRN e o propelente do desvio não têm massa publicada.
- **Circuito de fluido:** a massa vem de uma escala linear a partir de um requisito do MPF.
- **Isp:** a sensibilidade troca só o Isp; não é um projeto do MAV com outro motor.
- **Margem de sistema [F210]:** cópia do relatório no arXiv, não conferida contra o original do JPL.
- **Lançadores:** sem custo, e as curvas são as da Etapa 2.4.

## Nota (2026-11-01): decisões do portão
Decisões do Fabio (o texto acima fica como estava):
1. **Lista de massas:** caso B. A P-017 muda de valor-base (aprovado), e o caso A fica como referência otimista (ADR 0019).
2. **Circuito de fluido:** radiador no estágio de cruzeiro, descartado antes da entrada (ADR 0019).
3. **Mitigação do MAV:** (b), com diversidade (ADR 0020).
   - lander no Vulcan VC4, com o VC6 de reserva;
   - orbitador no Falcon Heavy descartável;
   - a (c) foi descartada.
4. **P-077:** aprovada, NÃO VALIDADA. Corrigidos o campo `uso` e o sinal dos ganhos em pontos.

Os números vigentes, com o antes e depois das decisões, estão em `results/etapa4.5/lista_massas.md`. As tabelas das seções 2
e 4 acima são da versão do portão.
