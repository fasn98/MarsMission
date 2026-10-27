"""Etapa 2.3: plataformas do orbitador e do lander por subsistema, com margem de crescimento de massa.

Orbitador: subsistemas do Mars Odyssey [F33], energia dimensionada para o afélio de Marte e o pior eclipse
na órbita de encontro do ADR 0005, cabeamento pela regra da ESA [F71]. Lander: comunicação e radar do
Phoenix [F74], coleta de amostras pela carga útil do Phoenix (P-034), núcleo do Phoenix sem divisão
publicada (limite inferior L1; L2 como referência; limite superior SRL 2024 − MAV, P-035); base = L3 (lander do
MSR sem MAV e sem rover de busca) + amostras provisórias (P-017, decisões do Fabio). Margem: AIAA S-120A,
categoria E1 [F70], ponto médio; GSFC e ESA na sensibilidade.
Refaz a massa total na órbita baixa (regra iii e missão A) reaplicando a regra dos 5 % do ADR 0005. Como a
bateria do orbitador depende do eclipse, plataforma e apoapse são iterados até o apoapse não mudar.
Dependências de etapas anteriores (lidas, não recalculadas): results/etapa2.1/varredura_encontro_rp300_O4.yaml
(apoapse e Δv do MAV antes desta etapa, usados como ponto de partida da iteração, para as colunas "no apoapse
anterior" e para o MAV da referência L2) e results/etapa2.2/mav_propulsao.yaml (opção e fonte de energia do MAV). Se essas etapas forem
regeneradas com o config novo, o ponto de partida muda; o caso "antes" usa 850/850 explícitos e não depende delas.
Saída: results/etapa2.3/plataformas.yaml e plataformas.md

Uso: python tools/plataformas.py
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(RAIZ / "src"), str(RAIZ / "tools")]

import dimensionamento as dm  # noqa: E402
import varredura_encontro as ve  # noqa: E402
from mav_propulsao import massas_opcao  # noqa: E402
from orbital import plataforma as pf  # noqa: E402
from orbital import superficie as sf  # noqa: E402
from superficie import _ler, _v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa2.3"
MARGENS = ("e1_medio", "e1_minimo", "e1_maximo", "e1_medio_mais_gsfc", "esa")


def _mga(cat, cfg, qual):
    lo, hi = cfg["margem_crescimento"]["categorias_e1"][cat]
    valores = {"e1_minimo": lo, "e1_maximo": hi, "e1_medio": 0.5 * (lo + hi), "e1_medio_mais_gsfc": 0.5 * (lo + hi)}
    if qual not in valores:
        raise ValueError(f"critério de margem desconhecido: {qual}")
    return valores[qual] / 100.0


def prevista(itens, cfg, qual):
    """Massa prevista da lista para um critério de margem. `itens`: [(nome, básica, categoria)]."""
    basica = sum(m for _, m, _ in itens)
    if qual == "esa":
        a = cfg["margem_crescimento"]["alternativas"]["esa"]
        return basica * (1 + a["equipamento"]) * (1 + a["sistema"])
    if qual not in MARGENS:
        raise ValueError(f"critério de margem desconhecido: {qual}")
    tot = sum(pf.com_margem(m, _mga(c, cfg, qual)) for _, m, c in itens)
    if qual == "e1_medio_mais_gsfc":
        tot += cfg["margem_crescimento"]["alternativas"]["gsfc"]["sistema_sobre_basica"] * basica
    return tot


def orbitador(cfg, po, apoapse_km, rp_alt_km):
    o = cfg["orbitador"]
    e = o["energia"]
    R, mu = _v(po["raio_marte_km"]), _v(po["gm_marte"])
    t_ecl, periodo = pf.eclipse_maximo(mu, R, R + rp_alt_km, R + apoapse_km)
    t_sol = periodo - t_ecl
    carga = _v(e["carga_w"])
    d_af = _v(e["distancia_ua"]["semieixo"]) * (1 + _v(e["distancia_ua"]["excentricidade"]))
    p_sa = pf.potencia_painel(carga, t_sol, t_ecl, _v(e["eficiencia_recarga"]))
    m_sa = pf.massa_painel(p_sa, _v(e["painel_w_kg_1ua"]), d_af, _v(e["fator_perdas_painel"]))
    e_ecl = carga * t_ecl / 3600.0
    cap, m_bat = pf.bateria(e_ecl, _v(e["profundidade_descarga"]), _v(e["energia_especifica_bateria_wh_kg"]))
    s = o["subsistemas"]
    er = s["energia_restante"]
    m_rest = _v(er["massa_energia_odyssey_kg"]) - _v(er["painel_odyssey_w_1ua"]) / _v(e["painel_w_kg_1ua"])
    itens = [(k, float(s[k]["massa_kg"]), s[k]["categoria"]) for k in
             ("estrutura", "termico", "comunicacao", "comando_e_dados", "gnc", "mecanismos", "rss_nac", "rss_lidar")]
    itens += [("painel_solar", m_sa, "painel_solar"), ("bateria", m_bat, "baterias"),
              ("energia_restante", m_rest, er["categoria"])]
    f = _v(o["cabeamento"]["fracao"])
    m_cab = f / (1 - f) * sum(m for _, m, _ in itens)  # base: só a plataforma (P-031)
    itens.append(("cabeamento", m_cab, "cabeamento"))
    energia = {"eclipse_max_h": t_ecl / 3600, "periodo_h": periodo / 3600, "carga_w": carga, "afelio_ua": d_af,
               "painel_w_afelio": p_sa, "energia_eclipse_wh": e_ecl, "bateria_wh_nominal": cap,
               "w_kg_painel_afelio": _v(e["painel_w_kg_1ua"]) * _v(e["fator_perdas_painel"]) / d_af**2}
    return itens, energia


def lander(cfg, opcao, mav_bloco_kg):
    la = cfg["lander"]
    e = la["energia"]
    ph = la["phoenix"]
    s = la["subsistemas"]
    sol_h = _v(e["duracao_sol_h"])
    e_sol = _v(e["energia_por_sol_wh"])
    carga = e_sol / sol_h
    e_noite = carga * _v(e["noite_fracao_sol"]) * sol_h
    oc = cfg["orbitador"]["energia"]
    cap, m_bat = pf.bateria(e_noite, _v(oc["profundidade_descarga"]), _v(oc["energia_especifica_bateria_wh_kg"]))
    rend = _v(e["rendimento_painel_wh_sol_m2"]["energia_wh"]) / _v(e["rendimento_painel_wh_sol_m2"]["area_m2"])
    area = e_sol / rend
    m_sa = area * _v(e["densidade_area_painel_w_m2"]) / _v(oc["painel_w_kg_1ua"])
    itens = [(k, float(s[k]["massa_kg"]), s[k]["categoria"]) for k in ("uhf", "banda_x_cruzeiro", "radar", "amostras")]
    itens += [("painel_solar", m_sa, "painel_solar"), ("bateria", m_bat, "baterias")]
    seco_ph = _v(ph["lander_kg"]) - _v(ph["combustivel_kg"])
    nucleo_ph = seco_ph - _v(ph["instrumentos_kg"]) - sum(float(s[k]["massa_kg"]) for k in ("uhf", "banda_x_cruzeiro", "radar"))
    if opcao == "L1":
        nucleo = nucleo_ph
    else:  # L2: núcleo = k × massa pousada seca, com k do Phoenix
        k = nucleo_ph / seco_ph
        nucleo = k / (1 - k) * (sum(m for _, m, _ in itens) + mav_bloco_kg)
    itens.insert(0, ("nucleo", nucleo, s["nucleo"]["categoria"]))
    energia = {"energia_por_sol_wh": e_sol, "carga_media_w": carga, "energia_noite_wh": e_noite, "bateria_wh_nominal": cap,
               "area_painel_m2": area, "rendimento_wh_sol_m2": rend, "nucleo_phoenix_kg": nucleo_ph,
               "fracao_nucleo_phoenix": nucleo_ph / seco_ph}
    return itens, energia


def lander_l3(cfg):
    """L3: lander do MSR sem MAV e sem rover de busca (alocação, sem MGA adicional no caso de base)."""
    t = cfg["lander"]["topo_para_baixo"]
    return _v(t["srl_seco_superficie_kg"]) - _v(t["srl_mav_kg"]) - _v(t["srl_sfr_kg"])


def l3_com_margem(m, cfg, qual):
    a = cfg["margem_crescimento"]["alternativas"]
    if qual == "esa":
        return m * (1 + a["esa"]["equipamento"]) * (1 + a["esa"]["sistema"])
    if qual == "e1_medio_mais_gsfc":
        return m * (1 + a["gsfc"]["sistema_sobre_basica"])
    if qual == "e1_medio":
        return m
    raise ValueError(f"critério de margem sem uso no L3: {qual}")


def lander_base(cfg, qual="e1_medio"):
    """Base do lander: L3 + item de amostras da P-034 (alocação provisória, com a sua margem E1)."""
    s = cfg["lander"]["subsistemas"]["amostras"]
    return l3_com_margem(lander_l3(cfg), cfg, qual) + prevista([("amostras", float(s["massa_kg"]), s["categoria"])], cfg, qual)


def limite_srl_2024(cfg):
    """Limite superior da faixa do lander: SRL de 2024 menos o MAV (comparabilidade não confirmada)."""
    t = cfg["lander"]["topo_para_baixo"]
    return _v(t["srl_2024_pousado_kg"]) - _v(t["srl_mav_kg"])


def plataforma_orbitador(cfg, po, apoapse_km, rp_alt_km, qual="e1_medio"):
    return prevista(orbitador(cfg, po, apoapse_km, rp_alt_km)[0], cfg, qual)


def main():
    cfg = _ler("config/plataformas.yaml")
    po = _ler("config/parametros_orbitais.yaml")
    scfg, icfg, mcfg = _ler("config/superficie.yaml"), _ler("config/isru.yaml"), _ler("config/mav_propulsao.yaml")
    dcfg = _ler("config/dimensionamento.yaml")
    cu = _ler("config/carga_util.yaml")
    p = dm.parametros()
    a_caso, jan, piores = dm.casos(dcfg, p)
    vs = dm.variantes(a_caso, jan, piores)

    antes = _ler("results/etapa2.1/varredura_encontro_rp300_O4.yaml")["escolha"]
    mp = _ler("results/etapa2.2/mav_propulsao.yaml")
    op_mav = mp["melhor_opcao"]
    fonte_mav = min((x for x in mp["opcoes"] if x["opcao"] == op_mav), key=lambda x: x["total_regra_iii_kg"])["energia"]
    vr = scfg["varreduras_encontro"]["rp300"]
    ap0, rp_alt = antes["apoapse_alt_km"], vr["periapse_alt_km"]
    margem_dv = _v(dcfg["margem_dv"])
    mav_pousado, _, _ = massas_opcao((1 + margem_dv) * antes["dv_mav_km_s"], op_mav, mcfg, scfg, icfg, fonte_mav)

    R = _v(po["raio_marte_km"])
    ms = _ler("results/etapa1.3/missoes.yaml")
    cand = {c["id"]: c for c in ms["candidatas"]}
    ref = _ler("config/missao_referencia.yaml")["missao_referencia"]["id"]
    janelas = [cand[v["missao"]] for v in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()]
    c3l = {"missao_A": cand[ref]["c3l_partida_marte_km2_s2"], "regra_iii": max(x["c3l_partida_marte_km2_s2"] for x in janelas)}
    mav_f = lambda d: massas_opcao(d, op_mav, mcfg, scfg, icfg, fonte_mav)[:2]  # noqa: E731

    def total(m_orb, m_lan):
        d2 = copy.deepcopy(dcfg)
        d2["plataforma_orbitador_kg"]["valor"] = m_orb
        ctx = (2 * np.pi * R / _v(scfg["marte"]["periodo_rotacao_s"]), _v(scfg["sitio_e_encontro"]["latitude_sitio_graus"]),
               _v(scfg["sitio_e_encontro"]["inclinacao_encontro_graus"]), _v(scfg["subida"]["dv_100x100_km_s"]), m_lan,
               _v(scfg["lander"]["razao_pousada_entrada"]["entrada_direta"]), _v(scfg["aerofrenagem"]["dv_saida_aerofrenagem_km_s"]),
               vs, a_caso, c3l)
        pontos, mins, esc = ve.varrer("rp300", vr, scfg, d2, cu, p, R, ctx, mav_massas=mav_f, gravar=False)
        mn_ = mins["quimico/total_regra_iii_kg"]
        no_ponto = next(x for x in pontos if x["apoapse_alt_km"] == ap0)["quimico"]
        return {"plataforma_orbitador_kg": m_orb, "plataforma_lander_kg": m_lan,
                "no_apoapse_anterior": {"total_regra_iii_kg": no_ponto["total_regra_iii_kg"], "total_missao_A_kg": no_ponto["total_missao_A_kg"]},
                "regra_5pct": {"apoapse_alt_km": esc["apoapse_alt_km"], "total_regra_iii_kg": esc["massa_regra_iii_kg"],
                               "total_missao_A_kg": esc["massa_missao_A_kg"], "minimo_kg": esc["minimo_kg"],
                               "acima_do_minimo": esc["acima_do_minimo"], "mav_glom_kg": esc["mav_glom_kg"],
                               "apoapse_do_minimo_km": mn_["apoapse_alt_km"], "minimo_no_extremo": mn_["no_extremo"]}}

    # Caso de base: orbitador (E1 médio) + lander (L3 + amostras), iterando plataforma ↔ apoapse
    m_l3 = lander_l3(cfg)
    m_base = lander_base(cfg)
    m_sup = limite_srl_2024(cfg)
    ap, iteracoes = ap0, []
    for _ in range(6):
        m_o = plataforma_orbitador(cfg, po, ap, rp_alt)
        t = total(m_o, m_base)
        iteracoes.append({"apoapse_entrada_km": ap, "plataforma_orbitador_kg": m_o, "apoapse_saida_km": t["regra_5pct"]["apoapse_alt_km"]})
        if t["regra_5pct"]["apoapse_alt_km"] == ap:
            break
        ap = t["regra_5pct"]["apoapse_alt_km"]
    else:
        raise RuntimeError("plataforma e apoapse não convergiram")
    ap_f = ap
    it_o, en_o = orbitador(cfg, po, ap_f, rp_alt)
    landers = {o: lander(cfg, o, mav_pousado) for o in cfg["lander"]["escala_nucleo"]["opcoes"]}

    def lista(itens):
        return [{"subsistema": n, "basica_kg": m, "categoria_e1": c, "mga_e1_medio": _mga(c, cfg, "e1_medio"),
                 "prevista_kg": pf.com_margem(m, _mga(c, cfg, "e1_medio"))} for n, m, c in itens]

    plat_o = {q: prevista(it_o, cfg, q) for q in MARGENS}
    plat_l = {o: {q: prevista(it, cfg, q) for q in MARGENS} for o, (it, _) in landers.items()}
    plat_l["base"] = {q: lander_base(cfg, q) for q in ("e1_medio", "e1_medio_mais_gsfc", "esa")}

    a = cfg["antes_etapa_2_3"]
    casos = {"antes": ("Antes (P-016 = P-017 = 850 kg)", a["orbitador_kg"], a["lander_kg"]),
             "base": ("**Base: orbitador E1 médio + L3 + amostras**", plat_o["e1_medio"], m_base),
             "gsfc": ("GSFC: E1 médio + 15 % nos dois", plat_o["e1_medio_mais_gsfc"], plat_l["base"]["e1_medio_mais_gsfc"]),
             "esa": ("ESA: 20 % × 20 % nos dois", plat_o["esa"], plat_l["base"]["esa"]),
             "orb_e1_min": ("Orbitador E1 mínimo + lander de base", plat_o["e1_minimo"], m_base),
             "orb_e1_max": ("Orbitador E1 máximo + lander de base", plat_o["e1_maximo"], m_base),
             "limite_L1": ("Limite inferior do lander: L1 (E1 médio)", plat_o["e1_medio"], plat_l["L1"]["e1_medio"]),
             "limite_srl_2024": ("Limite superior do lander: SRL 2024 − MAV (comparabilidade não confirmada)", plat_o["e1_medio"], m_sup),
             "referencia_L2": ("Referência: L2 (E1 médio), antigo limite superior", plat_o["e1_medio"], plat_l["L2"]["e1_medio"])}
    totais = {k: {"caso": r, **total(mo, ml)} for k, (r, mo, ml) in casos.items()}

    out = {"gerado_por": "tools/plataformas.py",
           "orbita_encontro": {"periapse_alt_km": rp_alt, "apoapse_antes_km": ap0, "apoapse_regra_5pct_km": ap_f,
                               "iteracoes": iteracoes},
           "mav": {"opcao": op_mav, "energia": fonte_mav, "massa_pousada_kg": mav_pousado},
           "escolha": {"plataforma_orbitador_kg": plat_o["e1_medio"], "plataforma_lander_kg": m_base,
                       "criterio": "orbitador: lista por subsistema, E1 médio; lander: L3 + amostras (provisório) (decisões do Fabio, portão 2.3)"},
           "orbitador": {"subsistemas": lista(it_o), "energia": en_o, "prevista_kg": plat_o,
                         "basica_kg": sum(m for _, m, _ in it_o)},
           "lander": {**{o: {"subsistemas": lista(it), "energia": en, "prevista_kg": plat_l[o],
                             "basica_kg": sum(m for _, m, _ in it)} for o, (it, en) in landers.items()},
                      "L3": {"basica_kg": m_l3}, "base_L3_mais_amostras": {"prevista_kg": plat_l["base"]},
                      "limite_superior_srl_2024_kg": m_sup},
           "totais": totais}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "plataformas.yaml").write_text(yaml.safe_dump(dm._nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")

    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    md = ["# Plataformas por subsistema (gerado por tools/plataformas.py)", "",
          f"Órbita de encontro {rp_alt} × {br(ap_f)} km (regra dos 5 % do ADR 0005 reaplicada; antes {br(ap0)} km); "
          f"MAV {op_mav} com energia {fonte_mav}. Massas em kg.", "",
          "## Orbitador (base: E1 médio)", "", "| Subsistema | Básica | Categoria E1 | MGA (médio) | Prevista |", "| :- | -: | :- | -: | -: |"]
    for r in out["orbitador"]["subsistemas"]:
        md.append(f"| {r['subsistema']} | {br(r['basica_kg'], 1)} | {r['categoria_e1']} | {br(100 * r['mga_e1_medio'], 1)} % | {br(r['prevista_kg'], 1)} |")
    md.append(f"| **Total** | **{br(out['orbitador']['basica_kg'], 1)}** | | | **{br(plat_o['e1_medio'], 1)}** |")
    e = en_o
    md += ["", f"Energia: pior eclipse {br(e['eclipse_max_h'], 2)} h num período de {br(e['periodo_h'], 2)} h; carga {br(e['carga_w'])} W; "
           f"painel {br(e['painel_w_afelio'])} W no afélio ({br(e['afelio_ua'], 3)} UA, {br(e['w_kg_painel_afelio'], 1)} W/kg); "
           f"bateria {br(e['bateria_wh_nominal'])} Wh nominais para {br(e['energia_eclipse_wh'])} Wh no eclipse."]
    md += ["", "## Lander", "", f"**Base:** L3 (lander do MSR sem MAV e sem rover de busca) {br(m_l3)} kg, sem MGA adicional, "
           f"+ amostras (P-034, provisório) com MGA E1 = {br(m_base, 1)} kg (GSFC: {br(plat_l['base']['e1_medio_mais_gsfc'], 1)}; "
           f"ESA: {br(plat_l['base']['esa'], 1)}). Faixa: L1 (abaixo) até SRL 2024 − MAV = {br(m_sup)} kg "
           "(comparabilidade não confirmada); L2 só como referência."]
    for o, d in out["lander"].items():
        if not isinstance(d, dict) or "subsistemas" not in d:
            continue
        md += ["", f"### {'Limite inferior' if o == 'L1' else 'Referência'} {o}", "", "| Subsistema | Básica | Categoria E1 | MGA (médio) | Prevista |", "| :- | -: | :- | -: | -: |"]
        for r in d["subsistemas"]:
            md.append(f"| {r['subsistema']} | {br(r['basica_kg'], 1)} | {r['categoria_e1']} | {br(100 * r['mga_e1_medio'], 1)} % | {br(r['prevista_kg'], 1)} |")
        md.append(f"| **Total** | **{br(d['basica_kg'], 1)}** | | | **{br(d['prevista_kg']['e1_medio'], 1)}** |")
    md += ["", "## Massa total na órbita baixa da Terra", "",
           f"| Caso | Orbitador | Lander | Total (iii) em {br(ap0)} km | Total (A) em {br(ap0)} km | Apoapse pela regra dos 5 % | Total (iii) nele | Total (A) nele |",
           "| :- | -: | -: | -: | -: | -: | -: | -: |"]
    for k, t in totais.items():
        a_, b = t["no_apoapse_anterior"], t["regra_5pct"]
        md.append(f"| {t['caso']} | {br(t['plataforma_orbitador_kg'])} | {br(t['plataforma_lander_kg'])} | {br(a_['total_regra_iii_kg'])} | "
                  f"{br(a_['total_missao_A_kg'])} | {br(b['apoapse_alt_km'])} | {br(b['total_regra_iii_kg'])} | {br(b['total_missao_A_kg'])} |")
    md += ["", "Nos casos de sensibilidade, a plataforma do orbitador é a calculada no apoapse do caso de base."]
    (SAIDA / "plataformas.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
