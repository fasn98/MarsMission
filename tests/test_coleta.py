"""Etapa 2.5: a opção escolhida de coleta, (c) + (a), reproduz o lander de base (ADR 0009)."""

import sys
from pathlib import Path

import pytest
import yaml

RAIZ = Path(__file__).resolve().parents[1]


def test_opcao_escolhida_igual_ao_lander_de_base(monkeypatch):
    monkeypatch.syspath_prepend(str(RAIZ / "tools"))
    import plataformas as pl

    r = yaml.safe_load((RAIZ / "results/etapa2.5/coleta.yaml").read_text(encoding="utf-8"))
    escolha = yaml.safe_load((RAIZ / "config/coleta.yaml").read_text(encoding="utf-8"))["escolha"]
    a = next(x for x in r["opcoes"] if x["opcao"] == escolha)
    cfg = yaml.safe_load((RAIZ / "config/plataformas.yaml").read_text(encoding="utf-8"))
    assert a["plataforma_lander_kg"] == pytest.approx(pl.lander_base(cfg))
    l24 = yaml.safe_load((RAIZ / "results/etapa2.4/lancamento.yaml").read_text(encoding="utf-8"))
    assert a["lander_injetado_kg"] == pytest.approx(l24["veiculos"]["lander"]["injetada_kg"])
