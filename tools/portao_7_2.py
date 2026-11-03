"""Portão da Etapa 7.2: página de decisão de aeroshell e MAV (nenhuma escolha é feita aqui; a decisão é do Fabio).

- Tabela: aeroshell 4,5 m (forma MSL/M2020) × 4,65 m (forma SRL-A) × MAV de cada diâmetro, deitado e em pé, com a folga
  no Vulcan pelas duas leituras da Fig. 4.3.1-1 de [F80] (results/etapa7.2/parametros.yaml), a folga do MAV no aeroshell
  (results/etapa7.2/mav_arranjo.yaml) e a massa por área (results/etapa7.1/envelope.yaml), comparada com a do Mars 2020.
- Piso do comprimento do MAV: quanto vem dos tanques em série (P-085) e quanto vem do comprimento fora dos tanques (P-086).
- Opções bloqueadas: para cada caso, o maior comprimento fora dos tanques que ainda caberia, contra o da P-086.
- Referências publicadas para a P-086 (config/cad.yaml, referencias_p086).
Saída: results/etapa7.2/portao_decisao.yaml e .md

Uso: python tools/portao_7_2.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital import motores as om  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"
POL = 0.0254   # definição da polegada (m)
OPCOES = {"msl_m2020": ("m2020", "MSL/M2020"), "srl_a": ("srl_duplo", "SRL-A")}


def classifica(max_fora, p086):
    """Situação de um caso: cabe com a P-086, depende dela, ou não cabe nem sem nada fora dos tanques."""
    if max_fora >= p086:
        return "cabe"
    return "depende da P-086" if max_fora > 0 else "bloqueada pelos tanques"


def main():
    ma = ler("results/etapa7.2/mav_arranjo.yaml")
    par = ler("results/etapa7.2/parametros.yaml")["conferencias"]["lander_vulcan"]["por_forma"]
    env = ler("results/etapa7.1/envelope.yaml")["lander"]
    p086 = ma["comprimento_fora_dos_tanques_m"]
    cad = ler("config/cad.yaml")

    aero = {}
    for k, (op, rot) in OPCOES.items():
        e = env["opcoes_aeroshell"][op]
        rotulo = f"{e['diametro_m']:g} m (forma {rot})".replace(".", ",")
        aero[k] = {"rotulo": rotulo, "folga_vulcan_linear_m": par[k]["folga_radial_m"], "folga_vulcan_sem_afunilamento_m": par[k]["folga_sem_afunilamento_m"],
                   "massa_por_area_lander_kg_m2": e["massa_por_area_lander_kg_m2"]}
    m2020 = env["opcoes_aeroshell"]["m2020"]["massa_por_area_referencia_kg_m2"]
    srl_c = par["srl_c"]

    linhas = []
    for c in ma["casos"]:
        tanques = c["comprimento_m"] - p086
        for k in OPCOES:
            for es in c["formas"][k]:
                for orient, disp in (("deitado", c["comprimento_m"] + 2 * es["deitado_folga_m"]), ("em pé", es["em_pe_comprimento_disponivel_m"])):
                    folga = es["deitado_folga_m"] if orient == "deitado" else es["em_pe_folga_m"]
                    max_fora = disp - tanques
                    linhas.append({"forma": k, "diametro_m": c["diametro_m"], "comprimento_m": c["comprimento_m"], "tanques_m": tanques,
                                   "orientacao": orient, "estacao": es["estacao"], "estacao_base_m": es["estacao_base_m"], "folga_m": folga,
                                   "disponivel_m": disp, "max_fora_dos_tanques_m": max_fora, "situacao": classifica(max_fora, p086)})
    contagem = {}
    for li in linhas:
        ch = (li["forma"], li["orientacao"], li["situacao"])
        contagem[ch] = contagem.get(ch, 0) + 1
    # R-4D-11 de bocal 164:1 [F228]: comprimento total, diâmetro de saída e o menor círculo com 4 saídas em quadrado
    rd = cad["r4d11_164"]
    comp_r4d = (v(rd["flange_a_saida_pol"]) + v(rd["a_frente_da_flange_pol"])) * POL
    saida = v(rd["diametro_saida_pol"]) * POL
    r4d = {"comprimento_m": comp_r4d, "diametro_saida_m": saida, "diametro_min_4_saidas_m": saida * (1 + math.sqrt(2)),
           "massa_164_kg": v(rd["massa_164_kg"]), "massa_catalogo_kg": om.catalogo()["R-4D-11"]["massa_kg"],
           "p086_motores_estagio_1_m": v(cad["mav"]["comprimento_nao_tanque_m"]["motores_estagio_1"]),
           "p086_motor_estagio_2_m": v(cad["mav"]["comprimento_nao_tanque_m"]["motor_estagio_2"]),
           "diametro_mav_escolhido_m": v(cad["mav"]["diametro_opcoes_m"][cad["escolha"]["mav_diametro"]])}
    # análogos publicados, só pela geometria (mesma conta do MAV deitado e em pé, mesma folga interna)
    h_deck = ma["altura_deck_m"]
    analogos = []
    for an in cad["analogos_mav"]:
        for k in OPCOES:
            xs, rs = [float(x) for x in cad["capsulas"][k]["x_m"]], [float(x) for x in cad["capsulas"][k]["r_m"]]
            x0 = xs[int(np.argmax(rs))]
            for rot, xb in (("ombro", x0), ("ombro + deck (P-094)", x0 + h_deck)):
                r_in = lambda x: float(np.interp(x, xs, rs)) - ma["folga_interna_m"]  # noqa: E731
                analogos.append({"nome": an["nome"], "fonte": an["fonte"], "forma": k, "estacao": rot, "comprimento_m": an["comprimento_m"], "diametro_m": an["diametro_m"],
                                 "folga_deitado_m": r_in(xb + an["diametro_m"]) - an["comprimento_m"] / 2})
    ult = ma["casos"][-1]
    piso = {"comprimento_m": ult["comprimento_m"], "tanques_m": ult["comprimento_m"] - p086, "fora_dos_tanques_m": p086,
            "fracao_p086": p086 / ult["comprimento_m"], "diametro_saturacao_m": ma["diametro_saturacao_m"]}
    out = nativo({"gerado_por": "tools/portao_7_2.py", "aeroshell": aero, "m2020_massa_por_area_kg_m2": m2020, "srl_c": srl_c, "p086_m": p086,
                  "folga_interna_m": ma["folga_interna_m"], "piso": piso, "linhas": linhas,
                  "contagem": [{"forma": a, "orientacao": b, "situacao": s, "casos": n} for (a, b, s), n in contagem.items()],
                  "referencias_p086": cad["referencias_p086"], "r4d": r4d, "analogos": analogos})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "portao_decisao.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    br = lambda x, n=2: f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    sg = lambda x, n=2: f"{round(x, n) + 0.0:+,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    p, pi = o["p086_m"], o["piso"]
    ests = []
    for li in o["linhas"]:
        if li["estacao"] not in ests:
            ests.append(li["estacao"])
    md = ["# Portão da Etapa 7.2: dados para a decisão de aeroshell e MAV (gerado por tools/portao_7_2.py)", "",
          "Esta página não escolhe. A decisão é do Fabio.", "",
          "## 1. Comparação", "",
          f"Folga do MAV no aeroshell com a folga interna de {br(o['folga_interna_m'])} m (P-087) e a base em cada estação ({', '.join(ests)}). A massa por área do lander é "
          f"comparada com {br(o['m2020_massa_por_area_kg_m2'], 0)} kg/m² do Mars 2020 (3.360 kg de entrada em 4,5 m, [F202] p. 13; calculado).", "",
          "| Aeroshell | Folga no Vulcan, contorno reto entre as cotas | Folga no Vulcan, Ø menor desde o PAF | Massa por área (kg/m²) | Ø do MAV | Comprimento | "
          + " | ".join(f"Deitado, {e}" for e in ests) + " | " + " | ".join(f"Em pé, {e}" for e in ests) + " |",
          "| :- | -: | -: | -: | -: | -: |" + " -: |" * (2 * len(ests))]
    vistos = []
    for li in o["linhas"]:
        ch = (li["forma"], li["diametro_m"])
        if ch in vistos:
            continue
        vistos.append(ch)
        sel = [x for x in o["linhas"] if (x["forma"], x["diametro_m"]) == ch]
        col = [next(x for x in sel if x["orientacao"] == ori and x["estacao"] == e) for ori in ("deitado", "em pé") for e in ests]
        ae = o["aeroshell"][li["forma"]]
        md.append(f"| {ae['rotulo']} | {sg(ae['folga_vulcan_linear_m'], 3)} | {sg(ae['folga_vulcan_sem_afunilamento_m'], 3)} | {br(ae['massa_por_area_lander_kg_m2'], 0)} | "
                  f"{br(li['diametro_m'])} | {br(li['comprimento_m'])} | " + " | ".join(sg(x["folga_m"]) for x in col) + " |")
    md += ["", "Duas leituras do envelope do Vulcan, [F80] Fig. 4.3.1-1 (\"Simplified\"), p. 4-8: a primeira interpola em linha reta entre Ø 4.877 mm e Ø 4.648 mm; a segunda "
           f"usa Ø 4.648 mm desde o plano do PAF. Com a forma SRL-C, as folgas são {sg(o['srl_c']['folga_radial_m'], 3)} e {sg(o['srl_c']['folga_sem_afunilamento_m'], 3)} m. "
           "A massa por área usa os diâmetros nominais. Comprimentos e folgas em m; folga positiva = cabe.", "",
           "## 2. Piso do comprimento do MAV", "",
           f"**Confirmado:** com o arranjo atual (P-085), o comprimento para de cair em {br(pi['comprimento_m'])} m a partir de Ø {br(pi['diametro_saturacao_m'])} m.", "",
           f"**A origem é só em parte a P-086:** {br(pi['fora_dos_tanques_m'])} m ({br(100 * pi['fracao_p086'], 0)} %) vêm da P-086, sem fonte. Os outros "
           f"{br(pi['tanques_m'])} m vêm dos tanques em série, cujo volume sai das massas de propelente e das densidades (P-078, [F211]) com a ullage da P-081, na "
           "geometria da P-085.", "",
           "## 3. Opções que dependem da P-086", "",
           f"Para cada caso, o maior comprimento fora dos tanques que ainda caberia, contra os {br(p)} m da P-086.", "",
           "| Aeroshell | Orientação | Cabe hoje | Depende da P-086 | Bloqueada pelos tanques (não cabe nem com zero fora dos tanques) |", "| :- | :- | -: | -: | -: |"]
    cont = {(c["forma"], c["orientacao"], c["situacao"]): c["casos"] for c in o["contagem"]}
    for k, a in o["aeroshell"].items():
        for ori in ("deitado", "em pé"):
            md.append(f"| {a['rotulo']} | {ori} | {cont.get((k, ori, 'cabe'), 0)} | {cont.get((k, ori, 'depende da P-086'), 0)} | {cont.get((k, ori, 'bloqueada pelos tanques'), 0)} |")
    md += ["", "Maior comprimento fora dos tanques que caberia (m), por estação da base:", "",
           "| Aeroshell | Ø do MAV | Orientação | " + " | ".join(ests) + " |", "| :- | -: | :- |" + " -: |" * len(ests)]
    for ch in vistos:
        for ori in ("deitado", "em pé"):
            sel = [x for x in o["linhas"] if (x["forma"], x["diametro_m"]) == ch and x["orientacao"] == ori]
            md.append(f"| {o['aeroshell'][ch[0]]['rotulo']} | {br(ch[1])} | {ori} | " + " | ".join(br(next(x for x in sel if x["estacao"] == e)["max_fora_dos_tanques_m"]) for e in ests) + " |")
    r4 = o["r4d"]
    md += ["", "## 4. O que as fontes dizem sobre a P-086", "", "| Item | O que foi achado | Fonte |", "| :- | :- | :- |"]
    for r in o["referencias_p086"]:
        md.append(f"| {r['item']} | {r['achado']} | {r['fonte']} |")
    md += ["", f"**R-4D-11, bocal 164:1 (a variante do Isp que usamos), conta a partir de [F228]:** {br(r4['comprimento_m'], 3)} m de comprimento total, contra "
           f"{br(r4['p086_motores_estagio_1_m'])} m (estágio 1) e {br(r4['p086_motor_estagio_2_m'])} m (estágio 2) da P-086; saída de Ø {br(r4['diametro_saida_m'], 3)} m. "
           f"Quatro saídas em quadrado pedem um círculo de Ø {br(r4['diametro_min_4_saidas_m'], 3)} m (conta geométrica, saídas encostadas), contra o Ø {br(r4['diametro_mav_escolhido_m'])} m do ADR 0022. "
           "Bocais podem ficar fora do diâmetro do veículo ou aninhados; isso não está modelado.", "",
           f"**Achado à parte, sem mudança aqui:** a mesma folha dá {br(r4['massa_164_kg'])} kg para o bocal 164:1, e o catálogo (config/motores.yaml) usa "
           f"{br(r4['massa_catalogo_kg'])} kg, a massa do bocal 300:1, junto com o Isp do 164:1.", "",
           "**Análogos publicados, só pela geometria (não são o nosso MAV):**", "",
           "| MAV | Comprimento × Ø | Aeroshell | Base | Folga deitado | Fonte |", "| :- | :- | :- | :- | -: | :- |"]
    for a in o["analogos"]:
        md.append(f"| {a['nome']} | {br(a['comprimento_m'])} × {br(a['diametro_m'])} | {o['aeroshell'][a['forma']]['rotulo']} | {a['estacao']} | {sg(a['folga_deitado_m'])} | {a['fonte']} |")
    md += ["", "## 5. Opinião do agente (separada dos dados; não é fato nem recomendação como fato)", "",
           "Opinião: com o que está calculado, nenhuma combinação com base realista cabe sem mexer na P-086 ou no arranjo dos tanques, e o que mais pesa na decisão é "
           "essa premissa sem fonte, não o diâmetro. Eu calcularia um arranjo sem tanques em série antes de escolher o aeroshell, porque alargar o MAV não o encurta. "
           "A decisão é do Fabio."]
    (SAIDA / "portao_decisao.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
