"""Testes de orbital.manobras contra relações fechadas independentes (casos-limite e Hohmann)."""

from __future__ import annotations

import numpy as np
import pytest

from orbital import manobras as mn

MU = 398600.4418
R1, R2 = 6778.0, 42164.0


def test_vinf_nulo_para_circular_e_raiz2_menos_1():
    vc = np.sqrt(MU / R1)
    assert mn.dv_hiperbole_orbita(MU, 0.0, R1) == pytest.approx((np.sqrt(2) - 1) * vc, rel=1e-14)


def test_hiperbole_orbita_por_energia():
    vinf, rp, ra = 3.2, 3700.0, 37000.0
    v_hip = np.sqrt(vinf**2 + 2 * MU / rp)
    v_eli = np.sqrt(2 * MU / rp - 2 * MU / (rp + ra))
    assert mn.dv_hiperbole_orbita(MU, vinf, rp, ra) == pytest.approx(v_hip - v_eli, rel=1e-14)


def test_elevacao_de_periapse_igual_segunda_queima_de_hohmann():
    hohmann_2 = np.sqrt(MU / R2) * (1 - np.sqrt(2 * R1 / (R1 + R2)))
    assert mn.dv_elevacao_periapse(MU, R1, R2, R2) == pytest.approx(hohmann_2, rel=1e-13)


def test_aerocaptura_sem_mudanca_de_periapse_custa_zero():
    assert mn.dv_captura_aerocaptura(MU, 3646.0, 3646.0, 37000.0) == pytest.approx(0.0, abs=1e-12)


def test_aerocaptura_mais_barata_que_captura_propulsiva():
    assert mn.dv_captura_aerocaptura(MU, 6450.0, R1) < mn.dv_hiperbole_orbita(MU, 3.0, R1)


def test_reentrada_com_vinf_nulo_e_velocidade_de_escape():
    assert mn.velocidade_reentrada(MU, 0.0, R1) == pytest.approx(np.sqrt(2 * MU / R1), rel=1e-15)


def test_declinacao():
    assert mn.declinacao_graus([1, 0, 0]) == pytest.approx(0.0)
    assert mn.declinacao_graus([0, 0, 2]) == pytest.approx(90.0)
    assert mn.declinacao_graus([1, 0, -1]) == pytest.approx(-45.0)
