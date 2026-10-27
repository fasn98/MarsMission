"""Plataformas (Etapa 2.3): eclipse, baterias, painéis solares e margem de crescimento de massa.

Eclipse: sombra cilíndrica de raio igual ao raio equatorial do planeta, com o Sol no plano da órbita
(ângulo beta = 0), varrendo a direção do Sol. É o pior caso geométrico: ignora a penumbra e a
precessão da linha das apsides, e por isso superestima a duração.
"""

from __future__ import annotations

import numpy as np


def eclipse_maximo(mu, raio, rp, ra, n_tempo=20001, passo_graus=0.5):
    """(maior duração de eclipse [s], período [s]) para a órbita rp × ra (raios, km)."""
    a = 0.5 * (rp + ra)
    e = (ra - rp) / (ra + rp)
    periodo = 2 * np.pi * np.sqrt(a**3 / mu)
    m = np.linspace(0.0, 2 * np.pi, n_tempo, endpoint=False)
    ex = m.copy()
    for _ in range(60):  # equação de Kepler por Newton
        ex = ex - (ex - e * np.sin(ex) - m) / (1 - e * np.cos(ex))
    x = a * (np.cos(ex) - e)
    y = a * np.sqrt(1 - e * e) * np.sin(ex)
    pior = 0.0
    for th in np.radians(np.arange(0.0, 360.0, passo_graus)):
        ao_longo = x * np.cos(th) + y * np.sin(th)
        perp = np.abs(-x * np.sin(th) + y * np.cos(th))
        pior = max(pior, float(np.mean((ao_longo < 0) & (perp < raio))))
    return pior * periodo, periodo


def bateria(energia_wh, profundidade_descarga, energia_especifica_wh_kg):
    """(capacidade nominal [Wh], massa [kg]) para fornecer `energia_wh` sem passar da profundidade de descarga."""
    cap = energia_wh / profundidade_descarga
    return cap, cap / energia_especifica_wh_kg


def potencia_painel(carga_w, t_sol_s, t_eclipse_s, eficiencia_recarga):
    """Potência do painel [W] para a carga no sol e para recarregar a energia gasta no eclipse."""
    return carga_w + carga_w * t_eclipse_s / (eficiencia_recarga * t_sol_s)


def massa_painel(potencia_w, w_kg_1ua, distancia_ua, fator_perdas):
    """Massa do painel [kg]: potência específica a 1 UA escalada pelo inverso do quadrado da distância."""
    return potencia_w / (w_kg_1ua * fator_perdas / distancia_ua**2)


def com_margem(massa_basica, mga):
    """Massa prevista = básica × (1 + MGA), como no AIAA S-120A (a MGA incide sobre a massa básica)."""
    return massa_basica * (1.0 + mga)
