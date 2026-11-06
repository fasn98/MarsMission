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
sys.path.insert(0, str(RAIZ / "tools"))

from conferencia_onshape import _bloco  # noqa: E402
from orbital import motores as om  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"
POL = 0.0254   # [F112] Apêndice B.8, PDF p. 62: polegada em metros
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
    med = ler("tests/data/onshape/medicoes.yaml")

    aero = {}
    for k, (op, rot) in OPCOES.items():
        e = env["opcoes_aeroshell"][op]
        rotulo = f"{e['diametro_m']:g} m (forma {rot})".replace(".", ",")
        aero[k] = {"rotulo": rotulo, "folga_vulcan_linear_m": par[k]["folga_radial_m"], "folga_vulcan_sem_afunilamento_m": par[k]["folga_sem_afunilamento_m"],
                   "folga_vulcan_linear_vertice_m": par[k]["folga_radial_vertice_m"], "folga_vulcan_sem_afunilamento_vertice_m": par[k]["folga_sem_afunilamento_vertice_m"],
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
    # R-4D-11 por variante [F228]: comprimento total e diâmetro de saída
    rd = cad["r4d11_variantes"]
    frente = v(rd["a_frente_da_flange_pol"])
    variantes = {k: {"comprimento_m": (rd[k]["flange_a_saida_pol"] + frente) * POL, "diametro_saida_m": rd[k]["diametro_saida_pol"] * POL,
                     "isp_s": rd[k].get("isp_s"), "massa_kg": rd[k].get("massa_kg"), "fonte": rd[k]["fonte"]} for k in ("44:1", "164:1", "300:1")}
    d_mav = v(cad["mav"]["diametro_opcoes_m"][cad["escolha"]["mav_diametro"]])
    # empacotamento: menor círculo que contém n círculos de diâmetro d (n = 1 a 4)
    fator = {1: 1.0, 2: 2.0, 3: 1 + 2 / math.sqrt(3), 4: 1 + math.sqrt(2)}
    s0 = variantes["164:1"]["diametro_saida_m"]
    bocais = {"diametro_saida_m": s0, "diametro_mav_m": d_mav, "fator_por_n": fator,
              "minimo_por_n_m": {n: f * s0 for n, f in fator.items()}, "cabe_por_n": {n: f * s0 <= d_mav for n, f in fator.items()},
              "minimo_4_por_variante_m": {k: fator[4] * x["diametro_saida_m"] for k, x in variantes.items()},
              "menor_diametro_da_varredura_que_contem_4_m": min((c["diametro_m"] for c in ma["casos"] if c["diametro_m"] >= fator[4] * s0), default=None)}
    # como os motores foram modelados no arquivo compilado (32cb41d)
    compilado = _bloco((RAIZ / med["mav"]["arquivo"]).read_text(encoding="utf-8"), "CORPOS")
    modelo = []
    for b in compilado:
        if b["nome"].startswith(("MAV motores", "MAV motor")):
            h = math.dist(b["p0"], b["p1"])
            modelo.append({"nome": b["nome"], "tipo": b["tipo"], "diametro_m": 2 * b["r"], "comprimento_m": h, "densidade_kg_m3": b["densidade"]})
    # catálogo: o que usa hoje, por grandeza
    cat = om.catalogo()["R-4D-11"]
    pc = cad["mav"]["comprimento_nao_tanque_m"]
    combos = ler("config/motores.yaml")
    n_motores = {f: sum(q["quantidade"] for q in next(c for g in combos["combinacoes"].values() for k_, c in g.items() if k_ == nome)["motores"] if q["motor"] == "R-4D-11")
                 for f, nome in combos["escolha"].items() if f in ("captura", "retorno", "mav_1", "mav_2")}
    r4d = {"variantes": variantes, "catalogo_isp_s": cat["isp_s"], "catalogo_massa_kg": cat["massa_kg"],
           "p086_motores_estagio_1_m": v(pc["motores_estagio_1"]), "p086_motor_estagio_2_m": v(pc["motor_estagio_2"]), "n_motores": n_motores,
           "diferenca_massa_por_motor_kg": cat["massa_kg"] - variantes["164:1"]["massa_kg"],
           "diferenca_massa_total_kg": (cat["massa_kg"] - variantes["164:1"]["massa_kg"]) * sum(n_motores.values()),
           "diferenca_massa_mav_kg": (cat["massa_kg"] - variantes["164:1"]["massa_kg"]) * (n_motores["mav_1"] + n_motores["mav_2"]),
           "falta_no_estagio_2_m": variantes["164:1"]["comprimento_m"] - v(pc["motor_estagio_2"]),
           "sobra_no_estagio_1_m": v(pc["motores_estagio_1"]) - variantes["164:1"]["comprimento_m"]}
    # nosso MAV, para a tabela lado a lado com o de Bowles
    mav_arq = ler("results/etapa2.5/arquitetura.yaml")["lander"]["mav"]
    res = ler("results/etapa7.2/parametros.yaml")["resumo"]["mav"]
    nosso = {"estagios": len(mav_arq["estagios"]), "dv_m_s": 1e3 * mav_arq["dv_com_margem_km_s"], "carga_kg": v(ler("config/superficie.yaml")["mav"]["carga_util_kg"]),
             "propelente_kg": sum(e["propelente_kg"] for e in mav_arq["estagios"]), "glom_orcamento_kg": mav_arq["estagios"][0]["massa_inicial_kg"],
             "massa_cad_kg": res["massa_kg"], "n_motores": [n_motores["mav_1"], n_motores["mav_2"]], "diametro_m": d_mav,
             "comprimento_m": next(c["comprimento_m"] for c in ma["casos"] if c["diametro_m"] == d_mav)}
    # análogos publicados, só pela geometria (mesma conta do MAV deitado, mesma folga interna)
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
    out = nativo({"gerado_por": "tools/portao_7_2.py", "aeroshell": aero, "m2020_massa_por_area_kg_m2": m2020,
                  "m2020": {"massa_entrada_kg": v(cad["aeroshell"]["opcoes"]["m2020"]["massa_entrada_kg"]), "diametro_m": v(cad["aeroshell"]["opcoes"]["m2020"]["diametro_m"])},
                  "vulcan_diametros_mm": cad["coifas"]["vulcan_15_5"]["perfil"]["diametro_mm"][:2], "srl_c": srl_c, "p086_m": p086,
                  "folga_interna_m": ma["folga_interna_m"], "piso": piso, "linhas": linhas,
                  "contagem": [{"forma": a, "orientacao": b, "situacao": s, "casos": n} for (a, b, s), n in contagem.items()],
                  "referencias_p086": cad["referencias_p086"], "r4d": r4d, "bocais": bocais, "modelo_motores_compilado": modelo, "nosso_mav": nosso,
                  "bowles": cad["comparacao_bowles"], "analogos": analogos})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "portao_decisao.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    br = lambda x, n=2: f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    # uma casa a mais quando o arredondamento apagaria o sinal
    sg = lambda x, n=2: f"{round(x, n + (x != 0 and round(x, n) == 0)) + 0.0:+,.{n + (x != 0 and round(x, n) == 0)}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    p, pi = o["p086_m"], o["piso"]
    ests = []
    for li in o["linhas"]:
        if li["estacao"] not in ests:
            ests.append(li["estacao"])
    md = ["# Portão da Etapa 7.2: dados para a decisão de aeroshell e MAV (gerado por tools/portao_7_2.py)", "",
          "Esta página não escolhe. A decisão é do Fabio.", "",
          "## 1. Comparação", "",
          f"Folga do MAV no aeroshell com a folga interna de {br(o['folga_interna_m'])} m (P-087) e a base em cada estação ({', '.join(ests)}). A massa por área do lander é "
          f"comparada com {br(o['m2020_massa_por_area_kg_m2'], 0)} kg/m² do Mars 2020 ({br(o['m2020']['massa_entrada_kg'], 0)} kg de entrada em {br(o['m2020']['diametro_m'], 1)} m, [F202] p. 13; calculado).", "",
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
    md += ["", f"Duas leituras do envelope do Vulcan, [F80] Fig. 4.3.1-1 (\"Simplified\"), p. 4-8: a primeira interpola em linha reta entre Ø {o['vulcan_diametros_mm'][0]} mm e Ø {o['vulcan_diametros_mm'][1]} mm; a segunda "
           f"usa Ø {o['vulcan_diametros_mm'][1]} mm desde o plano do PAF. Com a forma SRL-C, as folgas são {sg(o['srl_c']['folga_radial_m'], 3)} e {sg(o['srl_c']['folga_sem_afunilamento_m'], 3)} m. "
           "A massa por área usa os diâmetros nominais. Comprimentos e folgas em m; folga positiva = cabe.", "",
           "**Errata (2026-11-04, aprovada pelo Fabio):** as folgas no Vulcan da tabela acima valem um pouco menos. A conta amostrou o perfil em 400 pontos, e nenhum caiu no vértice do ombro. Os valores vigentes são os dos vértices; os antigos ficam como registro.", "",
           "| Aeroshell | Leitura do envelope | Publicado | Vigente |", "| :- | :- | -: | -: |"]
    for k_ in o["aeroshell"]:
        ae = o["aeroshell"][k_]
        md.append(f"| {ae['rotulo']} | contorno reto | {sg(ae['folga_vulcan_linear_m'], 4)} | {sg(ae['folga_vulcan_linear_vertice_m'], 4)} |")
        md.append(f"| {ae['rotulo']} | Ø menor desde o PAF | {sg(ae['folga_vulcan_sem_afunilamento_m'], 4)} | {sg(ae['folga_vulcan_sem_afunilamento_vertice_m'], 4)} |")
    md += ["", f"SRL-C, publicado e vigente: {sg(o['srl_c']['folga_radial_m'], 4)} e {sg(o['srl_c']['folga_radial_vertice_m'], 4)} m (contorno reto); {sg(o['srl_c']['folga_sem_afunilamento_m'], 4)} e {sg(o['srl_c']['folga_sem_afunilamento_vertice_m'], 4)} m (Ø menor).", "",
           "**Nota (2026-11-06):** a massa do MAV no CAD vem agora dos arquivos com 12 algarismos; a mudança, abaixo da casa mostrada nesta página, está em results/etapa7.2b/folgas.md.", "",
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
            md.append(f"| {o['aeroshell'][ch[0]]['rotulo']} | {br(ch[1])} | {ori} | " + " | ".join(br(next(x for x in sel if x["estacao"] == e)["max_fora_dos_tanques_m"], 3) for e in ests) + " |")
    r4, bc, no, bw = o["r4d"], o["bocais"], o["nosso_mav"], o["bowles"]
    bw_c = next(a["comprimento_m"] for a in o["analogos"] if "Bowles" in a["nome"])
    md.append("")
    md += ["## 4. O que as fontes dizem sobre a P-086", "", "| Item | O que foi achado | Fonte |", "| :- | :- | :- |"]
    for r in o["referencias_p086"]:
        md.append(f"| {r['item']} | {r['achado']} | {r['fonte']} |")
    md += ["", "**Análogos publicados, só pela geometria (não são o nosso MAV):**", "",
           "| MAV | Comprimento × Ø | Aeroshell | Base | Folga deitado | Fonte |", "| :- | :- | :- | :- | -: | :- |"]
    for a in o["analogos"]:
        md.append(f"| {a['nome']} | {br(a['comprimento_m'])} × {br(a['diametro_m'])} | {o['aeroshell'][a['forma']]['rotulo']} | {a['estacao']} | {sg(a['folga_deitado_m'])} | {a['fonte']} |")
    # ---- achado 1: Bowles × nosso MAV
    md += ["", "## 5. Achado: o MAV de Bowles ao lado do nosso", "",
           "| Grandeza | Bowles, conceito pressurizado de 20 kg | Fonte | Nosso MAV | Origem |", "| :- | :- | :- | :- | :- |",
           f"| Estágios | {bw['estagios']['valor']} | {bw['estagios']['fonte']} | {no['estagios']} | results/etapa2.5/arquitetura.yaml |",
           f"| Δv | {bw['dv']['valor']} | {bw['dv']['fonte']} | {br(no['dv_m_s'], 0)} m/s, com margem | results/etapa2.5/arquitetura.yaml |",
           f"| Carga útil | {bw['carga']['valor']} | {bw['carga']['fonte']} | {br(no['carga_kg'], 0)} kg | [F34] p. 4 |",
           f"| Propelente | {bw['propelente']['valor']} | {bw['propelente']['fonte']} | {br(no['propelente_kg'], 1)} kg, MMH/MON-3 | results/etapa2.5/arquitetura.yaml |",
           f"| Motores | {bw['motores']['valor']} | {bw['motores']['fonte']} | {no['n_motores'][0]} + {no['n_motores'][1]} R-4D-11 | config/motores.yaml (M2, N2) |",
           f"| Razão de expansão | {bw['expansao']['valor']} | {bw['expansao']['fonte']} | 164:1 no Isp; ver a seção 7 | [F107] p. 5 |",
           f"| Alimentação | {bw['alimentacao']['valor']} | {bw['alimentacao']['fonte']} | pressurizada | ADR 0007, config/mav_propulsao.yaml |",
           f"| Tanques | {bw['tanques']['valor']} | {bw['tanques']['fonte']} | em série | results/etapa7.2/mav_arranjo.md |",
           f"| Dimensões e massa | {bw['dimensoes']['valor']} | {bw['dimensoes']['fonte']} | {br(no['comprimento_m'])} m × {br(no['diametro_m'])} m; {br(no['glom_orcamento_kg'], 1)} kg no orçamento, {br(no['massa_cad_kg'], 1)} kg no CAD | results/etapa7.2 |",
           "", "**A comparação não é de veículos equivalentes:**",
           "- o de Bowles tem um estágio, então não tem interestágio nem segundo motor, que no nosso somam parte da P-086;",
           f"- o Δv dele é menor ({bw['dv']['valor']} contra {br(no['dv_m_s'], 0)} m/s, e não conferimos se as margens são iguais), embora a massa de propelente seja da mesma ordem;",
           "- os tanques do estudo dele são aninhados, para encurtar o veículo, e os nossos estão em série;",
           "- a carga, o motor e a origem dos números também diferem, e não achamos a razão de expansão dele.", "",
           f"**O que os dados permitem afirmar:** existe um conceito publicado, hipergólico e pressurizado, com massa de propelente da mesma ordem e {br(bw_c)} m. **O que não permitem:** "
           f"dizer que o nosso MAV caberia nesse comprimento, ou que o piso de {br(pi['comprimento_m'])} m está errado. O piso é o resultado do nosso arranjo (dois estágios em série e a P-086).", "",
           "## 6. Achado: bocais do estágio 1 no diâmetro do MAV", "",
           f"Saída do R-4D-11 de bocal 164:1: {br(bc['diametro_saida_m'], 3)} m ([F228], {br(bc['diametro_saida_m'] / POL, 1)} pol). Menor círculo que contém n saídas, contra o Ø {br(bc['diametro_mav_m'])} m do ADR 0022:", "",
           "| Saídas | Fator sobre o diâmetro de saída | Círculo mínimo (m) | Cabe em Ø do MAV? |", "| -: | :- | -: | :- |"]
    nomes_f = {1: "1", 2: "2", 3: "1 + 2/√3", 4: "1 + √2"}
    for n, x in bc["minimo_por_n_m"].items():
        md.append(f"| {n} | {nomes_f[n]} = {br(bc['fator_por_n'][n], 3)} | {br(x, 3)} | {'sim' if bc['cabe_por_n'][n] else 'não'} |")
    minv = bc["minimo_4_por_variante_m"]
    md += ["", "**Conta para 4 saídas, em qualquer arranjo:** se nenhum centro está no eixo, dois centros vizinhos ficam a no máximo 90° vistos do eixo, logo a no máximo R√2 um do outro, com R o "
           "maior raio entre os centros. Eles precisam estar a pelo menos d um do outro, então R ≥ d/√2, e o círculo total é 2R + d ≥ d(1 + √2). Com um centro no eixo, os outros "
           "três ficam a pelo menos d dele, e o círculo é ≥ 3d, pior.", "",
           f"**Resultado: 4 bocais de saída 164:1 não cabem em Ø {br(bc['diametro_mav_m'])} m em nenhum arranjo.** O mínimo é {br(minv['164:1'], 3)} m, sem folga entre eles e sem parede. "
           f"Na varredura, o primeiro diâmetro que os contém é {br(bc['menor_diametro_da_varredura_que_contem_4_m'])} m. Com outras variantes: {br(minv['44:1'], 3)} m (44:1) e {br(minv['300:1'], 3)} m (300:1).", "",
           "**Hipótese da conta:** as saídas não se sobrepõem vistas ao longo do eixo e ficam dentro do diâmetro. Saídas escalonadas no eixo, ou bocais que passem do diâmetro do corpo, não foram calculadas; "
           "o R-4D-11 de 44:1 cabe na conta, mas a folha não dá o Isp nem a massa dele.", "",
           "**Como o modelo compilado (32cb41d) representa os motores:**", "",
           "| Peça | Forma | Ø (m) | Comprimento (m) | Densidade equivalente (kg/m³) |", "| :- | :- | -: | -: | -: |"]
    for m_ in o["modelo_motores_compilado"]:
        md.append(f"| {m_['nome']} | {m_['tipo']} maciço | {br(m_['diametro_m'], 3)} | {br(m_['comprimento_m'])} | {br(m_['densidade_kg_m3'], 1)} |")
    md += ["", "**A peça é um volume simplificado, não os bocais reais.** O cilindro cabe no diâmetro por construção. **O modelo do Onshape esconde essa interferência**: a compilação e a "
           "conferência de massa não a mostram. As folgas do MAV no aeroshell da seção 1 também não consideram os bocais, porque usam o Ø do corpo.", "",
           f"**Ligação com o MSR:** a fonte cita \"the small clearances of the interstage hardware and the nested SRM2 nozzle\" ([F35] PDF p. 15). O bocal de um 2º estágio aninhado reduz comprimento, e o "
           f"nosso motor do estágio 2 só cabe nos {br(r4['p086_motor_estagio_2_m'])} m da P-086 se entrar ao menos {br(r4['falta_no_estagio_2_m'], 3)} m em outro elemento. Isso não resolve o diâmetro: o aninhamento é no 2º estágio, "
           "e o achado é no 1º (inferência, NÃO VALIDADO; o MSR usa motor sólido).", "",
           "## 7. Achado: variantes do R-4D-11 misturadas no catálogo", "",
           "| Variante | Isp (s) | Massa (kg) | Comprimento total (m) | Ø de saída (m) | Fonte |", "| :- | -: | -: | -: | -: | :- |"]
    for k, x in r4["variantes"].items():
        md.append(f"| {k} | {br(x['isp_s'], 1) if x['isp_s'] else 'não dado'} | {br(x['massa_kg']) if x['massa_kg'] else 'não dado'} | {br(x['comprimento_m'], 3)} | {br(x['diametro_saida_m'], 3)} | {x['fonte']} |")
    n_m = r4["n_motores"]
    md += ["", "| Grandeza | O que o estudo usa hoje | Variante | Fonte |", "| :- | :- | :- | :- |",
           f"| Isp | {br(r4['catalogo_isp_s'], 0)} s | 164:1 (Orion, requisito do Artemis I) | [F107] p. 6, Tab. 3; variante em p. 5 |",
           f"| Massa | {br(r4['catalogo_massa_kg'])} kg | 300:1, pela massa e pelo Isp de 315 s da mesma ficha ([F228]); a ficha não diz a variante | [F106] p. 3, em lb |",
           f"| Comprimento | {br(r4['p086_motores_estagio_1_m'])} m (estágio 1), {br(r4['p086_motor_estagio_2_m'])} m (estágio 2) | nenhuma: premissa sem fonte; o 164:1 tem {br(r4['variantes']['164:1']['comprimento_m'], 3)} m | P-086 |",
           "| Diâmetro de saída | não entra no modelo | — | ver a seção 6 |", "",
           f"**Misturas:** o Isp é do 164:1, e a massa coincide com a do 300:1 (inferência pelo valor e pelo Isp da ficha, que não diz a variante; NÃO VALIDADO). A diferença é de {br(r4['diferenca_massa_por_motor_kg'])} kg por motor, {br(r4['diferenca_massa_total_kg'], 1)} kg nos "
           f"{sum(n_m.values())} motores escolhidos (captura {n_m['captura']}, retorno {n_m['retorno']}, MAV {n_m['mav_1']} + {n_m['mav_2']}). A massa do catálogo entra no CAD do MAV "
           f"({br(r4['diferenca_massa_mav_kg'], 1)} kg de diferença), e portanto no CAD do lander que o leva, no CG lateral (results/etapa7.2/cg_lateral.md, repetido em docs/etapa7.3_portao_perguntas.md) e no modelo "
           "comparado com o Onshape. Também é um campo sem leitor em results/etapa3.1/queima_finita.yaml. Os estágios usam fração estrutural, então a cadeia de massa não depende dela (conferido por busca no código).", "",
           f"**Outras diferenças:** o motor 164:1 mede {br(r4['variantes']['164:1']['comprimento_m'], 3)} m, mais que os {br(r4['p086_motor_estagio_2_m'])} m do estágio 2 e {br(r4['sobra_no_estagio_1_m'], 3)} m menos que os "
           f"{br(r4['p086_motores_estagio_1_m'])} m do estágio 1. O Isp do 164:1 é {br(r4['catalogo_isp_s'], 0)} s como requisito do Orion [F107] e {br(r4['variantes']['164:1']['isp_s'], 0)} s na folha [F228]. "
           "Não conferido: se o 164:1 da folha é o mesmo motor \"modified\" do Orion [F107].", "",
           "**Para decidir (Fabio), sem nenhuma troca feita:**", "",
           "| Opção | Massa e Isp | Prós | Contras |", "| :- | :- | :- | :- |",
           f"| (a) 164:1 em tudo | {br(r4['variantes']['164:1']['massa_kg'])} kg [F228], {br(r4['catalogo_isp_s'], 0)} s [F107] | variante única, a do Isp escolhido no ADR 0011; a cadeia de massa não muda | mudam o CAD do MAV e do lander, o CG lateral e o campo da queima finita; pede gerar e conferir de novo o lander e o MAV no Onshape, e errata |",
           f"| (b) 300:1 em tudo | {br(r4['variantes']['300:1']['massa_kg'])} kg, {br(r4['variantes']['300:1']['isp_s'], 1)} s [F228] | variante única, com mais Isp | muda o Isp e reabre o ADR 0011; bocal maior ({br(minv['300:1'], 3)} m para 4 saídas); sem o voo no Orion |",
           "| (c) manter e registrar a limitação | sem mudança | nenhum resultado muda | a mistura continua, pequena na massa |", "",
           "## 8. Opinião do agente (separada dos dados; não é fato nem recomendação como fato)", "",
           f"Opinião: com o que está calculado, só {sum(x['situacao'] == 'cabe' for x in o['linhas'])} casos cabem, todos com a base no ombro, e não conferi se o deck permite isso. Os demais dependem da P-086 ou do arranjo dos tanques, e o que mais pesa na decisão é "
           f"essa premissa sem fonte, não o diâmetro. Além disso, a seção 6 pesa contra o Ø {br(bc['diametro_mav_m'])} m com quatro motores no estágio 1. Eu calcularia um arranjo sem tanques em série antes de "
           "escolher o aeroshell. A decisão é do Fabio."]
    (SAIDA / "portao_decisao.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
