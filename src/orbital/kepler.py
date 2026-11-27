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


# Newton protegido por bisseção (decisão do Fabio, 2026-11-26, 21h). Em f(χ) = Σ termos, f(0) = −√μ·dt e df/dχ = r > 0:
# f é estritamente crescente, a raiz é única e tem o sinal de dt. O intervalo [lo, hi] que contém a raiz começa em 0 e no
# chute, e o lado aberto é dobrado até f mudar de sinal. A cada iteração, o χ avaliado vira extremo do intervalo; quando o
# passo de Newton sai do intervalo, o passo é a bisseção. Parada: o tol de sempre; se o intervalo não encolhe mais
# (extremos vizinhos em ponto flutuante), o resíduo de f é conferido e, acima do limite (ou NaN), o Newton falha.
# Valores do tol e do resíduo: P-128 (NÃO VALIDADA). Substitui o piso de ruído da P-127, revertido (ver a errata dela).
RESIDUO = 1e-12


def _termos(r0n, vr0, smu, alpha, chi, c, s, dt):
    """Os quatro termos da equação universal de Kepler, cuja soma é f."""
    return (r0n * vr0 / smu * chi**2 * c, (1.0 - alpha * r0n) * chi**3 * s, r0n * chi, -smu * dt)


def _derivada(r0n, vr0, smu, alpha, chi, z, c, s):
    """df/dχ da equação universal de Kepler (igual a r, o raio no instante de χ)."""
    return r0n * vr0 / smu * chi * (1.0 - z * s) + (1.0 - alpha * r0n) * chi**2 * c + r0n


def _residuo_ok(t) -> bool:
    """Resíduo de f com o intervalo esgotado: |Σ termos| ≤ RESIDUO · Σ |termos| em todas as faixas (NaN reprova)."""
    return bool(np.all(np.abs(sum(t)) <= RESIDUO * sum(np.abs(x) for x in t)))


ERRO_RESIDUO = "Newton da equação universal de Kepler esgotou o intervalo com resíduo acima do limite"
ERRO_INTERVALO = "Newton da equação universal de Kepler não achou o intervalo que contém a raiz"


def _intervalo(f, chi, dt, reserva, max_iter):
    """[lo, hi] que contém a raiz: f(lo) < 0 ≤ f(hi) com dt > 0, f(lo) ≤ 0 < f(hi) com dt < 0, lo = hi = 0 com dt = 0. Um
    extremo é 0 (f(0) = −√μ·dt) e o outro sai do chute,
    dobrado até f mudar de sinal. Chute com o sinal errado ou nulo (o log do chute hiperbólico pode dar isso) é trocado
    pela `reserva` √μ·dt/r0, que tem o sinal de dt."""
    sinal = np.sign(dt)
    if sinal == 0:
        return 0.0, 0.0
    b, perto = (chi if sinal * chi > 0 else reserva), 0.0
    for _ in range(max_iter):
        fb = f(b)
        if np.isnan(fb):
            raise RuntimeError(ERRO_INTERVALO)
        if sinal * fb >= 0:
            return (perto, b) if sinal > 0 else (b, perto)
        perto, b = b, 2.0 * b
    raise RuntimeError(ERRO_INTERVALO)


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
    lo, hi = _intervalo(lambda x: sum(_termos(r0n, vr0, smu, alpha, x, *_cs(alpha * x**2), dt)), chi, dt, smu * dt / r0n,
                        max_iter)
    for _ in range(max_iter):
        z = alpha * chi**2
        c, s = _cs(z)
        t = _termos(r0n, vr0, smu, alpha, chi, c, s, dt)
        f = sum(t)
        df = _derivada(r0n, vr0, smu, alpha, chi, z, c, s)
        if f < 0:
            lo = max(lo, chi)
        elif f > 0:
            hi = min(hi, chi)
        passo = f / df
        novo = chi - passo
        if abs(passo) <= tol * max(1.0, abs(novo)):
            chi = novo
            break
        if not lo < novo < hi:   # Newton saiu do intervalo (ou não é número): bisseção
            novo = 0.5 * (lo + hi)
            if not lo < novo < hi:   # extremos vizinhos: o intervalo não encolhe mais
                if not _residuo_ok(t):
                    raise RuntimeError(ERRO_RESIDUO)
                break
            if abs(novo - chi) <= tol * max(1.0, abs(novo)):
                chi = novo
                break
        chi = novo
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


def _intervalo_lote(f, chi, dt, reserva, max_iter):
    """`_intervalo` vetorizado."""
    sinal = np.sign(dt)
    b = np.where(sinal * chi > 0, chi, reserva)
    perto = np.zeros_like(b)
    busca = sinal != 0
    for _ in range(max_iter):
        fb = f(b)
        if np.any(busca & np.isnan(fb)):
            raise RuntimeError(ERRO_INTERVALO)
        busca = busca & (sinal * fb < 0)
        if not np.any(busca):
            return np.where(sinal > 0, perto, b), np.where(sinal > 0, b, perto)
        perto = np.where(busca, b, perto)
        b = np.where(busca, 2.0 * b, b)
    raise RuntimeError(ERRO_INTERVALO)


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
    lo, hi = _intervalo_lote(lambda x: sum(_termos(r0n, vr0, smu, alpha, x, *_cs_lote(alpha * x**2), dt)), chi, dt,
                             smu * dt / r0n, max_iter)
    ativo = np.ones(len(r0), dtype=bool)
    for _ in range(max_iter):
        z = alpha * chi**2
        c, s = _cs_lote(z)
        t = _termos(r0n, vr0, smu, alpha, chi, c, s, dt)
        f = sum(t)
        df = _derivada(r0n, vr0, smu, alpha, chi, z, c, s)
        lo = np.where(ativo & (f < 0), np.maximum(lo, chi), lo)
        hi = np.where(ativo & (f > 0), np.minimum(hi, chi), hi)
        passo = f / df
        novo = chi - passo
        para = ativo & (np.abs(passo) <= tol * np.maximum(1.0, np.abs(novo)))
        fora = ativo & ~para & ~((lo < novo) & (novo < hi))   # Newton saiu do intervalo (ou não é número): bisseção
        meio = 0.5 * (lo + hi)
        vizinhos = fora & ~((lo < meio) & (meio < hi))       # extremos vizinhos: o intervalo não encolhe mais
        if np.any(vizinhos) and not _residuo_ok(tuple(x[vizinhos] for x in t)):
            raise RuntimeError(ERRO_RESIDUO)
        novo = np.where(fora, meio, novo)
        para |= fora & ~vizinhos & (np.abs(novo - chi) <= tol * np.maximum(1.0, np.abs(novo)))
        chi = np.where(ativo & ~vizinhos, novo, chi)
        ativo = ativo & ~para & ~vizinhos
        if not np.any(ativo):
            break
    else:
        raise RuntimeError("Newton da equação universal de Kepler não convergiu")
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
