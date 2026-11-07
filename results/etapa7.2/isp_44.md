# Isp esperado do R-4D-11 com bocal de 44:1 (gerado por tools/isp_44_bocal.py)

**NÃO VALIDADO.** Isp esperado: **298,2 s**, de 296,0 a 300,5 s com o arredondamento dos dados. É cálculo, não dado do fabricante. NASA CEA não está no workspace.

## Modelo

Mesmo motor: câmara, pressão e mistura iguais; muda só a razão de expansão ε. Com bocal ideal, para gás de γ constante:

- Γ = √γ · (2/(γ+1))^((γ+1)/(2(γ−1)))
- ε = Γ / √( 2γ/(γ−1) · x^(2/γ) · (1 − x^((γ−1)/γ)) ), com x = pe/pc
- CF = Γ · √( 2γ/(γ−1) · (1 − x^((γ−1)/γ)) ) + ε · x
- Isp = K · CF, com K = η c* / g0

Os dois pontos fixam as duas incógnitas: Isp(300:1)/Isp(164:1) = 315,5/311 = 1,01447 dá γ, e o 164:1 dá K. Fonte: [F228] PDF p. 22: "164:1 = 19.32"; "164:1 = 11.0"; "164:1 = 311 sec"; "164:1 = 3.76 kg (8.3 lbm)". γ e K são efetivos: absorvem perdas que variam com ε, e γ não é o do gás real. O γ ajustado não foi comparado com um cálculo de equilíbrio.

## Conta

| Caso | Isp 164:1 (s) | Isp 300:1 (s) | γ efetivo | K (s) | CF 44:1 | CF 164:1 | CF 300:1 | Isp 44:1 (s) | Isp 40:1 (s) |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| Central | 311,00 | 315,50 | 1,2277 | 160,07 | 1,8629 | 1,9429 | 1,9710 | 298,20 | 297,08 |
| Baixo: extremos do arredondamento | 310,50 | 315,75 | 1,1943 | 155,92 | 1,8984 | 1,9915 | 2,0251 | 295,99 | 294,74 |
| Alto: extremos do arredondamento | 311,50 | 315,25 | 1,2666 | 164,58 | 1,8257 | 1,8927 | 1,9155 | 300,47 | 299,47 |

A meia resolução dos dados (±0,50 s e ±0,25 s) é leitura do último dígito publicado, sem fonte, NÃO VALIDADA.

## Empuxo

Com a mesma câmara e a mesma vazão, o empuxo escala com CF: 489 N × 0,9588 = **469 N** (NÃO VALIDADO). O desenho de [F228] dá as cotas do 44:1, mas nenhum Isp, massa ou empuxo. A massa segue sem fonte.

## Sensibilidade a γ

γ imposto (NÃO VALIDADO), com K calibrado em um só ponto. A diferença entre as âncoras mostra quanto o γ imposto deixa de reproduzir os dois pontos.

| γ | Razão CF 300/164 | Isp 44:1, âncora 164:1 (s) | Isp 44:1, âncora 300:1 (s) |
| -: | -: | -: | -: |
| 1,15 | 1,02072 | 293,8 | 292,0 |
| 1,20 | 1,01647 | 296,8 | 296,2 |
| 1,25 | 1,01303 | 299,3 | 299,7 |
| 1,30 | 1,01025 | 301,3 | 302,6 |

## Comparação com o R-4D do Apollo

O modelo dá 297,1 s em ε = 40, de 294,7 a 299,5 s. [F242] PDF p. 15: "good performance Isp's of 295 and 297", "with an expansion ratio equal to 40"; PDF p. 19: "295 to 300 seconds"; PDF p. 62: "a mean Isp of 300 seconds". O valor calculado fica dentro do que a fonte relata para 295 a 300 s.

**Isto é uma comparação, não uma verificação.** O R-4D do Apollo tinha outra câmara (molibdênio com revestimento), outro injetor e O/F perto de 1,8 a 2,0 ([F242] PDF p. 15 e 19), contra 1,65 no R-4D-11 ([F228] PDF p. 22). A mesma página 15 cita "maximum performance" de "slightly over 310 seconds", sem dizer a condição; esse valor não entrou na comparação e contraria o modelo se for de 40:1 em regime permanente. Não conferido.

## Os análogos de 304 a 314 s

Decisão do Fabio (2026-11-07): não são coerentes com o R-4D-11. Têm câmara de irídio e rênio, ou só o resumo cita essa tecnologia, ou outro injetor ([F239], [F240]; results/etapa7.2/rotas_mav.md). Ficam na rota A só como comparação.
