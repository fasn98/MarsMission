# Etapa 1.3: missões completas Terra→Marte→Terra

Estado: aguardando o portão do Fabio, que escolhe a missão de referência. Nenhuma missão foi
escolhida aqui.

## 1. Método

- **Pares ida+volta.** `src/orbital/missao.py` combina uma grade de ida (partida da Terra × data
  em Marte) com uma grade de volta (data em Marte × chegada à Terra) que compartilham o eixo de
  datas em Marte. As grades são calculadas com o código verificado na Etapa 1.2 (`orbital.lambert`,
  `orbital.porkchop`), com passo de 2 dias, partida e chegada no **centro da Terra** e Marte no
  baricentro. As janelas de ida são as da Etapa 1.2 (2028, 2031, 2033, 2035). As datas em Marte e de
  chegada à Terra cobrem as estadas curtas e as janelas de retorno 2030–2039 da Etapa 1.2
  (`config/missoes.yaml`).
- **Classes** (`config/missoes.yaml`):
  - **oposição:** permanência de 30 a 90 d e duração total ≤ 650 d (DRA 5.0, SP p. 47 [F18]);
  - **conjunção:** permanência de 400 a 700 d (faixa de busca, P-009, NÃO VALIDADA; o DRA fala em
    "500 days or more", p. 47, e 475–540 d, p. 48);
  - **conjunção com trânsitos ≤ 210 d:** como a conjunção, com o limite de trânsito do DRA ("less
    than 180 to 210 days", p. 47).
- **Seleção.** Em cada janela e classe, a trajetória escolhida é a de menor Δv propulsivo com a
  órbita de Marte elíptica de 1 sol e sem aerocaptura (`criterio_selecao`). Os outros casos (órbita
  circular, com aerocaptura) são calculados **para a mesma trajetória**.
  - A busca combinatória foi testada contra força bruta (`tests/test_missao.py`, 36 casos).
  - A faixa de ±1° em torno de 180° (P-006) fica excluída.
  - A resolução é o passo da grade (2 dias), sem refinamento contínuo.
- **Manobras** (`src/orbital/manobras.py`; testes em `tests/test_manobras.py` contra casos-limite e
  Hohmann). São impulsivas e ideais, sem perdas gravitacionais nem mudança de plano:
  - injeção trans-Marte a partir da órbita circular de 407 km;
  - captura em Marte no periapse (propulsiva), ou aerocaptura ideal seguida de elevação do periapse
    no apoapse;
  - injeção trans-Terra no periapse da órbita marciana;
  - reentrada direta na Terra (sem Δv), com a velocidade calculada na interface.
- **Parâmetros** (`config/parametros_orbitais.yaml`):

| Parâmetro | Valor | Fonte |
| :- | :- | :- |
| Órbita baixa da Terra | circular de 407 km | DRA 5.0, SP p. 22 [F18] |
| Marte, circular baixa | circular de 500 km | DRA 5.0, SP p. 54 (alvo do estudo de aerocaptura) [F18] |
| Marte, elíptica alta | 250 × 33.793 km (1 sol) | DRA 5.0, SP p. 22 [F18] |
| Periapse da passagem de aerocaptura | 50 km | **NÃO VALIDADA** (P-010). O DRA ADD2 dá 50 km como mínimo, não como valor de projeto |
| Interface de reentrada na Terra | 121,92 km (400.000 ft) | NASA TN D-6725, p. 8 [F19] |
| Raios equatoriais da Terra e de Marte | 6378,1366 km; 3396,19 km | pck00011.tpc / IAU 2015 [F17] |
| GM da Terra e de Marte | 398600,4355; 42828,3736 km³/s² | gm_de440.tpc [F10] |

## 2. Resultados

Tabelas completas: `results/etapa1.3/missoes.md` e `missoes.yaml`, geradas por `tools/missoes.py`.
Gráfico Δv × duração: `results/etapa1.3/dv_x_duracao.png` (`tools/grafico_missoes.py`). Nenhuma das
12 combinações (4 janelas × 3 classes) tem data na borda do domínio de busca.

Leitura geral:

- **Oposição balística: v∞ na Terra de 11,9 a 15,2 km/s e reentrada a 16 a 19 km/s.** É bem acima
  dos limites de reentrada citados no DRA 5.0 (12 km/s no SP p. 31; 13 a 13,5 km/s no Addendum). As
  missões de oposição do DRA usam passagem por Vênus (SP Fig. 6-2), que não está no modelo. Na
  forma balística deste estudo, a oposição exigiria Δv de frenagem na Terra ou outra arquitetura de
  retorno, não modelados.
- **Conjunção: Δv total de 5,4 a 6,6 km/s** com órbita de 1 sol e captura propulsiva, e de 4,3 a
  5,2 km/s com aerocaptura. Com a órbita circular baixa, o total sobe 2,3 a 2,4 km/s, porque captura
  e saída ficam mais profundas no poço gravitacional.
- **A aerocaptura economiza quase todo o Δv de captura.** O custo residual (elevação do periapse de
  50 km) é de 0,01 km/s na órbita de 1 sol e de 0,10 km/s na circular de 500 km. O DRA reporta média
  de 19 m/s e máximo de 66 m/s depois da aerocaptura (SP p. 54), a mesma ordem. O custo térmico e de
  controle da passagem não está no modelo.

## 3. Candidatas, lado a lado (sem escolha)

Δv em km/s, com órbita de 1 sol. "Prop." = captura propulsiva; "Aero." = com aerocaptura.

| | A: 2028 conjunção | B: 2033 conjunção | C: 2035 conjunção, trânsitos ≤ 210 d | D: 2031 conjunção, trânsitos ≤ 210 d | E: 2033 oposição |
| :- | :- | :- | :- | :- | :- |
| Partida da Terra | 2028-11-23 | 2033-04-16 | 2035-06-28 | 2031-02-18 | 2033-04-08 |
| Chegada a Marte | 2029-09-19 | 2033-11-02 | 2036-01-16 | 2031-09-16 | 2033-10-09 |
| Partida de Marte | 2030-11-07 | 2035-05-06 | 2037-07-07 | 2033-02-01 | 2033-11-08 |
| Chegada à Terra | 2031-09-22 | 2035-11-21 | 2038-01-19 | 2033-08-30 | 2034-07-15 |
| Ida / em Marte / volta (d) | 300 / 414 / 319 | 200 / 550 / 199 | 202 / 538 / 196 | 210 / 504 / 210 | 184 / 30 / 249 |
| Duração total (d) | 1033 | 949 | 936 | 924 | 463 |
| C3 (km²/s²) / DLA (°) | 9,10 / 29,2 | 9,11 / −55,5 | 10,44 / 8,7 | 14,16 / −30,0 | 8,53 / −55,4 |
| v∞ chegada a Marte | 2,97 | 3,32 | 2,62 | 3,87 | 3,66 |
| Δv captura prop. / aero. | 1,06 / 0,01 | 1,25 / 0,01 | 0,89 / 0,01 | 1,58 / 0,01 | 1,45 / 0,01 |
| Δv saída de Marte | 0,75 | 1,05 | 1,52 | 0,78 | 3,74 |
| v∞ na Terra / v reentrada (km/s) | 5,44 / 12,34 | 3,04 / 11,48 | 3,89 / 11,74 | 4,19 / 11,84 | 11,88 / 16,24 |
| **Δv total prop. / aero.** | **5,40 / 4,35** | **5,89 / 4,65** | **6,06 / 5,18** | **6,17 / 4,61** | **8,75 / 7,32** |

Compromissos (fatos do modelo, sem recomendação):

- **A (2028):** menor Δv do conjunto e a missão mais cedo. Também é a mais longa (1033 d), com
  trânsitos de cerca de 300 d. A reentrada de 12,34 km/s passa do limite de 12 km/s do SP do DRA,
  mas fica abaixo dos 13,5 km/s do Addendum. Com trânsitos limitados a 210 d, a janela de 2028 sobe
  para 6,64 km/s, com reentrada de 12,95 km/s.
- **B (2033):** Δv baixo, trânsitos de ~200 d sem precisar de restrição e a menor velocidade de
  reentrada (11,48 km/s). A DLA de −55,5° é a maior em módulo do conjunto. Uma partida no plano de
  uma órbita de estacionamento exige inclinação ≥ |DLA|, então seria preciso uma órbita baixa de alta
  inclinação ou mudança de plano, nenhuma das duas modelada. Para comparar: o DRA usa 34,6° de
  inclinação na missão tripulada de 2033 e 55,3° na carga de 2033 (Addendum, Tabelas 4-2 e 4-3).
- **C (2035):** DLA de 8,7°, que é baixa, e o menor v∞ de chegada a Marte (2,62 km/s), o que importa
  para a captura e para uma eventual entrada atmosférica. A saída de Marte é a mais cara entre as
  conjunções (1,52 km/s), e por isso o Δv total é intermediário. É a janela mais próxima da linha de
  2035 do DRA (seção 4).
- **D (2031):** a conjunção mais curta (924 d), com C3 alto (14,16) e v∞ de chegada a Marte mais alto
  (3,87). Com aerocaptura, o total cai para 4,61 km/s, porque a saída de Marte é barata. DLA de −30°.
- **E (2033, oposição):** menos da metade da duração (463 d), mas com Δv ~50 % maior e reentrada de
  16,2 km/s, fora dos limites citados no DRA. Está aqui só para mostrar o compromisso de classe.
  Na forma balística, não é viável sem frenagem na Terra.

Variantes que aparecem só na tabela completa: 2031 conjunção sem restrição de trânsito (5,78 km/s,
982 d, DLA 14,8°) e 2035 conjunção sem restrição (5,91 km/s, 1014 d).

## 4. Comparação de ordem de grandeza com o DRA 5.0

**Rótulo: comparação de ordem de grandeza, não verificação.** O DRA 5.0 é uma arquitetura tripulada,
com restrições de tripulação (v∞ e trânsitos limitados) e Δv com perdas gravitacionais. Tabela
completa: `results/etapa1.3/comparacao_dra5.md` (`tools/compara_dra5.py`), contra o Addendum,
Tabela 4-2, p. 137.

| Janela | Δv total DRA (soma TMI+MOI+TEI, calculada aqui) | Δv total deste estudo (conjunção, trânsitos ≤ 210 d) | Razão |
| :- | -: | -: | -: |
| 2031 | 7,32 | 6,17 | 0,84 |
| 2033 | 7,18 | 5,89 | 0,82 |
| 2035 | 6,29 | 6,06 | 0,96 |

O SP do DRA dá para a conjunção "average total delta-V … approximately 7 km/s ± 1 km/s" (p. 48).
Os valores deste estudo ficam na mesma ordem, um pouco abaixo.

Explicação das diferenças, separando o modelo de Δv da trajetória:

1. **O modelo de Δv explica pouco.** Aplicando as fórmulas deste estudo aos **mesmos v∞ do DRA**, a
   diferença para o Δv do DRA fica entre 0,003 e 0,10 km/s por manobra, sempre com o DRA maior. É o
   sinal esperado das perdas gravitacionais que o DRA inclui ("All delta-Vs include gravity losses"),
   maiores na injeção trans-Marte (0,07 a 0,10 km/s).
2. **A trajetória explica quase tudo.** O DRA usa retornos mais curtos (133 a 183 d contra 196 a
   210 d aqui) e um v∞ de saída de Marte de 3,847 km/s em todas as linhas. É um valor de pior caso:
   aqui, nas mesmas janelas, o v∞ de saída fica entre 2,40 e 3,78 km/s. Em 2031 e 2033 isso dobra o
   Δv de saída de Marte do DRA (1,573 contra 0,79 e 1,05). Em 2035 as trajetórias são parecidas e a
   razão chega a 0,96.
3. A Tabela 4-1 do Addendum dá "Maximum TEI V∞ 3.487 km/s", mas a Tabela 4-2 traz 3.847 em todas as
   linhas. A inconsistência é da fonte, e não se decide aqui qual valor é o erro tipográfico.

## 5. Premissas novas (NÃO VALIDADAS)

- **P-009:** faixa de permanência de 400 a 700 d na busca da conjunção.
- **P-010:** periapse de 50 km na passagem de aerocaptura.

## 6. Limitações

- Impulsivo ideal, sem perdas gravitacionais (o DRA estima 0,07 a 0,10 km/s na injeção trans-Marte
  para os mesmos v∞).
- Sem mudança de plano: a DLA não é restringida pela inclinação da órbita de estacionamento.
- Aerocaptura ideal, sem modelo térmico ou de controle.
- Sem passagem por Vênus e sem frenagem na Terra.
- Resolução de datas de 2 dias, sem refinamento.
- A seleção da trajetória usa um único critério (`config/missoes.yaml`); outro critério pode escolher
  outras datas na mesma janela.
- O cenário do estudo é robótico. Os limites de reentrada e de trânsito do DRA são de missão
  tripulada e servem aqui só como referência.
