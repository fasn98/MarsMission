"""Verificação das efemérides locais (DE440 via SPICE) contra o JPL Horizons.

Referência: vetores geométricos heliocêntricos, ICRF, TDB, obtidos da API do Horizons
por tools/fetch_horizons_reference.py e guardados sem edição em tests/data/horizons/
(docs/fontes.md [F3]). O Horizons declara DE441 como fonte; DE440 e DE441 são
descritos juntos em Park et al. (2021), docs/fontes.md [F1].

Tolerâncias: config/premissas.yaml, P-001 e P-002 (NÃO VALIDADAS).
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pytest
import yaml

from orbital import ephemeris as eph

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "tests" / "data" / "horizons"

_NUM = r"([-+]?\d\.\d+E[-+]\d+)"


def _premissa(nome: str) -> float:
    cfg = yaml.safe_load((RAIZ / "config" / "premissas.yaml").read_text(encoding="utf-8"))
    return next(p["valor"] for p in cfg["premissas"] if p["nome"] == nome)


def ler_horizons(arquivo: Path) -> tuple[str, np.ndarray, np.ndarray]:
    """Extrai (época TDB ISO, r [km], v [km/s]) de uma resposta texto do Horizons."""
    texto = arquivo.read_text(encoding="utf-8")
    bloco = texto.split("$$SOE", 1)[1].split("$$EOE", 1)[0]
    data = re.search(r"A\.D\. (\d{4})-(\w{3})-(\d{2}) (\d{2}:\d{2}:\d{2})", bloco)
    meses = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    ano, mes, dia, hora = data.groups()
    iso = f"{ano}-{meses.index(mes) + 1:02d}-{dia}T{hora}"
    r = [float(re.search(rf"\b{c}\s*=\s*{_NUM}", bloco).group(1)) for c in ("X", "Y", "Z")]
    v = [float(re.search(rf"\b{c}\s*=\s*{_NUM}", bloco).group(1)) for c in ("VX", "VY", "VZ")]
    assert "TDB" in bloco and "Reference frame : ICRF" in texto
    assert "Center body name: Sun (10)" in texto
    return iso, np.array(r), np.array(v)


CASOS = [
    ("marte_bari_2028-01-01.txt", eph.BARICENTRO_MARTE),
    ("marte_bari_2033-06-15.txt", eph.BARICENTRO_MARTE),
    ("terra_2028-01-01.txt", eph.TERRA),
]


@pytest.mark.parametrize(("arquivo", "alvo"), CASOS)
def test_estado_heliocentrico_confere_com_horizons(arquivo, alvo):
    iso, r_ref, v_ref = ler_horizons(DADOS / arquivo)
    r, v = eph.estado(alvo, iso)
    erro_r = np.linalg.norm(r - r_ref)
    erro_v = np.linalg.norm(v - v_ref)
    print(f"{arquivo}: |Δr| = {erro_r * 1e3:.3f} m, |Δv| = {erro_v * 1e6:.3f} mm/s")
    assert erro_r < _premissa("tolerancia_efemeride_vs_horizons_km")
    assert erro_v < _premissa("tolerancia_velocidade_vs_horizons_km_s")


def test_kernels_cobrem_o_periodo_da_fase1():
    """As janelas da Fase 1 (2028–2035, mais retorno) precisam estar dentro do de440s.bsp."""
    import spiceypy as spice

    eph.carregar_kernels()
    spk = next(k for k in eph.kernels_configurados() if k.suffix == ".bsp")
    cobertura = spice.spkcov(str(spk), int(eph.BARICENTRO_MARTE))
    inicio, fim = spice.wnfetd(cobertura, 0)
    assert inicio < eph.tdb_para_et("2028-01-01T00:00:00")
    assert fim > eph.tdb_para_et("2040-12-31T00:00:00")


def test_leitor_horizons_rejeita_frame_errado(tmp_path):
    original = (DADOS / CASOS[0][0]).read_text(encoding="utf-8")
    falso = tmp_path / "eclip.txt"
    falso.write_text(original.replace("Reference frame : ICRF", "Reference frame : Ecliptic of J2000.0"),
                     encoding="utf-8")
    with pytest.raises(AssertionError):
        ler_horizons(falso)
