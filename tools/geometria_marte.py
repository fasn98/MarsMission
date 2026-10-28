"""Etapa 3.3: as espirais de baixo empuxo precisam de mudança de plano? (ADR 0012, item 2)

Para cada missão do envelope de dimensionamento (pior caso por janela, Etapa 1.3) e para a missão de referência:
declinação das assíntotas de chegada e de partida no equador de Marte (orbital.geometria), comparada com a inclinação
da órbita de encontro (config/superficie.yaml). Se |δ| ≤ i, a captura (ou a partida) pode ser feita já no plano de
encontro, escolhendo o plano de aproximação. Se não, o resto da inclinação é custeado por um impulso no apoapse da
órbita elíptica de 1 sol (onde a velocidade é menor), só como ordem de grandeza.
Saída: results/etapa3.3/geometria_planos.yaml e .md

Uso: python tools/geometria_marte.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital import geometria as ge  # noqa: E402
from orbital.config import ler, nativo, parametros, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa3.3"


def main():
    p = parametros()
    scfg = ler("config/superficie.yaml")["sitio_e_encontro"]
    i_enc, lat = v(scfg["inclinacao_encontro_graus"]), v(scfg["latitude_sitio_graus"])
    um = p.orbitas_marte["eliptica_alta"]
    v_apo = math.sqrt(p.mu_marte * (2 / um.ra - 2 / (um.rp + um.ra)))
    ms = ler("results/etapa1.3/missoes.yaml")
    cand = {c["id"]: c for c in ms["candidatas"]}
    ref = ler("config/missao_referencia.yaml")["missao_referencia"]["id"]
    ids = list(dict.fromkeys([w["missao"] for w in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()] + [ref]))
    linhas = []
    for i in ids:
        va, vd, et_c, et_p = ge.vinf_marte(cand[i])
        dc, dp = ge.declinacao_marte_graus(va, et_c), ge.declinacao_marte_graus(vd, et_p)
        falta_c, falta_p = max(0.0, abs(dc) - i_enc), max(0.0, abs(dp) - i_enc)
        linhas.append({"missao": i, "referencia": i == ref, "vinf_chegada_km_s": float(np.linalg.norm(va)),
                       "vinf_chegada_etapa1_3_km_s": cand[i]["vinf_chegada_marte_km_s"],
                       "declinacao_chegada_graus": dc, "declinacao_partida_graus": dp,
                       "excesso_chegada_graus": falta_c, "excesso_partida_graus": falta_p,
                       "dv_plano_no_apoapse_1sol_m_s": 1e3 * ge.mudanca_de_plano_kms(v_apo, max(falta_c, falta_p))})
    coplanar = all(x["excesso_chegada_graus"] == 0 and x["excesso_partida_graus"] == 0 for x in linhas)
    out = {"gerado_por": "tools/geometria_marte.py", "inclinacao_encontro_graus": i_enc, "latitude_sitio_graus": lat,
           "velocidade_apoapse_1sol_km_s": v_apo, "missoes": linhas, "todas_coplanares": coplanar,
           "maior_excesso_graus": max(max(x["excesso_chegada_graus"], x["excesso_partida_graus"]) for x in linhas)}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "geometria_planos.yaml").write_text(yaml.safe_dump(nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")

    br = lambda x, n=2: f"{x:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    md = ["# Plano das assíntotas em Marte (gerado por tools/geometria_marte.py)", "",
          f"Inclinação da órbita de encontro: {br(i_enc, 1)}° (config/superficie.yaml); latitude do sítio {br(lat, 2)}°. "
          "Declinação no equador de Marte (IAU_MARS, pck00011.tpc). A captura (partida) pode ser feita já no plano de "
          "encontro se |δ| ≤ i; o excesso é o que falta.", "",
          "| Missão | v∞ chegada (km/s) | δ chegada | δ partida | Excesso chegada | Excesso partida | Δv do excesso no apoapse de 1 sol |",
          "| :- | -: | -: | -: | -: | -: | -: |"]
    for x in linhas:
        md.append(f"| {x['missao']}{' (referência)' if x['referencia'] else ''} | {br(x['vinf_chegada_km_s'], 3)} | "
                  f"{br(x['declinacao_chegada_graus'])}° | {br(x['declinacao_partida_graus'])}° | {br(x['excesso_chegada_graus'])}° | "
                  f"{br(x['excesso_partida_graus'])}° | {br(x['dv_plano_no_apoapse_1sol_m_s'])} m/s |")
    md += ["", f"Todas coplanares com o plano de encontro: **{'sim' if coplanar else 'não'}**; maior excesso "
           f"{br(out['maior_excesso_graus'])}° (velocidade no apoapse de 1 sol: {br(v_apo, 3)} km/s).",
           "", "Não tratado: a orientação do nodo na partida, que depende da precessão da órbita durante a estada."]
    (SAIDA / "geometria_planos.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
