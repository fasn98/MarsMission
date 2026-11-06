"""Portão do comprimento do MAV (ADR 0023): dados pedidos pelo Fabio para decidir a rota A provisória e a P-097.

- Item 2: alvo com deck, por Ø; núcleo do lander no CAD atual; arranjo do MSL e do Mars 2020 nas fontes; Isp mínimo do 44:1.
- Item 3: tanques aninhados dimensionados: pressão, cúpulas, vão de purga, massa e comprimento real, com o estágio 2 em
  quatro geometrias lado a lado (a escolha é do Fabio).
- Item 5: folgas nas coifas com a altura dos adaptadores do guia do Vulcan.
Nada disso entra no CAD nem nas premissas. O que não tem fonte fica em varredura e está marcado NÃO VALIDADO.
Saída: results/etapa7.2/rota_a.yaml e .md

Uso: python tools/rota_a_dimensiona.py
"""

from __future__ import annotations

import copy
import math
import re
import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import comprimento_mav as cmv  # noqa: E402
import encaixe_coifas as ec  # noqa: E402
import envelope_arranjo as ea  # noqa: E402
import cad_parametros as cp  # noqa: E402
from orbital import veiculos as ve  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"
POL = 0.0254   # [F112] Apêndice B.8, PDF p. 62: polegada em metros
FATOR_4 = 1 + math.sqrt(2)   # círculo mínimo de 4 círculos iguais
PASSOS = 40   # bisseção do Isp (escolha numérica)


def br(x, n=3):
    return f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def sg(x, n=3):
    return f"{round(x, n) + 0.0:+,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def main():
    cad, ma, par = ler("config/cad.yaml"), ler("results/etapa7.2/mav_arranjo.yaml"), ler("results/etapa7.2/parametros.yaml")
    env, arq, mot = ler("results/etapa7.1/envelope.yaml"), ler("results/etapa2.5/arquitetura.yaml"), ler("config/motores.yaml")
    ra, ad = cad["rota_a_dimensionamento"], cad["adaptador_coifa"]
    pr = cad["propelentes"]
    arg = (v(pr["razao_mistura_r4d11"]), v(pr["densidade_oxidante_kg_m3"]), v(pr["densidade_mmh_kg_m3"]), v(pr["fracao_ullage"]))
    mcfg, po = ler("config/mav_propulsao.yaml"), ler("config/parametros_orbitais.yaml")
    R = v(po["raio_marte_km"])
    pl = ler("results/etapa2.3/plataformas.yaml")["orbita_encontro"]
    h0p, h0a = pl["periapse_alt_km"], pl["apoapse_regra_5pct_km"]
    op = ler("results/etapa2.2/mav_propulsao.yaml")["melhor_opcao"]
    nt = {k: v(x) for k, x in cad["mav"]["comprimento_nao_tanque_m"].items()}
    rd = cad["r4d11_variantes"]
    fr = v(rd["a_frente_da_flange_pol"])
    m44 = (rd["44:1"]["flange_a_saida_pol"] + fr) * POL
    nt44 = {**nt, "motores_estagio_1": m44, "motor_estagio_2": m44}
    t_par = v(cad["mav"]["espessura_parede_m"])
    d0 = v(cad["mav"]["diametro_opcoes_m"][cad["escolha"]["mav_diametro"]])
    caso = {c["diametro_m"]: c for c in ma["casos"]}
    forma = cad["rotas_mav"]["alvo"]["aeroshell"]
    est = {d: {e["estacao"]: e for e in c["formas"][forma]} for d, c in caso.items()}
    deck = {d: next(k for k in est[d] if "P-094" in k) for d in caso}
    lim_deck = {d: caso[d]["comprimento_m"] + 2 * est[d][deck[d]]["deitado_folga_m"] for d in caso}
    lim_ombro = {d: caso[d]["comprimento_m"] + 2 * est[d]["ombro"]["deitado_folga_m"] for d in caso}
    alvo = float(ra["alvo_folga_deck_m"])
    saidas = {"44:1": FATOR_4 * rd["44:1"]["diametro_saida_pol"] * POL, "164:1": FATOR_4 * rd["164:1"]["diametro_saida_pol"] * POL}
    d_alvo = min(d for d in caso if d - 2 * t_par >= saidas["44:1"])

    # ---------------- item 3: dimensionamento
    ti, fl = ra["titanio"], ra["flambagem"]
    mpa = v(ra["ksi_para_mpa"])
    ftu, fty, ec_ = v(ti["ftu_ksi"]) * mpa, v(ti["fty_ksi"]) * mpa, v(ti["ec_ksi"]) * mpa
    fs, fs_fl = v(ra["fator_seguranca_pressao"]), v(ra["fator_seguranca_flambagem"])
    sigma = min(ftu / fs, fty)
    nu = v(fl["poisson"])
    di = d_alvo - 2 * t_par
    r_i = di / 2
    rho_ti = v(cad["materiais"][cad["construcao"]["tanques"]["material"]])
    t_p093 = v(cad["construcao"]["tanques"]["espessura_m"])

    def t_cilindro(p):
        return p * r_i / sigma

    def t_cupula(p):
        return p * r_i / (2 * sigma)

    def t_flambagem(p, k):
        return r_i * math.sqrt(fs_fl * p * math.sqrt(3 * (1 - nu ** 2)) / (2 * ec_ * k))
    pressoes = {n: {"mpa": v(x), "fonte": x["fonte"], "t_cilindro_m": t_cilindro(v(x)), "t_cupula_m": t_cupula(v(x)),
                    "t_cupula_invertida_m": {str(k): t_flambagem(v(x), k) for k in fl["fatores_reducao"]}} for n, x in ra["pressao_tanque_mpa"].items()}
    p_base = pressoes[ra["pressao_base"]]["mpa"]

    carga, n_mot, m_motor = v(ler("config/superficie.yaml")["mav"]["carga_util_kg"]), ra["motores_por_estagio"], rd["164:1"]["massa_kg"]

    def lander_isp(isp):
        m2 = copy.deepcopy(mcfg)
        m2["opcoes"][op]["isp_s"] = [isp, isp]
        return ve.lander(R + h0p, R + h0a, mcfg=m2, detalhe=True)

    def lente(ra_, rr, c):
        """Volume comum a duas esferas de raios ra_ e rr, com centros à distância c."""
        return math.pi * (ra_ + rr - c) ** 2 * (c ** 2 + 2 * c * (rr + ra_) - 3 * (rr - ra_) ** 2) / (12 * c)

    def esboco(v1, v2, g, t_d, t_i, r_max, hemi):
        """Esfera num recesso de outra, nas duas ordens, com o menor comprimento; `hemi` limita o recesso a um hemisfério.
        Comprimento e massa com vão e paredes."""
        melhor = None
        for va, vb in ((v1, v2), (v2, v1)):
            r1 = (3 * vb / (4 * math.pi)) ** (1 / 3)
            rr = r1 + g + t_d + t_i
            a_, b_ = (3 * va / (4 * math.pi)) ** (1 / 3), r_max
            for _ in range(3):   # passes de refino da grade em torno do melhor raio da ordem
                grade, Ls = np.linspace(a_, b_, int(ra["grade_esboco"])), []
                for ra_ in grade:
                    falta = 4 / 3 * math.pi * ra_ ** 3 - va
                    lo = max(abs(ra_ - rr), math.sqrt(max(ra_ ** 2 - rr ** 2, 0.0)) if hemi else 0.0, 1e-9)
                    hi = ra_ + rr
                    if lente(ra_, rr, lo) < falta:
                        Ls.append(math.inf)
                        continue
                    for _ in range(PASSOS):
                        mid = (lo + hi) / 2
                        lo, hi = (mid, hi) if lente(ra_, rr, mid) > falta else (lo, mid)
                    c = hi
                    d1 = (c ** 2 + ra_ ** 2 - rr ** 2) / (2 * c)
                    area_ext = 4 * math.pi * ra_ ** 2 - 2 * math.pi * ra_ * (ra_ - d1) + 4 * math.pi * r1 ** 2
                    area_rec = 2 * math.pi * rr * (rr - (c - d1))
                    x = {"comprimento_m": max(ra_ + c + r1, 2 * ra_), "massa_kg": rho_ti * (area_ext * t_d + area_rec * t_i), "raio_tanque_ao_redor_m": ra_, "raio_esfera_m": r1, "raio_recesso_m": rr, "distancia_centros_m": c}
                    Ls.append(x["comprimento_m"])
                    if melhor is None or x["comprimento_m"] < melhor["comprimento_m"]:
                        melhor = x
                i_ = int(np.argmin(Ls))
                a_, b_ = grade[max(i_ - 1, 0)], grade[min(i_ + 1, len(grade) - 1)]
        return melhor

    def antepara(v1, v2, g, t_d, t_i, lt, k):
        """Esfera de volume somado, dividida no equador por calota de altura h: a lente recua o vão e as paredes. O raio da
        calota sai dos volumes; a espessura de flambagem com esse raio é informada, não aplicada: fica fora do domínio da fórmula."""
        rs = lt / 2
        dif = abs(v1 - v2) / 2
        lo, hi = 0.0, rs
        for _ in range(PASSOS):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if math.pi * mid * (3 * rs ** 2 + mid ** 2) / 6 < dif else (lo, mid)
        h = hi
        r_cal = (rs ** 2 + h ** 2) / (2 * h)
        return {"comprimento_m": lt + g + t_d + t_i, "massa_kg": rho_ti * (4 * math.pi * rs ** 2 * t_d + math.pi * (rs ** 2 + h ** 2) * (t_d + t_i)), "altura_calota_m": h, "raio_calota_m": r_cal, "t_flambagem_no_raio_da_calota_m": t_flambagem(p_base, k) * r_cal / r_i}

    def lente_igual(v1, v2, g, t_d, t_i, lt):
        """Esfera de volume somado, cortada por outra do mesmo raio: a lente tem o menor volume e recua o vão e as paredes."""
        rs = lt / 2
        alvo_v = min(v1, v2)
        lo, hi = 1e-9, 2 * rs
        for _ in range(PASSOS):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if lente(rs, rs, mid) > alvo_v else (lo, mid)
        c = hi
        area_cal = 2 * math.pi * rs * (rs - c / 2)
        return {"comprimento_m": lt + g + t_d + t_i, "massa_kg": rho_ti * (4 * math.pi * rs ** 2 * t_d + area_cal * (t_d + t_i)), "raio_m": rs, "distancia_centros_m": c, "raio_borda_m": math.sqrt(rs ** 2 - (c / 2) ** 2)}

    def real(est_m, d, g, k, fam):
        """Comprimento real e massa dos tanques aninhados: tanque único com o volume somado, mais o vão de purga e as duas
        paredes da antepara, por estágio; quando o volume cabe numa esfera menor que o diâmetro interno, entra a geometria
        `fam`. Espessura: a maior entre a de pressão e a de construção (P-093)."""
        t_c = max(t_cilindro(p_base), t_p093)
        t_d = max(t_cupula(p_base), t_p093)
        t_i = max(t_flambagem(p_base, k), t_p093)
        di_ = d - 2 * t_par
        L = cmv.comprimento(d, est_m, nt44, cad, aninhado=True)
        massa, por_est = 0.0, []
        for i, e in enumerate(est_m):
            vol = ea.volumes(e["propelente_kg"], *arg)
            v1, v2 = vol["tanque_oxidante_m3"], vol["tanque_combustivel_m3"]
            L += g + t_d + t_i
            lt = ea.tanque_cilindrico(v1 + v2, di_)
            lc = max(lt - di_, 0.0)
            a_hem = 2 * math.pi * (min(lt, di_) / 2) ** 2
            m_e = rho_ti * (math.pi * di_ * lc * t_c + 3 * a_hem * t_d + a_hem * t_i)   # 3 cúpulas normais e 1 invertida
            es = None
            if lt < di_:
                es = {"antepara_assimetrica": lambda: antepara(v1, v2, g, t_d, t_i, lt, k), "lente_mesmo_raio": lambda: lente_igual(v1, v2, g, t_d, t_i, lt)}.get(fam, lambda: esboco(v1, v2, g, t_d, t_i, di_ / 2, fam == "recesso_hemisferio"))()
                L += es["comprimento_m"] - (lt + g + t_d + t_i)
                m_e = es["massa_kg"]
            massa += m_e
            prox = est_m[i + 1]["massa_inicial_kg"] if i + 1 < len(est_m) else carga
            inerte = e["massa_inicial_kg"] - e["propelente_kg"] - prox
            motores = n_mot[i] * m_motor
            por_est.append({"estagio": i + 1, "inerte_kg": inerte, "tanques_kg": m_e, "parcela_do_inerte": m_e / inerte, "motores_164_kg": motores, "sobra_kg": inerte - m_e - motores,
                            "tanque_unico_m": lt, "volume_m3": v1 + v2, "volume_menor_m3": min(v1, v2), "vao_e_paredes_m": g + t_d + t_i, "geometria": es})
        return L, massa, por_est

    gs = [float(x) for x in ra["vao_purga_m"]["valores"]]
    g0 = float(ra["vao_purga_m"]["base"])
    ks = [float(k) for k in fl["fatores_reducao"]]
    k_b = float(fl["fator_base"])
    fams = list(ra["geometrias_estagio_2"])
    casos = []
    for isp in ra["isp_casos_s"]:
        lan = lander_isp(float(isp))
        e_ = lan["mav_estagios"]
        so = cmv.comprimento(d_alvo, e_, nt44, cad)
        lim = cmv.comprimento(d_alvo, e_, nt44, cad, aninhado=True)
        por_fam = {}
        for f in fams:
            L_b, mt_b, por_est = real(e_, d_alvo, g0, k_b, f)
            por_fam[f] = {"real_m": L_b, "reducao_real_m": so - L_b, "fracao_que_sobra": (so - L_b) / (so - lim), "folga_deck_real_m": (lim_deck[d_alvo] - L_b) / 2, "folga_ombro_real_m": (lim_ombro[d_alvo] - L_b) / 2,
                          "massa_tanques_kg": mt_b, "por_estagio": por_est, "por_vao": {str(g): real(e_, d_alvo, g, k_b, f)[0] for g in gs}}
        casos.append({"isp_s": isp, "glom_kg": e_[0]["massa_inicial_kg"], "so_44_m": so, "limite_otimista_m": lim, "reducao_limite_m": so - lim, "por_geometria": por_fam})

    # Isp mínimo com deck e folga ≥ alvo, para o limite otimista e para o comprimento real
    def isp_min(f):
        lo, hi = [float(x) for x in ra["faixa_isp_busca_s"]]
        if f(hi) > lim_deck[d_alvo] - 2 * alvo:
            return None
        for _ in range(PASSOS):
            mid = (lo + hi) / 2
            lo, hi = (lo, mid) if f(mid) <= lim_deck[d_alvo] - 2 * alvo else (mid, hi)
        return hi

    def l_lim(isp):
        return cmv.comprimento(d_alvo, lander_isp(isp)["mav_estagios"], nt44, cad, aninhado=True)

    def l_real(k, g, f):
        return lambda isp: real(lander_isp(isp)["mav_estagios"], d_alvo, g, k, f)[0]
    g_menor = float(ra["vao_purga_m"]["menor"])
    linhas_isp = [{"fator": k, "vao_m": g0, "por_geometria": {f: isp_min(l_real(k, g0, f)) for f in fams}} for k in ks]
    linhas_isp += [{"fator": k_b, "vao_m": g, "por_geometria": {f: isp_min(l_real(k_b, g, f)) for f in fams}} for g in (g_menor, max(gs))]
    isp_minimo = {"limite_otimista_s": isp_min(l_lim), "linhas": linhas_isp, "alvo_folga_m": alvo, "comprimento_max_m": lim_deck[d_alvo] - 2 * alvo}

    # ---------------- item 2: núcleo do lander no CAD atual
    ve_ = par["veiculos"]
    lan45 = cp.monta_lander(cad, env, arq, mot, "msl_m2020").corpos
    h_cz = par["conferencias"]["lander_vulcan"]["altura_estagio_cruzeiro_m"]

    def nucleo_de(forma_c, corpos_):
        c = next(x for x in corpos_ if x["nome"].startswith("Nucleo"))
        xs, rs = [float(x) for x in cad["capsulas"][forma_c]["x_m"]], [float(x) for x in cad["capsulas"][forma_c]["r_m"]]
        x_ = sorted(xs[-1] - (z - h_cz) for z in (c["p0"][2], c["p1"][2]))
        return {"estacao_de_m": x_[0], "estacao_ate_m": x_[1], "raio_m": c["r"], "raio_externo_na_frente_m": float(np.interp(x_[0], xs, rs)), "folga_a_face_externa_m": float(np.interp(x_[0], xs, rs)) - c["r"]}
    nucleo = {"srl_a": nucleo_de("srl_a", ve_["lander"]), "msl_m2020": nucleo_de("msl_m2020", lan45), "espessura_pica_m": v(cad["capsulas"]["espessura_pica_m"])}

    # ---------------- item 5: folgas com a altura do adaptador
    corpos = {"lander_4_5": ("Lander 4,5 m", lan45), "lander_4_65": ("Lander 4,65 m", ve_["lander"]), "orbitador": ("Orbitador no Falcon Heavy", ve_["orbitador"])}
    cv, cf = env["coifas"]["vulcan"], env["coifas"]["falcon"]
    leituras = {"reto": (cv["altura_m"], cv["raio_m"]), "menor": (cv["altura_m"], [cv["raio_m"][1], cv["raio_m"][1]] + list(cv["raio_m"][2:])), "falcon": (cf["altura_m"], cf["raio_m"])}
    combos = [("lander_4_5", "reto", "contorno reto"), ("lander_4_5", "menor", "Ø menor"), ("lander_4_65", "reto", "contorno reto"), ("lander_4_65", "menor", "Ø menor"), ("orbitador", "falcon", "keep-in")]
    adapt = []
    for k_, le, rot in combos:
        linha = {"veiculo": corpos[k_][0], "leitura": rot, "por_altura": []}
        r0, a0 = ec.folgas(corpos[k_][1], leituras[le])
        linha["sem_adaptador"] = {"radial_m": r0["folga_radial_m"], "axial_m": a0["folga_axial_m"]}
        for c in ad["casos"]:
            h = c["altura_m"]
            perf = ([z - h for z in leituras[le][0]], leituras[le][1])
            rr, aa = ec.folgas(corpos[k_][1], perf)
            linha["por_altura"].append({"nome": c["nome"], "altura_m": h, "radial_m": rr["folga_radial_m"], "axial_m": aa["folga_axial_m"], "corpo": rr["corpo"]})
        adapt.append(linha)

    out = nativo({"gerado_por": "tools/rota_a_dimensiona.py", "natureza": "dados para o portão; nada entra no CAD nem nas premissas", "alvo": {"diametro_m": d_alvo, "limite_com_deck_m": lim_deck[d_alvo], "limite_sem_deck_m": lim_ombro[d_alvo],
                  "por_diametro": [{"diametro_m": d, "limite_com_deck_m": lim_deck[d], "limite_sem_deck_m": lim_ombro[d]} for d in sorted(caso)], "circulo_44_m": saidas["44:1"], "circulo_164_m": saidas["164:1"], "parede_m": t_par},
                  "nucleo_cad": nucleo, "arranjo_msl": ra["arranjo_msl"], "isp_minimo": isp_minimo, "ressalva_analogos": ler("results/etapa7.2/rotas_mav.yaml")["rota_a_ressalva"].split(". ")[0],
                  "dimensionamento": {"tensao_admissivel_mpa": sigma, "ftu_mpa": ftu, "fty_mpa": fty, "fator_seguranca": fs, "fator_fonte": ra["fator_seguranca_pressao"]["fonte"], "fator_flambagem": fs_fl, "fator_flambagem_fonte": ra["fator_seguranca_flambagem"]["fonte"], "ec_mpa": ec_, "raio_interno_m": r_i, "t_p093_m": t_p093, "pressoes": pressoes,
                                      "nota_flambagem": fl["nota"], "vao_base_m": g0, "vao_fonte": ra["vao_purga_m"]["fonte"], "fator_base": k_b, "casos": casos, "massa_tanques_atual_kg": caso[d0]["massa_tanques_kg"], "fatores": ks, "vaos": gs, "geometrias": ra["geometrias_estagio_2"]},
                  "adaptador": {"casos": ad["casos"], "linhas": adapt, "ressalva_vulcan": ad["ressalva_vulcan"], "ressalva_falcon": ad["ressalva_falcon"], "p097_proposta": ad["p097_proposta"], "base_proposta": ad["base_proposta"]}})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "rota_a.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def compara_analogos(o):
    """Compara os Isp mínimos, por geometria, com a faixa dos análogos, lida da ressalva de results/etapa7.2/rotas_mav.yaml."""
    base, topo = (float(x) for x in re.search(r"de (\d+) a (\d+) s", o["ressalva_analogos"]).groups())
    frases = []
    for f, nome in o["dimensionamento"]["geometrias"].items():
        xs = [li["por_geometria"][f] for li in o["isp_minimo"]["linhas"]]
        dentro = sum(1 for x in xs if x is not None and base <= x <= topo)
        frases.append(f"{nome}: {dentro} de {len(xs)} linhas dentro da faixa")
    return "Na faixa de " + br(base, 0) + " a " + br(topo, 0) + " s: " + "; ".join(frases) + "."


def escreve_md(o):
    al, dm, im, nu, ad = o["alvo"], o["dimensionamento"], o["isp_minimo"], o["nucleo_cad"], o["adaptador"]
    md = ["# Portão do comprimento do MAV: rota A provisória (gerado por tools/rota_a_dimensiona.py)", "",
          "Dados para decisão do Fabio (ADR 0023). A rota A não está aplicada ao CAD nem às premissas. O que não tem fonte fica em varredura e está marcado NÃO VALIDADO.", "",
          "## 1. Alvo com deck", "", f"Com as 4 saídas de 44:1 ({br(al['circulo_44_m'])} m, com parede de {br(al['parede_m'], 2)} m de cada lado), o menor Ø da varredura é {br(al['diametro_m'], 2)} m: limite de {br(al['limite_com_deck_m'], 2)} m com deck; {br(al['limite_sem_deck_m'], 2)} m sem deck, que fica como limite otimista. Com 164:1 ({br(al['circulo_164_m'])} m), o Ø cresce e o limite cai.", "",
          "| Ø (m) | Limite com deck (m) | Limite sem deck (m) |", "| -: | -: | -: |"]
    md += [f"| {br(x['diametro_m'], 2)} | {br(x['limite_com_deck_m'], 2)} | {br(x['limite_sem_deck_m'], 2)} |" for x in al["por_diametro"]]
    md += ["", "## 2. O arranjo atual do CAD é viável? Comparação com o MSL e o Mars 2020", "",
           "**CAD atual:** núcleo do lander " + "; ".join(f"na forma {nome}, entre {br(n_['estacao_de_m'], 2)} e {br(n_['estacao_ate_m'], 2)} m do nariz, raio {br(n_['raio_m'], 2)} m, com face externa de raio {br(n_['raio_externo_na_frente_m'], 2)} m na frente dele: sobram {br(n_['folga_a_face_externa_m'], 2)} m" for nome, n_ in (("SRL-A", nu["srl_a"]), ("MSL/Mars 2020 (o alvo de 4,5 m)", nu["msl_m2020"]))) + f", com escudo de {br(nu['espessura_pica_m'], 3)} m. **Cabe na geometria, mas por construção:** o raio do núcleo é o da cápsula menos a folga interna (tools/cad_parametros.py), então essa sobra não é uma verificação independente.", "",
           "| Item | O que a fonte diz | Fonte |", "| :- | :- | :- |"]
    md += [f"| {x['item']} | {x['achado']} | {x['fonte']} |" for x in o["arranjo_msl"]]
    md += ["", "**O que dá para dizer:** no MSL, o que vai à superfície fica do lado do escudo, e o estágio de descida do lado da casca traseira, então ter o conjunto do lander à frente do ombro não contraria a ordem do MSL. **O que não dá:** confirmar a viabilidade. Não há cota interna nas fontes lidas, e o nosso arranjo é outro: o MAV deitado fica atrás do núcleo, e os tanques de descida atravessam a casca (results/etapa7.2b/folgas.md). Viabilidade funcional não conferida: abertura e separação do escudo, propulsão de descida e pernas.", "",
           "## 3. Isp mínimo do 44:1, com deck e folga de ao menos " + sg(im["alvo_folga_m"], 2) + " m", "",
           f"Comprimento máximo: {br(im['comprimento_max_m'])} m, em Ø {br(al['diametro_m'], 2)} m. MAV redimensionado para cada Isp, nos dois estágios.", "",
           "Colunas: a geometria do estágio 2 (seção 4), que é uma escolha do Fabio. " + "; ".join(f"**{f}**: {n}" for f, n in dm["geometrias"].items()) + ".", "",
           f"Limite otimista, sem tanques dimensionados: {br(im['limite_otimista_s'], 1)} s.", "",
           "| Vão (m) | Fator de flambagem (NÃO VALIDADO) | " + " | ".join(dm["geometrias"]) + " |", "| -: | -: |" + " -: |" * len(dm["geometrias"])]
    for li in im["linhas"]:
        md.append(f"| {br(li['vao_m'], 3)} | {br(li['fator'], 2)} | " + " | ".join(br(li["por_geometria"][f], 2) if li["por_geometria"][f] else "não fecha na faixa" for f in dm["geometrias"]) + " |")
    md += ["", f"Os valores de Isp conhecidos são só análogos (results/etapa7.2/rotas_mav.md). O Isp do 44:1 do R-4D-11 segue sem fonte. {o['ressalva_analogos']}. {compara_analogos(o)}", "",
           "**Fixada a geometria, estes valores são um piso quanto à massa.** O MAV redimensionado usa a fração estrutural fixa e não recebe a massa dos tanques da seção 4; se o inerte estourar, o MAV cresce e o Isp mínimo sobe. A geometria muda em que lado da faixa dos análogos o valor cai, e por isso a conclusão depende dela.", "",
           "## 4. Tanques aninhados dimensionados", "",
           f"Ti-6Al-4V recozido, base A: Ftu {br(dm['ftu_mpa'], 0)} MPa, Fty {br(dm['fty_mpa'], 0)} MPa ([F219]). Fator de {br(dm['fator_seguranca'], 1)}: {dm['fator_fonte']}. Tensão admissível: {br(dm['tensao_admissivel_mpa'], 0)} MPa. Na flambagem, fator de {br(dm['fator_flambagem'], 1)}: {dm['fator_flambagem_fonte']}; t varia com a raiz do fator. Raio interno {br(dm['raio_interno_m'], 3)} m. A P-093 usa {br(1e3 * dm['t_p093_m'], 1)} mm. **{dm['nota_flambagem']}.**", "",
           "**Pressão e espessura mínima (mm):**", "", "| Pressão | MPa | Cilindro | Cúpula normal | " + " | ".join(f"Cúpula invertida, fator {br(k, 2)}" for k in dm["fatores"]) + " | Fonte |", "| :- | -: | -: | -: |" + " -: |" * len(dm["fatores"]) + " :- |"]
    for n, p_ in dm["pressoes"].items():
        md.append(f"| {n} | {br(p_['mpa'], 2)} | {br(1e3 * p_['t_cilindro_m'], 2)} | {br(1e3 * p_['t_cupula_m'], 2)} | " + " | ".join(br(1e3 * p_["t_cupula_invertida_m"][str(k)], 2) for k in dm["fatores"]) + f" | {p_['fonte']} |")
    md += ["", f"**Comprimento e massa,** em Ø {br(al['diametro_m'], 2)} m, com o piso de entrada do motor, vão de {br(dm['vao_base_m'], 2)} m (NÃO VALIDADO: {dm['vao_fonte']}) e fator de flambagem {br(dm['fator_base'], 2)}. O estágio 1 soma ao limite o vão e as duas paredes da antepara. No estágio 2, o volume cabe numa esfera menor que o diâmetro interno: uma antepara do mesmo raio dessa esfera, com a borda no equador, não deixa volume para o segundo tanque, e por isso há quatro geometrias, sem fonte e NÃO VALIDADAS.", "",
           "| Isp (s) | Geometria do estágio 2 | Só 44:1 (m) | Limite otimista (m) | Real (m) | Redução no limite (m) | Redução real (m) | Sobra da redução | Folga, com deck (m) | Folga, sem deck (m) | Tanques (kg) |", "| -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
    for c in dm["casos"]:
        for f, x in c["por_geometria"].items():
            md.append(f"| {br(c['isp_s'], 0)} | {f} | {br(c['so_44_m'])} | {br(c['limite_otimista_m'])} | {br(x['real_m'])} | {br(c['reducao_limite_m'])} | {br(x['reducao_real_m'])} | {br(100 * x['fracao_que_sobra'], 0)} % | {sg(x['folga_deck_real_m'])} | {sg(x['folga_ombro_real_m'])} | {br(x['massa_tanques_kg'], 1)} |")
    md += ["", f"Massa dos tanques em série hoje: {br(dm['massa_tanques_atual_kg'], 1)} kg, na espessura da P-093. A massa do orçamento do MAV vem da fração estrutural, então esta conta não muda o GLOM; por isso o confronto abaixo.", "",
           "**Tanques contra o inerte, por estágio.** A sobra é o que resta no inerte para estrutura, pressurização e o resto. O motor é o de 164:1, porque o 44:1 não tem massa com fonte. O estágio 1 não depende da geometria.", "",
           "| Isp (s) | Estágio | Geometria | Inerte (kg) | Tanques (kg) | Parcela | Motores 164:1 (kg) | Sobra (kg) |", "| -: | -: | :- | -: | -: | -: | -: | -: |"]
    for c in dm["casos"]:
        p0 = next(iter(c["por_geometria"].values()))["por_estagio"][0]
        md.append(f"| {br(c['isp_s'], 0)} | 1 | todas | {br(p0['inerte_kg'], 1)} | {br(p0['tanques_kg'], 1)} | {br(100 * p0['parcela_do_inerte'], 0)} % | {br(p0['motores_164_kg'], 1)} | {sg(p0['sobra_kg'], 1)} |")
        for f, x in c["por_geometria"].items():
            e2 = x["por_estagio"][1]
            md.append(f"| {br(c['isp_s'], 0)} | 2 | {f} | {br(e2['inerte_kg'], 1)} | {br(e2['tanques_kg'], 1)} | {br(100 * e2['parcela_do_inerte'], 0)} % | {br(e2['motores_164_kg'], 1)} | {sg(e2['sobra_kg'], 1)} |")
    md += ["", "**As quatro geometrias do estágio 2.** " + "; ".join(f"**{f}**: {n}" for f, n in dm["geometrias"].items()) + ". As espessuras seguem as do raio interno, e nenhuma é um dimensionamento. Com recesso, o fundo do recesso não foi analisado. Em **antepara_assimetrica**, a calota fica quase plana, com o vão praticamente constante: a espessura de flambagem no raio da calota, na tabela, está fora do domínio da fórmula da casca esférica, uma calota tão rasa trabalha como placa, e a flexão de placa não foi calculada. O comprimento e a massa dessa coluna usam a espessura do raio interno, então são otimistas. Em **lente_mesmo_raio**, a antepara tem o raio da esfera e o canto vivo na borda não foi analisado.", "",
           "| Isp (s) | Tanque único (m) | recesso_hemisferio (m) | recesso_livre (m) | antepara_assimetrica (m) | lente_mesmo_raio (m) | Raio da calota, antepara (m) | Flambagem nesse raio, fora do domínio (mm) | Raio da esfera e raio da borda, lente (m) |", "| -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
    for c in dm["casos"]:
        ge = {f: x["por_estagio"][1]["geometria"] for f, x in c["por_geometria"].items()}
        md.append(f"| {br(c['isp_s'], 0)} | {br(c['por_geometria']['antepara_assimetrica']['por_estagio'][1]['tanque_unico_m'])} | {br(ge['recesso_hemisferio']['comprimento_m'])} | {br(ge['recesso_livre']['comprimento_m'])} | {br(ge['antepara_assimetrica']['comprimento_m'])} | {br(ge['lente_mesmo_raio']['comprimento_m'])} | {br(ge['antepara_assimetrica']['raio_calota_m'], 2)} | {br(1e3 * ge['antepara_assimetrica']['t_flambagem_no_raio_da_calota_m'], 1)} | {br(ge['lente_mesmo_raio']['raio_m'])} e {br(ge['lente_mesmo_raio']['raio_borda_m'])} |")
    md += ["", "**Sensibilidade do comprimento real (m) ao vão de purga:**", "", "| Isp (s) | Geometria | " + " | ".join(f"{br(g, 3)} m" for g in dm["vaos"]) + " |", "| -: | :- |" + " -: |" * len(dm["vaos"])]
    for c in dm["casos"]:
        for f, x in c["por_geometria"].items():
            md.append(f"| {br(c['isp_s'], 0)} | {f} | " + " | ".join(br(x["por_vao"][str(g)]) for g in dm["vaos"]) + " |")
    md += ["", "**Não dimensionado:** cargas de lançamento e de subida, fadiga e fratura, soldas, espessura mínima de fabricação, e o vão como peça. A fonte tem cúpula de excentricidade 0,707 em tanques de alta pressão ([F46] PDF p. 9), que encurtaria mais; aqui seguem os hemisférios da P-085.", "",
           "## 5. P-097: folgas nas coifas com a altura do adaptador", "",
           f"Ressalvas: {ad['ressalva_vulcan']}. {ad['ressalva_falcon']}.", "",
           "| Adaptador | Altura (m) | Massa (kg) | Fonte |", "| :- | -: | -: | :- |"]
    md += [f"| {c['nome']} | {br(c['altura_m'], 3)} | {br(c['massa_kg'], 1)} | {c['fonte']} |" for c in ad["casos"]]
    cab = [c["nome"] for c in ad["casos"]]
    md += ["", "Folga radial mínima (m):", "", "| Configuração | Leitura | Sem adaptador | " + " | ".join(f"{br(c['altura_m'], 3)} m" for c in ad["casos"]) + " |", "| :- | :- | -: |" + " -: |" * len(cab)]
    for li in ad["linhas"]:
        md.append(f"| {li['veiculo']} | {li['leitura']} | {sg(li['sem_adaptador']['radial_m'])} | " + " | ".join(sg(x["radial_m"]) for x in li["por_altura"]) + " |")
    md += ["", "Folga axial mínima (m):", "", "| Configuração | Leitura | Sem adaptador | " + " | ".join(f"{br(c['altura_m'], 3)} m" for c in ad["casos"]) + " |", "| :- | :- | -: |" + " -: |" * len(cab)]
    for li in ad["linhas"]:
        md.append(f"| {li['veiculo']} | {li['leitura']} | {sg(li['sem_adaptador']['axial_m'])} | " + " | ".join(sg(x["axial_m"]) for x in li["por_altura"]) + " |")
    md += ["", f"**P-097 reformulada, para nova decisão:** {ad['p097_proposta']}"]
    (SAIDA / "rota_a.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
