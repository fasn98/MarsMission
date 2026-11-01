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
    assert c["plataforma_kg"] == pytest.approx(r["m2020_descida_seca_kg"] + r["itens_todos_kg"] - r["dupla_contagem_energia_mav_kg"], rel=1e-12)
    # folga do núcleo: L3 menos os itens dentro dele (todos menos braço e helicópteros), devolvida a energia do MAV
    fora = sum(x["prevista_kg"] for x in r["itens"] if x["item"].startswith(("Braço", "Helicópteros")))
    assert r["folga_para_o_nucleo_kg"] == pytest.approx(r["l3_kg"] - (r["itens_todos_kg"] - fora) + r["dupla_contagem_energia_mav_kg"], rel=1e-12)
    # o orbitador não muda com a plataforma do lander
    assert a["orbitador_injetado_kg"] == pytest.approx(b["orbitador_injetado_kg"], rel=1e-12)
    assert c["orbitador_injetado_kg"] == pytest.approx(b["orbitador_injetado_kg"], rel=1e-12)


def test_dupla_contagem_e_rhus():
    r = ler("results/etapa4.5/lista_massas.yaml")
    arq = ler("results/etapa2.5/arquitetura.yaml")["lander"]
    mav = next(x["massa_kg"] for x in arq["composicao"] if x["item"].startswith("MAV"))
    assert r["dupla_contagem_energia_mav_kg"] == pytest.approx(mav - arq["mav"]["estagios"][0]["massa_inicial_kg"], rel=1e-12)
    assert r["dupla_contagem_energia_mav_kg"] > 0
    # número de RHUs igual ao da Etapa 4.1
    n = ler("results/etapa4.1/energia.yaml")["lander"]["variante_rhu"]["rhu_quantidade"]
    rhu = next(x for x in r["itens"] if x["item"].startswith("RHUs"))
    assert rhu["basica_kg"] == pytest.approx(n * v(C["itens_novos"]["rhu_massa_g"]) / 1e3, rel=1e-12)


def test_calor_e_isp():
    r = ler("results/etapa4.5/lista_massas.yaml")
    rc = C["rejeicao_calor_cruzeiro"]
    t = ler("config/termico.yaml")["cruzeiro"]
    rhu = ler("results/etapa4.2/termico.yaml")["cruzeiro"]["rhu_w"]
    assert r["calor_cruzeiro_w"] == pytest.approx(v(t["srl_dissipacao_max_lamp_w"]) + rhu, rel=1e-12)
    assert r["rejeicao_ativa_necessaria"] == (r["calor_cruzeiro_w"] > v(t["srl_perda_passiva_max_w"]))
    assert r["circuito_fluido_kg"] == pytest.approx(v(rc["mpf_massa_max_kg"]) * r["calor_cruzeiro_w"] / v(rc["mpf_calor_w"]), rel=1e-12)
    m = [x["lander_injetado_kg"] for x in sorted(r["mav_isp"], key=lambda x: x["isp_s"])]
    assert all(b < a for a, b in zip(m, m[1:]))   # Isp maior, lander mais leve
