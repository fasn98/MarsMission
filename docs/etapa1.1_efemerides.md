# Etapa 1.1 — Efemérides: fonte e verificação

## Fonte

- Efemérides planetárias JPL **DE440**, descritas em: Park, R. S.; Folkner, W. M.; Williams, J. G.;
  Boggs, D. H. *The JPL Planetary and Lunar Ephemerides DE440 and DE441*. The Astronomical Journal,
  161(3):105, 2021. doi:10.3847/1538-3881/abd414 (docs/fontes.md [F1]).
- Arquivo usado: `de440s.bsp` (NAIF), a mesma solução DE440 no intervalo 1849-12-25 a 2150-01-21.
  MD5 conferido contra o checksum publicado pelo NAIF. Decisão no ADR 0002.
- Leap seconds `naif0012.tls` [F2]. Acesso via spiceypy 8.3.0 / CSPICE N0067 [F4, F5].
- O arquivo traz os baricentros dos sistemas planetários. Para Marte, o corpo disponível é o
  **baricentro do sistema marciano (NAIF 4)**, não o centro de Marte (499). Para trajetórias
  heliocêntricas isso é o adequado. Numa consulta exploratória ao Horizons (2028-01-01 TDB), os
  alvos 499 e 4 diferiram em ~41 m na coordenada X. Esse valor não foi investigado nem está nos
  testes. Se uma etapa futura precisar do centro de Marte, será preciso
  um kernel de satélites marcianos (por exemplo `mar099.bsp`), e essa decisão fica para então.

## Verificação contra o JPL Horizons

Vetores geométricos heliocêntricos (centro: Sol, 10), frame ICRF, tempo TDB, obtidos da API do
Horizons por `tools/fetch_horizons_reference.py` em 2026-10-26 e guardados sem edição em
`tests/data/horizons/`. O teste é `tests/test_ephemeris.py`.

| Corpo | Época (TDB) | \|Δr\| | \|Δv\| |
| :- | :- | -: | -: |
| Baricentro de Marte (4) | 2028-01-01 00:00 | 3,3e-5 m | 5e-15 km/s |
| Baricentro de Marte (4) | 2033-06-15 00:00 | 6,0e-5 m | 4e-16 km/s |
| Terra (399) | 2028-01-01 00:00 | 0,028 m | 7e-11 km/s |

Tolerâncias usadas no teste: 1 km e 1e-6 km/s (premissas P-001 e P-002, NÃO VALIDADAS).

Troca de `de440.bsp` para `de440s.bsp` (ADR 0002): a tabela acima é a mesma com os dois arquivos.
Nas três épocas, a maior diferença entre os estados calculados com um e com outro é 0,0, isto é,
idênticos bit a bit.

### Como interpretar

- O Horizons declara **DE441** como fonte; usamos **DE440**. Para o baricentro de Marte a
  concordância é de dezenas de micrômetros, no nível do arredondamento numérico. A explicação mais
  provável é que, nesse intervalo, as duas soluções coincidem para esse corpo. Não encontrei uma
  afirmação publicada que confirme isso exatamente. Na prática, este teste verifica o **pipeline**
  (frame, escala de tempo, unidades, códigos de corpo, leitura do kernel). Ele **não** mede de forma
  independente a exatidão da DE440 frente às observações; isso é o objeto de Park et al. (2021).
- Os 2,8 cm da Terra ficam muito abaixo de qualquer efeito relevante para porkchop plots.
  A origem não foi investigada.
- A tolerância de 1 km detecta os erros de pipeline mais prováveis: UTC no lugar de TDB
  (~69 s × ~24 km/s ≈ 1600 km), frame eclíptico no lugar do equatorial e unidade errada.
