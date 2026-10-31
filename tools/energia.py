"""Etapa 4.1: energia do lander (solar em Jezero × MMRTG) e do orbitador (carga por modo × distância e eclipses).

Lander:
  - Insolação diária global na superfície em Jezero ao longo da estada da missão de referência (orbital.energia, modelo
    de Appelbaum & Landis), com o painel calibrado no 1º sol do InSight e a poeira acumulada de Lorenz et al. 2020.
  - Área e massa do painel, e a bateria da noite, para cada cenário de profundidade óptica (constante na estada, como
    envoltória), contra a demanda: plataforma (P-032) + aquecimento do MAV (orbital.mav, modelo atual).
  - Tempestade global: operação normal, ou sobrevivência (MAV + aquecedores e eletrônica do lander, P-056).
  - Opção C (linha de base desde o portão da 4.1): a maior área e a maior bateria entre céu claro e sobrevivência;
    acima de τ = 6, a razão de energia medida pelo Opportunity em 2018 (P-057) e comparação do modelo com ela.
  - Verificação da insolação diária calculada contra a tabela publicada do VL1 [F56].
  - MMRTG (alternativa A, condicionada ao Pu-238): quantos para a demanda média no fim da estada, a massa, a
    atividade do Pu-238 e o enquadramento no NSPM-20.
Orbitador:
  - Distância ao Sol por fase (ida, Marte, volta) nas janelas do envelope e na referência; eclipses das órbitas em Marte.
  - Carga por modo (P-053; o dominante é a P-028) × a carga anterior de 510 W: painel e bateria pelo modelo da plataforma
    (orbital.massa_plataformas) e o efeito no orbitador injetado e nas margens (órbita de encontro fixa).
Saída: results/etapa4.1/energia.yaml e .md

Uso: python tools/energia.py
"""

from __future__ import annotations

import copy
import datetime as dt
import math
import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital import energia as en  # noqa: E402
from orbital import ephemeris as eph  # noqa: E402
from orbital import kepler, lambert  # noqa: E402
from orbital import plataforma as pf  # noqa: E402
from orbital import porkchop as pc  # noqa: E402
from orbital import veiculos as ve  # noqa: E402
from orbital.config import ler, nativo, parametros, v  # noqa: E402
from orbital.constantes import GM_SOL, UA_KM  # noqa: E402
from orbital.lancamento import pior_margem_a  # noqa: E402
from orbital.massa_plataformas import mga, orbitador, plataforma_orbitador  # noqa: E402
from orbital.mav import massas_opcao  # noqa: E402

SAIDA = RAIZ / "results" / "etapa4.1"


def datas(ini, fim, passo_dias):
    d0, d1 = (dt.datetime.fromisoformat(x[:10]) for x in (ini, fim))
    n = int((d1 - d0).days / passo_dias)
    return [(d0 + dt.timedelta(days=k * passo_dias)).strftime("%Y-%m-%dT12:00:00") for k in range(n + 1)]


def data_com_ls(ls_alvo, ano_ini=2029):
    """Uma data (TDB) em que Ls ≈ ls_alvo (busca diária de dois anos; resolução de um dia, ~0,5° de Ls)."""
    ds = datas(f"{ano_ini}-01-01", f"{ano_ini + 2}-01-01", 1)
    ls = [en.geometria_marte(d)[0] for d in ds]
    for i in range(len(ds) - 1):
        a, b = ls[i], ls[i + 1]
        if b < a:
            b += 360.0
        alvo = ls_alvo if ls_alvo >= a else ls_alvo + 360.0
        if a <= alvo <= b:
            return ds[i]
    raise ValueError(ls_alvo)


def max_r_arco(r1, v1, tof, n=200):
    return max(np.linalg.norm(kepler.propagar(GM_SOL, r1, v1, tof * k / n)[0]) for k in range(n + 1)) / UA_KM


def main():
    ecfg, pcfg, scfg = ler("config/energia.yaml"), ler("config/plataformas.yaml"), ler("config/superficie.yaml")
    po, dcfg, mcfg, icfg, lcfg = (ler(x) for x in ("config/parametros_orbitais.yaml", "config/dimensionamento.yaml",
                                                   "config/mav_propulsao.yaml", "config/isru.yaml", "config/lancadores.yaml"))
    s1 = v(ecfg["geometria"]["constante_solar_1ua_w_m2"])
    hsol = v(pcfg["lander"]["energia"]["duracao_sol_h"])
    lc = ecfg["lander"]
    lat = v(scfg["sitio_e_encontro"]["latitude_sitio_graus"])
    ms = ler("results/etapa1.3/missoes.yaml")
    cand = {c["id"]: c for c in ms["candidatas"]}
    ref = cand[ler("config/missao_referencia.yaml")["missao_referencia"]["id"]]

    # ---------------- lander: geometria e calibração
    ci = lc["calibracao_insight"]
    ls_i, dec_i, r_i = en.geometria_marte(ci["data_tdb"]["valor"])
    fl = lc["fluxo_liquido"]
    al, tau_max, zmax = v(fl["albedo"]), v(fl["tau_max"]), v(fl["z_max_graus"])

    def hh(lat_, dec_, r_, tau):
        return en.insolacao_superficie(lat_, dec_, r_, s1, hsol, min(tau, tau_max), al, fl["k0"], fl["k1"], zmax)

    q_i = hh(v(ci["latitude_graus"]), dec_i, r_i, v(ci["tau"]))
    eta = v(ci["energia_wh"]) / (v(ci["area_m2"]) * q_i)
    perda = v(lc["perda_poeira_por_sol"])
    sois = datas(ref["chegada_marte"], ref["partida_marte"], hsol / 24.0)
    geo = [en.geometria_marte(d) for d in sois]
    q_topo = [en.insolacao_topo(lat, g[1], g[2], s1, hsol) for g in geo]

    # demanda: plataforma (P-032) + aquecimento do MAV (modelo atual, Δv de subida da arquitetura vigente)
    plat_wh = v(pcfg["lander"]["energia"]["energia_por_sol_wh"])
    lan = ve.veiculos(detalhe=True)[0]["lander"]
    mp = ler("results/etapa2.2/mav_propulsao.yaml")
    _, _, det = massas_opcao((1 + v(dcfg["margem_dv"])) * lan["dv_subida_mav_km_s"], mp["melhor_opcao"], mcfg, scfg, icfg, "mmrtg")
    mav_w = det["aquecimento_w"]
    mav_wh = mav_w * hsol
    demanda = plat_wh + mav_wh

    ka, kw = v(lc["painel_kg_m2"]["w_m2"]), v(lc["painel_kg_m2"]["w_kg"])
    kg_m2 = ka / kw
    m_painel, m_bat = mga("painel_solar", pcfg, "e1_medio"), mga("baterias", pcfg, "e1_medio")
    e = pcfg["orbitador"]["energia"]
    dod, wh_kg = v(e["profundidade_descarga"]), v(e["energia_especifica_bateria_wh_kg"])
    noite = v(pcfg["lander"]["energia"]["noite_fracao_sol"])
    efr = v(e["eficiencia_recarga"])   # P-029: a energia da noite passa pela bateria
    pk = lc["picos"]
    picos = {"braco": pk["braco"]["potencia_w"] * v(pk["braco"]["horas_por_sol"]),
             "recarga_helicopteros": v(pk["recarga_helicopteros"]["energia_por_voo_wh"]) * v(pk["recarga_helicopteros"]["voos_por_sol"]),
             "transmissoes_uhf": v(pk["transmissoes_uhf"]["potencia_w"]) * v(pk["transmissoes_uhf"]["passes_por_sol"])
             * v(pk["transmissoes_uhf"]["minutos_por_passe"]) / 60}
    e_pico = sum(picos.values())
    fator_recarga = (1 - noite) + noite / efr

    def dimensiona(tau, carga_wh, perda_por_sol=perda, pico_wh=e_pico):
        prod = [en.energia_painel(1.0, hh(lat, g[1], g[2], tau), eta, perda_por_sol, n) for n, g in enumerate(geo)]
        i = int(np.argmin([p / carga_wh for p in prod]))
        area = carga_wh * fator_recarga / prod[i]
        bat = en.bateria_kg(noite * carga_wh + pico_wh, dod, wh_kg)   # noite + picos (mesmo critério do MMRTG)
        return {"tau": tau, "tau_usado": min(tau, tau_max), "demanda_wh_sol": carga_wh, "area_m2": area, "painel_kg": area * kg_m2 * (1 + m_painel),
                "bateria_kg": bat * (1 + m_bat), "total_kg": area * kg_m2 * (1 + m_painel) + bat * (1 + m_bat),
                "pior_sol": i, "pior_sol_ls": geo[i][0], "energia_por_m2_no_pior_sol_wh": prod[i]}

    # sobrevivência do lander (P-056): MAV + aquecedores do Spirit escalados pela massa + eletrônica mínima do Spirit
    sv = lc["sobrevivencia"]
    m_lander = ler("results/etapa2.3/plataformas.yaml")["escolha"]["plataforma_lander_kg"]

    def carga_sobrevivencia(expoente):
        aq = v(sv["aquecedores_mer_wh_sol"]) * (m_lander / v(sv["massa_mer_kg"])) ** expoente
        return {"expoente": expoente, "aquecedores_lander_wh_sol": aq, "eletronica_wh_sol": v(sv["eletronica_mer_wh_sol"]),
                "mav_wh_sol": mav_wh, "total_wh_sol": mav_wh + aq + v(sv["eletronica_mer_wh_sol"])}
    sob_base, sob_sens = carga_sobrevivencia(v(sv["expoente_escala"])), carga_sobrevivencia(v(sv["expoente_sensibilidade"]))

    cen = {k: v(x) for k, x in lc["cenarios_tau"].items()}
    solar = [dict(dimensiona(t, demanda), cenario=k, carga="operação normal") for k, t in cen.items()]
    solar.append(dict(dimensiona(cen["global_2018"], sob_base["total_wh_sol"], pico_wh=0.0), cenario="global_2018",
                      carga="sobrevivência: MAV + aquecedores e eletrônica do lander (P-056)"))
    solar.append(dict(dimensiona(cen["claro_jezero"], demanda, 0.0), cenario="claro_jezero", carga="operação normal, sem poeira acumulada (sensibilidade)"))
    solar.append(dict(dimensiona(cen["global_2018"], sob_sens["total_wh_sol"], pico_wh=0.0), cenario="global_2018",
                      carga="sobrevivência, aquecedores com escala linear na massa (sensibilidade da P-056)"))

    def opcao_c(norm, sob):
        # o painel e a bateria têm de servir aos dois casos (operação normal com céu claro e sobrevivência na tempestade
        # global): a maior área e a maior bateria dos dois
        area_c, bat_c = max(norm["area_m2"], sob["area_m2"]), max(norm["bateria_kg"], sob["bateria_kg"])
        return {"cenario": "claro_jezero + global_2018", "carga": "operação normal com céu claro; sobrevivência na tempestade global",
                "area_m2": area_c, "painel_kg": area_c * kg_m2 * (1 + m_painel), "bateria_kg": bat_c,
                "total_kg": area_c * kg_m2 * (1 + m_painel) + bat_c, "dimensiona_area": "sobrevivência" if sob["area_m2"] > norm["area_m2"] else "operação normal"}
    solar_c, solar_c_sens = opcao_c(solar[0], solar[3]), opcao_c(solar[0], solar[5])

    # acima de τ = 6 (P-057): razão medida pelo Opportunity em 2018 [F140], aplicada à energia por m² com τ de referência
    to = lc["tempestade_2018_opportunity"]
    pts = {x["sol"]: x for x in to["pontos"]}
    ref_o = pts[to["referencia_sol"]]
    d0 = dt.datetime.fromisoformat(to["sol_data_conhecida"]["data"] + "T12:00:00")

    def data_sol(n):   # a data publicada do sol; sem ela, a partir do sol de data conhecida (P-057)
        if "data" in pts[n]:
            return pts[n]["data"] + "T12:00:00"
        return (d0 + dt.timedelta(days=(n - to["sol_data_conhecida"]["sol"]) * hsol / 24)).isoformat()
    lat_o = v(to["latitude_graus"])
    hh_ref = hh(lat_o, *en.geometria_marte(data_sol(ref_o["sol"]))[1:], ref_o["tau"])
    comp_opp = []
    for n, x in pts.items():
        if n == ref_o["sol"]:
            continue
        med = x["wh"] / ref_o["wh"]
        mod = hh(lat_o, *en.geometria_marte(data_sol(n))[1:], x["tau"]) / hh_ref if x["tau"] <= tau_max else None
        comp_opp.append({"sol": n, "data": data_sol(n)[:10], "tau": x["tau"], "razao_medida": med, "razao_modelo": mod,
                         "diferenca_relativa": None if mod is None else (mod - med) / med})
    tau_alto = max(pts.values(), key=lambda x: x["tau"])
    razao_alta = tau_alto["wh"] / ref_o["wh"]
    prod_ref = dimensiona(ref_o["tau"], 1.0)["energia_por_m2_no_pior_sol_wh"]   # Wh/m² no pior sol da estada com τ de referência

    def sobrevive_acima(c, sob):
        e_disp = c["area_m2"] * prod_ref * razao_alta
        return {"energia_disponivel_wh_sol": e_disp, "necessaria_wh_sol": sob["total_wh_sol"] * fator_recarga,
                "cobertura": e_disp / (sob["total_wh_sol"] * fator_recarga),
                "area_necessaria_m2": sob["total_wh_sol"] * fator_recarga / (prod_ref * razao_alta)}
    acima6 = {"tau": tau_alto["tau"], "tau_referencia": ref_o["tau"], "razao_medida": razao_alta, "energia_por_m2_referencia_wh": prod_ref,
              "base": sobrevive_acima(solar_c, sob_base), "sensibilidade": sobrevive_acima(solar_c_sens, sob_sens),
              "opportunity_wh_sol": tau_alto["wh"], "desfecho_opportunity": to["desfecho"]}

    # verificação contra a tabela do VL1 [F56] (Whr em horas de Marte: × 24,65/24 para horas terrestres, nota da tabela)
    vl = lc["conferencia_vl1"]
    conf = []
    for p in vl["pontos"]:
        d = data_com_ls(p["ls"])
        _, dec, r = en.geometria_marte(d)
        calc = hh(v(vl["latitude_graus"]), dec, r, p["tau"])
        pub = p["hh"] * v(vl["horas_marte_para_terrestres"])
        conf.append({"ls": p["ls"], "tau": p["tau"], "hh_publicado_wh": pub, "hh_calculado_wh": calc, "diferenca_relativa": (calc - pub) / pub})
    rz = [abs(c["diferenca_relativa"]) for c in conf]

    # MMRTG
    mm = icfg["energia"]["mmrtg"]
    anos = (dt.datetime.fromisoformat(ref["partida_marte"][:10]) - dt.datetime.fromisoformat(ref["partida_terra"][:10])).days / 365.25
    p_fim = en.potencia_mmrtg(v(mm["potencia_inicio_w"]), v(mm["degradacao_anual"]), anos)
    n_rtg = math.ceil(demanda / hsol / p_fim)
    anos_s = anos + v(lc["mmrtg_anos_antes_do_lancamento"])
    p_fim_s = en.potencia_mmrtg(v(mm["potencia_inicio_w"]), v(mm["degradacao_anual"]), anos_s)
    m_rtg = mga(lc["mmrtg_margem_categoria"]["valor"], pcfg, "e1_medio")
    bat_rtg = en.bateria_kg(e_pico, dod, wh_kg) * (1 + m_bat)
    rtg = {"potencia_inicio_w": v(mm["potencia_inicio_w"]), "anos_do_lancamento_ao_fim": anos, "potencia_fim_w": p_fim,
           "demanda_media_w": demanda / hsol, "unidades": n_rtg, "massa_sem_margem_kg": n_rtg * v(mm["massa_kg"]),
           "margem_crescimento": m_rtg, "bateria_kg": bat_rtg,
           "massa_kg": n_rtg * v(mm["massa_kg"]) * (1 + m_rtg) + bat_rtg,
           "sobra_por_sol_wh": (n_rtg * p_fim - demanda / hsol) * hsol,
           "fracao_potencia_fim": p_fim / v(mm["potencia_inicio_w"]),
           "pu238_g": n_rtg * v(lc["pu238"]["por_unidade_g"]),
           "nspm20": nspm20(n_rtg * v(lc["pu238"]["por_unidade_g"]), lc["pu238"]),
           "potencia_termica_total_w": n_rtg * v(lc["mmrtg"]["potencia_termica_w"]),
           "energia_por_sol_fim_wh": n_rtg * p_fim * hsol,
           "sensibilidade_abastecimento": {"anos": anos_s, "potencia_fim_w": p_fim_s, "unidades": math.ceil(demanda / hsol / p_fim_s)}}

    # ---------------- orbitador: distância por fase, eclipses, carga por modo
    janelas = [cand[w["missao"]] for w in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()]
    fases = {"ida": 0.0, "marte": 0.0, "volta": 0.0}
    for m in list({x["id"]: x for x in janelas + [ref]}.values()):
        t = [eph.tdb_para_et(m[k]) for k in ("partida_terra", "chegada_marte", "partida_marte", "chegada_terra")]
        s_t0, s_m1 = pc.estado_corpo(eph.TERRA, t[0]), pc.estado_corpo(eph.BARICENTRO_MARTE, t[1])
        s_m2, s_t3 = pc.estado_corpo(eph.BARICENTRO_MARTE, t[2]), pc.estado_corpo(eph.TERRA, t[3])
        fases["ida"] = max(fases["ida"], max_r_arco(s_t0[:3], lambert.resolver(GM_SOL, s_t0[:3], s_m1[:3], t[1] - t[0]).v1, t[1] - t[0]))
        fases["volta"] = max(fases["volta"], max_r_arco(s_m2[:3], lambert.resolver(GM_SOL, s_m2[:3], s_t3[:3], t[3] - t[2]).v1, t[3] - t[2]))
        fases["marte"] = max(fases["marte"], max(en.geometria_marte(eph.data_tdb(x))[2] for x in np.linspace(t[1], t[2], 60)))
    p = parametros()
    R = v(po["raio_marte_km"])
    pl = ler("results/etapa2.3/plataformas.yaml")["orbita_encontro"]
    rp_e, ra_e = R + pl["periapse_alt_km"], R + pl["apoapse_regra_5pct_km"]
    um = p.orbitas_marte["eliptica_alta"]
    ecl = {"encontro": pf.eclipse_maximo(p.mu_marte, R, rp_e, ra_e), "captura_1sol": pf.eclipse_maximo(p.mu_marte, R, um.rp, um.ra)}
    oc = ecfg["orbitador"]
    d_af = v(e["distancia_ua"]["semieixo"]) * (1 + v(e["distancia_ua"]["excentricidade"]))
    w1, fp, efr = v(e["painel_w_kg_1ua"]), v(e["fator_perdas_painel"]), v(e["eficiencia_recarga"])
    modos = []
    for nome, mo in oc["modos"].items():
        carga = mo["plataforma_w"] + mo["ccrs_w"] + mo["outros_w"]
        em_marte = nome in ("captura", "encontro")
        d = fases["marte"] if em_marte else fases["ida"] if nome == "cruzeiro" else max(fases["volta"], fases["marte"])
        t_e, per = ecl["captura_1sol"] if nome == "captura" else ecl["encontro"] if em_marte or nome == "retorno" else (0.0, 1.0)
        p_sa = pf.potencia_painel(carga, per - t_e, t_e, efr)
        modos.append({"modo": nome, "carga_w": carga, "distancia_max_ua": d, "eclipse_h": t_e / 3600, "painel_w": p_sa,
                      "painel_kg_sem_margem": pf.massa_painel(p_sa, w1, d, fp), "bateria_wh": carga * t_e / 3600})
    dominante = max(modos, key=lambda x: x["painel_kg_sem_margem"])
    adotada_w = v(e["carga_w"])   # P-028: desde o portão da 4.1, o modo dominante da P-053 (ADR 0015)
    if adotada_w != dominante["carga_w"]:
        raise SystemExit(f"P-028 ({adotada_w} W) difere do modo dominante da P-053 ({dominante['carga_w']} W)")
    c2 = copy.deepcopy(pcfg)
    c2["orbitador"]["energia"]["carga_w"]["valor"] = v(oc["carga_anterior_w"])
    ap = pl["apoapse_regra_5pct_km"]
    plat_ant, plat_adot = plataforma_orbitador(c2, po, ap, pl["periapse_alt_km"]), plataforma_orbitador(pcfg, po, ap, pl["periapse_alt_km"])
    _, en_ant = orbitador(c2, po, ap, pl["periapse_alt_km"])
    _, en_adot = orbitador(pcfg, po, ap, pl["periapse_alt_km"])
    vei1, jan, _ = ve.veiculos()
    d2 = copy.deepcopy(dcfg)
    d2["plataforma_orbitador_kg"]["valor"] = plat_ant
    vei0 = ve.veiculos(dcfg=d2)[0]   # sensibilidade: carga anterior com as perdas e o apoapse atuais
    margens = {nm: {"anterior": pior_margem_a(nm, vei0["orbitador_regra_iii"]["injetada_kg"], jan, lcfg)[0],
                    "adotada": pior_margem_a(nm, vei1["orbitador_regra_iii"]["injetada_kg"], jan, lcfg)[0]}
               for nm in lcfg["escolha"]["orbitador"]}
    orbit = {"distancia_max_ua_por_fase": fases, "afelio_marte_ua": d_af, "eclipse_max_h": {k: x[0] / 3600 for k, x in ecl.items()},
             "modos": modos, "modo_dominante": dominante["modo"],
             "anterior": {"carga_w": v(oc["carga_anterior_w"]), "plataforma_kg": plat_ant, "painel_w_afelio": en_ant["painel_w_afelio"],
                          "bateria_wh": en_ant["bateria_wh_nominal"], "orbitador_injetado_kg": vei0["orbitador_regra_iii"]["injetada_kg"],
                          "leo_kg": vei0["orbitador_regra_iii"]["leo_modelo_kg"]},
             "adotada": {"carga_w": adotada_w, "plataforma_kg": plat_adot, "painel_w_afelio": en_adot["painel_w_afelio"],
                         "bateria_wh": en_adot["bateria_wh_nominal"], "orbitador_injetado_kg": vei1["orbitador_regra_iii"]["injetada_kg"],
                         "leo_kg": vei1["orbitador_regra_iii"]["leo_modelo_kg"]},
             "margens_escolhidos": margens,
             "bateria_dod_mro_wh": {"profundidade_descarga": v(oc["profundidade_descarga_mro"]),
                                    "anterior": en_ant["energia_eclipse_wh"] / v(oc["profundidade_descarga_mro"]),
                                    "adotada": en_adot["energia_eclipse_wh"] / v(oc["profundidade_descarga_mro"])}}

    out = {"gerado_por": "tools/energia.py",
           "lander": {"estada": [ref["chegada_marte"], ref["partida_marte"]], "ls_inicio": geo[0][0], "ls_fim": geo[-1][0],
                      "latitude_graus": lat, "eficiencia_calibrada": eta, "insolacao_superficie_insight_wh": q_i, "ls_insight": ls_i,
                      "insolacao_topo_min_wh": min(q_topo), "insolacao_topo_max_wh": max(q_topo), "fator_poeira_fim": (1 - perda) ** (len(geo) - 1),
                      "albedo": al, "tau_max_modelo": tau_max,
                      "demanda": {"plataforma_wh_sol": plat_wh, "aquecimento_mav_w": mav_w, "aquecimento_mav_wh_sol": mav_wh, "total_wh_sol": demanda},
                      "picos_wh": picos, "pico_total_wh": e_pico,
                      "solar": solar, "solar_com_sobrevivencia": solar_c, "solar_com_sobrevivencia_sensibilidade": solar_c_sens,
                      "sobrevivencia": {"plataforma_lander_kg": m_lander, "base": sob_base, "sensibilidade": sob_sens},
                      "comparacao_opportunity_2018": comp_opp, "acima_do_modelo": acima6, "fator_recarga": fator_recarga,
                      # razão de energia por m² entre τ máximo e céu claro = razão inversa das áreas (mesma demanda)
                      "fracao_energia_tau_max_sobre_claro": solar[0]["area_m2"] / solar[2]["area_m2"],
                      "pu238_estado": lc["pu238"]["estado"], "pu238_disponibilidade": lc["pu238"]["disponibilidade"],
                      "braco_potencia_media_w": v(lc["braco"]["potencia_media_w"]), "mmrtg": rtg,
                      "verificacao_vl1": {"pontos": conf, "maior_diferenca_relativa": max(rz)}},
           "orbitador": orbit}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "energia.yaml").write_text(yaml.safe_dump(nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def nspm20(massa_g, pu):
    """Atividade do Pu-238 (λ N) em TBq e múltiplo do A2 do SSR-6, contra o limite do Tier I do NSPM-20 [F128]."""
    lam = math.log(2) / (v(pu["meia_vida_anos"]) * v(pu["dias_por_ano"]) * 86400.0)
    atividade_tbq = lam * massa_g / v(pu["massa_molar_g_mol"]) * v(pu["avogadro_mol"]) / 1e12
    multiplo = atividade_tbq / v(pu["a2_tbq"])
    return {"atividade_tbq": atividade_tbq, "multiplo_a2": multiplo, "limite_tier_i_a2": v(pu["tier_i_max_a2"]),
            "vezes_o_limite_tier_i": multiplo / v(pu["tier_i_max_a2"]),
            "enquadramento": "Tier I" if multiplo <= v(pu["tier_i_max_a2"]) else "acima do Tier I: Tier II, ou Tier III se a análise de segurança der probabilidade ≥ 1e-6 de exposição acima de 25 rem (não avaliada)"}


def escreve_md(o):
    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    pc_ = lambda x: "—" if x is None else f"{100 * x:+.0f} %".replace("-", "−")  # noqa: E731
    la = o["lander"]
    d = la["demanda"]
    md = ["# Energia (gerado por tools/energia.py)", "", "## Lander em Jezero", "",
          f"Estada {la['estada'][0]} a {la['estada'][1]} (Ls {br(la['ls_inicio'])}° a {br(la['ls_fim'])}°), latitude {br(la['latitude_graus'], 2)}°. "
          f"Insolação diária no topo da atmosfera entre {br(la['insolacao_topo_min_wh'])} e {br(la['insolacao_topo_max_wh'])} Wh/m² por sol. "
          f"Painel horizontal calibrado no 1º sol do InSight (Ls {br(la['ls_insight'])}°, superfície {br(la['insolacao_superficie_insight_wh'])} Wh/m², albedo {br(la['albedo'], 1)}): "
          f"η = {br(la['eficiencia_calibrada'], 3)}. Poeira acumulada no fim da estada, sem limpeza: fator {br(la['fator_poeira_fim'], 3)}.", "",
          f"Demanda: plataforma {br(d['plataforma_wh_sol'])} Wh/sol (P-032) + aquecimento do MAV {br(d['aquecimento_mav_w'], 1)} W "
          f"({br(d['aquecimento_mav_wh_sol'])} Wh/sol) = {br(d['total_wh_sol'])} Wh/sol.", "",
          "### Solar (τ constante na estada, como envoltória; bateria para a noite; com margens de crescimento)", "",
          f"A energia da noite passa pela bateria (eficiência de recarga da P-029): a produção necessária é {br(la['fator_recarga'], 3)} × a demanda.", "",
          f"O modelo de insolação vale até τ = {br(la['tau_max_modelo'], 0)}; acima disso usa-se esse limite, e o resultado fica otimista.", "",
          "| Cenário | τ | τ usado | Carga | Demanda (Wh/sol) | Área (m²) | Painel (kg) | Bateria (kg) | Total (kg) | Pior sol (Ls) |",
          "| :- | -: | -: | :- | -: | -: | -: | -: | -: | -: |"]
    for s in la["solar"]:
        md.append(f"| {s['cenario']} | {br(s['tau'], 1)} | {br(s['tau_usado'], 1)} | {s['carga']} | {br(s['demanda_wh_sol'])} | {br(s['area_m2'], 1)} | {br(s['painel_kg'])} | "
                  f"{br(s['bateria_kg'])} | {br(s['total_kg'])} | {br(s['pior_sol_ls'])}° |")
    sc, scs, sv, a6 = la["solar_com_sobrevivencia"], la["solar_com_sobrevivencia_sensibilidade"], la["sobrevivencia"], la["acima_do_modelo"]
    sb = sv["base"]
    md += ["", "### Opção C: solar com sobrevivência (linha de base)", "",
           f"Carga de sobrevivência na tempestade global (P-056): MAV {br(sb['mav_wh_sol'])} Wh/sol + aquecedores do lander "
           f"{br(sb['aquecedores_lander_wh_sol'])} Wh/sol (84 Wh/sol do Spirit × ({br(sv['plataforma_lander_kg'])} kg / 174 kg)^{br(sb['expoente'], 2)}) "
           f"+ eletrônica mínima {br(sb['eletronica_wh_sol'])} Wh/sol = {br(sb['total_wh_sol'])} Wh/sol. "
           f"Com escala linear na massa (sensibilidade): {br(sv['sensibilidade']['total_wh_sol'])} Wh/sol.", "",
           f"Painel e bateria para os dois casos (a maior área e a maior bateria; a área sai da {sc['dimensiona_area']}): "
           f"{br(sc['area_m2'], 1)} m², painel {br(sc['painel_kg'])} kg, bateria {br(sc['bateria_kg'])} kg, total {br(sc['total_kg'])} kg. "
           f"Sensibilidade com escala linear: {br(scs['area_m2'], 1)} m², total {br(scs['total_kg'])} kg (área da {scs['dimensiona_area']}).", "",
           f"Comparação do modelo com o Opportunity na tempestade de 2018 [F140] (razão de energia contra o sol de τ = {br(a6['tau_referencia'], 2)}; "
           "latitude do sítio, painel horizontal, poeira constante):", "",
           "| Sol | Data | τ | Razão medida | Razão do modelo | Diferença |", "| -: | :- | -: | -: | -: | -: |"]
    md += [f"| {c['sol']} | {c['data']} | {br(c['tau'], 1)} | {br(c['razao_medida'], 3)} | "
           + ("fora do modelo (τ > 6) | — |" if c["razao_modelo"] is None else f"{br(c['razao_modelo'], 3)} | {br(100 * c['diferenca_relativa'], 1)} % |")
           for c in la["comparacao_opportunity_2018"]]
    ab, as_ = a6["base"], a6["sensibilidade"]
    md += ["", f"Acima de τ = {br(la['tau_max_modelo'], 0)} (P-057): com τ = {br(a6['tau'], 1)} o Opportunity produziu {br(100 * a6['razao_medida'], 1)} % "
           f"da energia de τ = {br(a6['tau_referencia'], 2)}. Aplicada ao painel da opção C no pior sol da estada: {br(ab['energia_disponivel_wh_sol'])} Wh/sol "
           f"contra {br(ab['necessaria_wh_sol'])} Wh/sol necessários ({br(100 * ab['cobertura'])} %); a sobrevivência nessa condição exigiria "
           f"{br(ab['area_necessaria_m2'])} m². Sensibilidade (escala linear): {br(100 * as_['cobertura'])} %, {br(as_['area_necessaria_m2'])} m². "
           f"A duração da fase com τ > {br(la['tau_max_modelo'], 0)} e a ponte pela bateria não foram avaliadas.", "",
           f"Desfecho do único dado de voo acima de τ = {br(la['tau_max_modelo'], 0)}: {a6['desfecho_opportunity']}."]
    r = la["mmrtg"]
    s_ = r["sensibilidade_abastecimento"]
    md += ["", "Picos por sol (na bateria das duas opções): " + ", ".join(f"{k} {br(x, 1)} Wh" for k, x in la["picos_wh"].items())
           + f"; total {br(la['pico_total_wh'], 1)} Wh.", "", "### Alternativa A: MMRTG (condicionada à disponibilidade de Pu-238)", "",
           f"{r['unidades']} unidade(s): {br(r['potencia_fim_w'], 1)} W cada no fim da estada ({br(r['anos_do_lancamento_ao_fim'], 2)} anos depois do lançamento, "
           f"{br(100 * r['fracao_potencia_fim'], 1)} % da inicial), para {br(r['demanda_media_w'], 1)} W médios (sobra de {br(r['sobra_por_sol_wh'])} Wh/sol); "
           f"{br(r['massa_sem_margem_kg'])} kg sem margem + margem de {br(100 * r['margem_crescimento'], 1)} % + bateria dos picos {br(r['bateria_kg'], 1)} kg = "
           f"{br(r['massa_kg'])} kg; {br(r['potencia_termica_total_w'])} W térmicos; {br(r['pu238_g'])} g de Pu-238. "
           f"Sensibilidade com o abastecimento {br(s_['anos'] - r['anos_do_lancamento_ao_fim'], 0)} ano antes "
           f"do lançamento: {br(s_['potencia_fim_w'], 1)} W cada, {s_['unidades']} unidade(s).", "",
           f"Atividade do Pu-238: {br(r['nspm20']['atividade_tbq'])} TBq = {br(r['nspm20']['multiplo_a2'] / 1e6, 2)} × 10⁶ A2 "
           f"({br(r['nspm20']['vezes_o_limite_tier_i'], 1)} vezes o limite do Tier I do NSPM-20, {br(r['nspm20']['limite_tier_i_a2'] / 1e3)} mil A2): "
           f"{r['nspm20']['enquadramento']}.", "", "Disponibilidade de Pu-238:", ""]
    md += [f"- {x}" for x in la["pu238_disponibilidade"]]
    md += ["",
           "### Comparação com bases iguais (margens de crescimento e bateria dos picos nas duas fontes)", "",
           "| Opção | Massa (kg) | Área (m²) | Pu-238 | Tempestade global (inclusive τ > 6) | Degradação na estada |",
           "| :- | -: | -: | :- | :- | :- |",
           f"| **C. Solar com sobrevivência (linha de base)** | {br(sc['total_kg'])} | {br(sc['area_m2'], 1)} | — | sobrevive (MAV + lander, P-056) até τ = {br(la['tau_max_modelo'], 0)}; "
           f"com τ = {br(a6['tau'], 1)}, {br(100 * ab['cobertura'])} % da energia de sobrevivência (P-057) | poeira: fator {br(la['fator_poeira_fim'], 3)} no fim, sem limpeza |",
           f"| A. MMRTG × {r['unidades']} (alternativa condicionada) | {br(r['massa_kg'])} | — | {br(r['pu238_g'])} g; condicionada à disponibilidade "
           f"(fatos acima); acima do Tier I do NSPM-20 | não depende de τ | potência no fim {br(100 * r['fracao_potencia_fim'], 1)} % da inicial |",
           f"| B. Solar, céu claro | {br(la['solar'][0]['total_kg'])} | {br(la['solar'][0]['area_m2'], 1)} | — | não atravessa: com τ = {br(la['tau_max_modelo'], 0)} a energia "
           f"cai a {br(100 * la['fracao_energia_tau_max_sobre_claro'], 1)} % da de céu claro | "
           f"poeira: fator {br(la['fator_poeira_fim'], 3)} |",
           f"| D. Solar operando na tempestade | {br(la['solar'][2]['total_kg'])} | {br(la['solar'][2]['area_m2'], 1)} | — | opera até τ = {br(la['tau_max_modelo'], 0)}; "
           f"acima, ver a razão do Opportunity | poeira: fator {br(la['fator_poeira_fim'], 3)} |", "",
           "### Verificação da insolação diária contra a tabela do VL1 (22,3° N) [F56]", "",
           "A tabela é cálculo publicado (modelo de Appelbaum & Flood), não medida: a comparação verifica a implementação.", "",
           "| Ls | τ | Publicado (Wh/m², horas terrestres) | Calculado (Wh/m²) | Diferença |", "| -: | -: | -: | -: | -: |"]
    md += [f"| {c['ls']} | {br(c['tau'], 2)} | {br(c['hh_publicado_wh'])} | {br(c['hh_calculado_wh'])} | {br(100 * c['diferenca_relativa'], 1)} % |"
           for c in la["verificacao_vl1"]["pontos"]]
    md += ["", f"Maior diferença: {br(100 * la['verificacao_vl1']['maior_diferenca_relativa'], 1)} %.", ""]
    ob = o["orbitador"]
    md += ["## Orbitador", "", "Distância máxima ao Sol por fase (janelas do envelope e referência): "
           + ", ".join(f"{k} {br(x, 3)} UA" for k, x in ob["distancia_max_ua_por_fase"].items())
           + f"; afélio de Marte {br(ob['afelio_marte_ua'], 3)} UA. Eclipse máximo: "
           + ", ".join(f"{k} {br(x, 2)} h" for k, x in ob["eclipse_max_h"].items()) + ".", "",
           "| Modo (P-053) | Carga (W) | Distância (UA) | Eclipse (h) | Potência do painel na distância (W) | Painel sem margem (kg) | Energia no eclipse (Wh) |",
           "| :- | -: | -: | -: | -: | -: | -: |"]
    md += [f"| {m['modo']} | {br(m['carga_w'])} | {br(m['distancia_max_ua'], 3)} | {br(m['eclipse_h'], 2)} | {br(m['painel_w'])} | "
           f"{br(m['painel_kg_sem_margem'], 1)} | {br(m['bateria_wh'])} |" for m in ob["modos"]]
    a, p = ob["anterior"], ob["adotada"]
    md += ["", f"Modo dominante: {ob['modo_dominante']}.", "",
           "| | Carga (W) | Plataforma (kg) | Painel no afélio (W) | Bateria (Wh) | Orbitador injetado (kg) | Na órbita baixa (kg) |",
           "| :- | -: | -: | -: | -: | -: | -: |",
           f"| Anterior (510 W) | {br(a['carga_w'])} | {br(a['plataforma_kg'], 1)} | {br(a['painel_w_afelio'])} | {br(a['bateria_wh'])} | {br(a['orbitador_injetado_kg'])} | {br(a['leo_kg'])} |",
           f"| Adotada (P-028 = modo dominante da P-053) | {br(p['carga_w'])} | {br(p['plataforma_kg'], 1)} | {br(p['painel_w_afelio'])} | {br(p['bateria_wh'])} | {br(p['orbitador_injetado_kg'])} | {br(p['leo_kg'])} |",
           "", "A linha anterior usa as perdas e o apoapse atuais (sensibilidade, não o resultado da Etapa 3.4).", "",
           "Margens dos lançadores escolhidos para o orbitador (injeção direta, pior janela; órbita de encontro fixa), anterior → adotada: "
           + "; ".join(f"{k} {pc_(x['anterior'])} → {pc_(x['adotada'])}" for k, x in ob["margens_escolhidos"].items()) + ".", "",
           f"Sensibilidade da bateria com a profundidade de descarga do MRO ({br(100 * ob['bateria_dod_mro_wh']['profundidade_descarga'])} %, [F139]): "
           f"{br(ob['bateria_dod_mro_wh']['anterior'])} Wh (anterior) e {br(ob['bateria_dod_mro_wh']['adotada'])} Wh (adotada), contra "
           f"{br(a['bateria_wh'])} e {br(p['bateria_wh'])} Wh com 30 % (config)."]
    (SAIDA / "energia.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
