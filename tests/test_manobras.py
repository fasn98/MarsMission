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


def test_h_entrada_com_gama_zero_e_periapse_na_interface():
    # γ = 0 na interface significa que a interface é o periapse.
    assert mn.h_entrada(MU, 4.0, R1, 0.0) == pytest.approx(mn.h_periapse(MU, 4.0, R1), rel=1e-14)


def test_hiperbole_de_entrada_tem_o_gama_pedido():
    vinf, r, gama = 5.4, 6500.0, -25.0
    h = mn.h_entrada(MU, vinf, r, gama)
    v = mn.v_hiperbole(MU, vinf, r)
    assert np.degrees(np.arccos(h / (r * v))) == pytest.approx(25.0, rel=1e-12)


def test_desvio_cai_com_a_antecedencia():
    a = mn.dv_desvio(MU, 5.44, 6500.0, -25.0, 6678.0, 86400.0)
    b = mn.dv_desvio(MU, 5.44, 6500.0, -25.0, 6678.0, 2 * 86400.0)
    assert a == pytest.approx(2 * b, rel=1e-12)


def test_coaxial_entre_circulares_igual_hohmann():
    hohmann = (np.sqrt(MU / R1) * (np.sqrt(2 * R2 / (R1 + R2)) - 1)
               + np.sqrt(MU / R2) * (1 - np.sqrt(2 * R1 / (R1 + R2))))
    assert mn.dv_transferencia_coaxial(MU, R1, R1, R2, R2) == pytest.approx(hohmann, rel=1e-13)


def test_saida_de_orbita_e_entrada_por_energia():
    r, rei = 3800.0, 3521.0
    dv = mn.dv_saida_de_orbita(MU_M := 42828.37, r, r, rei)
    v_apo = np.sqrt(2 * MU_M * rei / (r * (r + rei)))
    assert dv == pytest.approx(np.sqrt(MU_M / r) - v_apo, rel=1e-13)
    # energia conservada entre o apoapse e a interface
    v_ei = mn.v_entrada_de_orbita(MU_M, r, rei)
    assert v_ei**2 / 2 - MU_M / rei == pytest.approx(v_apo**2 / 2 - MU_M / r, rel=1e-12)


def test_rotacao_no_equador_e_nos_polos():
    assert mn.v_rotacao(3396.19, 88642.66, 0.0) == pytest.approx(2 * np.pi * 3396.19 / 88642.66, rel=1e-15)
    assert mn.v_rotacao(3396.19, 88642.66, 90.0) == pytest.approx(0.0, abs=1e-15)
