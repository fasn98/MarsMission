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
    assert orb["CCRS"]["massa_kg"] == pytest.approx(620.0, rel=1e-5)   # densidade arredondada a 6 algarismos
    # propelente do orbitador = o do orçamento
    prop = sum(c["massa_kg"] for c in r["veiculos"]["orbitador"] if c["nome"].startswith("Propelente"))
    arq = ler("results/etapa2.5/arquitetura.yaml")["orbitador"]["composicao"]
    # raio arredondado a 6 algarismos (como no FeatureScript): o volume triplica o erro relativo, até ~1,5e-5
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
    (a do item, ou "pai_item") com o mesmo valor. Cobre P-078 a P-095, inclusive o ees_raio_ponta_m da P-094."""
    ps = {p["id"]: p["valor"] for p in ler("config/premissas.yaml")["premissas"]}
    itens = list(_itens_com_premissa(ler("config/cad.yaml")))
    assert any(c[-1] == "ees_raio_ponta_m" for c, _, _ in itens)
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
    # o arquivo atual do lander (cone interno com 12 algarismos) reproduz o modelo atual
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
                    assert c[k] == cp.r6(c[k])


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
    """Página do portão: o piso soma tanques e P-086; o caso de 0,57 m bate com a varredura; a situação segue a regra."""
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
    assert r["r4d"]["catalogo_massa_kg"] == pytest.approx(r["r4d"]["variantes"]["300:1"]["massa_kg"], rel=1e-3)


def test_consumo_cruzeiro():
    """Com propelente de cruzeiro cheio, o CG é o do lançamento; o CG x cai com o consumo (MON-3 mais pesado em +x)."""
    r = ler("results/etapa7.2/cg_lateral.yaml")
    li = r["consumo_cruzeiro"]["linhas"]
    assert li[0]["cg_m"] == pytest.approx(r["configuracoes"]["lançamento"]["cg_m"], abs=1e-12)
    xs = [x["cg_m"][0] for x in li]
    assert all(b < a for a, b in zip(xs, xs[1:]))
