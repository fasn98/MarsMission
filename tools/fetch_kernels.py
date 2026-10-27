"""Baixa os kernels SPICE listados em config/kernels.yaml e confere o MD5 (rotina em src/orbital/kernels.py).

Uso: python tools/fetch_kernels.py [config/kernels.yaml]
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital import kernels  # noqa: E402


def main() -> int:
    arquivo = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "config" / "kernels.yaml"
    falhas = 0
    for r in kernels.baixar(RAIZ / arquivo, RAIZ):
        falhas += not r["ok"]
        print(f"{'OK  ' if r['ok'] else 'FALHA'} {r['arquivo']} md5={r['md5_obtido']}")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
