"""Baixa os kernels SPICE listados em config/kernels.yaml e confere o MD5.

Uso: python tools/fetch_kernels.py [config/kernels.yaml]
"""

from __future__ import annotations

import hashlib
import sys
import urllib.request
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]


def md5(caminho: Path) -> str:
    h = hashlib.md5()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def main() -> int:
    arquivo = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "config" / "kernels.yaml"
    cfg = yaml.safe_load((RAIZ / arquivo).read_text(encoding="utf-8"))
    diretorio = RAIZ / cfg["diretorio"]
    diretorio.mkdir(parents=True, exist_ok=True)
    falhas = 0
    for k in cfg["kernels"]:
        destino = diretorio / k["arquivo"]
        if not destino.exists() or md5(destino) != k["md5"]:
            print(f"baixando {k['url']}")
            urllib.request.urlretrieve(k["url"], destino)
        obtido = md5(destino)
        ok = obtido == k["md5"]
        falhas += not ok
        print(f"{'OK  ' if ok else 'FALHA'} {k['arquivo']} md5={obtido}")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
