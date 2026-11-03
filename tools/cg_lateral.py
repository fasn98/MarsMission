"""Etapa 7.2 (achado para o portão da 7.3): CG lateral e produtos de inércia do lander, peça a peça.

- Contribuição de cada corpo (results/etapa7.2/parametros.yaml, modelo atual) para o CG x e y (m·x, m·y) e para os
  produtos de inércia no CG (termo de eixos paralelos mais o próprio tensor do corpo).
- CG na configuração de lançamento (todos os corpos) e na de entrada (sem o estágio de cruzeiro, descartado antes da
  entrada); deslocamento radial e razão sobre o diâmetro da cápsula.
- Referência do MSL (config/cad.yaml, entrada_referencia): deslocamento radial do CG intencional, com massas de balanço,
  para trimar e gerar sustentação [F226, F227, F214]. Nenhuma peça é mudada de lugar aqui.
Saída: results/etapa7.2/cg_lateral.yaml e .md

Uso: python tools/cg_lateral.py
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

import cad_parametros as cp  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"
# conjuntos de peças, pelo começo do nome dado em tools/cad_parametros.py (classificação, não dimensão)
CONJUNTOS = [("Estágio de cruzeiro", ("Tanque cruzeiro", "Propelente cruzeiro", "Circuito de fluido")),
             ("Descida (3 tanques a 120°)", ("Tanque descida", "Propelente descida")), ("MAV (deitado ao longo de y)", ("MAV",)),
             ("Braço (guardado em x = +0,45 m)", ("Braço",)), ("Helicópteros", ("Helicóptero",)), ("Núcleo do lander", ("Nucleo",)),
             ("Cápsula (escudo e casca)", ("Nariz", "Escudo", "Casca", "Tampa"))]


def agrupa(contrib):
    out = []
    for nome, pref in CONJUNTOS:
        xs = [x for x in contrib if x["nome"].startswith(pref)]
        if xs:
            out.append({"conjunto": nome, "massa_kg": sum(x["massa_kg"] for x in xs), **{k: sum(x[k] for x in xs) for k in ("mx_kg_m", "my_kg_m", "Ixy", "Ixz", "Iyz")}})
    resto = [x for x in contrib if not any(x["nome"].startswith(p) for _, pr in CONJUNTOS for p in pr)]
    assert not resto, [x["nome"] for x in resto]
    return out


def propriedades(corpos, dens):
    """(massa, CG, tensor no CG, contribuições por corpo)."""
    ms = [c["massa_kg"] for c in corpos]
    cs = [cp.centro(c) for c in corpos]
    m = sum(ms)
    cg = sum(mi * ci for mi, ci in zip(ms, cs)) / m
    T = np.zeros((3, 3))
    contrib = []
    for c, mi, ci in zip(corpos, ms, cs):
        rho = c["densidade"] if c["material"] == "equivalente" else dens[c["material"]]
        d = ci - cg
        t = cp.inercia(c, rho) + mi * (np.dot(d, d) * np.eye(3) - np.outer(d, d))
        T += t
        contrib.append({"nome": c["nome"], "massa_kg": mi, "centro_m": ci.tolist(), "mx_kg_m": mi * ci[0], "my_kg_m": mi * ci[1],
                        "Ixy": t[0][1], "Ixz": t[0][2], "Iyz": t[1][2]})
    return m, cg, T, contrib


def main():
    cad, r = ler("config/cad.yaml"), ler("results/etapa7.2/parametros.yaml")
    dens = {k: x["densidade_kg_m3"] for k, x in r["materiais"].items()}
    ref = cad["entrada_referencia"]
    corpos = r["veiculos"]["lander"]
    forma = cad["capsulas"]["forma_da_opcao"][cad["escolha"]["aeroshell"]]
    d_cap = 2 * max(float(x) for x in cad["capsulas"][forma]["r_m"])
    cruz = tuple(ref["pecas_do_estagio_de_cruzeiro"])
    configs = {"lançamento": corpos, "entrada (sem o estágio de cruzeiro)": [c for c in corpos if not c["nome"].startswith(cruz)]}
    out = {"gerado_por": "tools/cg_lateral.py", "diametro_capsula_m": d_cap, "configuracoes": {}}
    for nome, cs in configs.items():
        m, cg, T, contrib = propriedades(cs, dens)
        rad = math.hypot(cg[0], cg[1])
        grupos = agrupa(contrib)
        out["configuracoes"][nome] = {"massa_kg": m, "cg_m": cg.tolist(), "deslocamento_radial_m": rad, "radial_sobre_d": rad / d_cap,
                                      "produtos_kg_m2": {"Ixy": T[0][1], "Ixz": T[0][2], "Iyz": T[1][2]},
                                      "por_conjunto": grupos}
    out["msl"] = {"zcg_sobre_d": v(ref["msl_zcg_sobre_d"]), "deslocamento_radial_m": abs(v(ref["msl_zcg_sobre_d"])) * v(ref["msl_dref_m"]),
                  "trimagem_graus": v(ref["msl_trimagem_graus"]), "l_sobre_d": v(ref["msl_l_sobre_d"]),
                  "massas_balanco_entrada": [v(ref["msl_massas_balanco_entrada"]), ref["msl_massas_balanco_entrada"]["massa_cada_kg"]],
                  "massas_balanco_cruzeiro": [v(ref["msl_massas_balanco_cruzeiro"]), ref["msl_massas_balanco_cruzeiro"]["massa_cada_kg"]]}
    out = nativo(out)
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "cg_lateral.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    br = lambda x, n=3: f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    ms = o["msl"]
    md = ["# CG lateral e produtos de inércia do lander (gerado por tools/cg_lateral.py)", "",
          f"Modelo atual (results/etapa7.2/parametros.yaml). Diâmetro da cápsula no perfil lido: {br(o['diametro_capsula_m'], 2)} m. Nenhuma peça foi movida.", ""]
    for nome, c in o["configuracoes"].items():
        p = c["produtos_kg_m2"]
        md += [f"## Configuração de {nome}", "",
               f"Massa {br(c['massa_kg'], 1)} kg; CG ({br(c['cg_m'][0], 4)}; {br(c['cg_m'][1], 4)}; {br(c['cg_m'][2], 4)}) m; deslocamento radial "
               f"{br(c['deslocamento_radial_m'], 4)} m = {br(c['radial_sobre_d'], 4)} do diâmetro. Produtos de inércia: Ixy {br(p['Ixy'], 2)}, "
               f"Ixz {br(p['Ixz'], 2)}, Iyz {br(p['Iyz'], 2)} kg·m².", "",
               "| Conjunto | Massa (kg) | m·x (kg·m) | m·y (kg·m) | Contribuição ao CG x (m) | Contribuição ao CG y (m) | Ixy | Ixz | Iyz (kg·m²) |",
               "| :- | -: | -: | -: | -: | -: | -: | -: | -: |"]
        for x in c["por_conjunto"]:
            md.append(f"| {x['conjunto']} | {br(x['massa_kg'], 1)} | {br(x['mx_kg_m'], 2)} | {br(x['my_kg_m'], 2)} | {br(x['mx_kg_m'] / c['massa_kg'], 4)} | "
                      f"{br(x['my_kg_m'] / c['massa_kg'], 4)} | {br(x['Ixy'], 2)} | {br(x['Ixz'], 2)} | {br(x['Iyz'], 2)} |")
        md.append("")
    md += ["## Referência: MSL", "",
           f"- O MSL voou com deslocamento radial do CG intencional, zcg/d = {br(ms['zcg_sobre_d'], 4)} sobre dref = 4,5 m ([F226]), isto é, "
           f"{br(ms['deslocamento_radial_m'], 4)} m (calculado aqui), para trimar em cerca de {br(ms['trimagem_graus'], 0)}° de ângulo de ataque "
           f"hipersônico e gerar sustentação para a entrada guiada ([F226]), com L/D de {br(ms['l_sobre_d'], 2)} ([F227]).",
           f"- O deslocamento vinha de massas de balanço: {int(ms['massas_balanco_cruzeiro'][0])} de cerca de {ms['massas_balanco_cruzeiro'][1]} kg no "
           f"cruzeiro, ejetadas para criar o deslocamento, e {int(ms['massas_balanco_entrada'][0])} de cerca de {ms['massas_balanco_entrada'][1]} kg ejetadas "
           "antes do paraquedas para voltar o CG ao eixo ([F214]).",
           "- A sensibilidade da trimagem ao deslocamento do CG (graus por cm) não foi achada em texto legível nas fontes (não conferido); os valores do "
           "Mars 2020 também não (não conferido).", ""]
    (SAIDA / "cg_lateral.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
