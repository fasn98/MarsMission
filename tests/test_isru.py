"""Testes de orbital.isru (relações algébricas)."""

from __future__ import annotations

import pytest

from orbital import isru


def test_divisao_of_dra():
    ox, comb = isru.divisao_of(4.5, 3.5)
    assert (ox, comb) == pytest.approx((3.5, 1.0))
    assert ox / 4.5 == pytest.approx(0.7778, abs=1e-4)  # "78%" de Hecht et al. 2021, p. 3


def test_escala_linear_e_com_expoente():
    assert isru.escala(17.8, 12.0, 6.0, 1.0) == pytest.approx(35.6)
    assert isru.escala(17.8, 12.0, 6.0, 0.0) == pytest.approx(17.8)
    assert isru.escala(100.0, 8.0, 1.0, 2.0 / 3.0) == pytest.approx(400.0)


def test_rtg():
    assert isru.potencia_rtg_fim(110.0, 0.048, 0.0) == pytest.approx(110.0)
    m, n = isru.massa_rtg(250.0, 110.0, 45.0, 0.048, 2.0)
    assert n == 3 and m == pytest.approx(135.0)
