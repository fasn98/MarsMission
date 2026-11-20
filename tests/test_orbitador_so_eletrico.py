"""Orbitador só elétrico da família 1 (Etapa 2, issue #68): peças da ferramenta que não exigem otimizar a missão
inteira (a otimização completa roda na regeneração, parte orbitador_so_eletrico)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))

import orbitador_so_eletrico as ose  # noqa: E402
from orbital import lancamento as lc  # noqa: E402
from orbital import sims_flanagan as sf  # noqa: E402
from orbital.config import ler, v  # noqa: E402
from orbital.constantes import GM_SOL, UA_KM  # noqa: E402

DIA = 86400.0


def test_capacidade_suave_coincide_com_a_oficial_nos_pontos_publicados():
    """A curva suave (PCHIP) do objetivo passa pelos mesmos pontos do ELVPerf [F79] que a interpolação linear oficial."""
    e = ose._entradas()
    cap, cap_suave, c3_max = ose._capacidade(e)
    lan = e["lcfg"]["lancadores"][e["se"]["missao"]["lancador"]]
    assert c3_max == max(lan["c3"]["pontos"])
    for c3 in lan["c3"]["pontos"]:
        vinf = np.array([math.sqrt(c3), 0.0, 0.0])   # declinação zero: sem multiplicador de DLA
        assert cap_suave(vinf) == pytest.approx(cap(vinf), rel=1e-12)
        assert cap(vinf) == pytest.approx(lc.interpolar(c3, lan["c3"]["pontos"], lan["c3"]["massa_kg"]) - lc.adaptador_p097()[0])


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
