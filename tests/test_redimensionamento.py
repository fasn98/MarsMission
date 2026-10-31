"""Redimensionamento da Etapa 3.1 (ADR 0011): perdas calculadas no lugar da P-015, ponto fixo e histórico das etapas antigas."""

from __future__ import annotations

import shutil

import pytest
import yaml

from orbital import perdas as pd
from orbital import veiculos as ve
from orbital.config import RAIZ, ler, v
from orbital.historico import ARQUIVOS_3_1, aplicar_antes_etapa_3_1


def test_dimensionamento_le_a_perda_calculada_de_results():
    dcfg = ler("config/dimensionamento.yaml")
    r = ler("results/etapa3.1/perdas_calculadas.yaml")
    assert r["estado"] == "convergido"
    for k in ("captura_marte", "saida_marte"):
        assert v(dcfg["dv"]["perda_gravitacional"][k]) == r["perda_km_s"][k]
    assert v(dcfg["dv"]["perda_gravitacional"]["saida_terra"]) == 0.148   # a saída da Terra continua com a P-015


def test_ponto_fixo_fecha_nas_massas_atuais():
    """Recalcular as perdas nas massas do dimensionamento atual devolve as gravadas, dentro da tolerância (P-044)."""
    r = ler("results/etapa3.1/perdas_calculadas.yaml")
    tol = v(ler("config/queima_finita.yaml")["redimensionamento"]["tolerancia_km_s"])
    novo = pd.perdas_projeto(ve.veiculos(detalhe=True)[0])
    for k in ("captura_marte", "saida_marte"):
        assert novo["perda_km_s"][k] == pytest.approx(r["perda_km_s"][k], abs=tol)
    esc = ler("config/motores.yaml")["escolha"]
    assert novo["captura"]["combinacao"] == esc["captura"] and novo["saida"]["combinacao"] == esc["retorno"]


def test_motores_escolhidos_no_config():
    esc = ler("config/motores.yaml")["escolha"]
    assert esc == {"captura": "C4", "retorno": "R3", "cruzeiro": "Z1", "mav_1": "M2", "mav_2": "N2"}
    assert v(ler("config/dimensionamento.yaml")["estagios"]["insercao_marte"]["isp_s"]) == 310
    assert v(ler("config/superficie.yaml")["lancamento"]["cruzeiro_lander"]["isp_s"]) == 292
    assert ler("config/mav_propulsao.yaml")["opcoes"]["O4"]["isp_s"] == [310, 310]


def test_eps_do_mav_pressurizado_e_sensibilidade():
    """ε do MAV pressurizado de Bowles (0,230) na base; o caso pessimista (0,238) pesa mais e o otimista (0,176) menos,
    e o override do config pelo argumento mcfg não muda o orbitador."""
    import copy
    mcfg = ler("config/mav_propulsao.yaml")
    fe = mcfg["opcoes"]["O4"]["fracao_estrutural"]
    assert v(fe) == 0.230
    assert [v(fe["sensibilidade"][k]) for k in ("pessimista", "otimista", "ilustracao_risco")] == [0.238, 0.176, 0.30]
    base = ve.veiculos()[0]
    massas = {}
    for k in ("pessimista", "otimista"):
        m2 = copy.deepcopy(mcfg)
        m2["opcoes"]["O4"]["fracao_estrutural"]["valor"] = v(fe["sensibilidade"][k])
        r = ve.veiculos(mcfg=m2)[0]
        assert r["orbitador_regra_iii"]["injetada_kg"] == base["orbitador_regra_iii"]["injetada_kg"]
        massas[k] = r["lander"]["injetada_kg"]
    assert massas["otimista"] < base["lander"]["injetada_kg"] < massas["pessimista"]


def test_historico_antes_da_etapa_3_1_volta_os_valores_antigos(tmp_path):
    for a in ARQUIVOS_3_1 + ("config/motores.yaml",):
        (tmp_path / a).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(RAIZ / a, tmp_path / a)
    aplicar_antes_etapa_3_1(tmp_path)
    d = yaml.safe_load((tmp_path / "config/dimensionamento.yaml").read_text(encoding="utf-8"))
    assert v(d["estagios"]["insercao_marte"]["isp_s"]) == 321 and v(d["estagios"]["retorno"]["isp_s"]) == 321
    assert v(d["dv"]["perda_gravitacional"]["captura_marte"]) == 0.018
    assert v(d["dv"]["perda_gravitacional"]["saida_marte"]) == 0.011
    s = yaml.safe_load((tmp_path / "config/superficie.yaml").read_text(encoding="utf-8"))
    assert v(s["lancamento"]["cruzeiro_lander"]["isp_s"]) == 321
    m = yaml.safe_load((tmp_path / "config/mav_propulsao.yaml").read_text(encoding="utf-8"))
    assert m["opcoes"]["O4"]["isp_s"] == [343, 343]
    assert m["opcoes"]["O4"]["fracao_estrutural"]["valor"] == 0.238
    with pytest.raises(RuntimeError):   # aplicar duas vezes: as linhas novas não existem mais
        aplicar_antes_etapa_3_1(tmp_path)
