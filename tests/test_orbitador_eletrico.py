"""Etapa 3.3: geometria das assíntotas, orbitador híbrido (orbital.hibrido) e descida em arcos."""

from __future__ import annotations

import math

import pytest

from orbital import baixo_empuxo as be
from orbital import hibrido as hb
from orbital import plataforma as pf
from orbital.config import ler, v

TOL = v(ler("config/baixo_empuxo.yaml")["verificacao_schwenzfeger"]["tolerancia_relativa"])   # P-046
MU, R = 42828.0, 3396.0   # valores de teste


def test_geometria_dos_planos():
    r = ler("results/etapa3.3/geometria_planos.yaml")
    assert len(r["missoes"]) == 4
    i = r["inclinacao_encontro_graus"]
    for x in r["missoes"]:
        # mesmo Lambert e mesmas datas da Etapa 1.3, que grava o v∞ com 4 casas: só pode diferir pelo arredondamento
        assert abs(x["vinf_chegada_km_s"] - x["vinf_chegada_etapa1_3_km_s"]) <= 0.5e-4
        assert x["excesso_chegada_graus"] == max(0.0, abs(x["declinacao_chegada_graus"]) - i)
        assert x["excesso_partida_graus"] == max(0.0, abs(x["declinacao_partida_graus"]) - i)
    assert r["maior_excesso_graus"] == max(max(x["excesso_chegada_graus"], x["excesso_partida_graus"]) for x in r["missoes"])


def test_tempos_da_espiral_conferem_com_a_numerica():
    se = hb.SistemaEletrico(4, 5, 0.25, 3000.0, 4500.0, 10.0, 20.0, 10.0, 0.13, 22.0, 0.2, 0.15, 0.275)
    t_on, t_dec, dv, mf = hb.tempos_espiral(MU, R, R + 3000.0, R + 400.0, 2000.0, se)
    num = be.espiral(MU, R + 3000.0, R + 400.0, empuxo_n=se.empuxo_total_n, isp_s=se.isp_s, m0_kg=2000.0)
    assert num.dv == pytest.approx(dv, rel=TOL) and num.duracao == pytest.approx(t_on, rel=TOL)
    assert t_dec > t_on   # motor desligado no eclipse


def test_massas_do_hibrido_fecham_o_propelente():
    """Refazendo as queimas de frente para trás com as massas devolvidas, o orbitador termina com a massa final."""
    se = hb.SistemaEletrico(2, 3, 0.1, 3000.0, 2300.0, 8.0, 13.0, 11.0, 0.13, 22.0, 0.2, 0.2, 0.275)
    dv = {"correcoes_ida": 0.05, "captura": 2.0, "descida": 1.0, "encontro": 0.1, "subida": 1.0, "saida": 2.0,
          "correcoes_volta": 0.05, "desvio": 0.02}
    m = hb.massas(dv, se, 310.0, 0.24, 0.24, 1500.0, 100.0, 50.0)
    c, cx = 310.0 * 9.80665e-3, 3000.0 * 9.80665e-3
    x = m["massa_antes_descida_kg"] * math.exp(-dv["descida"] / cx) - 100.0
    x *= math.exp(-dv["encontro"] / c)
    assert x == pytest.approx(m["massa_antes_subida_kg"], rel=1e-12)
    for k, cc in (("subida", cx), ("saida", c), ("correcoes_volta", c)):
        x *= math.exp(-dv[k] / cc)
    x = (x - 50.0) * math.exp(-dv["desvio"] / c)
    assert x == pytest.approx(m["massa_final_kg"], rel=1e-9)
    # inserção: queima as correções e a captura e entrega a massa antes da descida mais o próprio inerte
    ins = m["injetada_kg"] * math.exp(-(dv["correcoes_ida"] + dv["captura"]) / c)
    assert ins == pytest.approx(m["massa_antes_descida_kg"] + m["insercao"]["inerte_kg"], rel=1e-12)
    assert m["insercao"]["inerte_kg"] == pytest.approx(0.24 / 0.76 * m["insercao"]["propelente_kg"], rel=1e-12)
    # massa final = carga + sistema elétrico + inertes do retorno e do xenônio
    assert m["massa_final_kg"] == pytest.approx(1500.0 + se.massa_seca_kg() + m["retorno"]["inerte_kg"] + m["eletrico"]["tanque_e_residuo_kg"], rel=1e-12)


def test_hiperbole_e_eclipse():
    """Δv para a circular pela energia; fração em eclipse da circular igual à do modelo da plataforma (mesmo pior caso)."""
    vinf, r = 3.0, R + 1000.0
    vp = math.sqrt(vinf ** 2 + 2 * MU / r)
    assert hb.dv_hiperbole_circular(MU, vinf, r) == pytest.approx(vp - math.sqrt(MU / r), rel=1e-15)
    t_ecl, per = pf.eclipse_maximo(MU, R, r, r)
    assert hb.fracao_eclipse_circular(R, r) == pytest.approx(t_ecl / per, abs=1.0 / 20001 + 1e-12)   # resolução da amostragem de pf


def test_arcos_tendem_ao_impulso_no_periapse():
    """O Δv em arcos fica acima do impulsivo no periapse (v_p − v_c) e se aproxima dele com arcos menores."""
    rp, ra = R + 300.0, R + 20000.0
    imp = math.sqrt(MU * (2 / rp - 2 / (rp + ra))) - math.sqrt(MU / rp)
    d = {th: be.apoapse_por_arcos(MU, rp, ra, rp * 1.001, 20.0, 3000.0, 3000.0, th) for th in (10.0, 30.0)}
    assert imp < d[10.0].dv_km_s < d[30.0].dv_km_s          # arco finito custa mais; arco menor custa menos
    assert d[10.0].tempo_total_s > d[30.0].tempo_total_s     # e leva mais tempo
    assert d[30.0].tempo_total_s > d[30.0].tempo_empuxo_s


def test_resultado_da_etapa_3_3():
    r = ler("results/etapa3.3/orbitador_eletrico.yaml")
    for nome, x in r["hibrido_c2"].items():
        if x["n_minimo"] is not None:
            assert abs(x["conferencia_descida"]["diferenca_relativa"]) < TOL
    q = r["quimico"]
    assert q["orbitador_injetado_kg"] == ler("results/etapa2.5/arquitetura.yaml")["orbitador"]["injetado_kg"]
