# Etapa 1.2 (continuação): retorno Marte→Terra

Estado: aprovado no portão de 2026-10-27; fecha com o merge do PR #3. Decisão anterior
(2026-10-27): verificar o método contra o JPL 82-43 Parte 5 num ano coberto por ele; depois
calcular 2029–2040 com o mesmo código. GMAT adiado.

## 1. Fonte de verificação

Sergeyevsky & Cunniff, JPL Publication 82-43, Vol. I, Part 5, *Mars-to-Earth Ballistic Mission
Opportunities, 1992–2007* (1987), docs/fontes.md [F14].

- **O manual tem tabelas numéricas.** Além dos gráficos de contorno, cada oportunidade de 1992 a
  2007 tem uma tabela "ENERGY MINIMA" com o mínimo de C3L (partida de Marte) e o mínimo de VHP
  (v∞ de chegada à Terra) por tipo, com datas. A verificação usa essas tabelas, 32 linhas ao todo.
  **Não é leitura de gráfico.** A ressalva de "precisão limitada" não se aplica aos números; a
  leitura visual entrou só como conferência da transcrição (próximo item).
- **Transcrição.** O PDF do NTRS é um escaneamento, e o texto obtido por OCR tem erros: em 1992 o
  OCR leu "12.961" e "9.136", mas a imagem mostra **12.981** e **9.138**. Todos os valores de
  `tests/data/jpl8243p5_minimos.yaml` foram conferidos na imagem da página.
- **Efeméride do manual: DE-118**, declarada na Seção IV ("Table of Constants"). O NAIF não
  distribui a DE118. A DE200 é a DE118 girada para J2000 (Standish, 1990 [F15]; afirmação conferida
  no resumo do registro NTRS, texto completo não lido). C3L e VHP são normas e não dependem
  da rotação, então a DE200 representa a DE118 aqui.
- **Tolerância esperada por causa da efeméride:** medida, não suposta. Trocar a DE440 pela DE200
  nas 32 linhas muda C3L e VHP em **no máximo 1,5e-5 relativo** (0,0015 %), e em menos de 1e-5
  fora da linha mais perto de 180°. Arquivo `results/etapa1.2/efeito_efemeride_de200.yaml`, gerado
  por `tools/efeito_efemeride.py`. É cerca de 10 vezes menor que o arredondamento das tabelas (3
  decimais e datas inteiras). A efeméride não explica nenhuma diferença observada.

## 2. Resultado da verificação (1992–2007)

Tabelas completas em `results/etapa1.2/verificacao_jpl8243.md`, gerado por
`tools/verifica_jpl8243.py`. Partida no baricentro de Marte; a chegada foi calculada no centro da
Terra (399) e no baricentro Terra–Lua (3).

| Grandeza | Linhas | Chegada no baricentro Terra–Lua: maior erro relativo nas datas do JPL | Chegada no centro da Terra |
| :- | -: | :- | :- |
| C3L, mínimo por tipo | 13 de 16 | ≤ 0,03 % | ≤ 0,04 % |
| VHP, mínimo por tipo | 16 de 16 | ≤ 0,09 % | até 0,45 % |

O mínimo próprio, buscado sem usar as datas do JPL, cai nas mesmas datas da tabela, com diferença
de no máximo 1 dia, em 28 das 29 linhas regulares com chegada no baricentro Terra–Lua. A exceção é
2002/3 VHP tipo II, explicada abaixo. O padrão é o mesmo
do manual da NASA na ida. Daí a **convenção INFERIDA**: as duas fontes tratam a Terra como o
baricentro Terra–Lua. **Nenhum dos dois documentos declara isso**; é uma inferência a partir da
concordância numérica. Nos cálculos da missão usa-se o centro da Terra (decisão do Fabio, 2026-10-27).

### Linhas fora do padrão (3 de 32), fora do teste automático

Ficam fora do teste pela lista explícita `config/excecoes_verificacao.yaml`, com o motivo de cada
uma. A tolerância P-008 não foi alargada para cobri-las.

| Linha | O que acontece | Explicação |
| :- | :- | :- |
| 1994, C3L tipo I (7.433) | Nas datas da tabela, às 00:00 TDB, o C3L sai 7.587 (+2,1 %) | O ângulo de transferência é 178,6°, perto da linha singular. O mínimo próprio reproduz **7.433 nas mesmas datas**, só que em outra hora do dia. A tabela dá datas inteiras, e perto de 180° algumas horas mudam o C3 em porcentagens. |
| 2002/3, C3L tipo II (9.525) | Mínimo próprio 9.627 (+1,1 %) | O mínimo do JPL fica em 180,2°, dentro da faixa de ±1° excluída pela P-006. Excluir essa faixa foi uma escolha nossa, e é ela que impede de reproduzir o valor. |
| 2004/5, C3L tipo II (13.197) | Nas datas impressas o ângulo é 307,9° e o C3L é 60,6 | O mínimo próprio reproduz **13.197 com a mesma partida (2005/07/08) e chegada em 2006/03/30**, não 2006/06/30 como impresso. A data de chegada impressa é inconsistente com o valor da mesma linha. Não conferi nos gráficos do documento. |

Uma quarta linha passa no teste de valor, mas tem uma diferença de classificação: 2002/3, VHP tipo
II (3.014). Nas datas da tabela o ângulo é 172,2°, que pela nossa definição (ângulo < 180° no
sentido prógrado da eclíptica) seria Tipo I. O valor confere (+0,09 %). A diferença é só de rótulo,
outra vez perto de 180°. Por causa disso, o mínimo próprio de VHP com restrição de Tipo II cai em
outro ponto (2003-02-28 → 2003-11-13, 3.107 km/s, +3,1 %, 9 dias de diferença na chegada).

Teste automático: `tests/test_retorno.py`, 29 linhas, tolerância P-008 (aprovada em 2026-10-27,
NÃO VALIDADA).

## 3. Retornos 2029–2040

Janelas com partida de Marte entre 2029 e 2040, localizadas por varredura de 2028 a 2041:
2030/31, 2032/33, 2034/35, 2037 e 2039/40. A janela de setembro de 2028 tem partida em 2028 e fica
fora. Partida no baricentro de Marte; **chegada no centro da Terra**, o fisicamente correto para a
reentrada. Valores de `results/etapa1.2/minimos_marte_terra.yaml`, gerado por
`tools/porkchop.py marte_terra`.

| Janela | Critério | Tipo | Partida | Chegada | TOF (d) | C3L (km²/s²) | v∞ Terra (km/s) |
| :- | :- | :- | :- | :- | -: | -: | -: |
| 2030 | mín. C3L | I | 2030-11-01 | 2031-07-07 | 247,7 | 5,79 | 5,64 |
| 2030 | mín. C3L | II | 2030-11-09 | 2031-09-23 | 318,2 | 5,43 | 5,47 |
| 2030 | mín. v∞ | I | 2031-01-08 | 2031-08-07 | 211,4 | 12,96 | 4,18 |
| 2030 | mín. v∞ | II | 2030-06-09 | 2031-07-23 | 408,3 | 12,80 | 3,80 |
| 2032 | mín. C3L | I | 2033-01-27 | 2033-09-02 | 217,5 | 5,72 | 4,06 |
| 2032 | mín. C3L | II | 2033-02-12 | 2033-11-02 | 263,2 | 5,81 | 4,95 |
| 2032 | mín. v∞ | I | 2033-02-28 | 2033-09-23 | 207,6 | 6,71 | 3,51 |
| 2032 | mín. v∞ | II | 2032-06-25 | 2033-08-19 | 420,3 | 14,96 | 4,16 |
| 2035 | mín. C3L | I | 2035-05-08 | 2035-11-22 | 198,1 | 8,76 | 3,04 |
| 2035 | mín. C3L | II | 2035-02-16 | 2035-11-12 | 268,9 | 12,94 | 3,16 |
| 2035 | mín. v∞ | I | 2035-06-03 | 2035-11-30 | 180,3 | 10,20 | 2,98 |
| 2035 | mín. v∞ | II | 2035-02-18 | 2035-11-13 | 268,0 | 13,39 | 3,01 |
| 2037 | mín. C3L | I | 2037-07-08 | 2038-01-19 | 195,2 | 14,31 | 3,91 |
| 2037 | mín. C3L | II | 2037-07-12 | 2038-04-07 | 269,6 | 12,55 | 3,53 |
| 2037 | mín. v∞ | I | 2037-08-24 | 2038-02-18 | 178,7 | 28,03 | 2,88 |
| 2037 | mín. v∞ | II | 2037-02-28 | 2038-01-07 | 313,3 | 31,71 | 3,00 |
| 2039 | mín. C3L | I | 2039-08-04 | 2040-03-11 | 220,7 | 13,60 | 4,41 |
| 2039 | mín. C3L | II | 2039-07-23 | 2040-05-04 | 286,0 | 9,59 | 2,85 |
| 2039 | mín. v∞ | I | 2039-09-11 | 2040-04-17 | 219,1 | 22,01 | 2,79 |
| 2039 | mín. v∞ | II | 2039-07-17 | 2040-05-01 | 289,3 | 9,71 | 2,85 |

Observações:

- **2035, Tipo II: não é um mínimo isolado.** Os dois mínimos (de C3L e de v∞) ficam em 181,0°,
  exatamente na borda da faixa excluída pela P-006, e o porkchop não mostra bacia própria do
  Tipo II nesse domínio. O arquivo de resultados marca esses pontos com
  `na_borda_da_exclusao_180: true`. Esses dois valores não devem ser usados como mínimo de Tipo II
  na Etapa 1.3 sem nova análise.
- **Domínios de busca.** Nenhum mínimo final ficou na borda do domínio (`na_borda_do_dominio`).
  Os domínios de 2030 e 2032 foram ampliados depois que os mínimos de v∞ do Tipo II apareceram na
  borda na primeira rodada.
- **Status desses números.** Os valores de 2029–2040 são **calculados**, não verificados: não há
  dado publicado para esse período (pesquisa na seção 4 de `docs/etapa1.2_lambert_porkchop.md`). O
  que foi verificado é o método, contra o JPL 82-43 em 1992–2007. A comparação com o GMAT fica
  para fases futuras.
- A velocidade de reentrada e o Δv a partir das órbitas de estacionamento ficam para a Etapa 1.3.

## 4. Porkchops

`results/etapa1.2/porkchop_marte_terra_<ano>.png` (2030, 2032, 2035, 2037, 2039) e os de ida,
regenerados com os ajustes pedidos em 2026-10-27, sem mudar os cálculos (arquivos de mínimos
idênticos byte a byte antes e depois):

1. a faixa de ±1° em torno de 180° (P-006) é mascarada no desenho, com nota de rodapé;
2. os níveis de contorno se limitam à região útil: C3 ≤ 20 km²/s² e v∞ ≤ 6 km/s
   (`config/janelas.yaml`);
3. vírgula decimal nos rótulos e na legenda.

## 5. Premissa nova

P-008 (tolerância da verificação contra o JPL 82-43, 0,2 %), aprovada em 2026-10-27, continua NÃO
VALIDADA.

## 6. Limitações

As mesmas da ida: cônicas emendadas, impulsivo, sem perturbações, sem manobra no espaço profundo.
A partida é no baricentro de Marte. Nada de órbita de estacionamento nem de captura (Etapa 1.3).

## Errata (Etapa 2.4, 2026-10-27): rótulos de instante dos mínimos
Os instantes gravados com o sufixo `_tdb` em `results/etapa1.2/minimos_*.yaml` eram, na verdade, UTC
(`spice.et2utc`), 69 s antes do instante TDB. Desde a Etapa 2.4 eles são TDB. Nenhuma data de mínimo muda de
dia (conferido por comparação dos arquivos antes e depois), e os valores de C3, v∞ e ângulo não mudam. As
verificações contra NASA/TM-2010-216764 e JPL 82-43 foram regeneradas sem nenhuma diferença.

