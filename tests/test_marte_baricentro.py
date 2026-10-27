"""Distância entre o centro de Marte (499) e o baricentro do sistema marciano (4).

Compara três coisas:
- o valor físico esperado, calculado por orbital.marte a partir de GM (MAR099) e dos
  elementos médios de Fobos e Deimos (docs/fontes.md [F7], [F8]);
- a diferença entre as consultas heliocêntricas do Horizons para 499 e para 4, feitas com
  os mesmos parâmetros;
- a consulta direta do Horizons para 499 relativo a 4.
"""

from __future__ import annotations

import numpy as np
import pytest

from orbital import marte
from test_ephemeris import DADOS, ler_horizons

EPOCAS = ["2028-01-01", "2033-06-15"]


def _incerteza_impressao_km(*vetores: np.ndarray) -> float:
    """Pior caso do erro de arredondamento ao subtrair vetores impressos com 16 dígitos.

    O Horizons imprime 16 algarismos significativos (d.ddddddddddddddd E±XX). O
    arredondamento de cada componente é de até 0,5e-15 * |x|.
    """
    return float(sum(np.linalg.norm(0.5e-15 * np.abs(v)) for v in vetores))


@pytest.mark.parametrize("epoca", EPOCAS)
def test_diferenca_heliocentrica_igual_a_consulta_direta(epoca):
    _, r_centro, _ = ler_horizons(DADOS / f"marte_centro_{epoca}.txt")
    _, r_bari, _ = ler_horizons(DADOS / f"marte_bari_{epoca}.txt")
    _, r_direto, _ = ler_horizons(DADOS / f"marte_centro_rel_bari_{epoca}.txt",
                                  centro="Mars Barycenter (4)")
    diferenca = r_centro - r_bari
    assert np.linalg.norm(diferenca - r_direto) <= _incerteza_impressao_km(r_centro, r_bari, r_direto)


@pytest.mark.parametrize("epoca", EPOCAS)
def test_distancia_baricentro_centro_dentro_da_faixa_fisica(epoca):
    _, r_direto, _ = ler_horizons(DADOS / f"marte_centro_rel_bari_{epoca}.txt",
                                  centro="Mars Barycenter (4)")
    minimo, maximo = marte.faixa_distancia_baricentro_centro_km()
    assert minimo <= np.linalg.norm(r_direto) <= maximo


def test_gm_do_sistema_igual_a_soma_dos_corpos():
    """Consistência interna do cabeçalho MAR099: sistema = Marte + Fobos + Deimos."""
    gm_marte = 4.282837485735626e04  # [F7] Mars 499
    soma = gm_marte + marte.GM_FOBOS + marte.GM_DEIMOS
    assert soma == pytest.approx(marte.GM_SISTEMA_MARTE, rel=1e-15)
