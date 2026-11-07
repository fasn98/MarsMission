# Subida do MAV com o empuxo/peso real (gerado por tools/subida_mav.py)

**NÃO VALIDADO.** Simulação plana da subida até 100 × 100 km, com redimensionamento do MAV até convergir. Modelo em src/orbital/subida.py; premissas P-104 a P-107.

## Resposta

**A iteração não convergiu na rota A:** ver a busca do ponto fixo abaixo. **A rota A sem deck NÃO fecha: nenhuma das combinações de Isp e geometria chega a folga ≥ +0,05 m**. Há caso que não convergiu: ver a tabela.

## Verificação do modelo contra [F37]

Veículo de referência, de um estágio, com empuxo/peso 2,5, Isp 343 s e área de 1,227 m² ([F37], [F46]); massa de 394,1 kg (P-105); CD 0,50 (P-104). Simulado: **4 094,7 m/s**, contra 4 027,9 m/s de [F37] Tab. 1: +66,8 m/s (+1,7 %). [F37] otimizou ângulo de ataque e inclinação no POST II com Mars-GRAM 2001; aqui o guiamento é linear-tangente e a atmosfera é a de [F245], então o modelo gasta mais. Esse desvio entra só pela diferença entre casos, porque o Δv de cada caso é o de [F37] mais a diferença entre a simulação do caso e a da referência.

## Casos, convergidos

| Caso | Isp (s) | Empuxo por motor (N) | Iterações | GLOM (kg) | Empuxo/peso | Empuxo/peso do estágio 2 | Δv 100 × 100 km (m/s) | Δv de subida com margem (km/s) | Massa por área (kg/m²) |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| Base: R-4D-11 164:1, sem aninhar | 310,0 | 489 | 16 | 355,7 | 1,48 | 1,60 | 3 933,3 | 5,668 | 274 |
| Rota A sem deck, Isp calculado baixo | 296,0 | 466 | não convergiu: diverge: no passo 2, GLOM de 762,9 kg e empuxo/peso de 0,66, abaixo de 1: o MAV não decola | | | | | | |
| Rota A sem deck, Isp calculado central | 298,2 | 469 | não convergiu: diverge: no passo 2, GLOM de 645,6 kg e empuxo/peso de 0,78, abaixo de 1: o MAV não decola | | | | | | |
| Rota A sem deck, Isp calculado alto | 300,5 | 472 | não convergiu: diverge: no passo 2, GLOM de 561,9 kg e empuxo/peso de 0,90, abaixo de 1: o MAV não decola | | | | | | |

Antes, todos os casos usavam 4 027,9 m/s, de empuxo/peso 2,5.

## Busca do ponto fixo nos casos que não convergiram

Para cada Δv de 100 × 100 km usado no dimensionamento, o Δv que a simulação pede para o MAV resultante. Há ponto fixo onde a diferença troca de sinal. Se a diferença é positiva em toda a varredura e o empuxo/peso cai abaixo de 1, não existe MAV que feche.

| Caso | Δv usado (m/s) | GLOM (kg) | Empuxo/peso | Δv pedido (m/s) | Pedido − usado (m/s) |
| :- | -: | -: | -: | -: | -: |
| Rota A sem deck, Isp calculado baixo | 3 900 | 429,3 | 1,17 | 4 185,3 | +285,3 |
| Rota A sem deck, Isp calculado baixo | 4 000 | 473,7 | 1,06 | 4 371,7 | +371,7 |
| Rota A sem deck, Isp calculado baixo | 4 100 | 524,4 | 0,96 | não decola | |
| **Rota A sem deck, Isp calculado baixo** | **sem ponto fixo na varredura** | | | | |
| Rota A sem deck, Isp calculado central | 3 900 | 413,9 | 1,22 | 4 124,1 | +224,1 |
| Rota A sem deck, Isp calculado central | 4 000 | 455,8 | 1,11 | 4 279,5 | +279,5 |
| Rota A sem deck, Isp calculado central | 4 100 | 503,6 | 1,00 | 4 517,0 | +417,0 |
| Rota A sem deck, Isp calculado central | 4 200 | 558,2 | 0,91 | não decola | |
| **Rota A sem deck, Isp calculado central** | **sem ponto fixo na varredura** | | | | |
| Rota A sem deck, Isp calculado alto | 3 900 | 399,0 | 1,27 | 4 071,4 | +171,4 |
| Rota A sem deck, Isp calculado alto | 4 000 | 438,7 | 1,16 | 4 200,9 | +200,9 |
| Rota A sem deck, Isp calculado alto | 4 100 | 483,7 | 1,05 | 4 395,6 | +295,6 |
| Rota A sem deck, Isp calculado alto | 4 200 | 535,0 | 0,95 | não decola | |
| **Rota A sem deck, Isp calculado alto** | **sem ponto fixo na varredura** | | | | |

## Comprimento e folga deitado

Limites em Ø 0,57 m: 3,184 m sem deck e 2,744 m com deck. Alvo de folga: +0,05 m. A base usa o seu próprio Ø.

| Caso | Geometria do estágio 2 | Comprimento (m) | Folga sem deck (m) | Folga com deck (m) |
| :- | :- | -: | -: | -: |
| Base: R-4D-11 164:1, sem aninhar | sem aninhar | 3,525 | −0,171 | −0,391 |

## Sensibilidade ao coeficiente de arrasto (rota A, Isp central)

A referência é simulada de novo com o mesmo CD.

| CD | Referência (m/s) | Referência − [F37] (m/s) | GLOM (kg) | Δv 100 × 100 km (m/s) | Folga sem deck, melhor e pior geometria (m) |
| -: | -: | -: | -: | -: | -: |
| 0,25 | 4 013,4 | −14,5 | não convergiu | | |
| 0,50 | 4 094,7 | +66,8 | não convergiu | | |
| 1,00 | 4 225,7 | +197,8 | não convergiu | | |

## Limitações

- Inserção direta, com queima contínua. Sem costa entre os estágios e sem queima de circularização separada: o MAV do MSR usa costa longa ([F57] PDF p. 2: "the MAV remains in a coast period"), que este modelo não explora.
- Sem perda por pressão no bocal (empuxo no vácuo nos dois lados da diferença); a de [F37] está dentro dos 4.027,9 m/s.
- Plano equatorial rumo leste, como [F37]; a latitude do sítio e a inclinação continuam no déficit de rotação de config/superficie.yaml.
- Atmosfera de página educacional ([F245]); densidade zero acima de 80 km (P-106); CD constante (P-104).
- A fração estrutural e a divisão de Δv entre os estágios são as de antes (P-019 e ε 0,230); a massa dos tanques da rota A não entra no GLOM.
- O estágio 2 também faz a transferência até a órbita de encontro, que não é simulada: entra pelo Δv ideal, como antes.
