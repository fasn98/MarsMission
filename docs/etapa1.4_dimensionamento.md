# Etapa 1.4, Parte B: orçamento de Δv e primeiro dimensionamento

Estado: aguardando o portão do Fabio, que escolhe a regra final do envelope (ADR 0004). Parte A
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
(`tests/test_foguete.py`). A cápsula é solta antes do desvio. Na CU-1, o módulo descartado em Marte
sai antes da partida de Marte. Caso base: CU-2, margem de 10 %, sem acréscimo na cápsula.

| Caso | Regra | Massa na órbita baixa da Terra | Massa depois da injeção trans-Marte |
| :- | :- | -: | -: |
| Missão A | os três estágios pela missão A | **6.180 kg** | 2.036 kg |
| **(i)** | saída da Terra com estágio próprio + um só estágio armazenável para captura e retorno; cada janela com a sua missão; projeto pela pior janela | **10.352 kg** (define: 2033) | 3.409 kg |
| **(ii)** | cada estágio pelo pior caso do seu trecho | **10.629 kg** | 3.420 kg |
| **(iii)** | estágios de Marte pelo pior caso; saída da Terra pela janela de referência (A) | **10.381 kg** | 3.420 kg |

Leitura:

- As três regras dão massas parecidas: 10,35 a 10,63 t, uma faixa de 3 %. Todas ficam ~70 % acima
  da missão A, porque precisam cobrir as janelas de 2031 a 2035, com captura (até 1,36 km/s) e
  saída de Marte (até 1,39 km/s) mais caras que as da janela de 2028.
- Na (i), a janela que define a massa é **2033**, não 2035 (a de maior Δv total). Com o estágio de
  Marte único, a distribuição do Δv entre os trechos pesa mais que o total.
- A (iii) fica 2,3 % abaixo da (ii). A diferença vem só da saída da Terra (3,735 contra 3,806 km/s),
  o trecho de menor Isp relativo ao Δv.
- A (i) é a mais sensível à fração estrutural: com ε × 1,5 passa a 41 t, perto de ficar inviável,
  porque o estágio único leva o inerte da captura até o fim da missão.

## 4. Sensibilidade da massa na órbita baixa

Tabela completa: `results/etapa1.4/dimensionamento.md`. Faixas em kg (missão A | variante ii):

| Parâmetro | Faixa testada | Missão A | (ii) |
| :- | :- | :- | :- |
| Margem de Δv (P-014) | 0 a 20 % | 4.990 a 7.692 | 8.070 a 14.124 |
| Isp de todos os estágios | −5 % a +5 % | 7.010 a 5.521 | 12.516 a 9.191 |
| Frações estruturais | × 0,5 a × 1,5 | 4.671 a 9.243 | 7.089 a 20.129 |
| Acréscimo na cápsula (P-012) | 0 a 50 % | 6.180 a 6.568 | 10.629 a 11.293 |
| Carga útil | CU-3 / CU-2b / CU-1 / CU-2 | 799 / 5.396 / 6.292 / 6.180 | 1.368 / 9.280 / 10.264 / 10.629 |

Pontos de atenção:

- **A cápsula mais rápida (12,34 contra 12,0 km/s) pesa pouco.** Até +50 % na massa da cápsula
  muda a massa total em +6 % (P-012; sem lei de escala, como decidido).
- **A margem e a fração estrutural dominam.** Margem de 20 % e ε × 1,5 aumentam a massa entre 25 e
  90 %, conforme o caso.
- **Possível contagem dupla na CU-2.** Martin-Mur et al. (ISSFD 2024, p. 5 [F32]) descrevem o
  "CCRS, including the Earth Entry System (EES)". Se os 620 kg do CCRS [F23] já incluírem a cápsula,
  a CU-2 conta a cápsula duas vezes. Na leitura alternativa (CU-2b), todas as massas caem 12,7 %.
  Nenhuma fonte diz isso explicitamente, e o caso base mantém a soma (conservador).

## 5. Comparação de ordem de grandeza com o MSR

**Rótulo: comparação de ordem de grandeza, não verificação.** Tabela: `results/etapa1.4/comparacao_msr.md`
(`tools/compara_msr.py`).

| | ERO (MSR) | Este estudo: missão A | Este estudo: (ii) |
| :- | -: | -: | -: |
| Massa a caminho de Marte | ≈ 6.500 kg úmida [F22] (7.200 kg em 2023 [F29]) | 2.036 kg | 3.420 kg |
| Módulo de inserção em Marte (seco + propelente) | 2.500 kg [F22] | 882 kg | 1.767 kg |

Explicação das diferenças:

1. **Propulsão.** O ERO volta com propulsão elétrica (Isp 4000 s; 1100 kg de xenônio; "ΔV 10 km/s"
   [F22]). Aqui toda a propulsão é química, e por isso a massa química calculada aqui deve ser
   **maior** que a de um sistema elétrico equivalente, não menor. A comparação química × elétrica
   fica para a Fase 3.
2. **Plataforma do orbitador ausente: o principal motivo de os valores daqui ficarem abaixo dos do
   ERO.** Este modelo não tem a massa da plataforma (energia, aviônica, comunicação, controle
   térmico, GNC). A carga útil é só a captura e a cápsula, e ε cobre só os módulos propulsivos. Para
   comparar: o módulo principal do ERO tem 2200 kg secos [F22], com painéis de 41 kW para a
   propulsão elétrica. A massa seca da Mars Odyssey, um orbitador químico, foi de 331,8 kg sem
   instrumentos [F33].
3. **Trajetória.** O ERO faz uma espiral de baixo empuxo com outro perfil de Δv. Aqui o Δv é
   impulsivo.

## 6. Pendências e premissas novas

- **Regra final do envelope:** escolher entre (i), (ii) e (iii); o ADR 0004 será atualizado.
- **Plataforma do orbitador:** decidir se entra uma massa de plataforma (com fonte ou como premissa)
  já nesta fase, ou na Fase 2/3.
- **CU-2 contra CU-2b:** decidir se os 620 kg incluem a cápsula.
- **Premissas novas (NÃO VALIDADAS):**
  - P-012: faixa de acréscimo na cápsula;
  - P-013: parâmetros do desvio;
  - P-014: margem de Δv de 10 %;
  - P-015: perdas gravitacionais tiradas do DRA.

## 7. Limitações

- Manobras impulsivas; sem queima finita (o motor de 400 N tem empuxo baixo para estas massas). As
  perdas entram só pela P-015 e pela margem.
- Sem plataforma do orbitador, sem margem de massa seca, sem propelente residual nem de controle de
  atitude além dos 15 m/s por trecho.
- O ε do Centaur III vem de um estágio de lançador. Um estágio de saída para esta massa seria muito
  menor, e o ε real tende a ser maior.
- Sem mudança de plano para a DLA (Fase 2) e sem cálculo de lançador.
