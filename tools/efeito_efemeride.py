"""Efeito da efeméride nas grandezas tabeladas pelo JPL 82-43 Parte 5 (efeméride DE-118).

A DE118 não é distribuída pelo NAIF. A DE200 é a DE118 girada para o equador e equinócio
J2000 (Standish, 1990, A&A 233:252 — docs/fontes.md [F15]). C3L e VHP são normas e não
dependem da rotação do referencial, então DE200 representa a DE118 para este fim.
Compara C3L e VHP nas datas das tabelas calculados com DE440 (de440s.bsp) e com DE200.
Saída: results/etapa1.2/efeito_efemeride_de200.yaml

Uso: python tools/efeito_efemeride.py   (requer config/kernels_verificacao.yaml baixado)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import spiceypy as spice
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital import lambert  # noqa: E402
from orbital.constantes import GM_SOL  # noqa: E402


def calcular(spk, linhas):
    spice.kclear()
    spice.furnsh(str(RAIZ / "data/kernels/naif0012.tls"))
    spice.furnsh(str(spk))
    res = []
    for r in linhas:
        e1 = spice.str2et(f"{r['partida']} 00:00 TDB")
        e2 = spice.str2et(f"{r['chegada']} 00:00 TDB")
        s1 = np.array(spice.spkezr("4", e1, "ECLIPJ2000", "NONE", "10")[0])
        s2 = np.array(spice.spkezr("3", e2, "ECLIPJ2000", "NONE", "10")[0])
        sol = lambert.resolver(GM_SOL, s1[:3], s2[:3], e2 - e1)
        d1 = sol.v1 - s1[3:]
        res.append((float(d1 @ d1), float(np.linalg.norm(sol.v2 - s2[3:]))))
    return res


def main():
    ref = yaml.safe_load((RAIZ / "tests/data/jpl8243p5_minimos.yaml").read_text(encoding="utf-8"))["janelas"]
    linhas = [dict(jan[k], janela=a, linha=k) for a, jan in ref.items() for k in ("c3l_1", "c3l_2", "vhp_1", "vhp_2")]
    novo = calcular(RAIZ / "data/kernels/de440s.bsp", linhas)
    antigo = calcular(RAIZ / "data/kernels/de200.bsp", linhas)
    saida = {"gerado_por": "tools/efeito_efemeride.py", "comparacao": "DE440 (de440s.bsp) vs DE200",
             "chegada": "baricentro Terra–Lua (3)", "linhas": []}
    rel_c3, rel_v = [], []
    for r, (c3a, va), (c3b, vb) in zip(linhas, novo, antigo):
        saida["linhas"].append({"janela": r["janela"], "linha": r["linha"],
                                "c3l_rel": (c3a - c3b) / c3b, "vhp_rel": (va - vb) / vb})
        rel_c3.append(abs((c3a - c3b) / c3b))
        rel_v.append(abs((va - vb) / vb))
    saida["max_abs_rel_c3l"] = float(max(rel_c3))
    saida["max_abs_rel_vhp"] = float(max(rel_v))
    out = RAIZ / "results/etapa1.2/efeito_efemeride_de200.yaml"
    out.write_text(yaml.safe_dump(saida, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print("max |rel| C3L:", saida["max_abs_rel_c3l"], " VHP:", saida["max_abs_rel_vhp"])


if __name__ == "__main__":
    main()
