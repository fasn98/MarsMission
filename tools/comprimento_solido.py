"""Comprimento do MAV sólido pela P-108 revista (aprovada pelo Fabio em 2026-11-12, NÃO VALIDADA).

Comprimento = motor do estágio 1 + motor do estágio 2 + resto fixo. O comprimento de cada motor vem do ajuste
L = a · P^b · D^c dos motores sólidos do catálogo [F270] (config/familia1.yaml, inerte_solido.motores); o resto
(interestágio, carga, aviônica e adaptadores) é o que falta para os 2,7 m do MAV do MSR ([F247]) no propelente e no
diâmetro dele, e fica fixo na escala, sem fonte.
Saída: results/familia1/comprimento_solido.yaml e .md. As ferramentas do sólido usam `comprimento`.

Uso: python tools/comprimento_solido.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "familia1"
POL = 0.0254   # [F112] Apêndice B.8, PDF p. 62: polegada em metros


def ajuste():
    cfg = ler("config/familia1.yaml")["inerte_solido"]
    ms = ler("config/cad.yaml")["mav_solido"]
    lb = v(ler("config/motores.yaml")["conversao"]["lb_para_kg"])
    P = np.array([m["propelente_lbm"] * lb for m in cfg["motores"]])
    D = np.array([m["diametro_pol"] * POL for m in cfg["motores"]])
    L = np.array([m["comprimento_pol"] * POL for m in cfg["motores"]])
    X = np.vstack([np.ones_like(P), np.log(P), np.log(D)]).T
    co, *_ = np.linalg.lstsq(X, np.log(L), rcond=None)
    r = np.log(L) - X @ co
    cov = float(r @ r) / (len(P) - 3) * np.linalg.inv(X.T @ X)
    Xp = np.vstack([np.ones_like(P), np.log(P)]).T
    cp, *_ = np.linalg.lstsq(Xp, np.log(L), rcond=None)
    rp = np.log(L) - Xp @ cp
    a, b, c = math.exp(co[0]), float(co[1]), float(co[2])
    mp, d0, L0 = ms["propelente_kg"]["valor"], v(ms["diametro_m"]), v(ms["comprimento_m"])
    motores = [a * p ** b * d0 ** c for p in mp]
    return {"a": a, "b": b, "c": c, "erro_padrao_b": math.sqrt(cov[1, 1]), "erro_padrao_c": math.sqrt(cov[2, 2]), "n": len(P),
            "fator_rms": math.exp(math.sqrt(float(r @ r) / (len(P) - 3))), "fator_max": math.exp(float(np.abs(r).max())),
            "so_propelente": {"a": math.exp(cp[0]), "b": float(cp[1]), "fator_rms": math.exp(math.sqrt(float(rp @ rp) / (len(P) - 2))), "fator_max": math.exp(float(np.abs(rp).max()))},
            "diametro_msr_m": d0, "propelente_msr_kg": mp, "comprimento_msr_m": L0, "motores_msr_m": motores, "resto_m": L0 - sum(motores),
            "residuos_fator": {m["nome"]: math.exp(float(x)) for m, x in zip(cfg["motores"], r)}}


def comprimento(propelentes_kg, diametro_m, aj=None):
    """Comprimento (m) do MAV sólido com o propelente de cada estágio e o diâmetro dados (P-108 revista)."""
    aj = ler("results/familia1/comprimento_solido.yaml") if aj is None else aj
    return sum(aj["a"] * p ** aj["b"] * diametro_m ** aj["c"] for p in propelentes_kg) + aj["resto_m"]


def main():
    aj = ajuste()
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "comprimento_solido.yaml").write_text(yaml.safe_dump(nativo({"gerado_por": "tools/comprimento_solido.py", "status": "NÃO VALIDADO", "premissa": "P-108 (revista)", **aj}), sort_keys=False, allow_unicode=True), encoding="utf-8")
    br = lambda x, n=3: f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    md = ["# Comprimento do MAV sólido, P-108 revista (gerado por tools/comprimento_solido.py)", "", "**NÃO VALIDADO.** P-108 revista, aprovada pelo Fabio em 2026-11-12.", "",
          f"- Motores do catálogo [F270] com diâmetro e comprimento publicados: {aj['n']}.",
          f"- Forma: L = a · P^b · D^c, mínimos quadrados em ln: a = {br(aj['a'], 4)}, b = {br(aj['b'], 3)} (erro-padrão {br(aj['erro_padrao_b'], 3)}), c = {br(aj['c'], 3)} (erro-padrão {br(aj['erro_padrao_c'], 3)}); erro: fator rms {br(aj['fator_rms'], 2)}, maior desvio fator {br(aj['fator_max'], 2)}.",
          f"- Só com o propelente (L = a · P^b): b = {br(aj['so_propelente']['b'], 3)}, fator rms {br(aj['so_propelente']['fator_rms'], 2)}, maior desvio {br(aj['so_propelente']['fator_max'], 2)}.",
          f"- No Ø {br(aj['diametro_msr_m'], 2)} m e no propelente do MSR: motores de {br(aj['motores_msr_m'][0], 2)} e {br(aj['motores_msr_m'][1], 2)} m; o resto até os {br(aj['comprimento_msr_m'], 1)} m do MSR ([F247]), {br(aj['resto_m'], 2)} m, é interestágio, carga, aviônica e adaptadores, sem fonte, fixo na escala.",
          "", "Comprimento do MAV = motor do estágio 1 + motor do estágio 2 + resto fixo."]
    (SAIDA / "comprimento_solido.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
