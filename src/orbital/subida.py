"""Subida do MAV em Marte (portão da rota A, 2026-11-07): Δv até 100 × 100 km com o empuxo/peso real.

Modelo:
  - Plano equatorial, lançamento rumo leste a 0° de latitude, como no caso de [F37] Tab. 1; Marte esférico (μ e raio do
    config), girando com o período do config; a atmosfera gira com Marte.
  - Atmosfera do NASA Glenn ([F245]), com densidade nula acima de h_topo (o ajuste leva T a 0 K perto de 112 km). NÃO VALIDADA.
  - Arrasto com coeficiente constante sobre a área da seção (premissa da subida); sem sustentação.
  - Empuxo no vácuo; a perda por pressão no bocal fica de fora (ver tools/subida_mav.py).
  - Guiamento: subida vertical por t_v, depois ângulo de empuxo sobre a horizontal local com tan θ = tan θ0 − c (t − t_v)
    (linear-tangente). Corte quando o apoapse chega ao alvo; costa sem arrasto até o apoapse e circularização impulsiva.
  - Os três parâmetros do guiamento minimizam o Δv total, como o POST de [F37] maximiza a massa no fim da queima.
  - Δv = Σ Isp g0 ln(m0/mf) das queimas + Δv da circularização.
Unidades: m, s, kg, N.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

from orbital.foguete import G0

G0_M = G0 * 1000.0   # foguete.G0 está em km/s²


@dataclass
class Estagio:
    massa_inicial_kg: float
    propelente_kg: float
    empuxo_n: float      # empuxo total no vácuo do estágio
    isp_s: float


@dataclass
class Planeta:
    mu: float            # m³/s²
    raio: float          # m
    omega: float         # rad/s


def atmosfera(h, atm):
    """Densidade (kg/m³) do ajuste do NASA Glenn [F245]: T em °C e p em kPa, h em m; zero acima de h_topo_m."""
    h = max(h, 0.0)
    if h > atm["h_topo_m"]:
        return 0.0
    t = atm["t0_baixa_c"] + atm["dtdh_baixa"] * h if h <= atm["h_troca_m"] else atm["t0_alta_c"] + atm["dtdh_alta"] * h
    tk = t + atm["kelvin"]
    if tk <= 0:
        return 0.0
    return atm["p0_kpa"] * math.exp(-atm["k_1_m"] * h) / (atm["r_kpa"] * tk)


def _deriv(pl, est, area_cd, atm, guia):
    t_v, th0, c = guia
    mdot = est.empuxo_n / (est.isp_s * G0_M)

    def f(t, s):
        r, _, vr, vt, m = s
        if t < t_v:
            th = math.pi / 2
        else:
            th = math.atan(math.tan(th0) - c * (t - t_v))
        a_t = est.empuxo_n / m
        vrel_r, vrel_t = vr, vt - pl.omega * r
        vrel = math.hypot(vrel_r, vrel_t)
        rho = atmosfera(r - pl.raio, atm)
        d = 0.5 * rho * vrel * area_cd / m
        ar = a_t * math.sin(th) - d * vrel_r
        at = a_t * math.cos(th) - d * vrel_t
        return [vr, vt / r, vt * vt / r - pl.mu / (r * r) + ar, -vr * vt / r + at, -mdot]
    return f


def voa(pl, estagios, area_cd, atm, guia, h_alvo, rtol=1e-8):
    """Simula a subida com queima contínua até a energia da circular de raio R + h_alvo. Devolve Δv, estado no corte e
    os resíduos de altitude (m) e de velocidade radial (m/s) em relação à circular."""
    r_alvo = pl.raio + h_alvo
    e_alvo = -pl.mu / (2 * r_alvo)
    s = [pl.raio, 0.0, 0.0, pl.omega * pl.raio, estagios[0].massa_inicial_kg]
    t0, dv, h_max = 0.0, 0.0, 0.0
    for i, est in enumerate(estagios):
        if i > 0:
            s[4] = est.massa_inicial_kg
        m_in = s[4]
        dur = est.propelente_kg / (est.empuxo_n / (est.isp_s * G0_M))

        def ev_energia(t, y):
            return (y[2] ** 2 + y[3] ** 2) / 2 - pl.mu / y[0] - e_alvo
        ev_energia.terminal, ev_energia.direction = True, 1

        def ev_chao(t, y):
            return y[0] - pl.raio + 1.0 if t > 1.0 else 1.0
        ev_chao.terminal, ev_chao.direction = True, -1
        sol = solve_ivp(_deriv(pl, est, area_cd, atm, guia), (t0, t0 + dur), s, rtol=rtol, atol=1e-6, events=[ev_energia, ev_chao], max_step=2.0)
        s = list(sol.y[:, -1])
        h_max = max(h_max, float(sol.y[0].max()) - pl.raio)
        dv += est.isp_s * G0_M * math.log(m_in / s[4])
        t0 = sol.t[-1]
        if sol.t_events[1].size:
            # resíduo contínuo: quanto faltou de altitude, mais uma faixa fixa, para o ajuste não ver um degrau
            return {"chegou": False, "motivo": "caiu", "dv_m_s": dv, "residuo": [h_max - (r_alvo - pl.raio) - 2 * (r_alvo - pl.raio), -abs(s[2]) - 500.0]}
        if sol.t_events[0].size:
            return {"chegou": True, "dv_m_s": dv, "t_corte_s": t0, "estagio_no_corte": i + 1, "massa_no_corte_kg": s[4], "propelente_restante_kg": est.propelente_kg - (m_in - s[4]),
                    "altitude_corte_m": s[0] - pl.raio, "vr_corte_m_s": s[2], "residuo": [(s[0] - r_alvo), s[2]]}
    return {"chegou": False, "motivo": "faltou propelente", "dv_m_s": dv, "residuo": [s[0] - r_alvo, s[2]]}


def otimiza(pl, estagios, area_cd, atm, h_alvo, grade, limites, tol_m=1.0, tol_m_s=0.1, n_melhores=3):
    """Guiamento de menor Δv que insere em 100 × 100 km. Para cada t_v da grade, uma grade grosseira de (θ0, c) dá os pontos
    de partida, e mínimos quadrados zeram os resíduos de altitude e de velocidade radial no corte; fica o menor Δv."""
    from scipy.optimize import least_squares
    (th_lo, th_hi), (c_lo, c_hi) = limites[1], limites[2]
    melhor = None
    for tv in grade["t_v_s"]:
        def res(x, tv=tv):
            r = voa(pl, estagios, area_cd, atm, (tv, x[0], x[1]), h_alvo)
            return [r["residuo"][0] / 1000.0, r["residuo"][1] / 10.0]
        pontos = sorted(((sum(e * e for e in res((th, c))), th, c) for th in grade["theta0_rad"] for c in grade["c_1_s"]))[:n_melhores]
        for _, th0, c in pontos:
            ls = least_squares(res, [th0, c], bounds=([th_lo, c_lo], [th_hi, c_hi]), xtol=1e-12, ftol=1e-12, gtol=1e-12)
            r = voa(pl, estagios, area_cd, atm, (tv, ls.x[0], ls.x[1]), h_alvo)
            ok = r["chegou"] and abs(r["residuo"][0]) <= tol_m and abs(r["residuo"][1]) <= tol_m_s
            if ok and (melhor is None or r["dv_m_s"] < melhor["dv_m_s"]):
                melhor = {**r, "guia": {"t_v_s": tv, "theta0_graus": math.degrees(ls.x[0]), "c_1_s": float(ls.x[1])}}
    return melhor
