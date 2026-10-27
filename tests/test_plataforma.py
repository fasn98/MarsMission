"""Testes da Etapa 2.3: eclipse, bateria, painel e margem (src/orbital/plataforma.py)."""

import numpy as np
import pytest

from orbital import plataforma as pf

MU, R = 42828.37362069909, 3396.19


def test_eclipse_circular_analitico():
    # Órbita circular, Sol no plano: fração em sombra cilíndrica = asin(R/r)/π.
    r = R + 400.0
    t, periodo = pf.eclipse_maximo(MU, R, r, r)
    assert t == pytest.approx(periodo * np.arcsin(R / r) / np.pi, rel=2e-3)
    assert periodo == pytest.approx(2 * np.pi * np.sqrt(r**3 / MU))


def test_eclipse_eliptico_maior_que_circular_no_periapse():
    t_el, _ = pf.eclipse_maximo(MU, R, R + 300, R + 26950)
    t_c, _ = pf.eclipse_maximo(MU, R, R + 300, R + 300)
    assert t_el > t_c


def test_bateria_e_painel():
    cap, m = pf.bateria(300.0, 0.3, 100.0)
    assert cap == pytest.approx(1000.0) and m == pytest.approx(10.0)
    assert pf.potencia_painel(100.0, 3.0, 1.0, 0.5) == pytest.approx(100.0 + 100.0 / 1.5)
    assert pf.massa_painel(80.0, 80.0, 1.0, 1.0) == pytest.approx(1.0)
    assert pf.massa_painel(80.0, 80.0, 2.0, 1.0) == pytest.approx(4.0)


def test_com_margem():
    assert pf.com_margem(100.0, 0.25) == pytest.approx(125.0)
