"""Espiral de baixo empuxo (Etapa 3.2): solução analítica quase circular (Edelbaum, forma coplanar) e integração
numérica com empuxo contínuo tangente à velocidade, uma conferida contra a outra.

Modelo numérico:
  - corpo central como massa pontual; movimento plano de dois corpos; sem J2, sem sombra, sem terceiro corpo;
  - empuxo sempre tangente à velocidade (a favor dela para subir, contra ela para descer);
  - aceleração constante (como em Schwenzfeger [F113]) ou empuxo constante com massa variável (vazão T / (Isp · g0));
  - a espiral para quando a energia osculadora chega à da órbita circular de raio r1 (semieixo a = r1).

Solução analítica (quase circular, coplanar): com a órbita sempre quase circular, h = −v_c²/2 e dh/dt = a_T · v ≈
a_T · v_c (energia por massa; a equação h' = ε|v| de [F113] p. 3, eq. (1), em tempo físico). Então dv_c = −a_T dt, e o Δv
entregue é Δv = |v_c0 − v_c1| = |√(μ/r0) − √(μ/r1)|, que não depende do perfil de aceleração (derivado aqui). A
atribuição a Edelbaum (1961), como a fórmula dele sem mudança de plano, não foi conferida: o artigo original não foi
consultado (acesso pago), e por isso a forma com mudança de plano não foi implementada.

Unidades: as funções aceitam qualquer sistema coerente (km e s, ou adimensional com μ = 1 e r0 = 1); empuxo em N com
massa em kg só em `espiral` com `empuxo_n`, em km/s².
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

from orbital.config import ler, v
from orbital.foguete import G0

_NUM = ler("config/baixo_empuxo.yaml")["integrador"]   # parâmetros numéricos, premissa P-046 (NÃO VALIDADA)
RTOL, ATOL = v(_NUM["rtol"]), v(_NUM["atol_relativo"])


@dataclass(frozen=True)
class Espiral:
    dv: float               # Δv entregue: a · t (aceleração constante) ou Isp · g0 · ln(m0/mf)
    duracao: float          # tempo de empuxo
    revolucoes: float       # voltas em torno do corpo central
    raio_final: float       # raio no instante em que a energia chega à do alvo (a órbita final é quase circular)
    excentricidade_final: float
    massa_final_kg: float = float("nan")   # só com empuxo constante


def dv_edelbaum_coplanar(mu, r0, r1):
    """Δv da espiral quase circular entre órbitas circulares coplanares de raios r0 e r1 (ver o docstring)."""
    return abs(math.sqrt(mu / r0) - math.sqrt(mu / r1))


def duracao_empuxo_constante(dv_km_s, m0_kg, empuxo_n, isp_s):
    """Tempo de empuxo (s) para entregar dv com empuxo e vazão constantes (equação do foguete)."""
    c = isp_s * G0                      # km/s
    mdot = empuxo_n / (c * 1e3)         # kg/s
    return m0_kg / mdot * (1 - math.exp(-dv_km_s / c))


def espiral(mu, r0, r1, aceleracao=None, empuxo_n=None, isp_s=None, m0_kg=None, t_max=None):
    """Espiral tangencial a partir da órbita circular de raio r0 até a energia da órbita circular de raio r1.

    Aceleração constante (`aceleracao`) ou empuxo constante (`empuxo_n` em N, `isp_s`, `m0_kg`; então μ e r em km).
    Sobe se r1 > r0 e desce se r1 < r0."""
    sentido = 1.0 if r1 > r0 else -1.0
    v0 = math.sqrt(mu / r0)
    massa = aceleracao is None
    if massa:
        c = isp_s * G0
        mdot = empuxo_n / (c * 1e3)
        a_n = empuxo_n * 1e-3             # N → kg·km/s²
        a_ref = a_n / m0_kg
    else:
        a_ref = aceleracao
    if t_max is None:   # folga: o dobro do tempo da solução analítica com a aceleração inicial
        t_max = 2 * dv_edelbaum_coplanar(mu, r0, r1) / a_ref

    def f(t, s):
        x, y, vx, vy = s[:4]
        r3 = (x * x + y * y) ** 1.5
        vel = math.hypot(vx, vy)
        a = sentido * (a_n / s[4] if massa else aceleracao) / vel
        d = [vx, vy, -mu * x / r3 + a * vx, -mu * y / r3 + a * vy]
        return d + [-mdot] if massa else d

    h1 = -mu / (2 * r1)

    def chegou(t, s):
        return 0.5 * (s[2] ** 2 + s[3] ** 2) - mu / math.hypot(s[0], s[1]) - h1
    chegou.terminal = True

    s0 = [r0, 0.0, 0.0, v0] + ([m0_kg] if massa else [])
    escala = [r0, r0, v0, v0] + ([m0_kg] if massa else [])
    sol = solve_ivp(f, (0.0, t_max), s0, method="DOP853", rtol=RTOL, atol=[ATOL * e for e in escala],
                    events=chegou, dense_output=True)
    if not sol.t_events[0].size:
        raise RuntimeError("a espiral não chegou ao alvo dentro do tempo máximo")
    te, se = float(sol.t_events[0][0]), sol.y_events[0][0]
    x, y, vx, vy = se[:4]
    r = math.hypot(x, y)
    # voltas: ângulo desenrolado da solução densa, amostrado finamente o bastante para não pular volta
    tt = np.linspace(0.0, te, max(1000, int(20 * te * math.sqrt(mu / min(r0, r1) ** 3) / (2 * math.pi)) + 1))
    xy = sol.sol(tt)
    voltas = float(np.unwrap(np.arctan2(xy[1], xy[0]))[-1] / (2 * math.pi))
    ev = ((vx * vx + vy * vy) - mu / r) * np.array([x, y]) / mu - (x * vx + y * vy) * np.array([vx, vy]) / mu
    if massa:
        mf = float(se[4])
        dv = c * math.log(m0_kg / mf)
    else:
        mf, dv = float("nan"), aceleracao * te
    return Espiral(dv, te, voltas, r, float(np.hypot(*ev)), mf)


def trajetoria_aceleracao_constante(eps, tempos, rtol=None, metodo="DOP853"):
    """Subida adimensional (μ = 1, r0 = 1, v0 = 1) com aceleração tangencial constante eps, como em [F113] eq. (1)
    a (5). Devolve, em cada tempo, (r, φ, u, v, h) nas variáveis de [F113]: u = r · ṙ, v = r · v_θ, h = energia
    (leitura deduzida das eq. (1), com t' = r; a lista de símbolos da fonte os chama de componentes da velocidade).
    `rtol` e `metodo` só para a conferência de convergência."""
    rtol = RTOL if rtol is None else rtol
    def f(t, s):
        x, y, vx, vy = s
        r3 = (x * x + y * y) ** 1.5
        a = eps / math.hypot(vx, vy)
        return [vx, vy, -x / r3 + a * vx, -y / r3 + a * vy]
    tempos = np.asarray(tempos, dtype=float)
    sol = solve_ivp(f, (0.0, float(tempos.max())), [1.0, 0.0, 0.0, 1.0], method=metodo, rtol=rtol, atol=rtol * ATOL / RTOL,
                    dense_output=True)
    tt = np.unique(np.concatenate([np.linspace(0.0, tempos.max(), int(tempos.max() * 20) + 2), tempos]))
    x, y, vx, vy = sol.sol(tt)
    fi = np.unwrap(np.arctan2(y, x))
    idx = np.searchsorted(tt, tempos)
    out = []
    for i in idx:
        r = math.hypot(x[i], y[i])
        vr, vt = (x[i] * vx[i] + y[i] * vy[i]) / r, (x[i] * vy[i] - y[i] * vx[i]) / r
        out.append({"r": r, "phi": float(fi[i]), "u": r * vr, "v": r * vt, "h": 0.5 * (vr ** 2 + vt ** 2) - 1 / r})
    return out


def trajetoria_em_s(eps, valores_s):
    """O sistema de [F113] eq. (1) integrado na variável independente da fonte, s (t' = r), a partir de (5). Devolve,
    em cada s, (r, φ, u, v, h, t). Serve para comparar a listagem da fonte nos valores de s que ela imprime."""
    def f(s, y):
        r, _, u, vv, h, _ = y
        V = math.hypot(u, vv)
        return [u, vv / r, 1 + 2 * h * r + eps * r * r * u / V, eps * r * r * vv / V, eps * V, r]
    valores_s = np.asarray(valores_s, dtype=float)
    sol = solve_ivp(f, (0.0, float(valores_s.max())), [1.0, 0.0, 0.0, 1.0, -0.5, 0.0], method="DOP853", rtol=RTOL,
                    atol=ATOL, t_eval=valores_s)
    return [dict(zip(("r", "phi", "u", "v", "h", "t"), map(float, y))) for y in sol.y.T]


@dataclass(frozen=True)
class Arcos:
    dv_km_s: float          # Isp · g0 · ln(m0/mf)
    tempo_empuxo_s: float   # soma dos arcos com o motor ligado
    tempo_total_s: float    # do início até o apoapse-alvo (arcos + trechos sem empuxo)
    voltas: int
    massa_final_kg: float
    rp_final_km: float
    ra_final_km: float


def _elementos_planos(mu, x, y, vx, vy):
    """(rp, ra, e, ν, período) da órbita osculadora plana (prograde)."""
    r = math.hypot(x, y)
    v2 = vx * vx + vy * vy
    ex = ((v2 - mu / r) * x - (x * vx + y * vy) * vx) / mu
    ey = ((v2 - mu / r) * y - (x * vx + y * vy) * vy) / mu
    e = math.hypot(ex, ey)
    a = 1 / (2 / r - v2 / mu)
    nu = math.atan2(ex * y - ey * x, ex * x + ey * y) if e > 1e-12 else 0.0
    return a * (1 - e), a * (1 + e), e, nu, 2 * math.pi * math.sqrt(a ** 3 / mu)


def _anomalia_media(e, nu):
    E = 2 * math.atan2(math.sqrt(1 - e) * math.sin(nu / 2), math.sqrt(1 + e) * math.cos(nu / 2))
    return E - e * math.sin(E)


def apoapse_por_arcos(mu, rp, ra, ra_alvo, empuxo_n, isp_s, m0_kg, meio_arco_graus, max_voltas=200000):
    """Muda o apoapse de uma órbita (rp × ra) até ra_alvo com empuxo tangencial só nos arcos |ν| ≤ meio_arco em torno do
    periapse (contra a velocidade para baixar o apoapse, a favor para subir); fora dos arcos, voo kepleriano (exato).
    O periapse também deriva um pouco; o valor final é devolvido. Cada arco é integrado com o mesmo modelo de
    `espiral` (dois corpos, empuxo constante, massa variável)."""
    sentido = 1.0 if ra_alvo > ra else -1.0
    c = isp_s * G0
    mdot = empuxo_n / (c * 1e3)
    a_n = empuxo_n * 1e-3
    th = math.radians(meio_arco_graus)
    a0 = (rp + ra) / 2
    # começa no início do arco (ν = −θ)
    p = a0 * (1 - ((ra - rp) / (ra + rp)) ** 2)
    e = (ra - rp) / (ra + rp)

    def estado(nu, p, e, w=0.0):
        r = p / (1 + e * math.cos(nu))
        h = math.sqrt(mu * p)
        ang = nu + w
        vr, vt = mu / h * e * math.sin(nu), mu / h * (1 + e * math.cos(nu))
        return [r * math.cos(ang), r * math.sin(ang), vr * math.cos(ang) - vt * math.sin(ang),
                vr * math.sin(ang) + vt * math.cos(ang)]

    s = estado(-th, p, e) + [m0_kg]
    t_emp = t_tot = 0.0
    voltas = 0

    def f(t, s):
        x, y, vx, vy, m = s
        r3 = (x * x + y * y) ** 1.5
        vel = math.hypot(vx, vy)
        a = sentido * a_n / m / vel
        return [vx, vy, -mu * x / r3 + a * vx, -mu * y / r3 + a * vy, -mdot]

    def fim_do_arco(t, s):
        return _elementos_planos(mu, *s[:4])[3] - th
    fim_do_arco.terminal, fim_do_arco.direction = True, 1

    def chegou(t, s):
        return _elementos_planos(mu, *s[:4])[1] - ra_alvo
    chegou.terminal = True

    while voltas < max_voltas:
        rp_c, ra_c, e_c, nu_c, per = _elementos_planos(mu, *s[:4])
        dur = per * (2 * th / (2 * math.pi)) * 3 + 10.0   # folga: o evento fecha o arco
        sol = solve_ivp(f, (0.0, dur), s, method="DOP853", rtol=RTOL, atol=[ATOL * rp] * 2 + [ATOL * 10] * 2 + [ATOL * m0_kg],
                        events=(fim_do_arco, chegou))
        s = list(sol.y[:, -1])
        t_emp += sol.t[-1]
        t_tot += sol.t[-1]
        voltas += 1
        if sol.t_events[1].size:
            break
        # voo livre de ν = +θ a ν = −θ (próxima volta), pela equação de Kepler
        rp_c, ra_c, e_c, nu_c, per = _elementos_planos(mu, *s[:4])
        w = math.atan2(s[1], s[0]) - nu_c
        p_c = (rp_c + ra_c) / 2 * (1 - e_c ** 2)
        m1, m2 = _anomalia_media(e_c, nu_c), _anomalia_media(e_c, -th)
        dm_ = (m2 - m1) % (2 * math.pi)
        t_tot += dm_ / (2 * math.pi) * per
        s = estado(-th, p_c, e_c, w) + [s[4]]
    else:
        raise RuntimeError("apoapse_por_arcos não chegou ao alvo")
    rp_f, ra_f, *_ = _elementos_planos(mu, *s[:4])
    return Arcos(c * math.log(m0_kg / s[4]), t_emp, t_tot, voltas, s[4], rp_f, ra_f)
