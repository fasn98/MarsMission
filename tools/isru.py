"""Etapa 2.2: estudo de troca do ISRU para o MAV, pela massa total na órbita baixa da Terra.

Opções (config/isru.yaml): O1 MAV sólido; O2 MAV LOX/CH4 com tudo da Terra; O3 MAV LOX/CH4 com O2 do
ISRU (MOXIE escalado) e CH4 da Terra. Para cada opção: massa pousada (MAV + plataforma P-017 + planta,
liquefação, armazenamento e fonte de energia quando houver), lander na órbita baixa (entrada direta,
P-018; lançamento separado) e total com o orbitador na órbita de encontro do ADR 0005 (regra iii e
missão A). Fonte de energia: MMRTG ou solar.
Saída: results/etapa2.2/isru.yaml e isru.md

Uso: python tools/isru.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(RAIZ / "src"), str(RAIZ / "tools")]

import dimensionamento as dm  # noqa: E402
from orbital import foguete as fg  # noqa: E402
from orbital import isru  # noqa: E402
from superficie import _ler, _v, lander_leo, mav  # noqa: E402

SAIDA = RAIZ / "results" / "etapa2.2"


def mav_loxch4(dv, scfg, icfg, eps):
    """MAV LOX/CH4 de dois estágios (mesma divisão de Δv do MAV sólido, P-019). (GLOM, propelente, seco)."""
    m = icfg["mav_loxch4"]
    f1 = _v(scfg["mav"]["fracao_dv_estagio_1"])
    isp = _v(m["isp_s"])
    e1 = fg.Estagio("loxch4_1", isp, eps, [fg.Queima("subida_1", f1 * dv)])
    e2 = fg.Estagio("loxch4_2", isp, eps, [fg.Queima("subida_2", (1 - f1) * dv)])
    r = fg.dimensionar_veiculo([e1, e2], _v(scfg["mav"]["carga_util_kg"]))
    prop = sum(s.propelente for s in r)
    return r[0].massa_inicial, prop, r[0].massa_inicial - prop


def zbo(icfg, m_ch4, m_lox):
    z = icfg["armazenamento_zbo"]
    a = _v(z["expoente"])
    p = m = 0.0
    if m_ch4 > 0:
        p += isru.escala(z["ch4"]["potencia_w"], m_ch4, _v(z["referencia_ch4_kg"]), a)
        m += isru.escala(z["ch4"]["massa_kg"], m_ch4, _v(z["referencia_ch4_kg"]), a)
    if m_lox > 0:
        p += isru.escala(z["lox"]["potencia_w"], m_lox, _v(z["referencia_lox_kg"]), a)
        m += isru.escala(z["lox"]["massa_kg"], m_lox, _v(z["referencia_lox_kg"]), a)
    return p, m


def energia(icfg, potencia_w, fonte):
    e = icfg["energia"]
    if potencia_w <= 0:
        return 0.0, ""
    if fonte == "mmrtg":
        r = e["mmrtg"]
        m, n = isru.massa_rtg(potencia_w, _v(r["potencia_inicio_w"]), _v(r["massa_kg"]), _v(r["degradacao_anual"]),
                              e["anos_ate_fim_da_estada"])
        return m, f"{n} MMRTG"
    s = e["solar"]
    return isru.escala(_v(s["massa_kg"]), potencia_w, _v(s["potencia_continua_w"]), _v(s["expoente"])), "solar"


def planta(icfg, taxa_kg_h, escala_planta):
    """(massa, potência W) da planta de O2 pela escala do MOXIE (base) ou do DRA (limite inferior)."""
    if escala_planta == "moxie":
        mx = icfg["moxie"]
        x_ref = _v(mx["producao_g_h"]) / 1000.0
        return (isru.escala(_v(mx["massa_kg"]), taxa_kg_h, x_ref, _v(mx["expoente_massa"])),
                isru.escala(_v(mx["potencia_w"]), taxa_kg_h, x_ref, _v(mx["expoente_potencia"])))
    d = icfg["planta_dra"]
    taxa_ref = _v(d["o2_kg"]) / (_v(icfg["producao"]["duracao_sols"]) * _v(icfg["producao"]["horas_por_sol"]))
    return isru.escala(_v(d["massa_kg"]), taxa_kg_h, taxa_ref, 1.0), isru.escala(1000 * _v(d["potencia_kw"]), taxa_kg_h, taxa_ref, 1.0)


def avaliar(opcao, fonte_energia, ctx, eps=None, escala_planta="moxie"):
    scfg, icfg, dcfg, p, a_caso, dv_mav, orbit = ctx
    plat = _v(scfg["lander"]["plataforma_superficie_kg"])
    razao = _v(scfg["lander"]["razao_pousada_entrada"]["entrada_direta"])
    of = _v(icfg["mav_loxch4"]["razao_of"])
    eps = _v(icfg["mav_loxch4"]["fracao_estrutural"]) if eps is None else eps
    reg = {"opcao": opcao, "fonte_energia": fonte_energia}
    if opcao == "O1":
        glom, _ = mav(dv_mav, scfg)
        pousada = glom + plat
        reg.update({"mav_glom_kg": glom, "extras_kg": 0.0, "potencia_w": 0.0})
    else:
        glom, prop, seco = mav_loxch4(dv_mav, scfg, icfg, eps)
        m_ox, m_ch4 = isru.divisao_of(prop, of)
        reg.update({"mav_glom_kg": glom, "mav_propelente_kg": prop, "mav_seco_kg": seco, "o2_kg": m_ox, "ch4_kg": m_ch4,
                    "fracao_o2": m_ox / prop})
        if opcao == "O2":
            p_zbo, m_zbo = zbo(icfg, m_ch4, m_ox)
            potencia, extras = p_zbo, m_zbo
            pousado_mav = glom
            reg.update({"zbo_w": p_zbo, "zbo_kg": m_zbo})
        else:
            horas = _v(icfg["producao"]["duracao_sols"]) * _v(icfg["producao"]["horas_por_sol"])
            taxa = m_ox / horas
            m_pl, p_pl = planta(icfg, taxa, escala_planta)
            lq = icfg["liquefacao_o2"]
            p_lq = isru.escala(_v(lq["potencia_w"]), taxa, _v(lq["taxa_kg_h"]), _v(lq["expoente"]))
            m_lq = isru.escala(_v(lq["massa_kg"]), taxa, _v(lq["taxa_kg_h"]), _v(lq["expoente"]))
            p_zbo, m_zbo = zbo(icfg, m_ch4, m_ox)
            potencia = p_pl + p_lq + p_zbo
            extras = m_pl + m_lq + m_zbo
            pousado_mav = glom - m_ox                  # MAV pousa com CH4 e tanques de O2 vazios
            reg.update({"taxa_o2_kg_h": taxa, "planta_kg": m_pl, "planta_w": p_pl, "liquefacao_kg": m_lq,
                        "liquefacao_w": p_lq, "zbo_w": p_zbo, "zbo_kg": m_zbo, "o2_economizado_kg": m_ox,
                        "escala_planta": escala_planta})
        m_en, desc = energia(icfg, potencia, fonte_energia)
        pousada = pousado_mav + plat + extras + m_en
        reg.update({"extras_kg": extras, "potencia_w": potencia, "energia_kg": m_en, "energia": desc})
    chegada = pousada / razao
    lander = lander_leo(chegada, scfg, dcfg, p, a_caso)
    reg.update({"massa_pousada_kg": pousada, "lander_orbita_baixa_kg": lander,
                "total_regra_iii_kg": orbit["regra_iii"] + lander, "total_missao_A_kg": orbit["missao_A"] + lander})
    return {k: (round(v, 3) if isinstance(v, float) else v) for k, v in reg.items()}


def main():
    scfg = _ler("config/superficie.yaml")
    icfg = _ler("config/isru.yaml")
    dcfg = _ler("config/dimensionamento.yaml")
    p = dm.parametros()
    a_caso, _, _ = dm.casos(dcfg, p)
    vz = _ler("results/etapa2.1/varredura_encontro_rp300.yaml")
    esc = vz["escolha"]
    ponto = next(x for x in vz["pontos"] if x["apoapse_alt_km"] == esc["apoapse_alt_km"])
    orbit = {"regra_iii": ponto["quimico"]["orbitador_regra_iii_kg"], "missao_A": ponto["quimico"]["orbitador_missao_A_kg"]}
    dv_mav = (1 + _v(dcfg["margem_dv"])) * ponto["dv_mav_km_s"]
    ctx = (scfg, icfg, dcfg, p, a_caso, dv_mav, orbit)

    base = [avaliar("O1", "-", ctx)]
    for fonte in ("mmrtg", "solar"):
        base += [avaliar("O2", fonte, ctx), avaliar("O3", fonte, ctx)]
    sens = []
    for fonte in ("mmrtg", "solar"):
        sens.append(("O3, planta pela escala do DRA (limite inferior)", avaliar("O3", fonte, ctx, escala_planta="dra")))
        for op in ("O2", "O3"):
            sens.append((f"{op}, ε do MAV LOX/CH4 = 0,114 (Bowles, veículo de ~2 t)",
                         avaliar(op, fonte, ctx, eps=_v(icfg["mav_loxch4"]["fracao_estrutural_alternativa"]))))
    out = {"gerado_por": "tools/isru.py", "orbita_encontro_apoapse_km": esc["apoapse_alt_km"], "dv_mav_com_margem_km_s": round(dv_mav, 4),
           "orbitador_kg": orbit, "base": base, "sensibilidade": [{"caso": c, **r} for c, r in sens]}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "isru.yaml").write_text(yaml.safe_dump(dm._nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")

    br = lambda x, n=0: "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    md = ["# Estudo de troca do ISRU (gerado por tools/isru.py)", "",
          f"Subida até 300 × {br(esc['apoapse_alt_km'])} km (ADR 0005), Δv com margem {br(dv_mav, 3)} km/s, carga útil 16 kg. "
          f"Orbitador na órbita baixa: {br(orbit['regra_iii'])} kg (regra iii) / {br(orbit['missao_A'])} kg (missão A). Massas em kg, potência em W.", "",
          "| Opção | Energia | MAV (decolagem) | O2 do MAV (fração) | CH4 | Planta + liquefação + armazenamento | Potência | Fonte de energia | Massa pousada | Lander na órbita baixa | **Total (iii)** | Total (A) |",
          "| :- | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: |"]

    def linha(r, rot=None):
        o2 = f"{br(r.get('o2_kg'))} ({br(100 * r['fracao_o2'], 1)} %)" if "o2_kg" in r else "—"
        md.append(f"| {rot or r['opcao']} | {r.get('energia') or r['fonte_energia']} | {br(r['mav_glom_kg'])} | {o2} | {br(r.get('ch4_kg'))} | "
                  f"{br(r['extras_kg'])} | {br(r['potencia_w'])} | {br(r.get('energia_kg'))} | {br(r['massa_pousada_kg'])} | "
                  f"{br(r['lander_orbita_baixa_kg'])} | **{br(r['total_regra_iii_kg'])}** | {br(r['total_missao_A_kg'])} |")

    for r in base:
        linha(r)
    md += ["", "## Sensibilidade", "", md[4], md[5]]
    for c, r in sens:
        linha(r, f"{c}")
    (SAIDA / "isru.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
