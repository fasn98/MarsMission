"""Comparação de ordem de grandeza das massas deste estudo com o ERO do MSR (Etapa 1.4).

NÃO é verificação: o ERO usa propulsão elétrica (Isp 4000 s) no retorno e tem plataforma completa;
este estudo usa só propulsão química e não modela a plataforma do orbitador.
Saída: results/etapa1.4/comparacao_msr.md

Uso: python tools/compara_msr.py   (depois de tools/dimensionamento.py)
"""

from __future__ import annotations

from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]


def main():
    d = yaml.safe_load((RAIZ / "results/etapa1.4/dimensionamento.yaml").read_text(encoding="utf-8"))
    m = {k: v["valor"] for k, v in yaml.safe_load((RAIZ / "tests/data/msr_massas.yaml").read_text(encoding="utf-8")).items()}
    br = lambda x: f"{x:,.0f}".replace(",", " ")  # noqa: E731
    md = ["# Comparação de ordem de grandeza com o MSR (gerado por tools/compara_msr.py)", "",
          "**Comparação de ordem de grandeza, não verificação.** O ERO volta com propulsão elétrica (Isp 4000 s) "
          "e tem plataforma completa (energia, aviônica, comunicação, térmica). Este estudo usa propulsão química e "
          "**não modela a plataforma do orbitador**: a carga útil é só captura + cápsula (CU-2) e a fração estrutural "
          "cobre só os módulos propulsivos. Massas em kg.", "",
          "| Grandeza | ERO (MSR) | " + " | ".join(d["variantes"]) + " |", "| :- |" + " -: |" * (1 + len(d["variantes"]))]

    def est(v, nome):
        return next((s for s in v.get("estagios", []) if s["nome"] == nome), None)

    def pos_tmi(v):  # massa depois da injeção trans-Marte = massa inicial do 2º estágio
        e = v.get("estagios", [])
        return e[1]["massa_inicial_kg"] if len(e) > 1 else None

    def modulo_insercao(v):
        e = est(v, "insercao_marte")
        return None if e is None else e["propelente_kg"] + e["inerte_kg"]

    linhas = [
        ("Massa a caminho de Marte (ERO: massa úmida no lançamento; aqui: depois da injeção trans-Marte)",
         m["ero_massa_umida_kg"], pos_tmi),
        ("Módulo de inserção em Marte (seco + propelente)", m["ero_oim_seco_kg"] + m["ero_oim_propelente_kg"], modulo_insercao),
    ]
    for rot, ero, f in linhas:
        vals = [f(v) for v in d["variantes"].values()]
        md.append(f"| {rot} | {br(ero)} | " + " | ".join("—" if x is None else br(x) for x in vals) + " |")
    md.append("| Massa na órbita baixa da Terra (inclui o estágio de saída da Terra; o ERO seria lançado num Ariane 64 [F32], sem esse estágio) | — | "
              + " | ".join(br(v["massa_orbita_baixa_kg"]) for v in d["variantes"].values()) + " |")
    (RAIZ / "results/etapa1.4/comparacao_msr.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
