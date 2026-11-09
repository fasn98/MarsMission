"""Etapa 7.1: envelope e arranjo (tools/envelope_arranjo.py)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

from orbital.config import ler, v

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import envelope_arranjo as ea  # noqa: E402


def test_geometria_dos_tanques():
    vol = ea.volumes(265.0, 1.65, 1431.0, 869.0, 0.05)
    assert vol["oxidante_kg"] + vol["combustivel_kg"] == pytest.approx(265.0)
    assert vol["tanque_oxidante_m3"] == pytest.approx(265.0 * 1.65 / 2.65 / 1431.0 / 0.95)
    assert math.pi * ea.esfera(1.0) ** 3 / 6 == pytest.approx(1.0)
    # tanque cilíndrico: volume recomposto; volume pequeno vira esfera menor que o diâmetro
    d, vol_t = 0.55, 0.2
    comp = ea.tanque_cilindrico(vol_t, d)
    assert math.pi * d ** 3 / 6 + math.pi * d ** 2 / 4 * (comp - d) == pytest.approx(vol_t)
    assert ea.tanque_cilindrico(0.01, d) == pytest.approx(ea.esfera(0.01))


def test_resultados_coerentes():
    r = ler("results/etapa7.1/envelope.yaml")
    arq = ler("results/etapa2.5/arquitetura.yaml")
    ins = next(x for x in arq["orbitador"]["composicao"] if x["item"].startswith("Estágio de inserção"))
    t = r["orbitador"]["tanques"]["insercao_marte"]
    assert t["propelente_kg"] == pytest.approx(ins["propelente_kg"])
    # conjuntos empilhados sem sobreposição e folga radial calculada contra o perfil do Falcon
    c = r["orbitador"]["conjuntos"]
    assert all(a["h1_m"] <= b["h0_m"] for a, b in zip(c, c[1:]))
    perf = (r["coifas"]["falcon"]["altura_m"], r["coifas"]["falcon"]["raio_m"])
    h_ad = ler("config/cad.yaml")["adaptador_coifa"]["altura_m"]["valor"]   # P-097, lida do config: o veículo sobe a altura do adaptador
    assert r["orbitador"]["altura_adaptador_m"] == h_ad
    assert c[0]["margem_radial_m"] == pytest.approx(ea.margem_conjunto(perf, c[0]["h0_m"] + h_ad, c[0]["h1_m"] + h_ad, c[0]["raio_m"]))
    # MAV: o comprimento é a soma dos segmentos
    for x in r["mav"].values():
        assert x["comprimento_m"] == pytest.approx(sum(s["comprimento_m"] for s in x["segmentos"]))
    # propelente de descida escalado do MSL pela massa de entrada (P-084)
    ds = ler("config/cad.yaml")["descida"]
    assert r["lander"]["descida"]["propelente_kg"] == pytest.approx(v(ds["msl_propelente_kg"]) * arq["lander"]["massa_entrada_kg"] / v(ds["msl_massa_entrada_kg"]))
    # área dos painéis do lander = a da Etapa 4.1
    assert r["lander"]["paineis"]["area_m2"] == pytest.approx(ler("results/etapa4.1/energia.yaml")["lander"]["variante_rhu"]["opcao"]["area_m2"])


def test_envelope_do_vulcan_lido_da_figura():
    vul = ler("config/cad.yaml")["coifas"]["vulcan_15_5"]["perfil"]
    r = ler("results/etapa7.1/envelope.yaml")["coifas"]["vulcan"]
    assert r["altura_m"][-1] == pytest.approx((3100.66 - 2596.66) * 0.0254)
    assert r["raio_m"][0] == pytest.approx(vul["diametro_mm"][0] / 2000)
