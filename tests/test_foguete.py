"""Testes de orbital.foguete contra a forma fechada da equação do foguete."""

from __future__ import annotations

import numpy as np
import pytest

from orbital import foguete as fg


def _R(dv, isp):
    return np.exp(dv / (fg.G0 * isp))


@pytest.mark.parametrize("eps", [0.0, 0.1, 0.24])
def test_uma_queima_forma_fechada(eps):
    dv, isp, carga = 1.5, 320.0, 700.0
    k = eps / (1 - eps)
    R = _R(dv, isp)
    mp_esperado = carga * (R - 1) / (1 - k * (R - 1))
    r = fg.dimensionar_estagio(fg.Estagio("x", isp, eps, [fg.Queima("q", dv)]), carga)
    assert r.propelente == pytest.approx(mp_esperado, rel=1e-10)
    assert r.inerte == pytest.approx(k * mp_esperado, rel=1e-10)
    # Tsiolkovsky: m_ini / m_fim = R
    assert r.massa_inicial / (carga + r.inerte) == pytest.approx(R, rel=1e-12)


def test_duas_queimas_igual_a_uma_com_soma():
    a = fg.dimensionar_estagio(fg.Estagio("a", 320.0, 0.15, [fg.Queima("1", 0.7), fg.Queima("2", 0.8)]), 500.0)
    b = fg.dimensionar_estagio(fg.Estagio("b", 320.0, 0.15, [fg.Queima("1", 1.5)]), 500.0)
    assert a.propelente == pytest.approx(b.propelente, rel=1e-10)


def test_descarte_antes_da_queima_economiza_propelente():
    sem = fg.dimensionar_estagio(fg.Estagio("s", 320.0, 0.15, [fg.Queima("1", 1.0), fg.Queima("2", 0.1)]), 600.0)
    com = fg.dimensionar_estagio(fg.Estagio("c", 320.0, 0.15, [fg.Queima("1", 1.0), fg.Queima("2", 0.1, 90.0)]), 600.0 - 90.0)
    # Mesma massa inicial carregada? Não: no caso "com", 90 kg saem antes da 2ª queima.
    # A massa inicial do caso "com" tem de ser menor ou igual à do caso "sem".
    assert com.massa_inicial < sem.massa_inicial
    assert com.propelente_por_queima["1"] == pytest.approx(
        com.massa_inicial * (1 - 1 / _R(1.0, 320.0)), rel=1e-10)


def test_inviavel_levanta_erro():
    with pytest.raises(ValueError):
        fg.dimensionar_estagio(fg.Estagio("x", 300.0, 0.3, [fg.Queima("q", 6.0)]), 100.0)


def test_estagios_em_serie():
    e1 = fg.Estagio("1", 450.0, 0.12, [fg.Queima("a", 3.6)])
    e2 = fg.Estagio("2", 320.0, 0.24, [fg.Queima("b", 1.0)])
    r = fg.dimensionar_veiculo([e1, e2], 700.0)
    assert r[0].massa_inicial == pytest.approx(r[1].massa_inicial + r[0].propelente + r[0].inerte, rel=1e-12)
    assert r[1].massa_inicial == pytest.approx(700.0 + r[1].propelente + r[1].inerte, rel=1e-12)
