"""Etapa 3.1, redimensionamento (ADR 0011): perdas de queima finita calculadas no lugar da P-015.

As perdas de captura e de saída de Marte dependem das massas (orbital.perdas, motores escolhidos, várias queimas), e as
massas dependem das perdas e da órbita de encontro (tools/plataformas.py, regra dos 5 % do ADR 0005). Ponto fixo:
  1. grava as perdas candidatas em results/etapa3.1/perdas_calculadas.yaml (começa pelas da P-015);
  2. refaz a Etapa 2.3 (tools/plataformas.py: plataformas, varredura da órbita de encontro, massas);
  3. calcula as perdas nas massas novas (orbital.veiculos, orbital.perdas);
  4. repete até nenhuma perda mudar mais que a tolerância (P-044).
As ferramentas seguintes (tools/plataformas.py e as das Etapas 2.4 e 2.5) leem as perdas convergidas pelo config
(config/dimensionamento.yaml, perda_gravitacional, chaves "resultado").
Saída: results/etapa3.1/perdas_calculadas.yaml e .md (e, de passagem, results/etapa2.3/, que tools/plataformas.py refaz)

Uso: python tools/redimensiona.py
"""

from __future__ import annotations

import contextlib
import io
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(RAIZ / "src"), str(RAIZ / "tools")]

import plataformas  # noqa: E402
from orbital import perdas as pd  # noqa: E402
from orbital import veiculos as ve  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa3.1"
ARQ = SAIDA / "perdas_calculadas.yaml"


def _grava(perda, extra):
    SAIDA.mkdir(parents=True, exist_ok=True)
    ARQ.write_text(yaml.safe_dump(nativo({"gerado_por": "tools/redimensiona.py", "perda_km_s": perda, **extra}),
                                  sort_keys=False, allow_unicode=True), encoding="utf-8")


def main():
    rcfg = ler("config/queima_finita.yaml")["redimensionamento"]
    tol, n_max = v(rcfg["tolerancia_km_s"]), int(v(rcfg["max_iteracoes"]))
    p015 = next(p for p in ler("config/premissas.yaml")["premissas"] if p["id"] == "P-015")["valor"]
    perda = {"captura_marte": float(p015["captura_marte"]), "saida_marte": float(p015["saida_marte"])}
    hist = []
    for it in range(1, n_max + 1):
        _grava(perda, {"estado": "em iteração"})
        with contextlib.redirect_stdout(io.StringIO()):   # a Etapa 2.3 imprime o relatório a cada iteração
            plataformas.main()
        vei = ve.veiculos(detalhe=True)[0]
        res = pd.perdas_projeto(vei)
        nova = res["perda_km_s"]
        delta = max(abs(nova[k] - perda[k]) for k in perda)
        hist.append({"iteracao": it, "perda_usada_km_s": dict(perda), "perda_calculada_km_s": dict(nova), "maior_mudanca_km_s": delta,
                     "orbitador_injetado_kg": vei["orbitador_regra_iii"]["injetada_kg"], "lander_injetado_kg": vei["lander"]["injetada_kg"]})
        perda = dict(nova)
        if delta <= tol:
            break
    else:
        raise RuntimeError(f"ponto fixo não convergiu em {n_max} iterações")
    _grava(perda, {"estado": "convergido", "tolerancia_km_s": tol, "iteracoes": hist,
                   "captura": res["captura"], "saida": res["saida"],
                   "p015_km_s": {"captura_marte": float(p015["captura_marte"]), "saida_marte": float(p015["saida_marte"])}})
    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    md = ["# Perdas de queima finita do projeto (gerado por tools/redimensiona.py)", "",
          "Motores escolhidos (ADR 0011), várias queimas no periapse (P-042), caso de projeto (regra iii). Ponto fixo com as "
          f"massas e a órbita de encontro, tolerância de {br(1e3 * tol, 3)} m/s (P-044). Rótulo: calculado (não verificado).", "",
          "| Manobra | Combinação | Missão | N | m0 (kg) | Propelente (kg) | Δv impulsivo (m/s) | Perda calculada (m/s) | P-015 (m/s) |",
          "| :- | :- | :- | -: | -: | -: | -: | -: | -: |"]
    for k, chave in (("captura", "captura_marte"), ("saida", "saida_marte")):
        x = res[k]
        md.append(f"| {k} | {x['combinacao']}: {x['motores']} | {x['missao']} | {x['n']} | {br(x['m0_kg'])} | {br(x['propelente_kg'])} | "
                  f"{br(1e3 * x['dv_impulsivo_km_s'])} | {br(1e3 * perda[chave], 1)} | {br(1e3 * float(p015[chave]), 1)} |")
    md += ["", "## Iterações", "", "| Iteração | Perda usada: captura / saída (m/s) | Calculada (m/s) | Maior mudança (m/s) | Orbitador injetado (kg) |",
           "| -: | :- | :- | -: | -: |"]
    for h in hist:
        md.append(f"| {h['iteracao']} | {br(1e3 * h['perda_usada_km_s']['captura_marte'], 2)} / {br(1e3 * h['perda_usada_km_s']['saida_marte'], 2)} | "
                  f"{br(1e3 * h['perda_calculada_km_s']['captura_marte'], 2)} / {br(1e3 * h['perda_calculada_km_s']['saida_marte'], 2)} | "
                  f"{br(1e3 * h['maior_mudanca_km_s'], 4)} | {br(h['orbitador_injetado_kg'])} |")
    (SAIDA / "perdas_calculadas.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
