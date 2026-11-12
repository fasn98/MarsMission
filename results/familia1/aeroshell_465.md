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
| Sólido, 380 km, sem margem (o menor que chega) | 0,57 | 2,87 | +0,362 | +0,208 | +0,156 | −0,064 | 267 | 294 | 285 |
| Sólido, 380 km, com a margem da P-014 na capacidade, não simulado | 0,57 | 8,61 | −2,510 | −2,664 | −2,715 | −2,935 | 562 | 562 | 600 |
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
| Sólido, 380 km, sem margem (o menor que chega) (modelo) | 4 534 | 4 723 | +36,4 % | +34,6 % | +74,7 % | +72,8 % |
| Sólido, 380 km, sem margem (o menor que chega) (piso do SRL) | 5 000 | 5 205 | +23,8 % | +22,1 % | +58,5 % | +56,8 % |
| Sólido, 380 km, com a margem da P-014 na capacidade, não simulado (modelo) | 9 549 | 9 906 | −34,9 % | −35,8 % | −16,7 % | −17,6 % |
| Sólido, 380 km, com a margem da P-014 na capacidade, não simulado (piso do SRL) | 9 549 | 9 906 | −34,9 % | −35,8 % | −16,7 % | −17,6 % |
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

Pior margem no VC4 com a curva da coifa padrão (limite otimista para a coifa longa): −34,9 %; melhor: +58,8 %.

**O VC4 com a coifa longa não tem margem positiva** (nem no limite otimista) para: Sólido, 380 km, com a margem da P-014 na capacidade, não simulado (modelo); Sólido, 380 km, com a margem da P-014 na capacidade, não simulado (piso do SRL). Nesses casos o VC6 fica como a alternativa; a decisão é do Fabio.

## (f) Sólido: P-111 × P-019, com a margem da P-014

| Inerte | Encontro (km) | Capacidade mínima (m/s) | Capacidade assintótica (m/s) | Caso | Escala | GLOM (kg) | Comprimento (m) | 4,65 m sem deck | 4,65 m com deck |
| :- | -: | -: | -: | :- | -: | -: | -: | -: | -: |
| P-111 (divisão da conferência) | 380 | 4 050 | 4 535 | sem margem | 1,15 | 451,2 | 2,87 | +0,362 | +0,208 |
| P-111 (divisão da conferência) | 380 | 4 050 | 4 535 | com a margem da P-014, não simulado | 7,90 | 3 003,8 | 8,61 | −2,510 | −2,664 |
| P-111 (divisão da conferência) | 814 | não fecha na varredura | 4 535 | melhor ponto (diagnóstico): resíduo 1,0e+02 (tolerância 1e-06), 613 × 790 km, 4 380 m/s | 4,00 | 1 528,0 | | | |
| P-111 (divisão da conferência) | 814 | | | indicativo com a margem da P-014: não existe (passa da capacidade assintótica) | | | | | |
| P-019 (ε 0,286 nos dois estágios) | 380 | 4 186 | 5 889 | sem margem | 0,55 | 225,8 | 2,16 | +0,719 | +0,565 |
| P-019 (ε 0,286 nos dois estágios) | 380 | 4 186 | 5 889 | com a margem da P-014, não simulado | 0,85 | 338,5 | 2,53 | +0,534 | +0,380 |
| P-019 (ε 0,286 nos dois estágios) | 814 | não fecha na varredura | 5 889 | melhor ponto (diagnóstico): resíduo 3,8e-01 (tolerância 1e-06), 802 × 814 km, 5 347 m/s | 2,55 | 981,7 | | | |
| P-019 (ε 0,286 nos dois estágios) | 814 | | | indicativo: o melhor ponto com a margem da P-014, não simulado | 206,41 | 78 187,5 | 95,47 | −45,940 | −46,093 |

A capacidade assintótica é a de um sólido de escala infinita com os mesmos k de inerte: se a capacidade com a margem passa dela, não há sólido que feche.

"Não fecha na varredura" quer dizer: em nenhuma escala da varredura da P-110 o ajuste chega à circular (critério da P-117). O melhor ponto é diagnóstico, não resultado.

**Nota (2026-11-12):** a escala mínima do sólido passou a ser a raiz de (maior semieixo de uma circular alcançável) − (raio-alvo) (P-117, PR #64); as versões anteriores desta página, com o ajuste antigo, davam a P-019 a 380 km como "não fecha na varredura", com o melhor ponto a menos de 1 km da órbita. Valem os números desta versão; os da linha do sólido nas seções (c) a (e) vêm de results/familia1/mavs.yaml, regenerado no PR #64.

O caso indicativo é a escala cuja capacidade ideal chega ao melhor ponto vezes 1 + a margem da P-014; "não existe" quando esse alvo passa da capacidade assintótica.

## Política de margem do MAV sólido do MSR, nas fontes

- [F34] PDF p. 6: "A mass growth allowance of 19% and 17% was assigned to the first and second stage structures, respectively."
- [F34] PDF p. 7: "the MAVSolid trajectory was designed so that it targeted above the ideal orbit altitude in order to maintain the minimum periapsis of 300 km, including when performance parameters like ISP, payload mass, launch angle, and azimuth were selectively dispersed."
- [F248] PDF p. 12: "Trajectories delivered the expected ~4 kg payload margin."
- [F248] PDF p. 17: "a MAV solid propulsion system was designed that allowed the vehicle to maintain a GLOM 6 kg below the 400 kg limit."
- [F230] PDF p. 6: "The designs themselves included a length margin of 10cm on SRM1 and 1.8kg of propellant mass margin in SRM2."
- [F267] PDF p. 3 (Tab. 1, requisitos do estudo de conceito de 2018): "Performance Margin" — "Addtl. 5 kg payload"; "Other Margin Allocation" — "AIAA margins / 25% for unknowns"
