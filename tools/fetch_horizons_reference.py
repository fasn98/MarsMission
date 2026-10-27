"""Baixa vetores de referência do JPL Horizons para testar as efemérides locais.

Grava a resposta bruta da API (sem edição) em tests/data/horizons/, um arquivo por
consulta. Os testes leem esses arquivos; nenhum número é digitado à mão.

Uso: python tools/fetch_horizons_reference.py
"""

from __future__ import annotations

import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "tests" / "data" / "horizons"
API = "https://ssd.jpl.nasa.gov/api/horizons.api"

# (nome do arquivo, alvo Horizons, época TDB)
CONSULTAS = [
    ("marte_bari_2028-01-01.txt", "4", "2028-01-01 00:00"),
    ("marte_bari_2033-06-15.txt", "4", "2033-06-15 00:00"),
    ("terra_2028-01-01.txt", "399", "2028-01-01 00:00"),
]


def consultar(alvo: str, tdb: str) -> str:
    params = {
        "format": "text",
        "COMMAND": f"'{alvo}'",
        "OBJ_DATA": "'NO'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'VECTORS'",
        "CENTER": "'500@10'",       # centro do Sol
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
    DESTINO.mkdir(parents=True, exist_ok=True)
    for nome, alvo, tdb in CONSULTAS:
        (DESTINO / nome).write_text(consultar(alvo, tdb), encoding="utf-8")
        print(f"gravado {DESTINO / nome}")


if __name__ == "__main__":
    main()
