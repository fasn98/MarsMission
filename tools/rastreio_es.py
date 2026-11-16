"""Roda uma ferramenta registrando os arquivos de results/ que ela abre para leitura e para escrita (audit hook do
Python), para o mapa de dependências da regeneração (tools/mapa_regeneracao.py).

Uso: python tools/rastreio_es.py <saida.json> <ferramenta.py> [argumentos...]
"""

from __future__ import annotations

import json
import os
import runpy
import sys
from pathlib import Path


def main():
    saida, ferramenta, args = sys.argv[1], sys.argv[2], sys.argv[3:]
    raiz = Path.cwd().resolve()
    lidos, gravados = set(), set()

    def gancho(evento, a):
        if evento != "open" or not a or not isinstance(a[0], (str, bytes, os.PathLike)):
            return
        try:
            p = Path(os.fsdecode(a[0])).resolve()
            rel = p.relative_to(raiz)
        except (ValueError, OSError):
            return
        if not rel.parts or rel.parts[0] != "results":
            return
        modo = a[1] if len(a) > 1 and isinstance(a[1], str) else "r"
        flags = a[2] if len(a) > 2 and isinstance(a[2], int) else 0
        escreve = any(c in modo for c in "wax+") or bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
        (gravados if escreve else lidos).add(str(rel))
    sys.addaudithook(gancho)
    sys.argv = [ferramenta, *args]
    sys.path.insert(0, str(Path(ferramenta).resolve().parent))
    try:
        runpy.run_path(ferramenta, run_name="__main__")
    finally:
        Path(saida).write_text(json.dumps({"ferramenta": " ".join([ferramenta, *args]), "lidos": sorted(lidos - gravados), "gravados": sorted(gravados)}), encoding="utf-8")


if __name__ == "__main__":
    main()
