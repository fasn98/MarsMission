"""Testes da propagação kepleriana analítica (orbital.kepler).

- Comparação com integração numérica de dois corpos (tolerância P-004, NÃO VALIDADA).
- Constantes do movimento: energia e momento angular conservados.
- Ida e volta: propagar +dt e depois −dt recupera o estado inicial.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import yaml
from scipy.integrate import solve_ivp

from orbital import kepler

RAIZ = Path(__file__).resolve().parents[1]
MU = 398600.4418


def _premissa(nome):
    cfg = yaml.safe_load((RAIZ / "config" / "premissas.yaml").read_text(encoding="utf-8"))
    return next(p["valor"] for p in cfg["premissas"] if p["nome"] == nome)


def _orbitas(n, semente):
    rng = np.random.default_rng(semente)
    for _ in range(n):
        r0 = rng.normal(size=3) * 1e4
        r0 *= max(1.0, 7000.0 / np.linalg.norm(r0))
        v0 = rng.normal(size=3)
        v0 *= np.sqrt(MU / np.linalg.norm(r0)) * rng.uniform(0.6, 1.8) / np.linalg.norm(v0)
        yield r0, v0, rng.uniform(100.0, 5e4)


def test_kepler_confere_com_integrador():
    tol = _premissa("tolerancia_kepler_vs_integrador_rel")

    def f(_, s):
        return np.r_[s[3:], -MU * s[:3] / np.linalg.norm(s[:3]) ** 3]

    for r0, v0, t in _orbitas(100, 20261027):
        r, _ = kepler.propagar(MU, r0, v0, t)
        st = solve_ivp(f, (0.0, t), np.r_[r0, v0], method="DOP853", rtol=1e-13, atol=1e-12).y[:, -1]
        assert np.linalg.norm(r - st[:3]) / np.linalg.norm(st[:3]) < tol


def test_conserva_energia_e_momento_angular():
    for r0, v0, t in _orbitas(100, 7):
        r, v = kepler.propagar(MU, r0, v0, t)
        e0 = v0 @ v0 / 2 - MU / np.linalg.norm(r0)
        e1 = v @ v / 2 - MU / np.linalg.norm(r)
        assert abs(e1 - e0) <= 1e-10 * abs(e0)
        h0, h1 = np.cross(r0, v0), np.cross(r, v)
        assert np.linalg.norm(h1 - h0) <= 1e-10 * np.linalg.norm(h0)


def test_ida_e_volta_recupera_estado():
    for r0, v0, t in _orbitas(50, 11):
        r, v = kepler.propagar(MU, r0, v0, t)
        rb, vb = kepler.propagar(MU, r, v, -t)
        assert np.linalg.norm(rb - r0) <= 1e-9 * np.linalg.norm(r0)
        assert np.linalg.norm(vb - v0) <= 1e-9 * np.linalg.norm(v0)
