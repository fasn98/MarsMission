"""Etapa 4.6: resumo integrado da Fase 4 (tools/fase4.py)."""

from __future__ import annotations

import pytest

from orbital.config import ler


def test_resumo_coerente_com_a_arquitetura():
    r = ler("results/fase4/resumo.yaml")
    m, lc = r["massas"], r["lancadores"]
    assert m["total_leo_kg"] == pytest.approx(m["orbitador_leo_kg"] + m["lander_leo_kg"], rel=1e-12)
    ar = ler("results/etapa2.5/arquitetura.yaml")
    assert m["lander_injetado_kg"] == pytest.approx(ar["lander"]["injetado_kg"], rel=1e-9)
    base = ler("config/lancadores.yaml")["base"]
    mb = ar["lancadores"]["margens_base"]
    assert lc["lander"]["margem_base"] == pytest.approx(mb["lander"][base["lander"]], rel=1e-9)
    assert lc["orbitador"]["margem_base"] == pytest.approx(mb["orbitador"][base["orbitador"]], rel=1e-9)
    # a pior margem nas sensibilidades não passa da margem na base (o caso Base está entre as sensibilidades)
    for k in ("orbitador", "lander", "lander_reserva"):
        assert lc[k]["pior"]["margem"] <= lc[k]["margem_base"] + 1e-12
    assert m["plataforma_superficie_kg"] == pytest.approx(ler("config/superficie.yaml")["lander"]["plataforma_superficie_kg"]["valor"])
