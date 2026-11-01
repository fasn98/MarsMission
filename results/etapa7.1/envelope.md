# Envelope e arranjo dos veículos (gerado por tools/envelope_arranjo.py)

Dimensões derivadas de results/ e config/cad.yaml (fontes e premissas). Comprimentos em m, volumes em m³, massas em kg.

## Orbitador no Falcon Heavy (coifa padrão, volume útil com mantas)

| Estágio | Propelente | Oxidante | Combustível | Tanque de oxidante | Tanque de combustível | Pares | Ø da esfera | Ø da esfera com 1 par |
| :- | -: | -: | -: | -: | -: | -: | -: | -: |
| Inserção em Marte | 3 210 | 1 999 | 1 211 | 1,470 | 1,467 | 2 | 1,12 | 1,41 |
| Retorno | 1 709 | 1 064 | 645 | 0,783 | 0,781 | 2 | 0,91 | 1,14 |

| Conjunto | Altura da base | Altura do topo | Raio do conjunto | Folga radial ao envelope |
| :- | -: | -: | -: | -: |
| Estágio de inserção em Marte | 0,00 | 1,12 | 1,96 | 0,36 |
| Estágio de retorno | 1,22 | 2,13 | 1,74 | 0,56 |
| CCRS (3,4 × 0,5 × 2 m, deitado) | 2,23 | 4,23 | 1,72 | 0,57 |

Altura do conjunto empilhado 4,23 m, contra 11,35 m do topo do volume útil: **cabe**. Painéis do orbitador: 14,3 m² (dobrados no lançamento; empacotamento na 7.2). EES: Ø 1,273 m, dentro do CCRS. A plataforma (614 kg) não tem volume dimensionado nesta etapa.

## Lander no Vulcan de 15,5 m (estágio de cruzeiro + aeroshell)

Massa de entrada do lander: 4 429 kg. Semiângulo da frente do aeroshell: 70°.

| Opção de aeroshell | Diâmetro | Massa de entrada da referência | Massa por área: lander / referência (kg/m²) | Altura do conjunto (P-083) | Folga radial no Vulcan | Diâmetro útil interno |
| :- | -: | -: | -: | -: | -: | -: |
| Mars 2020 | 4,50 | 3 360 | 279 / 211 | 3,00 | 0,136 | 4,00 |
| SRL, lançamento duplo | 4,65 | > 5 000 | 261 / > 294 | 3,10 | 0,060 | 4,15 |

- **Estágio de cruzeiro:** 113,8 kg de MMH/MON; tanques de 0,052 e 0,052 m³ (Ø 0,46 m).
- **Descida (P-084):** 544 kg de hidrazina em 3 esferas de Ø 0,71 m (0,571 m³ no total).
- **Painéis (P-088):** 32,8 m² em 2 asas circulares de Ø 4,57 m abertas (Phoenix: envergadura de 5,52 m e deck de 1,50 m).
- **Helicópteros:** rotor de Ø 1,40 m, altura 0,49 m. **Braço:** 2,35 m.

## MAV (dois estágios, R-4D-11)

| Segmento | Ø 0,50 m | Ø 0,57 m |
| :- | -: | -: |
| Motores do estágio 1 (4 × R-4D-11) | 0,60 | 0,60 |
| Tanque de oxidante do estágio 1 | 0,77 | 0,65 |
| Tanque de combustível do estágio 1 | 0,77 | 0,65 |
| Interestágio | 0,10 | 0,10 |
| Motor do estágio 2 (1 × R-4D-11) | 0,45 | 0,45 |
| Tanque de oxidante do estágio 2 | 0,38 | 0,38 |
| Tanque de combustível do estágio 2 | 0,38 | 0,38 |
| Carga (contêiner de amostras) | 0,35 | 0,35 |
| **Comprimento total** | **3,79** | **3,56** |

Referências: limite do MAV do MSR 2,99 m × Ø 0,50 m [F35]; restrição de 2019 3,00 m × Ø 0,57 m [F216]; Bowles, MAV de 312,5 kg: 2,19 m × Ø 0,52 m [F46]. GLOM do nosso MAV: 386,8 kg.
- Ø 0,50 m: cabe deitado no diâmetro útil interno do aeroshell? Mars 2020: sim; SRL, lançamento duplo: sim
- Ø 0,57 m: cabe deitado no diâmetro útil interno do aeroshell? Mars 2020: sim; SRL, lançamento duplo: sim

Vistas: orbitador_na_coifa.png, lander_na_coifa.png, lander_superficie.png, mav.png (esquemas, não desenho de projeto).
