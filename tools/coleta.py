"""Etapa 2.5, item 2: opções do conceito de coleta, lado a lado, com o efeito no lander e nos lançadores.

Cada opção (config/coleta.yaml) troca o item "amostras" da P-034 na plataforma de base do lander (L3 + amostras,
Etapa 2.3). Para cada uma: plataforma, massa injetada do lander (cadeia da Etapa 2.4) e a pior margem, nas quatro
janelas, dos lançadores do lander na forma (a) (ADR 0008). Não escolhe opção: a decisão é do Fabio.
Saída: results/etapa2.5/coleta.yaml e coleta.md

Uso: python tools/coleta.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(RAIZ / "src"), str(RAIZ / "tools")]

import dimensionamento as dm  # noqa: E402
import lancamento as lc  # noqa: E402
import plataformas as pl  # noqa: E402
from superficie import _ler  # noqa: E402

SAIDA = RAIZ / "results" / "etapa2.5"


def prevista(itens, pcfg):
    tot = 0.0
    for it in itens:
        cat = it.get("categoria", "sem_margem_adicional")
        tot += it["massa_kg"] if cat == "sem_margem_adicional" else it["massa_kg"] * (1 + pl._mga(cat, pcfg, "e1_medio"))
    return tot


def main():
    ccfg, pcfg, lcfg = _ler("config/coleta.yaml"), _ler("config/plataformas.yaml"), _ler("config/lancadores.yaml")
    l3 = pl.lander_l3(pcfg)
    # itens das Etapas 4.1 a 4.4 da P-017 vigente (caso B da Etapa 4.5, ADR 0019), comuns a todas as opções de coleta
    extra = float(_ler("config/superficie.yaml")["lander"]["plataforma_superficie_kg"]["valor"]) - pl.lander_base(pcfg)
    casos = {}
    for k, o in ccfg["opcoes"].items():
        casos[k] = (o["nome"], prevista(o["itens"], pcfg))
        if "variante_rochas" in o:
            v = o["variante_rochas"]
            casos[k + "_com_testemunhagem"] = (o["nome"] + " + ferramenta de testemunhagem",
                                               casos[k][1] + v["massa_kg"] * (1 + pl._mga("mecanismos", pcfg, "e1_medio")))
        if "limite_superior_kg" in o:
            casos[k + "_limite_superior"] = (o["nome"] + " (limite superior)", float(o["limite_superior_kg"]["valor"]))
    _, janelas, _ = lc.veiculos()
    lanc = lcfg["escolha"]["lander"]
    linhas = []
    for k, (nome, m_col) in casos.items():
        plat = l3 + m_col + extra
        m_inj = lc.veiculos(plat)[0]["lander"]["injetada_kg"]
        margens = {n: lc.pior_margem_a(n, m_inj, janelas, lcfg)[0] for n in lanc}
        linhas.append({"opcao": k, "nome": nome, "coleta_prevista_kg": m_col, "plataforma_lander_kg": plat,
                       "lander_injetado_kg": m_inj, "pior_margem_a": margens})
    out = {"gerado_por": "tools/coleta.py", "l3_kg": l3, "itens_etapa_4_kg": extra, "lancadores_do_lander_a": lanc, "opcoes": linhas}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "coleta.yaml").write_text(yaml.safe_dump(dm._nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")
    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    pc = lambda x: "—" if x is None else f"{100 * x:+.0f} %".replace("-", "−")  # noqa: E731
    md = ["# Opções de coleta (gerado por tools/coleta.py)", "",
          f"Plataforma do lander = L3 ({br(l3)} kg) + item de coleta + itens das Etapas 4.1 a 4.4, sem a energia do aquecimento do MAV já no item do MAV ({br(extra, 1)} kg; P-017, ADR 0019). Pior margem na forma (a), nas quatro janelas. Massas em kg.", "",
          "| Opção | Coleta (prevista) | Plataforma do lander | Lander injetado | " + " | ".join(lanc) + " |",
          "| :- | -: | -: | -: |" + " -: |" * len(lanc)]
    for r in linhas:
        md.append(f"| {r['nome']} | {br(r['coleta_prevista_kg'], 1)} | {br(r['plataforma_lander_kg'], 1)} | {br(r['lander_injetado_kg'])} | "
                  + " | ".join(pc(r["pior_margem_a"][n]) for n in lanc) + " |")
    (SAIDA / "coleta.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
