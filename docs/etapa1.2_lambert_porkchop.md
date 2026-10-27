# Etapa 1.2: Lambert e porkchop plots

Estado: parte Terra→Marte aprovada no portão de 2026-10-27. O retorno Marte→Terra é feito no branch seguinte (ver seção 4).

## 1. Solver de Lambert

`src/orbital/lambert.py` implementa o algoritmo de Izzo (2015), docs/fontes.md [F9]. Os números de
equação citados no código foram conferidos no preprint arXiv:1403.2705. O solver suporta várias
revoluções: até M_max, com dois ramos por M, como no Algoritmo 2 do artigo.

Testes (`tests/test_lambert.py`):

| Teste | Referência | Resultado |
| :- | :- | :- |
| 5 casos com 0 e 1 revolução, caminhos curto e longo | Testes oficiais do pacote `valladopy`, publicados pelo autor do livro [F12]. É o código de referência do autor, não a página do livro. | Passa. Diferença de 2,5e-9 km/s em todos os casos; tolerância P-005 |
| Vallado, Example 7-5 (impresso) | Livro: edição, página e resposta **não confirmadas** | **Pulado** |
| Curtis, Example 5.2 (impresso) | Livro: edição, página e resposta **não confirmadas**; entradas confirmadas no script do autor | **Pulado** |
| Propriedade física: Lambert seguido de propagação de Kepler analítica | Kepler por variável universal [F11], em `src/orbital/kepler.py` | Passa. 850 casos com M = 0, 1 e 2, sem exclusões; pior erro 6,2e-12; tolerância P-003 |

Exemplos impressos em livro: os livros não estavam acessíveis, e nenhuma página foi citada sem ser
vista. Por decisão do Fabio no portão de 2026-10-27, os testes oficiais do `valladopy` são a
**referência substituta declarada**. Os dois exemplos impressos continuam em
`tests/data/lambert_livros.yaml`, pulados com o motivo, até que alguém confira no exemplar.

`src/orbital/kepler.py` (propagação de Kepler analítica) tem testes próprios em
`tests/test_kepler.py`: comparação com integração numérica (P-004), conservação de energia e de
momento angular, e ida e volta no tempo.

## 2. Verificação Terra→Marte contra NASA/TM-2010-216764

O manual de referência é Burke, Falck & McGuire (2010) [F13]. Comparei as linhas de C3 mínimo por
tipo das tabelas "Energy Minima" (tabelas 3 a 6). A condição é a mesma do manual: balístico,
cônicas emendadas, sem manobra no espaço profundo, grade de 2 dias.

O manual **não declara** a efeméride nem o corpo de partida. Por isso calculei com dois corpos de
partida: o centro da Terra (399) e o baricentro Terra–Lua (3). As tabelas completas, com erro
absoluto e relativo, estão em `results/etapa1.2/verificacao_burke2010.md`, gerado por
`tools/verifica_burke2010.py`.

### 2.1 Resumo: C3 e v∞ calculados nas datas impressas no manual

| Janela | Tipo | C3 NASA | C3 (partida 3) | Erro rel. | C3 (partida 399) | Erro rel. | v∞ NASA | v∞ (partida 3) | Erro rel. |
| :- | :- | -: | -: | -: | -: | -: | -: | -: | -: |
| 2028 | I | 9.048 | 9.051 | +0,03 % | 9.029 | −0,21 % | 4.892 | 4.892 | +0,01 % |
| 2028 | II | 8.928 | 8.934 | +0,07 % | 8.999 | +0,80 % | 3.261 | 3.260 | −0,02 % |
| 2031 | I | 9.00 | 8.999 | −0,01 % | 8.976 | −0,27 % | 5.541 | 5.541 | +0,01 % |
| 2031 | II | 8.237 | 8.241 | +0,05 % | 8.171 | −0,81 % | 5.53 | 5.529 | −0,03 % |
| 2033 | I | 8.412 | 8.409 | −0,03 % | 8.413 | +0,01 % | 3.956 | 3.956 | +0,01 % |
| 2033 | II | 7.781 | 7.783 | +0,02 % | 7.709 | −0,93 % | 4.377 | 4.377 | −0,01 % |
| 2035 | I | 10.19 | 34.65 | +240 % | 34.67 | +240 % | 2.692 | 4.375 | +63 % |
| 2035 | II | 17.52 | 45.44 | +159 % | 45.29 | +158 % | 4.063 | 4.695 | +16 % |

### 2.2 Explicação das diferenças

1. **Corpo de partida (2028–2033).** Com partida no baricentro Terra–Lua, C3 e v∞ batem com o
   manual em até 0,07 %. Isso é compatível com os 3 a 4 algarismos impressos e com a grade de 2
   dias. Com partida no centro da Terra, o C3 difere até 0,9 %. A diferença tem causa física
   conhecida: a Terra se move cerca de 12 m/s em torno do baricentro Terra–Lua, e isso altera
   v∞,partida em até ~0,012 km/s. Como C3 = v∞², o efeito no C3 é de ~2·v∞·δv ≈ 0,07 km²/s², a
   ordem observada. **Convenção INFERIDA, não declarada pelo manual:** o manual usou o baricentro Terra–Lua (ou uma efeméride
   em que a Terra coincide com ele). O documento não diz isso. Para a missão, o fisicamente correto
   é partir do centro da Terra, e os porkchops usam 399.
2. **v∞ de chegada nos mínimos próprios.** A tabela (a) do arquivo de resultados compara o mínimo de
   C3 encontrado aqui com o do manual. As datas coincidem com as do manual a menos de 2 dias, mas o
   v∞ de chegada difere até 3 % com partida 399 e até 0,4 % com partida 3. O motivo é que o mínimo
   de C3 fica num vale raso: deslocar a data de chegada em poucos dias quase não muda o C3, mas muda
   o v∞. Avaliado nas mesmas datas do manual, o v∞ bate em até 0,03 % (tabela acima).
3. **2035: Tabela 6 inconsistente com as figuras do mesmo documento (pp. 41–42).** Os valores de
   C3, v∞ e tempo de voo da Tabela 6 são reproduzidos aqui, mas em datas cerca de 63 dias
   posteriores às impressas na tabela:

   | 2035 | Datas da Tabela 6 | Datas do mínimo próprio (partida 3) | C3 tabela / próprio | v∞ tabela / próprio | TOF tabela / próprio |
   | :- | :- | :- | :- | :- | :- |
   | Tipo I | 21/04/35 → 03/11/35 | 23/06/35 → 04/01/36 | 10.19 / 10.194 | 2.692 / 2.697 | 196 / 195,5 d |
   | Tipo II | 12/06/35 → 28/07/36 | 15/08/35 → 04/10/36 | 17.52 / 17.525 | 4.063 / 4.098 | 412 / 416,7 d |

   As figuras de 2035 do mesmo documento (pp. 41–42) mostram a bacia de mínimo do Tipo I perto da
   partida em ~28/06/35 e da chegada em ~02/01/36. Essa posição é coerente com as datas calculadas
   aqui e não com as da Tabela 6. É uma leitura visual da figura, sem extração numérica. Não se
   afirma aqui qual das duas está certa. A janela de 2035 fica fora do teste automático, pela lista
   explícita `config/excecoes_verificacao.yaml`.

   **Busca por errata (2026-10-27):** o registro NTRS 20100037210 tem um único documento (PDF
   original), sem itens relacionados nem versão revisada. A busca na web por errata ou revisão do
   NASA/TM-2010-216764 não encontrou nada. Resultado: nenhuma errata ou versão revisada encontrada.
4. **Linha de 180°.** Sem tratamento especial, o mínimo "Tipo II" de 2035 (partida 399) caiu
   exatamente em 180,0°. Nesse ponto o plano da transferência é mal definido, e é onde as curvas
   do gráfico do manual convergem. A busca de mínimos agora exclui ±1° em torno de 180° (premissa
   P-006, NÃO VALIDADA). O manual não diz como trata esse caso.

## 3. Porkchop plots

`results/etapa1.2/porkchop_terra_marte_<ano>.png` (2028, 2031, 2033, 2035), gerados por
`tools/porkchop.py terra_marte`. Mostram curvas de C3 de partida (azul), v∞ de chegada (laranja
tracejado) e tempo de voo (cinza pontilhado). Os mínimos próprios por tipo aparecem como marcadores
cheios e os do manual como marcadores vazados. Desde 2026-10-27 a faixa de ±1° em torno de 180°
(P-006) é mascarada no desenho, com nota de rodapé; os contornos se limitam a C3 ≤ 20 km²/s² e
v∞ ≤ 6 km/s; os números usam vírgula decimal. Partida no centro da Terra; chegada no baricentro de
Marte. Domínios de busca em `config/janelas.yaml`.

## 4. Retorno Marte→Terra: fontes publicadas (antes de calcular)

Pesquisa feita em 2026-10-27. Nenhuma fonte publicada encontrada **tabela retornos balísticos de
energia mínima com partida de Marte em 2029–2040**.

| Fonte | Período | O que traz | Serve para verificar 2029–2040? |
| :- | :- | :- | :- |
| George & Kos, *Interplanetary Mission Design Handbook: Earth-to-Mars Mission Opportunities and Mars-to-Earth Return Opportunities 2009–2024*, NASA/TM-1998-208533 (NTRS 19980210557) | partidas de Marte até 02/10/2026 | Retornos tripulados com tempo de voo restrito a ~180 d (não é energia mínima): ΔV de injeção trans-Terra, v∞ em Marte e na Terra | Não (termina em 2026 e é restrito) |
| Sergeyevsky & Cunniff, *Interplanetary Mission Design Handbook, Vol. I, Part 5: Mars-to-Earth Ballistic Mission Opportunities, 1992–2007*, JPL Publication 82-43 (NTRS 19880009154) | 1992–2007 | Porkchops balísticos de retorno (C3 em Marte, v∞ na Terra) | Não (período). Serviria para testar o método num ano antigo |
| Young, Mulqueen & Skinner, *Mars Exploration, Venus Swingby and Conjunction Class Mission Modes, Time Period 2000 to 2045*, NASA-TM-86477, 1984 (NTRS 19850003653), Tabela 22, p. 57 | 2031–2044 | Missões de ida e volta da classe conjunção otimizadas como um todo; v∞ em unidades de velocidade orbital média da Terra; efemérides de 1984 | Só como comparação de ordem de grandeza: não é tabela de retorno de energia mínima |
| Joffre et al., *Mars Sample Return: Mission Analysis for an ESA Earth Return Orbiter* (ICATT) | 2026–2030 | Porkchops e um retorno exemplo (partida de Marte 26/09/2028) | Não (período e um único ponto) |

Decisão do Fabio (2026-10-27): verificar o método contra o JPL 82-43 Parte 5 num ano coberto
por ele e depois calcular os retornos de 2029–2040 com o mesmo código. A comparação com o GMAT
fica adiada para fases futuras.

## 5. Premissas novas (todas NÃO VALIDADAS)

P-003 a P-007 em `config/premissas.yaml`, aprovadas no portão de 2026-10-27 e mantidas como NÃO VALIDADA: tolerâncias de teste (P-003, P-004, P-005, P-007) e
exclusão de ±1° em torno de 180° na busca de mínimos (P-006).

## 6. Limitações do modelo

Cônicas emendadas, manobras impulsivas, sem perturbações, sem manobra no espaço profundo. A chegada
é no baricentro de Marte. O C3 é medido em relação ao corpo de partida escolhido, sem modelar a
órbita de estacionamento (isso fica para a Etapa 1.3).
