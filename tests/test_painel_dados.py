"""Camada de dados do painel (src/painel/dados.py): reproduz results/, rotula cada número e chama src/orbital."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

from painel import dados as d

RAIZ = Path(__file__).resolve().parents[1]
ROTULOS = {d.VERIFICADO, d.CALCULADO}


def _p039():
    """Tolerância da P-039 (config/premissas.yaml): o recálculo no painel pode rodar noutra CPU que gerou results/.
    Nos asserts, o valor de results/ (versionado, a) é comparado com approx(recalculado, b): base |b|, como na P-039."""
    v = next(p["valor"] for p in _ler("config/premissas.yaml")["premissas"] if p["id"] == "P-039")
    return {"rel": float(v["relativa"]), "abs": float(v["piso_absoluto"])}


def _ler(c):
    return yaml.safe_load((RAIZ / c).read_text(encoding="utf-8"))


def _valores(x):
    """Todos os Valor dentro de uma estrutura de dicts e listas."""
    if isinstance(x, d.Valor):
        yield x
    elif isinstance(x, dict):
        for y in x.values():
            yield from _valores(y)
    elif isinstance(x, (list, tuple)):
        for y in x:
            yield from _valores(y)


def _rotulo_valido(v: d.Valor) -> bool:
    if v.rotulo in ROTULOS:
        return True
    if v.rotulo.startswith("premissa "):
        return len(v.premissas) == 1 and v.rotulo == d.rotulo_premissa(v.premissas[0])
    return v.rotulo.startswith("dado de fonte publicada [F") or v.rotulo == "dado publicado"


def test_orcamento_de_base_reproduz_a_arquitetura():
    a = _ler("results/etapa2.5/arquitetura.yaml")
    r = d.orcamento()
    assert a["orbitador"]["injetado_kg"] == pytest.approx(r["veiculos"]["orbitador"]["injetado"].valor, **_p039())
    assert a["lander"]["injetado_kg"] == pytest.approx(r["veiculos"]["lander"]["injetado"].valor, **_p039())
    for veic, margens in a["lancadores"]["margens_base"].items():
        for nome, m in margens.items():
            x = next(y for y in r["lancadores"] if y["veiculo"] == veic and y["lancador"] == nome)
            assert x["escolhido"] and m == pytest.approx(x["margem"].valor, **_p039())


@pytest.mark.parametrize("caso, kw", [
    ("Plataforma do lander no limite superior (SRL 2024 − MAV)", "limite_superior"),
    ("Margem de Δv 5 % (base 10 %)", {"margem_dv": 0.05}),
    ("Margem de Δv 20 % (base 10 %)", {"margem_dv": 0.20}),
])
def test_controles_reproduzem_a_sensibilidade_da_etapa_2_5(caso, kw):
    a = _ler("results/etapa2.5/arquitetura.yaml")
    s = next(x for x in a["sensibilidade"] if x["caso"] == caso)
    if kw == "limite_superior":
        kw = {"plataforma_lander_kg": _ler("results/etapa2.3/plataformas.yaml")["lander"]["limite_superior_srl_2024_kg"]}
    r = d.orcamento(**kw)
    assert s["orbitador_injetado_kg"] == pytest.approx(r["veiculos"]["orbitador"]["injetado"].valor, **_p039())
    assert s["lander_injetado_kg"] == pytest.approx(r["veiculos"]["lander"]["injetado"].valor, **_p039())
    for veic, margens in s["margens"].items():
        for nome, m in margens.items():
            x = next(y for y in r["lancadores"] if y["veiculo"] == veic and y["lancador"] == nome)
            assert m == pytest.approx(x["margem"].valor, **_p039())
            assert x["serve"] == (m >= 0)


def test_isp_e_fracao_estrutural_mudam_a_massa_no_sentido_fisico():
    base = d.orcamento()["veiculos"]
    c = d.controles_base()
    isp_hi = d.orcamento(isp_armazenavel_s=c["isp_armazenavel_s"]["faixa"][1])["veiculos"]
    eps_hi = d.orcamento(fracao_estrutural_armazenavel=c["fracao_estrutural_armazenavel"]["faixa"][1])["veiculos"]
    for v in ("orbitador", "lander"):
        assert isp_hi[v]["injetado"].valor < base[v]["injetado"].valor < eps_hi[v]["injetado"].valor
    # valor igual ao de base não muda nada (o override é o mesmo número do config)
    for k in ("isp_armazenavel_s", "fracao_estrutural_armazenavel"):
        igual = d.orcamento(**{k: c[k]["base"].valor})["veiculos"]
        for v in ("orbitador", "lander"):   # o cruzeiro tem Isp de base próprio (ADR 0011) e também não pode mudar
            assert igual[v]["injetado"].valor == pytest.approx(base[v]["injetado"].valor, rel=1e-12)


def test_orcamento_inviavel_e_informado():
    r = d.orcamento(isp_armazenavel_s=50.0)
    assert r["viavel"] is False and r["erro"]


def test_controles_tem_faixa_que_contem_a_base_e_rotulo():
    for k, c in d.controles_base().items():
        lo, hi = c["faixa"]
        assert lo <= c["base"].valor <= hi, k
        assert _rotulo_valido(c["base"]), (k, c["base"].rotulo)
    assert d.controles_base()["plataforma_lander_kg"]["base"].premissas == ("P-017",)
    assert d.controles_base()["margem_dv"]["base"].premissas == ("P-014",)


def test_todo_numero_tem_rotulo_valido():
    estruturas = [d.missao_referencia(), d.arquitetura(), d.orcamento(), d.controles_base(), d.verificacoes()]
    n = 0
    for e in estruturas:
        for v in _valores(e):
            n += 1
            assert _rotulo_valido(v), v
            assert v.origem
    assert n > 100


def test_rotulo_de_premissa_le_o_status_do_arquivo(monkeypatch):
    assert d.rotulo_premissa("P-017") == "premissa NÃO VALIDADA"
    trocadas = tuple({**p, "status": "ACEITA PELO FABIO"} if p["id"] == "P-017" else p for p in d.premissas())
    monkeypatch.setattr(d, "premissas", lambda: trocadas)
    assert d.rotulo_premissa("P-017") == "premissa ACEITA PELO FABIO"


def test_premissas_e_adrs():
    ps = d.premissas()
    assert len(ps) == len(_ler("config/premissas.yaml")["premissas"])
    numeros = [a["numero"] for a in d.adrs()]
    assert numeros == sorted(numeros) and {f"{i:04d}" for i in range(1, 11)} <= set(numeros)
    assert all(a["status"] for a in d.adrs())   # cada ADR tem a linha "Status:" (Accepted, Proposed…)
    assert all(a["url"].startswith("https://github.com/fasn98/MarsMission/blob/main/docs/adr/") for a in d.adrs())


def test_composicao_rotula_plataformas_como_premissa():
    a = d.arquitetura()
    itens = {x["item"]: x for x in a["orbitador"]["composicao"] + a["lander"]["composicao"]}
    plat = next(x for k, x in itens.items() if k.startswith("Plataforma (P-016"))
    assert plat["massa"].premissas == ("P-016",)
    assert plat["massa"].valor == pytest.approx(_ler("config/dimensionamento.yaml")["plataforma_orbitador_kg"]["valor"])
    est = next(x for k, x in itens.items() if k.startswith("Estágio de inserção"))
    assert est["propelente"].rotulo == d.CALCULADO


def test_missao_referencia_igual_a_results():
    m = d.missao_referencia()
    c = next(x for x in _ler("results/etapa1.3/missoes.yaml")["candidatas"] if x["id"] == "2028-conjuncao")
    assert [dt for _, dt in m["eventos"]] == [c["partida_terra"], c["chegada_marte"], c["partida_marte"], c["chegada_terra"]]
    assert m["duracoes"]["Total"].valor == c["total_dias"]
    assert m["reentrada"]["Velocidade de reentrada"].valor == c["v_reentrada_km_s"]


def test_verificacoes_vem_das_tabelas_publicadas():
    v = d.verificacoes()
    b, j = _ler("results/etapa1.2/verificacao_burke2010.yaml"), _ler("results/etapa1.2/verificacao_jpl8243.yaml")
    assert len(v) == 2 * len(b["linhas"]) + len(j["linhas"])
    assert all(x["calculado"].rotulo == d.VERIFICADO for x in v)
    x = v[0]
    assert x["publicado"].valor == b["linhas"][0]["nasa"]["c3"]
    assert x["dif_rel"] == pytest.approx((b["linhas"][0]["nas_datas_nasa"]["c3"] - b["linhas"][0]["nasa"]["c3"]) / b["linhas"][0]["nasa"]["c3"])


def test_porkchop_exportado_bate_com_a_missao_de_referencia():
    """No ponto da grade da missão de referência, C3 e DLA são os de results/etapa1.3 (arredondados a 4 e 3 casas)."""
    g = d.porkchop("terra_marte", "2028")
    c = next(x for x in _ler("results/etapa1.3/missoes.yaml")["candidatas"] if x["id"] == "2028-conjuncao")
    i = list(g["partida_tdb"]).index(c["partida_terra"])
    k = list(g["chegada_tdb"]).index(c["chegada_marte"])
    assert g["c3_km2_s2"][i, k] == pytest.approx(c["c3_km2_s2"], abs=5e-5)
    assert g["dla_graus"][i, k] == pytest.approx(c["dla_graus"], abs=5e-4)
    idx = d.porkchops()["sentidos"]
    assert set(idx["terra_marte"]["janelas"]) == {"2028", "2031", "2033", "2035"}
    assert set(idx["marte_terra"]["janelas"]) == {"2030", "2032", "2035", "2037", "2039"}
    for s, info in idx.items():
        for jn, x in info["janelas"].items():
            gg = d.porkchop(s, jn)
            assert gg["c3_km2_s2"].shape == tuple(x["pontos"])
            assert ("dla_graus" in gg) == (s == "terra_marte")


def test_mascara_do_porkchop_usa_p006():
    g = {"angulo_transf_graus": np.array([[179.5, 170.0, np.nan]]), "c3_km2_s2": np.array([[10.0, 70.0, np.nan]])}
    assert d.mascara_porkchop(g, 60).tolist() == [[True, True, True]]
    g["c3_km2_s2"] = np.array([[10.0, 10.0, 10.0]])
    assert d.mascara_porkchop(g, 60).tolist() == [[True, False, True]]


def test_trajetoria_fecha_nas_chegadas():
    t = d.trajetoria(pontos_arco=50)
    assert t["erro_chegada_ida_km"] < 1e-3 and t["erro_chegada_volta_km"] < 1e-3
    e0 = t["eventos"][0]
    assert np.allclose(t["ida"][0], e0["terra"], atol=1e-12)
    assert np.allclose(t["terra"][0], e0["terra"], atol=1e-12)
    r = np.linalg.norm(t["terra"], axis=1)
    assert 0.98 < r.min() and r.max() < 1.02          # órbita da Terra ≈ 1 UA (escala UA, IAU 2012)
    assert [e["data_tdb"] for e in t["eventos"]] == [dt for _, dt in d.missao_referencia()["eventos"]]


def test_ferramentas_chamam_as_funcoes_de_src(monkeypatch):
    """tools/ não tem mais cópia própria das funções movidas: usa as de src/orbital."""
    monkeypatch.syspath_prepend(str(RAIZ / "tools"))
    import dimensionamento as dm_t
    import lancamento as lc_t
    import plataformas as pl_t

    from orbital import dimensionamento, lancamento, massa_plataformas, veiculos

    assert dm_t.massa_leo is dimensionamento.massa_leo and dm_t.casos is dimensionamento.casos
    assert lc_t.veiculos is veiculos.veiculos and lc_t.pior_margem_a is lancamento.pior_margem_a
    assert pl_t.prevista is massa_plataformas.prevista and pl_t.lander_base is massa_plataformas.lander_base
    for m in ("dimensionamento", "lancamento", "plataformas"):
        sys.modules.pop(m, None)


def test_nomes_legiveis_vem_do_config_e_de_results():
    """Nomes de exibição: órbita pela descrição do config, missão pelo id de results/ e mínimos pela nota do arquivo."""
    m = d.missao_referencia()
    orbitas = yaml.safe_load((d.RAIZ / "config" / "parametros_orbitais.yaml").read_text(encoding="utf-8"))["orbitas_marte"]
    om = d.orbita_marte(m["orbita_marte"])
    it = orbitas[m["orbita_marte"]]
    assert om["nome"] == it["descricao"].split(",")[0] == "elíptica de 1 sol"
    assert (om["periapse"].valor, om["apoapse"].valor) == (it["periapse_alt_km"]["valor"], it["apoapse_alt_km"]["valor"])
    assert om["periapse"].rotulo == om["apoapse"].rotulo == "dado de fonte publicada [F18]"
    assert d.nome_missao("2028-conjuncao") == "conjunção de 2028"
    assert d.nome_missao("2031-conjuncao_transito_curto") == "conjunção com trânsito curto de 2031"
    classes = yaml.safe_load((d.RAIZ / "config" / "missoes.yaml").read_text(encoding="utf-8"))["classes"]
    assert set(d.NOMES_CLASSE) == set(classes)   # todo nome de classe corresponde a uma classe do config
    assert d.nome_minimo("tipo_1") == "Mín. C3 de partida, tipo I"
    assert d.nome_minimo("min_vinf_tipo_2") == "Mín. v∞ de chegada, tipo II"
    for sentido in ("terra_marte", "marte_terra"):
        nota = _ler(f"results/etapa1.2/minimos_{sentido}.yaml")["nota"]
        assert nota == "tipo_N = mínimo de C3 de partida; min_vinf_tipo_N = mínimo do v∞ de chegada"
        for janela in d.minimos(sentido).values():
            assert all(d.nome_minimo(k) != k for k in janela)   # nenhuma chave de mínimo fica sem nome


def test_estagios_do_orcamento_tem_os_nomes_de_results():
    """Os estágios recalculados no orçamento aparecem com os mesmos nomes dos itens de results/etapa2.5/arquitetura.yaml."""
    a = _ler("results/etapa2.5/arquitetura.yaml")
    itens = {x["item"] for v in ("orbitador", "lander") for x in a[v]["composicao"]}
    assert set(d.NOMES_ESTAGIO.values()) <= itens
    nomes = {e["nome"] for x in d.orcamento()["veiculos"].values() for e in x["estagios"]}
    assert nomes <= set(d.NOMES_ESTAGIO.values())   # nenhum estágio fica com a chave interna


def test_propulsao_le_os_resultados_da_fase_3():
    p = d.propulsao()
    oe = yaml.safe_load((RAIZ / "results/etapa3.3/orbitador_eletrico.yaml").read_text(encoding="utf-8"))
    assert p["opcoes"][0]["total"].valor == oe["quimico"]["total_regra_iii_kg"]
    assert p["verificacao"]["verificado"] is False and p["verificacao"]["fora_da_tolerancia"] == ["u"]   # ADR 0012
    assert {x["manobra"] for x in p["perdas"]} == {"captura", "saida"}
    assert all(x["ida"].rotulo == "calculado, não verificado" for x in p["b"])


def test_subsistemas_le_o_resumo_da_fase_4():
    s = d.subsistemas()
    r = yaml.safe_load((RAIZ / "results/fase4/resumo.yaml").read_text(encoding="utf-8"))
    assert s["massas"]["lander_injetado"].valor == r["massas"]["lander_injetado_kg"]
    assert s["massas"]["plataforma"].rotulo == d.rotulo_premissa("P-017")
    assert s["massas"]["circuito"].rotulo == d.rotulo_premissa("P-077")
    base = yaml.safe_load((RAIZ / "config/lancadores.yaml").read_text(encoding="utf-8"))["base"]
    assert [x["lancador"] for x in s["lancadores"]] == [base["orbitador"], base["lander"], base["lander_reserva"]]
    assert len(s["superficie"]["linha_do_tempo"]) == len(r["superficie"]["linha_do_tempo"])
    rot = dict((nome, x.rotulo) for nome, x in s["itens"])
    assert rot["Demanda de dados do lander"] == d.rotulo_premissa("P-063")
    assert rot["Alvo de temperatura do MAV"] == d.rotulo_premissa("P-027")
    assert rot["MRO, máximo"] == "dado de fonte publicada [F137]"
