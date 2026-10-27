"""Testes de orbital.superficie.

A composição do Δv de subida é conferida contra as outras linhas da Tabela 1 de Bowles et al.,
NASA/TM-2013-216620 [F37] (mesmo lançamento equatorial rumo leste, i = 0): a composição a partir
de 100 × 100 km deve ficar acima do valor publicado (é conservadora) e a menos de 10 m/s dele.
"""

from __future__ import annotations

import numpy as np
import pytest

from orbital import superficie as sf

MU, R = 42828.37362069909, 3396.19
TABELA = {(100, 500): 4.1155, (500, 500): 4.2067}


@pytest.mark.parametrize(("alvo", "publicado"), TABELA.items())
def test_composicao_confere_com_bowles(alvo, publicado):
    dv = sf.dv_subida(MU, R, 4.0279, R + alvo[0], R + alvo[1], 0.2407, 0.0, 0.0)
    assert 0.0 <= dv - publicado < 0.010


def test_fuga_confere_com_bowles():
    esc = 4.0279 + (np.sqrt(2) - 1) * np.sqrt(MU / (R + 100))
    assert abs(esc - 5.4761) < 0.010


def test_deficit_de_rotacao():
    a = sf.dv_subida(MU, R, 4.0279, R + 100, R + 100, 0.24, 0.0, 0.0)
    b = sf.dv_subida(MU, R, 4.0279, R + 100, R + 100, 0.24, 60.0, 18.85)
    assert b - a == pytest.approx(0.24 * 0.5, rel=1e-12)


def test_inclinacao_abaixo_da_latitude_falha():
    with pytest.raises(ValueError):
        sf.dv_subida(MU, R, 4.0279, R + 380, R + 380, 0.24, 10.0, 18.85)


def test_descida_vertical():
    assert sf.dv_descida_vertical(0.08, 3.7e-3, 60.0) == pytest.approx(0.08 + 0.222, rel=1e-12)
