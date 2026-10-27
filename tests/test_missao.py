"""Testes da busca de missões (orbital.missao).

A busca por mínimos cumulativos é comparada com força bruta sobre todas as quádruplas
(partida Terra, chegada Marte, partida Marte, chegada Terra) em grades sintéticas aleatórias.
"""

from __future__ import annotations

import itertools

import numpy as np
import pytest

from orbital import missao as ms
from orbital import porkchop as pc

DIA = pc.DIA
P = ms.Parametros(mu_terra=398600.4, mu_marte=42828.4, leo=ms.Orbita(6778.0, 6778.0),
                  orbitas_marte={"baixa": ms.Orbita(3800.0, 3800.0), "alta": ms.Orbita(3650.0, 37000.0)},
                  rp_aerocaptura_marte=3450.0, r_interface_terra=6500.0, exclusao_180=1.0)


def _grades(rng, n_dep=6, n_M=12, n_arr=10):
    et_dep = np.arange(n_dep) * 10 * DIA
    et_M = 100 * DIA + np.arange(n_M) * 10 * DIA
    et_arr = 300 * DIA + np.arange(n_arr) * 10 * DIA
    ida = pc.Grade(et_dep, et_M, rng.uniform(8, 20, (n_dep, n_M)), rng.uniform(2, 6, (n_dep, n_M)),
                   rng.uniform(100, 250, (n_dep, n_M)), (et_M[None, :] - et_dep[:, None]) / DIA)
    volta = pc.Grade(et_M, et_arr, rng.uniform(5, 20, (n_M, n_arr)), rng.uniform(2, 6, (n_M, n_arr)),
                     rng.uniform(100, 250, (n_M, n_arr)), (et_arr[None, :] - et_M[:, None]) / DIA)
    ida.c3[0, 3] = np.nan  # célula sem solução
    volta.angulo_transf[2, 4] = 180.4  # dentro da exclusão de 180°
    return ida, volta


def _forca_bruta(ida, volta, perm, dur, orbita, aero, tofmax=np.inf, p=P):
    melhor = (np.inf, None)
    for i, a, d, k in itertools.product(*(range(n) for n in (len(ida.et_partida), len(ida.et_chegada),
                                                                len(volta.et_partida), len(volta.et_chegada)))):
        s = (ida.et_chegada[d] - ida.et_chegada[a]) / DIA
        if not (perm[0] <= s <= perm[1]) or (volta.et_chegada[k] - ida.et_partida[i]) / DIA > dur:
            continue
        if ida.tof_dias[i, a] > tofmax or volta.tof_dias[d, k] > tofmax:
            continue
        if np.sqrt(volta.vinf_chegada[d, k] ** 2 + 2 * p.mu_terra / p.r_interface_terra) > p.v_reentrada_max:
            continue
        if not np.isfinite(ida.c3[i, a]) or abs(ida.angulo_transf[i, a] - 180) <= 1 or abs(volta.angulo_transf[d, k] - 180) <= 1:
            continue
        c = (ms.custo_saida_terra(p, ida.c3[i, a]) + ms.custo_captura_marte(p, ida.vinf_chegada[i, a], orbita, aero)
             + ms.custo_saida_marte(p, volta.c3[d, k], orbita))
        if c < melhor[0]:
            melhor = (float(c), (i, a, d, k))
    return melhor


@pytest.mark.parametrize("semente", range(6))
@pytest.mark.parametrize(("orbita", "aero"), [("baixa", False), ("alta", True)])
@pytest.mark.parametrize(("perm", "dur", "tofmax"), [((20, 60), 330, np.inf), ((40, 90), 1e9, np.inf),
                                                     ((20, 90), 1e9, 250.0)])
def test_busca_igual_forca_bruta(semente, orbita, aero, perm, dur, tofmax):
    ida, volta = _grades(np.random.default_rng(semente))
    esperado = _forca_bruta(ida, volta, perm, dur, orbita, aero, tofmax)
    obtido = ms.melhor_combinacao(P, ida, volta, perm, dur, orbita, aero, tofmax)
    if esperado[1] is None:
        assert obtido is None
    else:
        assert obtido[0] == pytest.approx(esperado[0], rel=1e-12)


@pytest.mark.parametrize("semente", range(6))
def test_limite_de_reentrada_igual_forca_bruta(semente):
    import dataclasses
    p = dataclasses.replace(P, v_reentrada_max=11.9)  # corta parte dos v∞ sintéticos (2–6 km/s)
    ida, volta = _grades(np.random.default_rng(semente))
    esperado = _forca_bruta(ida, volta, (20, 90), 1e9, "alta", False, np.inf, p)
    obtido = ms.melhor_combinacao(p, ida, volta, (20, 90), 1e9, "alta", False)
    if esperado[1] is None:
        assert obtido is None
    else:
        assert obtido[0] == pytest.approx(esperado[0], rel=1e-12)


def test_envelope_maior_dos_minimos_por_janela():
    def c(j, classe, dv):
        return {"id": f"{j}-{classe}", "janela_ida": j, "classe": classe,
                "por_orbita_marte": {"alta": {"dv_total_sem_aerocaptura_km_s": dv, "dv_total_com_aerocaptura_km_s": dv - 1}}}
    cands = [c("A", "conjuncao", 5.4), c("A", "curto", 9.0), c("A", "oposicao", 20.0),
             c("B", "conjuncao", 5.9), c("B", "oposicao", 17.0), c("C", "conjuncao", 5.7)]
    valor, define, minimos = ms.envelope_dimensionamento(cands, ["A", "B", "C"], ["conjuncao", "oposicao"],
                                                         "alta", "propulsiva")
    assert (valor, define) == (5.9, "B-conjuncao")
    assert minimos["A"] == ("A-conjuncao", 5.4)  # a classe "curto" não entra


@pytest.mark.parametrize("semente", [3, 11])
def test_limite_de_dla_equivale_a_excluir_as_celulas(semente):
    """dla_max_graus dá o mesmo resultado que remover da grade de ida as células com |DLA| acima do limite."""
    rng = np.random.default_rng(semente)
    ida, volta = _grades(rng)
    ida.dla_graus = rng.uniform(-60, 60, ida.c3.shape)
    r = ms.melhor_combinacao(P, ida, volta, (20, 200), 600, "alta", False, dla_max_graus=30.0)
    sem = pc.Grade(ida.et_partida, ida.et_chegada, np.where(np.abs(ida.dla_graus) > 30.0, np.nan, ida.c3),
                   ida.vinf_chegada, ida.angulo_transf, ida.tof_dias)
    r2 = ms.melhor_combinacao(P, sem, volta, (20, 200), 600, "alta", False)
    assert (r is None and r2 is None) or (r[0] == pytest.approx(r2[0]) and r[1] == r2[1])
    livre = ms.melhor_combinacao(P, ida, volta, (20, 200), 600, "alta", False)
    assert livre[0] <= r[0]
