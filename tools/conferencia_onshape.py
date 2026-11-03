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

import math
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
        res = m["resolucao"]
        meia = lambda x, alg: 0.5 * 10 ** (math.floor(math.log10(abs(x))) - alg + 1)  # noqa: E731   meia unidade do último algarismo
        medida = {"massa_kg": m["massa"] * lb, "cg_m": [x * MM for x in m["cg"]],
                  "inercia_cg_kg_m2": [m["inercia_no_cg"][e] * lb * MM ** 2 for e in ("Lxx", "Lyy", "Lzz")],
                  "volume_m3": m["volume"] * MM ** 3, "area_m2": m["area"] * MM ** 2, "pecas": m["pecas"]}
        # precisão de leitura (meia resolução do número mostrado, no SI) mais o arredondamento dos dados do FeatureScript
        # (6 algarismos significativos em tools/cad_parametros.py: meia unidade relativa = 5e-6)
        arred = 5e-6
        tol = {"massa_kg": 0.5 * res["massa"] * lb + arred * medida["massa_kg"],
               "cg_m": [0.5 * res["cg"] * MM + arred * abs(prevista["cg_m"][2]) for _ in range(3)],
               "inercia_cg_kg_m2": [meia(m["inercia_no_cg"][e], res["inercia_algarismos"]) * lb * MM ** 2 + arred * a
                                    for e, a in zip(("Lxx", "Lyy", "Lzz"), medida["inercia_cg_kg_m2"])],
               "volume_m3": meia(m["volume"], res["volume_algarismos"]) * MM ** 3 + arred * medida["volume_m3"]}
        dentro = {"massa_kg": abs(medida["massa_kg"] - prevista["massa_kg"]) <= tol["massa_kg"],
                  "cg_m": [abs(a - b) <= t for a, b, t in zip(medida["cg_m"], prevista["cg_m"], tol["cg_m"])],
                  "inercia_cg_kg_m2": [abs(a - b) <= t for a, b, t in zip(medida["inercia_cg_kg_m2"], prevista["inercia_cg_kg_m2"], tol["inercia_cg_kg_m2"])],
                  "volume_m3": abs(medida["volume_m3"] - prevista["volume_m3"]) <= tol["volume_m3"]}
        rel = lambda a, b: (a - b) / b  # noqa: E731
        desvio = {"massa_relativo": rel(medida["massa_kg"], prevista["massa_kg"]),
                  "cg_m": [a - b for a, b in zip(medida["cg_m"], prevista["cg_m"])],
                  "inercia_relativo": [rel(a, b) for a, b in zip(medida["inercia_cg_kg_m2"], prevista["inercia_cg_kg_m2"])],
                  "volume_relativo": rel(medida["volume_m3"], prevista["volume_m3"]),
                  "pecas": medida["pecas"] - prevista["corpos"]}
        pi = m.get("produtos_de_inercia")
        produtos = {"medido": pi if isinstance(pi, str) else [x * lb * MM ** 2 for x in pi],
                    "previsto_max_abs_kg_m2": max(abs(p["inercia_cg_kg_m2"][i][j]) for i in range(3) for j in range(3) if i != j)}
        out["veiculos"][k] = {"situacao": "conferido", "medicao": {x: m[x] for x in ("data", "responsavel", "versao_featurescript", "arquivo",
                                                                                   "compilou", "assign_materials", "eixos")},
                              "medido_onshape": medida, "previsto_script": prevista, "desvio": desvio,
                              "tolerancia_de_leitura": tol, "dentro_da_precisao_de_leitura": dentro, "produtos_de_inercia": produtos}
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
        mm, d, mi, dt = x["medido_onshape"], x["desvio"], x["medicao"], x["dentro_da_precisao_de_leitura"]
        ok = lambda b: "dentro" if b else "**fora**"  # noqa: E731
        md += [f"Medição: {mi['responsavel']}, {mi['data']}, FeatureScript versão {mi['versao_featurescript']}, {mi['arquivo']}; compilou: "
               f"{'sim' if mi['compilou'] else 'não'}; Assign materials: {'sim' if mi['assign_materials'] else 'não'}.", "",
               "| Grandeza | Medido no Onshape | Previsto pelo script | Desvio | Precisão de leitura |", "| :- | -: | -: | -: | :- |",
               f"| Peças | {mm['pecas']} | {p['corpos']} | {d['pecas']} | — |",
               f"| Massa (kg) | {br(mm['massa_kg'])} | {br(p['massa_kg'])} | {ex(d['massa_relativo'])} (relativo) | {ok(dt['massa_kg'])} |"]
        for i, e in enumerate("xyz"):
            md.append(f"| CG {e} (m) | {br(mm['cg_m'][i], 4)} | {br(p['cg_m'][i], 4)} | {ex(d['cg_m'][i])} m | {ok(dt['cg_m'][i])} |")
        for i, e in enumerate(("xx", "yy", "zz")):
            md.append(f"| I{e} no CG (kg·m²) | {br(mm['inercia_cg_kg_m2'][i], 2)} | {br(p['inercia_cg_kg_m2'][i], 2)} | {ex(d['inercia_relativo'][i])} (relativo) | "
                      f"{ok(dt['inercia_cg_kg_m2'][i])} |")
        pr = x["produtos_de_inercia"]
        pm = pr["medido"] if isinstance(pr["medido"], str) else ", ".join(br(v_, 2) for v_ in pr["medido"]) + " kg·m²"
        md += [f"| Volume (m³) | {br(mm['volume_m3'], 4)} | {br(p['volume_m3'], 4)} | {ex(d['volume_relativo'])} (relativo) | {ok(dt['volume_m3'])} |",
               f"| Produtos de inércia | {pm} | maior valor absoluto {ex(pr['previsto_max_abs_kg_m2'])} kg·m² | — | — |",
               f"| Área (m²) | {br(mm['area_m2'], 2)} | não calculada pelo script | — | — |", "",
               "Precisão de leitura: meia unidade do último algarismo que o Onshape mostrou (tests/data/onshape/medicoes.yaml, resolucao) mais o "
               "arredondamento dos dados do FeatureScript a 6 algarismos significativos (tools/cad_parametros.py).", ""]
    (SAIDA / "conferencia_onshape.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
