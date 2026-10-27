"""Testes da Etapa 2.4: geometria de lançamento, DLA na grade e dados do ELVPerf."""

import html
import re
from pathlib import Path

import numpy as np
import pytest
import yaml

from orbital import lancamento as la

RAIZ = Path(__file__).resolve().parents[1]
MU_T = 398600.43550702266


def test_inclinacao_de_azimute():
    assert la.inclinacao(28.45, 90.0) == pytest.approx(28.45)          # para leste: i = latitude
    assert la.inclinacao(0.0, 40.0) == pytest.approx(50.0)
    # cos i = cos φ · sen Σ, com Σ = 40° no Eastern Range [F13]
    assert la.inclinacao(28.45, 40.0) == pytest.approx(np.degrees(np.arccos(np.cos(np.radians(28.45)) * np.sin(np.radians(40.0)))))


def test_delta_plano():
    assert la.delta_plano(29.234, 28.5) == pytest.approx(0.734)
    assert la.delta_plano(-55.45, 51.6) == pytest.approx(3.85)
    assert la.delta_plano(14.8, 28.5) == 0.0


def test_dv_saida_coplanar_e_fora_do_plano():
    r = 6378.1366 + 407.0
    c3 = 9.0984
    v_c, v_h = np.sqrt(MU_T / r), np.sqrt(c3 + 2 * MU_T / r)
    assert la.dv_saida(MU_T, r, c3) == pytest.approx(v_h - v_c)
    di = 5.0
    esperado = np.sqrt(v_h**2 + v_c**2 - 2 * v_h * v_c * np.cos(np.radians(di)))
    assert la.dv_saida(MU_T, r, c3, di) == pytest.approx(esperado)
    assert la.dv_saida(MU_T, r, c3, di) > la.dv_saida(MU_T, r, c3)


def test_interpolar_sem_extrapolar():
    assert la.interpolar(9.5, [9, 10], [100, 80]) == pytest.approx(90)
    assert np.isnan(la.interpolar(10.7, [0, 5, 9, 10], [4, 3, 2, 1]))


def _capacidades(fn):
    t = (RAIZ / "tests/data/elvperf" / fn).read_text(encoding="utf-8")
    L = [x.strip() for x in html.unescape(re.sub(r"<[^>]+>", "\n", t)).split("\n") if x.strip()]
    out = {}
    for k in range(L.index("Ground Rules") + 1, len(L) - 3):
        if L[k + 1].startswith("(") and L[k + 2] in ("CCSFS", "KSC") and re.fullmatch(r"[\d,]+", L[k + 3]):
            out[(L[k] + " " + L[k + 1]).replace(" )", ")")] = int(L[k + 3].replace(",", ""))
    return out


NOMES = {"Falcon 9 (ASDS)": "Falcon 9 (Full Thrust, ASDS)", "Falcon Heavy (recuperação)": "Falcon Heavy (Recovery)",
         "Falcon Heavy (descartável)": "Falcon Heavy (Expendable)", "Vulcan VC2": "Vulcan (VC2)", "Vulcan VC4": "Vulcan (VC4)",
         "Vulcan VC6": "Vulcan (VC6)", "New Glenn": "New Glenn (New Glenn)"}


def test_config_lancadores_confere_com_elvperf():
    """Os pontos de C3 e de LEO tirados do ELVPerf [F79] batem com as respostas brutas guardadas."""
    cfg = yaml.safe_load((RAIZ / "config/lancadores.yaml").read_text(encoding="utf-8"))["lancadores"]
    for nome, elv in NOMES.items():
        c = cfg[nome]["c3"]
        for c3, m in zip(c["pontos"], c["massa_kg"]):
            assert _capacidades(f"elv_result_he_{c3:g}.html")[elv] == m, (nome, c3)
        for inc, m in cfg[nome]["leo_400km"].items():
            if isinstance(inc, float):
                assert _capacidades(f"elv_result_leo_{inc:g}_400.html")[elv] == m, (nome, inc)
    assert "Performance shown is applicable for declinations between 28.5 deg. and -28.5 deg." in \
        (RAIZ / "tests/data/elvperf/elv_result_he_9.html").read_text(encoding="utf-8")


def test_dla_da_grade_confere_com_a_missao_A():
    """A DLA calculada na grade (porkchop) é a mesma da linha detalhada da Etapa 1.3 (missão A)."""
    from orbital import ephemeris as eph
    from orbital import porkchop as pc
    import spiceypy as spice

    eph.carregar_kernels()
    m = yaml.safe_load((RAIZ / "results/etapa1.3/missoes.yaml").read_text(encoding="utf-8"))
    a = next(c for c in m["candidatas"] if c["id"] == "2028-conjuncao")
    # As datas gravadas são a conversão para UTC (et2utc) de épocas à meia-noite TDB; como TDB − UTC ≈ 69 s,
    # a data impressa é a do dia anterior. A época da grade é a meia-noite TDB do dia seguinte à data impressa.
    et1 = spice.str2et(a["partida_terra"] + " 00:00:00 TDB") + 86400.0
    et2 = spice.str2et(a["chegada_marte"] + " 00:00:00 TDB") + 86400.0
    assert spice.et2utc(et1, "ISOC", 0)[:10] == a["partida_terra"]
    g = pc.calcular_grade(eph.TERRA, eph.BARICENTRO_MARTE, [et1], [et2])
    assert g.dla_graus[0, 0] == pytest.approx(a["dla_graus"], abs=1e-3)
    assert g.c3[0, 0] == pytest.approx(a["c3_km2_s2"], abs=1e-3)
