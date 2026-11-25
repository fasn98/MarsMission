"""Orbitador só elétrico da família 1 (Etapa 2, issue #68): peças da ferramenta que não exigem otimizar a missão
inteira (a otimização completa roda na regeneração, parte orbitador_so_eletrico)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))

import orbitador_so_eletrico as ose  # noqa: E402
from orbital import lancamento as lc  # noqa: E402
from orbital import sims_flanagan as sf  # noqa: E402
from orbital.config import ler, v  # noqa: E402
from orbital.constantes import GM_SOL, UA_KM  # noqa: E402

DIA = 86400.0


def test_capacidade_do_objetivo_coincide_com_a_oficial_nos_pontos_publicados():
    """A curva do objetivo (PCHIP em C3) passa pelos mesmos pontos do ELVPerf [F79] que a interpolação linear oficial, nas
    duas formulações do limite de DLA, com DLA zero (sem multiplicador)."""
    import copy
    e = ose._entradas()
    for formulacao in ("suave", "restricao"):
        e2 = {**e, "se": copy.deepcopy(e["se"])}
        e2["se"]["otimizador"]["formulacao_dla"]["valor"] = formulacao
        cap, cap_obj, lim_dla, c3_max = ose._capacidade(e2)
        lan = e["lcfg"]["lancadores"][e["se"]["missao"]["lancador"]]
        assert c3_max == max(lan["c3"]["pontos"]) and lim_dla == 28.5
        for c3 in lan["c3"]["pontos"]:
            vinf = np.array([math.sqrt(c3), 0.0, 0.0])   # no equinócio: declinação zero
            assert cap_obj(vinf) == pytest.approx(cap(vinf), rel=1e-12)
            assert cap(vinf) == pytest.approx(lc.interpolar(c3, lan["c3"]["pontos"], lan["c3"]["massa_kg"]) - lc.adaptador_p097()[0])


def test_multiplicador_suave_de_dla_sem_quina_em_28_5():
    """Formulação "suave": o multiplicador do objetivo vale 1 até 28,5°, tem derivada zero ali (sem a quina da P-036) e
    passa pelos pontos da P-036."""
    import copy
    e = {**ose._entradas()}
    e["se"] = copy.deepcopy(e["se"])
    e["se"]["otimizador"]["formulacao_dla"]["valor"] = "suave"
    cap, cap_obj, lim, _ = ose._capacidade(e)
    rot = ose._ecl_para_eq()

    def vinf_com_dla(graus, c3=4.0):
        d = np.array([math.cos(math.radians(graus)), 0.0, math.sin(math.radians(graus))])   # no equador J2000
        return math.sqrt(c3) * (rot.T @ d)
    base = cap_obj(vinf_com_dla(0.0))
    k = [(cap_obj(vinf_com_dla(lim + x)) + lc.adaptador_p097()[0]) / (base + lc.adaptador_p097()[0]) for x in (-1e-3, 0.0, 1e-3)]
    assert k[0] == pytest.approx(1.0, abs=1e-12) and k[1] == pytest.approx(1.0, abs=1e-12)
    assert abs(k[2] - 1.0) < 1e-6   # derivada nula: variação de segunda ordem
    ad = lc.adaptador_p097()[0]
    for g in e["lcfg"]["dla"]["multiplicador_nordeste"]["dla_graus"]:
        oficial = cap(vinf_com_dla(g))
        if oficial > 0:   # acima da inclinação máxima a oficial dá zero (exige dogleg) e o objetivo não é usado ali
            assert (cap_obj(vinf_com_dla(g)) + ad) / (base + ad) == pytest.approx((oficial + ad) / (cap(vinf_com_dla(0.0)) + ad), rel=1e-9)


def test_regeneracao_verifica_sem_reotimizar():
    """Verificar, não reotimizar (decisão do Fabio, 2026-11-24): o CI roda o caso publicado e a verificação; as soluções
    gravadas cobrem todas as configurações do config, e a parte da verificação baixa o que ela lê."""
    import confere_regeneracao as cr
    assert cr.ORBITADOR_SO_ELETRICO == [["tools/orbitador_so_eletrico.py", "--caso-publicado"], ["tools/orbitador_so_eletrico.py", "--verifica"]]
    ps = yaml.safe_load((RAIZ / "tools" / "regeneracao_partes.yaml").read_text(encoding="utf-8"))["partes"]
    assert ps["se_verifica"] == {"depende_de": ["base", "mav_familia1", "se_caso_publicado"], "ferramentas": ["orbitador_so_eletrico --verifica"]}
    assert not any("--bloco" in f for p in ps.values() for f in p["ferramentas"])
    ms = ler("config/orbitador_so_eletrico.yaml")["missao"]
    for h in ms["altitudes_km"]["valor"]:
        for nome, ns in ms["n_ativos"]["valor"].items():
            d = yaml.safe_load(ose._arquivo_solucoes(nome, h).read_text(encoding="utf-8"))
            assert (d["formato"], d["propulsor"], d["altitude_km"]) == (1, nome, float(h))
            assert [c["n_ativos"] for c in d["configuracoes"]] == sorted(ns)
            assert all(c["tentativas"] for c in d["configuracoes"])


def test_avaliar_reproduz_o_otimizador():
    """sf.avaliar devolve, para a solução do otimizador, o mesmo resíduo e a mesma violação que o otimizar."""
    r0, v0 = np.array([UA_KM, 0.0, 0.0]), np.array([0.0, math.sqrt(GM_SOL / UA_KM), 0.0])
    tof = 250.0 * DIA
    alvo_r, alvo_v = sf.kepler.propagar(GM_SOL, r0, v0 * 1.03, tof)
    p = sf.Perna(GM_SOL, lambda t: (r0, v0), lambda t: (alvo_r, alvo_v), sf.Motor(0.5, 3000.0), 8, (0.0, 0.0), (tof, tof),
                 (0.0, 0.0), (0.0, 0.0), (1000.0, 1000.0), (200.0, 1000.0))
    chute = {"t0": 0.0, "tof": tof, "m0": 1000.0, "mf": 900.0, "vinf0": np.zeros(3), "vinf1": np.zeros(3),
             "u": np.tile([0.0, 0.3, 0.0], (8, 1))}
    s = sf.otimizar(p, lambda t0, tof, m0, mf, a, b: -mf, sf.viabilizar(p, chute)[0], maxiter=200)
    a = sf.avaliar(p, s)
    assert a["residuo_max"] == s["residuo_max"] and a["violacao_u"] == s["violacao_u"]


def test_verificacao_aceita_a_gravada_e_recusa_a_perturbada():
    """A verificação aceita uma solução gravada que fecha (NEXT-C, 4 ativos, 380 km) e recusa a mesma com a partida um dia
    depois (os comandos deixam de ligar os planetas)."""
    d = yaml.safe_load(ose._arquivo_solucoes("NEXT-C", 380).read_text(encoding="utf-8"))
    sm = next(tn["solucao"] for c in d["configuracoes"] if c["n_ativos"] == 4 for tn in c["tentativas"] if "solucao" in tn)
    r = ose.fecho("NEXT-C", 4, 380.0, chutes=ose._de_semente(sm), verificar=True)
    assert r["verificacao"]["verificada"] and r["fecha"]
    ruim = ose._de_semente(sm)
    ruim["ida"]["t0"] += DIA
    assert not ose.fecho("NEXT-C", 4, 380.0, chutes=ruim, verificar=True)["verificacao"]["verificada"]


def test_semente_da_cadeia_volta_igual_pelo_yaml():
    """Um bloco continua do anterior pela semente gravada em YAML: a volta é exata (os floats saem com repr)."""
    rng = np.random.default_rng(7)
    perna = lambda: {"t0": float(rng.normal()) * 1e8, "tof": float(rng.uniform(1e7, 9e7)), "m0": float(rng.uniform(5e3, 1e4)),
                     "mf": float(rng.uniform(1e3, 5e3)), "vinf0": rng.normal(size=3), "vinf1": rng.normal(size=3),
                     "u": rng.uniform(-1, 1, size=(30, 3)), "mensagem": "ignorada"}
    ch = {"ida": perna(), "volta": perna(), "empuxo_n": 1.234567890123, "isp_s": 2500.0}
    volta = ose._de_semente(yaml.safe_load(yaml.safe_dump(ose._semente(ch))))
    for k in ("ida", "volta"):
        for c in ose.SEMENTE:
            assert np.array_equal(np.asarray(volta[k][c]), np.asarray(ch[k][c]))
    assert volta["empuxo_n"] == ch["empuxo_n"]


def test_conclusoes_de_quem_nao_tem_solucao_e_do_propulsor():
    cfg = ler("config/orbitador_so_eletrico.yaml")
    falha = {"falha": "x", "situacao": "nenhuma solução verificada"}
    assert ose._conclusoes(falha, cfg) == ["não (nenhuma solução verificada)", "—", "—", "—"]
    ok = {"margem_falcon_heavy": 0.5, "ultimo_lancamento_mav": "2032-04-26", "pronto_no_encontro": "2031-01-01", "dentro_da_vida": True}
    ruim = {**ok, "margem_falcon_heavy": -0.5}
    borda = {**ok, "margem_falcon_heavy": 0.01}
    # existência (decisão do Fabio, 2026-11-24): quem não tem solução verificada não conta contra
    assert ose._fecha_propulsor([{**ok, "n_ativos": 3}, {**falha, "n_ativos": 1}], cfg) == ["sim", "3"]
    assert ose._fecha_propulsor([{**ruim, "n_ativos": 3}, {**falha, "n_ativos": 1}], cfg) == ["não demonstrado", "—"]
    assert ose._fecha_propulsor([{**ruim, "n_ativos": 3}], cfg) == ["não demonstrado", "—"]
    assert ose._fecha_propulsor([{**borda, "n_ativos": 3}, {**ruim, "n_ativos": 2}], cfg) == ["indeterminado", "3"]


def test_margem_como_limite_inferior():
    assert ose._pelo_menos(0.4593) == "45 %" and ose._pelo_menos(1.0) == "100 %" and ose._pelo_menos(-0.111) == "−12 %"


def test_viabilizar_acha_ponto_continuo():
    """Partida a frio: a etapa de mínimos quadrados leva um chute ruim a um ponto em que a perna é contínua."""
    r0, v0 = np.array([UA_KM, 0.0, 0.0]), np.array([0.0, math.sqrt(GM_SOL / UA_KM), 0.0])
    tof = 250.0 * DIA
    alvo_r, alvo_v = sf.kepler.propagar(GM_SOL, r0, v0 * 1.03, tof)   # alvo alcançável com um pouco de empuxo
    p = sf.Perna(GM_SOL, lambda t: (r0, v0), lambda t: (alvo_r, alvo_v), sf.Motor(0.5, 3000.0), 8, (0.0, 0.0), (tof, tof),
                 (0.0, 0.0), (0.0, 0.0), (1000.0, 1000.0), (200.0, 1000.0))
    chute = {"t0": 0.0, "tof": tof, "m0": 1000.0, "mf": 900.0, "vinf0": np.zeros(3), "vinf1": np.zeros(3),
             "u": np.tile([0.0, 0.3, 0.0], (8, 1))}
    ch, res = sf.viabilizar(p, chute)
    assert res < 1e-9
    assert np.all(np.linalg.norm(ch["u"], axis=1) <= 1.0 + 1e-12)


def test_config_fora_do_catalogo():
    """O NEXT-C fica fora do catálogo (ADR 0013, item 4) até a decisão do Fabio; a vida de cada propulsor tem fonte."""
    assert "NEXT-C" not in ler("config/eletrica.yaml")["propulsores"]
    cfg = ler("config/orbitador_so_eletrico.yaml")
    for nome in ("XIPS-25", "NEXT-C"):
        assert v(cfg["propulsores"][nome]["vida_kg"]) > 0 and "fonte" in cfg["propulsores"][nome]["vida_kg"]
    assert "[F278]" in cfg["propulsores"]["NEXT-C"]["voo"]


def test_declinacao_no_equador_da_terra():
    """Os estados vêm em ECLIPJ2000 (orbital.porkchop); a declinação é no equador J2000: o polo da eclíptica fica a
    90° − obliquidade de declinação, e um vetor no equinócio (eixo x, comum aos dois) tem declinação zero."""
    obl = math.degrees(math.acos(float(ose._ecl_para_eq()[2, 2])))
    assert 23.0 < obl < 24.0
    assert ose._declinacao(np.array([0.0, 0.0, 2.0])) == pytest.approx(90.0 - obl, abs=1e-9)
    assert ose._declinacao(np.array([3.0, 0.0, 0.0])) == pytest.approx(0.0, abs=1e-9)


def test_textos_do_diagnostico_passam_na_checagem_de_sanidade():
    """O CI reprova diagnóstico com número não finito (NAO_FINITO casa também o caractere ∞): os nomes dos casos e os
    cabeçalhos escritos no diagnóstico não podem usá-lo."""
    import confere_regeneracao as cr
    cfg = ler("config/orbitador_so_eletrico.yaml")
    for c in cfg["caso_publicado"]["casos"].values():
        assert not cr.NAO_FINITO.search(c["nome"]), c["nome"]
    fonte = (RAIZ / "tools" / "orbitador_so_eletrico.py").read_text(encoding="utf-8")
    trecho = fonte[fonte.index("def escreve("):]
    trecho = trecho[trecho.index("\n    d = ["):]
    assert "∞" not in trecho
