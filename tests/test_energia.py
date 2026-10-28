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
    assert r["orbitador"]["proposta"]["carga_w"] >= r["orbitador"]["atual"]["carga_w"]
