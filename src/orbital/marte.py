"""Constantes do sistema marciano e distância entre o baricentro e o centro de Marte.

Fontes (docs/fontes.md):
- [F7] GM: cabeçalho da efeméride de satélites MAR099 (JPL), em mar099.cmt (NAIF),
  seção "Bodies on the File". Solução descrita em Brozović, Jacobson & Park (2025),
  AJ 170:42.
- [F8] Elementos orbitais médios (a, e) de Fobos e Deimos: JPL SSD, "Planetary Satellite
  Mean Elements", ephemeris MAR099, época 2000-01-01.5 TDB.
"""

from __future__ import annotations

# [F7] km^3/s^2
GM_FOBOS = 7.087546066894452e-04
GM_DEIMOS = 9.615569648120313e-05
GM_SISTEMA_MARTE = 4.282837566226656e04  # Marte + Fobos + Deimos

# [F8] semieixo maior [km] e excentricidade
A_FOBOS, E_FOBOS = 9375.0, 0.015
A_DEIMOS, E_DEIMOS = 23457.0, 0.000


def deslocamento_baricentro_km(gm_lua: float, a_lua_km: float) -> float:
    """Distância do centro de Marte ao baricentro devida a uma lua, em órbita circular de raio a.

    Pela definição de baricentro, |r_499 - r_4| = (m_lua / m_total) * |r_lua - r_499|,
    com m_lua / m_total = GM_lua / GM_sistema.
    """
    return gm_lua / GM_SISTEMA_MARTE * a_lua_km


def faixa_distancia_baricentro_centro_km() -> tuple[float, float]:
    """Faixa [mín, máx] de |r_499 - r_4| com Fobos e Deimos, em km.

    As duas contribuições são vetores com direções que variam. O máximo ocorre com as luas
    alinhadas, no apoastro (a(1+e)). O mínimo ocorre com as luas opostas, usando o extremo da
    distância que torna a diferença menor.
    """
    f_max = deslocamento_baricentro_km(GM_FOBOS, A_FOBOS * (1 + E_FOBOS))
    f_min = deslocamento_baricentro_km(GM_FOBOS, A_FOBOS * (1 - E_FOBOS))
    d_max = deslocamento_baricentro_km(GM_DEIMOS, A_DEIMOS * (1 + E_DEIMOS))
    d_min = deslocamento_baricentro_km(GM_DEIMOS, A_DEIMOS * (1 - E_DEIMOS))
    return max(f_min - d_max, 0.0), f_max + d_max
