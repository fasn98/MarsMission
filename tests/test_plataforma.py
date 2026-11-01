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


def test_eclipse_eliptico_sombra_no_apoapse_analitico():
    # Sol ao longo da linha das apsides, apoapse atrás do planeta: a sombra é a faixa |y| < R no ramo do apoapse.
    # Entrada e saída em E = π ∓ asin(R/b); tempo pela equação de Kepler. Para apoapse alto é o pior caso.
    rp, ra = R + 300.0, R + 24991.9
    a, e = 0.5 * (rp + ra), (ra - rp) / (ra + rp)
    b = a * np.sqrt(1 - e * e)
    e1, e2 = np.pi - np.arcsin(R / b), np.pi + np.arcsin(R / b)
    n = np.sqrt(MU / a**3)
    t_analitico = ((e2 - e * np.sin(e2)) - (e1 - e * np.sin(e1))) / n
    t, _ = pf.eclipse_maximo(MU, R, rp, ra)
    assert t == pytest.approx(t_analitico, rel=2e-3)


@pytest.fixture
def ferramenta(monkeypatch):
    """Importa tools/plataformas.py com tools/ no sys.path só durante o teste."""
    import importlib
    from pathlib import Path

    import yaml

    raiz = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(raiz / "tools"))
    pl = importlib.import_module("plataformas")
    ler = lambda c: yaml.safe_load((raiz / c).read_text(encoding="utf-8"))  # noqa: E731
    return pl, ler


def test_criterios_de_margem(ferramenta):
    pl, ler = ferramenta
    cfg = ler("config/plataformas.yaml")
    itens = [("a", 100.0, "estrutura_primaria"), ("b", 10.0, "cabeamento")]
    assert pl.prevista(itens, cfg, "e1_medio") == pytest.approx(121.5 + 17.5)
    assert pl.prevista(itens, cfg, "e1_minimo") == pytest.approx(118.0 + 15.0)
    assert pl.prevista(itens, cfg, "e1_maximo") == pytest.approx(125.0 + 20.0)
    assert pl.prevista(itens, cfg, "e1_medio_mais_gsfc") == pytest.approx(139.0 + 0.15 * 110.0)
    assert pl.prevista(itens, cfg, "esa") == pytest.approx(110.0 * 1.44)
    with pytest.raises(ValueError):
        pl.prevista(itens, cfg, "e1_meio")


def test_lander_l1_l2_l3(ferramenta):
    pl, ler = ferramenta
    cfg = ler("config/plataformas.yaml")
    assert pl.lander_l3(cfg) == pytest.approx(2100 - 400 - 230)
    assert pl.l3_com_margem(1000.0, cfg, "e1_medio_mais_gsfc") == pytest.approx(1150.0)
    assert pl.l3_com_margem(1000.0, cfg, "esa") == pytest.approx(1440.0)
    it1, en = pl.lander(cfg, "L1", 300.0)
    assert dict((n, m) for n, m, _ in it1)["nucleo"] == pytest.approx(410 - 67 - 59 - 6.5 - 14.7 - 5.0)
    it2, _ = pl.lander(cfg, "L2", 300.0)
    k = en["fracao_nucleo_phoenix"]
    resto = sum(m for n, m, _ in it2 if n != "nucleo")
    nucleo = dict((n, m) for n, m, _ in it2)["nucleo"]
    assert nucleo / (nucleo + resto + 300.0) == pytest.approx(k)


def test_lander_base_e_limite_superior(ferramenta):
    pl, ler = ferramenta
    cfg = ler("config/plataformas.yaml")
    # L3 + braço (59 kg, instrumentação, 50 %) + helicópteros (5 kg, eletrônica 0–5 kg, 27,5 %) — ADR 0009
    assert pl.lander_base(cfg) == pytest.approx(1470 + 59 * 1.5 + 5 * 1.275)
    assert pl.lander_base(cfg, "e1_medio_mais_gsfc") == pytest.approx(1470 * 1.15 + 59 * 1.5 + 5 * 1.275 + 0.15 * 64)
    assert pl.lander_base(cfg, "esa") == pytest.approx((1470 + 64) * 1.44)
    assert pl.limite_srl_2024(cfg) == pytest.approx(2900 - 400)


def test_config_coincide_com_a_etapa_2_3(ferramenta):
    """P-016 no config é o valor calculado por tools/plataformas.py, e a base do lander da Etapa 2.3 é L3 + braço +
    helicópteros (a P-017 vigente, caso B da Etapa 4.5, é conferida em tests/test_lista_massas.py)."""
    pl, ler = ferramenta
    cfg, po = ler("config/plataformas.yaml"), ler("config/parametros_orbitais.yaml")
    res = ler("results/etapa2.3/plataformas.yaml")["orbita_encontro"]
    m_o = pl.plataforma_orbitador(cfg, po, res["apoapse_regra_5pct_km"], res["periapse_alt_km"])
    assert ler("config/dimensionamento.yaml")["plataforma_orbitador_kg"]["valor"] == pytest.approx(m_o, abs=0.05)
    assert ler("results/etapa2.3/plataformas.yaml")["escolha"]["plataforma_lander_kg"] == pytest.approx(pl.lander_base(cfg))
