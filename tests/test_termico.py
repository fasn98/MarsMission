"""Etapa 4.2: controle térmico (tools/termico.py)."""

from __future__ import annotations

import re

import pytest

from orbital.config import ler, v

C = ler("config/termico.yaml")


def test_faixas_tem_fonte_e_ordem():
    for f in C["faixas"]:
        assert re.search(r"\[F\d+\]", f["fonte"]), f["item"]
        if f["min_c"] is not None and f["max_c"] is not None:
            assert f["min_c"] < f["max_c"], f["item"]


def test_aquecimento_do_mav_escala_com_a_diferenca_de_temperatura():
    r = ler("results/etapa4.2/termico.yaml")
    a = r["aquecimento_mav"]
    t_amb = r["ambiente_mav_c"]
    base = a[0]
    for x in a[1:]:
        assert x["potencia_w"] / base["potencia_w"] == pytest.approx((x["t_c"] - t_amb) / (base["t_c"] - t_amb), rel=1e-12)
        assert x["carga_sobrevivencia_wh_sol"] - base["carga_sobrevivencia_wh_sol"] == pytest.approx(x["energia_wh_sol"] - base["energia_wh_sol"], rel=1e-9)
    en = ler("results/etapa4.1/energia.yaml")["lander"]["variante_rhu"]
    assert base["carga_sobrevivencia_wh_sol"] == pytest.approx(en["sobrevivencia"]["total_wh_sol"], rel=1e-12)
    assert base["area_opcao_m2"] == pytest.approx(en["opcao"]["area_m2"], rel=1e-9)   # reproduz a linha de base da 4.1
    assert base["total_opcao_kg"] == pytest.approx(en["opcao"]["total_kg"], rel=1e-9)


def test_cruzeiro_e_amostras():
    r = ler("results/etapa4.2/termico.yaml")
    cz = r["cruzeiro"]
    assert cz["fracao_do_srl_passivo"] == pytest.approx(cz["rhu_w"] / v(C["cruzeiro"]["srl_perda_passiva_max_w"]), rel=1e-12)
    am = r["amostras"]
    assert am["excesso_k"] == pytest.approx(am["mav_c"] - am["aft_c"])
