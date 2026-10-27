"""Comparação de ordem de grandeza da missão de conjunção com o DRA 5.0 ([F18]).

Para cada janela com linha na Tabela 4-2 do DRA 5.0 Addendum, compara a missão
"conjuncao_transito_curto" de results/etapa1.3/missoes.yaml (órbita elíptica de 1 sol, captura
propulsiva, igual ao DRA) com a linha do DRA. É uma comparação de ordem de grandeza, NÃO uma
verificação: as trajetórias não são as mesmas (o DRA limita v∞ e tempos de voo e inclui perdas
gravitacionais).
Saída: results/etapa1.3/comparacao_dra5.md

Uso: python tools/compara_dra5.py   (depois de tools/missoes.py)
"""

from __future__ import annotations

from pathlib import Path

import sys

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(RAIZ / "src"), str(RAIZ / "tools")]

from missoes import parametros  # noqa: E402
from orbital import manobras as mn  # noqa: E402


def main():
    dra = yaml.safe_load((RAIZ / "tests/data/dra5_tabela4-2.yaml").read_text(encoding="utf-8"))["linhas"]
    ms = yaml.safe_load((RAIZ / "results/etapa1.3/missoes.yaml").read_text(encoding="utf-8"))["candidatas"]
    br = lambda x, n=2: f"{x:.{n}f}".replace(".", ",")  # noqa: E731
    p = parametros()
    o = p.orbitas_marte["eliptica_alta"]
    md = ["# Comparação de ordem de grandeza com o DRA 5.0 (gerado por tools/compara_dra5.py)", "",
          "**Comparação de ordem de grandeza, não verificação.** DRA 5.0 Addendum, Tabela 4-2 (p. 137), "
          "com perdas gravitacionais, v∞ e tempos de voo limitados. Aqui: impulsivo ideal, sem perdas, "
          "classe `conjuncao_transito_curto` (trânsitos ≤ 210 d). Os dois usam órbita de 1 sol "
          "250 × 33.793 km e captura propulsiva. Δv e v∞ em km/s.", ""]
    for ano, d in dra.items():
        m = next(c for c in ms if c["id"] == f"{ano}-conjuncao_transito_curto")
        q = m["por_orbita_marte"]["eliptica_alta"]
        tot_dra = d["tmi_dv"] + d["moi_dv"] + d["tei_dv"]
        linhas = [
            ("Partida da Terra", d["partida"], m["partida_terra"]),
            ("Tempo de ida (d)", d["tof_ida"], round(m["ida_dias"])),
            ("Permanência (d)", d["permanencia"], round(m["em_marte_dias"])),
            ("Tempo de volta (d)", d["tof_volta"], round(m["volta_dias"])),
            ("v∞ de partida da Terra", br(d["tmi_vinf"], 3), br(m["c3_km2_s2"] ** 0.5, 3)),
            ("Δv injeção trans-Marte", br(d["tmi_dv"], 3), br(m["dv_saida_terra_km_s"], 3)),
            ("v∞ de chegada a Marte", br(d["moi_vinf"], 3), br(m["vinf_chegada_marte_km_s"], 3)),
            ("Δv captura em Marte", br(d["moi_dv"], 3), br(q["dv_captura_propulsiva_km_s"], 3)),
            ("v∞ de partida de Marte", br(d["tei_vinf"], 3), br(m["c3l_partida_marte_km2_s2"] ** 0.5, 3)),
            ("Δv injeção trans-Terra", br(d["tei_dv"], 3), br(q["dv_saida_marte_km_s"], 3)),
            ("v∞ de chegada à Terra", br(d["vinf_terra"], 3), br(m["vinf_chegada_terra_km_s"], 3)),
            ("Δv total (soma dos três)", br(tot_dra, 3) + " (soma calculada aqui)", br(q["dv_total_sem_aerocaptura_km_s"], 3)),
            ("Razão Δv total (este estudo / DRA)", "", br(q["dv_total_sem_aerocaptura_km_s"] / tot_dra, 2)),
        ]
        # Mesmas fórmulas deste estudo aplicadas aos v∞ do DRA: isola o modelo de Δv da trajetória.
        tmi = float(mn.dv_hiperbole_orbita(p.mu_terra, d["tmi_vinf"], p.leo.rp))
        moi = float(mn.dv_hiperbole_orbita(p.mu_marte, d["moi_vinf"], o.rp, o.ra))
        tei = float(mn.dv_hiperbole_orbita(p.mu_marte, d["tei_vinf"], o.rp, o.ra))
        iso = [("Δv injeção trans-Marte", d["tmi_dv"], tmi), ("Δv captura em Marte", d["moi_dv"], moi),
               ("Δv injeção trans-Terra", d["tei_dv"], tei)]
        md += [f"## Janela {ano}", "", "| Grandeza | DRA 5.0 | Este estudo |", "| :- | -: | -: |"]
        md += [f"| {a} | {b} | {c} |" for a, b, c in linhas] + [""]
        md += ["Mesmos v∞ do DRA, Δv pelas fórmulas impulsivas deste estudo:", "",
               "| Manobra | DRA (com perdas gravitacionais) | Fórmula impulsiva com o v∞ do DRA | DRA − fórmula |",
               "| :- | -: | -: | -: |"]
        md += [f"| {a} | {br(b, 3)} | {br(c, 3)} | {br(b - c, 3)} |" for a, b, c in iso] + [""]
    (RAIZ / "results/etapa1.3/comparacao_dra5.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
