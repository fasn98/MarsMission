# Modelo de baixo empuxo (gerado por tools/baixo_empuxo.py)

## 1. Verificação contra Schwenzfeger, NASA TM X-64836 (1973), p. 31 [F113]

Subida com aceleração tangencial constante ε = 0,01 a partir de órbita circular, adimensional (r0 = v0 = μ = 1). u = r·ṙ, v = r·v_θ, h = energia por massa. Diferença relativa = (calculado − publicado) / |publicado|, por componente; tolerância 0,01 % (P-046). **Verificado: NÃO (fora da tolerância: u).**
As duas últimas colunas (informativas, não são o critério declarado) dão o erro dos vetores posição e velocidade (ṙ, v_θ) relativo ao módulo de cada um.

| t | r publicado | r calculado | Dif. r | Dif. φ | Dif. u | Dif. v | Dif. h | Vetor posição | Vetor velocidade |
| -: | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| 0,1500 | 1,0000112 | 1,0000112 | +4,6e-08 | −2,6e-08 | +5,5e-09 | +8,4e-09 | −1,0e-08 | 4,6e-08 | 3,7e-08 |
| 2,5789 | 1,0408298 | 1,0408298 | −3,5e-08 | +3,9e-08 | +1,3e-06 | −2,2e-08 | −8,9e-09 | 1,1e-07 | 5,1e-08 |
| 9,8502 | 1,2116137 | 1,2116138 | +5,6e-08 | −3,1e-06 | −3,2e-04 | +2,2e-07 | −4,3e-07 | 2,7e-05 | 1,3e-05 |
| 18,5400 | 1,4787448 | 1,4787615 | +1,1e-05 | −2,0e-06 | −3,1e-04 | +3,0e-07 | −7,0e-07 | 3,0e-05 | 1,7e-05 |
| 35,0757 | 2,3098730 | 2,3098814 | +3,6e-06 | −1,5e-06 | −1,4e-04 | +7,2e-07 | −1,8e-06 | 3,1e-05 | 1,5e-05 |
| 70,1725 | 7,5562739 | 7,5563457 | +9,5e-06 | +5,9e-08 | +1,5e-05 | −3,5e-07 | +3,8e-06 | 9,6e-06 | 8,7e-06 |
| 85,6922 | 12,7045900 | 12,7046775 | +6,9e-06 | −3,1e-07 | +5,4e-06 | +1,7e-07 | −3,7e-06 | 1,1e-05 | 4,3e-06 |

### Investigação da diferença

Convergência do integrador deste estudo: maior mudança relativa, nos pontos publicados, contra o integrador de base (DOP853, rtol da P-046).

| Método | rtol | Mudança r | Mudança phi | Mudança u | Mudança v | Mudança h |
| :- | -: | -: | -: | -: | -: | -: |
| DOP853 | 1e-09 | 3,5e-09 | 1,8e-09 | 2,6e-07 | 1,8e-09 | 1,8e-08 |
| DOP853 | 1e-13 | 3,9e-11 | 2,0e-11 | 1,1e-08 | 2,0e-11 | 1,9e-10 |
| Radau | 1e-11 | 3,9e-11 | 2,0e-11 | 1,1e-08 | 2,1e-11 | 2,0e-10 |

A listagem comparada nos valores de s que a fonte imprime, integrando o sistema da fonte na variável s (t' = r): diferença relativa (calculado − publicado) / |publicado|.

| s | Dif. r | Dif. phi | Dif. u | Dif. v | Dif. h | Dif. t |
| -: | -: | -: | -: | -: | -: | -: |
| 0,150000 | +4,6e-08 | −1,4e-08 | +1,9e-08 | +8,4e-09 | −1,0e-08 | +1,2e-08 |
| 2,550000 | −3,6e-08 | +2,7e-08 | +1,3e-06 | −2,2e-08 | −9,6e-09 | −1,3e-08 |
| 8,950000 | +5,8e-07 | −1,6e-06 | −3,1e-04 | +4,1e-07 | −4,6e-08 | +1,7e-06 |
| 15,350000 | +1,2e-05 | −1,0e-06 | −3,0e-04 | +5,9e-07 | −8,9e-08 | +1,3e-06 |
| 24,310000 | +5,2e-06 | −8,1e-07 | −1,3e-04 | +1,5e-06 | −1,8e-07 | +1,4e-06 |
| 33,270000 | +8,6e-06 | +7,0e-09 | +1,3e-05 | −8,9e-07 | −1,9e-06 | −3,6e-07 |
| 34,488779 | −1,3e-01 | −4,8e-03 | −2,3e-01 | −8,4e-02 | −4,1e-01 | −5,2e-02 |

## 2. Conferência: espiral numérica × solução analítica quase circular (Edelbaum, coplanar)

Não é verificação: as duas soluções são deste estudo. ε = aceleração / (μ/r0²); tempo em unidades de √(r0³/μ). A espiral para quando a energia chega à da órbita circular de raio r1.

### Marte, descida da circular de mesma energia que a órbita de encontro até 300 km

r0 = 16 042 km, r1 = 3 696 km (r1/r0 = 0,2304); Δv de Edelbaum = 1,770 km/s; unidade de tempo 9 818 s; aceleração de referência μ/r0² = 0,1664 m/s².

| ε | Δv numérico (adim.) | Δv Edelbaum (adim.) | Diferença relativa | Duração (adim.) | Voltas | Raio final / r0 | Excentricidade final |
| -: | -: | -: | -: | -: | -: | -: | -: |
| 1e-02 | 1,0836173 | 1,0833105 | +2,8e-04 | 108,4 | 71,0 | 0,2304 | 0,0405 |
| 1e-03 | 1,0833141 | 1,0833105 | +3,3e-06 | 1 083,3 | 709,7 | 0,2295 | 0,0042 |
| 1e-04 | 1,0833106 | 1,0833105 | +2,9e-08 | 10 833,1 | 7 097,2 | 0,2305 | 0,0004 |

### Heliocêntrico, da órbita da Terra à de Marte (calculado, não verificado)

r0 = 149 597 871 km, r1 = 227 941 004 km (r1/r0 = 1,5237); Δv de Edelbaum = 5,655 km/s; unidade de tempo 5 022 643 s; aceleração de referência μ/r0² = 0,0059 m/s².

| ε | Δv numérico (adim.) | Δv Edelbaum (adim.) | Diferença relativa | Duração (adim.) | Voltas | Raio final / r0 | Excentricidade final |
| -: | -: | -: | -: | -: | -: | -: | -: |
| 1e-02 | 0,1892910 | 0,1898760 | −3,1e-03 | 18,9 | 2,3 | 1,4929 | 0,0503 |
| 1e-03 | 0,1898686 | 0,1898760 | −3,9e-05 | 189,9 | 22,7 | 1,5256 | 0,0057 |
| 1e-04 | 0,1898760 | 0,1898760 | −4,6e-07 | 1 898,8 | 226,5 | 1,5237 | 0,0006 |

O trecho heliocêntrico é **calculado, não verificado**: não foi encontrado caso publicado comparável (docs/etapa3.2_baixo_empuxo.md).
