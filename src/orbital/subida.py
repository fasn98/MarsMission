"""Subida do MAV em Marte (portão da rota A, 2026-11-07): Δv até 100 × 100 km com o empuxo/peso real.

Modelo:
  - Plano equatorial, lançamento rumo leste a 0° de latitude, como no caso de [F37] Tab. 1; Marte esférico (μ e raio do
    config), girando com o período do config; a atmosfera gira com Marte.
  - Atmosfera do NASA Glenn ([F245]), com densidade nula acima de h_topo (o ajuste leva T a 0 K perto de 112 km). NÃO VALIDADA.
  - Arrasto com coeficiente constante sobre a área da seção (premissa da subida); sem sustentação.
  - Empuxo no vácuo; a perda por pressão no bocal fica de fora (ver tools/subida_mav.py).
  - Guiamento: subida vertical por t_v, depois ângulo de empuxo sobre a horizontal local com tan θ = tan θ0 − c (t − t_v)
    (linear-tangente).
  - Inserção direta, com queima contínua: corte quando a energia chega à da circular de raio R + h; θ0 e c zeram os resíduos
    de altitude e de velocidade radial no corte; t_v percorre uma grade e fica o de menor Δv.
  - Δv = Σ Isp g0 ln(m0/mf) das queimas.
Unidades: m, s, kg, N.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from scipy.integrate import solve_ivp

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


def voa(pl, estagios, area_cd, atm, guia, h_alvo, rtol=1e-8, atol=1e-6, max_step=2.0):
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
        sol = solve_ivp(_deriv(pl, est, area_cd, atm, guia), (t0, t0 + dur), s, rtol=rtol, atol=atol, events=[ev_energia, ev_chao], max_step=max_step)
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


def otimiza(pl, estagios, area_cd, atm, h_alvo, grade, limites, tol_m=1.0, tol_m_s=0.1, n_melhores=3, integrador=None):
    """Guiamento de menor Δv que insere em 100 × 100 km. Para cada t_v da grade, uma grade grosseira de (θ0, c) dá os pontos
    de partida, e mínimos quadrados zeram os resíduos de altitude e de velocidade radial no corte; fica o menor Δv."""
    from scipy.optimize import least_squares
    (th_lo, th_hi), (c_lo, c_hi) = limites[1], limites[2]
    kw = {} if integrador is None else {"rtol": integrador["rtol"], "atol": integrador["atol"], "max_step": integrador["max_step_s"]}
    melhor = None
    for tv in grade["t_v_s"]:
        def res(x, tv=tv):
            r = voa(pl, estagios, area_cd, atm, (tv, x[0], x[1]), h_alvo, **kw)
            return [r["residuo"][0] / 1000.0, r["residuo"][1] / 10.0]
        pontos = sorted(((sum(e * e for e in res((th, c))), th, c) for th in grade["theta0_rad"] for c in grade["c_1_s"]))[:n_melhores]
        for _, th0, c in pontos:
            ls = least_squares(res, [th0, c], bounds=([th_lo, c_lo], [th_hi, c_hi]), xtol=1e-12, ftol=1e-12, gtol=1e-12)
            r = voa(pl, estagios, area_cd, atm, (tv, ls.x[0], ls.x[1]), h_alvo, **kw)
            ok = r["chegou"] and abs(r["residuo"][0]) <= tol_m and abs(r["residuo"][1]) <= tol_m_s
            if ok and (melhor is None or r["dv_m_s"] < melhor["dv_m_s"]):
                melhor = {**r, "guia": {"t_v_s": tv, "theta0_graus": math.degrees(ls.x[0]), "c_1_s": float(ls.x[1])}}
    return melhor


def dv_ideal(pl, h_alvo):
    """Δv ideal, sem perdas, da superfície no equador (girando com Marte) até a circular de raio R + h: Hohmann impulsiva
    rumo leste, com a velocidade de rotação descontada na primeira queima."""
    r1, r2 = pl.raio, pl.raio + h_alvo
    vp = math.sqrt(pl.mu * 2 * r2 / (r1 * (r1 + r2)))
    return (vp - pl.omega * r1) + (math.sqrt(pl.mu / r2) - vp * r1 / r2)



def omega_efetivo(omega, inclinacao_graus):
    """Rotação efetiva no plano da órbita: ω R cos φ sen Az = ω R cos i, com sen Az = cos i / cos φ (lançamento direto na
    inclinação i a partir da latitude φ ≤ i). No modelo plano, a superfície e a atmosfera giram com ω cos i."""
    return omega * math.cos(math.radians(inclinacao_graus))


def vetor_excentricidade(pl, s):
    """Semieixo maior (m) e componentes do vetor excentricidade no referencial local (radial e transversal) do estado plano
    s = [r, θ, vr, vt, m]: funções suaves do estado, sem a quina de |e| em e = 0."""
    r, _, vr, vt, _ = s
    e = (vr * vr + vt * vt) / 2 - pl.mu / r
    return {"semieixo_m": -pl.mu / (2 * e) if e < 0 else math.inf, "ecc_radial": r * vt * vt / pl.mu - 1.0, "ecc_transversal": r * vt * vr / pl.mu}


def elementos(pl, s):
    """(altitude do periapse, altitude do apoapse) em m do estado plano s = [r, θ, vr, vt, m]."""
    r, _, vr, vt, _ = s
    e = (vr * vr + vt * vt) / 2 - pl.mu / r
    if e >= 0:
        return math.inf, math.inf
    a = -pl.mu / (2 * e)
    ecc = math.sqrt(max(0.0, 1 + 2 * e * (r * vt) ** 2 / pl.mu ** 2))
    return a * (1 - ecc) - pl.raio, a * (1 + ecc) - pl.raio


def voa_solido(pl, estagios, inertes, area_cd, atm, guia, t_antes, rtol=1e-9, atol=1e-6, max_step=1.0, max_step_costa=5.0):
    """Motor sólido de dois estágios, sem corte: o 1º queima até esgotar com o guiamento linear-tangente, o veículo descarta o
    inerte do 1º e costa; o 2º acende t_antes segundos antes do apoapse da costa e queima até esgotar, com empuxo na
    horizontal local. A antecedência t_antes é um parâmetro livre, ajustado; [F249] PDF p. 9 descreve a lógica de voo
    (acender no apoapse ou antes, quando o Δv que falta iguala o do 2º), que o modelo não implementa.
    Devolve as altitudes finais do periapse e do apoapse (m), a costa (s) e a massa no fim, ou None se o veículo cai."""
    e1, e2 = estagios
    s = [pl.raio, 0.0, 0.0, pl.omega * pl.raio, e1.massa_inicial_kg]
    dur1 = e1.propelente_kg / (e1.empuxo_n / (e1.isp_s * G0_M))
    sol = solve_ivp(_deriv(pl, e1, area_cd, atm, guia), (0.0, dur1), s, rtol=rtol, atol=atol, max_step=max_step)
    s = list(sol.y[:, -1])
    if s[0] < pl.raio + 1000.0 or s[2] <= 0:
        return None
    s[4] -= inertes[0]
    costa = Estagio(1.0, 0.0, 0.0, 1.0)

    def apo(t, y):
        return y[2]
    apo.terminal, apo.direction = True, -1
    sol = solve_ivp(_deriv(pl, costa, area_cd, atm, guia), (dur1, dur1 + 1.0e4), s, rtol=rtol, atol=atol, events=apo, dense_output=True, max_step=max_step_costa)
    if not sol.t_events[0].size:
        return None
    t_apo = sol.t[-1]
    t_ign = max(dur1, t_apo - t_antes)
    s = list(sol.sol(t_ign))
    dur2 = e2.propelente_kg / (e2.empuxo_n / (e2.isp_s * G0_M))
    mdot2 = e2.empuxo_n / (e2.isp_s * G0_M)

    def horizontal(t, y):
        r, _, vr, vt, m = y
        return [vr, vt / r, vt * vt / r - pl.mu / (r * r), -vr * vt / r + e2.empuxo_n / m, -mdot2]
    sol = solve_ivp(horizontal, (t_ign, t_ign + dur2), s, rtol=rtol, atol=atol, max_step=max_step)
    s = list(sol.y[:, -1])
    p, a = elementos(pl, s)
    return {"periapse_m": p, "apoapse_m": a, "costa_s": t_ign - dur1, "massa_final_kg": s[4], "queima_1_s": dur1, "queima_2_s": dur2, **vetor_excentricidade(pl, s)}


def ajusta_solido(pl, estagios, inertes, area_cd, atm, h_alvo, t_v, partidas, limites, escala_m=1.0e4, integrador=None, residuo="suave"):
    """Guiamento (θ0, c) e antecedência da ignição do 2º que levam o sólido à circular de altitude h_alvo; mínimos quadrados
    a partir de cada ponto de partida. `integrador` ({rtol, atol, max_step_s, max_step_costa_s}) troca os do `voa_solido`.
    Resíduos ("suave", o padrão desde 2026-11-11): semieixo maior menos o raio-alvo e as duas componentes do vetor
    excentricidade vezes o raio-alvo, funções suaves do estado. A forma antiga ("apses": periapse e apoapse menos o alvo)
    tem uma quina em e = 0, exatamente no alvo circular, e o ajuste parava em custos espalhados entre 1e-9 e 4e-4
    (results/conferencia/ruido_subida.md); fica só para o diagnóstico.
    Devolve (custo, voo, parâmetros): custo ~0 quando a órbita é alcançada."""
    from scipy.optimize import least_squares
    kw = {} if integrador is None else {"rtol": integrador["rtol"], "atol": integrador["atol"], "max_step": integrador["max_step_s"], "max_step_costa": integrador["max_step_costa_s"]}
    melhor = None
    for x0 in partidas:
        def res(x):
            r = voa_solido(pl, estagios, inertes, area_cd, atm, (t_v, x[0], x[1]), x[2], **kw)
            if residuo == "apses":
                if r is None:
                    return [1.0e3, 1.0e3]
                return [(r["periapse_m"] - h_alvo) / escala_m, (r["apoapse_m"] - h_alvo) / escala_m]
            if r is None:
                return [1.0e3, 1.0e3, 1.0e3]
            r_alvo = pl.raio + h_alvo
            return [(min(r["semieixo_m"], 1.0e9) - r_alvo) / escala_m, r["ecc_radial"] * r_alvo / escala_m, r["ecc_transversal"] * r_alvo / escala_m]
        ls = least_squares(res, x0, bounds=([b[0] for b in limites], [b[1] for b in limites]))
        if melhor is None or ls.cost < melhor[0]:
            melhor = (ls.cost, ls.x)
    x = melhor[1]
    return melhor[0], voa_solido(pl, estagios, inertes, area_cd, atm, (t_v, x[0], x[1]), x[2], **kw), {"t_v_s": t_v, "theta0_graus": math.degrees(x[0]), "c_1_s": float(x[1]), "t_antes_apoapse_s": float(x[2])}
