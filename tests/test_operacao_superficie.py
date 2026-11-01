"""Etapa 4.4: operação de superfície (tools/operacao_superficie.py)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from orbital.config import ler, v

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import operacao_superficie as os_  # noqa: E402

C = ler("config/operacao_superficie.yaml")


def test_voos_do_ingenuity_em_ordem_e_completos():
    s = C["ingenuity"]["voos_sois"]["valor"]
    assert len(s) == 72 and all(b > a for a, b in zip(s, s[1:]))


def test_probabilidade_pelo_catalogo():
    cat = [{"ls": x} for x in (185, 200, 250, 300)]
    assert os_.prob_tempestade_ate(220, cat, 185, 0.25) == (pytest.approx(0.125), 2)
    assert os_.prob_tempestade_ate(360, cat, 185, 0.25)[0] == pytest.approx(0.25)


def test_linha_do_tempo_e_dados():
    r = ler("results/etapa4.4/operacao_superficie.yaml")
    fixos = v(C["srh"]["saida_sois"]) + v(C["srh"]["mapeamento_sois"]) + v(C["operacao"]["transferencia_e_lancamento_sois"])
    for x in r["linha_do_tempo"]:
        assert x["total_sois"] == pytest.approx(fixos + x["busca_sois"])
        assert x["busca_sois"] == pytest.approx(v(C["deposito"]["tubos"]) * x["sois_por_tubo"] / x["helicopteros_em_paralelo"])
        assert x["antes_da_conjuncao"] == (x["folga_conjuncao_dias"] > 0)
    base = next(x for x in r["linha_do_tempo"] if x["distancia_m"] == 200 and x["ritmo"] == "SRH" and x["helicopteros_em_paralelo"] == 2)
    assert base["sois_por_tubo"] == v(C["srh"]["sois_por_tubo"])          # o ritmo publicado no caso de ~200 m
    assert 0 <= base["prob_tempestade_ate_lancamento"] <= r["prob_tempestade_estada"]
    for d in r["dados_helicopteros"]:
        assert d["mbit_por_sol"][0] <= d["mbit_por_sol"][1]
