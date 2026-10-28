"""Espiral de baixo empuxo (Etapa 3.2): solução analítica quase circular, integração numérica e verificação contra
Schwenzfeger, NASA TM X-64836 [F113]."""

from __future__ import annotations

import math

import pytest

from orbital import baixo_empuxo as be
from orbital.config import ler, v

CFG = ler("config/baixo_empuxo.yaml")
TOL = v(CFG["verificacao_schwenzfeger"]["tolerancia_relativa"])   # 1e-4, precisão relevante do estudo (P-046)


def test_edelbaum_coplanar_e_a_diferenca_das_velocidades_circulares():
    assert be.dv_edelbaum_coplanar(1.0, 1.0, 4.0) == pytest.approx(0.5)
    assert be.dv_edelbaum_coplanar(1.0, 4.0, 1.0) == pytest.approx(0.5)   # descer custa o mesmo que subir


@pytest.mark.parametrize("r1", [0.5, 2.0])
def test_espiral_numerica_converge_para_a_analitica(r1):
    """Com ε pequeno a órbita fica quase circular, e o Δv numérico tende ao analítico (diferença ~ ε²)."""
    ed = be.dv_edelbaum_coplanar(1.0, 1.0, r1)
    dif = [abs(be.espiral(1.0, 1.0, r1, aceleracao=eps).dv - ed) / ed for eps in (1e-2, 1e-3)]
    assert dif[1] < TOL
    assert dif[1] < dif[0] / 10


def test_empuxo_constante_com_massa_variavel():
    """Δv pela equação do foguete e duração coerentes com a aceleração constante (mesmo Δv) e com a duração analítica."""
    mu, r0, r1 = 42828.0, 10000.0, 5000.0              # km³/s², km (valores de teste, não do estudo)
    e = be.espiral(mu, r0, r1, empuxo_n=1.0, isp_s=2000.0, m0_kg=1000.0)
    ed = be.dv_edelbaum_coplanar(mu, r0, r1)
    assert e.dv == pytest.approx(ed, rel=TOL)
    assert e.duracao == pytest.approx(be.duracao_empuxo_constante(e.dv, 1000.0, 1.0, 2000.0), rel=1e-9)
    assert e.massa_final_kg < 1000.0 and e.raio_final < r0


def test_verificacao_schwenzfeger_em_r_phi_v_h():
    """Raio, ângulo, v = r·v_θ e energia ficam dentro da tolerância declarada em todos os pontos publicados (p. 31).
    A componente u = r·ṙ fica fora em três pontos (até 3,2e-4): ver docs/etapa3.2_baixo_empuxo.md."""
    vs = CFG["verificacao_schwenzfeger"]
    calc = be.trajetoria_aceleracao_constante(v(vs["eps"]), [p["t"] for p in vs["pontos"]])
    for p, c in zip(vs["pontos"], calc):
        for k in ("r", "phi", "v", "h"):
            assert abs(c[k] - p[k]) <= TOL * abs(p[k]), (p["t"], k)
        assert math.hypot(c["u"] - p["u"], c["v"] - p["v"]) <= TOL * math.hypot(p["u"], p["v"])


def test_resultado_da_etapa_3_2():
    r = ler("results/etapa3.2/baixo_empuxo.yaml")
    assert r["verificacao_schwenzfeger"]["eps"] == v(CFG["verificacao_schwenzfeger"]["eps"])
    assert {k for q in r["verificacao_schwenzfeger"]["pontos"] for k in q["fora_da_tolerancia"]} <= {"u"}
    for caso in r["conferencia_edelbaum"].values():
        dif = [abs(x["diferenca_relativa"]) for x in caso["linhas"]]
        assert dif == sorted(dif, reverse=True) and dif[-1] < TOL
