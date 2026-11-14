# Diagnóstico da lei de massa inerte (gerado por tools/inerte_solido.py)

**Fora da comparação do CI** (CLAUDE.md, regra 6): saídas de ajustes que não fecham, de soluções não únicas e grandezas nulas por construção, arredondadas. Os resultados estão em results/familia1/inerte_solido.md.

## Verificação da lei A (nível do motor pelo [F269]) com o MAV do MSR

Órbita 318 × 344 km (publicada 350 km); costa 468 s (publicada 446 s); resíduo 2,6e+00.

## Voos da lei A (nível do motor pelo [F269]) a 380 km

| Caso | Órbita simulada (km) | Resíduo | Costa (s) |
| :- | :- | -: | -: |
| sem margem | 380 × 380 | raiz da P-117 | 517 |
| com margem | 421 × 632 | 1,6e+02 | 678 |

## Voos da variante nominal corrigida pelo viés, 380 km

| Caso | Órbita simulada (km) | Resíduo | Costa (s) |
| :- | :- | -: | -: |
| sem margem | 380 × 380 | raiz da P-117 | 518 |
| com margem | 422 × 633 | 1,6e+02 | 679 |

## Energia que sobra no sólido com margem (variante nominal)

- (a1) Melhor órbita 421 × 632 km; antecedência ótima 16 s (limite 300 s); c₁ = 0,050 1/s (limite da P-110 de 0,05 1/s).
- (b) Órbita aceita 421 × 632 km; semieixo a 527 km de altitude sobre o raio equatorial; orbitador com 9 420 kg (a massa injetada, limite superior):
  - circular de 380 km até o periapse: 18 m/s, 3,1 dias (recuperados na espiral de saída, Edelbaum coplanar);
  - apoapse em arcos em torno do periapse (P-049): 46 m/s, 18,5 dias (fim em 426 × 632 km).
- (a2) O ângulo e o guiamento da guinada não são mostrados: o ajuste é subdeterminado (curva de soluções exatas).

