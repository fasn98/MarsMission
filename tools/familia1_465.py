"""Família 1 com o aeroshell de 4,65 m (Fabio, 2026-11-10).

(a) Encaixe da cápsula de 4,65 m (forma SRL-A) e da de 4,5 m no Vulcan com a coifa longa de 21,3 m, nas duas leituras da
    figura simplificada de [F80] (contorno reto e Ø menor desde a interface, a regra de tools/cad_parametros.py), com o
    adaptador da P-097.
(b) Comprimento máximo do MAV deitado no aeroshell de 4,65 m, com e sem deck, por diâmetro (results/etapa7.2/mav_arranjo).
(c) Folga dos MAVs da família 1 (results/familia1/mavs.yaml) e da base da Fase 2 (results/etapa7.2/rotas_mav.yaml).
(d) Massa por área com 4,65 m, contra a do Mars 2020.
(e) Margem do lander no Vulcan VC4 e VC6 com a coifa longa: a capacidade publicada da coifa padrão (limite otimista) e,
    com a perda da coifa longa da P-112 (NÃO VALIDADA), a estimativa.
(f) Sólido com a fração estrutural da P-019 no lugar da P-111, com a margem da P-014: sensibilidade.
Saída: results/familia1/aeroshell_465.yaml e .md

Uso: python tools/familia1_465.py
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
sys.path.insert(0, str(RAIZ / "tools"))

import cad_parametros as cp  # noqa: E402
import envelope_arranjo as ea  # noqa: E402
import mav_familia1 as mf  # noqa: E402
import rota_a_dimensiona as rad  # noqa: E402
import subida_mav as sm  # noqa: E402
from orbital import dimensionamento as dm  # noqa: E402
from orbital import lancamento as lc  # noqa: E402
from orbital import subida as sb  # noqa: E402
from orbital import veiculos as ve  # noqa: E402
from orbital.config import ler, nativo, parametros, v  # noqa: E402

SAIDA = RAIZ / "results" / "familia1"
POL = 0.0254   # [F112] Apêndice B.8, PDF p. 62: polegada em metros
br, sg = sm.br, sm.sg


def main():
    cad, fc, scfg, dcfg = ler("config/cad.yaml"), ler("config/familia1.yaml"), ler("config/superficie.yaml"), ler("config/dimensionamento.yaml")
    a4 = fc["aeroshell_465"]
    forma = a4["forma"]
    par = ler("results/etapa7.2/parametros.yaml")
    h_cz = par["conferencias"]["lander_vulcan"]["altura_estagio_cruzeiro_m"]
    m_ad, h_ad = lc.adaptador_p097()
    cl = a4["coifa_longa_vulcan"]
    hs = [(s - cl["estacao_interface_pol"]) * POL for s in cl["estacao_pol"]]
    rs = [d / 2000 for d in cl["diametro_mm"]]
    leituras = {"contorno reto": (hs, rs), "Ø menor desde a interface": (hs, [rs[1], rs[1]] + rs[2:])}
    # (a) encaixe nas duas leituras, nos vértices do perfil da cápsula, com o veículo h_ad acima do plano da interface
    encaixe = []
    for f in (forma, "srl_c", "msl_m2020"):
        c = cad["capsulas"][f]
        xs, rr = [float(x) for x in c["x_m"]], [float(x) for x in c["r_m"]]
        L = xs[-1]
        for nome, perf in leituras.items():
            vert = min(ea.raio_envelope(perf, h_cz + h_ad + (L - x)) - r for x, r in zip(xs, rr))
            grade = min(ea.raio_envelope(perf, h_cz + h_ad + (L - x)) - cp.capsula_raio((xs, rr), x) for x in np.linspace(0, L, 400))
            encaixe.append({"forma": f, "diametro_m": 2 * max(rr), "leitura": nome, "folga_vertices_m": vert, "folga_grade_m": grade,
                            "topo_capsula_m": h_cz + h_ad + L, "topo_envelope_m": hs[-1]})
    # (b) comprimento máximo do MAV deitado na forma da cápsula de 4,65 m
    ma = ler("results/etapa7.2/mav_arranjo.yaml")
    lim = {}
    for c in ma["casos"]:
        est = {e["estacao"]: e for e in c["formas"][forma]}
        deck = next(k for k in est if "P-094" in k)
        lim[c["diametro_m"]] = {"sem_deck_m": c["comprimento_m"] + 2 * est["ombro"]["deitado_folga_m"], "com_deck_m": c["comprimento_m"] + 2 * est[deck]["deitado_folga_m"]}
    m = rad.modelo()
    lim45 = {d: {"sem_deck_m": m.lim_ombro[d], "com_deck_m": m.lim_deck[d]} for d in lim}
    # (c) folgas dos MAVs da família 1 e da base
    mv = ler("results/familia1/mavs.yaml")
    rb = ler("results/etapa7.2/rotas_mav.yaml")
    d_s, d_h = mv["limites"]["solido"]["diametro_m"], mv["limites"]["hipergolico"]["diametro_m"]
    linhas = []

    def folgas(L, d):
        return {k: (lim[d][k] - L) / 2 for k in ("sem_deck_m", "com_deck_m")}, {k: (lim45[d][k] - L) / 2 for k in ("sem_deck_m", "com_deck_m")}
    for x in mv["solido"] + mv["hipergolico"]:
        if not x.get("fecha"):
            linhas.append({"rotulo": x["rotulo"], "fecha": False})
            continue
        Ls = [c["comprimento_m"] for c in x["comprimentos"]] if "comprimentos" in x else [x["comprimento_m"]]
        d = d_s if x["tipo"] == "solido" else d_h
        f465 = [folgas(L, d)[0] for L in Ls]
        f45 = [folgas(L, d)[1] for L in Ls]
        linhas.append({"rotulo": x["rotulo"], "fecha": True, "diametro_m": d, "comprimento_m": [min(Ls), max(Ls)],
                       "folga_465": {k: [min(f[k] for f in f465), max(f[k] for f in f465)] for k in ("sem_deck_m", "com_deck_m")},
                       "folga_45": {k: [min(f[k] for f in f45), max(f[k] for f in f45)] for k in ("sem_deck_m", "com_deck_m")},
                       "glom_kg": x["glom_kg"], "tipo": x["tipo"], "altitude_km": x["altitude_km"]})
    for k_ in ("base", "base_real"):
        b = rb[k_]
        f465, f45 = folgas(b["comprimento_m"], b["diametro_m"])
        linhas.append({"rotulo": "Fase 2: " + b["rotulo"], "fecha": True, "diametro_m": b["diametro_m"], "comprimento_m": [b["comprimento_m"]] * 2,
                       "folga_465": {k: [f465[k]] * 2 for k in f465}, "folga_45": {k: [f45[k]] * 2 for k in f45}, "glom_kg": b["glom_kg"],
                       "lander_injetado_rotas_mav_kg": b["lander_injetado_kg"], "tipo": "base"})
    # (e) massa injetada e margem no Vulcan com a coifa longa
    po = ler("config/parametros_orbitais.yaml")
    R = v(po["raio_marte_km"])
    p = parametros()
    a_caso, _, _ = dm.casos(dcfg, p)
    razao = v(scfg["lander"]["razao_pousada_entrada"]["entrada_direta"])
    hip_lan = {}
    for x in mv["hipergolico"]:
        if x.get("convergiu") and "com a margem" in x["rotulo"]:
            s2 = copy.deepcopy(scfg)
            s2["subida"]["dv_100x100_km_s"]["valor"] = x["dv_100x100_m_s"] / 1000.0
            hip_lan[x["altitude_km"]] = ve.lander(R + x["altitude_km"], R + x["altitude_km"], scfg=s2, detalhe=True)
    ob = rb["base"]["orbita_km"]
    lan_b = ve.lander(R + ob[0], R + ob[1], detalhe=True)
    m_srl = v(cad["aeroshell"]["opcoes"]["srl_duplo"]["massa_entrada_min_kg"])
    for x in linhas:
        if not x.get("fecha"):
            continue
        if x["tipo"] == "base":
            cruz, entrada = lan_b["paineis_cruzeiro_kg"], lan_b["massa_entrada_kg"]
        else:
            lan = hip_lan.get(x["altitude_km"])
            if lan is None:
                continue
            cruz = lan["paineis_cruzeiro_kg"]
            entrada = lan["massa_entrada_kg"] + (x["glom_kg"] - lan["mav_estagios"][0]["massa_inicial_kg"]) / razao
        x["massa_entrada_kg"] = entrada
        x["lander_injetado_kg"] = ve.lander_estagios(entrada + cruz, scfg, dcfg, p, a_caso)[1].massa_inicial
        # massa de entrada levada ao piso publicado do SRL de 4,65 m ([F202] p. 13, ">5000"), quando o modelo dá menos
        x["lander_injetado_piso_srl_kg"] = ve.lander_estagios(max(entrada, m_srl) + cruz, scfg, dcfg, p, a_caso)[1].massa_inicial
    lcfg = ler("config/lancadores.yaml")
    ms = ler("results/etapa1.3/missoes.yaml")
    cand = {c["id"]: c for c in ms["candidatas"]}
    janelas = [cand[w["missao"]] for w in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()]
    pen = a4.get("penalidade_coifa_longa_kg")
    for x in linhas:
        if x.get("lander_injetado_kg"):
            x["margens"] = {nl: {f"{mm}_{cs}": (lc.pior_margem_a(nl, x[chave], janelas, lcfg, m_ad + perda)[0] if perda is not None else None)
                                 for mm, chave in (("modelo", "lander_injetado_kg"), ("piso_srl", "lander_injetado_piso_srl_kg"))
                                 for cs, perda in (("coifa_padrao", 0.0), ("coifa_longa", v(pen) if pen else None))}
                            for nl in a4["lancadores"]}
    # (d) massa por área
    d465 = v(cad["aeroshell"]["opcoes"]["srl_duplo"]["diametro_m"])
    d45 = v(cad["aeroshell"]["opcoes"]["m2020"]["diametro_m"])
    for x in linhas:
        if x.get("massa_entrada_kg"):
            x["massa_por_area_465_piso_srl_kg_m2"] = max(x["massa_entrada_kg"], m_srl) / (math.pi * d465 ** 2 / 4)
            x["massa_por_area_465_kg_m2"] = x["massa_entrada_kg"] / (math.pi * d465 ** 2 / 4)
            x["massa_por_area_45_kg_m2"] = x["massa_entrada_kg"] / (math.pi * d45 ** 2 / 4)
    # (f) sólido com a P-019 no lugar da P-111
    ctx = sm.contexto()
    sc, _, atm, pl0, _ = ctx
    g = fc["mav_solido"]["guia"]
    t_v, partidas, limites, tol = v(g["t_v_s"]), g["partidas"]["valor"], [tuple(t) for t in g["limites"]["valor"]], v(g["tol_custo"])
    msd = cad["mav_solido"]
    mp_msr, isp_s, t_q = msd["propelente_kg"]["valor"], msd["isp_s"]["valor"], msd["tempo_queima_s"]["valor"]
    f_tempo = [mp * i * sb.G0_M / t for mp, i, t in zip(mp_msr, isp_s, t_q)]
    carga = v(scfg["mav"]["carga_util_kg"])
    eps = v(ler("config/mav_propulsao.yaml")["opcoes"]["O1"]["fracao_estrutural"])
    k19 = [eps / (1 - eps)] * 2
    k111 = [i / x for i, x in zip(mv["verificacao"]["base"]["inertes_kg"], mp_msr)]
    pl_e = sb.Planeta(pl0.mu, pl0.raio, sb.omega_efetivo(pl0.omega, v(scfg["sitio_e_encontro"]["inclinacao_encontro_graus"])))
    area_s = v(sc["arrasto"]["cd_base"]) * math.pi * d_s ** 2 / 4
    margem = v(dcfg["margem_dv"])
    lo, hi = fc["mav_solido"]["guia"]["escala_busca"]["valor"]
    passo = v(g["passo_varredura_escala"])
    em_ = fc["mav_solido"]["escala_minima"]
    nm_ = {"tol_ls": v(em_["tol_ls"]), "custo_circular": v(em_["custo_circular"]), "xatol_c": v(em_["xatol_c"])}
    sens = []
    for rot, k in (("P-111 (divisão da conferência)", k111), ("P-019 (ε 0,286 nos dois estágios)", k19)):
        for h in sorted({x["altitude_km"] for x in mv["solido"]}):
            melhor = {}

            def tenta(s, k=k, h=h):
                est, ine = mf.solido([s * x for x in mp_msr], [s * x for x in f_tempo], isp_s, k, carga)
                aj = sb.ajusta_solido(pl_e, est, ine, area_s, atm, 1000 * h, t_v, partidas, limites)
                if not melhor or aj[0] < melhor["custo"]:
                    melhor.update({"custo": aj[0], "escala": s, "periapse_km": aj[1]["periapse_m"] / 1000, "apoapse_km": aj[1]["apoapse_m"] / 1000})
                return aj, est, ine

            def deficit(s, k=k, h=h):
                est, ine = mf.solido([s * x for x in mp_msr], [s * x for x in f_tempo], isp_s, k, carga)
                a_m, vo, gu = sb.semieixo_circular_maximo(pl_e, est, ine, area_s, atm, t_v, partidas, limites, nm_)
                return (-1.0e7 if a_m is None else a_m - (pl_e.raio + 1000 * h)), vo, gu
            # escala mínima pelo critério da P-117 (o mesmo de tools/mav_familia1.py)
            r_ = mf.escala_minima(tenta, deficit, lo, hi, passo, tol, v(em_["xtol_escala"]))
            linha = {"inerte": rot, "altitude_km": h, "fecha": r_ is not None}
            if r_:
                b_ = r_[0]
                ok = (None,) + mf.solido([b_ * x for x in mp_msr], [b_ * x for x in f_tempo], isp_s, k, carga)
                cap0 = mf.capacidade(ok[1], ok[2], carga)
                s2_ = escala_para((1 + margem) * cap0, b_, mp_msr, f_tempo, isp_s, k, carga)
                assint = assintotica(mp_msr, f_tempo, isp_s, k)
                for nome, esc in (("sem margem", b_), ("com a margem da P-014, não simulado", s2_)) if s2_ is not None else (("sem margem", b_),):
                    e_, i_ = mf.solido([esc * x for x in mp_msr], [esc * x for x in f_tempo], isp_s, k, carga)
                    mp = sum(x.propelente_kg for x in e_)
                    Ls = [lf + (v(msd["comprimento_m"]) - lf) * mp / sum(mp_msr) for lf in msd["escala"]["comprimento_fixo_m"]["valor"]]
                    linha.setdefault("casos", []).append({"margem": nome, "escala": esc, "capacidade_m_s": mf.capacidade(e_, i_, carga), "glom_kg": e_[0].massa_inicial_kg,
                                                          "comprimento_m": [min(Ls), max(Ls)], "folga_465_com_deck_m": [(lim[d_s]["com_deck_m"] - max(Ls)) / 2, (lim[d_s]["com_deck_m"] - min(Ls)) / 2],
                                                          "folga_465_sem_deck_m": [(lim[d_s]["sem_deck_m"] - max(Ls)) / 2, (lim[d_s]["sem_deck_m"] - min(Ls)) / 2]})
                linha.update({"capacidade_minima_m_s": cap0, "capacidade_assintotica_m_s": assint, "k": k})
            else:
                # nenhuma escala da grade fecha a circular (P-117): o melhor ponto da varredura, só como diagnóstico
                e_, i_ = mf.solido([melhor["escala"] * x for x in mp_msr], [melhor["escala"] * x for x in f_tempo], isp_s, k, carga)
                cap_b = mf.capacidade(e_, i_, carga)
                assint_ = assintotica(mp_msr, f_tempo, isp_s, k)
                s2_ = escala_para((1 + margem) * cap_b, melhor["escala"], mp_msr, f_tempo, isp_s, k, carga) or melhor["escala"]
                e2, i2 = mf.solido([s2_ * x for x in mp_msr], [s2_ * x for x in f_tempo], isp_s, k, carga)
                mp2 = sum(x.propelente_kg for x in e2)
                L2 = [lf + (v(msd["comprimento_m"]) - lf) * mp2 / sum(mp_msr) for lf in msd["escala"]["comprimento_fixo_m"]["valor"]]
                ind = {"escala": s2_, "capacidade_m_s": mf.capacidade(e2, i2, carga), "glom_kg": e2[0].massa_inicial_kg, "comprimento_m": [min(L2), max(L2)],
                       "folga_465_sem_deck_m": [(lim[d_s]["sem_deck_m"] - max(L2)) / 2, (lim[d_s]["sem_deck_m"] - min(L2)) / 2],
                       "folga_465_com_deck_m": [(lim[d_s]["com_deck_m"] - max(L2)) / 2, (lim[d_s]["com_deck_m"] - min(L2)) / 2],
                       "folga_45_com_deck_m": [(lim45[d_s]["com_deck_m"] - max(L2)) / 2, (lim45[d_s]["com_deck_m"] - min(L2)) / 2]}
                if escala_para((1 + margem) * cap_b, melhor["escala"], mp_msr, f_tempo, isp_s, k, carga) is None:
                    ind = None   # a capacidade com a margem passa da assintótica: não há escala que chegue
                linha.update({"k": k, "melhor_da_varredura": {**melhor, "tolerancia": tol, "capacidade_m_s": cap_b, "glom_kg": e_[0].massa_inicial_kg, "indicativo_com_margem": ind},
                              "capacidade_assintotica_m_s": assint_})
            sens.append(linha)
    out = nativo({"gerado_por": "tools/familia1_465.py", "status": "NÃO VALIDADO", "forma": forma, "diametro_m": d465, "altura_adaptador_m": h_ad, "massa_adaptador_kg": m_ad,
                  "encaixe": encaixe, "massa_entrada_min_srl_kg": m_srl, "limites_465": {str(d): x for d, x in lim.items()}, "limites_45": {str(d): x for d, x in lim45.items()}, "linhas": linhas,
                  "referencia_m2020_kg_m2": rb["referencia_m2020_kg_m2"], "alvo_folga_m": m.alvo, "capacidade_coifa_longa": a4["capacidade_coifa_longa"],
                  "penalidade_coifa_longa": a4.get("penalidade_coifa_longa_kg"), "sensibilidade_solido": sens, "politica_margem_msr": fc.get("politica_margem_msr", [])})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "aeroshell_465.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def assintotica(mp, f, isp, k):
    """Capacidade ideal do sólido de escala infinita: a carga útil some diante do resto, e a capacidade sem carga não
    depende da escala."""
    return mf.capacidade(*mf.solido(mp, f, isp, k, 0.0), 0.0)


def escala_para(cap_alvo, s0, mp, f, isp, k, carga):
    """Menor escala do propelente cuja capacidade ideal chega a `cap_alvo`, a partir de `s0`; None se o alvo passa da
    capacidade assintótica (escala infinita). A capacidade cresce com a escala: dobra até passar do alvo, depois bisseção."""
    def cap(s):
        return mf.capacidade(*mf.solido([s * x for x in mp], [s * x for x in f], isp, k, carga), carga)
    if cap_alvo >= assintotica(mp, f, isp, k):
        return None
    lo, hi = s0, s0
    while cap(hi) < cap_alvo:
        lo, hi = hi, 2 * hi
    while hi - lo > 1e-12 * hi:
        m = (lo + hi) / 2
        lo, hi = (m, hi) if cap(m) < cap_alvo else (lo, m)
    return hi


def faixa(par, f=sg):
    a, b = par
    return f(a) if abs(a - b) < 5e-4 else f"{f(a)} a {f(b)}"


def escreve_md(o):
    al = o["alvo_folga_m"]
    md = ["# Família 1 com o aeroshell de 4,65 m (gerado por tools/familia1_465.py)", "", "**NÃO VALIDADO.** Forma da cápsula: " + o["forma"].upper().replace("_", "-") + f" (Ø {br(o['diametro_m'], 2)} m); adaptador da P-097 ({br(o['altura_adaptador_m'], 3)} m e {br(o['massa_adaptador_kg'], 0)} kg).", "",
          "## (a) Encaixe no Vulcan com a coifa longa de 21,3 m", "", "Envelope de [F80] Fig. 4.3.1-2, PDF p. 45 (figura simplificada, leitura das cotas). Duas leituras entre as cotas, como na 7.2: contorno reto, e o Ø da segunda estação desde a interface.", "",
          "| Cápsula | Leitura | Folga radial nos vértices (m) | Folga na grade de 400 pontos (m) |", "| :- | :- | -: | -: |"]
    md += [f"| {e['forma'].upper().replace('_', '-')} (Ø máximo do perfil {br(e['diametro_m'], 2)} m) | {e['leitura']} | {sg(e['folga_vertices_m'])} | {sg(e['folga_grade_m'])} |" for e in o["encaixe"]]
    md += ["", "## (b) Comprimento máximo do MAV deitado", "", "| Ø do MAV (m) | 4,65 m sem deck | 4,65 m com deck (P-094) | 4,5 m sem deck | 4,5 m com deck |", "| -: | -: | -: | -: | -: |"]
    md += [f"| {br(float(d), 2)} | {br(x['sem_deck_m'])} | {br(x['com_deck_m'])} | {br(o['limites_45'][d]['sem_deck_m'])} | {br(o['limites_45'][d]['com_deck_m'])} |" for d, x in o["limites_465"].items()]
    md += ["", f"## (c) e (d) Folgas e massa por área (alvo {sg(al, 2)} m)", "",
           "| MAV | Ø (m) | Comprimento (m) | 4,65 m sem deck | 4,65 m com deck | 4,5 m sem deck | 4,5 m com deck | Massa por área com 4,65 m, modelo (kg/m²) | Com 4,65 m, piso do SRL (kg/m²) | Com 4,5 m, modelo (kg/m²) |", "| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
    for x in o["linhas"]:
        if not x.get("fecha"):
            md.append(f"| {x['rotulo']} | — | não fecha | | | | | | | |")
            continue
        md.append(f"| {x['rotulo']} | {br(x['diametro_m'], 2)} | {faixa(x['comprimento_m'], lambda y: br(y, 2))} | {faixa(x['folga_465']['sem_deck_m'])} | {faixa(x['folga_465']['com_deck_m'])} | {faixa(x['folga_45']['sem_deck_m'])} | {faixa(x['folga_45']['com_deck_m'])} | "
                  + (f"{br(x['massa_por_area_465_kg_m2'], 0)} | {br(x['massa_por_area_465_piso_srl_kg_m2'], 0)} | {br(x['massa_por_area_45_kg_m2'], 0)} |" if x.get("massa_entrada_kg") else "— | — | — |"))
    abaixo = [x for x in o["linhas"] if x.get("fecha") and "com a margem" in x["rotulo"] and 0 < x["folga_465"]["com_deck_m"][1] < al]
    if abaixo:
        md += ["", "Abaixo do alvo com deck no aeroshell de 4,65 m, embora positivos: " + "; ".join(f"{x['rotulo']} ({faixa(x['folga_465']['com_deck_m'])} m)" for x in abaixo)
               + f". O alvo de {sg(al, 2)} m continua (decisão do Fabio, 2026-11-10, PR #60)."]
    md += ["", f"Mars 2020: {br(o['referencia_m2020_kg_m2'], 0)} kg/m² (results/etapa7.2/rotas_mav.md). A massa de entrada não muda com o diâmetro no modelo (P-018 fixa): o aeroshell maior não pesa mais aqui, o que é otimista. A coluna do piso usa a massa de entrada publicada do SRL de 4,65 m (" + f"{br(o['massa_entrada_min_srl_kg'], 0)} kg, [F202] p. 13, \">5000\") quando o modelo dá menos.", "",
           "## (e) Margem do lander no Vulcan com a coifa longa", "", o["capacidade_coifa_longa"] + ". Coluna \"coifa padrão\": a curva do ELVPerf [F79] usada no estudo, menos o adaptador da P-097; a consulta não informa o comprimento da coifa, e tratá-la como a da coifa padrão é inferência (limite otimista para a coifa longa). Coluna \"coifa longa\": " + (f"a mesma curva menos também {br(o['penalidade_coifa_longa']['valor'], 0)} kg da P-112 (NÃO VALIDADA, análogo da Atlas V em GTO, [F27] PDF p. 57; sem fonte para o Vulcan)." if o["penalidade_coifa_longa"] else "não calculada, sem premissa."), "",
           f"Duas massas do lander: a do modelo (razão pousada/entrada da P-018 fixa, a mesma do aeroshell de 4,5 m) e a com a massa de entrada levada ao piso publicado do SRL de 4,65 m ({br(o['massa_entrada_min_srl_kg'], 0)} kg, [F202] p. 13, \">5000\"), quando o modelo dá menos.", "",
           "| Lander | Massa de entrada (kg) | Injetado (kg) | VC4, coifa padrão | VC4, coifa longa | VC6, coifa padrão | VC6, coifa longa |", "| :- | -: | -: | -: | -: | -: | -: |"]

    def pc(y):
        return "—" if y is None else f"{sg(100 * y, 1)} %"
    for x in o["linhas"]:
        if x.get("margens"):
            mg = x["margens"]
            for mm, rot, ch in (("modelo", "modelo", "lander_injetado_kg"), ("piso_srl", "piso do SRL", "lander_injetado_piso_srl_kg")):
                ent = x["massa_entrada_kg"] if mm == "modelo" else max(x["massa_entrada_kg"], o["massa_entrada_min_srl_kg"])
                md.append(f"| {x['rotulo']} ({rot}) | {br(ent, 0)} | {br(x[ch], 0)} | " + " | ".join(pc(mg[nl][f"{mm}_{cs}"]) for nl in ("Vulcan VC4", "Vulcan VC6") for cs in ("coifa_padrao", "coifa_longa")) + " |")
    vc4 = [x["margens"]["Vulcan VC4"][f"{mm}_coifa_padrao"] for x in o["linhas"] if x.get("margens") for mm in ("modelo", "piso_srl")]
    if vc4:
        md += ["", f"Pior margem no VC4 com a curva da coifa padrão (limite otimista para a coifa longa): {sg(100 * min(vc4), 1)} %; melhor: {sg(100 * max(vc4), 1)} %."]
        neg = [(x["rotulo"], mm) for x in o["linhas"] if x.get("margens") for mm in ("modelo", "piso_srl")
               if min(x["margens"]["Vulcan VC4"][f"{mm}_{cs}"] for cs in ("coifa_padrao", "coifa_longa") if x["margens"]["Vulcan VC4"][f"{mm}_{cs}"] is not None) <= 0]
        md += ["", ("**O VC4 com a coifa longa não tem margem positiva** (nem no limite otimista) para: " + "; ".join(f"{r} ({'modelo' if mm == 'modelo' else 'piso do SRL'})" for r, mm in dict.fromkeys(neg))
                    + ". Nesses casos o VC6 fica como a alternativa; a decisão é do Fabio.") if neg else "O VC4 com a coifa longa tem margem positiva em todos os casos da tabela, nas duas colunas."]
    md += ["", "## (f) Sólido: P-111 × P-019, com a margem da P-014", "",
           "| Inerte | Encontro (km) | Capacidade mínima (m/s) | Capacidade assintótica (m/s) | Caso | Escala | GLOM (kg) | Comprimento (m) | 4,65 m sem deck | 4,65 m com deck |", "| :- | -: | -: | -: | :- | -: | -: | -: | -: | -: |"]
    for s in o["sensibilidade_solido"]:
        if not s["fecha"]:
            b = s["melhor_da_varredura"]
            ind = b["indicativo_com_margem"]
            md.append(f"| {s['inerte']} | {br(s['altitude_km'], 0)} | não fecha na varredura | {br(s['capacidade_assintotica_m_s'], 0)} | melhor ponto (diagnóstico): resíduo {b['custo']:.1e} (tolerância {b['tolerancia']:.0e}), {br(b['periapse_km'], 0)} × {br(b['apoapse_km'], 0)} km, {br(b['capacidade_m_s'], 0)} m/s".replace(".", ",") + f" | {br(b['escala'], 2)} | {br(b['glom_kg'], 1)} | | | |")
            if ind is None:
                md.append(f"| {s['inerte']} | {br(s['altitude_km'], 0)} | | | indicativo com a margem da P-014: não existe (passa da capacidade assintótica) | | | | | |")
                continue
            md.append(f"| {s['inerte']} | {br(s['altitude_km'], 0)} | | | indicativo: o melhor ponto com a margem da P-014, não simulado | {br(ind['escala'], 2)} | {br(ind['glom_kg'], 1)} | {faixa(ind['comprimento_m'], lambda y: br(y, 2))} | {faixa(ind['folga_465_sem_deck_m'])} | {faixa(ind['folga_465_com_deck_m'])} |")
            continue
        for c in s["casos"]:
            md.append(f"| {s['inerte']} | {br(s['altitude_km'], 0)} | {br(s['capacidade_minima_m_s'], 0)} | {br(s['capacidade_assintotica_m_s'], 0)} | {c['margem']} | {br(c['escala'], 2)} | {br(c['glom_kg'], 1)} | {faixa(c['comprimento_m'], lambda y: br(y, 2))} | {faixa(c['folga_465_sem_deck_m'])} | {faixa(c['folga_465_com_deck_m'])} |")
    md += ["", "A capacidade assintótica é a de um sólido de escala infinita com os mesmos k de inerte: se a capacidade com a margem passa dela, não há sólido que feche.", "",
           "\"Não fecha na varredura\" quer dizer: em nenhuma escala da varredura da P-110 o ajuste chega à circular (critério da P-117). O melhor ponto é diagnóstico, não resultado.",
           "", "**Nota (2026-11-12):** a escala mínima do sólido passou a ser a raiz de (maior semieixo de uma circular alcançável) − (raio-alvo) (P-117, PR #64); as versões anteriores desta página, com o ajuste antigo, davam a P-019 a 380 km como \"não fecha na varredura\", com o melhor ponto a menos de 1 km da órbita. Valem os números desta versão; os da linha do sólido nas seções (c) a (e) vêm de results/familia1/mavs.yaml, regenerado no PR #64.",
           "", "O caso indicativo é a escala cuja capacidade ideal chega ao melhor ponto vezes 1 + a margem da P-014; \"não existe\" quando esse alvo passa da capacidade assintótica."]
    if o["politica_margem_msr"]:
        md += ["", "## Política de margem do MAV sólido do MSR, nas fontes", ""] + [f"- {x}" for x in o["politica_margem_msr"]]
    (SAIDA / "aeroshell_465.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
