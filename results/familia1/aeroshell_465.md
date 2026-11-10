# Família 1 com o aeroshell de 4,65 m (gerado por tools/familia1_465.py)

**NÃO VALIDADO.** Forma da cápsula: SRL-A (Ø 4,65 m); adaptador da P-097 (0,127 m e 43 kg).

## (a) Encaixe no Vulcan com a coifa longa de 21,3 m

Envelope de [F80] Fig. 4.3.1-2, PDF p. 45 (figura simplificada, leitura das cotas). Duas leituras entre as cotas, como na 7.2: contorno reto, e o Ø da segunda estação desde a interface.

| Cápsula | Leitura | Folga radial nos vértices (m) | Folga na grade de 400 pontos (m) |
| :- | :- | -: | -: |
| SRL-A (Ø máximo do perfil 4,68 m) | contorno reto | +0,085 | +0,088 |
| SRL-A (Ø máximo do perfil 4,68 m) | Ø menor desde a interface | +0,073 | +0,075 |
| SRL-C (Ø máximo do perfil 4,72 m) | contorno reto | +0,067 | +0,069 |
| SRL-C (Ø máximo do perfil 4,72 m) | Ø menor desde a interface | +0,053 | +0,055 |
| MSL-M2020 (Ø máximo do perfil 4,52 m) | contorno reto | +0,169 | +0,171 |
| MSL-M2020 (Ø máximo do perfil 4,52 m) | Ø menor desde a interface | +0,153 | +0,154 |

## (b) Comprimento máximo do MAV deitado

| Ø do MAV (m) | 4,65 m sem deck | 4,65 m com deck (P-094) | 4,5 m sem deck | 4,5 m com deck |
| -: | -: | -: | -: | -: |
| 0,57 | 3,595 | 3,287 | 3,184 | 2,744 |
| 0,60 | 3,564 | 3,257 | 3,140 | 2,700 |
| 0,63 | 3,534 | 3,226 | 3,096 | 2,656 |
| 0,66 | 3,503 | 3,195 | 3,052 | 2,612 |
| 0,69 | 3,472 | 3,164 | 3,008 | 2,568 |
| 0,72 | 3,441 | 3,133 | 2,964 | 2,524 |
| 0,75 | 3,410 | 3,103 | 2,920 | 2,480 |

## (c) e (d) Folgas e massa por área (alvo +0,05 m)

| MAV | Ø (m) | Comprimento (m) | 4,65 m sem deck | 4,65 m com deck | 4,5 m sem deck | 4,5 m com deck | Massa por área com 4,65 m, modelo (kg/m²) | Com 4,65 m, piso do SRL (kg/m²) | Com 4,5 m, modelo (kg/m²) |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| Sólido, 380 km, sem margem (o menor que chega) | 0,57 | 2,73 a 2,78 | +0,409 a +0,430 | +0,255 a +0,276 | +0,203 a +0,225 | −0,017 a +0,005 | 262 | 294 | 279 |
| Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | 0,57 | 6,12 a 10,40 | −3,401 a −1,263 | −3,555 a −1,417 | −3,607 a −1,469 | −3,827 a −1,689 | 385 | 385 | 411 |
| Sólido, 814 km | — | não fecha | | | | | | | |
| Hipergólico 4 × 164:1, 380 km, com a margem da P-014 | 0,72 | 3,06 | +0,191 | +0,037 | −0,047 | −0,267 | 233 | 294 | 249 |
| Hipergólico 4 × 164:1, 380 km, sem margem | 0,72 | 2,94 | +0,253 | +0,099 | +0,014 | −0,206 | 229 | 294 | 245 |
| Hipergólico 4 × 164:1, 814 km, com a margem da P-014 | 0,72 | 3,11 | +0,165 | +0,011 | −0,074 | −0,294 | 236 | 294 | 252 |
| Hipergólico 4 × 164:1, 814 km, sem margem | 0,72 | 2,98 | +0,232 | +0,078 | −0,007 | −0,227 | 231 | 294 | 246 |
| Fase 2: Base: 4 × 164:1, Ø atual | 0,57 | 3,56 | +0,017 | −0,137 | −0,188 | −0,408 | 261 | 294 | 279 |
| Fase 2: Base com a P-086 só pelo motor 164:1 [F228], sem estrutura de empuxo (a P-086 não muda) | 0,57 | 3,62 | −0,012 | −0,166 | −0,218 | −0,438 | 261 | 294 | 279 |

Abaixo do alvo com deck no aeroshell de 4,65 m, embora positivos: Hipergólico 4 × 164:1, 380 km, com a margem da P-014 (+0,037 m); Hipergólico 4 × 164:1, 814 km, com a margem da P-014 (+0,011 m). O alvo de +0,05 m continua (decisão do Fabio, 2026-11-10, PR #60).

Mars 2020: 211 kg/m² (results/etapa7.2/rotas_mav.md). A massa de entrada não muda com o diâmetro no modelo (P-018 fixa): o aeroshell maior não pesa mais aqui, o que é otimista. A coluna do piso usa a massa de entrada publicada do SRL de 4,65 m (5 000 kg, [F202] p. 13, ">5000") quando o modelo dá menos.

## (e) Margem do lander no Vulcan com a coifa longa

[F80] não publica a capacidade para C3 de Marte com a coifa longa: a Tab. 2.2.5-1 (PDF p. 21) só traz VC2S, VC4S e VC6S (coifa padrão). Coluna "coifa padrão": a curva do ELVPerf [F79] usada no estudo, menos o adaptador da P-097; a consulta não informa o comprimento da coifa, e tratá-la como a da coifa padrão é inferência (limite otimista para a coifa longa). Coluna "coifa longa": a mesma curva menos também 89 kg da P-112 (NÃO VALIDADA, análogo da Atlas V em GTO, [F27] PDF p. 57; sem fonte para o Vulcan).

Duas massas do lander: a do modelo (razão pousada/entrada da P-018 fixa, a mesma do aeroshell de 4,5 m) e a com a massa de entrada levada ao piso publicado do SRL de 4,65 m (5 000 kg, [F202] p. 13, ">5000"), quando o modelo dá menos.

| Lander | Massa de entrada (kg) | Injetado (kg) | VC4, coifa padrão | VC4, coifa longa | VC6, coifa padrão | VC6, coifa longa |
| :- | -: | -: | -: | -: | -: | -: |
| Sólido, 380 km, sem margem (o menor que chega) (modelo) | 4 443 | 4 629 | +39,2 % | +37,3 % | +78,2 % | +76,3 % |
| Sólido, 380 km, sem margem (o menor que chega) (piso do SRL) | 5 000 | 5 205 | +23,8 % | +22,1 % | +58,5 % | +56,8 % |
| Sólido, 380 km, com a margem da P-014 na capacidade, não simulado (modelo) | 6 539 | 6 795 | −5,2 % | −6,5 % | +21,4 % | +20,1 % |
| Sólido, 380 km, com a margem da P-014 na capacidade, não simulado (piso do SRL) | 6 539 | 6 795 | −5,2 % | −6,5 % | +21,4 % | +20,1 % |
| Hipergólico 4 × 164:1, 380 km, com a margem da P-014 (modelo) | 3 964 | 4 133 | +55,9 % | +53,8 % | +99,6 % | +97,4 % |
| Hipergólico 4 × 164:1, 380 km, com a margem da P-014 (piso do SRL) | 5 000 | 5 205 | +23,8 % | +22,1 % | +58,5 % | +56,8 % |
| Hipergólico 4 × 164:1, 380 km, sem margem (modelo) | 3 892 | 4 059 | +58,8 % | +56,6 % | +103,2 % | +101,0 % |
| Hipergólico 4 × 164:1, 380 km, sem margem (piso do SRL) | 5 000 | 5 205 | +23,8 % | +22,1 % | +58,5 % | +56,8 % |
| Hipergólico 4 × 164:1, 814 km, com a margem da P-014 (modelo) | 4 001 | 4 172 | +54,5 % | +52,3 % | +97,7 % | +95,6 % |
| Hipergólico 4 × 164:1, 814 km, com a margem da P-014 (piso do SRL) | 5 000 | 5 205 | +23,8 % | +22,1 % | +58,5 % | +56,8 % |
| Hipergólico 4 × 164:1, 814 km, sem margem (modelo) | 3 917 | 4 085 | +57,7 % | +55,6 % | +101,9 % | +99,8 % |
| Hipergólico 4 × 164:1, 814 km, sem margem (piso do SRL) | 5 000 | 5 205 | +23,8 % | +22,1 % | +58,5 % | +56,8 % |
| Fase 2: Base: 4 × 164:1, Ø atual (modelo) | 4 429 | 4 615 | +39,6 % | +37,7 % | +78,8 % | +76,8 % |
| Fase 2: Base: 4 × 164:1, Ø atual (piso do SRL) | 5 000 | 5 205 | +23,8 % | +22,1 % | +58,5 % | +56,8 % |
| Fase 2: Base com a P-086 só pelo motor 164:1 [F228], sem estrutura de empuxo (a P-086 não muda) (modelo) | 4 429 | 4 615 | +39,6 % | +37,7 % | +78,8 % | +76,8 % |
| Fase 2: Base com a P-086 só pelo motor 164:1 [F228], sem estrutura de empuxo (a P-086 não muda) (piso do SRL) | 5 000 | 5 205 | +23,8 % | +22,1 % | +58,5 % | +56,8 % |

Pior margem no VC4 com a curva da coifa padrão (limite otimista para a coifa longa): −5,2 %; melhor: +58,8 %.

**O VC4 com a coifa longa não tem margem positiva** (nem no limite otimista) para: Sólido, 380 km, com a margem da P-014 na capacidade, não simulado (modelo); Sólido, 380 km, com a margem da P-014 na capacidade, não simulado (piso do SRL). Nesses casos o VC6 fica como a alternativa; a decisão é do Fabio.

## (f) Sólido: P-111 × P-019, com a margem da P-014

| Inerte | Encontro (km) | Capacidade mínima (m/s) | Capacidade assintótica (m/s) | Caso | Escala | GLOM (kg) | Comprimento (m) | 4,65 m sem deck | 4,65 m com deck |
| :- | -: | -: | -: | :- | -: | -: | -: | -: | -: |
| P-111 (divisão da conferência) | 380 | 4 103 | 4 694 | sem margem | 1,03 | 404,9 | 2,73 a 2,78 | +0,409 a +0,430 | +0,255 a +0,276 |
| P-111 (divisão da conferência) | 380 | 4 103 | 4 694 | com a margem da P-014, não simulado | 3,85 | 1 471,7 | 6,12 a 10,40 | −3,401 a −1,263 | −3,555 a −1,417 |
| P-111 (divisão da conferência) | 814 | não fecha na varredura | 4 694 | melhor ponto (diagnóstico): resíduo 9,1e+01 (tolerância 1e-06), 679 × 803 km, 4 520 m/s | 4,00 | 1 528,0 | | | |
| P-111 (divisão da conferência) | 814 | | | indicativo com a margem da P-014: não existe (passa da capacidade assintótica) | | | | | |
| P-019 (ε 0,286 nos dois estágios) | 380 | não fecha na varredura | 5 889 | melhor ponto (diagnóstico): resíduo 3,3e-04 (tolerância 1e-06), 380 × 380 km, 4 268 m/s | 0,60 | 243,2 | | | |
| P-019 (ε 0,286 nos dois estágios) | 380 | | | indicativo: o melhor ponto com a margem da P-014, não simulado | 0,94 | 373,8 | 2,55 a 2,63 | +0,481 a +0,522 | +0,327 a +0,368 |
| P-019 (ε 0,286 nos dois estágios) | 814 | não fecha na varredura | 5 889 | melhor ponto (diagnóstico): resíduo 7,6e-01 (tolerância 1e-06), 802 × 814 km, 5 347 m/s | 2,55 | 981,7 | | | |
| P-019 (ε 0,286 nos dois estágios) | 814 | | | indicativo: o melhor ponto com a margem da P-014, não simulado | 206,41 | 78 187,5 | 249,20 a 557,32 | −276,862 a −122,801 | −277,016 a −122,955 |

A capacidade assintótica é a de um sólido de escala infinita com os mesmos k de inerte: se a capacidade com a margem passa dela, não há sólido que feche.

"Não fecha na varredura" quer dizer: nenhum ponto da varredura da P-110 (passo e tolerância de lá) chega à órbita dentro da tolerância. O melhor ponto é diagnóstico, não resultado: a P-110 não foi mudada.

Com a P-019 a 380 km, o melhor ponto fica a menos de 1 km da órbita (resíduo acima da tolerância da P-110). O sólido não regula o empuxo: Δv a mais passa da órbita, e a janela de escalas que chegam é estreita. O mais provável é que o passo da varredura da P-110 seja grosso para o inerte mais leve da P-019, e não que a P-019 piore o sólido: a capacidade assintótica com a P-019 é maior que com a P-111. Mudar o passo ou a tolerância da P-110 é decisão do Fabio.

O caso indicativo é a escala cuja capacidade ideal chega ao melhor ponto vezes 1 + a margem da P-014; "não existe" quando esse alvo passa da capacidade assintótica.

## Política de margem do MAV sólido do MSR, nas fontes

- [F34] PDF p. 6: "A mass growth allowance of 19% and 17% was assigned to the first and second stage structures, respectively."
- [F34] PDF p. 7: "the MAVSolid trajectory was designed so that it targeted above the ideal orbit altitude in order to maintain the minimum periapsis of 300 km, including when performance parameters like ISP, payload mass, launch angle, and azimuth were selectively dispersed."
- [F248] PDF p. 12: "Trajectories delivered the expected ~4 kg payload margin."
- [F248] PDF p. 17: "a MAV solid propulsion system was designed that allowed the vehicle to maintain a GLOM 6 kg below the 400 kg limit."
- [F230] PDF p. 6: "The designs themselves included a length margin of 10cm on SRM1 and 1.8kg of propellant mass margin in SRM2."
- [F267] PDF p. 3 (Tab. 1, requisitos do estudo de conceito de 2018): "Performance Margin" — "Addtl. 5 kg payload"; "Other Margin Allocation" — "AIAA margins / 25% for unknowns"
