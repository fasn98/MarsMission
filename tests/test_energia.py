"""Etapa 4.1: geometria solar em Marte, insolação na superfície (Appelbaum & Landis [F130]), MMRTG e resultados."""

from __future__ import annotations

import math

import pytest

from orbital import energia as en
from orbital.config import ler, v

C = ler("config/energia.yaml")
FL = C["lander"]["fluxo_liquido"]
P050 = next(p for p in ler("config/premissas.yaml")["premissas"] if p["id"] == "P-050")["valor"]


def test_solsticio_do_norte_em_ls_90():
    """A declinação máxima cai em Ls = 90°, dentro do quanto Ls anda num passo da busca (2 dias)."""
    import datetime as dt
    d0 = dt.datetime(2029, 1, 1)
    g = [en.geometria_marte((d0 + dt.timedelta(days=2 * k)).strftime("%Y-%m-%dT00:00:00")) for k in range(350)]
    i = max(range(len(g)), key=lambda k: g[k][1])
    passo_ls = (g[i + 1][0] - g[i][0]) % 360.0
    assert abs(g[i][0] - 90.0) <= passo_ls and g[i][1] > 0


def test_insolacao_no_topo_no_equador_no_equinocio():
    """φ = δ = 0: Q = S T / π (meio-dia a meio-dia, geometria esférica)."""
    assert en.insolacao_topo(0.0, 0.0, 1.0, 1000.0, 24.0) == pytest.approx(1000.0 * 24.0 / math.pi, rel=1e-12)


@pytest.mark.parametrize("tau,z,tabela", [(0.5, 0.0, 0.813), (1.0, 0.0, 0.728), (0.5, 40.0, 0.778)])
def test_fluxo_liquido_reproduz_a_tabela_iii_da_fonte(tau, z, tabela):
    """[F130] Tab. III(a), albedo 0,1; tolerância da P-050 (erro médio do ajuste declarado pela fonte, menor até 40°)."""
    assert en.fluxo_liquido_normalizado(z, tau, 0.1, FL["k0"], FL["k1"]) == pytest.approx(tabela, rel=P050["tolerancia_teste_fluxo"])


def test_mmrtg_degrada_composto():
    assert en.potencia_mmrtg(110.0, 0.048, 2.0) == pytest.approx(110.0 * 0.952 ** 2, rel=1e-12)


def test_resultado_da_etapa_4_1():
    r = ler("results/etapa4.1/energia.yaml")
    # verificação contra a tabela do VL1 [F56] dentro do erro máximo declarado do ajuste da fonte (P-050, [F130] p. 14)
    assert r["lander"]["verificacao_vl1"]["maior_diferenca_relativa"] <= P050["tolerancia_teste_vl1"]
    s = {(x["cenario"], x["carga"]): x["area_m2"] for x in r["lander"]["solar"]}
    assert s[("claro_jezero", "operação normal")] < s[("regional_jezero", "operação normal")] < s[("global_2018", "operação normal")]
    assert r["orbitador"]["adotada"]["carga_w"] > r["orbitador"]["anterior"]["carga_w"]


def test_bases_iguais_mmrtg_e_solar():
    """Picos pela soma das cargas do config; o MMRTG leva a margem da geração e a bateria dos picos (P-054)."""
    r = ler("results/etapa4.1/energia.yaml")["lander"]
    pk = C["lander"]["picos"]
    esperado = (pk["braco"]["potencia_w"] * v(pk["braco"]["horas_por_sol"])
                + v(pk["recarga_helicopteros"]["energia_por_voo_wh"]) * v(pk["recarga_helicopteros"]["voos_por_sol"])
                + v(pk["transmissoes_uhf"]["potencia_w"]) * v(pk["transmissoes_uhf"]["passes_por_sol"]) * v(pk["transmissoes_uhf"]["minutos_por_passe"]) / 60)
    assert r["pico_total_wh"] == pytest.approx(esperado, rel=1e-12)
    m = r["mmrtg"]
    assert m["margem_crescimento"] > 0 and m["bateria_kg"] > 0
    assert m["massa_kg"] == pytest.approx(m["massa_sem_margem_kg"] * (1 + m["margem_crescimento"]) + m["bateria_kg"], rel=1e-12)



def test_atividade_do_pu238_pela_meia_vida():
    """A = ln2/T½ · m/M · N_A; 1 g de Pu-238 dá ~0,63 TBq (conta independente, sem a ferramenta)."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
    import energia as te
    pu = C["lander"]["pu238"]
    r = te.nspm20(1.0, pu)
    t = v(pu["meia_vida_anos"]) * v(pu["dias_por_ano"]) * 86400.0
    assert r["atividade_tbq"] == pytest.approx(math.log(2) / t / v(pu["massa_molar_g_mol"]) * v(pu["avogadro_mol"]) / 1e12, rel=1e-12)
    assert r["multiplo_a2"] == pytest.approx(r["atividade_tbq"] / v(pu["a2_tbq"]), rel=1e-12)
    m = ler("results/etapa4.1/energia.yaml")["lander"]["mmrtg"]
    assert m["nspm20"]["multiplo_a2"] > v(pu["tier_i_max_a2"])   # duas MMRTG ficam acima do Tier I


def test_sobrevivencia_da_opcao_c():
    """Carga de sobrevivência = MAV + aquecedores escalados (P-056) + eletrônica; a opção C cobre os dois casos."""
    r = ler("results/etapa4.1/energia.yaml")["lander"]
    sv, sb = C["lander"]["sobrevivencia"], r["sobrevivencia"]["base"]
    aq = (v(sv["aquecedores_mer_wh_sol"]) + v(sv["rhu_mer_quantidade"]) * v(sv["rhu_w"]) * v(ler("config/plataformas.yaml")["lander"]["energia"]["duracao_sol_h"])) * (r["sobrevivencia"]["plataforma_lander_kg"] / v(sv["massa_mer_kg"])) ** v(sv["expoente_escala"])
    assert sb["aquecedores_lander_wh_sol"] == pytest.approx(aq, rel=1e-12)
    assert sb["total_wh_sol"] == pytest.approx(sb["mav_wh_sol"] + aq + v(sv["eletronica_mer_wh_sol"]), rel=1e-12)
    c = r["solar_com_sobrevivencia"]
    assert c["area_m2"] >= r["solar"][0]["area_m2"] and c["area_m2"] >= r["solar"][3]["area_m2"]
    a6 = r["acima_do_modelo"]
    pts = {x["sol"]: x["wh"] for x in C["lander"]["tempestade_2018_opportunity"]["pontos"]}
    assert a6["razao_medida"] == pytest.approx(pts[5111] / pts[5100], rel=1e-12)   # [F140]: τ = 10,8 sobre τ = 0,64
    assert a6["base"]["cobertura"] == pytest.approx(a6["base"]["energia_disponivel_wh_sol"] / a6["base"]["necessaria_wh_sol"], rel=1e-12)


def test_variante_rhu_e_potencia_especifica():
    """Potência específica do Pu-238 pela física confere com a da MMRTG publicada [F135]; RHUs em Tier I (NSPM-20)."""
    r = ler("results/etapa4.1/energia.yaml")["lander"]
    vr = r["variante_rhu"]
    tol = next(p for p in ler("config/premissas.yaml")["premissas"] if p["id"] == "P-060")["valor"]
    assert abs(vr["diferenca_relativa_potencia_especifica"]) <= tol   # P-060: arredondamentos da ficha da MMRTG e da meia-vida
    assert vr["pu238_g"] == pytest.approx(vr["rhu_quantidade"] * vr["rhu_w_cada"] / vr["potencia_especifica_w_g"], rel=1e-12)
    assert vr["rhu_quantidade"] >= vr["sobrevivencia"]["rhu_lander_w"] / vr["rhu_w_cada"]
    assert vr["sobrevivencia"]["total_wh_sol"] < r["sobrevivencia"]["base"]["total_wh_sol"]
    assert vr["nspm20"]["multiplo_a2"] <= v(C["lander"]["pu238"]["tier_i_max_a2"])


def test_sensibilidade_do_fator_do_opportunity():
    r = ler("results/etapa4.1/energia.yaml")["lander"]
    s = r["sensibilidade_fator_opportunity"]
    c = next(x for x in r["comparacao_opportunity_2018"] if x["razao_modelo"] is not None)
    assert s["fator"] == pytest.approx(c["razao_modelo"] / c["razao_medida"], rel=1e-12) and s["fator"] > 1
    for x in s["cenarios"]:
        assert x["area_com_fator_m2"] == pytest.approx(x["area_m2"] * s["fator"], rel=1e-9)


def test_tempestade_global_na_estada():
    r = ler("results/etapa4.1/energia.yaml")["lander"]["tempestade_global_na_estada"]
    tg = C["lander"]["tempestades_globais"]
    assert r["inicios_catalogo"] == len(tg["inicios"])
    assert r["inicios_dentro_da_estada"] + len(r["inicios_antes_da_chegada_na_estacao"]) <= r["inicios_catalogo"]
    assert 0 < r["fracao_da_estacao_dentro_da_estada"] <= 1
    assert r["probabilidade_por_ano_marciano"] == v(tg["probabilidade_por_ano_marciano"])
