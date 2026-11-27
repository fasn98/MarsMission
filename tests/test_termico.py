"""Etapa 4.2: controle térmico (tools/termico.py)."""

from __future__ import annotations

import re
from pathlib import Path

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


def test_aquecimento_do_solido_tem_uma_so_fonte():
    """Errata da issue #77: o aquecimento do MAV sólido vem da lei nominal da P-113 (results/familia1/inerte_solido.yaml), com
    a mesma conta (orbital.mav.aquecimento) do hipergólico e das colunas da P-111 em results/familia1/mavs.yaml."""
    from orbital.mav import aquecimento
    aq, tf = ler("config/mav_propulsao.yaml")["aquecimento"], ler("config/familia1.yaml")["termico"]
    mv, ins = ler("results/familia1/mavs.yaml"), ler("results/familia1/inerte_solido.yaml")
    nom = next(c for c in ins["casos"] if c["lei"] == ins["variante_nominal"])
    sol = [(nom[k]["termico"], sum(nom[k]["propelente_kg"])) for k in ("sem_margem", "com_margem")]
    p111 = [(x["termico"], sum(x["propelente_kg"]) if isinstance(x["propelente_kg"], list) else x["propelente_kg"])
            for t in ("solido", "hipergolico") for x in mv[t] if "termico" in x]
    assert len(sol) == 2 and len(p111) >= 3
    # as entradas do sólido da P-113 são as do caso de 380 km (as mesmas de mavs.yaml), não lidas do próprio resultado
    cm = next(c for c in ler("results/familia1/missao.yaml")["casos"] if c["altitude_km"] == ins["altitude_km"])
    for t, _ in sol:
        assert (t["temperatura_c"], t["ano"], t["dias"]) == (v(aq["t_minima_c"]["O1"]), int(str(cm["lancamento_mav"])[:4]), cm["mav_na_superficie_dias"])
    for t, m in sol + p111:
        assert aquecimento(aq, tf, t["temperatura_c"], m, t["ano"], t["dias"]) == pytest.approx(t, rel=1e-12)
    # o sólido da P-113 tem menos propelente que o da P-111 com margem, logo menos aquecimento
    com_p111 = next(x for x in mv["solido"] if "termico" in x and "com a margem" in x["rotulo"])
    assert nom["com_margem"]["termico"]["potencia_w"] < com_p111["termico"]["potencia_w"]
    # a estocagem do diagnóstico lê o sólido da P-113: as linhas "lei A da P-113" têm o aquecimento de inerte_solido.yaml
    diag = (Path(__file__).resolve().parents[1] / "results/familia1/diagnostico_orbitador_so_eletrico.md").read_text(encoding="utf-8")
    est = diag[diag.index("## Estocagem do MAV na superfície"):]
    for rot, k in (("sem margem", "sem_margem"), ("com a margem da P-014", "com_margem")):
        linhas = [x.split(" | ") for x in est.splitlines() if f"da P-113, {ins['altitude_km']:.0f} km, {rot} |" in x]
        assert linhas and all(x[9] == f"{nom[k]['termico']['potencia_w']:.1f}".replace(".", ",") for x in linhas)
