# Etapa 1.4, Parte B: orçamento de Δv e primeiro dimensionamento

Estado: portão da Parte B feito em 2026-10-27. Regra de projeto (iii) (ADR 0004); plataforma do orbitador incluída (P-016). Parte A
(carga útil): `docs/etapa1.4_carga_util.md`.

**Escopo:** só os trechos no espaço, ou seja, saída da órbita baixa da Terra, captura em Marte,
saída de Marte e chegada à Terra. **Descida, pouso, operações de superfície e subida ficam para a
Fase 2.**

## 1. Escolhas e premissas

**Carga útil:** CU-2, decisão do Fabio. São 709,9 kg até a órbita de Marte (captura 620 kg + cápsula
89,9 kg) e 89,9 kg de volta à Terra. A CU-1 e a CU-3 entram na sensibilidade
(`config/carga_util.yaml`).

**Propelente por trecho**, o mesmo nas três variantes (`config/dimensionamento.yaml`):

| Trecho | Propelente | Isp | Fração estrutural ε | Fontes |
| :- | :- | -: | -: | :- |
| Saída da Terra | LOX/LH2 (criogênico) | 450,5 s (RL10A-4-2) | 0,0972 (Centaur III de motor único: 2243 kg inertes, 20.830 kg de propelente; ε calculado aqui) | [F27] ULA, guia do Atlas V, p. 1-5 |
| Captura em Marte e retorno | MMH/MON (armazenável) | 321 s (motor de 400 N da ArianeGroup, ponto nominal) | 0,24 (módulo de inserção do ERO: 600 kg secos, 1900 kg de propelente; ε calculado aqui) | [F28], [F22] |

- **Por que armazenável em Marte:** o propelente fica guardado por ~3 anos (a missão A dura
  1033 d). O mesmo motor de 400 N voou na Mars Express (2003) e no ExoMars Orbiter (2016) [F28], e
  o módulo de inserção do ERO usa "2 x 400 N" [F29].
- **ε de referência:** o Fregat dá ε = 0,12 [F30], metade do valor usado. A sensibilidade cobre
  ε × 0,5 e × 1,5.
- **g0** = 9,80665 m/s² (3ª CGPM, 1901; NIST SP 330, p. 46 [F31]).

**Parcelas de Δv somadas ao Δv ideal da Etapa 1.3:**

| Parcela | Valor | Fonte ou premissa |
| :- | -: | :- |
| Correção de trajetória, por trecho | 50 m/s | DRA 5.0 Addendum, Tabela 5-15, p. 211 [F18] |
| Controle de atitude em cruzeiro, por trecho | 15 m/s | idem |
| Encontro em órbita de Marte | 45 m/s | idem ("Mars orbit rendezvous with lander") |
| Manutenção de órbita em Marte | 100 m/s | idem |
| Perdas gravitacionais: saída da Terra, captura, saída de Marte | 148, 18 e 11 m/s | diferença com/sem perdas no DRA, p. 211; aplicabilidade é a **P-015, NÃO VALIDADA** |
| Desvio do orbitador depois de soltar a cápsula | 19 a 31 m/s, conforme o v∞ na Terra | plano B, γ = −25° [F24]; periapse seguro de 300 km e 1 dia de antecedência (**P-013, NÃO VALIDADA**) |
| **Margem sobre todos os trechos** | **10 %** | **P-014, NÃO VALIDADA** |

## 2. Orçamento de Δv por trecho

Tabela completa: `results/etapa1.4/orcamento_dv.md`, gerada por `tools/dimensionamento.py`.

| | Missão A | Pior janela pelo total (2035) | Pior caso de cada trecho |
| :- | -: | -: | -: |
| Total sem margem (km/s) | 5,869 | 6,389 | 6,862 |
| Total com margem de 10 % (km/s) | 6,456 | 7,028 | 7,549 |

Os 5,91 e 6,38 km/s do ADR 0004 são só os Δv ideais. Os valores acima incluem as parcelas da
tabela anterior.

## 3. Dimensionamento: missão A e as três regras de envelope

Equação do foguete por estágio (`src/orbital/foguete.py`), testada contra a forma fechada
(`tests/test_foguete.py`).
- A cápsula é solta antes do desvio; na CU-1, o módulo descartado em Marte sai antes da partida de
  Marte.
- A **plataforma do orbitador** (P-016, 850 kg) fica com o orbitador até o fim.
- Caso base: CU-2, margem de 10 %, sem acréscimo na cápsula.

| Caso | Regra | Massa na órbita baixa da Terra | Massa depois da injeção trans-Marte |
| :- | :- | -: | -: |
| Missão A | os três estágios pela missão A | 13.587 kg | 4.476 kg |
| (i) | saída da Terra própria + um só estágio para captura e retorno; projeto pela pior janela (2033) | 22.768 kg | 7.499 kg |
| (ii) | cada estágio pelo pior caso do seu trecho | 23.378 kg | 7.522 kg |
| **(iii), regra de projeto (ADR 0004)** | **saída da Terra pela janela da missão A; captura (descartada em Marte) e retorno pelo pior caso de cada trecho** | **22.833 kg** | **7.522 kg** |

- A (iii) foi escolhida no portão da Parte B. O estágio de saída da Terra é montado para cada
  lançamento, e a (i) é frágil à fração estrutural: com ε × 1,5 vai a 90 t (ADR 0004).
- Na (i), a janela que define a massa é 2033, não 2035 (a de maior Δv total). Com o estágio de Marte
  único, a distribuição do Δv entre os trechos pesa mais que o total.

## 4. Plataforma do orbitador (P-016)

| | Valor | Fonte |
| :- | -: | :- |
| Limite inferior: Mars Odyssey, massa seca sem instrumentos | 331,8 kg | [F33] |
| Limite superior: módulo principal do ERO, massa seca | 2200 kg | [F22] |
| **Base: ≈ média geométrica dos dois limites, arredondada** | **850 kg** | **P-016, NÃO VALIDADA** |

Justificativa da base:
- A faixa cobre um fator de 6,6, e não há análogo direto: um orbitador químico que captura uma carga
  em órbita.
- A Odyssey não levava sistema de captura nem sensores de encontro, que o CCRS de 2021 não inclui
  ("w/o RSS" [F22]).
- O módulo do ERO inclui propulsão elétrica e painéis de 41 kW, desnecessários num orbitador químico.
  Como a fração estrutural já cobre os módulos propulsivos, o limite superior conta parte da
  propulsão duas vezes.
- O centro em escala logarítmica é a escolha neutra entre os dois.

Efeito na regra (iii): 15,2 t com 331,8 kg, 22,8 t com 850 kg e 42,6 t com 2200 kg. **A plataforma
passou a ser o parâmetro de maior efeito**, junto com a margem e a fração estrutural.

## 5. Sensibilidade da massa na órbita baixa

Tabela completa: `results/etapa1.4/dimensionamento.md`. Faixas em kg:

| Parâmetro | Faixa testada | Missão A | (iii) |
| :- | :- | :- | :- |
| Plataforma (P-016) | 331,8 a 2200 kg | 9.071 a 25.352 | 15.242 a 42.611 |
| Margem de Δv (P-014) | 0 a 20 % | 10.970 a 16.913 | 17.383 a 30.257 |
| Frações estruturais | × 0,5 a × 1,5 | 10.268 a 20.326 | 15.277 a 43.049 |
| Isp de todos os estágios | −5 % a +5 % | 15.413 a 12.140 | 26.845 a 19.773 |
| Acréscimo na cápsula (P-012) | 0 a 50 % | 13.587 a 13.975 | 22.833 a 23.483 |
| Carga útil | CU-3 / CU-2b / CU-1 / CU-2 | 8.206 / 12.804 / 13.699 / 13.587 | 13.788 / 21.516 / 22.477 / 22.833 |

- **A cápsula mais rápida (12,34 contra 12,0 km/s) pesa pouco.** Até +50 % na massa da cápsula dá
  +3 % na massa total (P-012; sem lei de escala, como decidido).
- **CU-2 contra CU-2b:**
  - a CU-2 continua sendo a base (decisão do Fabio);
  - a frase de Martin-Mur et al. (ISSFD 2024, p. 5 [F32]), "Capture, Containment, and Return System
    (CCRS), including the Earth Entry System (EES)", é **um indício a favor da CU-2b**, ou seja, de
    que os 620 kg [F23] já incluiriam a cápsula. A questão será revisada se surgir fonte mais clara;
  - na CU-2b, a massa da (iii) cai 5,8 %.

## 6. Comparação de ordem de grandeza com o MSR

**Rótulo: comparação de ordem de grandeza, não verificação.** Tabela: `results/etapa1.4/comparacao_msr.md`
(`tools/compara_msr.py`).

| | ERO (MSR) | Missão A | (iii) |
| :- | -: | -: | -: |
| Massa a caminho de Marte | ≈ 6.500 kg úmida [F22] (7.200 kg em 2023 [F29]) | 4.476 kg | 7.522 kg |
| Módulo de inserção em Marte (seco + propelente) | 2.500 kg [F22] | 1.938 kg | 3.886 kg |

Explicação das diferenças:

1. **Propulsão.** O ERO volta com propulsão elétrica (Isp 4000 s; 1100 kg de xenônio [F22]). Aqui
   toda a propulsão é química, então a massa química deve ser **maior** que a de um sistema elétrico
   equivalente. Com a plataforma incluída, é o que acontece na regra (iii): 7,5 t contra 6,5 t. A
   comparação química × elétrica fica para a Fase 3.
2. **Envelope contra missão única.** A (iii) cobre as janelas de 2028 a 2035. Só a missão A fica em
   4,5 t, abaixo do ERO, porque a janela de 2028 tem a captura e a saída de Marte mais baratas.
3. **Plataforma.** A massa de 850 kg é premissa (P-016). Com a faixa inteira, a (iii) vai de 5,0 a
   14,0 t a caminho de Marte. A ordem de grandeza do ERO fica dentro dela.
4. **Trajetória.** O ERO faz espirais de baixo empuxo, com outro perfil de Δv. Aqui o Δv é impulsivo.
5. **Massa na órbita baixa.** O ERO seria lançado num Ariane 64 [F32] e não tem estágio de saída da
   Terra próprio. Os 22,8 t da (iii) incluem esse estágio.

## 7. Premissas desta parte (todas NÃO VALIDADAS)

- **Aprovadas no portão da Parte B:**
  - P-012: faixa de acréscimo na cápsula;
  - P-013: parâmetros do desvio;
  - P-014: margem de Δv de 10 %;
  - P-015: perdas gravitacionais tiradas do DRA.
- **Nova:** P-016, plataforma do orbitador de 850 kg (faixa de 331,8 a 2200 kg).

## 8. Limitações

- Manobras impulsivas; sem queima finita (o motor de 400 N tem empuxo baixo para estas massas). As
  perdas entram só pela P-015 e pela margem.
- Plataforma representada por uma massa única (P-016), sem orçamento por subsistema e sem margem de
  massa seca.
- O ε do Centaur III vem de um estágio de lançador. Um estágio de saída para esta massa seria menor,
  e o ε real tende a ser maior.
- Sem mudança de plano para a DLA (Fase 2) e sem cálculo de lançador.

## Nota (Etapa 2.4, 2026-10-27): 2033 com |DLA| ≤ 50°
- A janela de 2033 passou a ter |DLA| ≤ 50° (ADR 0004, atualização da Etapa 2.4).
- A regra (i) desta etapa tinha 2033 como janela que define e usou a trajetória antiga (saída da Terra
  3,5873 km/s). A nova tem 3,6088 km/s, então o valor da regra (i) aqui fica um pouco abaixo do atual.
- Os resultados desta etapa não foram regenerados (também usam a plataforma de 850 kg da época).
- A regra (iii), a escolhida, não muda.

## Errata (2026-10-27): resultados desta etapa regenerados com a 2033 atual
**Os números de arquitetura vigentes são os das Etapas 2.3 a 2.5** (`docs/etapa2.3_plataformas.md`,
`docs/etapa2.4_lancamento.md`, `docs/fase2_relatorio.md`). Esta etapa usou a plataforma do orbitador de 850 kg e o
lançamento a partir da órbita baixa com estágio próprio, ambos substituídos depois. Os números abaixo corrigem só a
reprodutibilidade dos arquivos desta etapa; nenhum deles é vigente.

**O que estava errado.** Os arquivos de `results/etapa1.4/` foram gerados em 2026-10-26 (commit 60683bb). Na Etapa 2.4,
a missão de 2033 mudou para |DLA| ≤ 50° e `results/etapa1.3/missoes.yaml` foi regenerado (commit 286c1c1); os
arquivos desta etapa, não. A verificação de regeneração (`tools/confere_regeneracao.py`) mostrou que eles não saíam
do código e do config da `main`.

**Correção.** Os quatro arquivos (`dimensionamento.yaml` e `.md`, `orcamento_dv.md`, `comparacao_msr.md`) foram
regenerados com a mesma rotina, na ordem histórica, com a plataforma da época (850 kg) e a 2033 atual
(`results/conferencia/regeneracao_reprodutibilidade_1.4.md`). Valores que mudam, todos da janela de 2033 ou da regra (i):

| Grandeza | Antes (texto original acima) | Regenerado |
| :- | -: | -: |
| Δv saída da Terra, jan. 2033 (ideal + perdas) | 3,735 km/s | 3,757 km/s |
| Δv captura em Marte, jan. 2033 | 1,266 km/s | 1,268 km/s |
| Δv total jan. 2033, sem / com margem | 6,372 / 7,009 km/s | 6,395 / 7,034 km/s |
| Regra (i): massa na órbita baixa | 22.768 kg | 22.953 kg |
| Regra (i): massa depois da injeção trans-Marte | 7.499 kg | 7.506 kg |
| Regra (i) com ε × 1,5 (sensibilidade) | 90.213 kg | 91.351 kg |

- **Não mudam:** a missão A, a regra (ii) e a regra (iii), que foi a escolhida (ADR 0004). A sensibilidade da (iii) e a
  comparação com o MSR também ficam iguais, exceto a coluna da (i).
- **Afirmação da seção 3 que deixa de valer:** "Na (i), a janela que define a massa é 2033, não 2035 (a de maior Δv
  total)". Com a 2033 atual, 2033 passa a ter também o maior Δv total (6,395 contra 6,389 km/s de 2035).
- **Substitui** a "Nota (Etapa 2.4)" acima, que dizia que os resultados desta etapa não tinham sido regenerados.
