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


# Parada do Newton no piso de ruído (decisão do Fabio, 2026-11-26): além de |passo| ≤ tol·max(1, |χ|), o Newton para quando
# o passo relativo já passou por PISO e deixou de diminuir, porque daí em diante ele é arredondamento e o tol pode nunca ser
# atingido, conforme a CPU (CI da main em 86b39e9). Nessa parada, o resíduo de f é conferido contra PISO vezes a soma dos
# módulos dos termos da equação; acima disso (ou NaN), o Newton falha. Valores: P-127 (NÃO VALIDADA).
PISO = 1e-12


def _termos(r0n, vr0, smu, alpha, chi, c, s, dt):
    """Os quatro termos da equação universal de Kepler, cuja soma é f."""
    return (r0n * vr0 / smu * chi**2 * c, (1.0 - alpha * r0n) * chi**3 * s, r0n * chi, -smu * dt)


def _derivada(r0n, vr0, smu, alpha, chi, z, c, s):
    """df/dχ da equação universal de Kepler."""
    return r0n * vr0 / smu * chi * (1.0 - z * s) + (1.0 - alpha * r0n) * chi**2 * c + r0n


def _residuo_ok(t) -> bool:
    """Resíduo de f na parada pelo piso: |Σ termos| ≤ PISO · Σ |termos| em todas as faixas (NaN reprova)."""
    return bool(np.all(np.abs(sum(t)) <= PISO * sum(np.abs(x) for x in t)))


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
    passou, anterior = False, np.inf
    for _ in range(max_iter):
        z = alpha * chi**2
        c, s = _cs(z)
        f = sum(_termos(r0n, vr0, smu, alpha, chi, c, s, dt))
        df = _derivada(r0n, vr0, smu, alpha, chi, z, c, s)
        passo = f / df
        chi -= passo
        if abs(passo) <= tol * max(1.0, abs(chi)):
            break
        if passou and abs(passo) >= anterior:   # piso de ruído
            c, s = _cs(alpha * chi**2)
            t = _termos(r0n, vr0, smu, alpha, chi, c, s, dt)
            if not _residuo_ok(t):
                raise RuntimeError("Newton da equação universal de Kepler parou no piso de ruído com resíduo acima do limite")
            break
        passou = passou or abs(passo) <= PISO * max(1.0, abs(chi))
        anterior = abs(passo)
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


def _cs_lote(z):
    """C(z) e S(z) vetorizados, com a série de Taylor para |z| < 1e-3 (como `_cs`)."""
    z = np.asarray(z, dtype=float)
    c = np.empty_like(z)
    s = np.empty_like(z)
    pe = np.abs(z) < 1e-3
    zp = z[pe]
    c[pe] = 0.5 - zp / 24.0 + zp**2 / 720.0 - zp**3 / 40320.0 + zp**4 / 3628800.0
    s[pe] = 1.0 / 6.0 - zp / 120.0 + zp**2 / 5040.0 - zp**3 / 362880.0 + zp**4 / 39916800.0
    el = (~pe) & (z > 0)
    sz = np.sqrt(z[el])
    c[el] = (1.0 - np.cos(sz)) / z[el]
    s[el] = (sz - np.sin(sz)) / sz**3
    hi = (~pe) & (z < 0)
    sz = np.sqrt(-z[hi])
    c[hi] = (np.cosh(sz) - 1.0) / (-z[hi])
    s[hi] = (np.sinh(sz) - sz) / sz**3
    return c, s


def propagar_lote(mu: float, r0, v0, dt, max_iter: int = 200, tol: float = 1e-13):
    """`propagar` vetorizado: r0 e v0 com forma (k, 3), dt escalar ou (k,). Mesmas equações, Newton em paralelo."""
    r0 = np.atleast_2d(np.asarray(r0, dtype=float))
    v0 = np.atleast_2d(np.asarray(v0, dtype=float))
    dt = np.broadcast_to(np.asarray(dt, dtype=float), (len(r0),)).copy()
    r0n = np.linalg.norm(r0, axis=1)
    rv = np.einsum("ij,ij->i", r0, v0)
    vr0 = rv / r0n
    alpha = 2.0 / r0n - np.einsum("ij,ij->i", v0, v0) / mu
    smu = np.sqrt(mu)
    chi = np.where(alpha != 0, smu * np.abs(alpha) * dt, smu * dt / r0n)
    hip = alpha < 0
    if np.any(hip):
        a = 1.0 / alpha[hip]
        sinal = np.sign(dt[hip])
        arg = (-2.0 * mu * alpha[hip] * dt[hip]) / (rv[hip] + sinal * np.sqrt(-mu * a) * (1.0 - r0n[hip] * alpha[hip]))
        with np.errstate(invalid="ignore"):
            chute = sinal * np.sqrt(-a) * np.log(np.where(arg > 0, arg, 1.0))
        chi[hip] = np.where(arg > 0, chute, chi[hip])
    ativo = np.ones(len(r0), dtype=bool)
    passou = np.zeros(len(r0), dtype=bool)
    no_piso = np.zeros(len(r0), dtype=bool)
    anterior = np.full(len(r0), np.inf)
    for _ in range(max_iter):
        z = alpha * chi**2
        c, s = _cs_lote(z)
        f = sum(_termos(r0n, vr0, smu, alpha, chi, c, s, dt))
        df = _derivada(r0n, vr0, smu, alpha, chi, z, c, s)
        passo = np.where(ativo, f / df, 0.0)
        chi = chi - passo
        ap, escala = np.abs(passo), np.maximum(1.0, np.abs(chi))
        piso = ativo & passou & (ap >= anterior) & ~(ap <= tol * escala)
        no_piso |= piso
        ativo = ativo & ~(ap <= tol * escala) & ~piso
        passou |= ap <= PISO * escala
        anterior = np.where(ativo, ap, anterior)
        if not np.any(ativo):
            break
    else:
        raise RuntimeError("Newton da equação universal de Kepler não convergiu")
    if np.any(no_piso):
        c, s = _cs_lote(alpha[no_piso] * chi[no_piso] ** 2)
        t = _termos(r0n[no_piso], vr0[no_piso], smu, alpha[no_piso], chi[no_piso], c, s, dt[no_piso])
        if not _residuo_ok(t):
            raise RuntimeError("Newton da equação universal de Kepler parou no piso de ruído com resíduo acima do limite")
    z = alpha * chi**2
    c, s = _cs_lote(z)
    f = 1.0 - chi**2 / r0n * c
    g = dt - chi**3 / smu * s
    r = f[:, None] * r0 + g[:, None] * v0
    rn = np.linalg.norm(r, axis=1)
    fdot = smu / (rn * r0n) * (z * s - 1.0) * chi
    gdot = 1.0 - chi**2 / rn * c
    v = fdot[:, None] * r0 + gdot[:, None] * v0
    return r, v
