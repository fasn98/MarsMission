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
    assert orb["CCRS"]["massa_kg"] == pytest.approx(620.0)
    # propelente do orbitador = o do orçamento
    prop = sum(c["massa_kg"] for c in r["veiculos"]["orbitador"] if c["nome"].startswith("Propelente"))
    arq = ler("results/etapa2.5/arquitetura.yaml")["orbitador"]["composicao"]
    assert prop == pytest.approx(sum(x.get("propelente_kg", 0) for x in arq))


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
