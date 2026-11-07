"""MAV de propelente sólido para o nosso encontro (portão da rota A, Fabio, 2026-11-07; reabre o ADR 0007 sem alterá-lo).

Escala o MAV sólido de dois estágios do MSR de 2019 ([F34], [F247]) para o Δv de subida do ADR 0005, com a perda gravitacional
em dois limites para o Δv de 100 × 100 km: o de [F37] e o ideal, sem perdas. Comprimento por P-108; folga
deitado com e sem deck nos limites de results/etapa7.2/rota_a.yaml.
Saída: results/etapa7.2/mav_solido.yaml e .md

Uso: python tools/mav_solido.py
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import rota_a_dimensiona as rad  # noqa: E402
import subida_mav as sm  # noqa: E402
from orbital import subida as sb  # noqa: E402
from orbital import veiculos as ve  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"
br, sg = sm.br, sm.sg


def dimensiona(ctx, m, m2, ms, dv100):
    """MAV sólido dimensionado para o Δv de 100 × 100 km dado (composição do ADR 0005 e margem P-014)."""
    _, scfg, _, pl, _ = ctx
    s2 = copy.deepcopy(scfg)
    s2["subida"]["dv_100x100_km_s"]["valor"] = dv100 / 1000.0
    lan = ve.lander(m.R + m.h0p, m.R + m.h0a, mcfg=m2, scfg=s2, detalhe=True)
    e_ = lan["mav_estagios"]
    f = [fr * e["propelente_kg"] / mp for e, fr, mp in zip(e_, ms["empuxo_medio_n"]["valor"], ms["propelente_kg"]["valor"])]
    return lan, e_, f, f[0] / (e_[0]["massa_inicial_kg"] * pl.mu / pl.raio ** 2)


def main():
    ctx = sm.contexto()
    sc, _, _, pl, _ = ctx
    m = rad.modelo()
    ms = m.cad["mav_solido"]
    o1 = ler("config/mav_propulsao.yaml")["opcoes"]["O1"]
    mp_ref = ms["propelente_kg"]["valor"]
    d = v(ms["diametro_m"])
    m2 = copy.deepcopy(m.mcfg)
    m2["opcoes"][m.op] = {**m2["opcoes"][m.op], "isp_s": list(o1["isp_s"]), "fracao_estrutural": o1["fracao_estrutural"]}
    ref = sc["referencia"]
    casos = []
    for rot, dv100 in (("Δv de [F37], com perdas", v(ref["dv_100x100_m_s"])), ("Δv ideal, sem perdas (limite inferior)", sb.dv_ideal(pl, v(sc["alvo_altitude_m"])))):
        lan, e_, f, tw = dimensiona(ctx, m, m2, ms, dv100)
        mp = sum(e["propelente_kg"] for e in e_)
        comps = []
        for lf in ms["escala"]["comprimento_fixo_m"]["valor"]:
            L = lf + (v(ms["comprimento_m"]) - lf) * mp / sum(mp_ref)
            comps.append({"comprimento_fixo_m": lf, "comprimento_m": L, "folga_sem_deck_m": (m.lim_ombro[d] - L) / 2, "folga_com_deck_m": (m.lim_deck[d] - L) / 2})
        casos.append({"rotulo": rot, "dv_100x100_m_s": dv100, "dv_subida_com_margem_km_s": (1 + v(ler("config/dimensionamento.yaml")["margem_dv"])) * lan["dv_subida_mav_km_s"],
                      "glom_kg": e_[0]["massa_inicial_kg"], "propelente_kg": [e["propelente_kg"] for e in e_], "empuxos_n": f, "empuxo_peso": tw, "lander_injetado_kg": lan["injetada_kg"],
                      "razao_glom_msr": e_[0]["massa_inicial_kg"] / v(ms["glom_kg"]), "comprimentos": comps})
    out = nativo({"gerado_por": "tools/mav_solido.py", "status": "NÃO VALIDADO", "referencia_msr": {k: ms[k]["valor"] for k in ("glom_kg", "propelente_kg", "empuxo_medio_n", "tempo_queima_s", "isp_s", "comprimento_m", "diametro_m")},
                  "fracao_estrutural": v(o1["fracao_estrutural"]), "alvo_folga_m": m.alvo, "limites": {"sem_deck_m": m.lim_ombro[d], "com_deck_m": m.lim_deck[d]},
                  "casos": casos, "contra_no_adr_0007": ms["contra_no_adr_0007"]})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "mav_solido.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    r = o["referencia_msr"]
    todos = [c for x in o["casos"] for c in x["comprimentos"]]
    fecha = [c for c in todos if c["folga_sem_deck_m"] >= o["alvo_folga_m"]]
    md = ["# MAV de propelente sólido para o nosso encontro (gerado por tools/mav_solido.py)", "",
          "**NÃO VALIDADO.** Reabre o ADR 0007 só como dado; o ADR não muda. Escala do MAV sólido do MSR de 2019 (P-108).", "",
          "## Resposta", "",
          f"O MAV sólido fica entre **{br(min(x['glom_kg'] for x in o['casos']), 0)} e {br(max(x['glom_kg'] for x in o['casos']), 0)} kg** ({br(min(x['razao_glom_msr'] for x in o['casos']), 1)} a {br(max(x['razao_glom_msr'] for x in o['casos']), 1)} vezes o do MSR de 2019), com comprimento de {br(min(c['comprimento_m'] for c in todos), 2)} a {br(max(c['comprimento_m'] for c in todos), 2)} m em Ø {br(r['diametro_m'], 2)} m. "
          + (f"**Não cabe deitado, nem sem deck**, em nenhum caso: a melhor folga sem deck é {sg(max(c['folga_sem_deck_m'] for c in todos))} m." if not fecha else f"Cabe sem deck com folga ≥ {sg(o['alvo_folga_m'], 2)} m em {len(fecha)} de {len(todos)} casos."), "",
          "**A perda gravitacional do item 2 não foi aplicada ao sólido.** A simulação de subida corta a queima quando chega à energia da órbita, como um motor que desliga; o sólido não desliga, e o MSR usa queima, costa longa e queima do 2º estágio ([F57] PDF p. 2), que o modelo não tem. No lugar, há dois limites para o Δv de 100 × 100 km: o de [F37], com as perdas do caso de [F37], e o ideal, sem perdas (src/orbital/subida.py, dv_ideal). O empuxo/peso maior do sólido tende a reduzir a perda gravitacional; o arrasto, a aumentar.", "",
          "## MAV sólido do MSR de 2019 (fonte)", "", "| Grandeza | Estágio 1 | Estágio 2 |", "| :- | -: | -: |",
          f"| Propelente (kg) | {br(r['propelente_kg'][0], 1)} | {br(r['propelente_kg'][1], 1)} |", f"| Empuxo médio (N) | {br(r['empuxo_medio_n'][0], 0)} | {br(r['empuxo_medio_n'][1], 0)} |",
          f"| Tempo de queima (s) | {br(r['tempo_queima_s'][0], 1)} | {br(r['tempo_queima_s'][1], 1)} |", f"| Isp médio (s) | {br(r['isp_s'][0], 0)} | {br(r['isp_s'][1], 0)} |", "",
          f"GLOM {br(r['glom_kg'], 0)} kg, comprimento {br(r['comprimento_m'], 1)} m, diâmetro máximo {br(r['diametro_m'], 2)} m ([F34] PDF p. 4; [F247] PDF p. 2; [F248] PDF p. 4). O comprimento por estágio e a densidade do propelente não são publicados.", "",
          "## O nosso MAV sólido", "", "| Grandeza | " + " | ".join(x["rotulo"] for x in o["casos"]) + " |", "| :- |" + " -: |" * len(o["casos"])]
    for nome, f_ in (("Δv 100 × 100 km (m/s)", lambda x: br(x["dv_100x100_m_s"], 1)), ("Δv de subida com margem (km/s)", lambda x: br(x["dv_subida_com_margem_km_s"], 3)), ("GLOM (kg)", lambda x: br(x["glom_kg"], 1)),
                     ("Propelente, estágios 1 e 2 (kg)", lambda x: f"{br(x['propelente_kg'][0], 1)} e {br(x['propelente_kg'][1], 1)}"), ("Empuxo, estágios 1 e 2 (N, P-108)", lambda x: f"{br(x['empuxos_n'][0], 0)} e {br(x['empuxos_n'][1], 0)}"),
                     ("Empuxo/peso na decolagem", lambda x: br(x["empuxo_peso"], 2)), ("Lander injetado (kg)", lambda x: br(x["lander_injetado_kg"], 0))):
        md.append(f"| {nome} | " + " | ".join(f_(x) for x in o["casos"]) + " |")
    md += ["", f"Fração estrutural {br(o['fracao_estrutural'], 3)} (P-019), a do veículo inteiro de 2019.", "",
           "## Comprimento e folga deitado", "", f"Limites em Ø {br(r['diametro_m'], 2)} m: {br(o['limites']['sem_deck_m'], 3)} m sem deck e {br(o['limites']['com_deck_m'], 3)} m com deck.", "",
           "| Δv | Parte fixa (m, P-108) | Comprimento (m) | Folga sem deck (m) | Folga com deck (m) |", "| :- | -: | -: | -: | -: |"]
    md += [f"| {x['rotulo']} | {br(c['comprimento_fixo_m'], 1)} | {br(c['comprimento_m'], 2)} | {sg(c['folga_sem_deck_m'])} | {sg(c['folga_com_deck_m'])} |" for x in o["casos"] for c in x["comprimentos"]]
    md += ["", "## O que o ADR 0007 disse contra o sólido, e se ainda vale", "", "| Item | ADR 0007 | Hoje, com as fontes do MSR |", "| :- | :- | :- |"]
    md += [f"| {x['item']} | {x['adr']} | {x['hoje']} |" for x in o["contra_no_adr_0007"]]
    md += ["", "**Limitações:** escala linear de um único projeto; a fração estrutural de 0,286 é do veículo inteiro (P-019); sem simulação de subida própria do sólido."]
    (SAIDA / "mav_solido.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
