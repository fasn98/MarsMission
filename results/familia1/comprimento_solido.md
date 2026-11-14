# Comprimento do MAV sólido, P-108 revista (gerado por tools/comprimento_solido.py)

**NÃO VALIDADO.** P-108 revista, aprovada pelo Fabio em 2026-11-12.

- Motores do catálogo [F270] com diâmetro e comprimento publicados: 25.
- Forma: L = a · P^b · D^c, mínimos quadrados em ln: a = 0,0070, b = 0,780 (erro-padrão 0,059), c = −1,529 (erro-padrão 0,181); erro: fator rms 1,09, maior desvio fator 1,23.
- Só com o propelente (L = a · P^b): b = 0,294, fator rms 1,20, maior desvio 1,55.
- No Ø 0,57 m e no propelente do MSR: motores de 1,10 e 0,37 m; o resto até os 2,7 m do MSR ([F247]), 1,23 m, é interestágio, carga, aviônica e adaptadores, sem fonte, fixo na escala.

Comprimento do MAV = motor do estágio 1 + motor do estágio 2 + resto fixo.
