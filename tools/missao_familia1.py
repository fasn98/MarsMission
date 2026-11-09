"""Família 1 (Fabio, 2026-11-09), item 2: a menor estada em Marte em que o orbitador só elétrico fica pronto em órbita de
encontro antes do último lançamento do MAV, com a folga de 60 dias antes da conjunção (ADR 0018) e uma janela de retorno.

- Orbitador só elétrico: os tempos de results/etapa7.2/rotas_mav.yaml (rota B, "primeiro que fecha", calculado e NÃO
  verificado): pronto no encontro = partida da Terra + empuxo na ida + descida em espiral.
- Conjunções: ângulo Sol–Terra–Marte pelas efemérides (o mesmo critério de tools/comunicacao.py).
- MAV: lança depois que o orbitador está pronto e da chegada do lander, e ao menos 60 dias antes da conjunção seguinte.
- Retorno: a partida mais cedo é o lançamento do MAV + encontro + subida em espiral; o C3 balístico de Lambert nessa data
  (o mínimo na faixa de tempos de voo) mede a compatibilidade com a janela. O elétrico não usa esse C3: é só a referência
  de janela.
Saída: results/familia1/missao.yaml e .md

Uso: python tools/missao_familia1.py
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import comunicacao as cm  # noqa: E402
from orbital import ephemeris as eph  # noqa: E402
from orbital import lambert  # noqa: E402
from orbital import porkchop as pc  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402
from orbital.constantes import GM_SOL  # noqa: E402

SAIDA = RAIZ / "results" / "familia1"
D = dt.date.fromisoformat


def br(x, n=0):
    return f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def c3_minimo(partida, tofs):
    """(C3 mínimo em km²/s², tempo de voo em dias) da partida de Marte para a Terra, na faixa de tempos de voo."""
    t1 = eph.tdb_para_et(partida.isoformat() + "T00:00:00")
    s1 = pc.estado_corpo(eph.BARICENTRO_MARTE, t1)
    melhor = None
    for tof in tofs:
        t2 = t1 + tof * 86400.0
        s2 = pc.estado_corpo(eph.TERRA, t2)
        r = lambert.resolver(GM_SOL, s1[:3], s2[:3], t2 - t1)
        c3 = float(np.dot(r.v1 - s1[3:], r.v1 - s1[3:]))
        if melhor is None or c3 < melhor[0]:
            melhor = (c3, tof)
    return melhor


def main():
    fm, cc, op = ler("config/familia1.yaml")["missao"], ler("config/comunicacao.yaml"), ler("config/operacao_superficie.yaml")
    rb = ler("results/etapa7.2/rotas_mav.yaml")
    ref = rb["missao"]
    lim = v(cc["conjuncao"]["periodo_conjuncao_graus"])
    rec = int(v(cc["conjuncao"]["dias_de_recuperacao"]))
    folga = int(v(op["requisitos"]["folga_min_conjuncao_dias"]))
    passo = int(v(fm["passo_serie_dias"]))
    d, fim, serie = D(fm["inicio_busca"]["valor"]), D(fm["fim_busca"]["valor"]), []
    while d <= fim:
        s = d.isoformat() + "T00:00:00"
        rm, _ = eph.estado(eph.BARICENTRO_MARTE, s, eph.TERRA)
        rs, _ = eph.estado(eph.SOL, s, eph.TERRA)
        serie.append((d, cm.sep_e_distancia(rm, rs)[0]))
        d += dt.timedelta(days=passo)
    conj = [{"inicio": a, "fim": b, "dias": n} for a, b, n in cm.janelas(serie, lim)]
    tofs = list(range(int(fm["tof_retorno_dias"]["valor"][0]), int(fm["tof_retorno_dias"]["valor"][1]) + 1, int(v(fm["passo_tof_dias"]))))
    chegada_lander, partida_ref = D(ref["chegada"]), D(ref["partida"])
    casos = []
    for x in rb["rota_b"]:
        e = x["propulsores"]["XIPS-25"]["eletrico_primeiro_que_fecha"]
        pronto = D(e["pronto_no_encontro"])
        lanc0 = max(pronto, D(ref["lancamento_mav_mais_cedo"]), chegada_lander)
        # o MAV não lança durante a conjunção nem na recuperação; depois dela, o limite é a folga antes da seguinte
        for c in conj:
            if c["inicio"] - dt.timedelta(days=folga) <= lanc0 <= c["fim"] + dt.timedelta(days=rec):
                lanc0 = c["fim"] + dt.timedelta(days=rec)
        prox = next(c for c in conj if c["inicio"] > lanc0)
        lanc_tarde = prox["inicio"] - dt.timedelta(days=folga)
        partida = lanc0 + dt.timedelta(days=int(np.ceil(ref["encontro_dias"] + e["subida_dias"])))
        c3, tof = c3_minimo(partida, tofs)
        c3_ref, _ = c3_minimo(partida_ref, tofs)
        chegada_terra = partida + dt.timedelta(days=tof)
        casos.append({"altitude_km": x["altitude_km"], "n_ativos": e["n_ativos"], "potencia_kw": e["potencia_kw"], "orbitador_kg": e["orbitador_injetado_kg"],
                      "partida_terra": ref["partida_terra"], "empuxo_ida_dias": e["empuxo_ida_dias"], "descida_dias": e["descida_dias"], "subida_dias": e["subida_dias"],
                      "empuxo_volta_dias": e["empuxo_volta_dias"], "pronto_no_encontro": pronto, "lancamento_mav": lanc0, "lancamento_mav_mais_tarde": lanc_tarde,
                      "proxima_conjuncao": prox, "partida_marte": partida, "estada_dias": (partida - chegada_lander).days, "estada_referencia_dias": (partida_ref - chegada_lander).days,
                      "c3_partida_km2_s2": c3, "tof_balistico_dias": tof, "c3_partida_referencia_km2_s2": c3_ref, "chegada_terra": chegada_terra,
                      "missao_total_dias": (chegada_terra - D(ref["partida_terra"])).days, "mav_na_superficie_dias": (lanc0 - chegada_lander).days,
                      "conjuncoes_na_missao": [c for c in conj if D(ref["partida_terra"]) <= c["fim"] and c["inicio"] <= chegada_terra]})
    out = nativo({"gerado_por": "tools/missao_familia1.py", "status": "calculado, NÃO verificado (orbitador só elétrico)", "referencia": ref, "conjuncoes": conj,
                  "criterio_conjuncao_graus": lim, "folga_conjuncao_dias": folga, "recuperacao_dias": rec, "casos": casos})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "missao.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True, default_flow_style=None), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    ref = o["referencia"]
    md = ["# Família 1: missão de estada longa (gerado por tools/missao_familia1.py)", "",
          "**Calculado, NÃO verificado.** O orbitador só elétrico usa os tempos da rota B (results/etapa7.2/rotas_mav.md), com o trecho heliocêntrico quase circular e a margem de Δv, sem trajetória otimizada.", "",
          "## Conjunções solares (Sol–Terra–Marte ≤ " + br(o["criterio_conjuncao_graus"], 0) + "°)", "", "| Início | Fim | Dias |", "| :- | :- | -: |"]
    md += [f"| {c['inicio']} | {c['fim']} | {c['dias']} |" for c in o["conjuncoes"]]
    md += ["", "## Menor estada", "",
           f"Referência: chegada do lander em {ref['chegada']}, partida em {ref['partida']}; lançamento do MAV de {ref['lancamento_mav_mais_cedo']} a {ref['lancamento_mav_mais_tarde']}. O MAV lança no primeiro dia em que o orbitador está pronto, fora da conjunção, da recuperação de {o['recuperacao_dias']} dias e da folga de {o['folga_conjuncao_dias']} dias antes da conjunção seguinte (ADR 0018).", "",
           "| Encontro (km) | Propulsores | Orbitador (kg) | Pronto no encontro | Lançamento do MAV | Último lançamento possível | Partida de Marte | Estada (d) | Estada da referência (d) | C3 na partida (km²/s²) | C3 na partida da referência | Chegada à Terra (balístico) | Missão total (d) | MAV na superfície (d) |",
           "| -: | -: | -: | :- | :- | :- | :- | -: | -: | -: | -: | :- | -: | -: |"]
    for c in o["casos"]:
        md.append(f"| {br(c['altitude_km'])} | {c['n_ativos']} × XIPS-25, {br(c['potencia_kw'], 1)} kW | {br(c['orbitador_kg'])} | {c['pronto_no_encontro']} | {c['lancamento_mav']} | {c['lancamento_mav_mais_tarde']} | {c['partida_marte']} | {c['estada_dias']} | {c['estada_referencia_dias']} | {br(c['c3_partida_km2_s2'], 2)} | {br(c['c3_partida_referencia_km2_s2'], 2)} | {c['chegada_terra']} | {c['missao_total_dias']} | {c['mav_na_superficie_dias']} |")
    md += ["", "**Conjunção solar:** na referência, o MAV lança antes da conjunção de 2030. Aqui, o orbitador elétrico ainda desce em espiral durante ela, e o MAV lança depois, no intervalo até a conjunção seguinte. A espiral na conjunção pede operação autônoma do orbitador; o encontro e a subida em espiral ficam fora das duas conjunções.", "",
           "**O que falta para verificar o orbitador só elétrico:** (1) uma trajetória heliocêntrica de baixo empuxo com efemérides, nas datas de cada caso, no lugar do trecho quase circular com margem; (2) comparação dessa trajetória com um caso publicado de baixo empuxo Terra–Marte (por exemplo o ERO, [F260], ou um estudo com massas e tempos publicados); (3) a vida dos propulsores XIPS-25 com fonte (\"não achada\" em results/etapa7.2/rotas_mav.md). A espiral em Marte usa as leis de guiagem já verificadas da Etapa 3.2.", "",
           "**Retorno:** o C3 balístico na data de partida, contra o da partida da referência, mostra que a data ainda fica na janela. A volta do elétrico usa o tempo de empuxo da rota B, não esse C3; a chegada à Terra usa o tempo de voo balístico, como ordem de grandeza."]
    (SAIDA / "missao.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
