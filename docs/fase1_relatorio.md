# Fase 1: mecânica orbital e orçamento de Δv da missão Terra–Marte–Terra

Estudo conceitual (nível Pré-Fase A) de uma missão **robótica** de ida e volta a Marte. Autor:
Fabio Nogueira. Período: outubro de 2026. Etapas 1.1 a 1.4, PRs #1 a #5.

Este relatório resume a fase e remete aos relatórios de cada etapa, que trazem o detalhe e as
tabelas completas:

| Etapa | Relatório |
| :- | :- |
| 1.1 | `docs/etapa1.1_efemerides.md` |
| 1.2 | `docs/etapa1.2_lambert_porkchop.md`, `docs/etapa1.2_retorno.md` |
| 1.3 | `docs/etapa1.3_missoes.md` |
| 1.4 | `docs/etapa1.4_carga_util.md`, `docs/etapa1.4_dimensionamento.md` |

Todos os números de resultado vêm de arquivos em `results/`, gerados por scripts em `tools/`. As
fontes estão em `docs/fontes.md` (F1–F33) e as decisões nos ADRs 0001–0004.

## 1. Resultado em uma página

| Item | Valor | Onde |
| :- | :- | :- |
| Missão de referência (ADR 0003) | Conjunção de 2028: partida em 23/11/2028, chegada a Marte em 19/09/2029, partida de Marte em 07/11/2030, chegada à Terra em 22/09/2031; 1033 d no total, 414 d em Marte | `results/etapa1.3/missoes.yaml` |
| Órbita em Marte; captura | Elíptica de 1 sol, 250 × 33.793 km [F18]; captura propulsiva (a aerocaptura nunca foi feita em voo [F21]) | ADR 0003 |
| Δv ideal da missão A (impulsivo) | 5,40 km/s | Etapa 1.3 |
| Reentrada da missão A | 12,34 km/s (limite P-011: 12,9 km/s, Stardust [F20]) | Etapa 1.3 |
| Δv de projeto, regra (iii), com perdas, parcelas fixas e margem de 10 % | 7,47 km/s (6,79 sem margem) | `results/etapa1.4/orcamento_dv.md` |
| Carga útil | CU-2: 709,9 kg até a órbita de Marte (captura 620 + cápsula 89,9); 89,9 kg de volta [F23, F24] | `config/carga_util.yaml` |
| Massa na órbita baixa da Terra, regra (iii) | **22,8 t** (faixa da plataforma P-016: 15,2 a 42,6 t) | `results/etapa1.4/dimensionamento.yaml` |
| Massa na órbita baixa só para a missão A | 13,6 t | idem |

## 2. Método

1. **Efemérides** (Etapa 1.1, ADR 0002): JPL DE440, arquivo `de440s.bsp` [F1], via SPICE [F4, F5],
   tempo TDB, frame ICRF/J2000. Marte é representado pelo baricentro do sistema marciano.
2. **Lambert** (Etapa 1.2): algoritmo de Izzo (2015) [F9], com várias revoluções. Testado contra os
   testes oficiais do autor do Vallado (`valladopy` [F12], referência substituta declarada, porque os
   livros não estavam acessíveis) e contra propagação de Kepler analítica [F11].
3. **Porkchops**: grades de 2 dias, C3 de partida e v∞ de chegada, ida 2028–2035 e retorno 2030–2039
   (`tools/porkchop.py`).
4. **Missões completas** (Etapa 1.3): combinação das grades de ida e volta nas classes conjunção e
   oposição. A busca foi testada contra força bruta. O Δv sai de relações de vis-viva a partir de
   órbitas de estacionamento: 407 km na Terra; 500 km circular e 1 sol em Marte [F18]. Também são
   calculadas a DLA e a velocidade de reentrada (interface a 400.000 ft [F19]).
5. **Dimensionamento** (Etapa 1.4): equação do foguete por estágio, com fração estrutural. Saída da
   Terra em LOX/LH2 (RL10A-4-2, 450,5 s; Centaur III, ε = 0,097 [F27]). Estágios de Marte em MMH/MON
   (motor de 400 N, 321 s [F28]; módulo de inserção do ERO, ε = 0,24 [F22]), porque o propelente fica
   ~3 anos a bordo.

## 3. Verificação contra dados publicados

"Verificado" significa comparado com dados publicados. Comparações entre ferramentas ou de ordem de
grandeza vêm rotuladas como tal.

### 3.1 Efemérides contra o JPL Horizons (Etapa 1.1)

Posição heliocêntrica do baricentro de Marte e da Terra, comparada com o Horizons [F3]: |Δr| ≤ 0,03 m.
A comparação verifica o pipeline (frame, escala de tempo, unidades), não a exatidão intrínseca da
DE440.

### 3.2 Ida Terra→Marte contra NASA/TM-2010-216764 (Etapa 1.2)

C3 e v∞ de chegada calculados nas datas impressas nas tabelas "Energy Minima" de Burke, Falck &
McGuire (2010) [F13], com partida no baricentro Terra–Lua
(`results/etapa1.2/verificacao_burke2010.md`):

| Janela | Tipo | C3 NASA (km²/s²) | C3 calculado | Erro abs. | Erro rel. | v∞ NASA (km/s) | v∞ calculado | Erro rel. |
| :- | :- | -: | -: | -: | -: | -: | -: | -: |
| 2028 | I | 9,048 | 9,051 | +0,003 | +0,03 % | 4,892 | 4,892 | +0,01 % |
| 2028 | II | 8,928 | 8,934 | +0,006 | +0,07 % | 3,261 | 3,260 | −0,02 % |
| 2031 | I | 9,00 | 8,999 | −0,001 | −0,01 % | 5,541 | 5,541 | +0,01 % |
| 2031 | II | 8,237 | 8,241 | +0,004 | +0,05 % | 5,53 | 5,529 | −0,03 % |
| 2033 | I | 8,412 | 8,409 | −0,003 | −0,03 % | 3,956 | 3,956 | +0,01 % |
| 2033 | II | 7,781 | 7,783 | +0,002 | +0,02 % | 4,377 | 4,377 | −0,01 % |

Explicação das diferenças:
- **Corpo de partida.** Com partida no centro da Terra, os erros vão até 0,9 %. Os ~12 m/s da Terra
  em torno do baricentro Terra–Lua explicam a diferença. O uso do baricentro Terra–Lua pelo manual é
  uma **convenção inferida, não declarada** por ele. Nos cálculos da missão usa-se o centro da Terra.
- **2035.** A Tabela 6 é inconsistente com as figuras do mesmo documento (pp. 41–42). C3, v∞ e tempo
  de voo são reproduzidos em datas cerca de 63 dias posteriores. Não foi encontrada errata, e a
  janela fica fora do teste (`config/excecoes_verificacao.yaml`).

### 3.3 Retorno Marte→Terra contra JPL Publication 82-43, Part 5 (Etapa 1.2)

Tabelas "ENERGY MINIMA" de 1992 a 2007 [F14], com 32 linhas transcritas e conferidas na imagem da
página. Com chegada no baricentro Terra–Lua: C3L confere em até 0,03 % (13 de 16 linhas) e VHP em até
0,09 % (16 de 16). A efeméride do manual é a DE-118; o efeito medido com a DE200 é ≤ 1,5e-5. Três
linhas ficam fora do teste, com motivo em `config/excecoes_verificacao.yaml`:
- duas a até 1,4° da linha singular de 180°;
- uma com a data de chegada impressa inconsistente com o valor.

Os retornos de 2030 a 2039 são **calculados com o método verificado**, não verificados, porque não
há dado publicado para esse período.

### 3.4 Comparações de ordem de grandeza (não são verificações)

- **DRA 5.0** (Etapa 1.3, `results/etapa1.3/comparacao_dra5.md`):
  - o Δv total das conjunções fica entre 0,82 e 0,96 do valor do DRA;
  - com os mesmos v∞, as fórmulas deste estudo reproduzem os Δv do DRA a 0,003–0,10 km/s, o que
    corresponde às perdas gravitacionais;
  - a diferença vem da trajetória: o DRA usa retornos mais curtos e um v∞ de saída de Marte de
    pior caso.
- **MSR** (Etapa 1.4, `results/etapa1.4/comparacao_msr.md`):
  - massa a caminho de Marte: 7,5 t pela regra (iii), contra ~6,5 t do ERO [F22];
  - o ERO volta com propulsão elétrica (Isp 4000 s); aqui a propulsão é química, que deve dar massa
    maior;
  - só a missão A dá 4,5 t;
  - a plataforma (P-016) domina a incerteza: 5,0 a 14,0 t na faixa entre análogos.

## 4. Orçamento de Δv e massa (Etapa 1.4)

Δv por trecho, em km/s (`results/etapa1.4/orcamento_dv.md`):

| Trecho | Missão A | Projeto, regra (iii) | Fonte das parcelas |
| :- | -: | -: | :- |
| Saída da Terra (ideal + perdas gravitacionais) | 3,735 | 3,735 | Etapa 1.3 + P-015 |
| Correções e atitude na ida | 0,065 | 0,065 | [F18] p. 211 |
| Captura em Marte (ideal + perdas) | 1,077 | 1,362 | Etapa 1.3 + P-015 |
| Encontro e manutenção em órbita de Marte | 0,145 | 0,145 | [F18] p. 211 |
| Saída de Marte (ideal + perdas) | 0,764 | 1,389 | Etapa 1.3 + P-015 |
| Correções e atitude na volta | 0,065 | 0,065 | [F18] p. 211 |
| Desvio do orbitador | 0,019 | 0,031 | P-013 |
| **Total sem margem** | **5,869** | **6,791** | |
| **Total com margem de 10 % (P-014)** | **6,456** | **7,471** | |

Massa na órbita baixa da Terra, regra (iii), caso base: **22,8 t**. Sensibilidade
(`results/etapa1.4/dimensionamento.md`):
- plataforma de 331,8 a 2200 kg: 15,2 a 42,6 t;
- margem de 0 a 20 %: 17,4 a 30,3 t;
- frações estruturais × 0,5 a × 1,5: 15,3 a 43,0 t;
- Isp ±5 %: 26,8 a 19,8 t;
- cápsula +50 %: +3 %;
- CU-2b: −5,8 %.

Figura de Δv total × duração das candidatas: `results/etapa1.3/dv_x_duracao.png`.

## 5. Limitações do modelo

- **Cônicas emendadas:** heliocêntrico entre os centros dos planetas, sem esfera de influência
  explícita nem trajetória planetocêntrica completa.
- **Sem perturbações:** sem outros planetas, pressão de radiação ou assimetria do campo gravitacional.
- **Impulsivo:** manobras instantâneas. As perdas de queima finita entram só como parcelas tiradas do
  DRA (P-015) e na margem (P-014). O motor de 400 N tem empuxo baixo para estas massas, então as
  perdas reais podem ser maiores.
- **Sem mudança de plano para a DLA:** a janela de 2033 tem DLA de −55,5° (Fase 2).
- Sem passagem por Vênus nem frenagem na Terra: a oposição balística fica inviável sob a P-011.
- Aerocaptura ideal, sem modelo térmico e de controle; ela nunca foi demonstrada em voo [F21].
- Plataforma representada por uma massa única (P-016); sem orçamento por subsistema nem margem de
  massa seca.
- Sem lançador e sem descida, pouso ou subida da superfície (Fase 2).

## 6. Premissas NÃO VALIDADAS

Lista gerada de `config/premissas.yaml` em `results/fase1/premissas.md` (`tools/lista_premissas.py`):
16 premissas, todas NÃO VALIDADAS.

| Id | Premissa | Valor |
| :- | :- | :- |
| P-001, P-002 | Tolerâncias de efeméride contra o Horizons | 1 km; 1e-6 km/s |
| P-003, P-004, P-005 | Tolerâncias do Lambert e de Kepler | 1e-10; 1e-8; 1e-8 km/s |
| P-006 | Exclusão de ±1° em torno de 180° na busca de mínimos | 1° |
| P-007, P-008 | Tolerâncias contra NASA/TM-2010-216764 e JPL 82-43 | 0,2 % |
| P-009 | Faixa de permanência na busca da conjunção | 400 a 700 d |
| P-010 | Periapse da passagem de aerocaptura | 50 km |
| P-011 | Velocidade máxima de reentrada (Stardust) | 12,9 km/s |
| P-012 | Faixa de acréscimo na massa da cápsula | 0 a 50 % |
| P-013 | Desvio do orbitador: periapse seguro; antecedência | 300 km; 1 dia |
| P-014 | Margem de Δv | 10 % |
| P-015 | Perdas gravitacionais tiradas do DRA | 148 / 18 / 11 m/s |
| P-016 | Plataforma do orbitador | 850 kg (faixa de 331,8 a 2200) |

## 7. Figuras

- Porkchops de ida (2028, 2031, 2033, 2035) e de retorno (2030, 2032, 2035, 2037, 2039):
  `results/etapa1.2/porkchop_*.png`.
- Δv total × duração das missões candidatas: `results/etapa1.3/dv_x_duracao.png`.
- Tabela de Δv por trecho: `results/etapa1.4/orcamento_dv.md`.

## 8. Decisões (ADRs) e pendências para as próximas fases

- ADR 0001 (estrutura), ADR 0002 (efemérides DE440), ADR 0003 (missão de referência), ADR 0004
  (envelope e regra de estagiamento (iii)).
- **Fase 2:**
  - DLA e inclinação da órbita de estacionamento;
  - troca entre a órbita de 1 sol e o Δv da subida a partir da superfície;
  - descida, pouso e subida.
- **Fase 3:** comparação entre propulsão química e elétrica.
- **Em aberto:**
  - se a massa do CCRS inclui a cápsula (CU-2 contra CU-2b; indício a favor da CU-2b em [F32]);
  - orçamento por subsistema da plataforma;
  - exemplos impressos de Lambert, ainda pulados até conferência no livro.

## Errata (2026-10-27): Etapa 1.4 regenerada
- **Números vigentes:** os de arquitetura são os das Etapas 2.3 a 2.5 (`docs/fase2_relatorio.md`). Os desta fase
  ficam como registro da Fase 1.
- **O que mudou:** os resultados da Etapa 1.4 estavam atrasados em relação à 2033 com |DLA| ≤ 50° (Etapa 2.4) e foram
  regenerados. Mudam só valores da janela de 2033 e da regra (i), que não foi a escolhida. Tabela em
  `docs/etapa1.4_dimensionamento.md`, errata de 2026-10-27.
- **O que não muda:** os números citados neste relatório, da missão A e da regra (iii) (Δv por trecho e 22,8 t).
- **Seção 5:** "a janela de 2033 tem DLA de −55,5°" descreve a 2033 da Fase 1. A atual tem DLA de −49,7°
  (ADR 0004, atualização da Etapa 2.4).
