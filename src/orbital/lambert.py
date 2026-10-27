"""Problema de Lambert pelo algoritmo de Izzo (2015).

Referência: Izzo, D. "Revisiting Lambert's problem". Celestial Mechanics and Dynamical
Astronomy, 121(1):1–15, 2015. doi:10.1007/s10569-014-9587-y — docs/fontes.md [F9].

Notação do artigo: λ (aqui `ll`) é o parâmetro geométrico, T o tempo de voo adimensional,
x a variável de iteração e y = sqrt(1 − λ²(1 − x²)). Números de equação conferidos no preprint
arXiv:1403.2705:
- tempo de voo pela forma de Lancaster–Blanchard, eq. (18), com ψ da eq. (17);
- perto de x = 1 (M = 0), série hipergeométrica de Battin, eq. (20);
- derivadas de T(x), eq. (22); iteração de Householder, seção 4.1;
- chutes iniciais: seção 4.2.1 (M = 0, versão refinada da eq. (30)) e eq. (31) (M > 0);
- detecção de M máximo e T_min por Halley a partir de x = 0: Algoritmo 2;
- reconstrução das velocidades: Algoritmo 1.
A opção `prograde=False` (sentido retrógrado) não está no artigo; é a inversão de λ e dos
versores tangenciais usada em implementações correntes.

Unidades: as do chamador (km, s e km³/s² no projeto).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


class LambertError(RuntimeError):
    """Sem solução para os dados de entrada (por exemplo, M acima do máximo)."""


@dataclass(frozen=True)
class SolucaoLambert:
    v1: np.ndarray
    v2: np.ndarray
    revolucoes: int
    ramo: str  # "unica" (M = 0), "esquerdo" ou "direito" (M > 0)


def resolver(mu: float, r1, r2, tof: float, revolucoes: int = 0, prograde: bool = True,
             ramo: str = "esquerdo", max_iter: int = 35, tol: float = 1e-12) -> SolucaoLambert:
    """Velocidades nos extremos da cônica que liga r1 a r2 em `tof`.

    `prograde` define o sentido do movimento em relação a +z do frame de entrada.
    Para M > 0 há duas soluções; `ramo` escolhe o chute inicial x0l ("esquerdo") ou x0r
    ("direito") da eq. (31) do artigo. Para M = 0 o argumento é ignorado.
    """
    if ramo not in ("esquerdo", "direito"):
        raise ValueError("ramo deve ser 'esquerdo' ou 'direito'")
    r1 = np.asarray(r1, dtype=float)
    r2 = np.asarray(r2, dtype=float)
    if tof <= 0:
        raise ValueError("tempo de voo deve ser positivo")

    c_vec = r2 - r1
    c = np.linalg.norm(c_vec)
    r1n = np.linalg.norm(r1)
    r2n = np.linalg.norm(r2)
    s = 0.5 * (r1n + r2n + c)

    ir1 = r1 / r1n
    ir2 = r2 / r2n
    ih = np.cross(ir1, ir2)
    nh = np.linalg.norm(ih)
    if nh == 0.0:
        raise LambertError("r1 e r2 colineares: plano da transferência indefinido")
    ih = ih / nh

    ll = np.sqrt(max(0.0, 1.0 - min(1.0, c / s)))
    # Ângulo de transferência > 180° no sentido prógrado: λ < 0 (Izzo, 2015, Alg. 1).
    if ih[2] < 0:
        ll = -ll
        it1 = np.cross(ir1, ih)
        it2 = np.cross(ir2, ih)
    else:
        it1 = np.cross(ih, ir1)
        it2 = np.cross(ih, ir2)
    if not prograde:
        ll = -ll
        it1 = -it1
        it2 = -it2

    T = np.sqrt(2.0 * mu / s**3) * tof
    x, y = _achar_xy(ll, T, revolucoes, ramo, max_iter, tol)

    # Reconstrução das velocidades (Izzo, 2015, Alg. 1).
    gamma = np.sqrt(mu * s / 2.0)
    rho = (r1n - r2n) / c
    sigma = np.sqrt(1.0 - rho**2)
    vr1 = gamma * ((ll * y - x) - rho * (ll * y + x)) / r1n
    vr2 = -gamma * ((ll * y - x) + rho * (ll * y + x)) / r2n
    vt1 = gamma * sigma * (y + ll * x) / r1n
    vt2 = gamma * sigma * (y + ll * x) / r2n
    return SolucaoLambert(vr1 * ir1 + vt1 * it1, vr2 * ir2 + vt2 * it2, revolucoes,
                          "unica" if revolucoes == 0 else ramo)


def max_revolucoes(mu: float, r1, r2, tof: float, prograde: bool = True) -> int:
    """Maior número de revoluções completas M com solução para esse tempo de voo."""
    r1 = np.asarray(r1, dtype=float)
    r2 = np.asarray(r2, dtype=float)
    c = np.linalg.norm(r2 - r1)
    s = 0.5 * (np.linalg.norm(r1) + np.linalg.norm(r2) + c)
    ll = np.sqrt(max(0.0, 1.0 - min(1.0, c / s)))
    ih = np.cross(r1, r2)
    if ih[2] < 0:
        ll = -ll
    if not prograde:
        ll = -ll
    T = np.sqrt(2.0 * mu / s**3) * tof
    return _m_max(ll, T, 35, 1e-12)


# --- núcleo do algoritmo -----------------------------------------------------------------

def _y(x: float, ll: float) -> float:
    return np.sqrt(1.0 - ll**2 * (1.0 - x**2))


def _psi(x: float, y: float, ll: float) -> float:
    if -1.0 <= x < 1.0:
        return np.arccos(np.clip(x * y + ll * (1.0 - x**2), -1.0, 1.0))
    if x > 1.0:
        return np.arcsinh((y - x * ll) * np.sqrt(x**2 - 1.0))
    return 0.0


def _hyp2f1b(x: float) -> float:
    """2F1(3, 1; 5/2; x) por série, para |x| < 1."""
    if x >= 1.0:
        return np.inf
    soma, termo, k = 1.0, 1.0, 0
    while True:
        termo = termo * (3.0 + k) * (1.0 + k) / (2.5 + k) * x / (k + 1.0)
        anterior = soma
        soma += termo
        if soma == anterior:
            return soma
        k += 1


def _tof(x: float, y: float, ll: float, M: int) -> float:
    """Tempo de voo adimensional T(x): eq. (20) perto de x = 1 (M = 0), senão eq. (18)."""
    if M == 0 and np.sqrt(0.6) < x < np.sqrt(1.4):
        eta = y - ll * x
        s1 = 0.5 * (1.0 - ll - x * eta)
        q = 4.0 / 3.0 * _hyp2f1b(s1)
        return 0.5 * (eta**3 * q + 4.0 * ll * eta)
    psi = _psi(x, y, ll)
    return ((psi + M * np.pi) / np.sqrt(abs(1.0 - x**2)) - x + ll * y) / (1.0 - x**2)


def _d1(x, y, T, ll):
    return (3.0 * T * x - 2.0 + 2.0 * ll**3 * x / y) / (1.0 - x**2)


def _d2(x, y, T, d1, ll):
    return (3.0 * T + 5.0 * x * d1 + 2.0 * (1.0 - ll**2) * ll**3 / y**3) / (1.0 - x**2)


def _d3(x, y, d1, d2, ll):
    return (7.0 * x * d2 + 8.0 * d1 - 6.0 * (1.0 - ll**2) * ll**5 * x / y**5) / (1.0 - x**2)


def _t_min(ll: float, M: int, max_iter: int, tol: float) -> float:
    """T mínimo para M revoluções: zero de dT/dx por Halley a partir de x = 0 (Algoritmo 2)."""
    x = 0.0
    for _ in range(max_iter):
        y = _y(x, ll)
        T = _tof(x, y, ll, M)
        d1 = _d1(x, y, T, ll)
        d2 = _d2(x, y, T, d1, ll)
        d3 = _d3(x, y, d1, d2, ll)
        x_novo = x - 2.0 * d1 * d2 / (2.0 * d2**2 - d1 * d3)
        if abs(x_novo - x) < tol:
            return _tof(x_novo, _y(x_novo, ll), ll, M)
        x = x_novo
    raise LambertError("Halley não convergiu ao procurar T_min")


def _m_max(ll: float, T: float, max_iter: int, tol: float) -> int:
    m_max = int(np.floor(T / np.pi))
    t00 = np.arccos(ll) + ll * np.sqrt(1.0 - ll**2)
    if m_max > 0 and T < t00 + m_max * np.pi:
        if T < _t_min(ll, m_max, max_iter, tol):
            m_max -= 1
    return m_max


def _chute_inicial(T: float, ll: float, M: int, ramo: str) -> float:
    """Chutes iniciais: seção 4.2.1 (M = 0) e eq. (31) (M > 0)."""
    if M == 0:
        t00 = np.arccos(ll) + ll * np.sqrt(1.0 - ll**2)
        t1 = 2.0 / 3.0 * (1.0 - ll**3)
        if T >= t00:
            return (t00 / T) ** (2.0 / 3.0) - 1.0
        if T < t1:
            return 2.5 * t1 / T * (t1 - T) / (1.0 - ll**5) + 1.0
        return (t00 / T) ** np.log2(t1 / t00) - 1.0
    a = ((M * np.pi + np.pi) / (8.0 * T)) ** (2.0 / 3.0)
    x_esq = (a - 1.0) / (a + 1.0)
    b = ((8.0 * T) / (M * np.pi)) ** (2.0 / 3.0)
    x_dir = (b - 1.0) / (b + 1.0)
    return x_esq if ramo == "esquerdo" else x_dir


def _achar_xy(ll: float, T: float, M: int, ramo: str, max_iter: int, tol: float):
    if abs(ll) >= 1.0:
        raise LambertError("|λ| >= 1")
    if M > _m_max(ll, T, max_iter, tol):
        raise LambertError(f"sem solução com {M} revoluções para este tempo de voo")
    x = _chute_inicial(T, ll, M, ramo)
    for _ in range(max_iter):
        y = _y(x, ll)
        f = _tof(x, y, ll, M) - T
        Tx = f + T
        d1 = _d1(x, y, Tx, ll)
        d2 = _d2(x, y, Tx, d1, ll)
        d3 = _d3(x, y, d1, d2, ll)
        # Householder, 3ª ordem, na forma exata da seção 4.1 do artigo.
        x_novo = x - f * ((d1**2 - f * d2 / 2.0)
                          / (d1 * (d1**2 - f * d2) + d3 * f**2 / 6.0))
        if abs(x_novo - x) < tol:
            return x_novo, _y(x_novo, ll)
        x = x_novo
    raise LambertError("Householder não convergiu")
