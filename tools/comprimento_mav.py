"""Portão da Etapa 7.2: o que define o comprimento do MAV (investigação; não muda premissa nem arquitetura).

(a) O que as fontes dizem da divisão do comprimento do MAV do MSR, com a leitura proporcional da figura.
(b) Isp, massa e empuxo do R-4D-11 de expansão 44:1: o que foi achado e onde se procurou.
(c) De onde vêm os 5,772 km/s; comparação com Bowles; trade da órbita de encontro pelas funções do estudo: mesmas massas de
    plataforma, MAV redimensionado, Δv extra e massa do orbitador. O comprimento usa os mesmos segmentos da Etapa 7.1.
(d) O MAV em pé, de results/etapa7.2/mav_arranjo.yaml.
Saída: results/etapa7.2/comprimento_mav.yaml e .md

Uso: python tools/comprimento_mav.py
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

import envelope_arranjo as ea  # noqa: E402
from orbital import lancamento as lc  # noqa: E402
from orbital import manobras as mn  # noqa: E402
from orbital import motores as om  # noqa: E402
from orbital import superficie as sf  # noqa: E402
from orbital import veiculos as ve  # noqa: E402
from orbital.config import ler, nativo, parametros, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"
POL = 0.0254   # [F112] Apêndice B.8, PDF p. 62: polegada em metros


def comprimento(d, est, nt, cad, aninhado=False):
    """Comprimento do MAV (m) com os segmentos da Etapa 7.1; com `aninhado`, oxidante e combustível de cada estágio dividem
    os tampos (tanque único com o volume somado, sem o volume da antepara: limite otimista)."""
    pr, t = cad["propelentes"], v(cad["mav"]["espessura_parede_m"])
    arg = (v(pr["razao_mistura_r4d11"]), v(pr["densidade_oxidante_kg_m3"]), v(pr["densidade_mmh_kg_m3"]), v(pr["fracao_ullage"]))
    segs = ea.segmentos_mav(d, est, nt, t, *arg)
    L = sum(s[1] for s in segs)
    if aninhado:
        fora = sum(s[1] for s in segs if s[2] == "estrutura" or s[2] == "carga")
        L = fora
        for e in est:
            vol = ea.volumes(e["propelente_kg"], *arg)
            L += ea.tanque_cilindrico(vol["tanque_oxidante_m3"] + vol["tanque_combustivel_m3"], d - 2 * t) + 2 * t
    return L


def main():
    cad, ma, arq = ler("config/cad.yaml"), ler("results/etapa7.2/mav_arranjo.yaml"), ler("results/etapa2.5/arquitetura.yaml")
    cm = cad["comprimento_mav"]
    scfg, dcfg, mcfg, po = ler("config/superficie.yaml"), ler("config/dimensionamento.yaml"), ler("config/mav_propulsao.yaml"), ler("config/parametros_orbitais.yaml")
    lcfg = ler("config/lancadores.yaml")
    p = parametros()
    R, mu, um = v(po["raio_marte_km"]), p.mu_marte, p.orbitas_marte["eliptica_alta"]
    nt = {k: v(x) for k, x in cad["mav"]["comprimento_nao_tanque_m"].items()}
    p086 = sum(nt.values())
    d0 = v(cad["mav"]["diametro_opcoes_m"][cad["escolha"]["mav_diametro"]])
    caso = {c["diametro_m"]: c for c in ma["casos"]}
    ombro = {d: {k: next(e for e in c["formas"][k] if e["estacao"] == "ombro") for k in ("msl_m2020", "srl_a")} for d, c in caso.items()}

    def linha(rotulo, L, d=d0, grupo="", **extra):
        """Folga do MAV deitado com a base no ombro: a da varredura, corrigida pelo comprimento (metade de cada lado)."""
        base = caso[d]["comprimento_m"]
        o = ombro[d]
        return {"alavanca": rotulo, "grupo": grupo, "diametro_m": d, "comprimento_m": L, "delta_comprimento_m": L - caso[d0]["comprimento_m"],
                "deitado_4_5_m": o["msl_m2020"]["deitado_folga_m"] + (base - L) / 2, "deitado_4_65_m": o["srl_a"]["deitado_folga_m"] + (base - L) / 2,
                "em_pe_4_5_m": o["msl_m2020"]["em_pe_comprimento_disponivel_m"] - L, "em_pe_4_65_m": o["srl_a"]["em_pe_comprimento_disponivel_m"] - L, **extra}

    # ---------------- (a) figura do MSR
    fg = cm["figura_msr"]
    lim = v(cad["mav"]["comprimento_max_src_m"])
    fig = [{"item": t["item"], "fracao": t["px"] / fg["pixels_total"], "comprimento_m": lim * t["px"] / fg["pixels_total"], "equivale_a": t["equivale_a"]} for t in fg["trechos_px"]]
    nao_prop = sum(x["comprimento_m"] for x in fig if x["equivale_a"])
    prop_msr = sum(x["comprimento_m"] for x in fig if not x["equivale_a"])
    tanques_nosso = caso[d0]["comprimento_m"] - p086

    # ---------------- (c) Δv
    v_eq = 2 * np.pi * R / v(scfg["marte"]["periodo_rotacao_s"])
    inc = v(scfg["sitio_e_encontro"]["inclinacao_encontro_graus"])
    lat = v(scfg["sitio_e_encontro"]["latitude_sitio_graus"])
    dv100 = v(scfg["subida"]["dv_100x100_km_s"])
    margem = v(dcfg["margem_dv"])
    pl = ler("results/etapa2.3/plataformas.yaml")["orbita_encontro"]
    hp0, ha0 = pl["periapse_alt_km"], pl["apoapse_regra_5pct_km"]
    alt = cm["altitudes_tabela_bowles_km"]
    amostra = cm["amostragem"]
    r100 = R + alt["periapse"]
    transf = sf.dv_transferencia_de_100(mu, r100, R + hp0, R + ha0)
    deficit = v_eq * (1 - np.cos(np.radians(inc)))
    sem_margem = dv100 + transf + deficit
    transf_500 = sf.dv_transferencia_de_100(mu, r100, r100, R + alt["apoapse"])
    bw = cm["bowles"]
    origem_dv = {"dv_100x100_m_s": 1e3 * dv100, "transferencia_m_s": 1e3 * transf, "deficit_rotacao_m_s": 1e3 * deficit, "sem_margem_m_s": 1e3 * sem_margem, "margem_fracao": margem,
                 "margem_m_s": 1e3 * margem * sem_margem, "com_margem_m_s": 1e3 * (1 + margem) * sem_margem, "orbita_km": [hp0, ha0], "inclinacao_graus": inc,
                 "acima_da_velocidade_circular_m_s": 1e3 * dv100 - bw["velocidade_100x100_m_s"], "modelo_100x500_m_s": 1e3 * (dv100 + transf_500), "bowles_tabela_100x500_m_s": bw["dv_100x500_m_s"],
                 "bowles_m_s": v(bw["dv_m_s"]), "diferenca_para_bowles_m_s": 1e3 * (1 + margem) * sem_margem - v(bw["dv_m_s"])}

    # ---------------- (c) trade da órbita: as próprias funções do estudo
    ms = ler("results/etapa1.3/missoes.yaml")
    cand = {c["id"]: c for c in ms["candidatas"]}
    ref = ler("config/missao_referencia.yaml")["missao_referencia"]["id"]
    janelas = [cand[w["missao"]] for w in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()]
    c3l = {"missao_A": cand[ref]["c3l_partida_marte_km2_s2"], "regra_iii": max(x["c3l_partida_marte_km2_s2"] for x in janelas)}
    tmav = om.catalogo()["R-4D-11"]["empuxo_n"]
    g = ler("results/etapa3.1/queima_finita.yaml")["g_marte_m_s2"]
    def orbitador(rp, ra):
        """(massa injetada, margem no Falcon Heavy) pela regra (iii); None se um estágio do orbitador não fecha."""
        try:
            m = ve.veiculos(orbita=(rp, ra))[0]["orbitador_regra_iii"]["injetada_kg"]
        except ValueError:
            return None, None
        return m, lc.pior_margem_a("Falcon Heavy (descartável)", m, janelas, lcfg, lc.adaptador_p097()[0])[0]

    def ponto(hp, ha, fonte="", eh_base=False, rotulo="", diverge=False):
        rp, ra = R + hp, R + ha
        lan = ve.lander(rp, ra, detalhe=True)
        est = lan["mav_estagios"]
        descer = mn.dv_transferencia_coaxial(mu, um.rp, um.ra, rp, ra)
        extra = {k: ve.dv_extra_orbitador(mu, um, rp, ra, c3l[k], descer) for k in c3l}
        vinf = np.sqrt(c3l["regra_iii"])
        tei_1 = float(mn.dv_hiperbole_orbita(mu, vinf, um.rp, um.ra))
        tei_a = float(mn.dv_hiperbole_orbita(mu, vinf, rp, ra))
        voltar = mn.dv_transferencia_coaxial(mu, rp, ra, um.rp, um.ra) + tei_1
        # perto do limite em que o estágio deixa de fechar, a massa diverge e não significa nada: não é gravada
        m_o, mg_o = (None, None) if diverge else orbitador(rp, ra)
        return {"periapse_km": hp, "apoapse_km": ha, "fonte": fonte, "base": eh_base, "rotulo": rotulo, "diverge": diverge,
                "dv_mav_com_margem_m_s": 1e3 * (1 + margem) * lan["dv_subida_mav_km_s"], "glom_kg": est[0]["massa_inicial_kg"],
                "propelente_mav_kg": sum(e["propelente_kg"] for e in est), "comprimento_m": comprimento(d0, est, nt, cad),
                "comprimento_aninhado_m": comprimento(d0, est, nt, cad, aninhado=True),
                "empuxo_peso_4_motores": 4 * tmav / (est[0]["massa_inicial_kg"] * g), "empuxo_peso_2_motores": 2 * tmav / (est[0]["massa_inicial_kg"] * g),
                "descer_de_1_sol_m_s": 1e3 * descer, "partir_direto_extra_m_s": 1e3 * (tei_a - tei_1), "voltar_a_1_sol_extra_m_s": 1e3 * (voltar - tei_1),
                "extra_orbitador_regra_iii_m_s": 1e3 * extra["regra_iii"], "extra_orbitador_missao_a_m_s": 1e3 * extra["missao_A"],
                "orbitador_injetado_kg": m_o, "lander_injetado_kg": lan["injetada_kg"], "margem_falcon_heavy": mg_o,
                "margem_vulcan_vc4": lc.pior_margem_a("Vulcan VC4", lan["injetada_kg"], janelas, lcfg, lc.adaptador_p097()[0])[0],
                "margem_vulcan_vc6_orbitador": lc.pior_margem_a("Vulcan VC6", m_o, janelas, lcfg, lc.adaptador_p097()[0])[0] if m_o else None}

    def bissecao(cumpre, lo, hi, passos=amostra["passos_bissecao"]):
        """Menor apoapse (km) em [lo, hi] que cumpre a condição, com `hi` cumprindo; arredondado para cima em km."""
        for _ in range(passos):
            mid = (lo + hi) / 2
            lo, hi = (lo, mid) if cumpre(mid) else (mid, hi)
        return float(np.ceil(hi))
    h_baixa = v(scfg["sitio_e_encontro"]["orbita_baixa_alt_km"])
    def fh_ok(ha):
        mg = orbitador(R + hp0, R + ha)[1]
        return mg is not None and mg >= 0
    limite_fh = bissecao(fh_ok, h_baixa, float(ha0))
    limite_viavel = bissecao(lambda ha: orbitador(R + hp0, R + ha)[0] is not None, h_baixa, float(ha0))
    orbitas = [ponto(hp0, ha0, eh_base=True)] + [ponto(o_["rp"], o_["ra"], o_.get("fonte", "")) for o_ in cm["orbitas_amostra"]]
    orbitas.append(ponto(hp0, limite_fh, rotulo="margem zero no Falcon Heavy"))
    orbitas.append(ponto(hp0, limite_viavel, rotulo="limite em que o orbitador deixa de fechar", diverge=True))
    orbitas.sort(key=lambda x: -x["apoapse_km"])
    base = orbitas[0]

    # ---------------- (b) 44:1: sensibilidade do Isp pelos análogos, com o MAV redimensionado
    est0 = arq["lander"]["mav"]["estagios"]
    rd = cad["r4d11_variantes"]
    fr = v(rd["a_frente_da_flange_pol"])
    motor_m = {k: (rd[k]["flange_a_saida_pol"] + fr) * POL for k in ("44:1", "164:1", "300:1")}
    op = ler("results/etapa2.2/mav_propulsao.yaml")["melhor_opcao"]
    isps = sorted({a["isp_s"] for a in cm["variante_44_1"]["analogos_isp"]})
    nt44 = {**nt, "motores_estagio_1": motor_m["44:1"], "motor_estagio_2": motor_m["44:1"]}
    nt164 = {**nt, "motores_estagio_1": motor_m["164:1"], "motor_estagio_2": motor_m["164:1"]}
    sens44 = []
    for isp in isps:
        m2 = copy.deepcopy(mcfg)
        m2["opcoes"][op]["isp_s"] = [isp, isp]
        vei = ve.veiculos(detalhe=True, mcfg=m2)[0]["lander"]
        sens44.append({"isp_s": isp, "glom_kg": vei["mav_estagios"][0]["massa_inicial_kg"], "comprimento_m": comprimento(d0, vei["mav_estagios"], nt44, cad),
                       "comprimento_sem_mudar_p086_m": comprimento(d0, vei["mav_estagios"], nt, cad)})

    # ---------------- tabela final
    L0 = caso[d0]["comprimento_m"]
    lin = [linha(f"Base: Ø {d0:g} m, P-086 de {p086:g} m, órbita de base".replace(".", ","), L0, grupo="base")]
    lin.append(linha("P-086 pelo motor real 164:1 nos dois estágios ([F228])", comprimento(d0, est0, nt164, cad), grupo="p086"))
    lin.append(linha("P-086 pela leitura da figura do MSR (NÃO VALIDADO)", L0 + nao_prop - p086, grupo="p086"))
    lin.append(linha(f"Cada {amostra['exemplo_p086_m']:g} m a menos na P-086, por qualquer meio, inclusive bocal aninhado (NÃO VALIDADO)".replace(".", ","), L0 - amostra["exemplo_p086_m"], grupo="p086", exemplo=True))
    lin.append(linha(f"R-4D-11 44:1 nos dois estágios, P-086 pelo motor, Isp do 164:1 mantido (NÃO VALIDADO)", comprimento(d0, est0, nt44, cad), grupo="variante"))
    lin.append(linha(f"Idem, com o pior análogo ({isps[0]:g} s; NÃO VALIDADO)", sens44[0]["comprimento_m"], grupo="variante"))
    lin.append(linha("Tanques aninhados, antepara comum (limite otimista)", comprimento(d0, est0, nt, cad, aninhado=True), grupo="tanques"))
    for d in amostra["diametros_m"]:
        lin.append(linha(f"Ø {d:g} m".replace(".", ","), caso[d]["comprimento_m"], d=d, grupo="diametro"))
    for o in orbitas[1:]:
        extra_ = "" if not o["rotulo"] else f" ({o['rotulo']})"
        lin.append(linha(f"Órbita {o['periapse_km']:.0f} × {o['apoapse_km']:.0f} km{extra_}", o["comprimento_m"], grupo="orbita", extra_orbitador_m_s=o["extra_orbitador_regra_iii_m_s"] - base["extra_orbitador_regra_iii_m_s"], orbitador_fecha=o["orbitador_injetado_kg"] is not None or o["diverge"], diverge=o["diverge"], margem_falcon_heavy=o["margem_falcon_heavy"]))
    fh = next(o for o in orbitas if o["rotulo"].startswith("margem zero"))
    lin.append(linha("Órbita de margem zero + tanques aninhados (limite otimista)", fh["comprimento_aninhado_m"], grupo="combinada", extra_orbitador_m_s=fh["extra_orbitador_regra_iii_m_s"] - base["extra_orbitador_regra_iii_m_s"], orbitador_fecha=True, margem_falcon_heavy=fh["margem_falcon_heavy"]))
    # teste de resolução: dobrar cada parâmetro de amostragem e olhar as conclusões, nas casas mostradas
    def perfil(k):
        return [float(x) for x in cad["capsulas"][k]["x_m"]], [float(x) for x in cad["capsulas"][k]["r_m"]]

    def folga_em(d, forma):
        xs, rs = perfil(forma)
        x0 = xs[int(np.argmax(rs))]
        return float(np.interp(x0 + d, xs, rs)) - v(cad["aeroshell"]["folga_interna_m"]) - comprimento(d, est0, nt, cad) / 2
    diam = [float(x) for x in cad["mav_alternativas"]["diametros_m"]]
    finos = sorted(set(diam + [(a + b) / 2 for a, b in zip(diam, diam[1:])]))
    res = {}
    for forma in ("msl_m2020", "srl_a"):
        g1, g2 = max(diam, key=lambda d: folga_em(d, forma)), max(finos, key=lambda d: folga_em(d, forma))
        res[forma] = {"melhor_d_grade_m": g1, "melhor_folga_grade_m": folga_em(g1, forma), "melhor_d_fina_m": g2, "melhor_folga_fina_m": folga_em(g2, forma)}
    fino_passos = amostra["passos_bissecao"] * 2
    lim_fh2 = bissecao(fh_ok, h_baixa, float(ha0), passos=fino_passos)
    lim_v2 = bissecao(lambda ha: orbitador(R + hp0, R + ha)[0] is not None, h_baixa, float(ha0), passos=fino_passos)
    ras = sorted(x["apoapse_km"] for x in orbitas if x["periapse_km"] == hp0)
    meios = [math.sqrt(a * b) for a, b in zip(ras, ras[1:])]
    pts = [ponto(hp0, h) for h in meios]
    ref_l = {x["apoapse_km"]: x["comprimento_m"] for x in orbitas if x["periapse_km"] == hp0}
    todos = sorted(list(ref_l.items()) + [(x["apoapse_km"], x["comprimento_m"]) for x in pts])
    ex1, ex2 = amostra["exemplo_p086_m"], amostra["exemplo_p086_m"] / 2
    resolucao = {"passos_bissecao": {"passos": amostra["passos_bissecao"], "dobrado": fino_passos, "limite_fh_km": limite_fh, "limite_fh_dobrado_km": lim_fh2, "limite_fecha_km": limite_viavel, "limite_fecha_dobrado_km": lim_v2},
                 "orbitas_amostra": {"pontos_novos_km": meios, "comprimento_monotono": all(a[1] < b[1] for a, b in zip(todos, todos[1:])), "comprimentos_novos_m": [x["comprimento_m"] for x in pts]},
                 "diametros_m": {"pontos": len(diam), "dobrado": len(finos), "por_forma": res},
                 "exemplo_p086_m": {"valor": ex1, "metade": ex2, "folga_por_metro_valor": (linha("", L0 - ex1)["deitado_4_5_m"] - lin[0]["deitado_4_5_m"]) / ex1, "folga_por_metro_metade": (linha("", L0 - ex2)["deitado_4_5_m"] - lin[0]["deitado_4_5_m"]) / ex2}}
    # o que cada aeroshell pede, e a estação mais favorável
    ped = {k: {"deitado_comprimento_max_m": L0 + 2 * ombro[d0][k]["deitado_folga_m"], "em_pe_comprimento_max_m": ombro[d0][k]["em_pe_comprimento_disponivel_m"]} for k in ("msl_m2020", "srl_a")}
    out = nativo({"gerado_por": "tools/comprimento_mav.py", "natureza": "investigação para o portão; não muda premissa nem arquitetura", "p086_m": p086, "p086_itens_m": nt, "diametro_m": d0, "comprimento_base_m": L0,
                  "tanques_nosso_m": tanques_nosso, "figura_msr": {"fonte": fg["fonte"], "limite_m": lim, "diametro_m": v(cad["mav"]["diametro_opcoes_m"]["src_2022"]), "trechos": fig, "nao_propelente_m": nao_prop, "motores_solidos_m": prop_msr}, "fontes_p086": cm["fontes_p086"],
                  "variante_44_1": {"motor_44_1_m": motor_m["44:1"], "motor_164_1_m": motor_m["164:1"], "analogos": cm["variante_44_1"]["analogos_isp"], "onde_procurou": cm["variante_44_1"]["onde_procurou"], "sensibilidade": sens44},
                  "origem_dv": origem_dv, "aerofrenagem": {"walk_out_m_s": 1e3 * v(scfg["aerofrenagem"]["dv_saida_aerofrenagem_km_s"]), "dias": v(scfg["aerofrenagem"]["duracao_dias"])}, "limites_apoapse_km": {"margem_zero_falcon_heavy": limite_fh, "orbitador_fecha": limite_viavel}, "bowles": {k: bw[k] for k in ("dv_m_s", "orbita_tabela", "perdas")}, "orbitas": orbitas,
                  "em_pe_na_varredura": [{"diametro_m": d, "em_pe_4_5_m": ombro[d]["msl_m2020"]["em_pe_folga_m"], "em_pe_4_65_m": ombro[d]["srl_a"]["em_pe_folga_m"], "disponivel_4_5_m": ombro[d]["msl_m2020"]["em_pe_comprimento_disponivel_m"], "disponivel_4_65_m": ombro[d]["srl_a"]["em_pe_comprimento_disponivel_m"]} for d in (d0, 0.60, 0.69)],
                  "comprimento_maximo": ped, "alavancas": lin, "resolucao_amostragem": resolucao})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "comprimento_mav.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def br(x, n=3):
    return f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def sg(x, n=3):
    return f"{round(x, n) + 0.0:+,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def escreve_md(o):
    od, fm, va = o["origem_dv"], o["figura_msr"], o["variante_44_1"]
    b = o["orbitas"][0]
    md = ["# Portão da 7.2: o que define o comprimento do MAV (gerado por tools/comprimento_mav.py)", "",
          "Investigação. Nenhuma premissa muda, a arquitetura não muda, e a decisão é do Fabio. O que é leitura de figura ou análogo está marcado NÃO VALIDADO.", "",
          "## (a) P-086: o que as fontes dizem do MAV do MSR", "", "| Item | O que foi achado | Fonte |", "| :- | :- | :- |"]
    md += [f"| {r['item']} | {r['achado']} | {r['fonte']} |" for r in o["fontes_p086"]]
    md += ["", f"**Não há fonte primária com a divisão por elemento.** A P-086 ({br(o['p086_m'], 2)} m: " + ", ".join(f"{k} {br(x, 2)}" for k, x in o["p086_itens_m"].items()) + ") continua sem fonte.", "",
           f"**Leitura proporcional da figura (NÃO VALIDADO):** {fm['fonte']}. A figura não declara escala; os trechos abaixo escalam a altura pelo limite de {br(fm['limite_m'], 2)} m de [F35], que é um máximo. Motor sólido, Ø {br(fm['diametro_m'], 2)} m: outro veículo.", "",
           "| Trecho | Fração da altura | Comprimento (m) |", "| :- | -: | -: |"]
    md += [f"| {x['item']} | {br(100 * x['fracao'], 1)} % | {br(x['comprimento_m'], 2)} |" for x in fm["trechos"]]
    md += ["", f"**O que a leitura permite dizer:** o que fica fora do corpo dos motores no MSR (carga, interestágio com o bocal aninhado e aviônica, TVC e bocal do 1º estágio) soma cerca de {br(fm['nao_propelente_m'], 2)} m, da mesma ordem da P-086. A diferença de comprimento entre os dois veículos está sobretudo na parte com propelente: cerca de {br(fm['motores_solidos_m'], 2)} m de motores sólidos no MSR, contra {br(o['tanques_nosso_m'], 2)} m de tanques no nosso. **O que não permite:** validar a P-086, porque os elementos não são equivalentes.", "",
           "## (b) R-4D-11 44:1", "",
           f"**Não achado:** Isp, massa ou empuxo próprios do R-4D-11 44:1 em fonte primária. O comprimento sai do desenho de [F228]: {br(va['motor_44_1_m'])} m, contra {br(va['motor_164_1_m'])} m do 164:1.", "",
           "**Onde se procurou:**"]
    md += [f"- {x}" for x in va["onde_procurou"]]
    md += ["", "**Análogos da mesma classe e expansão (NÃO VALIDADO: não são o R-4D-11):**", "", "| Motor | Isp (s) | Fonte |", "| :- | -: | :- |"]
    md += [f"| {a['nome']} | {br(a['isp_s'], 1)} | {a['fonte']} |" for a in va["analogos"]]
    md += ["", "Sensibilidade, com o MAV redimensionado para o mesmo Isp nos dois estágios e o comprimento do motor 44:1 nos dois:", "", "| Isp (s) | GLOM (kg) | Comprimento (m) | Sem mudar a P-086 (m) |", "| -: | -: | -: | -: |"]
    md += [f"| {br(s['isp_s'], 1)} | {br(s['glom_kg'], 1)} | {br(s['comprimento_m'])} | {br(s['comprimento_sem_mudar_p086_m'])} |" for s in va["sensibilidade"]]
    md += ["", "Massa do 44:1 sem fonte: fica a do catálogo.", "",
           f"## (c) De onde vêm os {br(od['com_margem_m_s'], 0)} m/s", "", "| Parcela | m/s | Origem |", "| :- | -: | :- |",
           f"| Subida a 100 × 100 km | {br(od['dv_100x100_m_s'], 1)} | [F37] Tab. 1, p. 17; {br(od['acima_da_velocidade_circular_m_s'], 1)} m/s acima da velocidade circular da mesma linha: inclui a subida a 100 km e as perdas, já líquidas do ganho de rotação, porque o caso sai do equador rumo leste |",
           f"| Transferência até {br(od['orbita_km'][0], 0)} × {br(od['orbita_km'][1], 0)} km | {br(od['transferencia_m_s'], 1)} | órbita do ADR 0005 (regra dos 5 %), coaxial ideal |",
           f"| Rotação perdida a {br(od['inclinacao_graus'], 1)}° | {br(od['deficit_rotacao_m_s'], 1)} | inclinação de [F35] p. 3, v_eq·(1 − cos i) |",
           f"| Soma sem margem | {br(od['sem_margem_m_s'], 1)} | |",
           f"| Margem de {br(100 * od['margem_fracao'], 0)} % | {br(od['margem_m_s'], 1)} | P-014 |",
           f"| **Total** | **{br(od['com_margem_m_s'], 1)}** | results/etapa2.5/arquitetura.yaml |", "",
           f"**Bowles:** {o['bowles']['dv_m_s']['valor']:g} m/s em órbita baixa ({o['bowles']['dv_m_s']['fonte']}). {o['bowles']['orbita_tabela']['fonte']}. O modelo do estudo dá {br(od['modelo_100x500_m_s'], 1)} m/s para 100 × 500 km, sem rotação nem margem, contra {br(od['bowles_tabela_100x500_m_s'], 1)} da tabela. "
           f"Não conferido se o valor de Bowles tem margem. **A diferença de {br(od['diferenca_para_bowles_m_s'], 0)} m/s é principalmente a órbita-alvo e a margem**: as duas partem da mesma linha de 100 × 100 km.", "",
           "### Trade da órbita de encontro", "",
           "Cada linha roda `veiculos` do estudo com a órbita dada. O MAV é redimensionado, com a mesma carga e a mesma plataforma. Orbitador pela regra (iii). Descer vale de 1 sol até a órbita de encontro; \"voltar\" é o custo extra de voltar a 1 sol antes de partir para a Terra; \"direto\" é partir da órbita de encontro. O estudo soma o descer ao menor dos dois.", "",
           "| Órbita (km) | Δv do MAV (m/s) | GLOM (kg) | Comprimento (m) | Empuxo/peso, 4 e 2 motores | Descer (m/s) | Direto, extra (m/s) | Voltar, extra (m/s) | Extra do orbitador (m/s) | Orbitador (kg) | Margem no Falcon Heavy | Lander (kg) | Margem no Vulcan VC4 |", "| :- | -: | -: | -: | :- | -: | -: | -: | -: | -: | -: | -: | -: |"]
    for x in o["orbitas"]:
        md.append(f"| {br(x['periapse_km'], 0)} × {br(x['apoapse_km'], 0)}{' (base)' if x['base'] else ''}{' (' + x['rotulo'] + ')' if x['rotulo'] else ''} | {br(x['dv_mav_com_margem_m_s'], 0)} | {br(x['glom_kg'], 1)} | {br(x['comprimento_m'])} | {br(x['empuxo_peso_4_motores'], 2)} e {br(x['empuxo_peso_2_motores'], 2)} | {br(x['descer_de_1_sol_m_s'], 0)} | {sg(x['partir_direto_extra_m_s'], 0)} | {sg(x['voltar_a_1_sol_extra_m_s'], 0)} | {br(x['extra_orbitador_regra_iii_m_s'], 0)} | {'diverge' if x['diverge'] else (br(x['orbitador_injetado_kg'], 0) if x['orbitador_injetado_kg'] else 'não fecha')} | {sg(100 * x['margem_falcon_heavy'], 1) + ' %' if x['margem_falcon_heavy'] is not None else '—'} | {br(x['lander_injetado_kg'], 0)} | {sg(100 * x['margem_vulcan_vc4'], 1)} % |")
    md += ["", f"**Limites, com periapse de {br(o['orbitas'][0]['periapse_km'], 0)} km:** o orbitador químico com um estágio de retorno deixa de fechar em {br(o['limites_apoapse_km']['orbitador_fecha'], 0)} km de apoapse: abaixo disso, o Δv passa do que o estágio permite, e perto desse limite a massa diverge, então ele é só matemático. A margem no Falcon Heavy zera em {br(o['limites_apoapse_km']['margem_zero_falcon_heavy'], 0)} km. "
           f"O Δv extra acima não depende do veículo fechar. O Vulcan VC6, a alternativa do orbitador no ADR 0008, parte de {sg(100 * o['orbitas'][0]['margem_vulcan_vc6_orbitador'], 1)} % na órbita de base e zera bem antes.", "",
           f"**Não calculado:** aerofrenagem na descida (P-020): tiraria só o \"descer\", cerca de metade do extra, somando {br(o['aerofrenagem']['walk_out_m_s'], 0)} m/s de saída e {br(o['aerofrenagem']['dias'], 0)} dias, em valores de fonte para outra órbita; comunicação e relé, janela de encontro, sensores e o que muda na captura. A plataforma do orbitador não foi reiterada, e o MAV mais leve não mudou os motores.", "",
           "## (d) O MAV em pé", "",
           "**Sim, foi calculado:** results/etapa7.2/mav_arranjo.md tem o caso em pé, em todas as estações. Com a base no ombro, a mais favorável:", "",
           "| Ø (m) | Disponível 4,5 m (m) | Folga em pé 4,5 m | Disponível 4,65 m (m) | Folga em pé 4,65 m |", "| -: | -: | -: | -: | -: |"]
    md += [f"| {br(e['diametro_m'], 2)} | {br(e['disponivel_4_5_m'], 2)} | {sg(e['em_pe_4_5_m'], 2)} | {br(e['disponivel_4_65_m'], 2)} | {sg(e['em_pe_4_65_m'], 2)} |" for e in o["em_pe_na_varredura"]]
    md += ["", "## Tabela final: o que cada alavanca faz", "",
           "Folga em m, com a base no ombro, a estação mais favorável; positivo = cabe. Nas outras estações ela é menor (results/etapa7.2/mav_arranjo.md). A folga interna da P-087 já está descontada. A interferência dos bocais do estágio 1 (results/etapa7.2/bocais_alternativas.md) continua em todas as linhas com 164:1 até Ø " + br(o["diametro_m"], 2) + " m e no diâmetro intermediário; o maior diâmetro da tabela só contém as saídas sem parede, e a linha de 44:1 as contém. \"P-086 pelo motor\" supõe nada além do motor: sem estrutura de empuxo e sem encaixe no tampo.", "",
           "| Alavanca | Ø (m) | Comprimento (m) | Variação (m) | Deitado 4,5 m | Deitado 4,65 m | Em pé 4,5 m | Em pé 4,65 m | Extra do orbitador sobre a base (m/s) |", "| :- | -: | -: | -: | -: | -: | -: | -: | -: |"]
    for li in o["alavancas"]:
        ex = sg(li["extra_orbitador_m_s"], 0) if "extra_orbitador_m_s" in li else "—"
        if "orbitador_fecha" in li:
            ex += " (massa diverge)" if li.get("diverge") else ("" if li["orbitador_fecha"] else " (orbitador não fecha)")
        md.append(f"| {li['alavanca']} | {br(li['diametro_m'], 2)} | {br(li['comprimento_m'])} | {sg(li['delta_comprimento_m'])} | {sg(li['deitado_4_5_m'])} | {sg(li['deitado_4_65_m'])} | {sg(li['em_pe_4_5_m'])} | {sg(li['em_pe_4_65_m'])} | {ex} |")
    cm_ = o["comprimento_maximo"]
    md += ["", f"**Comprimento máximo com Ø {br(o['diametro_m'], 2)} m:** deitado, {br(cm_['msl_m2020']['deitado_comprimento_max_m'], 2)} m no 4,5 m e {br(cm_['srl_a']['deitado_comprimento_max_m'], 2)} m no 4,65 m; em pé, {br(cm_['msl_m2020']['em_pe_comprimento_max_m'], 2)} m e {br(cm_['srl_a']['em_pe_comprimento_max_m'], 2)} m.", "",
           "## Resolução da amostragem", "",
           "Teste pedido pelo Fabio para aceitar os parâmetros de amostragem como tais, não como premissas: dobrar a resolução de cada um e olhar as conclusões, nas casas mostradas.", "",
           "| Parâmetro | Como dobrei | Resultado | Muda nas casas mostradas? |", "| :- | :- | :- | :- |"]
    rs = o["resolucao_amostragem"]
    pb, oa, dm_, ep = rs["passos_bissecao"], rs["orbitas_amostra"], rs["diametros_m"], rs["exemplo_p086_m"]
    md.append(f"| passos_bissecao | {pb['passos']} para {pb['dobrado']} passos | margem zero em {br(pb['limite_fh_km'], 0)} e {br(pb['limite_fh_dobrado_km'], 0)} km; deixa de fechar em {br(pb['limite_fecha_km'], 0)} e {br(pb['limite_fecha_dobrado_km'], 0)} km | {'não' if pb['limite_fh_km'] == pb['limite_fh_dobrado_km'] and pb['limite_fecha_km'] == pb['limite_fecha_dobrado_km'] else '**sim**'} |")
    md.append(f"| orbitas_amostra | ponto médio geométrico entre as órbitas: {', '.join(br(x, 0) for x in oa['pontos_novos_km'])} km | comprimentos novos {', '.join(br(x) for x in oa['comprimentos_novos_m'])} m, {'em ordem entre os vizinhos' if oa['comprimento_monotono'] else 'FORA de ordem'} | {'não' if oa['comprimento_monotono'] else '**sim**'} |")
    for k, x in dm_["por_forma"].items():
        igual = br(x["melhor_folga_grade_m"]) == br(x["melhor_folga_fina_m"])
        md.append(f"| grade de diâmetros (mav_alternativas; amostragem.diametros_m é parte dela), {'4,5 m' if k == 'msl_m2020' else '4,65 m'} | {dm_['pontos']} para {dm_['dobrado']} diâmetros | melhor folga deitado na grade: {sg(x['melhor_folga_grade_m'])} m em Ø {br(x['melhor_d_grade_m'])} m; na fina: {sg(x['melhor_folga_fina_m'])} m em Ø {br(x['melhor_d_fina_m'])} m | {'não' if igual else '**sim, na folga máxima**; veja a nota'} |")
    md.append(f"| exemplo_p086_m | {br(ep['valor'], 2)} para {br(ep['metade'], 2)} m | folga por metro: {br(ep['folga_por_metro_valor'], 3)} e {br(ep['folga_por_metro_metade'], 3)} m/m | {'não' if br(ep['folga_por_metro_valor'], 3) == br(ep['folga_por_metro_metade'], 3) else '**sim**'} |")
    md += ["", "**Nota sobre os diâmetros:** a tabela de alavancas mostra só os pontos da varredura, cujos valores não dependem da grade. O que a grade fina muda é onde cai o melhor diâmetro; a conclusão de que o diâmetro não faz o MAV caber no 4,5 m se mantém enquanto a folga máxima seguir negativa.", "",
           "## Opinião do agente (separada dos dados; não é fato nem recomendação como fato)", ""]
    fh = next(x for x in o["orbitas"] if x["rotulo"].startswith("margem zero"))
    al = o["alavancas"]
    li_fh = next(x for x in al if x["grupo"] == "orbita" and x["comprimento_m"] == fh["comprimento_m"])
    ani = next(x for x in al if x["grupo"] == "tanques")
    v44 = [x for x in al if x["grupo"] == "variante"]
    md += [f"Opinião: as duas maiores alavancas são tanques aninhados ({sg(ani['delta_comprimento_m'], 2)} m, limite otimista) e R-4D-11 44:1 ({sg(v44[1]['delta_comprimento_m'], 2)} a {sg(v44[0]['delta_comprimento_m'], 2)} m, com Isp e massa sem fonte). A órbita de encontro dá {sg(li_fh['delta_comprimento_m'], 2)} m até o limite do lançador. "
           f"A órbita é a única que reduz o propelente, mas sozinha não basta: na margem zero do Falcon Heavy ({br(fh['periapse_km'], 0)} × {br(fh['apoapse_km'], 0)} km) a folga deitado é {sg(li_fh['deitado_4_5_m'], 2)} m no 4,5 m e {sg(li_fh['deitado_4_65_m'], 2)} m no 4,65 m, e margem zero não é ponto de projeto. "
           f"Ela também não resolve os bocais: ali o empuxo/peso com dois motores é {br(fh['empuxo_peso_2_motores'], 2)}, abaixo de 1, o motivo por que a opção C foi descartada. "
           "O 44:1 é a única das três alavancas que também resolveria os bocais, então eu buscaria primeiro o Isp e a massa dele. Eu não gastaria mais esforço em órbita antes disso, e a P-086 pesa pelo motor, não pela busca de mais cotas do MSR. A decisão é do Fabio."]
    (SAIDA / "comprimento_mav.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
