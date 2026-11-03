"""Etapa 7.2 (pedido do Fabio no portão): alternativas de arranjo do MAV na cápsula, antes da decisão de aeroshell e MAV.

- (d) MAV mais largo e mais curto, com o mesmo propelente: diâmetros de config/cad.yaml (mav_alternativas), comprimento
  pelos mesmos segmentos da Etapa 7.1 (tools/envelope_arranjo.segmentos_mav: P-085, P-086), nas formas MSL/M2020 e SRL-A
  ([F41] Fig. 2, P-089), com a folga interna da P-087 e a base do MAV deitado em três estações: o plano do ombro, o ombro
  + metade da altura do deck e o ombro + a altura do deck (P-094).
- (c) MAV em pé no eixo da cápsula: comprimento disponível da base até onde o raio interno (raio − folga da P-087) fica
  igual ao raio do MAV, nas mesmas estações.
- Efeito na massa: massa dos tanques (Ti-6Al-4V [F219], espessura da P-093; cilindro com tampos hemisféricos, ou esfera
  quando o volume cabe numa esfera menor que o diâmetro). O orçamento do MAV (fração estrutural, ADR 0007) não depende do
  diâmetro.
Saída: results/etapa7.2/mav_arranjo.yaml e .md

Uso: python tools/mav_arranjo.py
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

import envelope_arranjo as ea  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"


def massa_tanques(dmav, est_m, t_env, t_tq, rho_ti, of, rho_ox, rho_fu, ull):
    """Massa (kg) das cascas dos quatro tanques do MAV: cilindro com tampos hemisféricos no diâmetro interno, ou esfera."""
    di = dmav - 2 * t_env
    m = 0.0
    for e in est_m:
        vol = ea.volumes(e["propelente_kg"], of, rho_ox, rho_fu, ull)
        for vt in (vol["tanque_oxidante_m3"], vol["tanque_combustivel_m3"]):
            if vt <= math.pi * di ** 3 / 6:
                area = math.pi * ea.esfera(vt) ** 2
            else:
                lc = ea.tanque_cilindrico(vt, di) - di
                area = math.pi * di * lc + math.pi * di ** 2
            m += area * t_tq * rho_ti
    return m


def main():
    cad, arq = ler("config/cad.yaml"), ler("results/etapa2.5/arquitetura.yaml")
    pr, mv, alt = cad["propelentes"], cad["mav"], cad["mav_alternativas"]
    rho_ox, rho_fu = v(pr["densidade_oxidante_kg_m3"]), v(pr["densidade_mmh_kg_m3"])
    ull, of = v(pr["fracao_ullage"]), v(pr["razao_mistura_r4d11"])
    est_m = arq["lander"]["mav"]["estagios"]
    t_env = v(mv["espessura_parede_m"])
    nt = {k: v(x) for k, x in mv["comprimento_nao_tanque_m"].items()}
    t_tq = v(cad["construcao"]["tanques"]["espessura_m"])
    rho_ti = v(cad["materiais"][cad["construcao"]["tanques"]["material"]])
    fi = v(cad["aeroshell"]["folga_interna_m"])
    h_deck = v(cad["construcao"]["equivalentes"]["deck_lander_altura_m"])

    perfis = {k: ([float(x) for x in cad["capsulas"][k]["x_m"]], [float(x) for x in cad["capsulas"][k]["r_m"]]) for k in alt["formas"]}
    linhas, ref = [], None
    for d in [float(x) for x in alt["diametros_m"]]:
        segs = ea.segmentos_mav(d, est_m, nt, t_env, of, rho_ox, rho_fu, ull)
        comp = sum(s[1] for s in segs)
        mt = massa_tanques(d, est_m, t_env, t_tq, rho_ti, of, rho_ox, rho_fu, ull)
        ref = mt if ref is None else ref
        caso = {"diametro_m": d, "comprimento_m": comp, "massa_tanques_kg": mt, "variacao_massa_tanques_kg": mt - ref, "formas": {}}
        for k, (xs, rs) in perfis.items():
            x_ombro = xs[int(np.argmax(rs))]
            r_in = lambda x: float(np.interp(x, xs, rs)) - fi  # noqa: E731
            estacoes = []
            for nome, xb in (("ombro", x_ombro), ("ombro + meio deck", x_ombro + h_deck / 2), ("ombro + deck (P-094)", x_ombro + h_deck)):
                # (d) deitado: o topo do MAV (xb + d) limita o comprimento; folga = raio interno − meio comprimento
                deitado = r_in(xb + d) - comp / 2
                # (c) em pé no eixo: comprimento até onde o raio interno fica igual ao raio do MAV
                xg = np.linspace(xb, xs[-1], 2000)
                ok = np.array([r_in(x) >= d / 2 for x in xg])
                x_lim = xg[np.argmin(ok)] if not ok.all() else xs[-1]
                disponivel = float(x_lim - xb) if ok[0] else 0.0
                estacoes.append({"estacao": nome, "estacao_base_m": xb, "deitado_folga_m": deitado,
                                 "em_pe_comprimento_disponivel_m": disponivel, "em_pe_folga_m": disponivel - comp})
            caso["formas"][k] = estacoes
        linhas.append(caso)
    out = nativo({"gerado_por": "tools/mav_arranjo.py", "folga_interna_m": fi, "altura_deck_m": h_deck, "casos": linhas,
                  "glom_orcamento_kg": est_m[0]["massa_inicial_kg"]})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "mav_arranjo.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    br = lambda x, n=2: f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    nomes = {"msl_m2020": "MSL/M2020 (4,5 m)", "srl_a": "SRL-A (4,65 m)"}
    c0 = o["casos"][0]
    formas = list(c0["formas"])
    ests = [e["estacao"] for e in c0["formas"][formas[0]]]
    md = ["# MAV na cápsula: deitado e em pé, por diâmetro (gerado por tools/mav_arranjo.py)", "",
          f"Mesmo propelente; comprimento pelos segmentos da Etapa 7.1 (P-085, P-086); folga interna de {br(o['folga_interna_m'])} m (P-087); "
          f"altura do deck {br(o['altura_deck_m'])} m (P-094). Folga positiva = cabe. Comprimentos e folgas em m.", "",
          "## Comprimento e massa dos tanques", "",
          "| Diâmetro | Comprimento | Massa dos tanques (kg) | Variação sobre o diâmetro de 0,57 m (kg) |", "| -: | -: | -: | -: |"]
    for c in o["casos"]:
        md.append(f"| {br(c['diametro_m'])} | {br(c['comprimento_m'])} | {br(c['massa_tanques_kg'], 1)} | {br(c['variacao_massa_tanques_kg'], 1)} |")
    md += ["", f"O orçamento do MAV ({br(o['glom_orcamento_kg'], 1)} kg, fração estrutural do ADR 0007) não depende do diâmetro; a variação acima é só a das cascas dos tanques.", ""]
    for k in formas:
        md += [f"## {nomes.get(k, k)}", "",
               "| Diâmetro | Comprimento | " + " | ".join(f"Deitado, base no {e}" for e in ests) + " | " + " | ".join(f"Em pé, base no {e}" for e in ests) + " |",
               "| -: | -: |" + " -: |" * (2 * len(ests))]
        for c in o["casos"]:
            es = c["formas"][k]
            md.append(f"| {br(c['diametro_m'])} | {br(c['comprimento_m'])} | " + " | ".join(br(e["deitado_folga_m"]) for e in es) + " | "
                      + " | ".join(f"{br(e['em_pe_folga_m'])} (disp. {br(e['em_pe_comprimento_disponivel_m'])})" for e in es) + " |")
        md.append("")
    md += ["Estações da base (distância ao nariz): " + "; ".join(f"{e['estacao']} = {br(e['estacao_base_m'])} m" for e in c0["formas"][formas[0]]) + ".",
           "Em pé: comprimento disponível da base até onde o raio interno (raio − folga) fica igual ao raio do MAV; a folga é esse comprimento menos o do MAV."]
    (SAIDA / "mav_arranjo.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
