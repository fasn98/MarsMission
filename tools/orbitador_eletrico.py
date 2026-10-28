"""Etapa 3.3: orbitador químico × elétrico × híbrido.

(a) Químico: o atual (results/etapa2.5/arquitetura.yaml e results/etapa2.3/plataformas.yaml).
(c) Híbrido, concepção c2 (orbital.hibrido): captura química numa órbita circular de raio r_c, espiral elétrica
    tangencial (verificada na Etapa 3.2, ADR 0012) até a órbita circular de encontro r_e e de volta, saída química.
    Para cada propulsor de config/eletrica.yaml e cada número de propulsores ativos: varredura de r_e e r_c; em cada r_e,
    o r_c de menor massa total que cabe no tempo de cada janela (descida + encontro + subida ≤ estada); regra dos 5 %
    (ADR 0005) sobre r_e. Lander e MAV recalculados para a órbita de encontro circular (orbital.veiculos.lander).
    No ponto escolhido, a espiral quase circular é conferida contra a integração numérica (orbital.baixo_empuxo).
(b) Elétrico (cruzeiro e espiral): ordem de grandeza do tempo de empuxo do trecho heliocêntrico (solução quase
    circular Terra → Marte), comparado com as viagens da missão de referência. Calculado, NÃO verificado (ADR 0012).
Saída: results/etapa3.3/orbitador_eletrico.yaml e .md

Uso: python tools/orbitador_eletrico.py
"""

from __future__ import annotations

import copy
import math
import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital import baixo_empuxo as be  # noqa: E402
from orbital import dimensionamento as dm  # noqa: E402
from orbital import foguete as fg  # noqa: E402
from orbital import hibrido as hb  # noqa: E402
from orbital import lancamento as lc  # noqa: E402
from orbital import veiculos as ve  # noqa: E402
from orbital.config import ler, nativo, parametros, v  # noqa: E402
from orbital.constantes import GM_SOL, UA_KM  # noqa: E402
from orbital.massa_plataformas import mga, plataforma_orbitador  # noqa: E402

SAIDA = RAIZ / "results" / "etapa3.3"
DIA = 86400.0


def grade(x):
    return np.geomspace(x["min"], x["max"], int(x["pontos"]))


def sistema(nome, n, ecfg, pcfg):
    c = ecfg["propulsores"][nome]
    e = pcfg["orbitador"]["energia"]
    d_af = v(e["distancia_ua"]["semieixo"]) * (1 + v(e["distancia_ua"]["excentricidade"]))
    w = v(e["painel_w_kg_1ua"]) * v(e["fator_perdas_painel"]) / d_af ** 2
    t = v(ecfg["tanque"]["massa_seca_kg"]) / v(ecfg["tanque"]["xenonio_kg"])
    r = v(ecfg["residual_inutilizavel"])
    return hb.SistemaEletrico(n, n + int(v(ecfg["operacao"]["reservas"])), v(c["empuxo_n"]), v(c["isp_s"]), v(c["potencia_w"]),
                              v(c["massa_propulsor_kg"]), v(c["massa_ppu_kg"]), v(c["massa_alimentacao_kg"]), (t + r) / (1 - r), w,
                              mga("propulsao_fluidos", pcfg, "e1_medio"), mga("painel_solar", pcfg, "e1_medio"))


def main():
    p = parametros()
    po, dcfg, scfg = ler("config/parametros_orbitais.yaml"), ler("config/dimensionamento.yaml"), ler("config/superficie.yaml")
    pcfg, ecfg, cu, lcfg = ler("config/plataformas.yaml"), ler("config/eletrica.yaml"), ler("config/carga_util.yaml"), ler("config/lancadores.yaml")
    mu, R = p.mu_marte, v(po["raio_marte_km"])
    f = 1 + v(dcfg["margem_dv"])
    a_caso, jan, piores = dm.casos(dcfg, p)
    ms = ler("results/etapa1.3/missoes.yaml")
    cand = {c["id"]: c for c in ms["candidatas"]}
    janelas = [cand[w["missao"]] for w in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()]
    perdas = ler("results/etapa3.1/perdas_calculadas.yaml")["perda_km_s"]   # P-048
    orc_ins, orc_ret = dm.orcamento(piores["insercao_marte"], dcfg, p), dm.orcamento(piores["retorno"], dcfg, p)
    ate_marte, capsula, descartado = dm.carga(dcfg["caso_base"]["carga_util"], cu, float(dcfg["caso_base"]["acrescimo_capsula"]))
    est = dcfg["estagios"]
    isp_q, eps_i, eps_r = v(est["insercao_marte"]["isp_s"]), v(est["insercao_marte"]["fracao_estrutural"]), v(est["retorno"]["fracao_estrutural"])
    st = est["saida_terra"]
    dv_terra = f * dm.orcamento(a_caso, dcfg, p)["saida_terra"]
    t_enc = v(ecfg["operacao"]["tempo_encontro_dias"]) * DIA
    vz = ecfg["varredura"]
    alts_e, alts_c = grade(vz["encontro_alt_km"]["valor"]), grade(vz["captura_alt_km"]["valor"])

    def leo(m_inj):
        return fg.dimensionar_veiculo([fg.Estagio("saida_terra", v(st["isp_s"]), v(st["fracao_estrutural"]), [fg.Queima("saida_terra", dv_terra)])], m_inj)[0].massa_inicial

    # lander e plataforma do orbitador só dependem da órbita de encontro
    landers = {h: ve.lander(R + h, R + h, detalhe=True) for h in alts_e}
    plats = {h: plataforma_orbitador(pcfg, po, h, h) for h in alts_e}

    def ponto(se, h_e, h_c):
        r_e, r_c = R + h_e, R + h_c
        dv = {"correcoes_ida": f * orc_ins["correcoes_ida"],
              "captura": f * (max(hb.dv_hiperbole_circular(mu, w["vinf_chegada_marte_km_s"], r_c) for w in janelas) + perdas["captura_marte"]),
              "descida": f * hb.dv_circular(mu, r_c, r_e), "encontro": f * orc_ret["encontro_e_manutencao_marte"],
              "subida": f * hb.dv_circular(mu, r_e, r_c),
              "saida": f * (max(hb.dv_hiperbole_circular(mu, math.sqrt(w["c3l_partida_marte_km2_s2"]), r_c) for w in janelas) + perdas["saida_marte"]),
              "correcoes_volta": f * orc_ret["correcoes_volta"], "desvio": f * orc_ret["desvio_orbitador"]}
        carga_final = ate_marte - descartado - capsula + plats[h_e]
        m = hb.massas(dv, se, isp_q, eps_i, eps_r, carga_final, descartado, capsula)
        t_on_d, t_d, _, _ = hb.tempos_espiral(mu, R, r_c, r_e, m["massa_antes_descida_kg"], se)
        t_on_s, t_s, _, _ = hb.tempos_espiral(mu, R, r_e, r_c, m["massa_antes_subida_kg"], se)
        total_t = t_d + t_enc + t_s
        folgas = {w["id"]: w["em_marte_dias"] - total_t / DIA for w in janelas}
        vida = v(ecfg["propulsores"][se_nome[0]]["throughput_kg"]) if ecfg["propulsores"][se_nome[0]]["throughput_kg"] else None
        xe_por = m["eletrico"]["xenonio_kg"] / se.n_ativos
        ok = min(folgas.values()) >= 0 and (vida is None or xe_por <= vida)
        lan = landers[h_e]
        m_leo_o = leo(m["injetada_kg"])
        return {"encontro_alt_km": float(h_e), "captura_alt_km": float(h_c), "dv_km_s": dv, "massas": m,
                "plataforma_orbitador_kg": plats[h_e], "orbitador_injetado_kg": m["injetada_kg"], "orbitador_leo_kg": m_leo_o,
                "lander_injetado_kg": lan["injetada_kg"], "lander_leo_kg": lan["leo_modelo_kg"], "mav_kg": lan["mav_e_aquecimento_kg"],
                "dv_subida_mav_km_s": lan["dv_subida_mav_km_s"], "total_regra_iii_kg": m_leo_o + lan["leo_modelo_kg"],
                "tempo_descida_dias": t_d / DIA, "tempo_subida_dias": t_s / DIA, "tempo_empuxo_dias": (t_on_d + t_on_s) / DIA,
                "tempo_total_dias": total_t / DIA, "menor_folga_dias": min(folgas.values()),
                "xenonio_por_propulsor_kg": xe_por, "vida_kg": vida, "viavel": ok}

    resultados = {}
    se_nome = [None]
    for nome in ecfg["propulsores"]:
        se_nome[0] = nome
        por_n = []
        for n in range(1, int(vz["n_ativos_max"]["valor"]) + 1):
            se = sistema(nome, n, ecfg, pcfg)
            melhores = []
            for h_e in alts_e:
                viaveis = [x for x in (ponto(se, h_e, h_c) for h_c in alts_c if h_c > h_e) if x["viavel"]]
                if viaveis:
                    melhores.append(min(viaveis, key=lambda x: x["total_regra_iii_kg"]))
            if not melhores:
                por_n.append({"n_ativos": n, "viavel": False})
                continue
            mn_ = min(x["total_regra_iii_kg"] for x in melhores)
            esc = min((x for x in melhores if x["total_regra_iii_kg"] <= 1.05 * mn_), key=lambda x: x["encontro_alt_km"])
            por_n.append({"n_ativos": n, "viavel": True, "minimo_kg": mn_, "escolha": esc,
                          "potencia_eletrica_kw": se.potencia_total_w / 1e3, "empuxo_total_n": se.empuxo_total_n})
        primeiro = next((x for x in por_n if x["viavel"]), None)
        resultados[nome] = {"por_n": por_n, "n_minimo": primeiro["n_ativos"] if primeiro else None}

    # conferência da espiral quase circular contra a numérica, no ponto escolhido de cada propulsor (n mínimo)
    for nome, r in resultados.items():
        if r["n_minimo"] is None:
            continue
        esc = next(x for x in r["por_n"] if x["n_ativos"] == r["n_minimo"])["escolha"]
        se = sistema(nome, r["n_minimo"], ecfg, pcfg)
        m0 = esc["massas"]["massa_antes_descida_kg"]
        num = be.espiral(mu, R + esc["captura_alt_km"], R + esc["encontro_alt_km"], empuxo_n=se.empuxo_total_n, isp_s=se.isp_s, m0_kg=m0)
        t_on, _, dv_a, _ = hb.tempos_espiral(mu, R, R + esc["captura_alt_km"], R + esc["encontro_alt_km"], m0, se)
        r["conferencia_descida"] = {"dv_quase_circular_km_s": dv_a, "dv_numerico_km_s": num.dv, "diferenca_relativa": (num.dv - dv_a) / dv_a,
                                    "tempo_empuxo_quase_circular_dias": t_on / DIA, "tempo_empuxo_numerico_dias": num.duracao / DIA,
                                    "voltas": round(num.revolucoes, 1), "excentricidade_final": round(num.excentricidade_final, 4)}
        for veic, m in (("orbitador", esc["orbitador_injetado_kg"]), ("lander", esc["lander_injetado_kg"])):
            esc.setdefault("margens", {})[veic] = {nm: lc.pior_margem_a(nm, m, janelas, lcfg)[0] for nm in lcfg["lancadores"]}

    # (c1) captura química na elipse de 1 sol (periapse no encontro) e descida em arcos em torno do periapse
    um = p.orbitas_marte["eliptica_alta"]
    h_c1 = float(alts_e[0])
    vei_q = ve.veiculos(detalhe=True)[0]["orbitador_regra_iii"]
    m_pos_captura = next(e for e in vei_q["estagios"] if e["nome"] == "retorno")["massa_inicial_kg"]
    c1 = {"meio_arco_graus": float(vz["c1_meio_arco_graus"]["valor"]), "encontro_alt_km": h_c1, "apoapse_inicial_alt_km": um.ra - R,
          "massa_inicial_kg": m_pos_captura, "casos": []}
    for nome in ecfg["propulsores"]:
        for n in vz["c1_n_ativos"]["valor"]:
            se = sistema(nome, n, ecfg, pcfg)
            a = be.apoapse_por_arcos(mu, R + h_c1, um.ra, R + h_c1 * (1 + float(vz["c1_folga_apoapse"]["valor"])), se.empuxo_total_n,
                                     se.isp_s, m_pos_captura, c1["meio_arco_graus"])
            c1["casos"].append({"propulsor": nome, "n_ativos": n, "dv_km_s": a.dv_km_s, "tempo_empuxo_dias": a.tempo_empuxo_s / DIA,
                                "tempo_total_dias": a.tempo_total_s / DIA, "voltas": a.voltas,
                                "rp_final_alt_km": round(a.rp_final_km - R, 1), "ra_final_alt_km": round(a.ra_final_km - R, 1)})

    # (a) químico atual
    arq, pl = ler("results/etapa2.5/arquitetura.yaml"), ler("results/etapa2.3/plataformas.yaml")
    quimico = {"orbitador_injetado_kg": arq["orbitador"]["injetado_kg"], "lander_injetado_kg": arq["lander"]["injetado_kg"],
               "total_regra_iii_kg": pl["totais"]["base"]["regra_5pct"]["total_regra_iii_kg"],
               "orbita_encontro_km": arq["orbita_encontro_km"], "mav_kg": next(x["massa_kg"] for x in arq["lander"]["composicao"] if x["item"].startswith("MAV")),
               "dv_subida_mav_km_s": arq["lander"]["mav"]["dv_com_margem_km_s"] / f, "margens": arq["lancadores"]["margens_base"]}

    # (b) elétrico: tempo de empuxo do trecho heliocêntrico (ordem de grandeza), calculado, não verificado
    r_t, r_m = UA_KM, v(ler("config/mav_propulsao.yaml")["cruzeiro"]["distancia_marte_ua"]) * UA_KM
    dv_h = hb.dv_circular(GM_SOL, r_t, r_m)
    ref = cand[ler("config/missao_referencia.yaml")["missao_referencia"]["id"]]
    eletrico = {"dv_heliocentrico_km_s": dv_h, "ida_referencia_dias": ref["ida_dias"], "volta_referencia_dias": ref["volta_dias"], "casos": []}
    m0 = arq["orbitador"]["injetado_kg"]   # o orbitador químico atual, só como ordem de grandeza
    for nome in ecfg["propulsores"]:
        for n in vz["c1_n_ativos"]["valor"]:
            se = sistema(nome, n, ecfg, pcfg)
            t_on = m0 / se.vazao_kg_s * (1 - math.exp(-dv_h / (se.isp_s * fg.G0)))
            eletrico["casos"].append({"propulsor": nome, "n_ativos": n, "massa_inicial_kg": m0, "tempo_empuxo_ida_dias": t_on / DIA})

    out = {"gerado_por": "tools/orbitador_eletrico.py", "quimico": quimico, "hibrido_c2": resultados, "hibrido_c1": c1, "eletrico": eletrico,
           "tempo_encontro_dias": t_enc / DIA, "janelas": {w["id"]: w["em_marte_dias"] for w in janelas}}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "orbitador_eletrico.yaml").write_text(yaml.safe_dump(nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(out):
    br = lambda x, n=0: "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    pc = lambda x: "—" if x is None else f"{100 * x:+.0f} %".replace("-", "−")  # noqa: E731
    q = out["quimico"]
    md = ["# Orbitador químico × elétrico × híbrido (gerado por tools/orbitador_eletrico.py)", "",
          f"Estada em Marte por janela (dias): " + ", ".join(f"{k} {br(x)}" for k, x in out["janelas"].items())
          + f"; tempo de encontro {br(out['tempo_encontro_dias'])} d.", "",
          "## (a) Químico atual", "",
          f"Órbita de encontro {br(q['orbita_encontro_km'][0])} × {br(q['orbita_encontro_km'][1])} km; orbitador {br(q['orbitador_injetado_kg'])} kg; "
          f"lander {br(q['lander_injetado_kg'])} kg; MAV + aquecimento {br(q['mav_kg'])} kg (Δv de subida sem margem {br(q['dv_subida_mav_km_s'], 3)} km/s); "
          f"total (iii) {br(q['total_regra_iii_kg'])} kg.", "",
          "## (c) Híbrido c2: captura química em órbita circular, espiral elétrica até a órbita circular de encontro", ""]
    for nome, r in out["hibrido_c2"].items():
        md += [f"### {nome}", "", "| Ativos | Potência (kW) | Empuxo (N) | Viável | Encontro (km) | Captura (km) | Orbitador (kg) | Xenônio (kg) | Lander (kg) | MAV (kg) | Total (iii) (kg) | Tempo em Marte (d) | Menor folga (d) |",
               "| -: | -: | -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
        for x in r["por_n"]:
            if not x["viavel"]:
                md.append(f"| {x['n_ativos']} | | | não | | | | | | | | | |")
                continue
            e = x["escolha"]
            md.append(f"| {x['n_ativos']} | {br(x['potencia_eletrica_kw'], 1)} | {br(x['empuxo_total_n'], 2)} | sim | {br(e['encontro_alt_km'])} | {br(e['captura_alt_km'])} | "
                      f"{br(e['orbitador_injetado_kg'])} | {br(e['massas']['eletrico']['xenonio_kg'])} | {br(e['lander_injetado_kg'])} | {br(e['mav_kg'])} | "
                      f"{br(e['total_regra_iii_kg'])} | {br(e['tempo_total_dias'])} | {br(e['menor_folga_dias'])} |")
        md.append("")
        if r["n_minimo"] is not None:
            c = r["conferencia_descida"]
            e = next(x for x in r["por_n"] if x["n_ativos"] == r["n_minimo"])["escolha"]
            md += [f"Conferência da descida no ponto de {r['n_minimo']} ativos: Δv quase circular {br(c['dv_quase_circular_km_s'], 4)} km/s, numérico "
                   f"{br(c['dv_numerico_km_s'], 4)} km/s ({c['diferenca_relativa']:+.1e}); tempo de empuxo {br(c['tempo_empuxo_quase_circular_dias'], 1)} × "
                   f"{br(c['tempo_empuxo_numerico_dias'], 1)} d; {br(c['voltas'])} voltas; excentricidade final {br(c['excentricidade_final'], 4)}.".replace("e-", "e−"), "",
                   "Margens dos lançadores (injeção direta, pior janela): " + "; ".join(
                       f"{v_}: " + ", ".join(f"{k} {pc(m)}" for k, m in d.items()) for v_, d in e["margens"].items()), ""]
    c1 = out["hibrido_c1"]
    md += ["## (c) Híbrido c1: captura química na elipse de 1 sol, descida em arcos em torno do periapse", "",
           f"Só a descida, da elipse {br(c1['encontro_alt_km'])} × {br(c1['apoapse_inicial_alt_km'])} km até a circular, com empuxo contra a velocidade "
           f"em |ν| ≤ {br(c1['meio_arco_graus'])}° e voo livre no resto; massa inicial {br(c1['massa_inicial_kg'])} kg (a do orbitador químico depois "
           "da captura, só ordem de grandeza). Sem eclipse.", "",
           "| Propulsor | Ativos | Δv (km/s) | Tempo de empuxo (d) | Tempo decorrido (d) | Voltas | Periapse final (km) |", "| :- | -: | -: | -: | -: | -: | -: |"]
    md += [f"| {c['propulsor']} | {c['n_ativos']} | {br(c['dv_km_s'], 3)} | {br(c['tempo_empuxo_dias'])} | {br(c['tempo_total_dias'])} | {br(c['voltas'])} | "
           f"{br(c['rp_final_alt_km'])} |" for c in c1["casos"]]
    md.append("")
    el = out["eletrico"]
    md += ["## (b) Elétrico: trecho heliocêntrico (calculado, NÃO verificado)", "",
           "Massa inicial: a do orbitador químico atual (só ordem de grandeza; o elétrico leva outro sistema). "
           f"Δv quase circular da órbita da Terra à de Marte: {br(el['dv_heliocentrico_km_s'], 3)} km/s. Viagens da missão de referência: ida "
           f"{br(el['ida_referencia_dias'])} d, volta {br(el['volta_referencia_dias'])} d.", "",
           "| Propulsor | Ativos | Massa inicial (kg) | Tempo de empuxo só da ida (d) |", "| :- | -: | -: | -: |"]
    md += [f"| {c['propulsor']} | {c['n_ativos']} | {br(c['massa_inicial_kg'])} | {br(c['tempo_empuxo_ida_dias'])} |" for c in el["casos"]]
    (SAIDA / "orbitador_eletrico.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
