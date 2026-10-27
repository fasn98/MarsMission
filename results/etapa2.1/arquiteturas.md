# Arquiteturas de superfície (gerado por tools/superficie.py)

Δv em km/s, massas em kg. Margem de 10% (P-014) nos trechos propulsivos. Missão A (2028-conjuncao); "envelope" = pior caso entre os mínimos por janela (ADR 0004).

| | **S1**: Entrada direta + encontro em órbita baixa circular (como o MSR) | **S2**: Entrada direta + encontro na órbita de 1 sol (orbitador não muda de órbita) | **S3**: Pouso a partir da órbita de 1 sol (lander se captura) + encontro em órbita baixa circular | **S4**: Entrada direta + encontro em órbita baixa; orbitador desce por aerofrenagem |
| :- | :- | :- | :- | :- |
| Δv de subida do MAV (com perdas, sem margem) | 4,187 | 5,296 | 4,187 | 4,187 |
| Δv da descida propulsiva (vertical, conservador; só orçamento) | 0,309 | 0,309 | 0,309 | 0,309 |
| Δv captura do lander em 1 sol / saída de órbita (missão A) | — | — | 1,077 / 0,007 | — |
| Velocidade de entrada (missão A / envelope) | 5,76 / 6,04 | 5,76 / 6,04 | 4,71 / 4,71 | 5,76 / 6,04 |
| Δv extra do orbitador: descer até o encontro + saída de Marte (missão A / envelope) | 2,375 / 2,375 | 0,000 / 0,000 | 2,375 / 2,375 | 1,267 / 1,267 |
| MAV: massa na decolagem | 341 | 1 821 | 341 | 341 |
| Massa pousada (MAV + plataforma P-017) | 1 191 | 2 671 | 1 191 | 1 191 |
| Massa de entrada (missão A) | 2 341 | 5 248 | 1 909 | 2 341 |
| Lander na chegada a Marte (missão A / envelope) | 2 341 / 2 341 | 5 248 / 5 248 | 3 264 / 3 821 | 2 341 / 2 341 |
| Orbitador na órbita baixa da Terra: missão A / regra (iii) | 92 936 / 1 109 089 | 13 587 / 22 834 | 92 936 / 1 109 089 | 29 647 / 60 311 |

Referência sem superfície (Fase 1): orbitador de 13 587 kg (missão A) e 22 833 kg (regra iii) na órbita baixa.
S4: a aerofrenagem leva ~205 dias (P-020), dentro da estada em Marte.
