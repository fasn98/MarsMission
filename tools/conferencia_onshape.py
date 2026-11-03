"""Etapa 7.2: conferência do CAD no Onshape contra o modelo do script (VERIFICAÇÃO: o CAD reproduz o modelo; não é
validação do projeto).

- Medido: propriedades de massa que o Fabio leu no Onshape (tests/data/onshape/medicoes.yaml), nas unidades do Part
  Studio; convertidas para o SI (lb → kg por config/cad.yaml, onshape.lb_para_kg; mm → m pelo prefixo SI).
- Previsto: massa, CG, inércias no CG e volume calculados por tools/cad_parametros.py com a mesma geometria
  (results/etapa7.2/parametros.yaml).
- Veículos ainda não gerados no Onshape ficam como "aguardando medição".
Saída: results/etapa7.2/conferencia_onshape.yaml e .md

Uso: python tools/conferencia_onshape.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"
MM = 1e-3   # prefixo SI


def main():
    med = ler("tests/data/onshape/medicoes.yaml")
    prev = ler("results/etapa7.2/parametros.yaml")["resumo"]
    lb = v(ler("config/cad.yaml")["onshape"]["lb_para_kg"])
    out = {"gerado_por": "tools/conferencia_onshape.py", "natureza": "verificação: o CAD reproduz o modelo do script (não é validação)",
           "lb_para_kg": lb, "veiculos": {}}
    for k in ("orbitador", "lander", "mav"):
        m = med.get(k)
        p = prev[k]
        prevista = {"massa_kg": p["massa_kg"], "cg_m": p["cg_m"], "inercia_cg_kg_m2": [p["inercia_cg_kg_m2"][i][i] for i in range(3)],
                    "volume_m3": p["volume_m3"], "corpos": p["corpos"]}
        if m is None:
            out["veiculos"][k] = {"situacao": "aguardando medição", "previsto": prevista}
            continue
        assert m["unidades"] == {"massa": "lb", "comprimento": "mm"}, m["unidades"]
        medida = {"massa_kg": m["massa"] * lb, "cg_m": [x * MM for x in m["cg"]],
                  "inercia_cg_kg_m2": [m["inercia_no_cg"][e] * lb * MM ** 2 for e in ("Lxx", "Lyy", "Lzz")],
                  "volume_m3": m["volume"] * MM ** 3, "pecas": m["pecas"]}
        rel = lambda a, b: (a - b) / b  # noqa: E731
        desvio = {"massa_relativo": rel(medida["massa_kg"], prevista["massa_kg"]),
                  "cg_m": [a - b for a, b in zip(medida["cg_m"], prevista["cg_m"])],
                  "inercia_relativo": [rel(a, b) for a, b in zip(medida["inercia_cg_kg_m2"], prevista["inercia_cg_kg_m2"])],
                  "volume_relativo": rel(medida["volume_m3"], prevista["volume_m3"]),
                  "pecas": medida["pecas"] - prevista["corpos"]}
        out["veiculos"][k] = {"situacao": "conferido", "medicao": {x: m[x] for x in ("data", "responsavel", "versao_featurescript", "arquivo",
                                                                                   "compilou", "assign_materials", "eixos")},
                              "medido_onshape": medida, "previsto_script": prevista, "desvio": desvio}
    out = nativo(out)
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "conferencia_onshape.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    br = lambda x, n=3: f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    ex = lambda x: f"{x:+.1e}".replace(".", ",").replace("-", "−")  # noqa: E731
    md = ["# Conferência do CAD no Onshape (gerado por tools/conferencia_onshape.py)", "",
          "**VERIFICAÇÃO**: o CAD gerado no Onshape reproduz o modelo do script (mesma geometria e mesmas densidades). Não é validação do projeto "
          "nem comparação com o orçamento (Etapa 7.3).", "",
          f"Medido: propriedades de massa lidas no Onshape (tests/data/onshape/medicoes.yaml), convertidas com 1 lb = {o['lb_para_kg']} kg e 1 mm = 1e-3 m. "
          "Previsto: tools/cad_parametros.py (results/etapa7.2/parametros.yaml). Inércias no centro de massa, nos eixos do Part Studio.", ""]
    for k, x in o["veiculos"].items():
        md += [f"## {({'orbitador': 'Orbitador', 'lander': 'Lander', 'mav': 'MAV'})[k]}", ""]
        p = x["previsto"] if x["situacao"] != "conferido" else x["previsto_script"]
        if x["situacao"] != "conferido":
            md += [f"Aguardando medição. Previsto pelo script: massa {br(p['massa_kg'], 1)} kg; CG z {br(p['cg_m'][2])} m; "
                   "Ixx, Iyy, Izz = " + ", ".join(br(i, 2) for i in p["inercia_cg_kg_m2"]) + " kg·m²; " f"{p['corpos']} corpos.", ""]
            continue
        mm, d, mi = x["medido_onshape"], x["desvio"], x["medicao"]
        md += [f"Medição: {mi['responsavel']}, {mi['data']}, FeatureScript versão {mi['versao_featurescript']}, {mi['arquivo']}; compilou: "
               f"{'sim' if mi['compilou'] else 'não'}; Assign materials: {'sim' if mi['assign_materials'] else 'não'}.", "",
               "| Grandeza | Medido no Onshape | Previsto pelo script | Desvio |", "| :- | -: | -: | -: |",
               f"| Peças | {mm['pecas']} | {p['corpos']} | {d['pecas']} |",
               f"| Massa (kg) | {br(mm['massa_kg'])} | {br(p['massa_kg'])} | {ex(d['massa_relativo'])} (relativo) |"]
        for i, e in enumerate("xyz"):
            md.append(f"| CG {e} (m) | {br(mm['cg_m'][i], 4)} | {br(p['cg_m'][i], 4)} | {ex(d['cg_m'][i])} m |")
        for i, e in enumerate(("xx", "yy", "zz")):
            md.append(f"| I{e} no CG (kg·m²) | {br(mm['inercia_cg_kg_m2'][i], 2)} | {br(p['inercia_cg_kg_m2'][i], 2)} | {ex(d['inercia_relativo'][i])} (relativo) |")
        md += [f"| Volume (m³) | {br(mm['volume_m3'], 4)} | {br(p['volume_m3'], 4)} | {ex(d['volume_relativo'])} (relativo) |", "",
               "As inércias e o volume medidos têm 4 algarismos significativos (como o Onshape os mostrou); os desvios abaixo de ~1e-4 estão "
               "dentro dessa precisão de leitura. Os dados do FeatureScript vão com 6 algarismos significativos (tools/cad_parametros.py), o que "
               "explica desvios da ordem de 1e-6 na massa e no CG.", ""]
    (SAIDA / "conferencia_onshape.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
