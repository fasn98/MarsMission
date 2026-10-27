"""Gera as missões candidatas Terra→Marte→Terra (Etapa 1.3).

Entradas: config/missoes.yaml (janelas, classes, critério), config/parametros_orbitais.yaml
(órbitas e interface de reentrada), config/premissas.yaml (P-006).
Saída: results/etapa1.3/missoes.yaml e results/etapa1.3/missoes.md

Uso: python tools/missoes.py
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
from orbital import missao as ms  # noqa: E402
from orbital import porkchop as pc  # noqa: E402

SAIDA = RAIZ / "results" / "etapa1.3"


def _ler(nome):
    return yaml.safe_load((RAIZ / "config" / nome).read_text(encoding="utf-8"))


def _valor(item):
    return float(item["valor"])


def parametros():
    po = _ler("parametros_orbitais.yaml")
    premissas = {p["nome"]: p["valor"] for p in _ler("premissas.yaml")["premissas"]}
    rt, rm = _valor(po["raio_terra_km"]), _valor(po["raio_marte_km"])
    leo = rt + _valor(po["leo_altitude_km"])
    orbitas = {}
    for nome, o in po["orbitas_marte"].items():
        orbitas[nome] = ms.Orbita(rm + float(o["periapse_alt_km"]["valor"]), rm + float(o["apoapse_alt_km"]["valor"]))
    return ms.Parametros(
        mu_terra=_valor(po["gm_terra"]), mu_marte=_valor(po["gm_marte"]), leo=ms.Orbita(leo, leo),
        orbitas_marte=orbitas, rp_aerocaptura_marte=rm + _valor(po["aerocaptura_periapse_alt_km"]),
        r_interface_terra=rt + _valor(po["interface_reentrada_alt_km"]),
        exclusao_180=float(premissas["exclusao_angulo_180_graus"]),
        v_reentrada_max=_valor(po["reentrada_max_km_s"]))


def _eixo(ini, fim, passo):
    return np.arange(spice.str2et(f"{ini} 00:00 TDB"), spice.str2et(f"{fim} 00:00 TDB") + 1, passo * pc.DIA)


def main():
    eph.carregar_kernels()
    cfg = _ler("missoes.yaml")
    p = parametros()
    crit = cfg["criterio_selecao"]
    passo = cfg["passo_dias"]
    candidatas = []
    for nome, jan in cfg["janelas"].items():
        et_dep = _eixo(*jan["partida_terra"], passo)
        et_M = _eixo(*jan["datas_em_marte"], passo)
        et_arr = _eixo(*jan["chegada_terra"], passo)
        ida = pc.calcular_grade(eph.TERRA, eph.BARICENTRO_MARTE, et_dep, et_M)
        volta = pc.calcular_grade(eph.BARICENTRO_MARTE, eph.TERRA, et_M, et_arr)
        for classe, c in cfg["classes"].items():
            r = ms.melhor_combinacao(p, ida, volta, c["permanencia_dias"], c.get("duracao_max_dias", 1e9),
                                     crit["orbita_marte"], crit["aerocaptura"], c.get("tof_max_dias", np.inf))
            if r is None:
                print(nome, classe, "sem solução")
                continue
            i, a, d, k = r[1]
            linha = ms.detalhar(p, et_dep[i], et_M[a], et_M[d], et_arr[k])
            borda = {"partida_terra": i in (0, len(et_dep) - 1), "chegada_marte": a in (0, len(et_M) - 1),
                     "partida_marte": d in (0, len(et_M) - 1), "chegada_terra": k in (0, len(et_arr) - 1)}
            linha.update({"id": f"{nome}-{classe}", "janela_ida": nome, "classe": classe,
                          "na_borda_do_dominio": [k_ for k_, v in borda.items() if v]})
            candidatas.append(linha)
            print(linha["id"], round(r[0], 3), linha["partida_terra"], linha["chegada_terra"],
                  round(linha["total_dias"]), linha["na_borda_do_dominio"])

    def arred(x):
        if isinstance(x, (float, np.floating)):
            return round(float(x), 4)
        if isinstance(x, dict):
            return {k: arred(v) for k, v in x.items()}
        return x

    # Envelope de dimensionamento (ADR 0004): regra em config/missao_referencia.yaml.
    ref = _ler("missao_referencia.yaml")
    regra = ref["envelope_dimensionamento"]
    chave = "dv_total_sem_aerocaptura_km_s" if regra["captura"] == "propulsiva" else "dv_total_com_aerocaptura_km_s"
    elegiveis = [c for c in candidatas if c["janela_ida"] in regra["janelas"] and c["classe"] in regra["classes"]]
    pior = max(elegiveis, key=lambda c: c["por_orbita_marte"][regra["orbita_marte"]][chave])
    envelope = {"regra": regra, "missao_que_define": pior["id"],
                "dv_total_km_s": round(float(pior["por_orbita_marte"][regra["orbita_marte"]][chave]), 4),
                "elegiveis": {c["id"]: round(float(c["por_orbita_marte"][regra["orbita_marte"]][chave]), 4) for c in elegiveis}}
    referencia = next(c for c in candidatas if c["id"] == ref["missao_referencia"]["id"])
    print("envelope:", envelope["missao_que_define"], envelope["dv_total_km_s"])

    SAIDA.mkdir(parents=True, exist_ok=True)
    out = {"gerado_por": "tools/missoes.py", "criterio_selecao": crit,
           "missao_referencia": {**ref["missao_referencia"], "datas": [referencia[k] for k in (
               "partida_terra", "chegada_marte", "partida_marte", "chegada_terra")]},
           "envelope_dimensionamento": envelope,
           "parametros": {"leo_raio_km": p.leo.rp, "orbitas_marte_km": {k: [v.rp, v.ra] for k, v in p.orbitas_marte.items()},
                          "rp_aerocaptura_marte_km": p.rp_aerocaptura_marte, "r_interface_terra_km": p.r_interface_terra,
                          "v_reentrada_max_km_s": p.v_reentrada_max},
           "candidatas": [arred(c) for c in candidatas]}
    (SAIDA / "missoes.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")

    br = lambda x, n=2: f"{x:.{n}f}".replace(".", ",")  # noqa: E731
    orbs = list(p.orbitas_marte)
    md = ["# Missões candidatas (gerado por tools/missoes.py)", "",
          f"Critério de seleção da trajetória: menor Δv propulsivo com órbita de Marte `{crit['orbita_marte']}`, "
          f"aerocaptura = {crit['aerocaptura']}. Reentrada limitada a {br(p.v_reentrada_max, 1)} km/s (P-011). "
          f"Δv em km/s, C3 em km²/s², durações em dias.", "",
          f"Missão de referência: **{ref['missao_referencia']['id']}**. Envelope de dimensionamento: "
          f"**{br(envelope['dv_total_km_s'])} km/s**, definido por {envelope['missao_que_define']}.", "",
          "| Missão | Partida Terra | Chegada Marte | Partida Marte | Chegada Terra | Ida | Em Marte | Volta | Total | C3 | DLA (°) | v∞ Marte | v∞ Terra | v reentrada | Δv saída Terra |",
          "| :- | :- | :- | :- | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
    for c in candidatas:
        md.append(f"| {c['id']} | {c['partida_terra']} | {c['chegada_marte']} | {c['partida_marte']} | {c['chegada_terra']} "
                  f"| {c['ida_dias']:.0f} | {c['em_marte_dias']:.0f} | {c['volta_dias']:.0f} | {c['total_dias']:.0f} "
                  f"| {br(c['c3_km2_s2'])} | {br(c['dla_graus'], 1)} | {br(c['vinf_chegada_marte_km_s'])} "
                  f"| {br(c['vinf_chegada_terra_km_s'])} | {br(c['v_reentrada_km_s'])} | {br(c['dv_saida_terra_km_s'])} |")
    for o in orbs:
        md += ["", f"## Órbita de Marte: {o}", "",
               "| Missão | Captura propulsiva | Captura c/ aerocaptura | Saída de Marte | Total sem aerocaptura | Total com aerocaptura |",
               "| :- | -: | -: | -: | -: | -: |"]
        for c in candidatas:
            q = c["por_orbita_marte"][o]
            md.append(f"| {c['id']} | {br(q['dv_captura_propulsiva_km_s'])} | {br(q['dv_captura_aerocaptura_km_s'])} "
                      f"| {br(q['dv_saida_marte_km_s'])} | {br(q['dv_total_sem_aerocaptura_km_s'])} | {br(q['dv_total_com_aerocaptura_km_s'])} |")
    (SAIDA / "missoes.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
