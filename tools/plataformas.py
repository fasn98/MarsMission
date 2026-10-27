"""Etapa 2.3: plataformas do orbitador e do lander por subsistema, com margem de crescimento de massa.

Orbitador: subsistemas do Mars Odyssey [F63], energia dimensionada para o afélio de Marte e o pior eclipse
na órbita de encontro do ADR 0005, cabeamento pela regra da ESA [F71]. Lander: comunicação e radar do
Phoenix [F74], coleta de amostras pela carga útil do Phoenix (P-034), núcleo do Phoenix sem divisão
publicada (opções L1 e L2, P-035), energia para a noite marciana. Margem: AIAA S-120A, categoria E1 [F70].
Refaz a massa total na órbita baixa (regra iii e missão A) com as novas plataformas, no ponto escolhido
do ADR 0005 e com a regra dos 5 % reaplicada.
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
    return {"e1_minimo": lo, "e1_maximo": hi}.get(qual, 0.5 * (lo + hi)) / 100.0


def prevista(itens, cfg, qual):
    """Massa prevista da lista para um critério de margem. `itens`: [(nome, básica, categoria)]."""
    basica = sum(m for _, m, _ in itens)
    if qual == "esa":
        a = cfg["margem_crescimento"]["alternativas"]["esa"]
        return basica * (1 + a["equipamento"]) * (1 + a["sistema"])
    tot = sum(pf.com_margem(m, _mga(c, cfg, qual)) for _, m, c in itens)
    if qual == "e1_medio_mais_gsfc":
        tot += cfg["margem_crescimento"]["alternativas"]["gsfc"]["sistema_sobre_basica"] * basica
    return tot


def orbitador(cfg, po, cu_ate_marte, apoapse_km, rp_alt_km):
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
             ("estrutura", "termico", "comunicacao", "comando_e_dados", "gnc", "mecanismos")]
    itens += [("painel_solar", m_sa, "painel_solar"), ("bateria", m_bat, "baterias"),
              ("energia_restante", m_rest, er["categoria"])]
    f = _v(o["cabeamento"]["fracao"])
    m_cab = f / (1 - f) * (sum(m for _, m, _ in itens) + cu_ate_marte)
    itens.append(("cabeamento", m_cab, "cabeamento"))
    energia = {"eclipse_max_h": t_ecl / 3600, "periodo_h": periodo / 3600, "carga_w": carga, "afelio_ua": d_af,
               "painel_w_afelio_fim_de_vida": p_sa, "energia_eclipse_wh": e_ecl, "bateria_wh_nominal": cap,
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
    cu_base = dcfg["caso_base"]["carga_util"]
    cu_ate_marte = sum(x["massa"] for x in cu["opcoes"][cu_base]["ate_orbita_marte"])

    # Plataformas no ponto escolhido do ADR 0005
    it_o, en_o = orbitador(cfg, po, cu_ate_marte, ap0, rp_alt)
    margem_dv = _v(dcfg["margem_dv"])
    mav_pousado, _, _ = massas_opcao((1 + margem_dv) * antes["dv_mav_km_s"], op_mav, mcfg, scfg, icfg, fonte_mav)
    landers = {o: lander(cfg, o, mav_pousado) for o in cfg["lander"]["escala_nucleo"]["opcoes"]}

    def lista(itens):
        return [{"subsistema": n, "basica_kg": m, "categoria_e1": c, "mga_e1_medio": _mga(c, cfg, "e1_medio"),
                 "prevista_kg": pf.com_margem(m, _mga(c, cfg, "e1_medio"))} for n, m, c in itens]

    plat_o = {q: prevista(it_o, cfg, q) for q in MARGENS}
    plat_l = {o: {q: prevista(it, cfg, q) for q in MARGENS} for o, (it, _) in landers.items()}

    # Massa total: varredura completa (regra dos 5 % reaplicada) com as novas plataformas
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
        pontos, _, esc = ve.varrer("rp300", vr, scfg, d2, cu, p, R, ctx, mav_massas=mav_f, gravar=False)
        no_ponto = next(x for x in pontos if x["apoapse_alt_km"] == ap0)["quimico"]
        return {"plataforma_orbitador_kg": m_orb, "plataforma_lander_kg": m_lan,
                "no_apoapse_adr0005": {"apoapse_alt_km": ap0, "total_regra_iii_kg": no_ponto["total_regra_iii_kg"],
                                       "total_missao_A_kg": no_ponto["total_missao_A_kg"],
                                       "orbitador_regra_iii_kg": no_ponto["orbitador_regra_iii_kg"],
                                       "orbitador_missao_A_kg": no_ponto["orbitador_missao_A_kg"]},
                "regra_5pct": {"apoapse_alt_km": esc["apoapse_alt_km"], "total_regra_iii_kg": esc["massa_regra_iii_kg"],
                               "total_missao_A_kg": esc["massa_missao_A_kg"], "minimo_kg": esc["minimo_kg"]}}

    totais = {"antes_P016_P017": total(_v(dcfg["plataforma_orbitador_kg"]), _v(scfg["lander"]["plataforma_superficie_kg"]))}
    for o in plat_l:
        for q in MARGENS:
            totais[f"{o}/{q}"] = total(plat_o[q], plat_l[o][q])

    out = {"gerado_por": "tools/plataformas.py",
           "orbita_encontro": {"periapse_alt_km": rp_alt, "apoapse_alt_km": ap0},
           "mav": {"opcao": op_mav, "energia": fonte_mav, "massa_pousada_kg": mav_pousado},
           "orbitador": {"subsistemas": lista(it_o), "energia": en_o, "prevista_kg": plat_o,
                         "basica_kg": sum(m for _, m, _ in it_o)},
           "lander": {o: {"subsistemas": lista(it), "energia": en, "prevista_kg": plat_l[o],
                          "basica_kg": sum(m for _, m, _ in it)} for o, (it, en) in landers.items()},
           "totais": totais}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "plataformas.yaml").write_text(yaml.safe_dump(dm._nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")

    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    rot = {"e1_medio": "S-120A E1, ponto médio (base)", "e1_minimo": "S-120A E1, mínimo", "e1_maximo": "S-120A E1, máximo",
           "e1_medio_mais_gsfc": "E1 médio + 15 % da básica (GSFC pré-A)", "esa": "ESA: 20 % equipamento × 20 % sistema"}
    md = ["# Plataformas por subsistema (gerado por tools/plataformas.py)", "",
          f"Órbita de encontro {rp_alt} × {br(ap0)} km (ADR 0005); MAV {op_mav} com energia {fonte_mav}. Massas em kg.", "",
          "## Orbitador", "", "| Subsistema | Básica | Categoria E1 | MGA (médio) | Prevista |", "| :- | -: | :- | -: | -: |"]
    for r in out["orbitador"]["subsistemas"]:
        md.append(f"| {r['subsistema']} | {br(r['basica_kg'], 1)} | {r['categoria_e1']} | {br(100 * r['mga_e1_medio'], 1)} % | {br(r['prevista_kg'], 1)} |")
    md.append(f"| **Total** | **{br(out['orbitador']['basica_kg'], 1)}** | | | **{br(plat_o['e1_medio'], 1)}** |")
    e = en_o
    md += ["", f"Energia: pior eclipse {br(e['eclipse_max_h'], 2)} h num período de {br(e['periodo_h'], 2)} h; carga {br(e['carga_w'])} W; "
           f"painel {br(e['painel_w_afelio_fim_de_vida'])} W no afélio ({br(e['afelio_ua'], 3)} UA, {br(e['w_kg_painel_afelio'], 1)} W/kg); "
           f"bateria {br(e['bateria_wh_nominal'])} Wh nominais para {br(e['energia_eclipse_wh'])} Wh no eclipse."]
    for o, d in out["lander"].items():
        md += ["", f"## Lander, opção {o}", "", "| Subsistema | Básica | Categoria E1 | MGA (médio) | Prevista |", "| :- | -: | :- | -: | -: |"]
        for r in d["subsistemas"]:
            md.append(f"| {r['subsistema']} | {br(r['basica_kg'], 1)} | {r['categoria_e1']} | {br(100 * r['mga_e1_medio'], 1)} % | {br(r['prevista_kg'], 1)} |")
        md.append(f"| **Total** | **{br(d['basica_kg'], 1)}** | | | **{br(d['prevista_kg']['e1_medio'], 1)}** |")
    el = out["lander"]["L1"]["energia"]
    md += ["", f"Energia do lander: {br(el['energia_por_sol_wh'])} Wh/sol ({br(el['carga_media_w'])} W médios); painel {br(el['area_painel_m2'], 2)} m²; "
           f"bateria {br(el['bateria_wh_nominal'])} Wh nominais para {br(el['energia_noite_wh'])} Wh na noite."]
    md += ["", "## Plataformas por critério de margem", "", "| Critério | Orbitador | Lander L1 | Lander L2 |", "| :- | -: | -: | -: |"]
    for q in MARGENS:
        md.append(f"| {rot[q]} | {br(plat_o[q])} | {br(plat_l['L1'][q])} | {br(plat_l['L2'][q])} |")
    md += ["", "## Massa total na órbita baixa da Terra", "",
           f"| Caso | Orbitador | Lander | Total (iii) em {br(ap0)} km | Total (A) em {br(ap0)} km | Apoapse pela regra dos 5 % | Total (iii) nele | Total (A) nele |",
           "| :- | -: | -: | -: | -: | -: | -: | -: |"]
    for k, t in totais.items():
        nome = "Antes (P-016 = P-017 = 850 kg)" if k.startswith("antes") else f"{k.split('/')[0]}, {rot[k.split('/')[1]]}"
        a, b = t["no_apoapse_adr0005"], t["regra_5pct"]
        md.append(f"| {nome} | {br(t['plataforma_orbitador_kg'])} | {br(t['plataforma_lander_kg'])} | {br(a['total_regra_iii_kg'])} | "
                  f"{br(a['total_missao_A_kg'])} | {br(b['apoapse_alt_km'])} | {br(b['total_regra_iii_kg'])} | {br(b['total_missao_A_kg'])} |")
    (SAIDA / "plataformas.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
