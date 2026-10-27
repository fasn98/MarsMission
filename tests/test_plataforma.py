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


def test_config_coincide_com_a_etapa_2_3():
    """P-016 e P-017 no config são os valores calculados por tools/plataformas.py (sem cópia à mão divergente)."""
    import sys
    from pathlib import Path

    import yaml

    raiz = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(raiz / "tools"))
    import plataformas as pl

    ler = lambda c: yaml.safe_load((raiz / c).read_text(encoding="utf-8"))  # noqa: E731
    cfg, po = ler("config/plataformas.yaml"), ler("config/parametros_orbitais.yaml")
    res = ler("results/etapa2.3/plataformas.yaml")["orbita_encontro"]
    m_o = pl.plataforma_orbitador(cfg, po, res["apoapse_regra_5pct_km"], res["periapse_alt_km"])
    assert ler("config/dimensionamento.yaml")["plataforma_orbitador_kg"]["valor"] == pytest.approx(m_o, abs=0.05)
    assert ler("config/superficie.yaml")["lander"]["plataforma_superficie_kg"]["valor"] == pytest.approx(pl.lander_l3(cfg))
