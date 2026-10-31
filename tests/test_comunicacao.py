"""Etapa 4.3: comunicação (tools/comunicacao.py)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

from orbital.config import ler, v

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import comunicacao as tc  # noqa: E402


def test_angulo_sol_terra_alvo():
    sol = np.array([1.0, 0.0, 0.0])
    assert tc.sep_e_distancia(np.array([0.0, 2.0, 0.0]), sol) == pytest.approx((90.0, 2.0))
    assert tc.sep_e_distancia(np.array([3.0, 0.0, 0.0]), sol)[0] == pytest.approx(0.0, abs=1e-6)


def test_janelas_contiguas():
    import datetime as dt
    d = [dt.date(2030, 1, 1) + dt.timedelta(days=k) for k in range(6)]
    s = [6, 4, 3, 4, 6, 4]
    assert tc.janelas(list(zip(d, s)), 5) == [(d[1], d[3], 3), (d[5], d[5], 1)]


def test_resultado_da_etapa_4_3():
    r = ler("results/etapa4.3/comunicacao.yaml")
    c = ler("config/comunicacao.yaml")
    j = r["janelas"]
    # janelas encaixadas: quanto menor o limite, menor a janela
    a5, a2 = j["periodo_conjuncao_graus"][0], j["sem_comando_graus"][0]
    assert a5["inicio"] <= a2["inicio"] and a2["fim"] <= a5["fim"] and a2["dias"] < a5["dias"]
    assert r["sep_minimo"]["graus"] < v(c["conjuncao"]["sem_comando_graus"])
    di = r["distancias"]
    assert di["tempo_luz_max_min"] == pytest.approx(di["missao_max_km"] / v(c["luz_km_s"]) / 60, rel=1e-12)
    ox = r["orbitador_x"]
    assert ox["taxa_na_distancia_max_kbps"] == pytest.approx(
        v(c["orbitador_x"]["taxa_ref_kbps"]) * (v(c["orbitador_x"]["distancia_ref_km"]) / di["estada_max_km"]) ** 2, rel=1e-12)
