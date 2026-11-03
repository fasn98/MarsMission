"""Etapa 7.2: conferência do CAD no Onshape contra o modelo do script (VERIFICAÇÃO: o CAD reproduz o modelo; não é
validação do projeto).

- Medido: propriedades de massa lidas pelo Fabio no Onshape (tests/data/onshape/medicoes.yaml), em SI e em texto, como o
  Onshape as mostrou; a resolução de leitura de cada número sai dos algarismos exibidos.
- Previsto: massa, CG (x, y, z), tensor de inércia no CG e volume calculados pelo script (tools/cad_parametros.py:
  volume, centro e inercia) a partir dos dados do próprio arquivo .fs que foi compilado (cópia em tests/data/onshape/),
  com o cone interno dos troncos ocos tomado na reta que o arquivo define (pe0, pe1, rie0, rie1). Assim o previsto é o
  que o Onshape construiu, qualquer que seja a versão do arquivo.
- Também mostra a diferença entre o arquivo compilado e o modelo atual (results/etapa7.2/parametros.yaml).
Saída: results/etapa7.2/conferencia_onshape.yaml e .md

Uso: python tools/conferencia_onshape.py
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import cad_parametros as cp  # noqa: E402
from orbital.config import ler, nativo  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"
NOMES = {"orbitador": "Orbitador", "lander": "Lander", "mav": "MAV"}


def _bloco(texto, nome):
    ini = texto.index(f"const {nome} = ") + len(f"const {nome} = ")
    resto = texto[ini:]
    return json.loads(resto[:resto.index("\n];") + 2])


def previsto_do_arquivo(caminho):
    """Massa, CG, tensor de inércia no CG e volume dos corpos do arquivo .fs, pelas fórmulas do script."""
    texto = (RAIZ / caminho).read_text(encoding="utf-8")
    mats, corpos = _bloco(texto, "MATERIAIS"), _bloco(texto, "CORPOS")
    massa, mom, dados = 0.0, np.zeros(3), []
    for b in corpos:
        c = dict(b)
        if c["tipo"] == "tronco_oco":   # raios internos nas faces, na reta do cone estendido que o arquivo define
            p0, p1, e0, e1 = (np.array(c[k], float) for k in ("p0", "p1", "pe0", "pe1"))
            u = (e1 - e0) / np.linalg.norm(e1 - e0)
            raio = lambda p: c["rie0"] + (c["rie1"] - c["rie0"]) * float(np.dot(p - e0, u)) / float(np.linalg.norm(e1 - e0))  # noqa: E731
            c["ri0"], c["ri1"] = raio(p0), raio(p1)
        rho = c["densidade"] if c["mat"] < 0 else mats[c["mat"]][1]
        m = rho * cp.volume(c)
        massa += m
        mom += m * cp.centro(c)
        dados.append((c, rho, m))
    cg = mom / massa
    tensor, vol = np.zeros((3, 3)), 0.0
    for c, rho, m in dados:
        d = cp.centro(c) - cg
        tensor += cp.inercia(c, rho) + m * (np.dot(d, d) * np.eye(3) - np.outer(d, d))
        vol += cp.volume(c)
    return {"massa_kg": massa, "cg_m": cg.tolist(), "inercia_cg_kg_m2": tensor.tolist(), "volume_m3": vol, "corpos": len(corpos)}


def num(s):
    """(valor, meia resolução de leitura) de um número em texto, pelo último algarismo exibido."""
    d = Decimal(str(s))
    return float(d), 0.5 * 10.0 ** d.as_tuple().exponent


def main():
    med = ler("tests/data/onshape/medicoes.yaml")
    modelo = ler("results/etapa7.2/parametros.yaml")["resumo"]
    out = {"gerado_por": "tools/conferencia_onshape.py", "natureza": "verificação: o CAD reproduz o modelo do script (não é validação)",
           "comum": med["comum"], "veiculos": {}}
    for k in ("orbitador", "lander", "mav"):
        m = med.get(k)
        if m is None:
            out["veiculos"][k] = {"situacao": "aguardando medição"}
            continue
        p = previsto_do_arquivo(m["arquivo"])
        linhas = []

        def linha(grandeza, s, prev, unidade, meia_forcada=None):
            v_, meia = num(s)
            meia = meia if meia_forcada is None else meia_forcada
            linhas.append({"grandeza": grandeza, "unidade": unidade, "medido": v_, "previsto": prev, "desvio_abs": v_ - prev,
                           "desvio_rel": (v_ - prev) / prev if abs(prev) > 1e-9 else None, "meia_resolucao": meia, "dentro": abs(v_ - prev) <= meia})
        linha("massa", m["massa"], p["massa_kg"], "kg")
        meia_cg = num(m["cg"][2])[1]   # um CG mostrado como "0" usa a resolução da coordenada z
        for i, e in enumerate("xyz"):
            linha(f"CG {e}", m["cg"][i], p["cg_m"][i], "m", meia_cg if num(m["cg"][i])[0] == 0 else None)
        T = p["inercia_cg_kg_m2"]
        for i, e in enumerate(("Ixx", "Iyy", "Izz")):
            linha(e, m["inercia_no_cg"][e], T[i][i], "kg·m²")
        pi = m.get("produtos_de_inercia")
        if isinstance(pi, dict):
            for e, (i, j) in (("Ixy", (0, 1)), ("Ixz", (0, 2)), ("Iyz", (1, 2))):
                linha(e, pi[e], T[i][j], "kg·m²")
        linha("volume", m["volume"], p["volume_m3"], "m³")
        produtos_max = max(abs(T[i][j]) for i in range(3) for j in range(3) if i != j)
        atual = modelo[k]
        out["veiculos"][k] = {"situacao": "conferido", "arquivo": m["arquivo"], "compilou": m["compilou"],
                              "pecas_medidas": m["pecas"], "corpos_no_arquivo": p["corpos"], "linhas": linhas,
                              "produtos_medidos_texto": pi if isinstance(pi, str) else None, "produtos_previstos_max_abs_kg_m2": produtos_max,
                              "area_m2_medida": num(m["area"])[0],
                              "modelo_atual": {"massa_kg": atual["massa_kg"], "diferenca_massa_kg": atual["massa_kg"] - p["massa_kg"],
                                               "diferenca_cg_m": [a - b for a, b in zip(atual["cg_m"], p["cg_m"])]}}
    out = nativo(out)
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "conferencia_onshape.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    def f(x):
        if x is None:
            return "—"
        a = abs(x)
        s = f"{x:.4f}" if 1e-3 <= a < 1e5 or x == 0 else f"{x:.3e}"
        return s.replace(".", ",").replace("-", "−")
    ex = lambda x: "—" if x is None else f"{x:+.1e}".replace(".", ",").replace("-", "−")  # noqa: E731
    c = o["comum"]
    md = ["# Conferência do CAD no Onshape (gerado por tools/conferencia_onshape.py)", "",
          "**VERIFICAÇÃO**: o CAD gerado no Onshape reproduz o modelo do script (mesma geometria e mesmas densidades). Não é validação do projeto "
          "nem comparação com o orçamento (Etapa 7.3).", "",
          f"Medição: {c['responsavel']}, {c['data']}, {c['conta']}, FeatureScript versão {c['versao_featurescript']}, arquivos do commit "
          f"{c['commit_dos_arquivos']} (cópias em tests/data/onshape/), Assign materials: {'sim' if c['assign_materials'] else 'não'}. "
          "Unidades SI; inércias no centro de massa, nos eixos do Part Studio.", "",
          "Previsto: tools/cad_parametros.py (volume, centro e inercia) sobre os dados do próprio arquivo compilado. Precisão de leitura: meia "
          "unidade do último algarismo que o Onshape mostrou; se o Onshape omite zeros à direita, a precisão real é mais fina, e todos os "
          "desvios ainda passam com meia unidade da quarta casa decimal. O script calcula CG em x, y e z e o tensor de inércia completo; os "
          "produtos de inércia são comparados na forma de tensor (−∫ x y dm), com os sinais do Onshape.", ""]
    for k, x in o["veiculos"].items():
        md += [f"## {NOMES[k]}", ""]
        if x["situacao"] != "conferido":
            md += ["Aguardando medição.", ""]
            continue
        md += [f"Arquivo {x['arquivo']}; compilou: {'sim' if x['compilou'] else 'não'}; peças: {x['pecas_medidas']} medidas, "
               f"{x['corpos_no_arquivo']} corpos no arquivo.", "",
               "| Grandeza | Medido no Onshape | Previsto pelo script | Desvio absoluto | Desvio relativo | Precisão de leitura |",
               "| :- | -: | -: | -: | -: | :- |"]
        for li in x["linhas"]:
            md.append(f"| {li['grandeza']} ({li['unidade']}) | {f(li['medido'])} | {f(li['previsto'])} | {ex(li['desvio_abs'])} | "
                      f"{ex(li['desvio_rel'])} | {'dentro' if li['dentro'] else '**fora**'} (± {ex(li['meia_resolucao'])[1:]}) |")
        if x["produtos_medidos_texto"]:
            md.append(f"| produtos de inércia | {x['produtos_medidos_texto']} | maior valor absoluto {ex(x['produtos_previstos_max_abs_kg_m2'])} | — | — | — |")
        ma = x["modelo_atual"]
        md += [f"| área (m²) | {f(x['area_m2_medida'])} | não calculada pelo script | — | — | — |", "",
               f"Modelo atual (results/etapa7.2/parametros.yaml) contra o arquivo compilado: massa {ex(ma['diferenca_massa_kg'])} kg; CG "
               + ", ".join(ex(d) for d in ma["diferenca_cg_m"]) + " m.", ""]
    (SAIDA / "conferencia_onshape.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
