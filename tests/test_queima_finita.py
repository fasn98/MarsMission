"""Queima finita (orbital.queima_finita), catálogo de motores (orbital.motores) e massas por queima (Etapa 3.1)."""

from __future__ import annotations

import math
import re

import numpy as np
import pytest

from orbital import manobras as mn
from orbital import motores as mt
from orbital import queima_finita as qf
from orbital import veiculos as ve
from orbital.config import ler, parametros, v
from orbital.foguete import G0

P = parametros()
MU, R = P.mu_marte, v(ler("config/parametros_orbitais.yaml")["raio_marte_km"])
UM = P.orbitas_marte["eliptica_alta"]


def test_captura_com_empuxo_muito_alto_reproduz_o_impulso():
    r = qf.captura(MU, R, qf.Motor(1e7, 321), 6000.0, 3.0, UM.rp, UM.ra)
    assert abs(r.perda_km_s) < 1e-5                     # < 1 cm/s
    assert r.dv_impulsivo_km_s == pytest.approx(float(mn.dv_hiperbole_orbita(MU, 3.0, UM.rp, UM.ra)))
    assert r.rp_final_km == pytest.approx(UM.rp - R, rel=qf.TOL_ALVO)
    assert r.ra_final_km == pytest.approx(UM.ra - R, rel=qf.TOL_ALVO)


def test_saida_com_empuxo_muito_alto_reproduz_o_impulso():
    r = qf.saida(MU, R, qf.Motor(1e7, 321), 3000.0, UM.rp, UM.ra, 3.0)
    assert abs(r.perda_km_s) < 1e-5
    assert r.vinf_final_km_s == pytest.approx(3.0, rel=1e-9)


def test_propelente_e_dv_do_motor_seguem_a_equacao_do_foguete():
    m0 = 6000.0
    motor = qf.Motor(4000.0, 315.0)
    r = qf.captura(MU, R, motor, m0, 3.0, UM.rp, UM.ra)
    assert r.propelente_kg == pytest.approx(motor.vazao_kg_s * r.duracao_s, rel=1e-9)   # vazão constante
    assert r.dv_motor_km_s == pytest.approx(motor.isp_s * G0 * math.log(m0 / (m0 - r.propelente_kg)), rel=1e-12)


def test_perda_cresce_quando_o_empuxo_cai():
    perdas = [qf.captura(MU, R, qf.Motor(t, 321), 6000.0, 3.0, UM.rp, UM.ra).perda_km_s for t in (20000.0, 4000.0, 1000.0)]
    assert 0 < perdas[0] < perdas[1] < perdas[2]
    saidas = [qf.saida(MU, R, qf.Motor(t, 321), 3000.0, UM.rp, UM.ra, 3.0).perda_km_s for t in (20000.0, 2000.0, 500.0)]
    assert 0 < saidas[0] < saidas[1] < saidas[2]


def test_captura_com_empuxo_baixo_nao_entra_em_marte_e_atinge_o_alvo():
    r = qf.captura(MU, R, qf.Motor(850.0, 321), 6000.0, 3.0, UM.rp, UM.ra)
    assert r.altitude_minima_km > 0 and r.periapse_chegada_alt_km > UM.rp - R   # a continuação sobe o periapse de chegada
    assert r.ra_final_km == pytest.approx(UM.ra - R, rel=qf.TOL_ALVO)


def test_catalogo_tem_fonte_em_todo_valor_e_converte_unidades():
    cfg = ler("config/motores.yaml")
    for nome, m in cfg["motores"].items():
        for campo in ("empuxo_n", "isp_s", "massa_kg"):
            assert re.search(r"\[F\d+\]", m[campo]["fonte"]), (nome, campo)
        assert re.search(r"\[F\d+\]", m["voo"]) or "NÃO COMPROVADO" in m["voo"], nome
    cat = mt.catalogo(cfg)
    assert cat["R-4D-11"]["empuxo_n"] == pytest.approx(110 * 4.448222)   # NIST SP 811 [F112]
    assert cat["OMS-E"]["massa_kg"] == pytest.approx(297 * 0.4535924)
    usados = {p["motor"] for f in cfg["combinacoes"].values() for c in f.values() for p in c["motores"]}
    assert usados <= set(cfg["motores"]) and not any(cat[m]["sem_combinacao"] for m in usados)


def test_conjunto_soma_empuxo_e_massa():
    c = next(x for x in mt.conjuntos("captura") if x.nome == "C2")
    cat = mt.catalogo()
    assert c.motor.empuxo_n == pytest.approx(8 * cat["R-4D-11"]["empuxo_n"]) and c.massa_kg == pytest.approx(8 * cat["R-4D-11"]["massa_kg"])
    assert c.motor.isp_s == cat["R-4D-11"]["isp_s"]


def test_massa_antes_de_cada_queima_fecha_com_o_propelente():
    vei = ve.veiculos()[0]
    for veic in ("orbitador_regra_iii", "lander"):
        for e in vei[veic]["estagios"]:
            q = e["queimas"]
            assert q[0]["massa_antes_kg"] <= e["massa_inicial_kg"] + 1e-9
            for a, b in zip(q, q[1:]):
                assert b["massa_antes_kg"] <= a["massa_antes_kg"] - a["propelente_kg"] + 1e-9   # igual, menos descartes
            assert sum(x["propelente_kg"] for x in q) == pytest.approx(e["propelente_kg"], rel=1e-12)
    mav = vei["lander"]["mav_estagios"]
    assert [x["nome"] for x in mav] == ["mav_1", "mav_2"] and mav[0]["massa_inicial_kg"] > mav[1]["massa_inicial_kg"]


def test_resultado_da_etapa_3_1_compara_com_a_p015():
    r = ler("results/etapa3.1/queima_finita.yaml")
    assert r["p015_km_s"] == {"captura_marte": 0.018, "saida_marte": 0.011}
    for x in r["captura"] + r["saida"]:
        assert np.isfinite(x["perda_km_s"]) and x["perda_km_s"] > 0


def test_parametros_numericos_p041_nao_mudam_a_perda(monkeypatch):
    """Sensibilidade à P-041: tolerâncias e continuação diferentes dão a mesma perda dentro de 1e-4 relativo."""
    args = (MU, R, qf.Motor(850.0, 321), 6000.0, 3.0, UM.rp, UM.ra)
    base = qf.captura(*args).perda_km_s
    monkeypatch.setattr(qf, "RTOL", 1e-9)
    monkeypatch.setattr(qf, "PASSO_CONTINUACAO", 1.5)
    monkeypatch.setattr(qf, "DURACAO_INICIAL_S", 30.0)
    assert qf.captura(*args).perda_km_s == pytest.approx(base, rel=1e-4)
    s_base = qf.saida(MU, R, qf.Motor(850.0, 321), 3000.0, UM.rp, UM.ra, 3.0).perda_km_s
    monkeypatch.setattr(qf, "RTOL", 1e-11)
    monkeypatch.setattr(qf, "ATOL", 1e-7)
    assert qf.saida(MU, R, qf.Motor(850.0, 321), 3000.0, UM.rp, UM.ra, 3.0).perda_km_s == pytest.approx(s_base, rel=1e-4)
