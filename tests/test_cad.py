"""Etapa 7.2: CAD paramétrico (tools/cad_parametros.py e cad/featurescript/modelo.fs)."""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import pytest

from orbital.config import ler

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))
import cad_parametros as cp  # noqa: E402

NOME = re.compile(r'"Name"\s*:\s*"([^"]*)"')


def test_modelo_sem_dimensoes():
    """Nenhuma dimensão digitada no FeatureScript: fora do cabeçalho (versão), só os índices 0, 1 e 2 e o expoente 3 da
    unidade de densidade (kilogram / meter ^ 3)."""
    linhas = cp.MODELO.read_text(encoding="utf-8").splitlines()[2:]
    codigo = "\n".join(re.sub(r"//.*$", "", x) for x in linhas)
    numeros = set(re.findall(r"(?<![\w.])\d+(?:\.\d+)?", codigo))
    assert numeros <= {"0", "1", "2", "3"}, numeros
    assert codigo.count("^ 3") == len(re.findall(r"(?<![\w.])3(?![\w.])", codigo))   # o 3 só aparece no expoente


def test_nomes_em_ascii():
    """O Onshape rejeita anotação "Name" fora do ASCII imprimível (método reaproveitado de projeto anterior)."""
    for f in sorted((RAIZ / "results/etapa7.2").glob("*.fs")) + [cp.MODELO]:
        texto = f.read_text(encoding="utf-8")
        assert all(32 <= ord(ch) <= 126 for m in NOME.finditer(texto) for ch in m.group(1)), f
        assert all(ord(ch) < 128 for ch in texto), f


def test_volumes_e_centros():
    cil = {"tipo": "cilindro", "p0": [0, 0, 0], "p1": [0, 0, 2], "r": 1}
    assert cp.volume(cil) == pytest.approx(2 * math.pi)
    cone = {"tipo": "tronco", "p0": [0, 0, 0], "p1": [0, 0, 3], "r0": 1, "r1": 0, "ri0": 0, "ri1": 0}
    assert cp.volume(cone) == pytest.approx(math.pi)
    assert cp.centro(cone)[2] == pytest.approx(0.75)   # centroide do cone: h/4 da base
    oca = {"tipo": "esfera_oca", "c": [0, 0, 0], "r": 1, "t": 0.1}
    assert cp.volume(oca) == pytest.approx(4 / 3 * math.pi * (1 - 0.9 ** 3))
    # casca de tronco: o deslocamento radial dá o volume área lateral × espessura
    d = cp.casca_tronco(0, 2.0, 1.0, 1.5, 0.01)
    alvo = math.pi * 3.5 * math.hypot(1.0, 0.5) * 0.01
    assert cp.vol_tronco(1.0, 2.0, 1.5) - cp.vol_tronco(1.0, 2.0 - d, 1.5 - d) == pytest.approx(alvo, rel=1e-6)


def test_arquivos_gerados_coerentes():
    r = ler("results/etapa7.2/parametros.yaml")
    for k, corpos in r["veiculos"].items():
        texto = (RAIZ / f"results/etapa7.2/{k}.fs").read_text(encoding="utf-8")
        assert texto == cp.featurescript(k, corpos, r["materiais"])
        assert texto.count('"tipo" :') == len(corpos)
        assert r["resumo"][k]["massa_kg"] == pytest.approx(sum(c["massa_kg"] for c in corpos))
    # peças equivalentes: massa = a do orçamento usada (P-094)
    orb = {c["nome"]: c for c in r["veiculos"]["orbitador"]}
    assert orb["CCRS"]["massa_kg"] == pytest.approx(620.0, rel=1e-10)   # densidade arredondada a 13 algarismos
    # propelente do orbitador = o do orçamento
    prop = sum(c["massa_kg"] for c in r["veiculos"]["orbitador"] if c["nome"].startswith("Propelente"))
    arq = ler("results/etapa2.5/arquitetura.yaml")["orbitador"]["composicao"]
    # raio arredondado a 13 algarismos (como no FeatureScript): o volume triplica o erro relativo
    assert prop == pytest.approx(sum(x.get("propelente_kg", 0) for x in arq), rel=2e-5)


def test_conferencias():
    r = ler("results/etapa7.2/parametros.yaml")["conferencias"]
    for linhas in r["mav_deitado"]["por_forma"].values():
        comp = [x["comprimento_max_m"] for x in linhas]
        assert all(b <= a for a, b in zip(comp, comp[1:]))   # mais para trás, a casca estreita
    assert set(r["lander_vulcan"]["por_forma"]) == {"msl_m2020", "srl_a", "srl_c"}


def test_casca_do_escudo_tem_o_volume_da_espessura():
    """A casca de PICA tem volume = área lateral × espessura [F215] (o deslocamento não fica limitado pelo nariz)."""
    r = ler("results/etapa7.2/parametros.yaml")
    t = ler("config/cad.yaml")["capsulas"]["espessura_pica_m"]["valor"]
    c = next(x for x in r["veiculos"]["lander"] if x["nome"] == "Escudo térmico (PICA)")
    h = abs(c["p1"][2] - c["p0"][2])
    alvo = math.pi * (c["r0"] + c["r1"]) * math.hypot(h, c["r1"] - c["r0"]) * t
    assert cp.volume(c) == pytest.approx(alvo, rel=1e-3)


def test_cone_interno_estendido_na_mesma_reta():
    """O cone interno estendido de cada tronco oco passa pelos raios internos ri0 e ri1 nas faces do tronco."""
    r = ler("results/etapa7.2/parametros.yaml")
    for corpos in r["veiculos"].values():
        for c in corpos:
            if c["tipo"] != "tronco_oco":
                continue
            x = cp.extensao_interna(c)
            pe0, pe1 = x["pe0"][2], x["pe1"][2]
            raio = lambda z: x["rie0"] + (x["rie1"] - x["rie0"]) * (z - pe0) / (pe1 - pe0)  # noqa: E731
            assert raio(c["p0"][2]) == pytest.approx(c["ri0"], abs=1e-9)
            assert raio(c["p1"][2]) == pytest.approx(c["ri1"], abs=1e-9)
            assert min(x["rie0"], x["rie1"]) > 0


def _itens_com_premissa(no, caminho=()):
    """(caminho, chave, valor, premissa) dos itens de config com valor numérico (ou lista) e premissa."""
    if isinstance(no, dict):
        if "premissa" in no and "valor" in no:
            yield caminho, no["valor"], no["premissa"]
        for k, x in no.items():
            if isinstance(x, (dict, list)):
                yield from _itens_com_premissa(x, caminho + (k,))


def test_config_cad_coincide_com_as_premissas():
    """Cada valor de config/cad.yaml que cita uma premissa aparece nela: valor escalar igual, ou chave de mesmo nome
    (a do item, ou "pai_item") com o mesmo valor. Cobre P-078 a P-095, inclusive o ees_raio_ponta_m da P-094, e P-097 a P-103."""
    ps = {p["id"]: p["valor"] for p in ler("config/premissas.yaml")["premissas"]}
    itens = list(_itens_com_premissa(ler("config/cad.yaml")))
    assert any(c[-1] == "ees_raio_ponta_m" for c, _, _ in itens)
    assert {"P-097", "P-098", "P-099", "P-100", "P-101", "P-102", "P-103"} <= {pid for _, _, pid in itens}
    for caminho, valor, pid in itens:
        pv = ps[pid]
        if isinstance(pv, dict):
            chaves = [caminho[-1], "_".join(caminho[-2:])]
            k = next((c for c in chaves if c in pv), None)
            assert k is not None, (pid, caminho)
            assert pv[k] == valor, (pid, caminho, pv[k], valor)
        else:
            assert pv == valor, (pid, caminho, pv, valor)


def test_mav_arranjo_coerente():
    """Varredura do MAV (tools/mav_arranjo.py): o diâmetro de 0,57 m reproduz o comprimento da Etapa 7.1 e a folga do MAV
    deitado é o raio interno no topo menos o meio comprimento."""
    r = ler("results/etapa7.2/mav_arranjo.yaml")
    env = ler("results/etapa7.1/envelope.yaml")["mav"]["restricao_2019"]
    c57 = next(c for c in r["casos"] if c["diametro_m"] == pytest.approx(0.57))
    assert c57["comprimento_m"] == pytest.approx(env["comprimento_m"])
    cad = ler("config/cad.yaml")
    xs, rs = cad["capsulas"]["srl_a"]["x_m"], cad["capsulas"]["srl_a"]["r_m"]
    e = c57["formas"]["srl_a"][0]
    import numpy as np
    r_in = float(np.interp(e["estacao_base_m"] + 0.57, xs, rs)) - r["folga_interna_m"]
    assert e["deitado_folga_m"] == pytest.approx(r_in - c57["comprimento_m"] / 2)
    assert all(c["comprimento_m"] <= c57["comprimento_m"] + 1e-12 for c in r["casos"])


def test_inercias_analiticas():
    """Inércia no CG dos primitivos contra as fórmulas fechadas (cilindro, cone, caixa)."""
    m_cil = 1000.0 * math.pi * 1.0 * 2.0
    I = cp.inercia({"tipo": "cilindro", "p0": [0, 0, 0], "p1": [0, 0, 2], "r": 1.0}, 1000.0)
    assert I[2][2] == pytest.approx(m_cil / 2, rel=1e-6)
    assert I[0][0] == pytest.approx(m_cil * (3 + 4) / 12, rel=1e-6)
    cone = {"tipo": "tronco", "p0": [0, 0, 0], "p1": [0, 0, 3], "r0": 1.0, "r1": 0.0, "ri0": 0, "ri1": 0}
    m_cone = 1000.0 * math.pi * 3 / 3
    I = cp.inercia(cone, 1000.0)
    assert I[2][2] == pytest.approx(3 / 10 * m_cone, rel=1e-5)
    assert I[0][0] == pytest.approx(m_cone * (3 / 20 + 3 * 9 / 80), rel=1e-5)
    I = cp.inercia({"tipo": "caixa", "c1": [0, 0, 0], "c2": [1, 2, 3]}, 1.0)
    assert I[0][0] == pytest.approx(6 * (4 + 9) / 12)
    # cilindro ao longo de y: o eixo de simetria vira yy
    I = cp.inercia({"tipo": "cilindro", "p0": [0, 0, 0], "p1": [0, 2, 0], "r": 1.0}, 1000.0)
    assert I[1][1] == pytest.approx(m_cil / 2, rel=1e-6)


def test_conferencia_onshape():
    """Medido no Onshape (tests/data/onshape) contra o previsto pelo script sobre o arquivo compilado."""
    import conferencia_onshape as co
    r = ler("results/etapa7.2/conferencia_onshape.yaml")
    med = ler("tests/data/onshape/medicoes.yaml")
    for k in ("orbitador", "lander", "mav"):
        x = r["veiculos"][k]
        assert x["situacao"] == "conferido"
        p = co.previsto_do_arquivo(med[k]["arquivo"])
        li = {y["grandeza"]: y for y in x["linhas"]}
        assert li["massa"]["previsto"] == pytest.approx(p["massa_kg"], rel=1e-12)
        assert li["massa"]["medido"] == float(med[k]["massa"])
        for y in x["linhas"]:
            assert y["dentro"] == (abs(y["medido"] - y["previsto"]) <= y["meia_resolucao"])
    # tolerância: meia unidade da última casa decimal mostrada
    assert co.casas("348.127") == 3 and co.casas("6506.2448") == 4
    mav = {y["grandeza"]: y for y in r["veiculos"]["mav"]["linhas"]}
    assert mav["massa"]["meia_resolucao"] == pytest.approx(5e-4)
    lan = {y["grandeza"]: y for y in r["veiculos"]["lander"]["linhas"]}
    assert lan["massa"]["meia_resolucao"] == pytest.approx(5e-5) and lan["CG x"]["meia_resolucao"] == pytest.approx(5e-5)
    # o arquivo atual do lander (geometria com 13 algarismos) reproduz o modelo atual
    m = ler("results/etapa7.2/parametros.yaml")["resumo"]["lander"]
    assert co.previsto_do_arquivo("results/etapa7.2/lander.fs")["massa_kg"] == pytest.approx(m["massa_kg"], rel=1e-9)


def test_cg_lateral_por_conjunto():
    """Os conjuntos somam o CG lateral e os produtos de inércia do lander, nas duas configurações."""
    r = ler("results/etapa7.2/cg_lateral.yaml")
    for c in r["configuracoes"].values():
        g = c["por_conjunto"]
        assert sum(x["mx_kg_m"] for x in g) / c["massa_kg"] == pytest.approx(c["cg_m"][0], abs=1e-12)
        assert sum(x["my_kg_m"] for x in g) / c["massa_kg"] == pytest.approx(c["cg_m"][1], abs=1e-12)
        assert sum(x["Ixz"] for x in g) == pytest.approx(c["produtos_kg_m2"]["Ixz"], abs=1e-9)
    lan = r["configuracoes"]["lançamento"]
    assert lan["cg_m"] == pytest.approx(ler("results/etapa7.2/parametros.yaml")["resumo"]["lander"]["cg_m"], abs=1e-12)


def test_previsto_e_a_geometria_do_featurescript():
    """Os corpos do script já estão arredondados como no FeatureScript: o previsto é o que o Onshape constrói."""
    r = ler("results/etapa7.2/parametros.yaml")
    for corpos in r["veiculos"].values():
        for c in corpos:
            for k in ("p0", "p1", "c", "c1", "c2", "r", "t", "r0", "r1", "ri0", "ri1", "densidade"):
                if k in c:
                    assert c[k] == cp.r13(c[k])


def test_cg_lateral_achado_e_produtos_no_eixo():
    """Razão lander/MSL e azimute calculados pela ferramenta; peças simétricas ou no eixo dão produtos nulos no eixo."""
    import math as m_
    r = ler("results/etapa7.2/cg_lateral.yaml")
    ce = r["comparacao_entrada"]
    ent = r["configuracoes"]["entrada (sem o estágio de cruzeiro)"]
    assert ce["razao_lander_msl"] == pytest.approx(ent["radial_sobre_d"] / abs(r["msl"]["zcg_sobre_d"]))
    assert ce["azimute_graus"] == pytest.approx(m_.degrees(m_.atan2(ent["cg_m"][1], ent["cg_m"][0])))
    for c in r["configuracoes"].values():
        g = {x["conjunto"]: x for x in c["por_conjunto"]}
        for nome in ("Núcleo do lander", "Cápsula (escudo e casca)", "Descida (3 tanques a 120°)"):
            for k in ("Ixy_origem", "Ixz_origem", "Iyz_origem"):
                assert abs(g[nome][k]) < 1e-6, (nome, k)
        # Ixz e Iyz no eixo somam o total (o ponto de referência fica na altura do CG)
        assert sum(x["Ixz_origem"] for x in c["por_conjunto"]) == pytest.approx(c["produtos_kg_m2"]["Ixz"], abs=1e-6)


def test_portao_7_2():
    """Página do portão: o piso soma tanques e P-086; a situação segue a regra; os achados de bocais e variantes."""
    import portao_7_2 as pt
    r = ler("results/etapa7.2/portao_decisao.yaml")
    ma = ler("results/etapa7.2/mav_arranjo.yaml")
    pi = r["piso"]
    assert pi["tanques_m"] + pi["fora_dos_tanques_m"] == pytest.approx(pi["comprimento_m"])
    assert pi["comprimento_m"] == pytest.approx(ma["casos"][-1]["comprimento_m"])
    for li in r["linhas"]:
        assert li["situacao"] == pt.classifica(li["max_fora_dos_tanques_m"], r["p086_m"])
        # coerência: cabe hoje se e só se a folga é positiva
        assert (li["situacao"] == "cabe") == (li["folga_m"] >= 0)
    # R-4D-11 de bocal 164:1: (19,32 + 2,5) pol; 4 saídas não cabem em Ø 0,57 m (mínimo d(1 + √2))
    assert r["r4d"]["variantes"]["164:1"]["comprimento_m"] == pytest.approx(21.82 * 0.0254)
    assert r["bocais"]["minimo_por_n_m"][4] == pytest.approx(11.0 * 0.0254 * (1 + math.sqrt(2)))
    assert r["bocais"]["cabe_por_n"][4] is False and r["bocais"]["cabe_por_n"][2] is True
    # a peça do modelo compilado é um cilindro maciço que cabe no diâmetro, não os bocais
    m1 = next(x for x in r["modelo_motores_compilado"] if "estagio 1" in x["nome"])
    assert m1["tipo"] == "cilindro" and m1["diametro_m"] < r["bocais"]["diametro_mav_m"]
    # mistura de variantes: o catálogo usa a massa do 300:1
    assert round(r["r4d"]["catalogo_massa_kg"], 2) == r["r4d"]["variantes"]["300:1"]["massa_kg"]
    assert sum(r["r4d"]["n_motores"].values()) == 19   # C4 + R3 + M2 + N2


def test_consumo_cruzeiro():
    """Com propelente de cruzeiro cheio, o CG é o do lançamento; o CG x cai com o consumo (MON-3 mais pesado em +x)."""
    r = ler("results/etapa7.2/cg_lateral.yaml")
    li = r["consumo_cruzeiro"]["linhas"]
    assert li[0]["cg_m"] == pytest.approx(r["configuracoes"]["lançamento"]["cg_m"], abs=1e-12)
    xs = [x["cg_m"][0] for x in li]
    assert all(b < a for a, b in zip(xs, xs[1:]))


def test_bocais_estagio1():
    """Alternativas dos bocais: círculo mínimo, empuxo/peso, Δv e folga, conferidos por fora da ferramenta."""
    r = ler("results/etapa7.2/bocais_alternativas.yaml")
    a = {x["id"]: x for x in r["alternativas"]}
    assert a["A"]["circulo_minimo_m"] == pytest.approx(11.0 * 0.0254 * (1 + math.sqrt(2)))
    assert a["E"]["circulo_minimo_m"] == pytest.approx(2 * 15.34 * 0.0254) and a["E"]["menor_d_varredura_m"] is None
    assert a["F"]["cabe_em_d_mav_com_parede"] and a["F"]["comprimento_motor_m"] == pytest.approx(28.0 * 0.0254)
    # empuxo/peso: a C não vence o peso, e A, E e F batem com a Etapa 3.1
    assert a["C"]["empuxo_peso_marte"] < 1 < a["D"]["empuxo_peso_marte"]
    q = {x["combinacao"]: x["empuxo_peso_marte"] for x in ler("results/etapa3.1/queima_finita.yaml")["mav"] if x["estagio"] == "mav_1"}
    for k, c in (("A", "M2"), ("E", "M1"), ("F", "M3")):
        assert a[k]["empuxo_peso_marte"] == pytest.approx(q[c], rel=1e-12)
    # o 44:1 não tem Isp na fonte: o Δv não é calculado
    assert a["B"]["isp_s"] is None and a["B"]["variacao_dv_estagio_m_s"] is None
    # círculo de 3 saídas, varredura com parede e Δv proporcional ao Isp
    assert a["D"]["circulo_minimo_m"] == pytest.approx(11.0 * 0.0254 * (1 + 2 / math.sqrt(3)))
    assert a["A"]["menor_d_varredura_m"] == 0.69 and a["A"]["menor_d_varredura_com_parede_m"] == 0.72
    assert a["F"]["variacao_dv_estagio_m_s"] == pytest.approx(r["dv_estagio_1_m_s"] * (a["F"]["isp_s"] / r["isp_dimensionamento_s"] - 1))
    # folga: a do portão menos a metade do excesso sobre a P-086, em cada aeroshell e sem trocar um pelo outro
    por = ler("results/etapa7.2/portao_decisao.yaml")["linhas"]
    base = lambda forma: next(x["folga_m"] for x in por if x["forma"] == forma and x["diametro_m"] == 0.57 and x["orientacao"] == "deitado" and x["estacao"] == "ombro")  # noqa: E731
    f = a["F"]["folgas"][0]
    assert a["F"]["excesso_sobre_p086_m"] == pytest.approx(28.0 * 0.0254 - r["p086_motores_estagio_1_m"])
    assert f["folga_4_5_m"] == pytest.approx(base("msl_m2020") - a["F"]["excesso_sobre_p086_m"] / 2)
    assert f["folga_4_65_m"] == pytest.approx(base("srl_a") - a["F"]["excesso_sobre_p086_m"] / 2)
    assert a["A"]["excesso_sobre_p086_m"] == 0
    # comprimento com o excesso, parede nos dois lugares e rótulos dos aeroshells
    compr = next(c["comprimento_m"] for c in ler("results/etapa7.2/mav_arranjo.yaml")["casos"] if c["diametro_m"] == 0.57)
    assert f["comprimento_m"] == pytest.approx(compr + a["F"]["excesso_sobre_p086_m"])
    assert a["C"]["cabe_em_d_mav"] and not a["C"]["cabe_em_d_mav_com_parede"]
    rot = ler("results/etapa7.2/portao_decisao.yaml")["aeroshell"]
    assert r["aeroshell"] == {k: rot[k]["rotulo"] for k in ("msl_m2020", "srl_a")}
    # decisões do Fabio na página
    md = (RAIZ / "results/etapa7.2/bocais_alternativas.md").read_text(encoding="utf-8")
    assert "**C: DESCARTADA.**" in md and "**F: REFERÊNCIA APENAS.**" in md and "Not in Production" in md


def test_encaixe_coifas():
    """Etapa 7.2b: os veículos têm os mesmos corpos da 7.2, e as folgas no vértice do ombro saem do perfil e do envelope."""
    from conferencia_onshape import _bloco
    r = ler("results/etapa7.2b/folgas.yaml")
    par = ler("results/etapa7.2/parametros.yaml")
    for novo, antigo, chave in (("lander_4_65", "lander", "lander"), ("orbitador", "orbitador", "orbitador")):
        a = (RAIZ / f"results/etapa7.2b/{novo}.fs").read_text(encoding="utf-8")
        b = (RAIZ / f"results/etapa7.2/{antigo}.fs").read_text(encoding="utf-8")
        assert _bloco(a, "CORPOS") == _bloco(b, "CORPOS") and _bloco(a, "MATERIAIS") == _bloco(b, "MATERIAIS")
        assert r["veiculos"][novo]["massa_kg"] == pytest.approx(par["resumo"][chave]["massa_kg"], rel=1e-12)
        assert r["veiculos"][novo]["cg_m"] == pytest.approx(par["resumo"][chave]["cg_m"], rel=1e-12, abs=1e-12)
    for arq in ("envelope_vulcan", "envelope_falcon_heavy", "lander_4_65", "lander_4_5", "orbitador"):
        t = (RAIZ / f"results/etapa7.2b/{arq}.fs").read_text(encoding="utf-8")
        assert t.startswith('FeatureScript 3112;\nimport(path : "onshape/std/geometry.fs", version : "3112.0");')
        assert t.count("opMateConnector(context") == 1
    # o modelo do envelope não tem dimensão
    modelo = (RAIZ / "cad/featurescript/envelope.fs").read_text(encoding="utf-8")
    assert not re.search(r"\d\.\d", re.sub(r"//.*", "", modelo))
    # a casca: a face interna é o envelope, e o envelope do Vulcan traz as duas leituras
    seg = _bloco((RAIZ / "results/etapa7.2b/envelope_vulcan.fs").read_text(encoding="utf-8"), "SEGMENTOS")
    assert len(seg) == 2 and seg[0]["interno"][1][2:] == [2.4385, 2.324] and seg[1]["interno"][1][2:] == [2.324, 2.324]
    # folga no vértice do ombro, à mão, com o perfil de [F41] e o envelope de [F80]
    cad = ler("config/cad.yaml")
    h_cz = par["conferencias"]["lander_vulcan"]["altura_estagio_cruzeiro_m"]
    li = {(x["veiculo"], x["leitura"][:8]): x for x in r["configuracoes"]}
    for veic, forma in (("lander_4_5", "msl_m2020"), ("lander_4_65", "srl_a")):
        p = cad["capsulas"][forma]
        r_o = max(float(x) for x in p["r_m"])
        z_o = h_cz + float(p["x_m"][-1]) - float(p["x_m"][[float(x) for x in p["r_m"]].index(r_o)])
        linear = 2.4385 + (2.324 - 2.4385) * z_o / 6.604
        assert li[(veic, "Contorno")]["radial"]["folga_radial_m"] == pytest.approx(linear - r_o, abs=1e-9)
        assert li[(veic, "Diametro")]["radial"]["folga_radial_m"] == pytest.approx(2.324 - r_o, abs=1e-9)
        # a conta da 7.2, repetida, dá o valor publicado: a diferença é só a amostragem
        for x in (li[(veic, "Contorno")], li[(veic, "Diametro")]):
            assert x["reproducao_grade_400_m"] == pytest.approx(x["referencia_7_2_m"], abs=1e-12)
            assert x["diferenca_m"] < 0
    # errata: os valores vigentes de parametros.yaml são os da geometria
    fv = par["conferencias"]["lander_vulcan"]["por_forma"]
    assert li[("lander_4_65", "Contorno")]["radial"]["folga_radial_m"] == pytest.approx(fv["srl_a"]["folga_radial_vertice_m"], abs=1e-9)
    assert li[("lander_4_65", "Diametro")]["radial"]["folga_radial_m"] == pytest.approx(fv["srl_a"]["folga_sem_afunilamento_vertice_m"], abs=1e-9)
    assert li[("lander_4_5", "Contorno")]["radial"]["folga_radial_m"] == pytest.approx(fv["msl_m2020"]["folga_radial_vertice_m"], abs=1e-9)
    assert li[("lander_4_5", "Diametro")]["radial"]["folga_radial_m"] == pytest.approx(fv["msl_m2020"]["folga_sem_afunilamento_vertice_m"], abs=1e-9)
    assert "Errata (2026-11-04" in (RAIZ / "results/etapa7.2/conferencias.md").read_text(encoding="utf-8")
    assert "Errata (2026-11-04" in (RAIZ / "results/etapa7.2/portao_decisao.md").read_text(encoding="utf-8")
    # o 4,5 m: arquivo igual ao modelo montado, e todos os corpos que cruzam o envelope listados
    import encaixe_coifas as ec
    t45 = (RAIZ / "results/etapa7.2b/lander_4_5.fs").read_text(encoding="utf-8")
    assert [c["nome"] for c in _bloco(t45, "CORPOS")] == [cp.ascii_(c["nome"]) for c in cp.monta_lander(cad, ler("results/etapa7.1/envelope.yaml"), ler("results/etapa2.5/arquitetura.yaml"), ler("config/motores.yaml"), "msl_m2020").corpos]
    neg = {x["corpo"] for x in li[("lander_4_65", "Diametro")]["radial"]["corpos_com_folga_negativa"]}
    assert neg == {"Escudo térmico (PICA)", "Casca traseira 1 (SLA-561V)"}
    assert not li[("lander_4_65", "Contorno")]["radial"]["corpos_com_folga_negativa"]
    # corpo fora do eixo, à mão: esfera em (x, 0, z), com o envelope reto de raio 2
    perfil = ([0.0, 10.0], [2.0, 2.0])
    rad, ax = ec.folgas([{"nome": "e", "tipo": "esfera", "c": [1.0, 0.0, 3.0], "r": 0.5}], perfil)
    assert rad["folga_radial_m"] == pytest.approx(0.5, abs=1e-4) and ax["folga_axial_m"] == pytest.approx(6.5, abs=1e-4)
    # cilindro deitado ao longo de y, centrado: a ponta define a folga radial
    rad, _ = ec.folgas([{"nome": "m", "tipo": "cilindro", "p0": [0.0, -1.0, 3.0], "p1": [0.0, 1.0, 3.0], "r": 0.2}], perfil)
    assert rad["folga_radial_m"] == pytest.approx(2 - math.hypot(1.0, 0.2), abs=1e-3)
    # o MAV deitado do 4,5 m não atravessa a cápsula; os helicópteros e os tanques de descida, sim
    pc = {x["corpo"]: x["folga_m"] for x in r["pecas_contra_a_capsula"]["lander_4_5"]}
    assert next(v_ for k, v_ in pc.items() if k.startswith("MAV")) > 0 and pc["Helicóptero 1"] < 0 and pc["Tanque descida 1"] < 0
    # desempate: corpos iguais a menos de ruído mantêm o primeiro da lista, nos dois sentidos do ruído
    for ruido in (1e-13, -1e-13):
        par_ = [{"nome": "a", "tipo": "cilindro", "p0": [0.0, 0.0, 0.0], "p1": [0.0, 0.0, 1.0], "r": 1.0},
                {"nome": "b", "tipo": "cilindro", "p0": [0.0, 0.0, 0.0], "p1": [0.0, 0.0, 1.0 + ruido], "r": 1.0 + ruido}]
        rad, ax = ec.folgas(par_, perfil)
        assert rad["corpo"] == "a" and ax["corpo"] == "a"
    # o MAV empatado cita as peças empatadas, em ordem de nome, e a ordem da lista não depende de ruído
    mavs = [x["corpo"] for x in r["pecas_contra_a_capsula"]["lander_4_5"] if x["corpo"].startswith("MAV")]
    assert len(mavs) == 1 and "MAV carga" in mavs[0] and "MAV motores" in mavs[0] and mavs[0].index("MAV carga") < mavs[0].index("MAV motores")
    # texto gerado: rótulo, lista de interferências em A4 e aviso da face interna
    assert "VERIFICACAO geometrica" in t45
    rot = (RAIZ / "results/etapa7.2b/roteiro_onshape.md").read_text(encoding="utf-8")
    assert "| A4 | interferência com `Escudo termico (PICA)` e `Casca traseira 1 (SLA-561V)`, no ombro |" in rot and "face INTERNA" in rot
    # grade alinhada: peças exatamente simétricas sem diferença da grade; 2 e 3 são espelhos bit a bit
    td = [c for c in par["veiculos"]["lander"] if c["nome"].startswith("Tanque descida")]
    assert td[1]["c"][0] == td[2]["c"][0] and td[1]["c"][1] == -td[2]["c"][1] and td[1]["c"][2] == td[2]["c"][2]
    assert r["criterio_empate"]["simetricas"]["diferenca_m"] == pytest.approx(r["tanques_descida"]["diferenca_max_raio_m"], rel=1e-3)
    # topo da Casca traseira 1 e do Braço em z = 3,12 m: com a grade nos ângulos cardeais, é coincidência, não diferença
    assert any({"Braço de coleta (guardado)", "Casca traseira 1 (SLA-561V)"} <= set(x) for x in r["criterio_empate"]["coincidencias"])
    for arq_ in ("results/etapa7.2/conferencias.md", "results/etapa7.2/cg_lateral.md", "results/etapa7.2/conferencia_onshape.md"):
        assert "Errata (2026-11-06" in (RAIZ / arq_).read_text(encoding="utf-8")
    # nas casas do roteiro, nada mudou com a grade alinhada e os 13 algarismos
    assert all(x["igual_em_3_casas"] for x in r["comparacao_grade_e_precisao"])
    assert ec.EMPATE_M == 1e-9 and ec.CASAS_DE_ORDEM == 9
    # critério do Fabio para aprovar os dois parâmetros
    crit = r["criterio_empate"]
    assert crit["passa"] and crit["simetricas"]["diferenca_m"] <= 1e-12 and crit["distintas"]["diferenca_m"] >= 1e-6
    # coincidências não dependem do último bit: ruído que inverte a ordem de valores empatados dá a mesma saída
    chaves = [("a",), ("b",), ("c",), ("d",)]
    base = [(1.0, "a", chaves[0]), (1.0 + 1e-15, "b", chaves[1]), (1.0 + 2e-15, "c", chaves[2]), (2.0, "d", chaves[3])]
    invertido = [(1.0 + 2e-15, "a", chaves[0]), (1.0 + 1e-15, "b", chaves[1]), (1.0, "c", chaves[2]), (2.0, "d", chaves[3])]
    r0, r1 = ec.criterio_de_empate([("x", base + [(9.0, "e", ("e",)), (9.0, "f", ("e",))])]), ec.criterio_de_empate([("x", invertido + [(9.0, "e", ("e",)), (9.0, "f", ("e",))])])
    assert r0[3] == r1[3] == [["a", "b", "c"]]
    assert r0[1]["pecas"] == r1[1]["pecas"] and r0[2]["pecas"] == r1[2]["pecas"]
    # as premissas propostas não entraram
    ids = {p["id"] for p in ler("config/premissas.yaml")["premissas"]}
    assert not ({p["id"] for p in r["premissas_propostas"]} & ids)


def test_comprimento_mav():
    """Investigação do comprimento: a base reproduz o estudo; a folga segue o comprimento; o trade usa as funções do estudo."""
    r = ler("results/etapa7.2/comprimento_mav.yaml")
    arq = ler("results/etapa2.5/arquitetura.yaml")
    ma = ler("results/etapa7.2/mav_arranjo.yaml")
    b = next(o for o in r["orbitas"] if o["base"])
    # a órbita de base devolve os números vigentes, então o parâmetro `orbita` de veiculos não muda nada
    assert b["dv_mav_com_margem_m_s"] == pytest.approx(1e3 * arq["lander"]["mav"]["dv_com_margem_km_s"], rel=1e-12)
    assert b["glom_kg"] == pytest.approx(arq["lander"]["mav"]["estagios"][0]["massa_inicial_kg"], rel=1e-12)
    assert b["orbitador_injetado_kg"] == pytest.approx(arq["orbitador"]["injetado_kg"], rel=1e-12)
    assert b["lander_injetado_kg"] == pytest.approx(arq["lander"]["injetado_kg"], rel=1e-12)
    caso = next(c for c in ma["casos"] if c["diametro_m"] == r["diametro_m"])
    assert b["comprimento_m"] == pytest.approx(caso["comprimento_m"], rel=1e-12) and r["comprimento_base_m"] == pytest.approx(caso["comprimento_m"], rel=1e-12)
    od = r["origem_dv"]
    assert od["dv_100x100_m_s"] + od["transferencia_m_s"] + od["deficit_rotacao_m_s"] == pytest.approx(od["sem_margem_m_s"])
    assert od["com_margem_m_s"] == pytest.approx(b["dv_mav_com_margem_m_s"], rel=1e-12)
    # folga: a de mav_arranjo menos a metade da variação, nos dois aeroshells; em pé, disponível menos comprimento
    fo = {k: next(e for e in caso["formas"][k] if e["estacao"] == "ombro") for k in ("msl_m2020", "srl_a")}
    al = {x["alavanca"]: x for x in r["alavancas"]}
    a0 = r["alavancas"][0]
    assert a0["deitado_4_5_m"] == pytest.approx(fo["msl_m2020"]["deitado_folga_m"]) and a0["deitado_4_65_m"] == pytest.approx(fo["srl_a"]["deitado_folga_m"])
    assert a0["em_pe_4_65_m"] == pytest.approx(fo["srl_a"]["em_pe_folga_m"])
    ex = next(x for k, x in al.items() if k.startswith("Cada 0,1"))
    assert ex["deitado_4_5_m"] == pytest.approx(a0["deitado_4_5_m"] + 0.05) and ex["em_pe_4_65_m"] == pytest.approx(a0["em_pe_4_65_m"] + 0.10)
    # motor real 164:1 nos dois estágios: 2 × 0,55423 m contra 0,60 + 0,45 m da P-086
    real = next(x for k, x in al.items() if k.startswith("P-086 pelo motor real"))
    assert real["delta_comprimento_m"] == pytest.approx(2 * 21.82 * 0.0254 - 1.05)
    # trade: órbita mais baixa encurta o MAV e custa Δv ao orbitador; margem zero de fato perto de zero, e 380 km não fecha
    orb = sorted(r["orbitas"], key=lambda o: -o["apoapse_km"])
    assert all(a["comprimento_m"] > c["comprimento_m"] for a, c in zip(orb, orb[1:]))
    assert all(a["extra_orbitador_regra_iii_m_s"] < c["extra_orbitador_regra_iii_m_s"] for a, c in zip(orb, orb[1:]))
    zero = next(o for o in orb if o["rotulo"].startswith("margem zero"))
    assert abs(zero["margem_falcon_heavy"]) < 1e-3
    assert next(o for o in orb if o["apoapse_km"] == 380)["orbitador_injetado_kg"] is None
    # Δv do orbitador: descer + o menor entre partir direto e voltar a 1 sol; empuxo/peso de 2 motores é metade do de 4
    for o in orb:
        assert o["extra_orbitador_regra_iii_m_s"] == pytest.approx(o["descer_de_1_sol_m_s"] + min(o["partir_direto_extra_m_s"], o["voltar_a_1_sol_extra_m_s"]), rel=1e-9)
        assert o["empuxo_peso_2_motores"] == pytest.approx(o["empuxo_peso_4_motores"] / 2)
    # massa perto da divergência não é gravada
    assert next(o for o in orb if o["diverge"])["orbitador_injetado_kg"] is None
    # limite do Falcon Heavy: margem positiva ali, negativa um pouco abaixo
    import comprimento_mav as cmv  # noqa: F401
    from orbital import lancamento as lc
    from orbital import veiculos as ve
    from orbital.config import parametros, v as v_
    R = v_(ler("config/parametros_orbitais.yaml")["raio_marte_km"])
    ms = ler("results/etapa1.3/missoes.yaml")
    cand = {c["id"]: c for c in ms["candidatas"]}
    janelas = [cand[w["missao"]] for w in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()]
    lcfg = ler("config/lancadores.yaml")
    mg = lambda ha: lc.pior_margem_a("Falcon Heavy (descartável)", ve.veiculos(orbita=(R + zero["periapse_km"], R + ha))[0]["orbitador_regra_iii"]["injetada_kg"], janelas, lcfg)[0]  # noqa: E731
    assert mg(zero["apoapse_km"]) >= 0 > mg(zero["apoapse_km"] - 1)
    # figura: frações somam 1, e a escala é o limite de [F35]
    fm = r["figura_msr"]
    assert sum(x["fracao"] for x in fm["trechos"]) == pytest.approx(1.0)
    assert sum(x["comprimento_m"] for x in fm["trechos"]) == pytest.approx(fm["limite_m"])
    # 44:1 com o motor nos dois estágios: 2 × (9,97 + 2,5) pol no lugar de 0,60 + 0,45 m da P-086
    v44 = next(x for k, x in al.items() if k.startswith("R-4D-11 44:1"))
    assert v44["delta_comprimento_m"] == pytest.approx(2 * 12.47 * 0.0254 - 1.05)
    # comprimento máximo: base + 2 × folga deitado
    assert r["comprimento_maximo"]["srl_a"]["deitado_comprimento_max_m"] == pytest.approx(r["comprimento_base_m"] + 2 * a0["deitado_4_65_m"])
    # tanques aninhados: um tampo a menos por estágio, com o volume somado
    assert r["alavancas"][0]["comprimento_m"] > next(x for k, x in al.items() if k.startswith("Tanques aninhados"))["comprimento_m"]
    # a opinião é a última seção
    md = (RAIZ / "results/etapa7.2/comprimento_mav.md").read_text(encoding="utf-8")
    assert md.rindex("## ") == md.index("## Opinião do agente")
    assert "NÃO VALIDADO" in md


def test_rotas_mav():
    """Rotas do portão: a base reproduz o estudo; rota A e rota B conferidas por fora da ferramenta."""
    r = ler("results/etapa7.2/rotas_mav.yaml")
    arq = ler("results/etapa2.5/arquitetura.yaml")
    b = r["base"]
    assert b["glom_kg"] == pytest.approx(arq["lander"]["mav"]["estagios"][0]["massa_inicial_kg"], rel=1e-12)
    assert b["orbitador_injetado_kg"] == pytest.approx(arq["orbitador"]["injetado_kg"], rel=1e-12)
    assert b["circulo_saidas_m"] == pytest.approx(11.0 * 0.0254 * (1 + math.sqrt(2)))
    # rota A: 4 saídas de 44:1 em Ø 0,57 m com parede de 0,01 m
    a = r["rota_a"][0]["com_aninhados"]
    assert a["circulo_saidas_m"] == pytest.approx(6.01 * 0.0254 * (1 + math.sqrt(2)))
    assert a["folga_radial_bocais_m"] == pytest.approx((0.57 - 0.02 - a["circulo_saidas_m"]) / 2)
    # folga = (disponível − comprimento) / 2, e o 4,5 m com Ø 0,57 m é o limite da varredura
    assert a["folga_deitado_m"] == pytest.approx((a["disponivel_m"] - a["comprimento_m"]) / 2)
    # aninhar encurta, e Isp maior encurta e reduz a massa
    for x in r["rota_a"]:
        assert x["com_aninhados"]["comprimento_m"] < x["so_44"]["comprimento_m"]
    glom = [x["com_aninhados"]["glom_kg"] for x in r["rota_a"]]
    assert glom == sorted(glom, reverse=True)
    # rota A e rota B na mesma base: o motor real nos dois estágios (2 × 0,55423 m no lugar de 0,60 + 0,45 m)
    assert r["base_real"]["comprimento_m"] - b["comprimento_m"] == pytest.approx(2 * 21.82 * 0.0254 - 1.05)
    assert r["base_real"]["folga_deitado_m"] == pytest.approx(b["folga_deitado_m"] - (2 * 21.82 * 0.0254 - 1.05) / 2)
    # deck, área e empuxo/peso por fora da ferramenta
    from orbital import veiculos as ve
    from orbital.config import v as v_
    R = v_(ler("config/parametros_orbitais.yaml")["raio_marte_km"])
    ma = next(c for c in ler("results/etapa7.2/mav_arranjo.yaml")["casos"] if c["diametro_m"] == 0.57)
    dk = next(e for e in ma["formas"]["msl_m2020"] if "P-094" in e["estacao"])
    assert b["folga_deitado_com_deck_m"] == pytest.approx(dk["deitado_folga_m"])
    assert a["empuxo_peso"] == pytest.approx(4 * 110 * 4.448222 / (a["glom_kg"] * ler("results/etapa3.1/queima_finita.yaml")["g_marte_m_s2"]))
    pl = ler("results/etapa2.3/plataformas.yaml")["orbita_encontro"]
    lan = ve.lander(R + pl["periapse_alt_km"], R + pl["apoapse_regra_5pct_km"])
    assert b["massa_por_area_kg_m2"] == pytest.approx(lan["massa_entrada_kg"] / (math.pi * 4.5 ** 2 / 4))
    # rota B: 2 saídas de 164:1 com parede exigem Ø 0,60 m; a segunda órbita está no limite do alvo
    assert r["diametro_b_m"] == 0.60 and r["rota_b"][0]["altitude_km"] == 380
    bx = r["rota_b"][1]["mav"]
    assert 0 <= bx["folga_deitado_m"] < 2e-3   # a segunda órbita é a maior que cumpre o alvo, com o motor real
    assert bx["com_p086_atual"]["comprimento_m"] == pytest.approx(bx["comprimento_m"] - (2 * 21.82 * 0.0254 - 1.05))
    assert r["rota_a_referencia"]["so_44"]["glom_kg"] > 450   # Isp de 297 s, o do caso de referência
    assert bx["empuxo_peso"] == pytest.approx(2 * 110 * 4.448222 / (bx["glom_kg"] * ler("results/etapa3.1/queima_finita.yaml")["g_marte_m_s2"]))
    # o híbrido reproduz a Etapa 3.3 na altitude dela
    c33 = r["conferencia_etapa_3_3"]
    assert c33["aqui_kg"] == pytest.approx(c33["etapa_3_3_kg"], rel=1e-9) and c33["aqui_descida_dias"] == pytest.approx(c33["etapa_3_3_descida_dias"], rel=1e-9)
    # a opção C e o caso de referência aparecem na página
    assert "opção C, descartada" in (RAIZ / "results/etapa7.2/rotas_mav.md").read_text(encoding="utf-8")
    assert r["rota_a_referencia"]["com_aninhados"]["glom_kg"] > r["rota_a"][0]["com_aninhados"]["glom_kg"]
    # a opinião é a última seção
    md = (RAIZ / "results/etapa7.2/rotas_mav.md").read_text(encoding="utf-8")
    assert md.rindex("## ") == md.index("## Opinião do agente")
    # resolução da amostragem
    rs = ler("results/etapa7.2/comprimento_mav.yaml")["resolucao_amostragem"]
    assert rs["passos_bissecao"]["limite_fh_km"] == rs["passos_bissecao"]["limite_fh_dobrado_km"]
    assert rs["orbitas_amostra"]["comprimento_monotono"]
    assert rs["exemplo_p086_m"]["folga_por_metro_valor"] == pytest.approx(0.5)


def test_pendencia_recompilar_onshape():
    """A conferência registra que os arquivos atuais ainda não foram compilados, com as diferenças por veículo."""
    md = (RAIZ / "results/etapa7.2/conferencia_onshape.md").read_text(encoding="utf-8")
    assert "**Pendência (decisão do Fabio, 2026-11-06):**" in md and "bocais e do aeroshell" in md
    assert "Orbitador +6,8 g; Lander −0,015 kg; MAV −0,6 g" in md
    # resíduo da descida com 4 algarismos: o passo de impressão fica em 1 % do piso da P-039
    el = (RAIZ / "results/etapa3.3/orbitador_eletrico.md").read_text(encoding="utf-8")
    assert "(-2.105e-09)" in el and "(-3.350e-09)" in el


def test_rota_a_dimensiona():
    """Rota A provisória: limites com deck, espessuras por fora da ferramenta, comprimento real e folgas com adaptador."""
    r = ler("results/etapa7.2/rota_a.yaml")
    al, dm, im = r["alvo"], r["dimensionamento"], r["isp_minimo"]
    # alvo: 4 saídas de 44:1 cabem em Ø 0,57 m com parede; com deck, o limite é o de mav_arranjo
    assert al["diametro_m"] == 0.57 and al["circulo_44_m"] == pytest.approx(6.01 * 0.0254 * (1 + math.sqrt(2)))
    c = next(x for x in ler("results/etapa7.2/mav_arranjo.yaml")["casos"] if x["diametro_m"] == 0.57)
    dk = next(e for e in c["formas"]["msl_m2020"] if "P-094" in e["estacao"])
    assert al["limite_com_deck_m"] == pytest.approx(c["comprimento_m"] + 2 * dk["deitado_folga_m"])
    # espessuras à mão: σ = Ftu / 2; cilindro p R / σ; cúpula p R / (2 σ); flambagem clássica com o fator de redução
    sig = 134 * 6.894757 / 2
    p = dm["pressoes"]["entrada_piso_r4d11"]
    assert dm["tensao_admissivel_mpa"] == pytest.approx(sig)
    assert p["t_cilindro_m"] == pytest.approx(1.40 * 0.275 / sig) and p["t_cupula_m"] == pytest.approx(1.40 * 0.275 / (2 * sig))
    tf = 0.275 * math.sqrt(2 * 1.40 * math.sqrt(3 * (1 - 0.342 ** 2)) / (2 * 16400 * 6.894757 * 0.25))
    assert p["t_cupula_invertida_m"]["0.25"] == pytest.approx(tf)
    # real = limite + vão e paredes no estágio 1 + troca do tanque único pela geometria no estágio 2
    t_d, t_i = max(p["t_cupula_m"], dm["t_p093_m"]), max(p["t_cupula_invertida_m"][str(dm["fator_base"])], dm["t_p093_m"])
    assert list(dm["geometrias"]) == ["recesso_hemisferio", "recesso_livre", "antepara_assimetrica", "lente_mesmo_raio"]
    for x_ in dm["casos"]:
        hemi, livre, ant, len_ = (x_["por_geometria"][f] for f in dm["geometrias"])
        assert livre["real_m"] <= hemi["real_m"]   # relaxar o recesso não alonga
        for x in (hemi, livre, ant, len_):
            e1, e2 = x["por_estagio"]
            ge = e2["geometria"]
            assert e1["geometria"] is None
            assert e1["vao_e_paredes_m"] == pytest.approx(dm["vao_base_m"] + t_d + t_i)
            assert x["real_m"] == pytest.approx(x_["limite_otimista_m"] + e1["vao_e_paredes_m"] + ge["comprimento_m"] - e2["tanque_unico_m"])
            assert x["folga_deck_real_m"] == pytest.approx((al["limite_com_deck_m"] - x["real_m"]) / 2)
            assert e1["tanques_kg"] + e2["tanques_kg"] == pytest.approx(x["massa_tanques_kg"])
        # esboço: os volumes fecham, por fora da ferramenta; cabe no raio interno; com hemisfério, recesso de até um hemisfério
        def lente_(a_, b_, c_):
            return math.pi * (a_ + b_ - c_) ** 2 * (c_ ** 2 + 2 * c_ * (b_ + a_) - 3 * (b_ - a_) ** 2) / (12 * c_)
        for q in (hemi, livre):
            e2 = q["por_estagio"][1]
            es = e2["geometria"]
            ra_, r1, rr, c_ = es["raio_tanque_ao_redor_m"], es["raio_esfera_m"], es["raio_recesso_m"], es["distancia_centros_m"]
            assert 4 / 3 * math.pi * (ra_ ** 3 + r1 ** 3) - lente_(ra_, rr, c_) == pytest.approx(e2["volume_m3"], rel=1e-6)
            assert ra_ <= 0.275 + 1e-12
        es = hemi["por_estagio"][1]["geometria"]
        assert es["distancia_centros_m"] ** 2 + es["raio_recesso_m"] ** 2 >= es["raio_tanque_ao_redor_m"] ** 2 * (1 - 1e-9)
        # antepara: comprimento = tanque único + vão e paredes; volumes pela calota; raio de calota pela geometria da calota
        ea_ = ant["por_estagio"][1]
        ga = ea_["geometria"]
        assert ga["comprimento_m"] == pytest.approx(ea_["tanque_unico_m"] + ea_["vao_e_paredes_m"])
        rs = ea_["tanque_unico_m"] / 2
        h = ga["altura_calota_m"]
        assert ga["raio_calota_m"] == pytest.approx((rs ** 2 + h ** 2) / (2 * h))
        assert 2 * math.pi * h * (3 * rs ** 2 + h ** 2) / 6 == pytest.approx(ea_["volume_m3"] - 2 * ea_["volume_menor_m3"], rel=1e-6)
        # lente: a lente tem o menor volume, e o tanque único recua só o vão e as paredes
        el = len_["por_estagio"][1]
        gl = el["geometria"]
        assert lente_(gl["raio_m"], gl["raio_m"], gl["distancia_centros_m"]) == pytest.approx(el["volume_menor_m3"], rel=1e-6)
        assert gl["comprimento_m"] == pytest.approx(el["tanque_unico_m"] + el["vao_e_paredes_m"])
        assert gl["raio_borda_m"] ** 2 + (gl["distancia_centros_m"] / 2) ** 2 == pytest.approx(gl["raio_m"] ** 2)
    e2 = len_["por_estagio"][1]
    # motores [4, 1] com a massa do 164:1 de [F228]
    assert e2["motores_164_kg"] == pytest.approx(3.76) and x_["por_geometria"]["recesso_livre"]["por_estagio"][0]["motores_164_kg"] == pytest.approx(4 * 3.76)
    # Isp mínimo: o comprimento real pede mais Isp que o limite otimista, e a folga pedida bate no alvo
    assert all(li["por_geometria"][f] > im["limite_otimista_s"] for li in im["linhas"] for f in dm["geometrias"])
    assert im["comprimento_max_m"] == pytest.approx(al["limite_com_deck_m"] - 2 * im["alvo_folga_m"])
    # adaptador: a folga axial cai a altura; a leitura cilíndrica do Vulcan não muda a folga radial
    ad = r["adaptador"]["linhas"]
    assert ad[0]["por_altura"][0]["axial_m"] == pytest.approx(ad[0]["sem_adaptador"]["axial_m"] - 0.127, abs=1e-9)
    assert ad[1]["por_altura"][-1]["radial_m"] == pytest.approx(ad[1]["sem_adaptador"]["radial_m"], abs=1e-9)
    # premissas aprovadas pelo Fabio (2026-11-06 e 2026-11-07)
    ids = {q["id"] for q in ler("config/premissas.yaml")["premissas"]}
    assert {"P-096", "P-097", "P-098", "P-099", "P-100"} <= ids
    # margens: os 43 kg saem da capacidade, não entram na massa
    for x in r["margens"]:
        assert 0 > x["com_adaptador"] - x["sem_adaptador"] == pytest.approx(-43 / x["injetado_kg"])
    # o Isp calculado é o central, e a resposta de "fecha" sai das folgas
    central = next(c for c in dm["casos"] if c["origem"] == "calculado, central")
    assert central["isp_s"] == r["isp_calculado"]["s"]["central"]
    for f, x in r["fecha"]["por_geometria"].items():
        assert x["com_deck"] == (central["por_geometria"][f]["folga_deck_real_m"] >= 0.05)
        assert x["sem_deck"] == (central["por_geometria"][f]["folga_ombro_real_m"] >= 0.05)


def test_isp_44_bocal_ideal():
    """CF ideal contra limites analíticos, e o Isp calculado contra os dois pontos com fonte: abaixo do 164:1."""
    sys.path.insert(0, str(RAIZ / "tools"))
    import isp_44_bocal as ib
    for g in (1.15, 1.2277, 1.3):
        gam = ib.gama_termo(g)
        x_g = (2 / (g + 1)) ** (g / (g - 1))
        # garganta: ε = 1 em x crítico; CF(1) = (γ + 1) · x crítico, por fora da ferramenta
        assert ib.razao_area(x_g, g) == pytest.approx(1.0)
        assert ib.cf_vacuo(1.0 + 1e-9, g) == pytest.approx((g + 1) * x_g, rel=1e-3)
        # ε crescente se aproxima de CF máximo = Γ √(2γ/(γ−1)), por baixo
        cfm = gam * math.sqrt(2 * g / (g - 1))
        assert ib.cf_vacuo(300, g) < ib.cf_vacuo(1e7, g) < cfm
        # ponto intermediário, na forma em Mach e sem a razão de pressão da ferramenta: CF = ε x (1 + γ M²)
        for mach in (3.0, 4.5):
            base = 1 + (g - 1) / 2 * mach ** 2
            eps_m = (1 / mach) * ((2 / (g + 1)) * base) ** ((g + 1) / (2 * (g - 1)))
            assert ib.cf_vacuo(eps_m, g) == pytest.approx(eps_m * base ** (-g / (g - 1)) * (1 + g * mach ** 2))
        # a inversão de ε fecha
        assert ib.razao_area(ib.razao_pressao(44, g), g) == pytest.approx(44)
        # monotônico em ε
        assert ib.cf_vacuo(40, g) < ib.cf_vacuo(44, g) < ib.cf_vacuo(164, g) < ib.cf_vacuo(300, g)
    r = ler("results/etapa7.2/isp_44.yaml")
    c = r["central"]
    # os dois pontos com fonte são reproduzidos
    assert c["k_s"] * c["cf"]["164"] == pytest.approx(311) and c["k_s"] * c["cf"]["300"] == pytest.approx(315.5)
    assert ib.cf_vacuo(300, c["gama"]) / ib.cf_vacuo(164, c["gama"]) == pytest.approx(315.5 / 311)
    # abaixo do 164:1, e ordem coerente
    assert r["baixo"]["isp_s"]["44"] < c["isp_s"]["44"] < r["alto"]["isp_s"]["44"] < 311
    assert c["isp_s"]["40"] < c["isp_s"]["44"]
    assert r["empuxo_44_n"] == pytest.approx(r["empuxo_164_n"] * c["cf"]["44"] / c["cf"]["164"])


def test_config_subida_coincide_com_as_premissas():
    """config/subida.yaml cita P-104 a P-107 com os valores das premissas."""
    ps = {p["id"]: p["valor"] for p in ler("config/premissas.yaml")["premissas"]}
    itens = list(_itens_com_premissa(ler("config/subida.yaml")))
    assert {"P-104", "P-105", "P-106", "P-107"} <= {pid for _, _, pid in itens}
    for caminho, valor, pid in itens:
        pv = ps[pid]
        assert (pv[caminho[-1]] if isinstance(pv, dict) else pv) == valor, (pid, caminho)


def test_atmosfera_e_subida_vertical():
    """Atmosfera de [F245] contra as equações à mão; voo vertical sem arrasto contra a solução analítica de g constante."""
    from orbital import subida as sb
    from orbital.config import v
    atm = {k: v(x) for k, x in ler("config/subida.yaml")["atmosfera"].items()}
    assert sb.atmosfera(0.0, atm) == pytest.approx(0.699 / (0.1921 * (-31 + 273.1)))
    assert sb.atmosfera(20000.0, atm) == pytest.approx(0.699 * math.exp(-0.00009 * 20000) / (0.1921 * (-23.4 - 0.00222 * 20000 + 273.1)))
    assert sb.atmosfera(80001.0, atm) == 0.0
    # Marte sem rotação e quase plano (raio enorme, μ = g R²): voo vertical, sem arrasto, por 10 s
    g, R = 3.7, 1e9
    pl = sb.Planeta(g * R * R, R, 0.0)
    est = [sb.Estagio(100.0, 50.0, 2 * 100.0 * g, 300.0)]
    f = sb._deriv(pl, est[0], 0.0, atm, (1e9, 0.0, 0.0))
    from scipy.integrate import solve_ivp
    sol = solve_ivp(f, (0, 10), [R, 0.0, 0.0, 0.0, 100.0], rtol=1e-10, atol=1e-9)
    mdot = 2 * 100.0 * g / (300.0 * 9.80665)
    m = 100.0 - mdot * 10
    v_an = 300.0 * 9.80665 * math.log(100.0 / m) - g * 10
    assert sol.y[2, -1] == pytest.approx(v_an, rel=1e-6)


def test_subida_mav():
    """Subida: referência perto de [F37], casos convergidos com Δv coerente, e folgas pelos limites da rota A."""
    r = ler("results/etapa7.2/subida_mav.yaml")
    assert abs(r["referencia"]["diferenca_para_f37_m_s"]) < 0.05 * r["referencia"]["f37_m_s"]
    for c in r["casos"]:
        h = c["historico"]
        if not c["convergiu"]:
            # sem ponto fixo: o Δv pedido passa do usado em toda a varredura, até o MAV não decolar
            pf = c["ponto_fixo"]
            assert all(x["pedido_menos_usado_m_s"] > 0 for x in pf if x.get("pedido_menos_usado_m_s") is not None)
            continue
        assert abs(h[-1]["glom_kg"] - h[-2]["glom_kg"]) < 0.01
        # o Δv usado é o de [F37] mais a diferença simulada contra a referência
        assert c["dv_100x100_m_s"] == pytest.approx(r["referencia"]["f37_m_s"] + h[-2]["dv_simulado_m_s"] - r["referencia"]["dv_m_s"])
        for x in c["comprimentos"].values():
            lim = r["limites"]["sem_deck_m"] if c["variante"] == "44:1" else None
            if lim:
                assert x["folga_sem_deck_m"] == pytest.approx((lim - x["comprimento_m"]) / 2)
    # rota A: no mesmo Δv usado, o Isp menor (empuxo/peso menor) pede mais Δv; e o empuxo/peso cai com o Δv usado
    a = {c["isp_s"]: {x["dv_100x100_usado_m_s"]: x for x in c.get("ponto_fixo", [])} for c in r["casos"] if c["variante"] == "44:1"}
    isps = sorted(a)
    for dv in a[isps[0]]:
        if all(dv in a[i] and a[i][dv].get("dv_100x100_pedido_m_s") for i in isps):
            assert a[isps[0]][dv]["dv_100x100_pedido_m_s"] >= a[isps[-1]][dv]["dv_100x100_pedido_m_s"]
    for x in a.values():
        tws = [y["empuxo_peso"] for _, y in sorted(x.items())]
        assert all(t1 > t2 for t1, t2 in zip(tws, tws[1:]))


def test_mav_solido():
    """MAV sólido: escala do comprimento pela P-108, empuxo proporcional ao propelente e folgas pelos limites."""
    r = ler("results/etapa7.2/mav_solido.yaml")
    ref = r["referencia_msr"]
    assert r["casos"][0]["glom_kg"] > r["casos"][1]["glom_kg"]   # o Δv com perdas pede mais massa
    for x in r["casos"]:
        mp = sum(x["propelente_kg"])
        assert x["empuxos_n"][0] == pytest.approx(ref["empuxo_medio_n"][0] * x["propelente_kg"][0] / ref["propelente_kg"][0])
        for c in x["comprimentos"]:
            assert c["comprimento_m"] == pytest.approx(c["comprimento_fixo_m"] + (ref["comprimento_m"] - c["comprimento_fixo_m"]) * mp / sum(ref["propelente_kg"]))
            assert c["folga_sem_deck_m"] == pytest.approx((r["limites"]["sem_deck_m"] - c["comprimento_m"]) / 2)
