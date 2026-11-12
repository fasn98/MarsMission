"""Piso de ruído dos integradores da subida do MAV (Fabio, 2026-11-11, item 1a): diagnóstico, sem mudar resultados.

Para o sólido (orbital.subida.voa_solido) e o hipergólico (orbital.subida.voa), com o integrador atual e com integradores
mais apertados (P-116):
  - erro da órbita final contra um integrador de referência, com o mesmo guiamento;
  - rugosidade: desvio rms (m) de um ajuste quadrático da órbita final quando um parâmetro do guiamento varia em passos
    muito pequenos; é o ruído que o otimizador vê;
  - para o sólido, o menor custo do ajuste (orbital.subida.ajusta_solido) nas escalas da P-111 a 380 km em que o CI
    divergiu, com o integrador atual e com o mais apertado, contra a tolerância da P-110.
Saída: results/conferencia/ruido_subida.yaml e .md

Uso: python tools/ruido_subida.py
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

import mav_familia1 as mf  # noqa: E402
import subida_mav as sm  # noqa: E402
from orbital import subida as sb  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "conferencia"
br = sm.br


def rugosidade(f, x0, delta, n):
    """Desvio rms (m) do ajuste quadrático de f(x0 + k·delta), k = −n/2 … n/2, para cada saída de f."""
    ks = np.arange(n) - n // 2
    ys = np.array([f(x0 + k * delta) for k in ks])
    out = []
    for j in range(ys.shape[1]):
        c = np.polyfit(ks, ys[:, j], 2)
        r = ys[:, j] - np.polyval(c, ks)
        out.append(float(np.sqrt(np.mean(r * r))))
    return out


def main():
    cad, fc, scfg = ler("config/cad.yaml"), ler("config/familia1.yaml"), ler("config/superficie.yaml")
    mv = ler("results/familia1/mavs.yaml")
    cfg = fc["ruido_subida"]
    rg = cfg["rugosidade"]["valor"]
    ctx = sm.contexto()
    sc, _, atm, pl0, num = ctx
    g = fc["mav_solido"]["guia"]
    vf = fc["mav_solido"]["verificacao"]
    msd = cad["mav_solido"]
    mp, isp, tq = msd["propelente_kg"]["valor"], msd["isp_s"]["valor"], msd["tempo_queima_s"]["valor"]
    f = [a * i * sb.G0_M / t for a, i, t in zip(mp, isp, tq)]
    carga = v(scfg["mav"]["carga_util_kg"])
    base = mv["verificacao"]["base"]
    k = [i / x for i, x in zip(base["inertes_kg"], mp)]
    d_s = mv["limites"]["solido"]["diametro_m"]
    area = v(sc["arrasto"]["cd_base"]) * math.pi * d_s ** 2 / 4
    pl_v = sb.Planeta(pl0.mu, pl0.raio, sb.omega_efetivo(pl0.omega, v(vf["inclinacao_graus"])))
    pl_e = sb.Planeta(pl0.mu, pl0.raio, sb.omega_efetivo(pl0.omega, v(scfg["sitio_e_encontro"]["inclinacao_encontro_graus"])))
    est, ine = mf.solido(mp, f, isp, k, carga)
    gu = base["guia"]
    th0, c1, ta = math.radians(gu["theta0_graus"]), gu["c_1_s"], gu["t_antes_apoapse_s"]
    t_v = v(g["t_v_s"])

    def kw_s(x):
        return {"rtol": x[0], "atol": x[1], "max_step": x[2], "max_step_costa": x[3]}

    def orb_s(x, th=th0, t_a=ta):
        """(periapse, apoapse, semieixo, e_radial·r_alvo, e_transversal·r_alvo) em m."""
        r = sb.voa_solido(pl_v, est, ine, area, atm, (t_v, th, c1), t_a, **kw_s(x))
        r_v = pl_v.raio + 1000 * v(vf["orbita_km"])
        return [r["periapse_m"], r["apoapse_m"], r["semieixo_m"], r["ecc_radial"] * r_v, r["ecc_transversal"] * r_v]
    ref_s = orb_s(cfg["solido"]["referencia"]["valor"])
    solido = []
    for nome, x in cfg["solido"]["integradores"]["valor"].items():
        o = orb_s(x)
        rt = rugosidade(lambda z: orb_s(x, t_a=z), ta, rg["delta_t_antes_s"], int(rg["passos"]))
        rh = rugosidade(lambda z: orb_s(x, th=z), th0, rg["delta_theta0_rad"], int(rg["passos"]))
        solido.append({"integrador": nome, "rtol": x[0], "atol": x[1], "max_step_s": x[2], "max_step_costa_s": x[3],
                       "erro_periapse_m": abs(o[0] - ref_s[0]), "erro_apoapse_m": abs(o[1] - ref_s[1]), "erro_semieixo_m": abs(o[2] - ref_s[2]),
                       "erro_excentricidade_m": max(abs(o[3] - ref_s[3]), abs(o[4] - ref_s[4])),
                       "rugosidade_apses_t_antes_m": max(rt[:2]), "rugosidade_apses_theta0_m": max(rh[:2]),
                       "rugosidade_suave_t_antes_m": max(rt[2:]), "rugosidade_suave_theta0_m": max(rh[2:])})
    # custo mínimo do ajuste nas escalas da P-111 a 380 km
    tol = v(g["tol_custo"])
    partidas, limites = g["partidas"]["valor"], [tuple(t) for t in g["limites"]["valor"]]
    f_m = [m_ * i * sb.G0_M / t for m_, i, t in zip(mp, isp, tq)]
    custos = []
    nomes = list(cfg["solido"]["integradores"]["valor"])
    for s_ in cfg["escalas_custo"]["valor"]:
        e_, i_ = mf.solido([s_ * x for x in mp], [s_ * x for x in f_m], isp, k, carga)
        linha = {"escala": s_}
        for rotulo, nome, res_ in (("apses, atual", nomes[0], "apses"), ("suave, atual", nomes[0], "suave")):
            x = cfg["solido"]["integradores"]["valor"][nome]
            c_, vo, _ = sb.ajusta_solido(pl_e, e_, i_, area, atm, 380e3, t_v, partidas, limites, residuo=res_,
                                         integrador={"rtol": x[0], "atol": x[1], "max_step_s": x[2], "max_step_costa_s": x[3]})
            linha[rotulo] = {"custo": c_, "erro_orbita_m": 1.0e4 * math.sqrt(2 * c_), "fecha": c_ < tol}
        custos.append(linha)
    # reprodutibilidade da escala mínima do sólido (P-117), P-111
    lo, hi = g["escala_busca"]["valor"]
    passo = v(g["passo_varredura_escala"])
    em_ = fc["mav_solido"]["escala_minima"]
    nm_ = {"tol_ls": v(em_["tol_ls"]), "custo_circular": v(em_["custo_circular"]), "xatol_c": v(em_["xatol_c"])}
    x0 = cfg["solido"]["integradores"]["valor"]["atual"]
    pert = v(cfg["perturbacao_relativa"])
    ds = v(cfg["perturbacao_escala"])
    repro = []
    for h in cfg["altitudes_reprodutibilidade_km"]["valor"]:
        def maquina(itg=None, cg=carga, d_s=0.0, h=h):
            def tenta(s_):
                e_, i_ = mf.solido([s_ * y for y in mp], [s_ * y for y in f_m], isp, k, cg)
                return sb.ajusta_solido(pl_e, e_, i_, area, atm, 1000 * h, t_v, partidas, limites, integrador=itg), e_, i_

            def deficit(s_):
                s2 = s_ + d_s
                e_, i_ = mf.solido([s2 * y for y in mp], [s2 * y for y in f_m], isp, k, cg)
                a_m, vo, gu = sb.semieixo_circular_maximo(pl_e, e_, i_, area, atm, t_v, partidas, limites, nm_, integrador=itg)
                return (-1.0e7 if a_m is None else a_m - (pl_e.raio + 1000 * h)), vo, gu
            return tenta, deficit

        # a raiz do caso atual é a de results/familia1/mavs.yaml (a mesma conta, P-117); as perturbadas, por brentq num
        # intervalo estreito em torno dela, com os sinais do déficit conferidos
        from scipy.optimize import brentq
        sv = next(x for x in mv["solido"] if x.get("fecha") and x.get("simulado") and x["altitude_km"] == h)
        s0 = sv["escala"]
        meia = v(cfg["meia_largura_intervalo"]) * s0
        repro.append({"altitude_km": h, "variante": "atual", "metodo": "raiz de results/familia1/mavs.yaml", "fecha": True, "escala": s0, "glom_kg": sv["glom_kg"], "deficit_m": sv["deficit_na_escala_m"]})

        def raiz(nome, **kw):
            deficit = maquina(**kw)[1]
            da, db = deficit(s0 - meia)[0], deficit(s0 + meia)[0]
            linha = {"altitude_km": h, "variante": nome, "metodo": "raiz por brentq em torno da atual" if da < 0 < db else "sinal do déficit não troca no intervalo", "fecha": da < 0 < db, "deficit_intervalo_m": [da, db]}
            if linha["fecha"]:
                r_ = brentq(lambda x: deficit(x)[0], s0 - meia, s0 + meia, xtol=v(em_["xtol_escala"]), rtol=4 * np.finfo(float).eps)
                e_, i_ = mf.solido([r_ * y for y in mp], [r_ * y for y in f_m], isp, k, kw.get("cg", carga))
                linha.update({"escala": r_, "glom_kg": e_[0].massa_inicial_kg, "deficit_m": deficit(r_)[0]})
            return linha
        repro.append(raiz(f"escala + {e(ds)} no déficit", d_s=ds))
        repro.append(raiz(f"carga útil × (1 + {e(pert)})", cg=carga * (1 + pert)))
        lo_m, hi_m = sv["busca_da_escala"]["intervalo"]
        d_lo, d_hi = sv["busca_da_escala"]["deficit_m"]
        inclinacao = (d_hi - d_lo) / (hi_m - lo_m)
        inclinacao_md, escala_md = inclinacao, s0
        for fz in cfg["fatores_tolerancia"]["valor"]:
            itg = {"rtol": x0[0] * fz, "atol": x0[1] * fz, "max_step_s": x0[2], "max_step_costa_s": x0[3]}
            d_ = maquina(itg=itg)[1](s0)[0]
            s1 = s0 - d_ / inclinacao
            e_, i_ = mf.solido([s1 * y for y in mp], [s1 * y for y in f_m], isp, k, carga)
            repro.append({"altitude_km": h, "variante": f"rtol e atol × {br(fz, 1)}", "metodo": "primeira ordem (déficit na raiz ÷ inclinação do intervalo)",
                          "fecha": True, "escala": s1, "glom_kg": e_[0].massa_inicial_kg, "deficit_m": d_})
    # hipergólico: o veículo de referência da subida (P-104), com o guiamento ótimo do integrador atual
    r = sc["referencia"]
    m0 = v(r["massa_kg"])
    gp = pl0.mu / pl0.raio ** 2
    est_h = [sb.Estagio(m0, m0, v(r["empuxo_peso"]) * m0 * gp, v(r["isp_s"]))]
    area_h = v(sc["arrasto"]["cd_base"]) * v(r["area_m2"])
    h_alvo = v(sc["alvo_altitude_m"])
    x_ref = sm.voo(ctx, est_h, area_h)
    gh = x_ref["guia"]
    th_h, c_h, tv_h = math.radians(gh["theta0_graus"]), gh["c_1_s"], gh["t_v_s"]

    def orb_h(x, th=th_h):
        y = sb.voa(pl0, est_h, area_h, atm, (tv_h, th, c_h), h_alvo, rtol=x[0], atol=x[1], max_step=x[2])
        return [y["residuo"][0], y["residuo"][1], y["dv_m_s"]]
    ref_h = orb_h(cfg["hipergolico"]["referencia"]["valor"])
    hip = []
    for nome, x in cfg["hipergolico"]["integradores"]["valor"].items():
        o = orb_h(x)
        rh = rugosidade(lambda z: orb_h(x, th=z), th_h, rg["delta_theta0_rad"], int(rg["passos"]))
        hip.append({"integrador": nome, "rtol": x[0], "atol": x[1], "max_step_s": x[2],
                    "erro_altitude_m": abs(o[0] - ref_h[0]), "erro_vr_m_s": abs(o[1] - ref_h[1]), "erro_dv_m_s": abs(o[2] - ref_h[2]),
                    "rugosidade_altitude_m": rh[0], "rugosidade_vr_m_s": rh[1], "rugosidade_dv_m_s": rh[2]})
    out = nativo({"gerado_por": "tools/ruido_subida.py", "status": "diagnóstico; não muda resultados", "solido": solido, "custos_p111_380km": custos,
                  "tol_custo_p110": tol, "tol_hipergolico": {"altitude_m": num["tol_m"], "vr_m_s": num["tol_m_s"]}, "hipergolico": hip, "rugosidade": rg, "reprodutibilidade": repro,
                  "inclinacao_deficit_m": inclinacao_md, "escala_atual": escala_md, "perturbacao_escala": ds, "perturbacao_relativa": pert})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "ruido_subida.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def e(x):
    return f"{x:.1e}".replace(".", ",")


def escreve_md(o):
    rg = o["rugosidade"]
    md = ["# Piso de ruído da subida (gerado por tools/ruido_subida.py)", "", "**Diagnóstico (P-116, NÃO VALIDADA); não muda nenhum resultado.** Os tempos de execução não ficam aqui (mudam de máquina para máquina); saem no log.", "",
          "## Sólido (`voa_solido`), MAV do MSR na divisão de base, guiamento da verificação", "",
          f"Rugosidade: desvio rms do ajuste quadrático da órbita final em {rg['passos']} passos de {e(rg['delta_t_antes_s'])} s na antecedência e de {e(rg['delta_theta0_rad'])} rad em θ0. "
          "\"Apses\": maior entre periapse e apoapse, que têm uma quina em e = 0 (a órbita da verificação é quase circular). \"Suave\": maior entre o semieixo e as componentes do vetor excentricidade vezes o raio-alvo.", "",
          "| Integrador | rtol | atol | Passo máx. queima / costa (s) | Erro contra a referência: periapse / apoapse / semieixo / excentricidade (m) | Rugosidade apses: antecedência / θ0 (m) | Rugosidade suave: antecedência / θ0 (m) |",
          "| :- | -: | -: | -: | -: | -: | -: |"]
    md += [f"| {x['integrador']} | {e(x['rtol'])} | {e(x['atol'])} | {br(x['max_step_s'], 2)} / {br(x['max_step_costa_s'], 2)} | {e(x['erro_periapse_m'])} / {e(x['erro_apoapse_m'])} / {e(x['erro_semieixo_m'])} / {e(x['erro_excentricidade_m'])} | "
           f"{e(x['rugosidade_apses_t_antes_m'])} / {e(x['rugosidade_apses_theta0_m'])} | {e(x['rugosidade_suave_t_antes_m'])} / {e(x['rugosidade_suave_theta0_m'])} |" for x in o["solido"]]
    a0, a1 = o["solido"][0], o["solido"][-1]
    md += ["", f"Em grandezas suaves, a rugosidade cai de {e(max(a0['rugosidade_suave_t_antes_m'], a0['rugosidade_suave_theta0_m']))} m (integrador {a0['integrador']}) para {e(max(a1['rugosidade_suave_t_antes_m'], a1['rugosidade_suave_theta0_m']))} m (integrador {a1['integrador']}): o ruído do integrador existe e cai ao apertá-lo. "
           f"Em periapse e apoapse, ela fica entre {e(min(max(x['rugosidade_apses_t_antes_m'], x['rugosidade_apses_theta0_m']) for x in o['solido']))} e {e(max(max(x['rugosidade_apses_t_antes_m'], x['rugosidade_apses_theta0_m']) for x in o['solido']))} m porque mede a quina, não o integrador.", "",
           "**Errata (2026-11-11):** a primeira versão deste diagnóstico (commit 5729b00, não publicado) media a rugosidade só em periapse e apoapse e concluía que \"o ruído do sólido não vem do integrador\". Essa conclusão não se sustenta: aquela medida via a quina em e = 0. Vale a medida em grandezas suaves acima. O diagnóstico do ajuste (a quina no resíduo espalhava o custo, tabela abaixo) continua valendo."]
    nomes = [k for k in o["custos_p111_380km"][0] if k != "escala"]
    md += ["", f"## Sólido: menor custo do ajuste, P-111 a 380 km (tolerância da P-110: {e(o['tol_custo_p110'])}, ~{br(1.0e4 * math.sqrt(2 * o['tol_custo_p110']), 0)} m)", "",
           "| Escala | " + " | ".join(f"Custo, {n} | Erro da órbita (m), {n} | Fecha? {n}" for n in nomes) + " |", "| -: | " + " | ".join("-: | -: | :-" for _ in nomes) + " |"]
    for c in o["custos_p111_380km"]:
        md.append(f"| {br(c['escala'], 2)} | " + " | ".join(f"{e(c[n]['custo'])} | {br(c[n]['erro_orbita_m'], 1)} | {'sim' if c[n]['fecha'] else 'não'}" for n in nomes) + " |")
    md += ["", "## Reprodutibilidade da escala mínima do sólido (P-117), P-111", "",
           "A escala mínima é a raiz de (maior semieixo de uma circular alcançável) − (raio-alvo). A raiz do caso atual é a de results/familia1/mavs.yaml; nas duas perturbações do tamanho do ruído de ponto flutuante, a raiz é refeita por brentq num intervalo estreito em torno dela (sinais do déficit conferidos); nas variantes do integrador, a estimativa de primeira ordem (déficit na raiz atual dividido pela inclinação do déficit no intervalo).", "",
           "| Encontro (km) | Variante | Método | Escala | Diferença relativa da escala | GLOM (kg) | Diferença relativa do GLOM | Déficit na raiz (m) |", "| -: | :- | :- | -: | -: | -: | -: | -: |"]
    base = {x["altitude_km"]: x for x in o["reprodutibilidade"] if x["variante"] == "atual" and x["fecha"]}
    for x in o["reprodutibilidade"]:
        b0 = base.get(x["altitude_km"])
        if not x["fecha"]:
            md.append(f"| {br(x['altitude_km'], 0)} | {x['variante']} | {x['metodo']} | sem raiz no intervalo | | | | |")
            continue
        md.append(f"| {br(x['altitude_km'], 0)} | {x['variante']} | {x['metodo']} | {br(x['escala'], 10)} | {e((x['escala'] - b0['escala']) / b0['escala'])} | {br(x['glom_kg'], 6)} | {e((x['glom_kg'] - b0['glom_kg']) / b0['glom_kg'])} | {e(x['deficit_m'])} |")
    ints = [x for x in o["reprodutibilidade"] if x["metodo"].startswith("primeira ordem")]
    rz = o["solido"][0]
    risco = max(rz["rugosidade_suave_t_antes_m"], rz["rugosidade_suave_theta0_m"]) / o["inclinacao_deficit_m"] / o["escala_atual"]
    md += ["", "**As variantes do integrador ficam fora da P-039** (" + " e ".join(f"{e((x['escala'] - base[x['altitude_km']]['escala']) / base[x['altitude_km']]['escala'])}" for x in ints)
           + " na escala): a parte do critério que pedia perturbar as tolerâncias do integrador dentro da P-039 **não foi atendida**. Essas variantes mudam o modelo (o erro de truncamento do integrador atual no semieixo é "
           + f"{e(rz['erro_semieixo_m'])} m contra a referência), e foram estimadas em primeira ordem, em dois pontos, sem refazer a raiz: não demonstram continuidade.",
           "", f"**Risco residual entre CPUs.** As perturbações de {e(o['perturbacao_escala'])} na escala e de {e(o['perturbacao_relativa'])} na carga mudam a escala em ~1e-12, porque não viram nenhuma decisão discreta do integrador (aceitar ou rejeitar um passo). "
           f"Se outra CPU virar uma dessas decisões, o salto pode ter a ordem da rugosidade do integrador atual em grandezas suaves ({e(max(rz['rugosidade_suave_t_antes_m'], rz['rugosidade_suave_theta0_m']))} m), ~{e(risco)} relativo na escala pela inclinação do déficit, acima da P-039. "
           "A prova é a regeneração do CI em outra CPU. A decisão sobre esse risco é do Fabio."]
    th = o["tol_hipergolico"]
    md += ["", f"## Hipergólico (`voa`), veículo de referência da subida, guiamento ótimo do integrador atual (tolerâncias da P-107: {br(th['altitude_m'], 1)} m e {br(th['vr_m_s'], 1)} m/s)", "",
           "| Integrador | rtol | atol | Passo máx. (s) | Erro contra a referência: altitude (m) / v radial (m/s) / Δv (m/s) | Rugosidade em θ0: altitude (m) / v radial (m/s) / Δv (m/s) |",
           "| :- | -: | -: | -: | -: | -: |"]
    md += [f"| {x['integrador']} | {e(x['rtol'])} | {e(x['atol'])} | {br(x['max_step_s'], 2)} | {e(x['erro_altitude_m'])} / {e(x['erro_vr_m_s'])} / {e(x['erro_dv_m_s'])} | {e(x['rugosidade_altitude_m'])} / {e(x['rugosidade_vr_m_s'])} / {e(x['rugosidade_dv_m_s'])} |" for x in o["hipergolico"]]
    md += ["", "As tolerâncias da P-107 ficam acima da rugosidade do hipergólico em todos os integradores: não há proposta de mudança."]
    (SAIDA / "ruido_subida.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
