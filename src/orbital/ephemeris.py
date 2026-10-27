"""Acesso às efemérides planetárias via SPICE (spiceypy).

Efemérides: JPL DE440 (Park et al., 2021, AJ 161:105), arquivo de440s.bsp
(1849–2150) — docs/fontes.md [F1], ADR 0002.
Leap seconds: NAIF naif0012.tls — docs/fontes.md [F2].

Convenções:
- Tempo de entrada em TDB (string ISO "AAAA-MM-DDTHH:MM:SS"), o tempo das equações
  de movimento das efemérides DE.
- Frame "J2000" do SPICE. As efemérides DE são referidas ao ICRF; o SPICE trata
  J2000 e ICRF como o mesmo frame para SPKs DE (NAIF, "Frames Required Reading").
- Estados geométricos (sem correção de aberração), em km e km/s.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import spiceypy as spice
import yaml

RAIZ = Path(__file__).resolve().parents[2]
CONFIG_KERNELS = RAIZ / "config" / "kernels.yaml"

# Códigos NAIF (NAIF, "NAIF Integer ID codes" Required Reading).
# de440s.bsp traz o baricentro de Marte (4), não o centro do corpo (499).
# A distância entre os dois vem de Fobos e Deimos: Σ GM_lua/GM_sistema × a_lua, entre
# 0,10 e 0,21 m conforme a geometria (GM: MAR099 [F7]; a, e: SSD/JPL [F8]; ver
# orbital.marte e results/etapa1.1/baricentro_marte.yaml).
SOL = "10"
TERRA = "399"
BARICENTRO_TERRA_LUA = "3"
BARICENTRO_MARTE = "4"

_carregados: set[Path] = set()


def kernels_configurados(config: Path = CONFIG_KERNELS) -> list[Path]:
    """Caminhos dos kernels listados em config/kernels.yaml."""
    cfg = yaml.safe_load(config.read_text(encoding="utf-8"))
    diretorio = RAIZ / cfg["diretorio"]
    return [diretorio / k["arquivo"] for k in cfg["kernels"]]


def carregar_kernels(config: Path = CONFIG_KERNELS) -> None:
    """Carrega (furnsh) os kernels configurados, uma única vez por processo."""
    for caminho in kernels_configurados(config):
        if caminho in _carregados:
            continue
        if not caminho.exists():
            raise FileNotFoundError(
                f"Kernel ausente: {caminho}. Rode: python tools/fetch_kernels.py"
            )
        spice.furnsh(str(caminho))
        _carregados.add(caminho)


def tdb_para_et(tdb_iso: str) -> float:
    """Converte data ISO em TDB para segundos TDB após J2000 (ET do SPICE)."""
    # str2et não aceita o delimitador ISO "T" junto do rótulo de escala "TDB".
    return spice.str2et(f"{tdb_iso.replace('T', ' ')} TDB")


def estado(alvo: str, tdb_iso: str, observador: str = SOL,
           frame: str = "J2000") -> tuple[np.ndarray, np.ndarray]:
    """Estado geométrico (r [km], v [km/s]) de `alvo` relativo a `observador`."""
    carregar_kernels()
    st, _ = spice.spkezr(alvo, tdb_para_et(tdb_iso), frame, "NONE", observador)
    st = np.asarray(st)
    return st[:3], st[3:]


def data_tdb(et: float) -> str:
    """Data do calendário em TDB (AAAA-MM-DD) de uma época ET.

    As grades de datas do projeto são épocas à meia-noite TDB; converter para UTC (et2utc) dá 69 s antes da
    meia-noite e, portanto, o dia anterior. Este é o rótulo correto dessas épocas (errata da Etapa 2.4)."""
    carregar_kernels()
    return spice.timout(et, "YYYY-MM-DD ::TDB")


def instante_tdb(et: float) -> str:
    """Data e hora em TDB (AAAA-MM-DDTHH:MM:SS) de uma época ET."""
    carregar_kernels()
    return spice.timout(et, "YYYY-MM-DDTHR:MN:SC ::TDB ::RND")
