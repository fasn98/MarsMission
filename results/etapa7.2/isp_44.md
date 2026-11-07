# Isp esperado do R-4D-11 com bocal de 44:1 (gerado por tools/isp_44_bocal.py)

**NÃO VALIDADO.** Isp esperado: **298,2 s**, de 296,0 a 300,5 s com o arredondamento dos dados. A faixa não inclui o erro de modelo: a conta extrapola de 164–300 para 44, sem grau de liberdade sobrando para conferi-la. É cálculo, não dado do fabricante. NASA CEA não está no workspace.

## Modelo

Mesmo motor: câmara, pressão e mistura iguais; muda só a razão de expansão ε. Com bocal ideal, para gás de γ constante:

- Γ = √γ · (2/(γ+1))^((γ+1)/(2(γ−1)))
- ε = Γ / √( 2γ/(γ−1) · x^(2/γ) · (1 − x^((γ−1)/γ)) ), com x = pe/pc
- CF = Γ · √( 2γ/(γ−1) · (1 − x^((γ−1)/γ)) ) + ε · x
- Isp = K · CF, com K = η c* / g0

Os dois pontos fixam as duas incógnitas: Isp(300:1)/Isp(164:1) = 315,5/311 = 1,01447 dá γ, e o 164:1 dá K. Fonte: [F228] PDF p. 22: "164:1 = 311 sec"; "300:1 = 315.5 sec". γ e K são efetivos: absorvem perdas que variam com ε, e γ não é o do gás real. O γ ajustado não foi comparado com um cálculo de equilíbrio.

## Conta

| Caso | Isp 164:1 (s) | Isp 300:1 (s) | γ efetivo | K (s) | CF 44:1 | CF 164:1 | CF 300:1 | Isp 44:1 (s) | Isp 40:1 (s) |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| Central | 311,00 | 315,50 | 1,2277 | 160,07 | 1,8629 | 1,9429 | 1,9710 | 298,20 | 297,08 |
| Baixo: extremos do arredondamento | 310,50 | 315,75 | 1,1943 | 155,92 | 1,8984 | 1,9915 | 2,0251 | 295,99 | 294,74 |
| Alto: extremos do arredondamento | 311,50 | 315,25 | 1,2666 | 164,58 | 1,8257 | 1,8927 | 1,9155 | 300,47 | 299,47 |

A meia resolução dos dados (±0,50 s e ±0,25 s) supõe resolução de 1 s no 311 e de 0,5 s no 315,5, sem fonte, NÃO VALIDADA.

## Empuxo

Com a mesma câmara e a mesma vazão, o empuxo escala com CF: 489 N × 0,9588 = **469 N** (NÃO VALIDADO). A folha dá o empuxo nominal sem separar as variantes; atribuí-lo ao 164:1 é escolha deste cálculo, e no 300:1 daria 462 N. O desenho de [F228] dá as cotas do 44:1, mas nenhum Isp, massa ou empuxo. A massa segue sem fonte.

## Sensibilidade a γ

γ imposto (NÃO VALIDADO), com K calibrado em um só ponto. A diferença entre as âncoras mostra quanto o γ imposto deixa de reproduzir os dois pontos.

| γ | Razão CF 300/164 | Isp 44:1, âncora 164:1 (s) | Isp 44:1, âncora 300:1 (s) |
| -: | -: | -: | -: |
| 1,15 | 1,02072 | 293,8 | 292,0 |
| 1,20 | 1,01647 | 296,8 | 296,2 |
| 1,25 | 1,01303 | 299,3 | 299,7 |
| 1,30 | 1,01025 | 301,3 | 302,6 |

## Comparação com o R-4D do Apollo

O modelo dá 297,1 s em ε = 40, de 294,7 a 299,5 s. Razão de expansão: [F242] PDF p. 15: "with an expansion ratio equal to 40", da câmara inicial; as outras páginas não repetem ε.

| [F242] | O que relata |
| :- | :- |
| PDF p. 15 | "good performance Isp's of 295 and 297"; "its maximum performance, Isp slightly over 310 seconds", em O/F perto de 1,9 (sem ε, pressão nem regime na frase) |
| PDF p. 19 | "295 to 300 seconds of impulse", em O/F de 1,8 a 1,9 |
| PDF p. 26, Fig. 12 | cerca de 300 s em O/F de 1,6 a 1,9, com máximo perto de 304 s, leitura a olho, sem ε na figura |
| PDF p. 62 | "maintained a mean Isp of 300 seconds" |
| PDF p. 66 | "the Isp was 295 seconds" com sangria de combustível para filme; cerca de 304 s sem filme |
| PDF p. 81 | 273 s e 313 s em O/F 2,0, com injetor triplet |
| PDF p. 87 | configuração PFRT, Isp em regime permanente de 286 ± 6 s |

**Isto é uma comparação, não uma verificação.** O programa relata de 273 a 313 s, conforme injetor, resfriamento e O/F, então a comparação discrimina pouco. O R-4D do Apollo também teve outra câmara (molibdênio com revestimento), outro injetor, O/F perto de 1,8 a 2,0 contra 1,65 no R-4D-11 ([F228] PDF p. 22), e trocou MMH por A-50 (PDF p. 19). A Fig. 12, perto de O/F 1,65, fica acima do valor calculado. O valor de pouco mais de 310 s não diz ε, pressão nem regime: se fosse de 40:1 em regime permanente, contrariaria o modelo. Não conferido

## Os análogos de 304 a 314 s

Decisão do Fabio (2026-11-07): não são coerentes com o R-4D-11. Têm câmara de irídio e rênio, ou só o resumo cita essa tecnologia, ou outro injetor ([F239], [F240]; results/etapa7.2/rotas_mav.md). Ficam na rota A só como comparação.
