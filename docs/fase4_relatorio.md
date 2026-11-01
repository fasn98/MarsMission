# Fase 4: subsistemas (relatório)

Estudo conceitual (Pré-Fase A) MarsMission. Autor e decisor: Fabio Nogueira.
- Os números vêm de `results/`, gerados por `tools/` a partir de `config/`, e são citados com o arquivo.
- O resumo integrado está em `results/fase4/resumo.md` (`tools/fase4.py`).
- Nada aqui é "validado". "Verificado" só quando há comparação com dado publicado.

## 1. Resultado em uma página
- **Energia** (Etapa 4.1, ADRs 0015 e 0016):
  - lander solar com sobrevivência e 35 RHUs (C + RHU), com 61,6 g de Pu-238, Tier I pelo critério de quantidade;
  - painel de 32,8 m² e total de 277,5 kg;
  - orbitador com carga de 1.022 W;
  - MMRTG (alternativa A, hoje com 3 unidades em `results/etapa4.1/energia.md`) é alternativa condicionada à disponibilidade
    de Pu-238.
- **Térmico** (Etapa 4.2):
  - MAV aquecido a 15 °C (P-027): 60,8 W;
  - amostras com transferência tardia para o MAV;
  - no cruzeiro, o lander precisa de rejeição de calor ativa (Etapa 4.5): 357 W contra 200 W de perda passiva máxima.
- **Comunicação** (Etapa 4.3, ADR 0017):
  - TGO como relé primário e MRO enquanto disponível;
  - reserva própria (relé pelo orbitador + enlace direto mínimo de 22,4 kg);
  - conjunção solar de 2030-05-06 a 2030-06-13.
- **Operação de superfície** (Etapa 4.4, ADR 0018):
  - helicópteros em operação adaptativa;
  - pouso de precisão é requisito (P-075, crítica);
  - MAV lançado com folga mínima de 60 dias antes da conjunção, alvo de 100 a 180 dias.
- **Massas e lançadores** (Etapa 4.5, ADRs 0019 e 0020):
  - plataforma do lander no caso B (P-017), com o circuito de fluido no estágio de cruzeiro (P-077);
  - lander no Vulcan VC4, com o VC6 de reserva; orbitador no Falcon Heavy descartável.

Os números de energia, térmico, comunicação e superfície estão em `results/fase4/resumo.md`. Massas vigentes
(`results/fase4/resumo.md`; fim da Fase 3 pelo relatório da Fase 3, seção 1):

| Item | Fim da Fase 3 | Fim da Fase 4 |
| :- | -: | -: |
| Orbitador injetado (regra iii) | 7.205 kg | **7.796 kg** |
| Lander injetado | 3.996 kg | **4.615 kg** |
| MAV + energia do aquecimento | 403 kg | **411 kg** |
| Plataforma de superfície do lander (P-017) | 1.564,9 kg | **1.843,7 kg** |
| Total na órbita baixa da Terra, regra (iii) | 34.003 kg | **37.675 kg** |

**Por que as massas mudaram na Fase 4:**
- **Orbitador:** carga de 1.022 W e captura com 10 × R-4D-11 (ADR 0015; errata da 4.1 no relatório da Fase 3).
- **MAV:** alvo de 15 °C (Etapa 4.2).
- **Lander:** itens das Etapas 4.1 a 4.4 e circuito de fluido (ADR 0019).

**Lançadores de base** (`results/fase4/resumo.md`; pior janela, injeção direta):

| Veículo | Lançador | Margem na base | Pior margem nas sensibilidades |
| :- | :- | -: | -: |
| Orbitador | Falcon Heavy descartável | +44 % | +18 % (margem de Δv 20 %) |
| Lander | Vulcan VC4 | +41 % | +8 % (ε do MAV 0,300, sem fonte) |
| Lander (reserva) | Vulcan VC6 | +80 % | +38 % (ε do MAV 0,300, sem fonte) |

## 2. Método
- **Energia** (`src/orbital/energia.py`, `tools/energia.py`):
  - insolação em Jezero com τ por Ls, painel calibrado no 1º sol do InSight e poeira sem limpeza;
  - sobrevivência na tempestade global com o aquecimento do MAV e análogos do Spirit e do MER;
  - carga do orbitador por modo (P-053).
- **Térmico** (`tools/termico.py`):
  - aquecimento do MAV pela perda até o ambiente de Jezero;
  - comparação com o projeto publicado do lander do SRL [F165, F166];
  - faixas das amostras [F167].
- **Comunicação** (`tools/comunicacao.py`):
  - SEP pela efeméride DE440;
  - enlace direto escalado do MSL, relé UHF por Friis e capacidade dos orbitadores existentes por fonte atual.
- **Superfície** (`tools/operacao_superficie.py`):
  - linha do tempo da busca dos tubos em três distâncias e dois ritmos (SRH e Ingenuity);
  - probabilidade de tempestade pelo catálogo de Ls;
  - folga até a conjunção.
- **Massas** (`tools/lista_massas_lander.py`):
  - itens identificados com margem E1 e conferência do L3;
  - três casos de plataforma e as margens dos lançadores;
  - sensibilidade a um Isp maior.
- **Integração** (`tools/fase4.py`): resumo e margens dos lançadores de base, com a pior margem nas sensibilidades de
  `results/etapa2.5/arquitetura.md`.

## 3. Verificações
- **Insolação diária contra a tabela do VL1** [F56] (`results/etapa4.1/energia.md`): maior diferença de 1,8 %.
  - A tabela é cálculo publicado (Appelbaum & Flood), não medida.
  - A comparação verifica a implementação, não o ambiente de Jezero.
- **Comparações com dados de voo, sem critério de aceitação declarado** (não são "verificado"):
  - o modelo contra o Opportunity na tempestade de 2018 [F140] (`results/etapa4.1/energia.md`) sai otimista. Por isso há a
    sensibilidade da P-059;
  - a escala do enlace em banda X e o relé UHF contra o Electra (`results/etapa4.3/comunicacao.md`) são conferências de
    ordem de grandeza.
- **Reprodutibilidade:** os `results/` da Fase 4 saem do código e do `config/` atuais (`tools/confere_regeneracao.py`, CI).

## 4. Decisões (ADRs da Fase 4)
| ADR | Decisão |
| :- | :- |
| 0015 | Energia: lander solar com sobrevivência (C); carga do orbitador de 1.022 W; captura com 10 × R-4D-11 |
| 0016 | MMRTG como alternativa condicionada à disponibilidade de Pu-238 |
| 0017 | Comunicação: TGO primário, MRO enquanto disponível, reserva própria para o mínimo crítico |
| 0018 | Superfície: helicópteros adaptativos; pouso de precisão como requisito; folga mínima de 60 dias antes da conjunção |
| 0019 | Plataforma do lander no caso B; circuito de fluido no estágio de cruzeiro |
| 0020 | Lançadores de base com diversidade: lander no Vulcan VC4 (VC6 de reserva), orbitador no Falcon Heavy descartável |

## 5. Limitações
- **Lista de massas:** não há lista publicada por subsistema para um lander de Marte.
  - O núcleo do lander fica de cima para baixo (L3).
  - O caso B pode contar duas vezes energia e telecomunicações próprias do SRL (ADR 0019).
- **Sem massa publicada:** o computador de visão do TRN e o propelente do desvio.
- **Circuito de fluido:** a massa é ordem de grandeza (P-077).
- **Energia:** a sobrevivência acima de τ = 6 só é avaliada pelo dado do Opportunity, que não sobreviveu (ADR 0015).
- **Comunicação:** a extensão das missões do TGO e do MRO até 2030 não foi conferida (ADR 0017).
- **Superfície:** o ritmo do SRH e o pouso de precisão de 200 m são previstos, não voados (ADR 0018).
- **Lançadores:** custo e disponibilidade não avaliados (Fase 6).
- **Rejeição de calor do orbitador:** não estudada à parte; os radiadores estão dentro da plataforma (Etapa 2.3).

## 6. Riscos
1. **Risco principal da Fase 4** (ADR 0018): o plano de superfície depende de uma capacidade não demonstrada em voo, em
   qualquer combinação.
   - Com a precisão de pouso já voada (~1,7 km, Mars 2020), só fecha com o ritmo do SRH, que não voou.
   - Com o ritmo voado do Ingenuity, só fecha com pouso de precisão abaixo de ~300 m, que é previsto, não voado.
   - A linha do tempo está em `results/fase4/resumo.md`.
2. **Dependência de ativo externo** (ADR 0017): o TGO é praticamente ponto único de falha do relé. O ritmo rápido dos
   helicópteros depende de capacidade que os relés existentes não garantem.
3. **MAV perto da assíntota da equação do foguete** (ADR 0007):
   - mitigado pelo lançador maior (ADR 0020);
   - no VC4 a margem fica positiva em todas as sensibilidades, com a pior em +8 % (ε do MAV 0,300, sem fonte).
4. **Orbitador dependente do Falcon Heavy descartável:** o Vulcan VC6 fica negativo em dois casos de sensibilidade
   (`results/etapa2.5/arquitetura.md`). A diversidade do ADR 0020 evita que o lander dependa do mesmo veículo.
5. **Tempestade global:** probabilidade de 25 % na estada (`results/fase4/resumo.md`); risco acima de τ = 6 aceito como
   registrado (ADR 0015).
6. **Pu-238 das RHUs:** a disponibilidade de 61,6 g é risco de programa (ADR 0016).

## 7. Premissas NÃO VALIDADAS
`results/fase4/premissas_nao_validadas.md`, gerado por `tools/lista_premissas.py`:
- todas as 77 premissas estão NÃO VALIDADAS;
- 28 foram criadas na Fase 4 (P-050 a P-077);
- a P-075 (pouso a 200 m do depósito) é crítica.

Só o Fabio altera o status.
