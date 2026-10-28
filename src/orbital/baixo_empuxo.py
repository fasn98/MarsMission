"""Espiral de baixo empuxo (Etapa 3.2): solução analítica quase circular (Edelbaum, forma coplanar) e integração
numérica com empuxo contínuo tangente à velocidade, uma conferida contra a outra.

Modelo numérico:
  - corpo central como massa pontual; movimento plano de dois corpos; sem J2, sem sombra, sem terceiro corpo;
  - empuxo sempre tangente à velocidade (a favor dela para subir, contra ela para descer);
  - aceleração constante (como em Schwenzfeger [F113]) ou empuxo constante com massa variável (vazão T / (Isp · g0));
  - a espiral para quando a energia osculadora chega à da órbita circular de raio r1 (semieixo a = r1).

Solução analítica (quase circular, coplanar): com a órbita sempre quase circular, h = −v_c²/2 e dh/dt = a_T · v ≈
a_T · v_c (energia por massa; a equação h' = ε|v| de [F113] p. 3, eq. (1), em tempo físico). Então dv_c = −a_T dt, e o Δv
entregue é Δv = |v_c0 − v_c1| = |√(μ/r0) − √(μ/r1)|, que não depende do perfil de aceleração (derivado aqui). É a
fórmula de Edelbaum (1961) sem mudança de plano. O artigo original não foi consultado (acesso pago), e por isso a forma
com mudança de plano não foi implementada.

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


def trajetoria_aceleracao_constante(eps, tempos):
    """Subida adimensional (μ = 1, r0 = 1, v0 = 1) com aceleração tangencial constante eps, como em [F113] eq. (1)
    a (5). Devolve, em cada tempo, (r, φ, u, v, h) nas variáveis de [F113]: u = r · ṙ, v = r · v_θ, h = energia."""
    def f(t, s):
        x, y, vx, vy = s
        r3 = (x * x + y * y) ** 1.5
        a = eps / math.hypot(vx, vy)
        return [vx, vy, -x / r3 + a * vx, -y / r3 + a * vy]
    tempos = np.asarray(tempos, dtype=float)
    sol = solve_ivp(f, (0.0, float(tempos.max())), [1.0, 0.0, 0.0, 1.0], method="DOP853", rtol=RTOL, atol=ATOL,
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
