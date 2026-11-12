"""Família 1 (Fabio, 2026-11-09), itens 1 e 3: dois MAVs para o encontro em órbita baixa, lado a lado, com o térmico.

(i) Sólido de dois estágios, a partir do MAV do MSR de 2019 ([F34]). Subida com queima até o esgotamento, costa e 2º
    estágio (orbital.subida.voa_solido). Verificação: com as massas, empuxos e Isp publicados, o modelo leva o veículo à
    órbita publicada; a divisão do inerte entre os estágios não é publicada e é escolhida no meio do intervalo que fecha
    (P-110); o tempo de costa, não ajustado, é comparado com o publicado. Dimensionamento: propelente e empuxo escalados
    juntos (P-108), a menor escala que chega à circular de encontro, e depois a margem de Δv da P-014 sobre a capacidade.
(ii) Hipergólico 4 × R-4D-11 164:1 em Ø que contém as saídas com parede, com a perda gravitacional pelo modelo do
    PR #55 (tools/subida_mav.py) e o encontro na circular baixa.
Para cada MAV: Δv, GLOM, comprimento, empuxo/peso, folga deitado com e sem deck no aeroshell de 4,5 m e massa por área; e
o tempo na superfície (results/familia1/missao.yaml), a energia e os RHUs para manter a faixa de temperatura.
Saída: results/familia1/mavs.yaml e .md

Uso: python tools/mav_familia1.py
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

import comprimento_mav as cmv  # noqa: E402
import comprimento_solido as cs  # noqa: E402
import rota_a_dimensiona as rad  # noqa: E402
import subida_mav as sm  # noqa: E402
from orbital import motores as om  # noqa: E402
from orbital.mav import mav_estagios  # noqa: E402
from orbital import subida as sb  # noqa: E402
from orbital import veiculos as ve  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "familia1"
POL = 0.0254   # [F112] Apêndice B.8, PDF p. 62: polegada em metros
G0 = sb.G0_M
br, sg = sm.br, sm.sg


def capacidade(est, inertes, carga):
    """Δv ideal (m/s) do sólido: soma de Isp g0 ln(m0/mf) dos dois estágios."""
    m0 = carga + sum(e.propelente_kg + i for e, i in zip(est, inertes))
    dv = 0.0
    for e, i in zip(est, inertes):
        dv += e.isp_s * G0 * math.log(m0 / (m0 - e.propelente_kg))
        m0 -= e.propelente_kg + i
    return dv


def escala_minima(tenta, deficit, lo, hi, passo, tol, xtol):
    """Menor escala do propelente com que o sólido chega à circular-alvo (P-117): a raiz de deficit(s) = (maior semieixo de
    uma circular alcançável) − (raio-alvo), por brentq. O intervalo vem da varredura rápida: a última escala da grade em que
    o ajuste suave não fecha e a primeira em que fecha (`tenta(s)` devolve ((custo, voo, guia), estágios, inertes)); se o
    sinal de deficit não troca nele, o intervalo cresce um passo de cada vez. `deficit(s)` devolve (déficit em m, voo,
    guia). Devolve (escala, (déficit, voo, guia), registro do intervalo) ou None se nenhuma escala da grade fecha."""
    from scipy.optimize import brentq
    a_, s_, b_ = lo, lo, None
    while s_ <= hi + 1e-9:
        if tenta(s_)[0][0] < tol:
            b_ = s_
            break
        a_, s_ = s_, s_ + passo
    if b_ is None:
        return None
    da, db = deficit(a_)[0], deficit(b_)[0]
    while da >= 0 and a_ - passo > 0:
        a_ -= passo
        da = deficit(a_)[0]
    while db <= 0:
        if b_ + passo > hi + 1e-9:
            raise RuntimeError(f"déficit sem troca de sinal até a escala {hi}: o ajuste fecha, mas nenhuma circular foi achada no alvo")
        b_ += passo
        db = deficit(b_)[0]
    # o intervalo vem da decisão do ajuste na grade (robusta: déficit de milhares de metros longe da borda)
    raiz = brentq(lambda x: deficit(x)[0], a_, b_, xtol=xtol, rtol=4 * np.finfo(float).eps)
    return raiz, deficit(raiz), {"intervalo": [a_, b_], "deficit_m": [da, db]}


def solido(mp, f, isp, k, carga):
    """Estágios e inertes do sólido com propelente mp, empuxo f e inerte k·mp por estágio."""
    ine = [ki * m for ki, m in zip(k, mp)]
    m0 = carga + sum(mp) + sum(ine)
    est = [sb.Estagio(m0, mp[0], f[0], isp[0]), sb.Estagio(m0 - mp[0] - ine[0], mp[1], f[1], isp[1])]
    return est, ine


def main():
    ctx = sm.contexto()
    sc, scfg, atm, pl0, num = ctx
    fc = ler("config/familia1.yaml")
    m = rad.modelo()
    cad = m.cad
    ms = cad["mav_solido"]
    g = fc["mav_solido"]["guia"]
    t_v, partidas, limites = v(g["t_v_s"]), g["partidas"]["valor"], [tuple(x) for x in g["limites"]["valor"]]
    tol = v(g["tol_custo"])
    mp_msr, f_msr, isp_s = ms["propelente_kg"]["valor"], ms["empuxo_medio_n"]["valor"], ms["isp_s"]["valor"]
    carga = v(scfg["mav"]["carga_util_kg"])
    inerte_total = v(ms["glom_kg"]) - sum(mp_msr) - carga
    d_s = v(ms["diametro_m"])
    cd = v(sc["arrasto"]["cd_base"])
    area_s = cd * math.pi * d_s ** 2 / 4
    vf = fc["mav_solido"]["verificacao"]
    pl_v = sb.Planeta(pl0.mu, pl0.raio, sb.omega_efetivo(pl0.omega, v(vf["inclinacao_graus"])))

    # ---------------- verificação com o MAV do MSR de 2019
    # os dados publicados não fecham entre si (P-111): na base, o empuxo sai do propelente, do Isp e do tempo de queima
    t_q = ms["tempo_queima_s"]["valor"]
    f_tempo = [mp * i * G0 / t for mp, i, t in zip(mp_msr, isp_s, t_q)]
    modelos = {"tempo_publicado": f_tempo, "empuxo_publicado": f_msr}
    verif = []
    for nome, f_m in modelos.items():
        for f2 in vf["fracao_inerte_estagio_2"]["valor"]:
            ine = [(1 - f2) * inerte_total, f2 * inerte_total]
            k = [i / x for i, x in zip(ine, mp_msr)]
            est, ine = solido(mp_msr, f_m, isp_s, k, carga)
            custo, voo, guia = sb.ajusta_solido(pl_v, est, ine, area_s, atm, 1000 * v(vf["orbita_km"]), t_v, partidas, limites)
            x = {"modelo": nome, "fracao_inerte_2": f2, "inertes_kg": ine, "empuxos_n": f_m, "fecha": custo < tol}
            if x["fecha"]:
                x.update({"costa_s": voo["costa_s"], "queimas_s": [voo["queima_1_s"], voo["queima_2_s"]], "guia": guia})
            verif.append(x)
    # base da escala: a divisão do inerte publicada no [F269] (errata da P-110, decisão do Fabio em 2026-11-12); a varredura
    # acima fica como registro. Com essa divisão, o modelo não chega à órbita publicada; a diferença é o viés da P-114.
    msr = fc["inerte_solido"]["msr"]
    f2_base = (msr["inerte_motor_kg"]["valor"][1] + msr["inerte_nao_propulsivo_kg"]["valor"][1]) / (sum(msr["inerte_motor_kg"]["valor"]) + sum(msr["inerte_nao_propulsivo_kg"]["valor"]))
    ine_b = [(1 - f2_base) * inerte_total, f2_base * inerte_total]
    k_b = [i / x for i, x in zip(ine_b, mp_msr)]
    est_b, ine_b = solido(mp_msr, f_tempo, isp_s, k_b, carga)
    custo_b, voo_b, guia_b = sb.ajusta_solido(pl_v, est_b, ine_b, area_s, atm, 1000 * v(vf["orbita_km"]), t_v, partidas, limites)
    base = {"modelo": "tempo_publicado", "fracao_inerte_2": f2_base, "fonte": "[F269] (errata da P-110)", "inertes_kg": ine_b, "empuxos_n": f_tempo, "fecha": custo_b < tol,
            "orbita_km": [voo_b["periapse_m"] / 1000, voo_b["apoapse_m"] / 1000], "costa_s": voo_b["costa_s"], "queimas_s": [voo_b["queima_1_s"], voo_b["queima_2_s"]], "guia": guia_b}
    # ---------------- dimensionamento do sólido para o encontro da família 1
    inc = v(scfg["sitio_e_encontro"]["inclinacao_encontro_graus"])
    pl_e = sb.Planeta(pl0.mu, pl0.raio, sb.omega_efetivo(pl0.omega, inc))
    margem = v(ler("config/dimensionamento.yaml")["margem_dv"])
    alts = [x["altitude_km"] for x in ler("results/familia1/missao.yaml")["casos"]]
    sol_casos = []
    if base:
        k = [i / x for i, x in zip(base["inertes_kg"], mp_msr)]
        f_msr = f_tempo
        lo, hi = fc["mav_solido"]["guia"]["escala_busca"]["valor"]
        for h in alts:
            def tenta(s):
                est, ine = solido([s * x for x in mp_msr], [s * x for x in f_msr], isp_s, k, carga)
                return sb.ajusta_solido(pl_e, est, ine, area_s, atm, 1000 * h, t_v, partidas, limites), est, ine
            em_ = fc["mav_solido"]["escala_minima"]
            nm_ = {"tol_ls": v(em_["tol_ls"]), "custo_circular": v(em_["custo_circular"]), "xatol_c": v(em_["xatol_c"])}

            def deficit(s, h=h):
                e_, i_ = solido([s * x for x in mp_msr], [s * x for x in f_msr], isp_s, k, carga)
                a_m, vo, gu = sb.semieixo_circular_maximo(pl_e, e_, i_, area_s, atm, t_v, partidas, limites, nm_)
                return (-1.0e7 if a_m is None else a_m - (pl_e.raio + 1000 * h)), vo, gu
            esc_ = escala_minima(tenta, deficit, lo, hi, v(fc["mav_solido"]["guia"]["passo_varredura_escala"]), tol, v(em_["xtol_escala"]))
            if esc_ is None:
                sol_casos.append({"tipo": "solido", "altitude_km": h, "rotulo": f"Sólido, {br(h, 0)} km", "fecha": False})
                continue
            b_, (_, voo, guia), abaixo = esc_
            est, ine = solido([b_ * x for x in mp_msr], [b_ * x for x in f_msr], isp_s, k, carga)
            cap0 = capacidade(est, ine, carga)
            # margem da P-014 sobre a capacidade: a escala cresce até a capacidade ser (1 + margem) vezes a mínima
            s1, s2 = b_, 4 * b_
            for _ in range(60):
                sm_ = (s1 + s2) / 2
                e_, i_ = solido([sm_ * x for x in mp_msr], [sm_ * x for x in f_msr], isp_s, k, carga)
                s1, s2 = (sm_, s2) if capacidade(e_, i_, carga) < (1 + margem) * cap0 else (s1, sm_)
            for rot, esc, simulado in (("sem margem (o menor que chega)", b_, True), ("com a margem da P-014 na capacidade, não simulado", s2, False)):
                est_m, ine_m = solido([esc * x for x in mp_msr], [esc * x for x in f_msr], isp_s, k, carga)
                sol_casos.append({"tipo": "solido", "altitude_km": h, "rotulo": f"Sólido, {br(h, 0)} km, {rot}", "fecha": True, "simulado": simulado, "escala": esc,
                                  **({"costa_s": voo["costa_s"], "guia": guia, "busca_da_escala": abaixo, "deficit_na_escala_m": esc_[1][0]} if simulado else {}),
                                  "capacidade_m_s": capacidade(est_m, ine_m, carga), "capacidade_minima_m_s": cap0,
                                  "glom_kg": est_m[0].massa_inicial_kg, "propelente_kg": [e.propelente_kg for e in est_m], "inertes_kg": ine_m,
                                  "empuxos_n": [e.empuxo_n for e in est_m], "empuxo_peso": est_m[0].empuxo_n / (est_m[0].massa_inicial_kg * pl0.mu / pl0.raio ** 2)})
    # ---------------- hipergólico 4 × 164:1 em Ø 0,72 m
    d_h = v(fc["mav_hipergolico"]["diametro_m"])
    rd = cad["r4d11_variantes"]
    l164 = (rd["164:1"]["flange_a_saida_pol"] + v(rd["a_frente_da_flange_pol"])) * POL
    nt = {k_: v(x) for k_, x in cad["mav"]["comprimento_nao_tanque_m"].items()}
    nt164 = {**nt, "motores_estagio_1": l164, "motor_estagio_2": l164}
    f164 = om.catalogo()["R-4D-11"]["empuxo_n"]
    isp_h = float(m.mcfg["opcoes"][m.op]["isp_s"][0])
    ref = sm.referencia(ctx, cd)
    area_h = cd * math.pi * d_h ** 2 / 4
    hip = []
    for h in alts:
        dv100, glom_ant, hist = v(sc["referencia"]["dv_100x100_m_s"]), None, []
        fim = None
        for _ in range(num["iter"]):
            s2c = copy.deepcopy(scfg)
            s2c["subida"]["dv_100x100_km_s"]["valor"] = dv100 / 1000.0
            lan = ve.lander(m.R + h, m.R + h, mcfg=m.mcfg, scfg=s2c, detalhe=True)
            e_ = lan["mav_estagios"]
            est = [sb.Estagio(e["massa_inicial_kg"], e["propelente_kg"], n * f164, isp_h) for e, n in zip(e_, m.n_mot)]
            x = sm.voo(ctx, est, area_h)
            glom = e_[0]["massa_inicial_kg"]
            hist.append({"glom_kg": glom, "dv_100x100_usado_m_s": dv100, "dv_simulado_m_s": x["dv_m_s"] if x else None})
            if x is None:
                break
            if glom_ant is not None and abs(glom - glom_ant) < num["tol_kg"]:
                fim = (lan, e_, est)
                break
            glom_ant, dv100 = glom, v(sc["referencia"]["dv_100x100_m_s"]) + x["dv_m_s"] - ref["dv_m_s"]
        linha = {"tipo": "hipergolico", "altitude_km": h, "rotulo": f"Hipergólico 4 × 164:1, {br(h, 0)} km, com a margem da P-014", "fecha": fim is not None, "convergiu": fim is not None, "historico": hist}
        if fim:
            lan, e_, est = fim
            L = cmv.comprimento(d_h, e_, nt164, cad)
            linha.update({"glom_kg": e_[0]["massa_inicial_kg"], "dv_subida_com_margem_km_s": (1 + margem) * lan["dv_subida_mav_km_s"], "dv_100x100_m_s": hist[-1]["dv_100x100_usado_m_s"],
                          "empuxo_peso": est[0].empuxo_n / (est[0].massa_inicial_kg * pl0.mu / pl0.raio ** 2), "comprimento_m": L,
                          "folga_sem_deck_m": (m.lim_ombro[d_h] - L) / 2, "folga_com_deck_m": (m.lim_deck[d_h] - L) / 2,
                          "massa_entrada_kg": lan["massa_entrada_kg"], "propelente_kg": sum(e["propelente_kg"] for e in e_)})
        hip.append(linha)
        if fim:
            # o mesmo MAV sem a margem de Δv da P-014 (só no MAV; o resto do lander igual)
            e0 = [{"massa_inicial_kg": r_.massa_inicial, "propelente_kg": r_.propelente} for r_, _, _ in mav_estagios(lan["dv_subida_mav_km_s"], m.mcfg["opcoes"][m.op], s2c)]
            L0 = cmv.comprimento(d_h, e0, nt164, cad)
            hip.append({"tipo": "hipergolico", "altitude_km": h, "rotulo": f"Hipergólico 4 × 164:1, {br(h, 0)} km, sem margem", "fecha": True, "convergiu": True,
                        "glom_kg": e0[0]["massa_inicial_kg"], "dv_subida_km_s": lan["dv_subida_mav_km_s"], "dv_100x100_m_s": linha["dv_100x100_m_s"],
                        "empuxo_peso": est[0].empuxo_n / (e0[0]["massa_inicial_kg"] * pl0.mu / pl0.raio ** 2), "comprimento_m": L0,
                        "folga_sem_deck_m": (m.lim_ombro[d_h] - L0) / 2, "folga_com_deck_m": (m.lim_deck[d_h] - L0) / 2,
                        "massa_entrada_kg": linha["massa_entrada_kg"] - (linha["glom_kg"] - e0[0]["massa_inicial_kg"]) / v(scfg["lander"]["razao_pousada_entrada"]["entrada_direta"]),
                        "propelente_kg": sum(e["propelente_kg"] for e in e0), "nota": "massa por área: o lander com margem menos a diferença do MAV"})
    # ---------------- comprimento, folga e massa por área do sólido
    area_ae = math.pi * v(cad["aeroshell"]["opcoes"]["m2020"]["diametro_m"]) ** 2 / 4
    razao = v(scfg["lander"]["razao_pousada_entrada"]["entrada_direta"])
    hip_m = {x["altitude_km"]: x for x in hip if "com a margem" in x["rotulo"] and x.get("convergiu")}
    for s_ in sol_casos:
        h_ = hip_m.get(s_["altitude_km"], {})
        if not s_["fecha"]:
            continue
        mp = sum(s_["propelente_kg"])
        # P-108 revista: motores pelo ajuste do catálogo [F270] mais o resto fixo (tools/comprimento_solido.py)
        L_ = cs.comprimento(s_["propelente_kg"], d_s)
        s_["comprimentos"] = [{"lei": "P-108 revista", "comprimento_m": L_, "folga_sem_deck_m": (m.lim_ombro[d_s] - L_) / 2, "folga_com_deck_m": (m.lim_deck[d_s] - L_) / 2}]
        if h_.get("convergiu"):
            s_["massa_entrada_kg"] = h_["massa_entrada_kg"] + (s_["glom_kg"] - h_["glom_kg"]) / razao
    for x in sol_casos + hip:
        if "massa_entrada_kg" in x:
            x["massa_por_area_kg_m2"] = x["massa_entrada_kg"] / area_ae
    # ---------------- térmico na superfície
    aq = ler("config/mav_propulsao.yaml")["aquecimento"]
    tf = fc["termico"]
    dias = {c["altitude_km"]: c["mav_na_superficie_dias"] for c in ler("results/familia1/missao.yaml")["casos"]}

    lanc = {c["altitude_km"]: int(str(c["lancamento_mav"])[:4]) for c in ler("results/familia1/missao.yaml")["casos"]}

    def termico(t_min, m_prop, h):
        rhu_w = v(tf["rhu_w_2014"]) - v(tf["rhu_queda_w_ano"]) * (lanc[h] - v(tf["rhu_ano_referencia"]))
        p = v(aq["referencia_w"]) * (t_min - v(aq["t_ambiente_c"])) / (v(aq["t_referencia_c"]) - v(aq["t_ambiente_c"])) * (m_prop / v(aq["m_prop_referencia_kg"])) ** v(aq["expoente_area"])
        return {"temperatura_c": t_min, "potencia_w": p, "dias": dias[h], "energia_kwh": p * 24 * dias[h] / 1000, "rhu_w": rhu_w, "ano": lanc[h], "rhus": math.ceil(p / rhu_w), "rhu_teto_new_frontiers": v(tf["rhu_teto_new_frontiers"])}
    for s_ in sol_casos:
        if s_["fecha"]:
            s_["termico"] = termico(v(aq["t_minima_c"]["O1"]), sum(s_["propelente_kg"]), s_["altitude_km"])
    for h_ in hip:
        if h_.get("convergiu"):
            h_["termico"] = termico(v(aq["t_minima_c"][m.op]), h_["propelente_kg"], h_["altitude_km"])
    out = nativo({"gerado_por": "tools/mav_familia1.py", "status": "NÃO VALIDADO", "alvo_folga_m": m.alvo, "margem_dv": margem,
                  "verificacao": {"orbita_km": v(vf["orbita_km"]), "costa_publicada_s": v(vf["costa_publicada_s"]), "casos": verif, "base": base},
                  "limites": {"solido": {"diametro_m": d_s, "sem_deck_m": m.lim_ombro[d_s], "com_deck_m": m.lim_deck[d_s]}, "hipergolico": {"diametro_m": d_h, "sem_deck_m": m.lim_ombro[d_h], "com_deck_m": m.lim_deck[d_h]}},
                  "solido": sol_casos, "hipergolico": hip, "envelhecimento_solido": tf["envelhecimento_solido"], "tempo_no_msr": tf["tempo_no_msr"]})
    SAIDA.mkdir(parents=True, exist_ok=True)
    out["errata"] = fc.get("errata_mavs_2026_11_11")
    out["errata_2"] = fc.get("errata_mavs_2026_11_12")
    (SAIDA / "mavs.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    vb = o["verificacao"]
    md = ["# Família 1: dois MAVs para o encontro em órbita baixa (gerado por tools/mav_familia1.py)", "", "**NÃO VALIDADO.** Premissas P-014, P-018, P-019, P-027, P-104 a P-108, P-110, P-111 e P-117.", "",
          "## Verificação do modelo do sólido com o MAV do MSR de 2019", "",
          f"Propelente, Isp, tempos de queima e empuxos médios publicados ([F34] PDF p. 4; [F249] PDF p. 5); alvo de {br(vb['orbita_km'], 0)} km ([F34] PDF p. 4). **Os dados publicados não fecham entre si:** empuxo médio × tempo de queima é maior que propelente × Isp × g0. A base usa o tempo de queima publicado e tira o empuxo dele; a alternativa usa o empuxo publicado e tira o tempo (P-111). A divisão do inerte entre os estágios não é publicada: varrida (P-110).", "",
          "| Modelo de empuxo | Empuxos (N) | Fração do inerte no estágio 2 | Inertes (kg) | Chega à órbita | Queimas (s) | Costa (s) |", "| :- | -: | -: | -: | :- | -: | -: |"]
    for x in vb["casos"]:
        md.append(f"| {x['modelo'].replace('_', ' ')} | {br(x['empuxos_n'][0], 0)} e {br(x['empuxos_n'][1], 0)} | {br(x['fracao_inerte_2'], 2)} | {br(x['inertes_kg'][0], 1)} e {br(x['inertes_kg'][1], 1)} | {'sim' if x['fecha'] else 'não'} | " + (f"{br(x['queimas_s'][0], 1)} e {br(x['queimas_s'][1], 1)} | {br(x['costa_s'], 0)} |" if x["fecha"] else "— | — |"))
    b = vb["base"]
    md += ["", (f"**Base: tempo de queima publicado, fração {br(b['fracao_inerte_2'], 3)}, a do [F269]** (errata da P-110, 2026-11-12): " + ("chega à órbita publicada. " if b["fecha"] else f"**não chega à órbita publicada** ({br(b['orbita_km'][0], 0)} × {br(b['orbita_km'][1], 0)} km); a diferença é o viés da P-114. ") + f"Até 2026-11-11, a base era a divisão escolhida no meio das que chegam (P-110 original; ver a errata no fim). Costa de {br(b['costa_s'], 0)} s no melhor ajuste, contra {br(vb['costa_publicada_s'], 0)} s publicados ([F34] PDF p. 7). Três parâmetros de guiamento para três resíduos (semieixo e vetor excentricidade; até 2026-11-11, dois: periapse e apoapse): **o modelo não fica verificado**; é uma conferência parcial." if b else "**Nenhuma divisão do inerte leva à órbita publicada com o tempo de queima publicado: o modelo não reproduz o MSR.**"), "",
           "## Comparação lado a lado", ""]
    hd = "| Grandeza | " + " | ".join(x["rotulo"] for x in o["solido"] + o["hipergolico"]) + " |"
    md += [hd, "| :- |" + " -: |" * (len(o["solido"]) + len(o["hipergolico"]))]

    def cel(x, f):
        if not x.get("fecha", x.get("convergiu")) and f is not linhas[0][1]:
            return "—"
        try:
            return f(x)
        except (KeyError, TypeError):
            return "—"
    linhas = [("Fecha", lambda s: ("não simulado" if s.get("simulado") is False else "sim") if s.get("fecha", s.get("convergiu")) else "não"),
              ("Δv (m/s)", lambda s: f"{br(s['capacidade_m_s'], 0)} (capacidade ideal)" if "capacidade_m_s" in s else f"{br(1000 * s.get('dv_subida_com_margem_km_s', s.get('dv_subida_km_s', 0)), 0)} (de projeto)"),
              ("GLOM (kg)", lambda s: br(s["glom_kg"], 1)),
              ("Empuxo/peso na decolagem", lambda s: br(s["empuxo_peso"], 2)),
              ("Comprimento (m)", lambda s: br(s["comprimentos"][0]["comprimento_m"], 2) if "comprimentos" in s and len(s["comprimentos"]) == 1 else (f"{br(min(c['comprimento_m'] for c in s['comprimentos']), 2)} a {br(max(c['comprimento_m'] for c in s['comprimentos']), 2)}" if "comprimentos" in s else br(s["comprimento_m"], 3))),
              ("Folga deitado sem deck (m)", lambda s: f"{sg(min(c['folga_sem_deck_m'] for c in s['comprimentos']))} a {sg(max(c['folga_sem_deck_m'] for c in s['comprimentos']))}" if "comprimentos" in s else sg(s["folga_sem_deck_m"])),
              ("Folga deitado com deck (m)", lambda s: f"{sg(min(c['folga_com_deck_m'] for c in s['comprimentos']))} a {sg(max(c['folga_com_deck_m'] for c in s['comprimentos']))}" if "comprimentos" in s else sg(s["folga_com_deck_m"])),
              ("Massa por área (kg/m²)", lambda s: br(s["massa_por_area_kg_m2"], 0)),
              ("Dias na superfície", lambda s: br(s["termico"]["dias"], 0)),
              ("Temperatura mantida (°C)", lambda s: br(s["termico"]["temperatura_c"], 0)),
              ("Aquecimento (W)", lambda s: br(s["termico"]["potencia_w"], 1)),
              ("Energia na superfície (kWh)", lambda s: br(s["termico"]["energia_kwh"], 0)),
              ("RHUs equivalentes", lambda s: f"{s['termico']['rhus']} de {br(s['termico']['rhu_w'], 2)} W em {s['termico']['ano']}")]
    for nome, f in linhas:
        md.append(f"| {nome} | " + " | ".join(cel(s, f) for s in o["solido"] + o["hipergolico"]) + " |")
    ls, lh = o["limites"]["solido"], o["limites"]["hipergolico"]
    md += ["", f"Alvo de folga: {sg(o['alvo_folga_m'], 2)} m. Limites deitado: sólido em Ø {br(ls['diametro_m'], 2)} m, {br(ls['sem_deck_m'], 3)} m sem deck e {br(ls['com_deck_m'], 3)} m com deck; hipergólico em Ø {br(lh['diametro_m'], 2)} m, {br(lh['sem_deck_m'], 3)} m e {br(lh['com_deck_m'], 3)} m. O comprimento do sólido varia com a parte fixa da P-108.", "",
           "**A margem no sólido:** com o inerte de cada estágio proporcional ao propelente (P-111), o sólido está perto da assíntota da equação do foguete: somar a margem de 10 % da P-014 à capacidade multiplica a escala do veículo. Essa coluna não foi simulada: um sólido sem corte com capacidade sobrando precisa de gestão de energia para chegar à circular. Com a fração 0,286 da P-019, o resultado seria outro. Por isso a tabela mostra o sólido sem e com margem, e o hipergólico também.", "",
           "**Sólido a 814 km:** nenhuma escala da varredura (P-110) leva à circular, com a proporção de propelente entre estágios do MSR e o 2º estágio na horizontal. Causa provável, não demonstrada: a limitação do método. Não é uma conclusão sobre o sólido.", "",
           "**Hipergólico:** Ø 0,72 m é o menor da grade de diâmetros que contém as quatro saídas com parede (results/etapa7.2/bocais_alternativas.md); o mínimo contínuo é menor. A versão sem margem tira a margem só do MAV: o Δv de 100 × 100 km é o do veículo com margem (empuxo/peso menor, conservador), e a massa de entrada desconta só a diferença do GLOM, sem a da energia de aquecimento. Os números diferem dos da rota B (results/etapa7.2/rotas_mav.md) porque aqui entra a perda gravitacional do PR #55, e porque a rota B usou 2 × 164:1 em Ø 0,60 m.", "",
           "**Como cada Δv foi obtido:** o sólido é dimensionado pela simulação da subida (queima até esgotar, costa e 2º estágio) até a circular de encontro, e a margem da P-014 entra sobre a capacidade ideal; o hipergólico usa o Δv de 100 × 100 km da simulação do PR #55 com o empuxo/peso dele, mais a transferência e o déficit de rotação, com a margem da P-014. A massa por área do sólido troca no lander o GLOM do hipergólico pelo do sólido, dividido pela razão pousada/entrada (P-018); a energia do aquecimento e o seu hardware não entram nessa troca.", "",
           "## Térmico e estocagem", "", "O aquecimento segue o modelo da Etapa 4.2 (P-027, [F57]): a potência escala com a diferença de temperatura até o ambiente do igloo e com a massa de propelente elevada a 2/3. O sólido fica no mínimo fora de operação de [F57]; o hipergólico, a 15 °C (P-027). Os RHUs são o número de unidades de [F155] que dariam a mesma potência no ano do lançamento do MAV, com a potência de 2014 caindo 0,01 W por ano. Para comparar: [F155] p. 2 registra um teto de 43 RHUs oferecido a um edital do New Frontiers, não o tamanho do inventário.", "",
           "**Envelhecimento do propelente sólido, nas fontes:**"]
    md += [f"- {x}" for x in o["envelhecimento_solido"]]
    md += ["", "**Tempo do MAV em Marte no MSR, para comparar:**"]
    md += [f"- {x}" for x in o["tempo_no_msr"]]
    er = o.get("errata")
    if er:
        sm_, cm_ = (next(x for x in o["solido"] if x.get("fecha") and x["altitude_km"] == 380 and nome in x["rotulo"]) for nome in ("sem margem", "com a margem"))
        a_, b_ = er["solido_380_sem_margem"], er["solido_380_com_margem"]

        def fx(par, f=sg):
            return f(par[0]) if abs(par[0] - par[1]) < 5e-4 else f"{f(par[0])} a {f(par[1])}"

        def novo(x, ch):
            v_ = [c[ch] for c in x["comprimentos"]]
            return [min(v_), max(v_)]

        def linha_vigente(rot, x_, rotulo="vigente"):
            if "comprimentos" in x_:   # caso calculado agora
                cmp_, fs_, fc_ = novo(x_, "comprimento_m"), novo(x_, "folga_sem_deck_m"), novo(x_, "folga_com_deck_m")
                pot, en, rh = x_["termico"]["potencia_w"], x_["termico"]["energia_kwh"], x_["termico"]["rhus"]
            else:   # registro do config
                cmp_, fs_, fc_ = x_["comprimento_m"], x_["folga_sem_deck_m"], x_["folga_com_deck_m"]
                pot, en, rh = x_["potencia_w"], x_["energia_kwh"], x_["rhus"]
            return (f"| {rot}, {rotulo} | {br(x_['escala'], 4)} | {br(x_['glom_kg'], 1)} | {br(x_['capacidade_m_s'], 0)} | {br(x_['empuxo_peso'], 2)} | {fx(cmp_, lambda y: br(y, 2))} | {fx(fs_)} | {fx(fc_)} | "
                    f"{br(x_['massa_entrada_kg'], 0)} | {br(x_['massa_por_area_kg_m2'], 0)} | {br(pot, 1)} | {br(en, 0)} | {rh} |")
        md += ["", "## Errata (2026-11-11, decisão do Fabio)", "",
               "O ajuste do sólido media o periapse e o apoapse, que têm uma quina em e = 0, exatamente no alvo circular; o custo parava em valores espalhados, a tolerância da P-110 caía no meio desse ruído, e a escala escolhida mudava com a CPU (CI do PR #60, run 42896102600; results/conferencia/ruido_subida.md). "
               "O ajuste passou a usar o semieixo e o vetor excentricidade, funções suaves, e a escala mínima do sólido passou a ser a raiz de (maior semieixo de uma circular alcançável) − (raio-alvo), por brentq (P-117, NÃO VALIDADA, para aprovação). "
               f"Os valores publicados vêm de {er['fonte']}; os antigos ficam como registro. O hipergólico não mudou.", "",
               "| Sólido, 380 km | Escala | GLOM (kg) | Capacidade (m/s) | Empuxo/peso | Comprimento (m) | Folga sem deck (m) | Folga com deck (m) | Massa de entrada (kg) | Massa por área (kg/m²) | Aquecimento (W) | Energia (kWh) | RHUs |",
               "| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
        er2 = o.get("errata_2")
        for rot, a_, x_ in (("sem margem", er["solido_380_sem_margem"], sm_), ("com a margem da P-014", er["solido_380_com_margem"], cm_)):
            if er2:   # a linha "vigente" desta errata é a do PR #64 (registro); os vigentes de hoje estão na errata de 2026-11-12
                x_ = er2["solido_380_sem_margem" if rot == "sem margem" else "solido_380_com_margem"]
            md.append(f"| {rot}, publicado | {br(a_['escala'], 4)} | {br(a_['glom_kg'], 1)} | {br(a_['capacidade_m_s'], 0)} | {br(a_['empuxo_peso'], 2)} | {fx(a_['comprimento_m'], lambda y: br(y, 2))} | {fx(a_['folga_sem_deck_m'])} | {fx(a_['folga_com_deck_m'])} | {br(a_['massa_entrada_kg'], 0)} | {br(a_['massa_por_area_kg_m2'], 0)} | {br(a_['potencia_w'], 1)} | {br(a_['energia_kwh'], 0)} | {a_['rhus']} |")
            md.append(linha_vigente(rot, x_))
        vfa = er["verificacao_fecha"]
        vfn = {m_: [c["fracao_inerte_2"] for c in o["verificacao"]["casos"] if c["modelo"] == m_ and c["fecha"]] for m_ in vfa}
        md += ["", "Verificação, divisões que chegam à órbita publicada: " + "; ".join(f"{m_.replace('_', ' ')}: publicado {', '.join(br(x, 2) for x in vfa[m_])}, vigente {', '.join(br(x, 2) for x in vfn[m_])}" for m_ in vfa)
               + f". A base continua em {br(er2['fracao_inerte_2_base'] if er2 else o['verificacao']['base']['fracao_inerte_2'], 2)}."]
        if er2:
            sm2, cm2 = (next(x for x in o["solido"] if x.get("fecha") and x["altitude_km"] == 380 and nome in x["rotulo"]) for nome in ("sem margem", "com a margem"))
            md += ["", "## Errata (2026-11-12, decisões do Fabio)", "",
                   f"Duas propostas aprovadas foram aplicadas: a P-108 revista (comprimento = motores pelo ajuste do catálogo [F270] + resto fixo sem fonte; results/familia1/comprimento_solido.md) e a errata da P-110 (a divisão do inerte na base passa de {br(er2['fracao_inerte_2_base'], 2)}, escolhida pela varredura, para {br(o['verificacao']['base']['fracao_inerte_2'], 3)}, publicada no [F269]; o valor antigo fica como registro). "
                   "A tabela da errata de 2026-11-11 mostra, na linha \"vigente\", os valores do PR #64; os vigentes de hoje estão abaixo. "
                   + ("Com a divisão do [F269], o modelo **não chega à órbita publicada** do MSR " + f"({br(o['verificacao']['base']['orbita_km'][0], 0)} × {br(o['verificacao']['base']['orbita_km'][1], 0)} km); a diferença é o viés do modelo de subida (P-114, results/familia1/inerte_solido.md)." if not o["verificacao"]["base"]["fecha"] else "Com a divisão do [F269], o modelo chega à órbita publicada do MSR."), "",
                   "| Sólido, 380 km | Escala | GLOM (kg) | Capacidade (m/s) | Empuxo/peso | Comprimento (m) | Folga sem deck (m) | Folga com deck (m) | Massa de entrada (kg) | Massa por área (kg/m²) | Aquecimento (W) | Energia (kWh) | RHUs |",
                   "| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
            for rot, a_, x_ in (("sem margem", er2["solido_380_sem_margem"], sm2), ("com a margem da P-014", er2["solido_380_com_margem"], cm2)):
                md.append(linha_vigente(rot, a_, f"PR #64 ({er2['fonte']})"))
                md.append(linha_vigente(rot, x_))
    (SAIDA / "mavs.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
