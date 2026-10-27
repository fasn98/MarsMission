"""Propagação kepleriana (dois corpos) por variável universal, com coeficientes de Lagrange.

Formulação de anomalia universal χ e funções de Stumpff C(z), S(z), z = αχ², α = 1/a,
válida para órbitas elípticas, parabólicas e hiperbólicas. Fonte: docs/fontes.md [F11]
(Curtis, *Orbital Mechanics for Engineering Students*, cap. 3, algoritmos de anomalia
universal e de propagação por f e g). Aqui é usada como referência independente do Lambert.
"""

from __future__ import annotations

import numpy as np


def stumpff_c(z: float) -> float:
    if z > 0:
        return (1.0 - np.cos(np.sqrt(z))) / z
    if z < 0:
        return (np.cosh(np.sqrt(-z)) - 1.0) / (-z)
    return 0.5


def stumpff_s(z: float) -> float:
    if z > 0:
        sz = np.sqrt(z)
        return (sz - np.sin(sz)) / sz**3
    if z < 0:
        sz = np.sqrt(-z)
        return (np.sinh(sz) - sz) / sz**3
    return 1.0 / 6.0


def _serie_pequeno_z(z: float) -> tuple[float, float]:
    """C(z) e S(z) por série de Taylor quando |z| é pequeno (evita cancelamento)."""
    c = 0.5 - z / 24.0 + z**2 / 720.0 - z**3 / 40320.0 + z**4 / 3628800.0
    s = 1.0 / 6.0 - z / 120.0 + z**2 / 5040.0 - z**3 / 362880.0 + z**4 / 39916800.0
    return c, s


def _cs(z: float) -> tuple[float, float]:
    if abs(z) < 1e-3:
        return _serie_pequeno_z(z)
    return stumpff_c(z), stumpff_s(z)


def propagar(mu: float, r0, v0, dt: float, max_iter: int = 200, tol: float = 1e-13):
    """Estado (r, v) após `dt` a partir de (r0, v0) no problema de dois corpos."""
    r0 = np.asarray(r0, dtype=float)
    v0 = np.asarray(v0, dtype=float)
    r0n = np.linalg.norm(r0)
    vr0 = r0 @ v0 / r0n
    alpha = 2.0 / r0n - (v0 @ v0) / mu
    smu = np.sqrt(mu)

    # Chute inicial e Newton na equação universal de Kepler em χ.
    chi = smu * abs(alpha) * dt if alpha != 0 else smu * dt / r0n
    if alpha < 0:  # hiperbólica: chute de Vallado para não começar longe demais
        a = 1.0 / alpha
        sinal = np.sign(dt)
        arg = (-2.0 * mu * alpha * dt) / (r0 @ v0 + sinal * np.sqrt(-mu * a) * (1.0 - r0n * alpha))
        chi = sinal * np.sqrt(-a) * np.log(arg) if arg > 0 else chi
    for _ in range(max_iter):
        z = alpha * chi**2
        c, s = _cs(z)
        f = (r0n * vr0 / smu * chi**2 * c + (1.0 - alpha * r0n) * chi**3 * s
             + r0n * chi - smu * dt)
        df = (r0n * vr0 / smu * chi * (1.0 - z * s) + (1.0 - alpha * r0n) * chi**2 * c + r0n)
        passo = f / df
        chi -= passo
        if abs(passo) <= tol * max(1.0, abs(chi)):
            break
    else:
        raise RuntimeError("Newton da equação universal de Kepler não convergiu")

    z = alpha * chi**2
    c, s = _cs(z)
    f = 1.0 - chi**2 / r0n * c
    g = dt - chi**3 / smu * s
    r = f * r0 + g * v0
    rn = np.linalg.norm(r)
    fdot = smu / (rn * r0n) * (z * s - 1.0) * chi
    gdot = 1.0 - chi**2 / rn * c
    v = fdot * r0 + gdot * v0
    return r, v
