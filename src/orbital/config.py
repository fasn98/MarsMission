"""Leitura de config/ e results/ e parâmetros orbitais do estudo.

RAIZ é a raiz do repositório que contém este pacote (src/orbital → ../..). Funciona com o pacote instalado em
modo editável (pip install -e .), que é como environment.yml e o Replit o instalam.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from orbital import missao as ms

RAIZ = Path(__file__).resolve().parents[2]


def ler(caminho, raiz=None):
    """YAML de um caminho relativo à raiz do repositório (ex.: "config/superficie.yaml")."""
    return yaml.safe_load(((raiz or RAIZ) / caminho).read_text(encoding="utf-8"))


def v(item):
    """Valor numérico de um item {valor: ..., fonte: ...} do config."""
    return float(item["valor"])


def nativo(x):
    """Converte tipos do numpy para tipos nativos (para o YAML)."""
    if isinstance(x, dict):
        return {k: nativo(y) for k, y in x.items()}
    if isinstance(x, (list, tuple)):
        return [nativo(y) for y in x]
    if hasattr(x, "item"):
        return x.item()
    return x


def parametros(raiz=None):
    """Parâmetros orbitais da busca de missões (config/parametros_orbitais.yaml e premissa P-006)."""
    po = ler("config/parametros_orbitais.yaml", raiz)
    premissas = {p["nome"]: p["valor"] for p in ler("config/premissas.yaml", raiz)["premissas"]}
    rt, rm = v(po["raio_terra_km"]), v(po["raio_marte_km"])
    leo = rt + v(po["leo_altitude_km"])
    orbitas = {}
    for nome, o in po["orbitas_marte"].items():
        orbitas[nome] = ms.Orbita(rm + float(o["periapse_alt_km"]["valor"]), rm + float(o["apoapse_alt_km"]["valor"]))
    return ms.Parametros(
        mu_terra=v(po["gm_terra"]), mu_marte=v(po["gm_marte"]), leo=ms.Orbita(leo, leo),
        orbitas_marte=orbitas, rp_aerocaptura_marte=rm + v(po["aerocaptura_periapse_alt_km"]),
        r_interface_terra=rt + v(po["interface_reentrada_alt_km"]),
        exclusao_180=float(premissas["exclusao_angulo_180_graus"]),
        v_reentrada_max=v(po["reentrada_max_km_s"]))
