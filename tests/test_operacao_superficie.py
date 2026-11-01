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
        if x["antes_da_partida"]:
            assert x["antes_da_conjuncao"] == (x["folga_conjuncao_dias"] > 0)
        else:
            assert x["folga_conjuncao_dias"] is None and x["prob_tempestade_ate_lancamento"] is None and not x["antes_da_conjuncao"]
    base = next(x for x in r["linha_do_tempo"] if x["distancia_m"] == 200 and x["ritmo"] == "SRH" and x["helicopteros_em_paralelo"] == 2)
    assert base["sois_por_tubo"] == v(C["srh"]["sois_por_tubo"])          # o ritmo publicado no caso de ~200 m
    assert 0 <= base["prob_tempestade_ate_lancamento"] <= r["prob_tempestade_estada"]
    for d in r["dados_helicopteros"]:
        assert d["mbit_por_sol"][0] <= d["mbit_por_sol"][1]


def test_requisitos_de_folga():
    r = ler("results/etapa4.4/operacao_superficie.yaml")
    rq = C["requisitos"]
    for x in r["linha_do_tempo"]:
        if x["antes_da_partida"]:
            assert x["atende_folga_minima"] == (x["folga_conjuncao_dias"] >= v(rq["folga_min_conjuncao_dias"]))
            alvo = rq["folga_alvo_conjuncao_dias"]
            assert x["dentro_do_alvo"] == (alvo["min"] <= x["folga_conjuncao_dias"] <= alvo["max"])
    # todos os casos do ritmo do SRH atendem a folga mínima (base da decisão do Fabio)
    assert all(x["atende_folga_minima"] for x in r["linha_do_tempo"] if x["ritmo"] == "SRH")


def test_faixa_sem_mudanca():
    r = ler("results/etapa4.4/operacao_superficie.yaml")["faixa_sem_mudanca"]
    assert r["SRH"]["sem_mudanca_ate_m"] == v(C["srh"]["alcance_por_carga_m"]) and r["SRH"]["mesmo_resultado"]
    assert r["Ingenuity"]["sem_mudanca_ate_m"] == v(C["ingenuity"]["alcance_de_projeto_m"]) and r["Ingenuity"]["mesmo_resultado"]
