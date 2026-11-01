"""Etapa 4.5: lista de massas do lander (tools/lista_massas_lander.py)."""

from __future__ import annotations

import pytest

from orbital.config import ler, v

C = ler("config/lista_massas.yaml")


def test_lista_e_casos():
    r = ler("results/etapa4.5/lista_massas.yaml")
    assert r["itens_todos_kg"] == pytest.approx(sum(x["prevista_kg"] for x in r["itens"]), rel=1e-12)
    for x in r["itens"]:
        if "basica_kg" in x:
            assert x["prevista_kg"] == pytest.approx(x["basica_kg"] * (1 + x["margem"]), rel=1e-12)
    a, b, c = r["casos"]
    assert b["plataforma_kg"] == pytest.approx(a["plataforma_kg"] + r["itens_novos_kg"] - r["dupla_contagem_energia_mav_kg"], rel=1e-12)
    assert b["lander_injetado_kg"] > a["lander_injetado_kg"]
    # o orbitador não muda com a plataforma do lander
    assert a["orbitador_injetado_kg"] == pytest.approx(b["orbitador_injetado_kg"], rel=1e-12)


def test_calor_e_isp():
    r = ler("results/etapa4.5/lista_massas.yaml")
    rc = C["rejeicao_calor_cruzeiro"]
    assert r["circuito_fluido_kg"] == pytest.approx(v(rc["mpf_massa_max_kg"]) * r["calor_cruzeiro_w"] / v(rc["mpf_calor_w"]), rel=1e-12)
    m = [x["lander_injetado_kg"] for x in sorted(r["mav_isp"], key=lambda x: x["isp_s"])]
    assert all(b < a for a, b in zip(m, m[1:]))   # Isp maior, lander mais leve
