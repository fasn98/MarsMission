"""Verificação do retorno Marte→Terra contra JPL Publication 82-43, Vol. I, Part 5 ([F14]).

Para cada oportunidade de 1992 a 2007 e para cada linha das tabelas "ENERGY MINIMA" (mínimo de
C3L por tipo e mínimo de VHP por tipo), com partida no baricentro de Marte (4) e chegada no
centro da Terra (399) e no baricentro Terra–Lua (3):
  (a) o mínimo próprio (grade de 2 dias + refinamento) da mesma grandeza e tipo;
  (b) a grandeza calculada nas datas impressas na tabela.
O manual usa a efeméride DE-118. O efeito de trocar a efeméride é medido à parte, com a DE200
(a DE118 girada para J2000), em docs/etapa1.2_retorno.md.
Saída: results/etapa1.2/verificacao_jpl8243.yaml e .md.

Uso: python tools/verifica_jpl8243.py
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
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
CHEGADAS = {"399": "centro da Terra", "3": "baricentro Terra–Lua"}
LINHAS = {"c3l_1": ("c3", 1), "c3l_2": ("c3", 2), "vhp_1": ("vinf", 1), "vhp_2": ("vinf", 2)}


def _et(d):
    return spice.str2et(f"{d} 00:00 TDB")


def _dia(et):
    return eph.data_tdb(et)


def _dominio(jan):
    """Domínio da grade: ±120 dias em torno das partidas da tabela; chegada de +100 a +520 dias."""
    deps = [date.fromisoformat(jan[k]["partida"]) for k in LINHAS]
    p0, p1 = min(deps) - timedelta(days=120), max(deps) + timedelta(days=120)
    return p0.isoformat(), p1.isoformat(), (p0 + timedelta(days=100)).isoformat(), (p1 + timedelta(days=520)).isoformat()


def main():
    eph.carregar_kernels()
    ref = yaml.safe_load((RAIZ / "tests/data/jpl8243p5_minimos.yaml").read_text(encoding="utf-8"))["janelas"]
    out = {"gerado_por": "tools/verifica_jpl8243.py", "fonte": "JPL Publication 82-43, Vol. I, Part 5",
           "linhas": []}
    for ano, jan in ref.items():
        p0, p1, a0, a1 = _dominio(jan)
        etp = np.arange(_et(p0), _et(p1) + 1, 2 * pc.DIA)
        etc = np.arange(_et(a0), _et(a1) + 1, 2 * pc.DIA)
        for chegada in CHEGADAS:
            g = pc.calcular_grade(eph.BARICENTRO_MARTE, chegada, etp, etc)
            for chave, (grandeza, tipo) in LINHAS.items():
                r = jan[chave]
                m = pc.minimo_c3_por_tipo(eph.BARICENTRO_MARTE, chegada, g, tipo, _exclusao(), grandeza)
                c3d, vd, angd, _ = pc.transferencia(eph.BARICENTRO_MARTE, chegada, _et(r["partida"]), _et(r["chegada"]))
                valor_m = m["c3"] if grandeza == "c3" else m["vinf_chegada"]
                out["linhas"].append({
                    "janela": ano, "linha": chave, "grandeza": grandeza, "tipo": tipo, "corpo_chegada": chegada,
                    "jpl": {"partida": r["partida"], "chegada": r["chegada"], "valor": float(r["valor"]),
                            "pagina": jan["pagina"]},
                    "minimo_proprio": {"partida": _dia(m["et_partida"]), "chegada": _dia(m["et_chegada"]),
                                       "valor": round(valor_m, 4), "angulo": round(m["angulo"], 1)},
                    "nas_datas_jpl": {"valor": round(c3d if grandeza == "c3" else vd, 4), "angulo": round(angd, 1)},
                })
                print(ano, chave, chegada, out["linhas"][-1]["minimo_proprio"], out["linhas"][-1]["nas_datas_jpl"])
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "verificacao_jpl8243.yaml").write_text(
        yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")

    def err(a, b):
        return f"{a - b:+.3f} | {100 * (a - b) / b:+.2f} %"

    md = ["# Verificação contra JPL Publication 82-43, Vol. I, Part 5 (gerado por tools/verifica_jpl8243.py)", "",
          "C3L em km²/s² (partida de Marte); VHP em km/s (chegada à Terra). Partida: baricentro de Marte.", ""]
    for chegada, nome in CHEGADAS.items():
        md += [f"## Chegada: {nome} (NAIF {chegada})", "",
               "| Janela | Linha | Datas JPL | Valor JPL | (b) nas datas JPL | Erro abs. | Erro rel. | Ângulo (b) | (a) mínimo próprio | Datas (a) | Erro abs. | Erro rel. |",
               "| :- | :- | :- | -: | -: | -: | -: | -: | -: | :- | -: | -: |"]
        for l in (x for x in out["linhas"] if x["corpo_chegada"] == chegada):
            j, d, m = l["jpl"], l["nas_datas_jpl"], l["minimo_proprio"]
            md.append(f"| {l['janela']} | {l['linha']} | {j['partida']} → {j['chegada']} | {j['valor']} | {d['valor']:.3f} "
                      f"| {err(d['valor'], j['valor'])} | {d['angulo']}° | {m['valor']:.3f} | {m['partida']} → {m['chegada']} "
                      f"| {err(m['valor'], j['valor'])} |")
        md.append("")
    (SAIDA / "verificacao_jpl8243.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
