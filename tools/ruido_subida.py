"""Piso de ruído dos integradores da subida do MAV (Fabio, 2026-11-11, item 1a): diagnóstico, sem mudar resultados.

Para o sólido (orbital.subida.voa_solido) e o hipergólico (orbital.subida.voa), com o integrador atual e com integradores
mais apertados (P-116):
  - erro da órbita final contra um integrador de referência, com o mesmo guiamento;
  - rugosidade: desvio rms (m) de um ajuste quadrático da órbita final quando um parâmetro do guiamento varia em passos
    muito pequenos; é o ruído que o otimizador vê;
  - tempo por voo;
  - para o sólido, o menor custo do ajuste (orbital.subida.ajusta_solido) nas escalas da P-111 a 380 km em que o CI
    divergiu, com o integrador atual e com o mais apertado, contra a tolerância da P-110.
Saída: results/conferencia/ruido_subida.yaml e .md

Uso: python tools/ruido_subida.py
"""

from __future__ import annotations

import math
import sys
import time
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
        r = sb.voa_solido(pl_v, est, ine, area, atm, (t_v, th, c1), t_a, **kw_s(x))
        return [r["periapse_m"], r["apoapse_m"]]
    ref_s = orb_s(cfg["solido"]["referencia"]["valor"])
    solido = []
    for nome, x in cfg["solido"]["integradores"]["valor"].items():
        t0 = time.perf_counter()
        o = orb_s(x)
        dt = time.perf_counter() - t0
        rt = rugosidade(lambda z: orb_s(x, t_a=z), ta, rg["delta_t_antes_s"], int(rg["passos"]))
        rh = rugosidade(lambda z: orb_s(x, th=z), th0, rg["delta_theta0_rad"], int(rg["passos"]))
        solido.append({"integrador": nome, "rtol": x[0], "atol": x[1], "max_step_s": x[2], "max_step_costa_s": x[3], "tempo_voo_s": dt,
                       "erro_periapse_m": abs(o[0] - ref_s[0]), "erro_apoapse_m": abs(o[1] - ref_s[1]),
                       "rugosidade_t_antes_m": max(rt), "rugosidade_theta0_m": max(rh)})
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
            t0 = time.perf_counter()
            c_, vo, _ = sb.ajusta_solido(pl_e, e_, i_, area, atm, 380e3, t_v, partidas, limites, residuo=res_,
                                         integrador={"rtol": x[0], "atol": x[1], "max_step_s": x[2], "max_step_costa_s": x[3]})
            linha[rotulo] = {"custo": c_, "erro_orbita_m": 1.0e4 * math.sqrt(2 * c_), "fecha": c_ < tol, "tempo_s": time.perf_counter() - t0}
        custos.append(linha)
    # reprodutibilidade da escala mínima do sólido (P-117), P-111, nas altitudes da família 1
    alts = cfg["altitudes_reprodutibilidade_km"]["valor"]
    lo, hi = g["escala_busca"]["valor"]
    passo, passos = v(g["passo_varredura_escala"]), int(v(g["passos_escala"]))
    x0 = cfg["solido"]["integradores"]["valor"]["atual"]
    variantes = [("atual", x0, carga)] + [(f"rtol e atol × {br(fz, 1)}", [x0[0] * fz, x0[1] * fz, x0[2], x0[3]], carga) for fz in cfg["fatores_tolerancia"]["valor"]]
    variantes.append((f"carga útil × (1 + {e(v(cfg['perturbacao_relativa']))})", x0, carga * (1 + v(cfg["perturbacao_relativa"]))))
    repro = []
    for h in alts:
        for nome, x, cg in variantes:
            itg = {"rtol": x[0], "atol": x[1], "max_step_s": x[2], "max_step_costa_s": x[3]}

            def tenta(s_, itg=itg, cg=cg):
                e_, i_ = mf.solido([s_ * y for y in mp], [s_ * y for y in f_m], isp, k, cg)
                return sb.ajusta_solido(pl_e, e_, i_, area, atm, 1000 * h, t_v, partidas, limites, integrador=itg), e_, i_
            t0 = time.perf_counter()
            r_ = mf.escala_minima(tenta, lo, hi, passo, passos, tol)
            linha = {"altitude_km": h, "variante": nome, "fecha": r_ is not None, "tempo_s": time.perf_counter() - t0}
            if r_:
                (c_, vo, gu), e_, i_ = r_[1]
                linha.update({"escala": r_[0], "glom_kg": e_[0].massa_inicial_kg, "custo": c_, "costa_s": vo["costa_s"], "guia": gu,
                              "semieixo_abaixo_km": (r_[2]["semieixo_m"] - pl_e.raio) / 1000 if r_[2] and r_[2]["semieixo_m"] else None})
            repro.append(linha)
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
        t0 = time.perf_counter()
        o = orb_h(x)
        dt = time.perf_counter() - t0
        rh = rugosidade(lambda z: orb_h(x, th=z), th_h, rg["delta_theta0_rad"], int(rg["passos"]))
        hip.append({"integrador": nome, "rtol": x[0], "atol": x[1], "max_step_s": x[2], "tempo_voo_s": dt,
                    "erro_altitude_m": abs(o[0] - ref_h[0]), "erro_vr_m_s": abs(o[1] - ref_h[1]), "erro_dv_m_s": abs(o[2] - ref_h[2]),
                    "rugosidade_altitude_m": rh[0], "rugosidade_vr_m_s": rh[1], "rugosidade_dv_m_s": rh[2]})
    out = nativo({"gerado_por": "tools/ruido_subida.py", "status": "diagnóstico; não muda resultados", "solido": solido, "custos_p111_380km": custos,
                  "tol_custo_p110": tol, "tol_hipergolico": {"altitude_m": num["tol_m"], "vr_m_s": num["tol_m_s"]}, "hipergolico": hip, "rugosidade": rg, "reprodutibilidade": repro})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "ruido_subida.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def e(x):
    return f"{x:.1e}".replace(".", ",")


def escreve_md(o):
    rg = o["rugosidade"]
    md = ["# Piso de ruído da subida (gerado por tools/ruido_subida.py)", "", "**Diagnóstico (P-116, NÃO VALIDADA); não muda nenhum resultado.**", "",
          "## Sólido (`voa_solido`), MAV do MSR na divisão de base, guiamento da verificação", "",
          f"Rugosidade: desvio rms do ajuste quadrático da órbita final em {rg['passos']} passos de {e(rg['delta_t_antes_s'])} s na antecedência e de {e(rg['delta_theta0_rad'])} rad em θ0 (maior entre periapse e apoapse).", "",
          "| Integrador | rtol | atol | Passo máx. queima / costa (s) | Erro contra a referência, periapse / apoapse (m) | Rugosidade na antecedência (m) | Rugosidade em θ0 (m) | Tempo por voo (s) |",
          "| :- | -: | -: | -: | -: | -: | -: | -: |"]
    md += [f"| {x['integrador']} | {e(x['rtol'])} | {e(x['atol'])} | {br(x['max_step_s'], 2)} / {br(x['max_step_costa_s'], 2)} | {e(x['erro_periapse_m'])} / {e(x['erro_apoapse_m'])} | {e(x['rugosidade_t_antes_m'])} | {e(x['rugosidade_theta0_m'])} | {br(x['tempo_voo_s'], 3)} |" for x in o["solido"]]
    nomes = [k for k in o["custos_p111_380km"][0] if k != "escala"]
    md += ["", f"## Sólido: menor custo do ajuste, P-111 a 380 km (tolerância da P-110: {e(o['tol_custo_p110'])}, ~{br(1.0e4 * math.sqrt(2 * o['tol_custo_p110']), 0)} m)", "",
           "| Escala | " + " | ".join(f"Custo, {n} | Erro da órbita (m), {n} | Fecha? {n} | Tempo (s), {n}" for n in nomes) + " |", "| -: | " + " | ".join("-: | -: | :- | -:" for _ in nomes) + " |"]
    for c in o["custos_p111_380km"]:
        md.append(f"| {br(c['escala'], 2)} | " + " | ".join(f"{e(c[n]['custo'])} | {br(c[n]['erro_orbita_m'], 1)} | {'sim' if c[n]['fecha'] else 'não'} | {br(c[n]['tempo_s'], 0)}" for n in nomes) + " |")
    md += ["", "## Reprodutibilidade da escala mínima do sólido (P-117), P-111", "",
           "| Encontro (km) | Variante | Escala | GLOM (kg) | Custo | Costa (s) | Semieixo na maior escala que não fecha (km) | Tempo (s) |", "| -: | :- | -: | -: | -: | -: | -: | -: |"]
    for x in o["reprodutibilidade"]:
        md.append(f"| {br(x['altitude_km'], 0)} | {x['variante']} | " + (f"{br(x['escala'], 6)} | {br(x['glom_kg'], 3)} | {e(x['custo'])} | {br(x['costa_s'], 3)} | " + (br(x['semieixo_abaixo_km'], 1) if x['semieixo_abaixo_km'] is not None else "—") if x["fecha"] else "não fecha | | | | ") + f" | {br(x['tempo_s'], 0)} |")
    th = o["tol_hipergolico"]
    md += ["", f"## Hipergólico (`voa`), veículo de referência da subida, guiamento ótimo do integrador atual (tolerâncias da P-107: {br(th['altitude_m'], 1)} m e {br(th['vr_m_s'], 1)} m/s)", "",
           "| Integrador | rtol | atol | Passo máx. (s) | Erro contra a referência: altitude (m) / v radial (m/s) / Δv (m/s) | Rugosidade em θ0: altitude (m) / v radial (m/s) / Δv (m/s) | Tempo por voo (s) |",
           "| :- | -: | -: | -: | -: | -: | -: |"]
    md += [f"| {x['integrador']} | {e(x['rtol'])} | {e(x['atol'])} | {br(x['max_step_s'], 2)} | {e(x['erro_altitude_m'])} / {e(x['erro_vr_m_s'])} / {e(x['erro_dv_m_s'])} | {e(x['rugosidade_altitude_m'])} / {e(x['rugosidade_vr_m_s'])} / {e(x['rugosidade_dv_m_s'])} | {br(x['tempo_voo_s'], 3)} |" for x in o["hipergolico"]]
    (SAIDA / "ruido_subida.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
