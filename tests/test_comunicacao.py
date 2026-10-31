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


def test_taxa_uhf_e_comparacao():
    c = ler("config/comunicacao.yaml")["rele_proprio"]
    assert tc.taxa_uhf(250.0, c) == 1024           # órbita baixa: topo da tabela do Electra
    taxas = [tc.taxa_uhf(r_km, c) for r_km in (300.0, 3000.0, 30000.0)]
    assert taxas[0] >= taxas[1] >= taxas[2] > 0       # cai com a distância e ainda fecha no apoapse
    r = ler("results/etapa4.3/comunicacao.yaml")["comparacao"]
    h = ler("config/comunicacao.yaml")["helicopteros"]
    assert r["helicopteros"]["mbit_por_voo_max"] == pytest.approx(v(h["imagens_por_voo_max"]) * h["navcam_px"]["valor"][0] * h["navcam_px"]["valor"][1] * v(h["bits_por_pixel"]) / 1e6)
    assert r["demanda_total_mbit_sol"] == pytest.approx(r["demanda_lander_mbit_sol"] + r["helicopteros"]["mbit_por_sol"])
    for x in r["rele_proprio"]:
        assert x["mbit_por_passe_medio"] <= x["mbit_por_passe_max"] and x["passes_por_sol"] > 0
    d = r["dte_maior"]
    assert d["diametro_com_100w_m"] < d["diametro_com_15w_m"]
