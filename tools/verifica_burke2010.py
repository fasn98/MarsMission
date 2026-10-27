"""Verificação dos mínimos de C3 Terra→Marte contra NASA/TM-2010-216764 ([F13]).

Para cada janela e tipo calcula, com partida no centro da Terra (399) e no baricentro
Terra–Lua (3), já que o manual não declara o corpo de partida:
  (a) o mínimo de C3 próprio (grade de 2 dias + refinamento), comparado com o manual;
  (b) C3 e v∞ nas datas exatas impressas no manual.
Saída: results/etapa1.2/verificacao_burke2010.yaml e .md (tabelas com erro absoluto e relativo).

Uso: python tools/verifica_burke2010.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import spiceypy as spice
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))


def _exclusao():
    """Faixa em torno de 180° excluída da busca de mínimos (premissa P-006)."""
    cfg = yaml.safe_load((RAIZ / "config" / "premissas.yaml").read_text(encoding="utf-8"))
    return next(p["valor"] for p in cfg["premissas"] if p["nome"] == "exclusao_angulo_180_graus")

from orbital import ephemeris as eph  # noqa: E402
from orbital import porkchop as pc  # noqa: E402

SAIDA = RAIZ / "results" / "etapa1.2"
CORPOS = {"399": "centro da Terra", "3": "baricentro Terra–Lua"}


def _et(data):
    return spice.str2et(f"{data} 00:00 TDB")


def _dia(et):
    return spice.et2utc(et, "ISOC", 0)[:10]


def main():
    eph.carregar_kernels()
    ref = yaml.safe_load((RAIZ / "tests/data/burke2010_minimos.yaml").read_text(encoding="utf-8"))
    cfg = yaml.safe_load((RAIZ / "config/janelas.yaml").read_text(encoding="utf-8"))["terra_marte"]
    out = {"gerado_por": "tools/verifica_burke2010.py", "fonte": "NASA/TM-2010-216764", "linhas": []}
    for ano, jan in cfg["janelas"].items():
        etp = np.arange(_et(jan["partida"][0]), _et(jan["partida"][1]) + 1, cfg["passo_dias"] * pc.DIA)
        etc = np.arange(_et(jan["chegada"][0]), _et(jan["chegada"][1]) + 1, cfg["passo_dias"] * pc.DIA)
        for corpo in CORPOS:
            g = pc.calcular_grade(corpo, cfg["chegada"], etp, etc)
            for tipo in (1, 2):
                r = ref["janelas"][ano][f"tipo_{tipo}"]
                m = pc.minimo_c3_por_tipo(corpo, cfg["chegada"], g, tipo, _exclusao())
                c3d, vd, angd, _ = pc.transferencia(corpo, cfg["chegada"], _et(r["partida"]), _et(r["chegada"]))
                c3n, vn = float(r["c3"]), float(r["vinf_chegada"])
                out["linhas"].append({
                    "janela": ano, "tipo": tipo, "corpo_partida": corpo,
                    "nasa": {"partida": r["partida"], "chegada": r["chegada"], "c3": c3n, "vinf": vn,
                             "tabela": ref["janelas"][ano]["tabela"], "pagina": ref["janelas"][ano]["pagina"]},
                    "minimo_proprio": {"partida": _dia(m["et_partida"]), "chegada": _dia(m["et_chegada"]),
                                       "tof_dias": round(m["tof_dias"], 1), "c3": round(m["c3"], 4),
                                       "vinf": round(m["vinf_chegada"], 4), "angulo": round(m["angulo"], 1),
                                       "desloc_partida_dias": round((m["et_partida"] - _et(r["partida"])) / pc.DIA, 1)},
                    "nas_datas_nasa": {"c3": round(c3d, 4), "vinf": round(vd, 4), "angulo": round(angd, 1)},
                })
                print(ano, tipo, corpo, out["linhas"][-1]["minimo_proprio"], out["linhas"][-1]["nas_datas_nasa"])
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "verificacao_burke2010.yaml").write_text(
        yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")

    def err(a, b):
        return f"{a - b:+.3f} | {100 * (a - b) / b:+.2f} %"

    md = ["# Verificação contra NASA/TM-2010-216764 (gerado por tools/verifica_burke2010.py)", ""]
    for corpo, nome in CORPOS.items():
        md += [f"## Partida: {nome} (NAIF {corpo})", "",
               "### (a) Mínimo de C3 próprio vs. manual", "",
               "| Janela | Tipo | Partida NASA → própria | Chegada NASA → própria | C3 NASA | C3 próprio | Erro abs. | Erro rel. | v∞ NASA | v∞ próprio | Erro abs. | Erro rel. |",
               "| :- | :- | :- | :- | -: | -: | -: | -: | -: | -: | -: | -: |"]
        for l in (x for x in out["linhas"] if x["corpo_partida"] == corpo):
            n, p = l["nasa"], l["minimo_proprio"]
            md.append(f"| {l['janela']} | {'I' * l['tipo']} | {n['partida']} → {p['partida']} | {n['chegada']} → {p['chegada']} "
                      f"| {n['c3']} | {p['c3']:.3f} | {err(p['c3'], n['c3'])} | {n['vinf']} | {p['vinf']:.3f} | {err(p['vinf'], n['vinf'])} |")
        md += ["", "### (b) Nas datas impressas no manual", "",
               "| Janela | Tipo | Datas NASA | C3 NASA | C3 calc. | Erro abs. | Erro rel. | v∞ NASA | v∞ calc. | Erro abs. | Erro rel. |",
               "| :- | :- | :- | -: | -: | -: | -: | -: | -: | -: | -: |"]
        for l in (x for x in out["linhas"] if x["corpo_partida"] == corpo):
            n, d = l["nasa"], l["nas_datas_nasa"]
            md.append(f"| {l['janela']} | {'I' * l['tipo']} | {n['partida']} → {n['chegada']} | {n['c3']} | {d['c3']:.3f} "
                      f"| {err(d['c3'], n['c3'])} | {n['vinf']} | {d['vinf']:.3f} | {err(d['vinf'], n['vinf'])} |")
        md.append("")
    (SAIDA / "verificacao_burke2010.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
