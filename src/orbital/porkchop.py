"""Grades de transferência balística (porkchop) entre dois corpos, por Lambert (Izzo, 2015).

Modelo: cônicas emendadas, heliocêntrico, manobras impulsivas na partida e chegada, sem
manobra no espaço profundo, sem perturbações. Posições e velocidades dos corpos vêm das
efemérides (ADR 0002). Frame ECLIPJ2000 (eclíptica e equinócio J2000) para que "prógrado"
seja o sentido do movimento planetário; C3 e v∞ são normas e não dependem do frame.

Tipo I: ângulo de transferência < 180°; Tipo II: entre 180° e 360° (só 0 revoluções).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import spiceypy as spice

from orbital import ephemeris as eph
from orbital import lambert
from orbital.constantes import GM_SOL

FRAME = "ECLIPJ2000"
DIA = 86400.0


@dataclass
class Grade:
    et_partida: np.ndarray        # (n,) segundos TDB após J2000
    et_chegada: np.ndarray        # (m,)
    c3: np.ndarray                # (n, m) km²/s², NaN onde não há solução
    vinf_chegada: np.ndarray      # (n, m) km/s
    angulo_transf: np.ndarray     # (n, m) graus, 0–360 no sentido prógrado
    tof_dias: np.ndarray          # (n, m)


def estado_corpo(corpo: str, et: float) -> np.ndarray:
    eph.carregar_kernels()
    st, _ = spice.spkezr(corpo, et, FRAME, "NONE", eph.SOL)
    return np.asarray(st)


def angulo_prograde(r1: np.ndarray, r2: np.ndarray) -> float:
    """Ângulo de r1 para r2 medido no sentido de +z da eclíptica, em graus [0, 360)."""
    cosang = np.dot(r1, r2) / (np.linalg.norm(r1) * np.linalg.norm(r2))
    ang = np.degrees(np.arccos(np.clip(cosang, -1.0, 1.0)))
    return float(ang if np.cross(r1, r2)[2] >= 0 else 360.0 - ang)


def transferencia(partida: str, chegada: str, et1: float, et2: float):
    """(C3, v∞ chegada, ângulo, v∞ partida vetor) da transferência balística de 0 revoluções."""
    s1 = estado_corpo(partida, et1)
    s2 = estado_corpo(chegada, et2)
    sol = lambert.resolver(GM_SOL, s1[:3], s2[:3], et2 - et1)
    vinf1 = sol.v1 - s1[3:]
    vinf2 = sol.v2 - s2[3:]
    return float(vinf1 @ vinf1), float(np.linalg.norm(vinf2)), angulo_prograde(s1[:3], s2[:3]), vinf1


def calcular_grade(partida: str, chegada: str, et_partida, et_chegada) -> Grade:
    et_partida = np.asarray(et_partida, dtype=float)
    et_chegada = np.asarray(et_chegada, dtype=float)
    st1 = [estado_corpo(partida, t) for t in et_partida]
    st2 = [estado_corpo(chegada, t) for t in et_chegada]
    n, m = len(et_partida), len(et_chegada)
    c3 = np.full((n, m), np.nan)
    vinf = np.full((n, m), np.nan)
    ang = np.full((n, m), np.nan)
    tof = (et_chegada[None, :] - et_partida[:, None]) / DIA
    for i, s1 in enumerate(st1):
        for j, s2 in enumerate(st2):
            if tof[i, j] <= 0:
                continue
            try:
                sol = lambert.resolver(GM_SOL, s1[:3], s2[:3], tof[i, j] * DIA)
            except lambert.LambertError:
                continue
            d1 = sol.v1 - s1[3:]
            c3[i, j] = d1 @ d1
            vinf[i, j] = np.linalg.norm(sol.v2 - s2[3:])
            ang[i, j] = angulo_prograde(s1[:3], s2[:3])
    return Grade(et_partida, et_chegada, c3, vinf, ang, tof)


def minimo_c3_por_tipo(partida: str, chegada: str, grade: Grade, tipo: int, exclusao_180: float = 0.0,
                       grandeza: str = "c3"):
    """Mínimo local de C3 (ou, com grandeza="vinf", do v∞ de chegada) no tipo dado (1 ou 2).

    `exclusao_180` (graus) remove da busca os ângulos dentro de ±exclusao_180 de 180°, onde o
    plano da transferência é mal definido (premissa P-006).

    Parte do menor valor da grade nesse tipo e refina com Nelder–Mead em (partida, chegada),
    penalizando pontos que mudem de tipo ou saiam do domínio da grade. Se o mínimo cair na
    borda do domínio, o campo "na_borda" fica True: o mínimo verdadeiro pode estar fora. Devolve dict com datas, C3, v∞ e ângulo.
    """
    from scipy.optimize import minimize

    def do_tipo(a):
        return (a < 180.0 - exclusao_180) if tipo == 1 else (a > 180.0 + exclusao_180)

    mascara = do_tipo(np.nan_to_num(grade.angulo_transf, nan=-1.0)) & np.isfinite(grade.c3)
    if not mascara.any():
        return None
    alvo = grade.c3 if grandeza == "c3" else grade.vinf_chegada
    c3m = np.where(mascara, alvo, np.inf)
    i, j = np.unravel_index(np.argmin(c3m), c3m.shape)
    x0 = np.array([grade.et_partida[i], grade.et_chegada[j]]) / DIA

    lim_p = (grade.et_partida[0], grade.et_partida[-1])
    lim_c = (grade.et_chegada[0], grade.et_chegada[-1])

    def f(x):
        et1, et2 = x * DIA
        # Refinamento restrito ao domínio da grade, para não sair da janela estudada.
        if et2 <= et1 or not (lim_p[0] <= et1 <= lim_p[1] and lim_c[0] <= et2 <= lim_c[1]):
            return 1e6
        try:
            c3, vinf, a, _ = transferencia(partida, chegada, et1, et2)
        except lambert.LambertError:
            return 1e6
        valor = c3 if grandeza == "c3" else vinf
        return valor if do_tipo(a) else 1e6

    res = minimize(f, x0, method="Nelder-Mead",
                   options={"xatol": 1e-4, "fatol": 1e-8, "initial_simplex": [x0, x0 + [2, 0], x0 + [0, 2]]})
    et1, et2 = res.x * DIA
    c3, vinf2, a, _ = transferencia(partida, chegada, et1, et2)
    passo = 1.5 * min(np.diff(grade.et_partida).min(), np.diff(grade.et_chegada).min())
    na_borda = bool(min(et1 - lim_p[0], lim_p[1] - et1, et2 - lim_c[0], lim_c[1] - et2) < passo)
    return {"et_partida": float(et1), "et_chegada": float(et2), "c3": c3, "vinf_chegada": vinf2,
            "angulo": a, "tof_dias": float((et2 - et1) / DIA), "na_borda": na_borda}
