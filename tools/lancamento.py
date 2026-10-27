"""Etapa 2.4: lançamento e DLA — quais lançadores servem cada veículo, em cada janela, pelas duas formas.

(a) Injeção direta: o lançador entrega o veículo (sem estágio de saída próprio) no C3 da janela. Capacidade
    pela curva publicada (interpolação linear entre os pontos da fonte), vezes o multiplicador de DLA (P-036)
    quando |DLA| > 28,5°; inviável se |DLA| passar da inclinação máxima da subida coplanar dentro da faixa
    de azimutes do Eastern Range [F13].
(b) Órbita baixa + estágio criogênico próprio (modelo atual): o estágio de saída é redimensionado para o C3
    e a DLA de cada janela, com giro de plano na queima de saída quando |DLA| passa da inclinação da órbita
    baixa (P-037). Capacidade de LEO a 28,5° ou 51,6°; usa-se a de maior margem.

Veículos: plataformas e órbita de encontro da Etapa 2.3 (results/etapa2.3/plataformas.yaml). Orbitador pela
regra (iii) verificado nas quatro janelas do envelope (2028–2035), com o caso mais restritivo; orbitador da
missão A só em 2028; lander nas quatro janelas.
Saída: results/etapa2.4/lancamento.yaml e lancamento.md

Uso: python tools/lancamento.py
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
import missoes as mi  # noqa: E402
from orbital import ephemeris as eph  # noqa: E402
from orbital import foguete as fg  # noqa: E402
from orbital import missao as ms_  # noqa: E402
from orbital import porkchop as pc  # noqa: E402
from orbital import lancamento as la  # noqa: E402
from orbital import manobras as mn  # noqa: E402
from orbital import superficie as sf  # noqa: E402
from superficie import _ler, _v, lander_estagios  # noqa: E402

SAIDA = RAIZ / "results" / "etapa2.4"


def veiculos():
    """Massas injetadas (sem estágio de saída) do orbitador (iii e A) e do lander, no caso de base da Etapa 2.3."""
    dcfg, scfg, cu = _ler("config/dimensionamento.yaml"), _ler("config/superficie.yaml"), _ler("config/carga_util.yaml")
    mcfg, icfg, po = _ler("config/mav_propulsao.yaml"), _ler("config/isru.yaml"), _ler("config/parametros_orbitais.yaml")
    p = dm.parametros()
    a_caso, jan, piores = dm.casos(dcfg, p)
    vs = dm.variantes(a_caso, jan, piores)
    pl = _ler("results/etapa2.3/plataformas.yaml")
    mp = _ler("results/etapa2.2/mav_propulsao.yaml")
    op_mav = mp["melhor_opcao"]
    fonte_mav = min((x for x in mp["opcoes"] if x["opcao"] == op_mav), key=lambda x: x["total_regra_iii_kg"])["energia"]
    R, mu, um = _v(po["raio_marte_km"]), p.mu_marte, p.orbitas_marte["eliptica_alta"]
    rp, ra = R + pl["orbita_encontro"]["periapse_alt_km"], R + pl["orbita_encontro"]["apoapse_regra_5pct_km"]
    ms = _ler("results/etapa1.3/missoes.yaml")
    cand = {c["id"]: c for c in ms["candidatas"]}
    ref = _ler("config/missao_referencia.yaml")["missao_referencia"]["id"]
    janelas = [cand[v["missao"]] for v in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()]
    c3l = {"missao_A": cand[ref]["c3l_partida_marte_km2_s2"], "regra_iii": max(x["c3l_partida_marte_km2_s2"] for x in janelas)}
    descer = mn.dv_transferencia_coaxial(mu, um.rp, um.ra, rp, ra)
    margem = _v(dcfg["margem_dv"])
    out = {}
    for caso, var in (("missao_A", "missao_A"), ("regra_iii", dcfg["regra_projeto"])):
        extra = ve.dv_extra_orbitador(mu, um, rp, ra, c3l[caso], descer)
        c2 = copy.deepcopy(dcfg)
        c2["dv"]["encontro_orbita_marte"]["valor"] = _v(dcfg["dv"]["encontro_orbita_marte"]) + extra
        m, r, _ = dm.massa_leo(vs[var], c2, cu, dcfg["caso_base"]["carga_util"], margem, float(dcfg["caso_base"]["acrescimo_capsula"]))
        out[f"orbitador_{caso}"] = {"injetada_kg": r[1].massa_inicial, "leo_modelo_kg": m}
    v_eq = 2 * np.pi * R / _v(scfg["marte"]["periodo_rotacao_s"])
    dv = sf.dv_subida(mu, R, _v(scfg["subida"]["dv_100x100_km_s"]), rp, ra, v_eq,
                      _v(scfg["sitio_e_encontro"]["inclinacao_encontro_graus"]), _v(scfg["sitio_e_encontro"]["latitude_sitio_graus"]))
    pous, cruz, _ = massas_opcao((1 + margem) * dv, op_mav, mcfg, scfg, icfg, fonte_mav)
    chegada = (pous + _v(scfg["lander"]["plataforma_superficie_kg"])) / _v(scfg["lander"]["razao_pousada_entrada"]["entrada_direta"]) + cruz
    r = lander_estagios(chegada, scfg, dcfg, p, a_caso)
    out["lander"] = {"injetada_kg": r[1].massa_inicial, "leo_modelo_kg": r[0].massa_inicial}
    return out, janelas, ref


def capacidade_direta(lan, c3, dla, cfg, i_max):
    """(capacidade kg ou NaN, nota) da injeção direta no C3 e na DLA."""
    if "pontos" not in lan["c3"]:
        return float("nan"), "sem curva de C3 publicada"
    cap = la.interpolar(c3, lan["c3"]["pontos"], lan["c3"]["massa_kg"])
    if cap != cap:
        return cap, "C3 fora da faixa publicada"
    if i_max is not None and abs(dla) > i_max:
        return 0.0, f"|DLA| > {i_max:.2f}° (azimute 40°): exige dogleg ou plano quebrado".replace(".", ",")
    m = cfg["dla"]["multiplicador_nordeste"]
    f = 1.0 if abs(dla) <= _v(cfg["dla"]["faixa_sem_penalidade_graus"]) else la.interpolar(abs(dla), m["dla_graus"], m["fator"])
    return cap * f, ("" if f == 1.0 else f"multiplicador de DLA {f:.3f}".replace(".", ","))


def leo_por_janela(m_inj, cand, dcfg, po, i_graus):
    """(massa na órbita baixa kg, β graus, giro no perigeu θ graus, Δv extra do giro km/s), com o estágio de saída
    próprio redimensionado para a janela."""
    mu = _v(po["gm_terra"])
    r = _v(po["raio_terra_km"]) + _v(po["leo_altitude_km"])
    c3 = cand["c3_km2_s2"]
    beta = la.delta_plano(cand["dla_graus"], i_graus)
    theta = la.giro_no_perigeu(beta, mu, r, c3)
    if theta != theta:
        return float("nan"), beta, theta, float("nan")
    extra = la.dv_saida(mu, r, c3, theta) - la.dv_saida(mu, r, c3, 0.0)
    dv_ideal = cand["dv_saida_terra_km_s"] + extra
    dv = (1 + _v(dcfg["margem_dv"])) * (dv_ideal + _v(dcfg["dv"]["perda_gravitacional"]["saida_terra"]))
    st = dcfg["estagios"]["saida_terra"]
    e = fg.Estagio("saida_terra", _v(st["isp_s"]), _v(st["fracao_estrutural"]), [fg.Queima("saida_terra", dv)])
    try:
        return fg.dimensionar_veiculo([e], m_inj)[0].massa_inicial, beta, theta, extra
    except ValueError:  # Δv alto demais para o estágio (giro grande): inviável
        return float("inf"), beta, theta, extra


def revisar_janela(cfg):
    """Melhor missão da janela com |DLA| limitado, por classe (mesma busca da Etapa 1.3)."""
    rv = cfg["revisao_2033"]
    eph.carregar_kernels()
    mcfg = mi._ler("missoes.yaml")
    p = mi.parametros()
    crit, passo, jan = mcfg["criterio_selecao"], mcfg["passo_dias"], mcfg["janelas"][rv["janela"]]
    et_dep = mi._eixo(*jan["partida_terra"], passo)
    et_M = mi._eixo(*jan["datas_em_marte"], passo)
    et_arr = mi._eixo(*jan["chegada_terra"], passo)
    ida = pc.calcular_grade(eph.TERRA, eph.BARICENTRO_MARTE, et_dep, et_M)
    volta = pc.calcular_grade(eph.BARICENTRO_MARTE, eph.TERRA, et_M, et_arr)
    out = []
    for classe in rv["classes"]:
        c = mcfg["classes"][classe]
        for lim in [float("inf")] + list(rv["dla_max_graus"]):
            r = ms_.melhor_combinacao(p, ida, volta, c["permanencia_dias"], c.get("duracao_max_dias", 1e9), crit["orbita_marte"],
                                      crit["aerocaptura"], c.get("tof_max_dias", np.inf), dla_max_graus=lim)
            if r is None:
                out.append({"classe": classe, "dla_max_graus": lim, "solucao": None})
                continue
            i, a, d, k = r[1]
            ln = ms_.detalhar(p, et_dep[i], et_M[a], et_M[d], et_arr[k])
            borda = [n for n, (x, ax) in {"partida_terra": (i, et_dep), "chegada_marte": (a, et_M),
                                          "partida_marte": (d, et_M), "chegada_terra": (k, et_arr)}.items() if x in (0, len(ax) - 1)]
            out.append({"classe": classe, "dla_max_graus": lim, "dv_total_km_s": r[0], "partida_terra": ln["partida_terra"],
                        "chegada_terra": ln["chegada_terra"], "c3_km2_s2": ln["c3_km2_s2"], "dla_graus": ln["dla_graus"],
                        "dv_saida_terra_km_s": ln["dv_saida_terra_km_s"], "na_borda_do_dominio": borda})
    return out


def main():
    cfg = _ler("config/lancadores.yaml")
    dcfg, po = _ler("config/dimensionamento.yaml"), _ler("config/parametros_orbitais.yaml")
    vei, janelas, ref = veiculos()
    az_min = cfg["centro"]["azimute_graus"]["valor"][0]
    lat_c = _v(cfg["centro"]["latitude_graus"])

    def i_max(lan):
        """Inclinação máxima coplanar no Eastern Range; None fora dele (ELA-4, Kourou)."""
        if lan.get("plataforma") == "ELA-4":
            return None
        pfm = cfg["centro"]["plataformas"].get(lan.get("plataforma"), {})
        return la.inclinacao(pfm.get("latitude_graus", lat_c), az_min)

    def avaliar(veic, jans):
        m_inj = vei[veic]["injetada_kg"]
        ls = []
        for nome, lan in cfg["lancadores"].items():
            for j in jans:
                c3, dla = j["c3_km2_s2"], j["dla_graus"]
                cap_a, nota_a = (float("nan"), "Kourou: só C3 = 6,25 publicado") if lan.get("plataforma") == "ELA-4" and c3 > 6.25 \
                    else capacidade_direta(lan, c3, dla, cfg, i_max(lan))
                melhor_b = None
                for inc in cfg["orbita_estacionamento_b"]["inclinacoes_graus"]:
                    cap = lan["leo_400km"].get(inc)
                    if cap is None:
                        continue
                    m_leo, beta, theta, extra = leo_por_janela(m_inj, j, dcfg, po, inc)
                    if m_leo != m_leo:  # giro impossível com um impulso no perigeu
                        m_leo = float("inf")
                    marg = cap / m_leo - 1
                    if melhor_b is None or marg > melhor_b["margem"]:
                        melhor_b = {"inclinacao_graus": inc, "beta_graus": beta, "giro_perigeu_graus": theta,
                                    "dv_extra_giro_m_s": 1000 * extra, "massa_leo_kg": m_leo, "capacidade_kg": cap, "margem": marg}
                ls.append({"veiculo": veic, "lancador": nome, "categoria": lan["categoria"], "janela": j["id"],
                           "c3_km2_s2": c3, "dla_graus": dla, "massa_injetada_kg": m_inj,
                           "a_capacidade_kg": None if cap_a != cap_a else cap_a,
                           "a_margem": None if cap_a != cap_a else cap_a / m_inj - 1, "a_nota": nota_a, "b": melhor_b})
        return ls

    def resumir(ls):
        def pior(veic, nome, chave):
            sel = [x for x in ls if x["veiculo"] == veic and x["lancador"] == nome]
            vals = [(x["a_margem"] if chave == "a" else (x["b"] or {}).get("margem"), x["janela"]) for x in sel]
            if any(v is None for v, _ in vals):  # sem dado em alguma janela: não se pode afirmar que serve
                return None, next(j for v, j in vals if v is None)
            return min(vals)
        res = []
        for veic in sorted({x["veiculo"] for x in ls}, key=list(casos).index):
            for nome, lan in cfg["lancadores"].items():
                ma, ja = pior(veic, nome, "a")
                mb, jb = pior(veic, nome, "b")
                res.append({"veiculo": veic, "lancador": nome, "categoria": lan["categoria"],
                            "a_pior_margem": ma, "a_janela_mais_restritiva": ja, "b_pior_margem": mb, "b_janela_mais_restritiva": jb})
        return res

    def servem(res):
        d = {}
        for r in res:
            ok = (r["a_pior_margem"] if r["a_pior_margem"] is not None else -1) >= 0 or \
                 (r["b_pior_margem"] if r["b_pior_margem"] is not None else -1) >= 0
            d.setdefault(r["veiculo"], {"operacional": [], "anunciado": []})
            if ok:
                d[r["veiculo"]][r["categoria"]].append(r["lancador"])
        return d

    casos = {"orbitador_regra_iii": janelas, "orbitador_missao_A": [j for j in janelas if j["id"] == ref], "lander": janelas}
    linhas = [x for veic, jans in casos.items() for x in avaliar(veic, jans)]
    resumo = resumir(linhas)
    lancamentos = servem(resumo)

    # Revisão de 2033: a melhor conjunção com |DLA| limitado, no lugar da de 2033 atual
    revisao = revisar_janela(cfg)
    envelope = _ler("results/etapa1.3/missoes.yaml")["envelope_dimensionamento"]
    alternativas = {}
    for r in revisao:
        if r["dla_max_graus"] == float("inf") or r.get("dv_total_km_s") is None:
            continue
        alt = {"id": f"2033-conjuncao, |DLA| ≤ {r['dla_max_graus']:g}°", "c3_km2_s2": r["c3_km2_s2"], "dla_graus": r["dla_graus"],
               "dv_saida_terra_km_s": r["dv_saida_terra_km_s"], "partida_terra": r["partida_terra"]}
        jans = [j for j in janelas if not j["id"].startswith("2033")] + [alt]
        ls = [x for veic in ("orbitador_regra_iii", "lander") for x in avaliar(veic, jans)]
        res = resumir(ls)
        alternativas[alt["id"]] = {"dv_total_km_s": r["dv_total_km_s"], "acima_do_envelope_km_s": r["dv_total_km_s"] - envelope["dv_total_km_s"],
                                   "linhas_2033": [x for x in ls if x["janela"] == alt["id"]], "resumo": res, "servem": servem(res)}
    n_op = sum(1 for v in ("orbitador_regra_iii", "lander") if lancamentos[v]["operacional"])
    out = {"gerado_por": "tools/lancamento.py",
           "veiculos": vei, "inclinacao_max_coplanar_graus": {n: i_max(l) for n, l in cfg["lancadores"].items()},
           "janelas": [{"id": j["id"], "partida": j["partida_terra"], "c3_km2_s2": j["c3_km2_s2"], "dla_graus": j["dla_graus"]} for j in janelas],
           "revisao_2033": {"envelope_atual_dv_km_s": envelope["dv_total_km_s"], "missao_que_define": envelope["missao_que_define"],
                            "casos": revisao, "lancadores_com_2033_alternativo": alternativas},
           "linhas": linhas, "resumo": resumo, "lancadores_que_servem": lancamentos,
           "lancamentos_da_arquitetura": {"um_por_veiculo_com_operacionais": n_op == 2,
                                          "numero": 2 if n_op == 2 else None}}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "lancamento.yaml").write_text(yaml.safe_dump(dm._nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")

    br = lambda x, n=0: "—" if x is None else ("inviável" if x == float("inf") else f"{x:,.{n}f}".replace(",", " ").replace(".", ","))  # noqa: E731
    pc = lambda x: "—" if x is None else f"{100 * x:+.0f} %".replace("-", "−")  # noqa: E731
    rot = {"orbitador_regra_iii": "Orbitador, regra (iii)", "orbitador_missao_A": "Orbitador, missão A", "lander": "Lander"}
    md = ["# Lançamento e DLA (gerado por tools/lancamento.py)", "",
          "Margem = capacidade / massa − 1. (a) injeção direta; (b) órbita baixa + estágio criogênico próprio. "
          "Capacidades interpoladas linearmente entre os pontos publicados. \"—\" = sem dado publicado naquele C3 ou "
          "naquela órbita (ex.: Falcon 9 só até C3 = 10; Falcon Heavy sem LEO de 400 km; Atlas V sem curva de C3); "
          "sem dado em alguma janela, o lançador não conta como servindo.", "",
          "## Veículos (massas em kg)", "", "| Veículo | Injetado na trajetória | Na órbita baixa (modelo, janela de referência) |", "| :- | -: | -: |"]
    for k, v in vei.items():
        md.append(f"| {rot[k]} | {br(v['injetada_kg'])} | {br(v['leo_modelo_kg'])} |")
    md += ["", "## Janelas", "", "| Janela | Partida | C3 (km²/s²) | DLA |", "| :- | :- | -: | -: |"]
    for j in out["janelas"]:
        md.append(f"| {j['id']} | {j['partida']} | {br(j['c3_km2_s2'], 2)} | {br(j['dla_graus'], 1)}° |")
    md += ["", f"Inclinação máxima coplanar (azimute {az_min}°): " + "; ".join(
        f"{n} {br(v, 2)}°" for n, v in out["inclinacao_max_coplanar_graus"].items() if v is not None and n in ("Falcon 9 (ASDS)", "Falcon Heavy (descartável)", "Vulcan VC6"))]
    for veic in casos:
        md += ["", f"## {rot[veic]}: margem no caso mais restritivo", "",
               "| Lançador | Categoria | (a) pior margem | (a) janela | (b) pior margem | (b) janela |", "| :- | :- | -: | :- | -: | :- |"]
        for r in resumo:
            if r["veiculo"] == veic:
                md.append(f"| {r['lancador']} | {r['categoria']} | {pc(r['a_pior_margem'])} | {r['a_janela_mais_restritiva']} | "
                          f"{pc(r['b_pior_margem'])} | {r['b_janela_mais_restritiva']} |")
    md += ["", "## Detalhe por janela", "",
           "| Veículo | Lançador | Janela | (a) capacidade | (a) margem | (a) nota | (b) inclinação; β; giro no perigeu; Δv extra | (b) massa LEO | (b) capacidade | (b) margem |",
           "| :- | :- | :- | -: | -: | :- | :- | -: | -: | -: |"]
    for x in linhas:
        b = x["b"] or {}
        md.append(f"| {rot[x['veiculo']]} | {x['lancador']} | {x['janela']} | {br(x['a_capacidade_kg'])} | {pc(x['a_margem'])} | {x['a_nota']} | "
                  f"{(br(b['inclinacao_graus'], 1) + '°; ' + br(b['beta_graus'], 2) + '°; ' + br(b['giro_perigeu_graus'], 2) + '°; ' + br(b['dv_extra_giro_m_s']) + ' m/s') if b else '—'} | {br(b.get('massa_leo_kg'))} | "
                  f"{br(b.get('capacidade_kg'))} | {pc(b.get('margem'))} |")
    md += ["", f"## Revisão da janela de 2033 (envelope atual: {br(envelope['dv_total_km_s'], 3)} km/s, {envelope['missao_que_define']})", "",
           "| Classe | Limite de \\|DLA\\| | Δv total | Partida | Chegada à Terra | C3 | DLA | Na borda do domínio |",
           "| :- | -: | -: | :- | :- | -: | -: | :- |"]
    for r in revisao:
        lim = "sem limite" if r["dla_max_graus"] == float("inf") else f"{br(r['dla_max_graus'], 1)}°"
        if r.get("dv_total_km_s") is None:
            md.append(f"| {r['classe']} | {lim} | sem solução | | | | | |")
            continue
        md.append(f"| {r['classe']} | {lim} | {br(r['dv_total_km_s'], 3)} km/s | {r['partida_terra']} | {r['chegada_terra']} | "
                  f"{br(r['c3_km2_s2'], 2)} | {br(r['dla_graus'], 1)}° | {', '.join(r['na_borda_do_dominio']) or '—'} |")
    md += ["", "Pior margem com a 2033 trocada pela alternativa (as outras três janelas iguais):", "",
           "| Veículo | Lançador | " + " | ".join("(a) / (b), " + k.split(", ")[1].replace("|", "\\|").replace(".", ",") for k in alternativas) + " |",
           "| :- | :- |" + " -: |" * len(alternativas)]
    for veic in ("orbitador_regra_iii", "lander"):
        for nome in cfg["lancadores"]:
            cel = []
            for k, a in alternativas.items():
                r = next(x for x in a["resumo"] if x["veiculo"] == veic and x["lancador"] == nome)
                cel.append(f"{pc(r['a_pior_margem'])} / {pc(r['b_pior_margem'])}")
            md.append(f"| {rot[veic]} | {nome} | " + " | ".join(cel) + " |")
    md += ["", "## Lançadores que servem (alguma das formas, todas as janelas do veículo)", ""]
    for veic, d in lancamentos.items():
        md.append(f"- {rot[veic]}: operacionais: {', '.join(d['operacional']) or 'NENHUM'}; "
                  f"desempenho anunciado, não demonstrado: {', '.join(d['anunciado']) or 'nenhum'}.")
    (SAIDA / "lancamento.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
