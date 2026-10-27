"""Verificação das transferências Terra→Marte contra NASA/TM-2010-216764 ([F13]).

Nas datas impressas no manual, com partida no baricentro Terra–Lua (o manual não declara o
corpo de partida; ver docs/etapa1.2_lambert_porkchop.md), C3 e v∞ de chegada devem bater
dentro de P-007 (NÃO VALIDADA). Janela de 2035 excluída: datas da Tabela 6 inconsistentes
com as figuras do próprio manual.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import spiceypy as spice
import yaml

from orbital import ephemeris as eph
from orbital import porkchop as pc

RAIZ = Path(__file__).resolve().parents[1]
REF = yaml.safe_load((RAIZ / "tests/data/burke2010_minimos.yaml").read_text(encoding="utf-8"))["janelas"]
CASOS = [(ano, t) for ano in ("2028", "2031", "2033") for t in (1, 2)]


def _premissa(nome):
    cfg = yaml.safe_load((RAIZ / "config" / "premissas.yaml").read_text(encoding="utf-8"))
    return next(p["valor"] for p in cfg["premissas"] if p["nome"] == nome)


@pytest.mark.parametrize(("ano", "tipo"), CASOS, ids=lambda x: str(x))
def test_c3_e_vinf_nas_datas_do_manual(ano, tipo):
    eph.carregar_kernels()
    r = REF[ano][f"tipo_{tipo}"]
    c3, vinf, ang, _ = pc.transferencia(eph.BARICENTRO_TERRA_LUA, eph.BARICENTRO_MARTE,
                                        spice.str2et(f"{r['partida']} 00:00 TDB"),
                                        spice.str2et(f"{r['chegada']} 00:00 TDB"))
    tol = _premissa("tolerancia_burke2010_rel")
    assert abs(c3 - float(r["c3"])) / float(r["c3"]) < tol
    assert abs(vinf - float(r["vinf_chegada"])) / float(r["vinf_chegada"]) < tol
    assert (ang < 180.0) == (tipo == 1)


def test_angulo_prograde():
    assert pc.angulo_prograde([1, 0, 0], [0, 1, 0]) == pytest.approx(90.0)
    assert pc.angulo_prograde([1, 0, 0], [0, -1, 0]) == pytest.approx(270.0)
