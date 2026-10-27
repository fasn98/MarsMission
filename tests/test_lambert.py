"""Testes do solver de Lambert (Izzo, 2015).

1. Implementação de referência do autor (valladopy, Vallado/CelesTrak, [F12]): 0 e 1
   revolução, caminhos curto e longo (tests/data/lambert_livros.yaml), tolerância P-005.
2. Exemplos impressos em livro-texto: pulados enquanto edição, página e resposta não forem
   conferidas no exemplar (mesmo arquivo).
3. Propriedade física: a solução propagada por Kepler analítico (variável universal,
   orbital.kepler, [F11]) pelo tempo de voo chega em r2 com v2 (tolerância P-003, NÃO
   VALIDADA), para M = 0 e para várias revoluções, sem excluir nenhum caso.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import numpy as np
import pytest
import yaml
from orbital import kepler, lambert

RAIZ = Path(__file__).resolve().parents[1]
CASOS_LIVRO = yaml.safe_load((RAIZ / "tests" / "data" / "lambert_livros.yaml").read_text(encoding="utf-8"))


def _premissa(nome):
    cfg = yaml.safe_load((RAIZ / "config" / "premissas.yaml").read_text(encoding="utf-8"))
    return next(p["valor"] for p in cfg["premissas"] if p["nome"] == nome)


REF = CASOS_LIVRO["referencia_autor"]


@pytest.mark.parametrize("caso", REF["casos"], ids=lambda c: c["id"])
def test_referencia_do_autor_valladopy(caso):
    tol = _premissa("tolerancia_lambert_vs_referencia_km_s")
    re = REF["re_km"]
    sol = lambert.resolver(REF["mu"], np.array(REF["r1_re"]) * re, np.array(REF["r2_re"]) * re,
                           REF["tof_s"], revolucoes=caso["revolucoes"], prograde=caso["prograde"],
                           ramo=caso["ramo"])
    assert np.abs(sol.v1 - caso["v1"]).max() < tol
    assert np.abs(sol.v2 - caso["v2"]).max() < tol


def _meia_unidade(texto: str) -> float:
    """Meia unidade do último algarismo de um número impresso, ex.: '-5.9925' -> 5e-5."""
    return 0.5 * 10.0 ** Decimal(texto).as_tuple().exponent


@pytest.mark.parametrize("caso", CASOS_LIVRO["livros"], ids=lambda c: c["id"])
def test_exemplo_impresso_em_livro(caso):
    if caso["v1"] is None:
        pytest.skip(f"{caso['id']}: edição, página e resposta impressa não conferidas no livro")
    sol = lambert.resolver(float(caso["mu"]), [float(x) for x in caso["r1"]],
                           [float(x) for x in caso["r2"]], float(caso["tof_s"]),
                           prograde=caso.get("prograde", True))
    for calc, impresso in [(sol.v1, caso["v1"]), (sol.v2, caso["v2"])]:
        for c, txt in zip(calc, impresso):
            assert abs(c - float(txt)) <= _meia_unidade(str(txt)), (caso["id"], c, txt)


def test_propriedade_kepler_varias_revolucoes():
    mu = 398600.4418
    tol = _premissa("tolerancia_lambert_vs_kepler_rel")
    rng = np.random.default_rng(20261027)
    verificados = {0: 0, 1: 0, 2: 0}
    for _ in range(200):
        r1 = rng.normal(size=3) * 1e4
        r2 = rng.normal(size=3) * 1e4
        tof = rng.uniform(600.0, 2e5)
        m_max = min(lambert.max_revolucoes(mu, r1, r2, tof), 2)
        for M in range(m_max + 1):
            for ramo in (["esquerdo"] if M == 0 else ["esquerdo", "direito"]):
                sol = lambert.resolver(mu, r1, r2, tof, revolucoes=M, ramo=ramo)
                r, v = kepler.propagar(mu, r1, sol.v1, tof)
                assert np.linalg.norm(r - r2) / np.linalg.norm(r2) < tol
                assert np.linalg.norm(v - sol.v2) / np.linalg.norm(sol.v2) < tol
                verificados[M] += 1
    assert all(n > 100 for n in verificados.values()), verificados


def test_ramos_de_varias_revolucoes_sao_distintos():
    mu = 398600.4418
    r1, r2, tof = [7000.0, 0, 0], [0, 8000.0, 1000.0], 30000.0
    assert lambert.max_revolucoes(mu, r1, r2, tof) >= 1
    a = lambert.resolver(mu, r1, r2, tof, revolucoes=1, ramo="esquerdo")
    b = lambert.resolver(mu, r1, r2, tof, revolucoes=1, ramo="direito")
    assert np.linalg.norm(a.v1 - b.v1) > 1e-3


def test_revolucoes_acima_do_maximo_falham():
    mu = 398600.4418
    r1, r2, tof = [7000.0, 0, 0], [0, 8000.0, 1000.0], 30000.0
    m = lambert.max_revolucoes(mu, r1, r2, tof)
    with pytest.raises(lambert.LambertError):
        lambert.resolver(mu, r1, r2, tof, revolucoes=m + 1)
