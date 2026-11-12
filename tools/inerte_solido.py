"""Lei de massa inerte do MAV sólido ancorada em motores reais (Fabio, 2026-11-10, PR #60, itens 3 e 4).

Item 3: ajuste inerte × propelente dos motores sólidos de estágio superior do catálogo [F270]; comparação com a P-019 e a
P-111; a lei proposta (P-113, NÃO VALIDADA) em duas variantes do nível do motor:
  inerte do estágio i = N_i + c_i · P_i^b
  b: expoente do ajuste do catálogo; N_i: inerte não propulsivo do MAV do MSR ([F269]), fixo na escala;
  A: c_i pelo inerte do motor do MSR ([F269]); B: c_i pela divisão do inerte que a verificação da P-110 escolheu.
Item 4: cada variante na verificação (órbita publicada do MSR), na varredura da escala a 380 km (P-110), no caso com a
margem da P-014 simulado com o modelo de subida do sólido, e as folgas com deck no aeroshell de 4,65 m.
Saída: results/familia1/inerte_solido.yaml e .md

Uso: python tools/inerte_solido.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import comprimento_solido as cs  # noqa: E402
import mav_familia1 as mf  # noqa: E402
import subida_mav as sm  # noqa: E402
from orbital import subida as sb  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "familia1"
POL = 0.0254   # [F112] Apêndice B.8, PDF p. 62: polegada em metros
br, sg = sm.br, sm.sg


def ajuste(P, I):
    """Ajuste de mínimos quadrados de ln I = ln a + b ln P: (a, b, erro-padrão de b, resíduos em ln)."""
    x, y = np.log(P), np.log(I)
    A = np.vstack([np.ones_like(x), x]).T
    (la, b), *_ = np.linalg.lstsq(A, y, rcond=None)
    r = y - (la + b * x)
    s2 = float(r @ r) / (len(x) - 2)
    se_b = math.sqrt(s2 / float(((x - x.mean()) ** 2).sum()))
    return math.exp(la), float(b), se_b, r


def estagios(s, lei, mp, f, isp, carga):
    """Estágios e inertes do sólido na escala s do propelente e do empuxo do MSR, com o inerte da lei (N, c, b)."""
    N, c, b = lei
    P = [s * x for x in mp]
    ine = [n + ci * p ** b for n, ci, p in zip(N, c, P)]
    m0 = carga + sum(P) + sum(ine)
    return [sb.Estagio(m0, P[0], s * f[0], isp[0]), sb.Estagio(m0 - P[0] - ine[0], P[1], s * f[1], isp[1])], ine


def main():
    cad, fc, scfg = ler("config/cad.yaml"), ler("config/familia1.yaml"), ler("config/superficie.yaml")
    dcfg, mv, a4 = ler("config/dimensionamento.yaml"), ler("results/familia1/mavs.yaml"), ler("results/familia1/aeroshell_465.yaml")
    cfg = fc["inerte_solido"]
    lb = v(ler("config/motores.yaml")["conversao"]["lb_para_kg"])
    mot = [{"nome": m["nome"], "envelope": m["envelope"], "propelente_kg": m["propelente_lbm"] * lb, "inerte_kg": m["inerte_lbm"] * lb, "pagina_pdf": m["pagina_pdf"]} for m in cfg["motores"]]
    P = np.array([m["propelente_kg"] for m in mot])
    I = np.array([m["inerte_kg"] for m in mot])
    a, b, se_b, r = ajuste(P, I)
    for m, ri in zip(mot, r):
        m["residuo_fator"] = math.exp(ri)
        m["inerte_sobre_propelente"] = m["inerte_kg"] / m["propelente_kg"]
    lk = float(np.mean(np.log(I / P)))   # ajuste proporcional (b = 1), para comparar com as leis lineares
    rk = np.log(I / P) - lk
    ajuste_cat = {"a": a, "b": b, "erro_padrao_b": se_b, "n": len(P), "faixa_propelente_kg": [float(P.min()), float(P.max())],
                  "rms_ln": float(np.sqrt(r @ r / (len(P) - 2))), "fator_rms": math.exp(float(np.sqrt(r @ r / (len(P) - 2)))),
                  "fator_max": math.exp(float(np.abs(r).max())),
                  "proporcional": {"k": math.exp(lk), "fator_rms": math.exp(float(np.sqrt(rk @ rk / (len(P) - 1)))), "fator_max": math.exp(float(np.abs(rk).max()))}}
    # ---------------- MSR, P-019, P-111 e as duas variantes
    msd = cad["mav_solido"]
    mp, isp, tq = msd["propelente_kg"]["valor"], msd["isp_s"]["valor"], msd["tempo_queima_s"]["valor"]
    f = [m_ * i * sb.G0_M / t for m_, i, t in zip(mp, isp, tq)]
    carga = v(scfg["mav"]["carga_util_kg"])
    msr = cfg["msr"]
    Nm, Im, Pm = (msr[k]["valor"] for k in ("inerte_nao_propulsivo_kg", "inerte_motor_kg", "propelente_kg"))
    eps = v(ler("config/mav_propulsao.yaml")["opcoes"]["O1"]["fracao_estrutural"])
    ine_v = mv["verificacao"]["base"]["inertes_kg"]
    leis = {"A (nível do motor pelo [F269])": ([float(x) for x in Nm], [im / pm ** b for im, pm in zip(Im, Pm)], b),
            "B (nível pela divisão verificada da P-110)": ([float(x) for x in Nm], [(iv - n) / p ** b for iv, n, p in zip(ine_v, Nm, mp)], b)}
    comparacao = []
    for i_, nome in enumerate(("estágio 1", "estágio 2")):
        comparacao.append({"estagio": nome, "propelente_kg": mp[i_], "catalogo_motor_kg": a * mp[i_] ** b, "msr_motor_kg": Im[i_], "msr_nao_propulsivo_kg": Nm[i_],
                           "msr_estagio_kg": Im[i_] + Nm[i_], "p019_estagio_kg": eps / (1 - eps) * mp[i_], "p111_estagio_kg": ine_v[i_],
                           **{f"lei_{k[0]}_estagio_kg": l[0][i_] + l[1][i_] * mp[i_] ** l[2] for k, l in leis.items()}})
    # ---------------- subida: verificação, varredura a 380 km, caso com margem
    ctx = sm.contexto()
    sc, _, atm, pl0, _ = ctx
    g = fc["mav_solido"]["guia"]
    vf = fc["mav_solido"]["verificacao"]
    t_v, partidas, limites, tol = v(g["t_v_s"]), g["partidas"]["valor"], [tuple(t) for t in g["limites"]["valor"]], v(g["tol_custo"])
    d_s = mv["limites"]["solido"]["diametro_m"]
    area = v(sc["arrasto"]["cd_base"]) * math.pi * d_s ** 2 / 4
    pl_v = sb.Planeta(pl0.mu, pl0.raio, sb.omega_efetivo(pl0.omega, v(vf["inclinacao_graus"])))
    pl_e = sb.Planeta(pl0.mu, pl0.raio, sb.omega_efetivo(pl0.omega, v(scfg["sitio_e_encontro"]["inclinacao_encontro_graus"])))
    h = v(cfg["altitude_km"])
    margem = v(dcfg["margem_dv"])
    lo, hi = g["escala_busca"]["valor"]
    passo = v(g["passo_varredura_escala"])
    l465, l45 = a4["limites_465"][str(d_s)], a4["limites_45"][str(d_s)]

    gn = cfg["guinada"]
    part_g = [list(x) + [v(gn["partida_rad"])] for x in partidas]
    lim_g = limites + [tuple(gn["limites_rad"]["valor"])]

    lim_a = limites[:2] + [(limites[2][0], v(cfg["antecedencia_max_s"]))]

    def voo(pl, est, ine, h_m, guinada=False, antecipada=False):
        lim_ = lim_g if guinada else lim_a if antecipada else limites
        c_, vo, gu = sb.ajusta_solido(pl, est, ine, area, atm, h_m, t_v, part_g if guinada else partidas, lim_)
        return {"custo": c_, "fecha": c_ < tol, "periapse_km": vo["periapse_m"] / 1000, "apoapse_km": vo["apoapse_m"] / 1000, "costa_s": vo["costa_s"], "guiamento": gu}

    # ---------------- comprimento: P-108 revista (tools/comprimento_solido.py)
    comp = dict(ler("results/familia1/comprimento_solido.yaml"))
    comp["diametro_mav_m"] = comp["diametro_msr_m"]
    for m_, cfg_m in zip(mot, cfg["motores"]):
        m_["comprimento_m"], m_["diametro_m"], m_["residuo_comprimento_fator"] = cfg_m["comprimento_pol"] * POL, cfg_m["diametro_pol"] * POL, comp["residuos_fator"][cfg_m["nome"]]

    def geometria(est):
        L_ = cs.comprimento([e.propelente_kg for e in est], d_s, comp)   # P-108 revista
        return {"comprimento_m": L_, "folga_465_com_deck_m": (l465["com_deck_m"] - L_) / 2, "folga_465_sem_deck_m": (l465["sem_deck_m"] - L_) / 2,
                "folga_45_com_deck_m": (l45["com_deck_m"] - L_) / 2}

    em_ = fc["mav_solido"]["escala_minima"]
    nm_ = {"tol_ls": v(em_["tol_ls"]), "custo_circular": v(em_["custo_circular"]), "xatol_c": v(em_["xatol_c"])}

    def maquina(lei, isp_, pl, h_m, escala_ou_fator="escala"):
        """(tenta, deficit) da escala mínima (P-117) para a lei e o Isp dados; com "fator", a variável é o fator no Isp na
        escala 1 (viés da P-114)."""
        def veiculo(z):
            isp2 = [i * z for i in isp_] if escala_ou_fator == "fator" else isp_
            f2 = [m_ * i * sb.G0_M / t for m_, i, t in zip(mp, isp2, tq)]   # P-111: tempo de queima publicado
            return estagios(1.0 if escala_ou_fator == "fator" else z, lei, mp, f2, isp2, carga)

        def tenta(z):
            e_, i_ = veiculo(z)
            return sb.ajusta_solido(pl, e_, i_, area, atm, h_m, t_v, partidas, limites), e_, i_

        def deficit(z):
            e_, i_ = veiculo(z)
            a_m, vo, gu = sb.semieixo_circular_maximo(pl, e_, i_, area, atm, t_v, partidas, limites, nm_)
            return (-1.0e7 if a_m is None else a_m - (pl.raio + h_m)), vo, gu
        return tenta, deficit

    def voo_raiz(r_):
        vo = r_[1][1]
        return {"custo": None, "fecha": True, "deficit_m": r_[1][0], "periapse_km": vo["periapse_m"] / 1000, "apoapse_km": vo["apoapse_m"] / 1000, "costa_s": vo["costa_s"], "guiamento": r_[1][2]}

    def dimensiona(lei, isp_):
        f_ = [m_ * i * sb.G0_M / t for m_, i, t in zip(mp, isp_, tq)]   # P-111: tempo de queima publicado
        x = {}
        tenta, deficit = maquina(lei, isp_, pl_e, 1000 * h)
        r_ = mf.escala_minima(tenta, deficit, lo, hi, passo, tol, v(em_["xtol_escala"]))   # P-117
        x["fecha_na_varredura"] = r_ is not None
        if r_ is None:
            return x
        b_ = r_[0]
        x["busca_da_escala"] = r_[2]
        e0, i0 = estagios(b_, lei, mp, f_, isp_, carga)
        cap0 = mf.capacidade(e0, i0, carga)
        # escala do caso com a margem: a capacidade cresce sem limite com a escala (o inerte cresce menos que o propelente)
        s1, s2 = b_, b_
        while mf.capacidade(*estagios(s2, lei, mp, f_, isp_, carga), carga) < (1 + margem) * cap0:
            s1, s2 = s2, 2 * s2
        while s2 - s1 > 1e-12 * s2:
            m_ = (s1 + s2) / 2
            s1, s2 = (m_, s2) if mf.capacidade(*estagios(m_, lei, mp, f_, isp_, carga), carga) < (1 + margem) * cap0 else (s1, m_)
        em, im = estagios(s2, lei, mp, f_, isp_, carga)
        x["sem_margem"] = {"escala": b_, "capacidade_m_s": cap0, "glom_kg": e0[0].massa_inicial_kg, "propelente_kg": [e.propelente_kg for e in e0], "inertes_kg": i0,
                           "voo": voo_raiz(r_), **geometria(e0)}
        x["com_margem"] = {"escala": s2, "capacidade_m_s": mf.capacidade(em, im, carga), "glom_kg": em[0].massa_inicial_kg, "propelente_kg": [e.propelente_kg for e in em],
                           "inertes_kg": im, "voo": voo(pl_e, em, im, 1000 * h), "voo_antecipada": voo(pl_e, em, im, 1000 * h, antecipada=True),
                           "voo_com_guinada": voo(pl_e, em, im, 1000 * h, guinada=True), **geometria(em)}
        return x

    casos = []
    for nome, lei in leis.items():
        e1, i1 = estagios(1.0, lei, mp, f, isp, carga)
        x = {"lei": nome, "N_kg": lei[0], "c": lei[1], "b": lei[2], "verificacao": {**voo(pl_v, e1, i1, 1000 * v(vf["orbita_km"])), "inertes_kg": i1, "glom_kg": e1[0].massa_inicial_kg}}
        x.update(dimensiona(lei, isp))
        casos.append(x)
    # ---------------- viés do modelo na variante nominal (P-114) e a variante corrigida
    nom = next(k for k in leis if k.startswith(cfg["variante_nominal"]))
    lei_n = leis[nom]
    vz = cfg["vies"]

    # o menor fator no Isp com que o MAV do MSR chega à circular publicada (P-117 aplicado ao fator, P-114)
    f_lo, f_top = vz["fator_isp_busca"]["valor"]
    tenta_v, deficit_v = maquina(lei_n, isp, pl_v, 1000 * v(vf["orbita_km"]), "fator")
    rv_ = mf.escala_minima(tenta_v, deficit_v, f_lo, f_top, v(vz["passo_varredura"]), tol, v(em_["xtol_escala"]))
    vies = {"variante": nom, "fecha_na_busca": rv_ is not None}
    if rv_ is not None:
        f_hi = rv_[0]

        def fecha_verif(fator):
            isp_ = [i * fator for i in isp]
            f_ = [m_ * i * sb.G0_M / t for m_, i, t in zip(mp, isp_, tq)]
            e_, i_ = estagios(1.0, lei_n, mp, f_, isp_, carga)
            return voo_raiz(rv_), mf.capacidade(e_, i_, carga)
        rv, cap_v = fecha_verif(f_hi)
        cap_1 = mf.capacidade(*estagios(1.0, lei_n, mp, f, isp, carga), carga)
        vies.update({"fator_isp": f_hi, "dv_vies_m_s": cap_v - cap_1, "voo": rv})
        corr = dimensiona(lei_n, [i * f_hi for i in isp])
        corr.update({"lei": nom + ", corrigida pelo viés"})
        vies["corrigida"] = corr
    # incerteza numérica do integrador (results/conferencia/ruido_subida.yaml), ao lado da P-114
    rs = ler("results/conferencia/ruido_subida.yaml")["reprodutibilidade"]
    at = next(x for x in rs if x["variante"] == "atual")
    incerteza = [(x["escala"] - at["escala"]) / at["escala"] for x in rs if x["metodo"].startswith("primeira ordem")]
    # ---------------- (b): aceitar a órbita do sólido com margem e levar o orbitador elétrico até ela
    caso_n = next(c for c in casos if c["lei"] == nom)
    orb = None
    if caso_n.get("fecha_na_varredura"):
        import orbitador_eletrico as oe
        from orbital import baixo_empuxo as be
        from orbital import hibrido as hb
        from orbital.config import parametros
        po = ler("config/parametros_orbitais.yaml")
        mu, R = parametros().mu_marte, v(po["raio_marte_km"])
        rb = ler("results/etapa7.2/rotas_mav.yaml")
        prop = cfg["propulsor_orbitador"]["valor"]
        el = next(x for x in rb["rota_b"] if abs(x["altitude_km"] - h) < 1e-6)["propulsores"][prop]["eletrico_primeiro_que_fecha"]
        se = oe.sistema(prop, el["n_ativos"], ler("config/eletrica.yaml"), ler("config/plataformas.yaml"))
        m0 = el["orbitador_injetado_kg"]   # limite superior da massa no encontro: o tempo sai maior que o real
        vo = caso_n["com_margem"]["voo"]
        rp_, ra_ = R + vo["periapse_km"], R + vo["apoapse_km"]
        t_on1, t_d1, dv1, m1 = hb.tempos_espiral(mu, R, R + h, rp_, m0, se)
        arc = be.apoapse_por_arcos(mu, rp_, rp_, ra_, se.empuxo_total_n, se.isp_s, m1, float(ler("config/eletrica.yaml")["varredura"]["c1_meio_arco_graus"]["valor"]))
        orb = {"propulsor": prop, "n_ativos": el["n_ativos"], "massa_kg": m0, "orbita_km": [vo["periapse_km"], vo["apoapse_km"]],
               "circular_dv_m_s": 1000 * dv1, "circular_dias": (t_on1 + t_d1) / 86400, "apoapse_dv_m_s": 1000 * arc.dv_km_s, "apoapse_dias": arc.tempo_total_s / 86400,
               "apoapse_final_km": arc.ra_final_km - R, "periapse_final_km": arc.rp_final_km - R, "subida_dias_familia1": el["subida_dias"],
               "semieixo_alt_eq_km": (rp_ + ra_) / 2 - v(cfg["raio_equatorial_f273_km"])}
    out = nativo({"gerado_por": "tools/inerte_solido.py", "status": "NÃO VALIDADO", "lb_para_kg": lb, "motores": mot, "ajuste": ajuste_cat, "comparacao_msr": comparacao,
                  "p019_k": eps / (1 - eps), "p111_k": [i / x for i, x in zip(ine_v, mp)], "altitude_km": h, "margem_dv": margem, "tol_custo": tol, "passo": passo,
                  "orbita_verificacao_km": v(vf["orbita_km"]), "criterio_selecao": cfg["criterio_selecao"],
                  "fracao_2_f269": (Im[1] + Nm[1]) / (sum(Im) + sum(Nm)), "fracao_2_p110": mv["verificacao"]["base"]["fracao_inerte_2"],
                  "costa_publicada_s": v(vf["costa_publicada_s"]), "alvo_folga_m": a4["alvo_folga_m"], "casos": casos,
                  "comprimento": comp, "vies": vies, "orbitador_b": orb, "variante_nominal": nom,
                  "incerteza_integrador": incerteza, "fracao_2_p110_original": fc["errata_mavs_2026_11_12"]["fracao_inerte_2_base"], "semieixo_max_alt_km": v(cfg["semieixo_max_alt_km"]),
                  "antecedencia_max_s": v(cfg["antecedencia_max_s"])})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "inerte_solido.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def e_(x):
    return f"{x:.1e}".replace(".", ",")


def faixa(par, f=sg):
    a, b = par
    return f(a) if abs(a - b) < 5e-4 else f"{f(a)} a {f(b)}"


def escreve_md(o):
    aj = o["ajuste"]
    lim2 = (aj["b"] - 2 * aj["erro_padrao_b"], aj["b"] + 2 * aj["erro_padrao_b"])
    md = ["# Lei de massa inerte do MAV sólido (gerado por tools/inerte_solido.py)", "", "**NÃO VALIDADO.** Premissas P-014, P-019, P-108, P-110, P-111, P-113 (aprovada como NÃO VALIDADA em 2026-11-10: variante A nominal, B sensibilidade), P-114 e P-115.", "",
          "## Motores do catálogo [F270] (inerte total impresso, salvo o Orion 38)", "", "Critério: " + o["criterio_selecao"], "",
          "| Motor | Envelope | Propelente (kg) | Inerte (kg) | Inerte/propelente | Fator do resíduo | PDF p. |", "| :- | :- | -: | -: | -: | -: | -: |"]
    md += [f"| {m['nome']} | {m['envelope']} | {br(m['propelente_kg'], 1)} | {br(m['inerte_kg'], 1)} | {br(m['inerte_sobre_propelente'], 3)} | {br(m['residuo_fator'], 2)} | {m['pagina_pdf']} |" for m in o["motores"]]
    md += ["", f"Massas do catálogo em lbm; 1 lb = {br(o['lb_para_kg'], 7)} kg ([F112] p. 65 do PDF).", "",
           "## Ajuste", "",
           f"- Forma: potência, inerte = a · propelente^b, mínimos quadrados em ln, {aj['n']} motores de {br(aj['faixa_propelente_kg'][0], 1)} a {br(aj['faixa_propelente_kg'][1], 0)} kg de propelente.",
           f"- a = {br(aj['a'], 3)}, b = {br(aj['b'], 3)} (erro-padrão {br(aj['erro_padrao_b'], 3)}; ±2 erros-padrão: {br(lim2[0], 3)} a {br(lim2[1], 3)}).",
           f"- Erro do ajuste: fator rms {br(aj['fator_rms'], 2)} (resíduo rms em ln {br(aj['rms_ln'], 3)}); maior desvio, fator {br(aj['fator_max'], 2)}.",
           f"- Proporcional (b = 1, a forma da P-019 e da P-111): k = {br(aj['proporcional']['k'], 3)}, fator rms {br(aj['proporcional']['fator_rms'], 2)}, maior desvio {br(aj['proporcional']['fator_max'], 2)}.",
           "", "## Comparação no tamanho do MSR (kg)", "",
           "| Estágio | Propelente | Motor pelo catálogo | Motor do MSR [F269] | Não propulsivo do MSR | Estágio do MSR | P-019 | P-111 | Lei A | Lei B |", "| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
    md += [f"| {c['estagio']} | {br(c['propelente_kg'], 1)} | {br(c['catalogo_motor_kg'], 1)} | {br(c['msr_motor_kg'], 0)} | {br(c['msr_nao_propulsivo_kg'], 0)} | {br(c['msr_estagio_kg'], 0)} | {br(c['p019_estagio_kg'], 1)} | {br(c['p111_estagio_kg'], 1)} | {br(c['lei_A_estagio_kg'], 1)} | {br(c['lei_B_estagio_kg'], 1)} |" for c in o["comparacao_msr"]]
    linear = lim2[0] <= 1.0 <= lim2[1]
    md += ["", "## O que os dados sustentam", "",
           f"- **Escala.** A P-019 (k = {br(o['p019_k'], 3)} nos dois estágios) e a P-111 (k = {br(o['p111_k'][0], 3)} e {br(o['p111_k'][1], 3)}) são proporcionais: o inerte cresce como o propelente (b = 1). "
           + ("O catálogo é compatível com b = 1 dentro de ±2 erros-padrão." if linear else f"O catálogo dá b = {br(aj['b'], 2)}, e b = 1 fica fora de ±2 erros-padrão: **para o motor, os dados não sustentam a escala proporcional de nenhuma das duas**; ao crescer, a fração inerte do motor cai. Para o estágio inteiro, isso depende também de como cresce o inerte não propulsivo, que não tem fonte (a P-113 o fixa). O catálogo junta projetos diferentes: a dispersão entre eles não é a escala de um único projeto."),
           "- **Erro-padrão.** Supõe resíduos independentes; há variantes do mesmo motor (STAR 26/26B/26C, 30BP/30C/30C-BP/30E, 37FM/37FMV), então o erro-padrão está subestimado. A distância de b a 1 é de " + f"{br((1 - aj['b']) / aj['erro_padrao_b'], 1)} erros-padrão.",
           "- **Nível.** No tamanho do MSR, o motor do catálogo é mais leve que o motor do MSR [F269] (tabela acima). A verificação da P-110 reproduz o inerte total do MSR e a órbita publicada, não a divisão por estágio: a P-111 dá " + f"{br(o['comparacao_msr'][0]['p111_estagio_kg'], 1)} e {br(o['comparacao_msr'][1]['p111_estagio_kg'], 1)} kg, contra {br(o['comparacao_msr'][0]['msr_estagio_kg'], 0)} e {br(o['comparacao_msr'][1]['msr_estagio_kg'], 0)} kg do [F269]. A P-019 dá outra divisão. Nenhuma das duas separa o inerte não propulsivo (aviônica, RCS, estrutura da carga), que o [F269] dá à parte.",
           "- **Divisão do inerte (P-110).** A justificativa original da P-110 dizia que a divisão por estágio não tinha fonte; o [F269] publica uma (fração do estágio 2 = " + f"{br(o['fracao_2_f269'], 3)}, contra {br(o['fracao_2_p110_original'], 2)} escolhida pela varredura da P-110). Errata da P-110 aplicada (aprovada pelo Fabio em 2026-11-12): vale a do [F269]; ver o fim da página.",
           "- **Lei (P-113, NÃO VALIDADA; aprovada pelo Fabio em 2026-11-10):** inerte do estágio = N + c · P^b, com b do catálogo e N, o não propulsivo do [F269], fixo. Nível c: A, pelo motor do MSR [F269] (nominal); B, pela divisão que a verificação da P-110 escolheu (sensibilidade).",
           "", f"## Subida com cada variante (modelo de subida do sólido; tolerância {o['tol_custo']:.0e}, passo da varredura {br(o['passo'], 2)}, os da P-110)".replace(".0e", "e"), ""]
    def tabela(c):
        t = [f"| Caso, {br(o['altitude_km'], 0)} km | Escala | Capacidade (m/s) | GLOM (kg) | Propelente (kg) | Inertes (kg) | Órbita simulada (km) | Chega? | Comprimento (m, P-108 revista) | 4,65 m com deck | 4,65 m sem deck | 4,5 m com deck |",
             "| :- | -: | -: | -: | -: | -: | :- | :- | -: | -: | -: | -: |"]
        for rot, k in (("sem margem (o menor que chega)", "sem_margem"), ("com a margem da P-014 na capacidade", "com_margem")):
            y = c[k]
            t.append(f"| {rot} | {br(y['escala'], 3)} | {br(y['capacidade_m_s'], 0)} | {br(y['glom_kg'], 1)} | {br(y['propelente_kg'][0], 1)} + {br(y['propelente_kg'][1], 1)} | {br(y['inertes_kg'][0], 1)} + {br(y['inertes_kg'][1], 1)} | "
                     f"{br(y['voo']['periapse_km'], 0)} × {br(y['voo']['apoapse_km'], 0)} | {'sim' if y['voo']['fecha'] else 'não'} | "
                     f"{br(y['comprimento_m'], 2)} | {sg(y['folga_465_com_deck_m'])} | {sg(y['folga_465_sem_deck_m'])} | {sg(y['folga_45_com_deck_m'])} |")
        return t
    for c in o["casos"]:
        vf = c["verificacao"]
        papel = "nominal" if c["lei"] == o["variante_nominal"] else "sensibilidade"
        md += [f"### Lei {c['lei']}: {papel}", "",
               f"- N = {br(c['N_kg'][0], 0)} e {br(c['N_kg'][1], 0)} kg; c = {br(c['c'][0], 3)} e {br(c['c'][1], 3)}; b = {br(c['b'], 3)}." + (" O c da variante A é calibrado no propelente do [F269] (216 e 54 kg) e aplicado ao do MSR usado no estudo (216 e 54,4 kg, config/cad.yaml), daí o estágio 2 com um pouco mais que 48 kg." if c["lei"].startswith("A") else ""),
               f"- Verificação com o MAV do MSR (órbita publicada de {br(o['orbita_verificacao_km'], 0)} km): inertes {br(vf['inertes_kg'][0], 1)} e {br(vf['inertes_kg'][1], 1)} kg; órbita {br(vf['periapse_km'], 0)} × {br(vf['apoapse_km'], 0)} km; costa {br(vf['costa_s'], 0)} s (publicada {br(o['costa_publicada_s'], 0)} s); "
               + ("**chega à órbita publicada**." if vf["fecha"] else f"**não chega à órbita publicada** (resíduo {vf['custo']:.1e}).".replace(".", ",", 1))]
        if not c["fecha_na_varredura"]:
            md += [f"- {br(o['altitude_km'], 0)} km: não fecha na varredura da P-110.", ""]
            continue
        md += [""] + tabela(c) + [""]
    if all(c["fecha_na_varredura"] for c in o["casos"]):
        md += [f"As duas variantes chegam à circular de {br(o['altitude_km'], 0)} km; a escala mínima é a raiz da P-117 (results/familia1/mavs.md).", ""]
    md += [f"Alvo de folga: {sg(o['alvo_folga_m'], 2)} m. O caso com a margem foi simulado com o mesmo guiamento (subida vertical, tangente linear, costa e queima do estágio 2 antes do apoapse): o sólido não regula o empuxo, então a capacidade a mais só chega à órbita de {br(o['altitude_km'], 0)} km se o guiamento conseguir gastá-la; \"não\" na coluna \"Chega?\" quer dizer que ele passa da órbita com esse guiamento, não que falta Δv. O gasto por guinada está na seção da energia que sobra.", ""]
    vz = o["vies"]
    md += ["## Viés do modelo de subida do sólido (P-114, NÃO VALIDADO)", ""]
    if vz.get("fator_isp"):
        vv = vz["voo"]
        md += [f"Fator comum no Isp dos dois estágios que leva o MAV do MSR na variante {vz['variante'][0]} à órbita publicada: **{br(vz['fator_isp'], 4)}**, ou **{br(vz['dv_vies_m_s'], 0)} m/s** de capacidade ideal (órbita {br(vv['periapse_km'], 0)} × {br(vv['apoapse_km'], 0)} km). É a incerteza do modelo de subida do sólido (P-114, aprovada pelo Fabio em 2026-11-12 como NÃO VALIDADA); o modelo não foi ajustado.", "",
               f"**Incerteza numérica do modelo de subida** (aceita pelo Fabio em 2026-11-12 como sensibilidade numérica): com o rtol e o atol do integrador × 0,5 e × 2, a escala mínima do sólido muda {' e '.join(e_(x) for x in o['incerteza_integrador'])} relativo (results/conferencia/ruido_subida.md).", "",
               "### Variante nominal corrigida pelo viés (Isp × fator nos dois estágios)", ""]
        cr = vz["corrigida"]
        md += (tabela(cr) if cr.get("fecha_na_varredura") else [f"Não fecha na varredura da P-110 a {br(o['altitude_km'], 0)} km."]) + [""]
    else:
        md += ["Nenhum fator de Isp na busca da P-114 leva o MAV do MSR à órbita publicada: viés não medido.", ""]
    cp = o["comprimento"]
    md += ["## Comprimento (P-108 revista, aplicada)", "", "P-108 revista, aprovada pelo Fabio em 2026-11-12 como NÃO VALIDADA; o ajuste está em results/familia1/comprimento_solido.md.", "",
           f"- Os {cp['n']} motores do catálogo publicam diâmetro e comprimento (\"Motor length\"; no Orion 38, \"Overall motor length (including nozzle)\"); nenhum tem bocal extensível.",
           f"- Forma: L = a · P^b · D^c, mínimos quadrados em ln: a = {br(cp['a'], 4)}, b = {br(cp['b'], 3)} (erro-padrão {br(cp['erro_padrao_b'], 3)}), c = {br(cp['c'], 3)} (erro-padrão {br(cp['erro_padrao_c'], 3)}); erro: fator rms {br(cp['fator_rms'], 2)}, maior desvio fator {br(cp['fator_max'], 2)}.",
           f"- Só com o propelente (L = a · P^b): b = {br(cp['so_propelente']['b'], 3)}, fator rms {br(cp['so_propelente']['fator_rms'], 2)}, maior desvio {br(cp['so_propelente']['fator_max'], 2)}. O diâmetro entra porque o do MAV é fixo e menor que o da maioria dos motores.",
           f"- No Ø {br(cp['diametro_mav_m'], 2)} m do MAV e no propelente do MSR: motores de {br(cp['motores_msr_m'][0], 2)} e {br(cp['motores_msr_m'][1], 2)} m. O resto até os {br(cp['comprimento_msr_m'], 1)} m do MSR ([F247]), {br(cp['resto_m'], 2)} m, é interestágio, carga, aviônica e adaptadores: continua sem fonte e fica fixo na escala.",
           "- Comprimento do MAV = motor do estágio 1 + motor do estágio 2 (pelo ajuste) + o resto fixo acima. A P-108 original escalava o comprimento não fixo na proporção do propelente, com a parte fixa de 0 a 1,5 m (registro na errata de results/familia1/mavs.md).", ""]
    ob = o["orbitador_b"]
    cn = next(c for c in o["casos"] if c["lei"] == o["variante_nominal"])
    md += ["## Energia que sobra no sólido com margem (variante nominal)", ""]
    if ob:
        cm = cn["com_margem"]
        vg = cm["voo_com_guinada"]
        va = cm["voo_antecipada"]
        md += [f"- **(a1) Ignição antecipada do estágio 2, o método do MSR** ([F230] PDF p. 9: \"This second stage burn is performed slightly before predicted apoapsis, expending excess energy by lowering apoapsis while at the same time raising periapsis\"; [F271] PDF p. 3: \"The solid motors are sized so as to nominally impart more delta-v than required to meet the target orbit\"), com a antecedência até o limite da P-115: "
               + (f"chega a {br(va['periapse_km'], 0)} × {br(va['apoapse_km'], 0)} km, acendendo {br(va['guiamento']['t_antes_apoapse_s'], 0)} s antes do apoapse." if va["fecha"] else f"não chega a {br(o['altitude_km'], 0)} km (melhor órbita {br(va['periapse_km'], 0)} × {br(va['apoapse_km'], 0)} km, antecedência ótima {br(va['guiamento']['t_antes_apoapse_s'], 0)} s, longe do limite de {br(o['antecedencia_max_s'], 0)} s: o limite não esteve ativo). Com o empuxo do estágio 2 na horizontal local, antecipar a ignição não tira energia; o excesso vem do estágio 1 (guiamento no limite c₁ = " + f"{br(va['guiamento']['c_1_s'], 3)} 1/s da P-110), e o semieixo fica acima do alvo. No MSR o excesso era menor e o estágio 2 tinha guiamento próprio; gastar um excesso deste tamanho exige apontar fora do ótimo, que é o (a2).")]
        md += [f"- **(a2) Guinada alternada do estágio 2 (P-115, sem fonte para o MAV; o mais próximo é o GEM, pilotagem fora do ótimo, [F272] PDF p. 4):** " + f"melhor órbita {br(vg['periapse_km'], 2)} × {br(vg['apoapse_km'], 2)} km com guinada de {br(vg['guiamento']['guinada_2_graus'], 1)}° (resíduo {vg['custo']:.1e}".replace(".", ",", 1) + f", tolerância {o['tol_custo']:.0e}: " + ("dentro" if vg["fecha"] else "**fora**") + " da tolerância da P-110). Custo para a missão: nenhuma massa a mais (a margem já está no MAV); o que se perde é a energia da margem quando ela não é usada.",
               f"- **(b) Aceitar a órbita do sólido ({br(ob['orbita_km'][0], 0)} × {br(ob['orbita_km'][1], 0)} km) e levar o orbitador até ela** (orbitador só elétrico, {ob['propulsor']} × {ob['n_ativos']}, **calculado, não verificado**, e não usado como fato). Limite superior, na hipótese de o orbitador esperar na circular de {br(o['altitude_km'], 0)} km, com a massa injetada ({br(ob['massa_kg'], 0)} kg):",
               f"  - subir a circular de {br(o['altitude_km'], 0)} km até o periapse: {br(ob['circular_dv_m_s'], 0)} m/s, {br(ob['circular_dias'], 1)} dias; essa parte se recupera na espiral de saída (Edelbaum coplanar: o Δv entre circulares soma), então não entra no custo;",
               f"  - subir o apoapse em arcos em torno do periapse (P-049): {br(ob['apoapse_dv_m_s'], 0)} m/s, {br(ob['apoapse_dias'], 1)} dias (fim em {br(ob['periapse_final_km'], 0)} × {br(ob['apoapse_final_km'], 0)} km);",
               f"  - semieixo dessa órbita a {br(ob['semieixo_alt_eq_km'], 0)} km de altitude sobre o raio equatorial (o referencial do [F273]), acima do limite de {br(o['semieixo_max_alt_km'], 0)} km do MSR ([F273] PDF p. 1): no MSR, essa órbita estaria fora da faixa aceita;",
               f"  - custo: no máximo {br(ob['apoapse_dv_m_s'], 0)} m/s e {br(ob['apoapse_dias'], 1)} dias, sem a fase (RAAN e anomalia). Não foi calculado o ganho: na rota B o orbitador desce em espiral desde a captura, e uma órbita de encontro mais alta encurta a descida e a espiral de saída.",
               "- **Qual afeta menos a missão:** " + ("(a): não muda massa nem datas." if (va["fecha"] or vg["fecha"]) else f"pelos critérios atuais, nenhum dos dois fecha: (a2) erra a circular de {br(o['altitude_km'], 0)} km por {br(1000 * max(abs(vg['periapse_km'] - o['altitude_km']), abs(vg['apoapse_km'] - o['altitude_km'])), 0)} m (resíduo acima da tolerância da P-110), e a órbita de (b) fica fora da faixa do MSR. (a2) não custa massa nem datas, mas a guinada não tem fonte para o MAV; o custo de (b) é só um limite superior, com o orbitador não verificado. Os dados não bastam para ordenar as duas; decisão do Fabio."), ""]
    md += ["## Errata da P-110 (aplicada)", "",
           f"- Aprovada pelo Fabio em 2026-11-12: a divisão do inerte do [F269] (fração do estágio 2 = {br(o['fracao_2_f269'], 3)}) é a base da escala, no lugar da que a varredura escolhia ({br(o['fracao_2_p110_original'], 2)}, registro em results/familia1/mavs.md). "
           f"Com ela, a verificação não chega à órbita publicada, e a diferença é o viés da P-114 (acima).",
           f"- Consequência para a P-113: a variante B tomava o nível da divisão verificada da P-110, que agora é a do [F269]; ela fica quase igual à A (estágios de {br(o['comparacao_msr'][0]['lei_B_estagio_kg'], 1)} e {br(o['comparacao_msr'][1]['lei_B_estagio_kg'], 1)} kg, contra {br(o['comparacao_msr'][0]['lei_A_estagio_kg'], 1)} e {br(o['comparacao_msr'][1]['lei_A_estagio_kg'], 1)} kg na A, no tamanho do MSR). A diferença que resta vem do inerte total ([F34] contra [F269]).", ""]
    (SAIDA / "inerte_solido.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
