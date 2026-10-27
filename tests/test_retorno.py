"""Verificação do retorno Marte→Terra contra JPL Publication 82-43, Vol. I, Part 5 ([F14]).

Nas datas impressas nas tabelas "ENERGY MINIMA" (1992–2007), com partida no baricentro de
Marte e chegada no baricentro Terra–Lua, C3L e VHP devem bater dentro de P-008 (NÃO
VALIDADA). As linhas fora do teste vêm da lista explícita em config/excecoes_verificacao.yaml,
cada uma com o motivo; a tolerância não é alargada para cobri-las.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import spiceypy as spice
import yaml

from orbital import ephemeris as eph
from orbital import porkchop as pc

RAIZ = Path(__file__).resolve().parents[1]
REF = yaml.safe_load((RAIZ / "tests/data/jpl8243p5_minimos.yaml").read_text(encoding="utf-8"))["janelas"]
EXCECOES = yaml.safe_load((RAIZ / "config/excecoes_verificacao.yaml").read_text(encoding="utf-8"))
FORA = {(e["janela"], e["linha"]) for e in EXCECOES["jpl8243p5"]}
CASOS = [(a, k) for a in REF for k in ("c3l_1", "c3l_2", "vhp_1", "vhp_2") if (a, k) not in FORA]


def _premissa(nome):
    cfg = yaml.safe_load((RAIZ / "config" / "premissas.yaml").read_text(encoding="utf-8"))
    return next(p["valor"] for p in cfg["premissas"] if p["nome"] == nome)


@pytest.mark.parametrize(("ano", "linha"), CASOS, ids=lambda x: str(x))
def test_c3l_e_vhp_nas_datas_do_manual(ano, linha):
    eph.carregar_kernels()
    r = REF[ano][linha]
    c3, vinf, _, _ = pc.transferencia(eph.BARICENTRO_MARTE, eph.BARICENTRO_TERRA_LUA,
                                      spice.str2et(f"{r['partida']} 00:00 TDB"),
                                      spice.str2et(f"{r['chegada']} 00:00 TDB"))
    calc = c3 if linha.startswith("c3l") else vinf
    assert abs(calc - float(r["valor"])) / float(r["valor"]) < _premissa("tolerancia_jpl8243_rel")


def test_excecoes_existem_e_tem_motivo():
    for e in EXCECOES["jpl8243p5"]:
        assert e["linha"] in REF[e["janela"]]
        assert e["motivo"].strip()
