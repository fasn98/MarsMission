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
    """Valor de um número em texto (como o Onshape o mostrou)."""
    return float(Decimal(str(s)))


def casas(s):
    """Casas decimais mostradas num número em texto."""
    return max(-Decimal(str(s)).as_tuple().exponent, 0)


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

        def linha(grandeza, s, prev, unidade, casas_forcadas=None):
            v_ = num(s)
            nc = casas(s) if casas_forcadas is None else casas_forcadas
            meia = 0.5 * 10.0 ** -nc   # meia unidade da última casa decimal mostrada
            linhas.append({"grandeza": grandeza, "unidade": unidade, "medido": v_, "medido_texto": str(s), "casas_mostradas": nc,
                           "previsto": prev, "desvio_abs": v_ - prev,
                           "desvio_rel": (v_ - prev) / prev if abs(prev) > 1e-9 else None, "meia_resolucao": meia, "dentro": abs(v_ - prev) <= meia})
        linha("massa", m["massa"], p["massa_kg"], "kg")
        casas_cg = casas(m["cg"][2])   # um CG mostrado como "0" usa as casas da coordenada z
        for i, e in enumerate("xyz"):
            linha(f"CG {e}", m["cg"][i], p["cg_m"][i], "m", casas_cg if num(m["cg"][i]) == 0 else None)
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
                              "area_m2_medida": num(m["area"]), "area_texto": str(m["area"]),
                              "modelo_atual": {"massa_kg": atual["massa_kg"], "diferenca_massa_kg": atual["massa_kg"] - p["massa_kg"],
                                               "diferenca_cg_m": [a - b for a, b in zip(atual["cg_m"], p["cg_m"])]}}
    out = nativo(out)
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "conferencia_onshape.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def ex_kg(x):
    """Diferença de massa (modelo menos compilado), em kg ou, abaixo de 10 g, em g."""
    if abs(x) < 5e-5:   # abaixo da última casa mostrada (0,1 g)
        return "sem diferença"
    s = f"{x:+.3f} kg" if abs(x) >= 0.01 else f"{1e3 * x:+.1f} g"
    return s.replace(".", ",").replace("-", "−")


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
          f"Documento no Onshape: \"{c['documento_onshape']}\", gerado com os arquivos do commit {c['commit_dos_arquivos']} e versionado no Onshape como "
          f"\"{c['versao_no_onshape']}\". Os arquivos atuais (results/etapa7.2/*.fs) diferem dos compilados: modelo atual menos compilado, "
          + "; ".join(f"{NOMES[k]} {ex_kg(x['modelo_atual']['diferenca_massa_kg'])}" for k, x in o["veiculos"].items() if x["situacao"] == "conferido")
          + ". Os previstos dos arquivos atuais estão em results/etapa7.2/parametros.yaml.", "",
          "Previsto: tools/cad_parametros.py (volume, centro e inercia) sobre os dados do próprio arquivo compilado. O script calcula CG em "
          "x, y e z e o tensor de inércia completo; os produtos de inércia são comparados na forma de tensor (−∫ x y dm), com os sinais do Onshape.", "",
          f"Tolerância: {c['origem_da_tolerancia']}. Cada linha mostra as casas decimais lidas; um CG mostrado como \"0\" usa as casas da "
          "coordenada z do mesmo veículo.", ""]
    for k, x in o["veiculos"].items():
        md += [f"## {NOMES[k]}", ""]
        if x["situacao"] != "conferido":
            md += ["Aguardando medição.", ""]
            continue
        md += [f"Arquivo {x['arquivo']}; compilou: {'sim' if x['compilou'] else 'não'}; peças: {x['pecas_medidas']} medidas, "
               f"{x['corpos_no_arquivo']} corpos no arquivo.", "",
               "| Grandeza | Medido no Onshape | Casas mostradas | Previsto pelo script | Desvio absoluto | Desvio relativo | Tolerância de leitura |",
               "| :- | -: | -: | -: | -: | -: | :- |"]
        for li in x["linhas"]:
            md.append(f"| {li['grandeza']} ({li['unidade']}) | {li['medido_texto'].replace('.', ',').replace('-', '−')} | {li['casas_mostradas']} | "
                      f"{f(li['previsto'])} | {ex(li['desvio_abs'])} | {ex(li['desvio_rel'])} | "
                      f"± {ex(li['meia_resolucao'])[1:]}: {'dentro' if li['dentro'] else '**fora**'} |")
        if x["produtos_medidos_texto"]:
            md.append(f"| produtos de inércia | {x['produtos_medidos_texto']} | — | maior valor absoluto {ex(x['produtos_previstos_max_abs_kg_m2'])} | — | — | — |")
        ma = x["modelo_atual"]
        md += [f"| área (m²) | {x['area_texto'].replace('.', ',')} | {casas(x['area_texto'])} | não calculada pelo script | — | — | — |", "",
               f"Modelo atual (results/etapa7.2/parametros.yaml) contra o arquivo compilado: massa {ex(ma['diferenca_massa_kg'])} kg; CG "
               + ", ".join(ex(d) for d in ma["diferenca_cg_m"]) + " m.", ""]
    md += ["", "## Errata (2026-11-06, decisão do Fabio): 13 algarismos nos arquivos atuais", "",
           "Com 6 algarismos, o modelo atual menos o compilado era: Orbitador +0,6 g, CG z +3,2e−07 m; Lander −0,027 kg, CG z +1,8e−06 m; MAV sem diferença. Os valores vigentes são os da linha \"Modelo atual\" de cada veículo. "
           "A conferência contra o Onshape não muda: ela vale para os arquivos do commit 32cb41d, copiados em tests/data/onshape/."]
    (SAIDA / "conferencia_onshape.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
