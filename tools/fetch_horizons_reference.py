"""Baixa vetores de referência do JPL Horizons para testar as efemérides locais.

Grava a resposta bruta da API (sem edição) em tests/data/horizons/, um arquivo por
consulta. Os testes leem esses arquivos; nenhum número é digitado à mão.

Arquivos já existentes não são sobrescritos (para preservar a resposta original);
use --forcar para baixar de novo.

Uso: python tools/fetch_horizons_reference.py [--forcar]
"""

from __future__ import annotations

import sys
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "tests" / "data" / "horizons"
API = "https://ssd.jpl.nasa.gov/api/horizons.api"

SOL = "500@10"
BARICENTRO_MARTE = "500@4"

# (nome do arquivo, alvo Horizons, época TDB, centro)
CONSULTAS = [
    ("marte_bari_2028-01-01.txt", "4", "2028-01-01 00:00", SOL),
    ("marte_bari_2033-06-15.txt", "4", "2033-06-15 00:00", SOL),
    ("terra_2028-01-01.txt", "399", "2028-01-01 00:00", SOL),
    # Centro de Marte (499) com os mesmos parâmetros do baricentro (4): investigação
    # da distância baricentro–centro (docs/etapa1.1_efemerides.md).
    ("marte_centro_2028-01-01.txt", "499", "2028-01-01 00:00", SOL),
    ("marte_centro_2033-06-15.txt", "499", "2033-06-15 00:00", SOL),
    # Mesma grandeza obtida direto: centro de Marte relativo ao baricentro de Marte.
    ("marte_centro_rel_bari_2028-01-01.txt", "499", "2028-01-01 00:00", BARICENTRO_MARTE),
    ("marte_centro_rel_bari_2033-06-15.txt", "499", "2033-06-15 00:00", BARICENTRO_MARTE),
]


def consultar(alvo: str, tdb: str, centro: str) -> str:
    params = {
        "format": "text",
        "COMMAND": f"'{alvo}'",
        "OBJ_DATA": "'NO'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'VECTORS'",
        "CENTER": f"'{centro}'",
        "REF_PLANE": "'FRAME'",     # eixos do ICRF (equatorial), não eclíptica
        "REF_SYSTEM": "'ICRF'",
        "TLIST": f"'{tdb}'",
        "TIME_TYPE": "'TDB'",
        "VEC_TABLE": "'2'",
        "VEC_CORR": "'NONE'",       # geométrico
        "OUT_UNITS": "'KM-S'",
        "CSV_FORMAT": "'NO'",
        "VEC_LABELS": "'YES'",
    }
    url = f"{API}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=60) as r:
        return f"# URL: {url}\n" + r.read().decode("utf-8")


def main() -> None:
    forcar = "--forcar" in sys.argv[1:]
    DESTINO.mkdir(parents=True, exist_ok=True)
    for nome, alvo, tdb, centro in CONSULTAS:
        destino = DESTINO / nome
        if destino.exists() and not forcar:
            print(f"mantido {destino}")
            continue
        destino.write_text(consultar(alvo, tdb, centro), encoding="utf-8")
        print(f"gravado {destino}")


if __name__ == "__main__":
    main()
