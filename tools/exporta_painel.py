"""Grades dos porkchops (ida e volta) para o painel, no mesmo domínio e passo de tools/porkchop.py.

O painel não recalcula Lambert em grade (lento): lê estas grades de results/. Cada arquivo traz as datas (TDB),
C3 de partida, v∞ de chegada, tempo de voo e ângulo de transferência; na ida, também a DLA (graus, J2000).
Os mínimos marcados no painel vêm de results/etapa1.2/minimos_<sentido>.yaml (tools/porkchop.py), não daqui.
Saída: results/painel/porkchop_<sentido>_<janela>.npz (compactado) e results/painel/porkchops.yaml (índice)

Uso: python tools/exporta_painel.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import spiceypy as spice
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital import ephemeris as eph  # noqa: E402
from orbital import porkchop as pc  # noqa: E402

SAIDA = RAIZ / "results" / "painel"


def main():
    cfg = yaml.safe_load((RAIZ / "config" / "janelas.yaml").read_text(encoding="utf-8"))
    eph.carregar_kernels()
    SAIDA.mkdir(parents=True, exist_ok=True)
    indice = {"gerado_por": "tools/exporta_painel.py", "fonte_dos_dominios": "config/janelas.yaml", "sentidos": {}}
    for sentido in ("terra_marte", "marte_terra"):
        c = cfg[sentido]
        indice["sentidos"][sentido] = {"titulo": c["titulo"], "c3_max": c["c3_max"], "niveis_c3": c["niveis_c3"],
                                       "niveis_vinf": c["niveis_vinf"], "janelas": {}}
        for nome, jan in c["janelas"].items():
            passo = c["passo_dias"] * pc.DIA
            etp = np.arange(spice.str2et(f"{jan['partida'][0]} TDB"), spice.str2et(f"{jan['partida'][1]} TDB") + 1, passo)
            etc = np.arange(spice.str2et(f"{jan['chegada'][0]} TDB"), spice.str2et(f"{jan['chegada'][1]} TDB") + 1, passo)
            g = pc.calcular_grade(c["partida"], c["chegada"], etp, etc)
            arq = f"porkchop_{sentido}_{nome}.npz"
            dados = {"partida_tdb": np.array([eph.data_tdb(t) for t in etp]),
                     "chegada_tdb": np.array([eph.data_tdb(t) for t in etc]),
                     "c3_km2_s2": g.c3, "vinf_chegada_km_s": g.vinf_chegada, "tof_dias": g.tof_dias,
                     "angulo_transf_graus": g.angulo_transf}
            if g.dla_graus is not None:
                dados["dla_graus"] = g.dla_graus
            np.savez_compressed(SAIDA / arq, **dados)
            indice["sentidos"][sentido]["janelas"][nome] = {"arquivo": arq, "pontos": [len(etp), len(etc)]}
            print(sentido, nome, g.c3.shape)
    (SAIDA / "porkchops.yaml").write_text(yaml.safe_dump(indice, sort_keys=False, allow_unicode=True), encoding="utf-8")


if __name__ == "__main__":
    main()
