"""Portão da Etapa 7.2: rotas para o alvo do Fabio (aeroshell de 4,5 m, MAV deitado, Ø que contenha as saídas com parede).

(A) MAV melhorado na arquitetura atual: R-4D-11 44:1 nos dois estágios, Isp dos análogos (NÃO VALIDADO), tanques aninhados.
(B) Orbitador elétrico com encontro em órbita baixa (reabre o trade do ADR 0013, sem alterá-lo):
    B-c2: híbrido do ADR 0013 (captura e saída químicas, espiral verificada), pelas fórmulas de tools/orbitador_eletrico.py;
    B-b: elétrico em tudo, com massas fechadas aqui; trecho heliocêntrico quase circular, calculado, NÃO verificado.
Não muda premissa nem ADR.
Saída: results/etapa7.2/rotas_mav.yaml e .md

Uso: python tools/rotas_mav.py
"""

from __future__ import annotations

import copy
import datetime as dt
import math
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import comprimento_mav as cmv  # noqa: E402
import orbitador_eletrico as oe  # noqa: E402
from orbital import dimensionamento as dm  # noqa: E402
from orbital import foguete as fg  # noqa: E402
from orbital import hibrido as hb  # noqa: E402
from orbital import lancamento as lc  # noqa: E402
from orbital import motores as om  # noqa: E402
from orbital import veiculos as ve  # noqa: E402
from orbital.config import ler, nativo, parametros, v  # noqa: E402
from orbital.constantes import UA_KM  # noqa: E402
from orbital.massa_plataformas import plataforma_orbitador  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"
POL = 0.0254   # [F112] Apêndice B.8, PDF p. 62: polegada em metros
DIA = 86400.0
FATOR = {1: 1.0, 2: 2.0, 3: 1 + 2 / math.sqrt(3), 4: 1 + math.sqrt(2)}   # círculo mínimo de n círculos iguais


def br(x, n=3):
    return f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def sg(x, n=3):
    return f"{round(x, n) + 0.0:+,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def main():
    cad, ma, arq = ler("config/cad.yaml"), ler("results/etapa7.2/mav_arranjo.yaml"), ler("results/etapa2.5/arquitetura.yaml")
    ro = cad["rotas_mav"]
    p, po = parametros(), ler("config/parametros_orbitais.yaml")
    dcfg, scfg, mcfg, pcfg, ecfg, cu, lcfg = (ler(f"config/{x}.yaml") for x in ("dimensionamento", "superficie", "mav_propulsao", "plataformas", "eletrica", "carga_util", "lancadores"))
    mu, R = p.mu_marte, v(po["raio_marte_km"])
    f = 1 + v(dcfg["margem_dv"])
    forma = ro["alvo"]["aeroshell"]
    nt = {k: v(x) for k, x in cad["mav"]["comprimento_nao_tanque_m"].items()}
    t_par = v(cad["mav"]["espessura_parede_m"])
    d0 = v(cad["mav"]["diametro_opcoes_m"][cad["escolha"]["mav_diametro"]])
    caso = {c["diametro_m"]: c for c in ma["casos"]}
    ombro = {d: next(e for e in c["formas"][forma] if e["estacao"] == "ombro") for d, c in caso.items()}
    disponivel = {d: caso[d]["comprimento_m"] + 2 * ombro[d]["deitado_folga_m"] for d in caso}
    deck = {d: next(e for e in c["formas"][forma] if "P-094" in e["estacao"]) for d, c in caso.items()}
    folga_ombro = lambda d, L: (disponivel[d] - L) / 2  # noqa: E731
    folga_deck = lambda d, L: deck[d]["deitado_folga_m"] + (caso[d]["comprimento_m"] - L) / 2  # noqa: E731
    g = ler("results/etapa3.1/queima_finita.yaml")["g_marte_m_s2"]
    tm = om.catalogo()["R-4D-11"]["empuxo_n"]
    ms = ler("results/etapa1.3/missoes.yaml")
    cand = {c["id"]: c for c in ms["candidatas"]}
    ref = cand[ler("config/missao_referencia.yaml")["missao_referencia"]["id"]]
    janelas = [cand[w["missao"]] for w in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()]
    area = math.pi * v(cad["aeroshell"]["opcoes"]["m2020"]["diametro_m"]) ** 2 / 4
    rd = cad["r4d11_variantes"]
    fr = v(rd["a_frente_da_flange_pol"])
    motor = {k: (rd[k]["flange_a_saida_pol"] + fr) * POL for k in ("44:1", "164:1")}
    saida = {k: rd[k]["diametro_saida_pol"] * POL for k in ("44:1", "164:1")}
    margem_vc4 = lambda m: lc.pior_margem_a("Vulcan VC4", m, janelas, lcfg)[0]  # noqa: E731
    margem_fh = lambda m: lc.pior_margem_a("Falcon Heavy (descartável)", m, janelas, lcfg)[0]  # noqa: E731

    def linha_mav(rot, est, d, n, variante, nt_, aninhado, lan):
        L = cmv.comprimento(d, est, nt_, cad, aninhado=aninhado)
        circ = FATOR[n] * saida[variante]
        glom = est[0]["massa_inicial_kg"]
        return {"rotulo": rot, "diametro_m": d, "n_motores": n, "variante": variante, "aninhado": aninhado, "glom_kg": glom, "propelente_kg": sum(e["propelente_kg"] for e in est),
                "comprimento_m": L, "disponivel_m": disponivel[d], "folga_deitado_m": folga_ombro(d, L), "folga_deitado_com_deck_m": folga_deck(d, L),
                "circulo_saidas_m": circ, "folga_radial_bocais_m": (d - 2 * t_par - circ) / 2, "empuxo_peso": n * tm / (glom * g),
                "lander_injetado_kg": lan["injetada_kg"], "margem_vulcan_vc4": margem_vc4(lan["injetada_kg"]), "massa_por_area_kg_m2": lan["massa_entrada_kg"] / area}

    # ---------------- base
    h0p, h0a = arq_alt()
    lan0 = ve.lander(R + h0p, R + h0a, detalhe=True)
    base = linha_mav("Base: 4 × 164:1, Ø atual", lan0["mav_estagios"], d0, 4, "164:1", nt, False, lan0)
    base.update(_orbitador_base(arq, margem_fh, h0p, h0a, lan0, f))
    nt_real = {**nt, "motores_estagio_1": motor["164:1"], "motor_estagio_2": motor["164:1"]}
    base_real = linha_mav("Base com a P-086 só pelo motor 164:1 [F228], sem estrutura de empuxo (a P-086 não muda)", lan0["mav_estagios"], d0, 4, "164:1", nt_real, False, lan0)

    # ---------------- rota A
    nt44 = {**nt, "motores_estagio_1": motor["44:1"], "motor_estagio_2": motor["44:1"]}
    op = ler("results/etapa2.2/mav_propulsao.yaml")["melhor_opcao"]
    rota_a = []
    for isp in ro["rota_a"]["isp_s"]:
        m2 = copy.deepcopy(mcfg)
        m2["opcoes"][op]["isp_s"] = [isp, isp]
        lan = ve.lander(R + h0p, R + h0a, mcfg=m2, detalhe=True)
        rota_a.append({"isp_s": isp, "so_44": linha_mav(f"44:1, Isp {isp} s", lan["mav_estagios"], d0, 4, "44:1", nt44, False, lan),
                       "com_aninhados": linha_mav(f"44:1 e aninhados, Isp {isp} s", lan["mav_estagios"], d0, 4, "44:1", nt44, True, lan)})

    m3 = copy.deepcopy(mcfg)
    isp_ref = v(ro["rota_a"]["isp_referencia"])
    m3["opcoes"][op]["isp_s"] = [isp_ref, isp_ref]
    lan_ref = ve.lander(R + h0p, R + h0a, mcfg=m3, detalhe=True)
    ref_a = {"so_44": linha_mav(f"Referência, Isp {isp_ref:g} s: só 44:1", lan_ref["mav_estagios"], d0, 4, "44:1", nt44, False, lan_ref),
             "com_aninhados": linha_mav(f"Referência, Isp {isp_ref:g} s: 44:1 e aninhados", lan_ref["mav_estagios"], d0, 4, "44:1", nt44, True, lan_ref)}

    # ---------------- rota B: órbitas e MAV
    n_b = int(ro["rota_b"]["n_motores_mav"])
    d_b = min(d for d in caso if d - 2 * t_par >= FATOR[n_b] * saida["164:1"])

    def mav_circular(h):
        lan = ve.lander(R + h, R + h, detalhe=True)
        return lan, cmv.comprimento(d_b, lan["mav_estagios"], nt_real, cad)
    h_baixa = v(scfg["sitio_e_encontro"]["orbita_baixa_alt_km"])
    lo, hi = h_baixa, float(h0a)
    if mav_circular(lo)[1] > disponivel[d_b]:
        raise ValueError("o MAV da rota B não cabe nem na órbita baixa")
    for _ in range(int(ro["rota_b"]["passos_h_max"])):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if mav_circular(mid)[1] <= disponivel[d_b] else (lo, mid)
    h_max = math.floor(lo)
    orbitas_b = [("Órbita do MSR", h_baixa, ro["rota_b"]["orbita_baixa"]["fonte"]), ("Maior que cumpre o alvo", float(h_max), ro["rota_b"]["motivo_segunda_orbita"])]
    mav_b = {}
    for rot, h, _ in orbitas_b:
        lan, _ = mav_circular(h)
        mav_b[h] = {**linha_mav(f"{n_b} × 164:1, Ø {br(d_b, 2)} m, {br(h, 0)} × {br(h, 0)} km", lan["mav_estagios"], d_b, n_b, "164:1", nt_real, False, lan), "dv_mav_com_margem_m_s": 1e3 * f * lan["dv_subida_mav_km_s"],
                    "com_p086_atual": linha_mav(f"Idem, com a P-086 atual", lan["mav_estagios"], d_b, n_b, "164:1", nt, False, lan)}

    # ---------------- rota B: orbitador
    a_caso, jan, piores = dm.casos(dcfg, p)
    perdas = ler("results/etapa3.1/perdas_calculadas.yaml")["perda_km_s"]
    orc_ins, orc_ret = dm.orcamento(piores["insercao_marte"], dcfg, p), dm.orcamento(piores["retorno"], dcfg, p)
    ate_marte, capsula, descartado = dm.carga(dcfg["caso_base"]["carga_util"], cu, float(dcfg["caso_base"]["acrescimo_capsula"]))
    est = dcfg["estagios"]
    isp_q, eps_i, eps_r = v(est["insercao_marte"]["isp_s"]), v(est["insercao_marte"]["fracao_estrutural"]), v(est["retorno"]["fracao_estrutural"])
    t_enc = v(ecfg["operacao"]["tempo_encontro_dias"]) * DIA
    vz = ecfg["varredura"]
    alts_c = oe.grade(vz["captura_alt_km"]["valor"])
    op_s = ler("results/etapa4.4/operacao_superficie.yaml")
    chegada = dt.date.fromisoformat(op_s["chegada"])
    conj_ini = dt.date.fromisoformat(op_s["inicio_conjuncao"])
    conj_fim = _fim_conjuncao()
    partida = dt.date.fromisoformat(ler("results/etapa4.3/comunicacao.yaml")["estada"][1])
    lancs = [dt.date.fromisoformat(x["lancamento"]) for x in op_s["linha_do_tempo"] if x["atende_folga_minima"]]
    lanc_cedo, lanc_tarde = min(lancs), max(lancs)

    def tempo(h_e, t_d, t_s):
        """Linha do tempo na missão de referência: quando a espiral acaba e se ela cruza a conjunção."""
        pronto = chegada + dt.timedelta(days=math.ceil(t_d))
        inicio_sub = max(pronto, lanc_cedo) + dt.timedelta(days=round(t_enc / DIA))
        fim_sub = inicio_sub + dt.timedelta(days=math.ceil(t_s))
        return {"pronto_no_encontro": pronto.isoformat(), "pronto_antes_do_ultimo_lancamento": pronto <= lanc_tarde, "folga_ao_ultimo_lancamento_dias": (lanc_tarde - pronto).days,
                "inicio_subida_mais_cedo": inicio_sub.isoformat(), "fim_subida_mais_cedo": fim_sub.isoformat(), "folga_a_partida_dias": (partida - fim_sub).days,
                "subida_cruza_conjuncao": inicio_sub <= conj_fim and fim_sub >= conj_ini, "espera_lancamento_tardio_termina": (lanc_tarde + dt.timedelta(days=round(t_enc / DIA) + math.ceil(t_s))).isoformat()}

    def c2(se, nome, h_e, plat):
        r_e = R + h_e
        melhor = None
        for h_c in alts_c:
            if h_c <= h_e:
                continue
            r_c = R + float(h_c)
            dv = {"correcoes_ida": f * orc_ins["correcoes_ida"], "captura": f * (max(hb.dv_hiperbole_circular(mu, w["vinf_chegada_marte_km_s"], r_c) for w in janelas) + perdas["captura_marte"]),
                  "descida": f * hb.dv_circular(mu, r_c, r_e), "encontro": f * orc_ret["encontro_e_manutencao_marte"], "subida": f * hb.dv_circular(mu, r_e, r_c),
                  "saida": f * (max(hb.dv_hiperbole_circular(mu, math.sqrt(w["c3l_partida_marte_km2_s2"]), r_c) for w in janelas) + perdas["saida_marte"]),
                  "correcoes_volta": f * orc_ret["correcoes_volta"], "desvio": f * orc_ret["desvio_orbitador"]}
            m = hb.massas(dv, se, isp_q, eps_i, eps_r, ate_marte - descartado - capsula + plat, descartado, capsula, tol_kg=v(vz["convergencia_massas_kg"]))
            _, t_d, _, _ = hb.tempos_espiral(mu, R, r_c, r_e, m["massa_antes_descida_kg"], se, fator_dv=f)
            _, t_s, _, _ = hb.tempos_espiral(mu, R, r_e, r_c, m["massa_antes_subida_kg"], se, fator_dv=f)
            folga = min(w["em_marte_dias"] for w in janelas) - (t_d + t_enc + t_s) / DIA
            vida = ecfg["propulsores"][nome]["throughput_kg"]
            xe = m["eletrico"]["xenonio_kg"] / se.n_ativos
            if folga >= 0 and (vida is None or xe <= v(vida)) and (melhor is None or m["injetada_kg"] < melhor["orbitador_injetado_kg"]):
                melhor = {"captura_alt_km": float(h_c), "orbitador_injetado_kg": m["injetada_kg"], "xenonio_kg": m["eletrico"]["xenonio_kg"], "descida_dias": t_d / DIA, "subida_dias": t_s / DIA,
                          "folga_estada_dias": folga, "dv_eletrico_km_s": dv["descida"], "dv_captura_km_s": dv["captura"], "dv_saida_km_s": dv["saida"]}
        return melhor

    # B-b: elétrico em tudo, de trás para a frente
    rt, rm = UA_KM, v(mcfg["cruzeiro"]["distancia_marte_ua"]) * UA_KM
    dv_h = f * hb.dv_circular(hb_mu_sol(), rt, rm)
    hill = ler("results/etapa3.1/queima_finita.yaml")["raio_hill_km"]

    def eletrico(se, h_e, plat):
        r_e = R + h_e
        dv_e = f * hb.dv_circular(mu, hill, r_e)
        c, cx = isp_q * fg.G0, se.isp_s * fg.G0
        k_r, k_x = eps_r / (1 - eps_r), se.inerte_por_kg_xenonio
        carga = ate_marte - descartado - capsula + plat
        pr = px = 0.0
        for _ in range(200):
            mf = carga + se.massa_seca_kg() + k_r * pr + k_x * px
            b_desv = mf * math.exp(f * orc_ret["desvio_orbitador"] / c)
            a_cap = b_desv + capsula
            b_volta = a_cap * math.exp(dv_h / cx)
            b_sub = b_volta * math.exp(dv_e / cx)
            b_enc = b_sub * math.exp(f * orc_ret["encontro_e_manutencao_marte"] / c)
            a_desc = b_enc + descartado
            b_desc = a_desc * math.exp(dv_e / cx)
            b_ida = b_desc * math.exp(dv_h / cx)
            nr = (b_desv - mf) + (b_enc - b_sub)
            nx = (b_volta - a_cap) + (b_sub - b_volta) + (b_desc - a_desc) + (b_ida - b_desc)
            if abs(nr - pr) < v(vz["convergencia_massas_kg"]) and abs(nx - px) < v(vz["convergencia_massas_kg"]):
                break
            pr, px = nr, nx
        else:
            raise RuntimeError("massas do orbitador elétrico não convergiram")
        _, t_d, _, _ = hb.tempos_espiral(mu, R, hill, r_e, b_desc, se, fator_dv=f)
        _, t_s, _, _ = hb.tempos_espiral(mu, R, r_e, hill, b_sub, se, fator_dv=f)
        t_ida = b_ida / se.vazao_kg_s * (1 - math.exp(-dv_h / cx)) / DIA
        t_volta = b_volta / se.vazao_kg_s * (1 - math.exp(-dv_h / cx)) / DIA
        return {"orbitador_injetado_kg": b_ida, "xenonio_kg": px, "xenonio_por_propulsor_kg": px / se.n_ativos, "descida_dias": t_d / DIA, "subida_dias": t_s / DIA, "empuxo_ida_dias": t_ida, "empuxo_volta_dias": t_volta,
                "folga_estada_dias": min(w["em_marte_dias"] for w in janelas) - (t_d + t_enc + t_s) / DIA, "dv_espiral_km_s": dv_e, "dv_heliocentrico_km_s": dv_h, "total_empuxo_dias": t_ida + t_volta + (t_d + t_s) / DIA}

    # o híbrido reproduz a Etapa 3.3 na altitude que ela escolheu
    esc33 = ler("results/etapa3.3/orbitador_eletrico.yaml")["hibrido_c2"]["NSTAR"]
    e33 = next(x for x in esc33["por_n"] if x["n_ativos"] == esc33["n_minimo"])["escolha"]
    x33 = c2(oe.sistema("NSTAR", esc33["n_minimo"], ecfg, pcfg), "NSTAR", e33["encontro_alt_km"], e33["plataforma_orbitador_kg"])
    conf33 = {"etapa_3_3_kg": e33["orbitador_injetado_kg"], "aqui_kg": x33["orbitador_injetado_kg"], "etapa_3_3_descida_dias": e33["tempo_descida_dias"], "aqui_descida_dias": x33["descida_dias"]}

    rota_b = []
    for rot, h, justif in orbitas_b:
        plat = plataforma_orbitador(pcfg, po, h, h)
        por_prop = {}
        for nome in ecfg["propulsores"]:
            viaveis = []
            for n in range(1, int(vz["n_ativos_max"]["valor"]) + 1):
                se = oe.sistema(nome, n, ecfg, pcfg)
                x = c2(se, nome, h, plat)
                if x:
                    viaveis.append({**x, "n_ativos": n, "potencia_kw": se.potencia_total_w / 1e3, "margem_falcon_heavy": margem_fh(x["orbitador_injetado_kg"]), "tempo": tempo(h, x["descida_dias"], x["subida_dias"])})
            mais_leve = min(viaveis, key=lambda x: x["orbitador_injetado_kg"]) if viaveis else None
            b_b = []
            for n in range(1, int(vz["n_ativos_max"]["valor"]) + 1):
                se = oe.sistema(nome, n, ecfg, pcfg)
                e_ = eletrico(se, h, plat)
                vida = ecfg["propulsores"][nome]["throughput_kg"]
                mg = margem_fh(e_["orbitador_injetado_kg"])
                pronto = dt.date.fromisoformat(ref["partida_terra"]) + dt.timedelta(days=math.ceil(e_["empuxo_ida_dias"] + e_["descida_dias"]))
                b_b.append({**e_, "n_ativos": n, "potencia_kw": se.potencia_total_w / 1e3, "margem_falcon_heavy": mg, "vida_kg": v(vida) if vida else None,
                            "dentro_da_vida": vida is None or e_["xenonio_por_propulsor_kg"] <= v(vida), "vida_conhecida": vida is not None,
                            "fecha_estada_e_lancador": e_["folga_estada_dias"] >= 0 and mg >= 0, "pronto_no_encontro": pronto.isoformat(), "pronto_antes_do_ultimo_lancamento": pronto <= lanc_tarde,
                            "ida_referencia_dias": ref["ida_dias"], "volta_referencia_dias": ref["volta_dias"]})
            fecha = [x for x in b_b if x["fecha_estada_e_lancador"] and x["dentro_da_vida"]]
            por_prop[nome] = {"c2_mais_leve": mais_leve, "c2_n_viaveis": [x["n_ativos"] for x in viaveis], "eletrico": b_b,
                              "eletrico_primeiro_que_fecha": fecha[0] if fecha else None, "eletrico_maior_n": b_b[-1]}
        rota_b.append({"rotulo": rot, "altitude_km": h, "justificativa": justif, "plataforma_kg": plat, "mav": mav_b[h], "propulsores": por_prop})

    out = nativo({"gerado_por": "tools/rotas_mav.py", "natureza": "dados para o portão; não muda premissa nem ADR", "alvo": ro["alvo"], "disponivel_deitado_m": {str(d): disponivel[d] for d in caso},
                  "base": base, "base_real": base_real, "rota_a": rota_a, "rota_a_referencia": ref_a, "rota_a_ressalva": ro["rota_a"]["ressalva_analogos"], "isp_referencia_fonte": ro["rota_a"]["isp_referencia"]["fonte"], "conferencia_etapa_3_3": conf33,
                  "empuxo_peso_opcao_c": next(a["empuxo_peso_marte"] for a in ler("results/etapa7.2/bocais_alternativas.yaml")["alternativas"] if a["id"] == "C"), "fase_raan_dias": v(ro["rota_b"]["fase_raan_dias"]), "motivo_fim": ro["rota_b"]["motivo_segunda_orbita_fim"], "folga_min_conjuncao_dias": v(ler("config/operacao_superficie.yaml")[next(k for k, x in ler("config/operacao_superficie.yaml").items() if isinstance(x, dict) and "folga_min_conjuncao_dias" in x)]["folga_min_conjuncao_dias"]), "rota_a_fonte": ro["rota_a"]["tanques_aninhados"], "rota_b": rota_b, "diametro_b_m": d_b, "n_motores_b": n_b, "bowles_empuxo_peso": ro["rota_b"]["bowles_empuxo_peso"],
                  "missao": {"chegada": chegada.isoformat(), "partida": partida.isoformat(), "conjuncao_inicio": conj_ini.isoformat(), "conjuncao_fim": conj_fim.isoformat(), "lancamento_mav_mais_cedo": lanc_cedo.isoformat(), "lancamento_mav_mais_tarde": lanc_tarde.isoformat(), "encontro_dias": t_enc / DIA, "estada_minima_dias": min(w["em_marte_dias"] for w in janelas), "partida_terra": ref["partida_terra"], "ida_dias": ref["ida_dias"], "volta_dias": ref["volta_dias"]},
                  "referencia_m2020_kg_m2": v(cad["aeroshell"]["opcoes"]["m2020"]["massa_entrada_kg"]) / area, "folgas_coifa_vulcan_m": ler("results/etapa7.2/parametros.yaml")["conferencias"]["lander_vulcan"]["por_forma"][forma],
                  "adr_0013": "Na missão de referência (414 dias em Marte) e com as leis de guiagem verificadas, nenhuma opção elétrica fecha massa e tempo. Uma missão de estada longa, como a do ERO, poderia mudar isso, mas exigiria outra missão de referência e uma guiagem otimizada, não estudadas."})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "rotas_mav.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def lin_mav(x):
    return f"| {x['rotulo']} | {br(x['glom_kg'], 1)} | {br(x['comprimento_m'])} | {sg(x['folga_deitado_m'])} | {sg(x['folga_deitado_com_deck_m'])} | {br(x['circulo_saidas_m'])} | {sg(x['folga_radial_bocais_m'])} | {br(x['empuxo_peso'], 2)} | {br(x['massa_por_area_kg_m2'], 0)} | {sg(100 * x['margem_vulcan_vc4'], 1)} % |"


CAB = ["| Caso | GLOM (kg) | Comprimento (m) | Folga deitado, ombro (m) | Folga deitado, ombro + deck (m) | Círculo das saídas (m) | Folga radial dos bocais, com parede (m) | Empuxo/peso em Marte | Massa por área (kg/m²) | Margem no Vulcan VC4 |", "| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |"]


def escreve_md(o):
    b, mi = o["base"], o["missao"]
    fc = o["folgas_coifa_vulcan_m"]
    md = ["# Portão da 7.2: rotas para o alvo de aeroshell de 4,5 m (gerado por tools/rotas_mav.py)", "",
          "Dados para o portão. Nenhuma premissa nem ADR muda, e a decisão é do Fabio. O que usa análogo ou leitura está marcado NÃO VALIDADO.", "",
          f"**Alvo:** {o['alvo']['descricao']}. Coifa do Vulcan com 4,5 m: {sg(fc['folga_radial_vertice_m'])} e {sg(fc['folga_sem_afunilamento_vertice_m'])} m, nas duas leituras da figura. Comprimento máximo deitado por Ø, com a base no ombro: "
          + "; ".join(f"Ø {br(float(k), 2)} m, {br(x, 2)} m" for k, x in o["disponivel_deitado_m"].items()) + ". Com o deck (P-094) sob o MAV, o limite em Ø " + br(b["diametro_m"], 2) + " m cai " + br(2 * (b["folga_deitado_m"] - b["folga_deitado_com_deck_m"]), 2) + " m; por isso as duas folgas aparecem. A folga é por extremidade: (disponível − comprimento) / 2. \"Motor real\" é a P-086 só com o motor de [F228] nos dois estágios, sem estrutura de empuxo: um limite inferior do comprimento.", "",
          "## Rota A: MAV melhorado, arquitetura atual", "",
          f"R-4D-11 44:1 nos dois estágios; a P-086 segue o motor do [F228]; o MAV é redimensionado para cada Isp. **Tanques aninhados:** {o['rota_a_fonte']['fonte']}. Ressalva: {o['rota_a_fonte']['ressalva']}. Massa e empuxo do 44:1 são os do catálogo (NÃO VALIDADO). Isp NÃO VALIDADO: análogos.", ""] + CAB
    md.append(lin_mav(b))
    md.append(lin_mav(o["base_real"]))
    for x in o["rota_a"]:
        md.append(lin_mav(x["so_44"]))
    for x in o["rota_a"]:
        md.append(lin_mav(x["com_aninhados"]))
    md.append(lin_mav(o["rota_a_referencia"]["so_44"]))
    md.append(lin_mav(o["rota_a_referencia"]["com_aninhados"]))
    md += ["", f"**Ressalva sobre a faixa:** {o['rota_a_ressalva']} O caso de referência usa o R-4D do Apollo ({o['isp_referencia_fonte']}), fora da faixa pedida, para mostrar o efeito de um Isp menor. Isp {br(o['rota_a'][-1]['isp_s'], 0)} s fica acima do 164:1 do mesmo motor, por isso o GLOM dele sai menor que o da base.", "",
           "O Δv de subida vem de [F46], calculado com empuxo/peso de " + br(o["bowles_empuxo_peso"]["valor"], 1) + f" na decolagem ({o['bowles_empuxo_peso']['fonte']}). Todos os casos aqui têm empuxo/peso menor, e a perda gravitacional maior disso não está modelada, nem na base.", "",
           "## Rota B: orbitador elétrico e encontro em órbita baixa", "",
           "### MAV", "",
           f"{o['n_motores_b']} × R-4D-11 164:1, Ø {br(o['diametro_b_m'], 2)} m, o menor da varredura que contém as saídas com parede. Comprimento com o motor real nos dois estágios, a mesma base da rota A. **Esta é a configuração da opção C, descartada pelo Fabio** " + f"por empuxo/peso de {br(o['empuxo_peso_opcao_c'], 2)} no GLOM atual. Ela só passa de 1 aqui porque o GLOM cai, o que depende de reabrir o ADR 0013. Além disso, {o['motivo_fim']}."]
    md += [""] + CAB
    for r in o["rota_b"]:
        md.append(lin_mav(r["mav"]))
        md.append(lin_mav(r["mav"]["com_p086_atual"]))
    md += ["", "| Órbita | Altitude (km) | Δv do MAV, com margem (m/s) | Por que esta órbita |", "| :- | -: | -: | :- |"]
    for r in o["rota_b"]:
        md.append(f"| {r['rotulo']} | {br(r['altitude_km'], 0)} | {br(r['mav']['dv_mav_com_margem_m_s'], 0)} | {r['justificativa']} |")
    md += ["", "### Orbitador híbrido (c2 do ADR 0013): captura e saída químicas, espiral elétrica verificada", "",
           f"O mais leve que cabe na menor estada das quatro janelas, varrendo a altitude de captura e o número de propulsores. Massa e margem pela regra (iii). A folga não inclui a fase de RAAN de {br(o['fase_raan_dias'], 0)} d (ADR 0013, item 6). Conferência com a Etapa 3.3, na altitude dela: {br(o['conferencia_etapa_3_3']['etapa_3_3_kg'], 0)} e {br(o['conferencia_etapa_3_3']['aqui_kg'], 0)} kg.", "",
           "| Órbita (km) | Propulsor | Ativos | Potência (kW) | Captura (km) | Orbitador (kg) | Xenônio (kg) | Descida (d) | Subida (d) | Folga na estada (d) | Margem no Falcon Heavy | Em órbita de encontro | Chega antes do último lançamento? | Subida cruza a conjunção? |", "| -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | :- | :- |"]
    for r in o["rota_b"]:
        for nome, q in r["propulsores"].items():
            x = q["c2_mais_leve"]
            if not x:
                md.append(f"| {br(r['altitude_km'], 0)} | {nome} | não cabe no tempo | | | | | | | | | | | |")
                continue
            t = x["tempo"]
            md.append(f"| {br(r['altitude_km'], 0)} | {nome} | {x['n_ativos']} | {br(x['potencia_kw'], 1)} | {br(x['captura_alt_km'], 0)} | {br(x['orbitador_injetado_kg'], 0)} | {br(x['xenonio_kg'], 0)} | {br(x['descida_dias'], 0)} | {br(x['subida_dias'], 0)} | {br(x['folga_estada_dias'], 0)} | {sg(100 * x['margem_falcon_heavy'], 1)} % | {t['pronto_no_encontro']} | {'sim' if t['pronto_antes_do_ultimo_lancamento'] else '**não**'} ({t['folga_ao_ultimo_lancamento_dias']} d) | {'sim' if t['subida_cruza_conjuncao'] else 'não'} |")
    md += ["", "### Orbitador só elétrico (opção b do ADR 0013): calculado, NÃO verificado", "",
           f"Massas fechadas aqui, sem estágio químico de captura. Trecho heliocêntrico quase circular, com a margem de Δv: não é trajetória otimizada nem traz janela nova. **A conta é de ordem de grandeza e o sentido do erro é desconhecido:** a margem cobra os C3 das janelas atuais, mas o Δv não dá crédito a esse v∞ (o que piora o tempo), e não há fasagem, ciclo de trabalho nem correções (o que melhora). As datas valem para crédito zero de C3 e partida em {mi['partida_terra']}, e não decidem o trade. A folga conta a estada de outra chegada, então pode não bater com as datas, e não inclui a fase de RAAN. Primeiro número de propulsores que fecha estada e lançador, e o maior da varredura. Vida do XIPS-25 não achada: conta como não limitante.", "",
           "| Órbita (km) | Propulsor | Caso | Ativos | Potência (kW) | Orbitador (kg) | Xenônio por propulsor (kg) | Vida (kg) | Empuxo na ida (d) | Empuxo na volta (d) | Descida (d) | Subida (d) | Folga na estada (d) | Margem no Falcon Heavy | Em órbita de encontro, partindo em " + mi["partida_terra"] + " | Chega antes do último lançamento? |", "| -: | :- | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | :- |"]
    for r in o["rota_b"]:
        for nome, q in r["propulsores"].items():
            casos = ([("primeiro que fecha", q["eletrico_primeiro_que_fecha"])] if q["eletrico_primeiro_que_fecha"] else [("nenhum fecha; o maior", q["eletrico_maior_n"])]) if not q["eletrico_primeiro_que_fecha"] or q["eletrico_primeiro_que_fecha"]["n_ativos"] == q["eletrico_maior_n"]["n_ativos"] else [("primeiro que fecha", q["eletrico_primeiro_que_fecha"]), ("o maior", q["eletrico_maior_n"])]
            for rot, e in casos:
                md.append(f"| {br(r['altitude_km'], 0)} | {nome} | {rot} | {e['n_ativos']} | {br(e['potencia_kw'], 1)} | {br(e['orbitador_injetado_kg'], 0)} | {br(e['xenonio_por_propulsor_kg'], 0)} | {br(e['vida_kg'], 0) if e['vida_kg'] else 'não achada'} | {br(e['empuxo_ida_dias'], 0)} | {br(e['empuxo_volta_dias'], 0)} | {br(e['descida_dias'], 0)} | {br(e['subida_dias'], 0)} | {br(e['folga_estada_dias'], 0)} | {sg(100 * e['margem_falcon_heavy'], 1)} % | {e['pronto_no_encontro']} | {'sim' if e['pronto_antes_do_ultimo_lancamento'] else '**não**'} |")
    md += ["", "### Linha do tempo da missão de referência", "",
           f"Chegada {mi['chegada']}; partida {mi['partida']}; viagens de {br(mi['ida_dias'], 0)} e {br(mi['volta_dias'], 0)} d; encontro de {br(mi['encontro_dias'], 0)} d. Conjunção de {mi['conjuncao_inicio']} a {mi['conjuncao_fim']}. Lançamento do MAV, dentro da folga mínima de {br(o['folga_min_conjuncao_dias'], 0)} d do ADR 0018: de {mi['lancamento_mav_mais_cedo']} a {mi['lancamento_mav_mais_tarde']}. "
           "O orbitador precisa estar em órbita antes desse lançamento. Hoje, com o químico, ele já chega pronto. Cruzar a conjunção significa operar a espiral sem o enlace normal com a Terra no período.", "",
           "### Por que o ADR 0013 rejeitou o elétrico, e se ainda vale", "",
           f"**Conclusão do ADR:** \"{o['adr_0013']}\"", "",
           "- **Híbrido c2:** continua valendo. A captura química em órbita baixa custa caro, e o orbitador fica muitas vezes acima do lançador.",
           "- **Só elétrico:** o ADR só o estimou em ordem de grandeza. Com as massas fechadas, a massa pode caber, mas pede dezenas de kW, xenônio além da vida conhecida no NSTAR e sem vida publicada no XIPS-25. Nesta conta não chega a tempo do lançamento do MAV, com crédito zero de C3 e a partida atual; isso é ordem de grandeza e não decide. O que continua de pé é a outra parte do ADR: exigiria outra missão de referência e outra guiagem, não estudadas.", "",
           "## Tabela final: A × B × base", "",
           "| Grandeza | Base | A: 44:1 e aninhados, 304 a 314 s | B: híbrido c2, " + br(o["rota_b"][0]["altitude_km"], 0) + " a " + br(o["rota_b"][1]["altitude_km"], 0) + " km | B: só elétrico, só XIPS-25, sem vida conhecida, NÃO verificado |", "| :- | :- | :- | :- | :- |"]
    an = [x["com_aninhados"] for x in o["rota_a"]]
    rb = o["rota_b"]
    faixa = lambda vals, n=3, f_=br: f"{f_(min(vals), n)} a {f_(max(vals), n)}"  # noqa: E731
    mavs = [r["mav"] for r in rb]
    c2s = [q["c2_mais_leve"] for r in rb for q in r["propulsores"].values() if q["c2_mais_leve"]]
    els = [q["eletrico_primeiro_que_fecha"] for r in rb for q in r["propulsores"].values() if q["eletrico_primeiro_que_fecha"]]
    el_txt = lambda k, n=0, f_=br: faixa([x[k] for x in els], n, f_) if els else "nenhum fecha"  # noqa: E731
    md += [f"| Δv do MAV (m/s) | {br(b['dv_mav_com_margem_m_s'], 0)} | {br(b['dv_mav_com_margem_m_s'], 0)} | {faixa([x['dv_mav_com_margem_m_s'] for x in mavs], 0)} | a mesma do híbrido |",
           f"| GLOM (kg) | {br(b['glom_kg'], 1)} | {faixa([x['glom_kg'] for x in an], 1)} | {faixa([x['glom_kg'] for x in mavs], 1)} | a mesma do híbrido |",
           f"| Comprimento, com o motor real (m) | {br(o['base_real']['comprimento_m'])} | {faixa([x['comprimento_m'] for x in an])} | {faixa([x['comprimento_m'] for x in mavs])} | a mesma do híbrido |",
           f"| Folga deitado, ombro, com o motor real (m) | {sg(o['base_real']['folga_deitado_m'])} | {faixa([x['folga_deitado_m'] for x in an], 3, sg)} | {faixa([x['folga_deitado_m'] for x in mavs], 3, sg)} | a mesma do híbrido |",
           f"| Folga deitado, ombro + deck, com o motor real (m) | {sg(o['base_real']['folga_deitado_com_deck_m'])} | {faixa([x['folga_deitado_com_deck_m'] for x in an], 3, sg)} | {faixa([x['folga_deitado_com_deck_m'] for x in mavs], 3, sg)} | a mesma do híbrido |",
           f"| Folga radial dos bocais, com parede (m) | {sg(b['folga_radial_bocais_m'])} | {sg(an[0]['folga_radial_bocais_m'])} | {sg(mavs[0]['folga_radial_bocais_m'])} | a mesma do híbrido |",
           f"| Empuxo/peso em Marte | {br(b['empuxo_peso'], 2)} | {faixa([x['empuxo_peso'] for x in an], 2)} | {faixa([x['empuxo_peso'] for x in mavs], 2)} | a mesma do híbrido |",
           f"| Massa por área, 4,5 m (kg/m²; Mars 2020: {br(o['referencia_m2020_kg_m2'], 0)}) | {br(b['massa_por_area_kg_m2'], 0)} | {faixa([x['massa_por_area_kg_m2'] for x in an], 0)} | {faixa([x['massa_por_area_kg_m2'] for x in mavs], 0)} | a mesma do híbrido |",
           f"| Orbitador (kg) | {br(b['orbitador_injetado_kg'], 0)} | {br(b['orbitador_injetado_kg'], 0)} | {faixa([x['orbitador_injetado_kg'] for x in c2s], 0)} | {el_txt('orbitador_injetado_kg')} |",
           f"| Potência elétrica (kW) | — | — | {faixa([x['potencia_kw'] for x in c2s], 1)} | {el_txt('potencia_kw', 1)} |",
           f"| Margem no Falcon Heavy | {sg(100 * b['margem_falcon_heavy'], 1)} % | {sg(100 * b['margem_falcon_heavy'], 1)} % | {faixa([100 * x['margem_falcon_heavy'] for x in c2s], 1, sg)} % | {el_txt('margem_falcon_heavy') if not els else faixa([100 * x['margem_falcon_heavy'] for x in els], 1, sg) + ' %'} |",
           f"| Espiral de descida e de subida (d) | — | — | {faixa([x['descida_dias'] for x in c2s], 0)} e {faixa([x['subida_dias'] for x in c2s], 0)} | {el_txt('descida_dias')} e {el_txt('subida_dias')} |",
           f"| Efeito na linha do tempo | nenhum | nenhum | em órbita em {min(x['tempo']['pronto_no_encontro'] for x in c2s)} a {max(x['tempo']['pronto_no_encontro'] for x in c2s)}, {'depois' if not any(x['tempo']['pronto_antes_do_ultimo_lancamento'] for x in c2s) else 'em parte antes'} do último lançamento do MAV ({mi['lancamento_mav_mais_tarde']}); {'a subida cruza a conjunção' if all(x['tempo']['subida_cruza_conjuncao'] for x in c2s) else 'a subida cruza a conjunção em parte dos casos'} | outra missão de referência |",
           "| Muda o quê | — | motor sem Isp e massa de fonte, e arranjo dos tanques | reabre os ADRs 0005 e 0013 e usa a opção C | reabre os ADRs 0003, 0005 e 0013 e usa a opção C |", "",
           "## Opinião do agente (separada dos dados; não é fato nem recomendação como fato)", "",
           f"Opinião: a rota A é a única que cumpre o alvo sem mudar a arquitetura: no ombro, cabe com {sg(an[0]['folga_deitado_m'], 2)} m no pior Isp da faixa e com {sg(o['rota_a_referencia']['com_aninhados']['folga_deitado_m'], 2)} m no caso de referência, mas com o deck sob o MAV ela fica entre {sg(o['rota_a_referencia']['com_aninhados']['folga_deitado_com_deck_m'], 2)} e {sg(an[-1]['folga_deitado_com_deck_m'], 2)} m. "
           f"Só o 44:1, sem aninhar, cabe no ombro de {br(next(x['isp_s'] for x in o['rota_a'] if x['so_44']['folga_deitado_m'] >= 0), 0)} s para cima, com pouca folga, e não cabe com o deck. O que sustenta a rota não está verificado: Isp e massa do 44:1 e o tanque aninhado na pressão real. "
           f"A rota B reduz bem o MAV e a massa por área, mas o híbrido pede de {br(min(1 / (1 + x['margem_falcon_heavy']) for x in c2s), 1)} a {br(max(1 / (1 + x['margem_falcon_heavy']) for x in c2s), 1)} vezes a capacidade do Falcon Heavy, e, com o deck, o MAV dela não cabe em nenhuma das duas órbitas. Os motivos de massa do ADR 0013 continuam. O só elétrico merece no máximo uma conta melhor, se a missão de referência mudar. "
           "Meu próximo passo seria fechar os dados do 44:1 e dimensionar o tanque aninhado. A decisão é do Fabio."]
    (SAIDA / "rotas_mav.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def arq_alt():
    pl = ler("results/etapa2.3/plataformas.yaml")["orbita_encontro"]
    return pl["periapse_alt_km"], pl["apoapse_regra_5pct_km"]


def _orbitador_base(arq, margem_fh, hp, ha, lan, f):
    m = arq["orbitador"]["injetado_kg"]
    return {"orbitador_injetado_kg": m, "margem_falcon_heavy": margem_fh(m), "orbita_km": [hp, ha], "dv_mav_com_margem_m_s": 1e3 * f * lan["dv_subida_mav_km_s"]}


def hb_mu_sol():
    from orbital.constantes import GM_SOL
    return GM_SOL


def _fim_conjuncao():
    return dt.date.fromisoformat(ler("results/etapa4.3/comunicacao.yaml")["janelas"]["periodo_conjuncao_graus"][0]["fim"])


if __name__ == "__main__":
    main()
