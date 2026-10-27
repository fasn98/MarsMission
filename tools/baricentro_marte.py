"""Gera results/etapa1.1/baricentro_marte.yaml: distância baricentro–centro de Marte.

Fontes: valor físico de orbital.marte ([F7], [F8]); vetores do Horizons em tests/data/horizons/.
Uso: python tools/baricentro_marte.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(RAIZ / "src"), str(RAIZ / "tests")]

from orbital import marte  # noqa: E402
from test_ephemeris import DADOS, ler_horizons  # noqa: E402

SAIDA = RAIZ / "results" / "etapa1.1" / "baricentro_marte.yaml"


def main() -> None:
    minimo, maximo = marte.faixa_distancia_baricentro_centro_km()
    resultado = {
        "gerado_por": "tools/baricentro_marte.py",
        "fisico_m": {
            "contribuicao_fobos": float(marte.deslocamento_baricentro_km(marte.GM_FOBOS, marte.A_FOBOS) * 1e3),
            "contribuicao_deimos": float(marte.deslocamento_baricentro_km(marte.GM_DEIMOS, marte.A_DEIMOS) * 1e3),
            "faixa": [float(minimo * 1e3), float(maximo * 1e3)],
        },
        "horizons_m": {},
    }
    for epoca in ["2028-01-01", "2033-06-15"]:
        _, r_c, _ = ler_horizons(DADOS / f"marte_centro_{epoca}.txt")
        _, r_b, _ = ler_horizons(DADOS / f"marte_bari_{epoca}.txt")
        _, r_d, _ = ler_horizons(DADOS / f"marte_centro_rel_bari_{epoca}.txt", centro="Mars Barycenter (4)")
        resultado["horizons_m"][epoca] = {
            "r499_menos_r4_heliocentrico": [float(x) for x in (r_c - r_b) * 1e3],
            "norma_heliocentrico": float(np.linalg.norm(r_c - r_b) * 1e3),
            "r499_rel_4_direto": [float(x) for x in r_d * 1e3],
            "norma_direto": float(np.linalg.norm(r_d) * 1e3),
            "diferenca_entre_os_dois": float(np.linalg.norm((r_c - r_b) - r_d) * 1e3),
        }
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(yaml.safe_dump(resultado, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(SAIDA.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
