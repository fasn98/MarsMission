"""Mapa de dependências da regeneração de results/ (issue #61): roda toda a regeneração numa cópia, como
tools/confere_regeneracao.py, registrando por ferramenta os arquivos de results/ lidos e gravados (tools/rastreio_es.py) e o
tempo. Uma ferramenta depende das que gravaram por último, antes dela, os arquivos que ela lê.
Saída: results/conferencia/mapa_regeneracao.yaml e .md (fora da comparação do CI). Os tempos são observação de ambiente.

Uso: python tools/mapa_regeneracao.py
"""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))
import confere_regeneracao as cr  # noqa: E402

SAIDA = RAIZ / "results" / "conferencia"


def main():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "repo"
        shutil.copytree(RAIZ, d, ignore=cr._ignorar)
        shutil.copytree(RAIZ / "data", d / "data")
        (d / "results").mkdir()
        subprocess.run(["git", "init", "-q"], cwd=d, check=True, env=cr._env_git())
        subprocess.run(["git", "add", "-A"], cwd=d, check=True, env=cr._env_git())
        subprocess.run(["git", "-c", "user.name=x", "-c", "user.email=x@x", "commit", "-qm", "copia"], cwd=d, check=True, env=cr._env_git())
        rs = Path(tmp) / "rastreio"
        rs.mkdir()
        log = cr.regenerar(d, rastreio=rs)
        es = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(rs.glob("*.json"))]
    rodadas = [x for x in log if x["rodou"]]
    assert len(rodadas) == len(es), (len(rodadas), len(es))
    ultimo, nos = {}, []
    for i, (x, r) in enumerate(zip(rodadas, es)):
        deps = sorted({ultimo[f] for f in r["lidos"] if f in ultimo})
        nos.append({"ordem": i, "ferramenta": x["ferramenta"], "segundos": x["segundos"], "depende_de": deps, "lidos": r["lidos"], "gravados": r["gravados"]})
        for f in r["gravados"]:
            ultimo[f] = i
    # caminho crítico: o maior tempo acumulado por uma cadeia de dependências
    fim = []
    for n in nos:
        fim.append(n["segundos"] + max((fim[j] for j in n["depende_de"]), default=0.0))
    k = max(range(len(nos)), key=lambda i: fim[i])
    cadeia = []
    while True:
        cadeia.append(k)
        if not nos[k]["depende_de"]:
            break
        k = max(nos[k]["depende_de"], key=lambda j: fim[j])
    out = {"gerado_por": "tools/mapa_regeneracao.py", "data": date.today().isoformat(), "maquina": platform.processor() or platform.machine(),
           "total_sequencial_s": sum(n["segundos"] for n in nos), "caminho_critico_s": max(fim), "caminho_critico": [nos[i]["ferramenta"] for i in reversed(cadeia)],
           "nao_rodadas": [x for x in log if not x["rodou"]], "ferramentas": nos}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "mapa_regeneracao.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    md = ["# Mapa de dependências da regeneração (gerado por tools/mapa_regeneracao.py)", "",
          f"Observação de ambiente ({out['data']}, {out['maquina']}): tempos desta máquina. Total em série {out['total_sequencial_s'] / 60:.0f} min; caminho crítico {out['caminho_critico_s'] / 60:.0f} min.", "",
          "Caminho crítico: " + " → ".join(f"`{x}`" for x in out["caminho_critico"]), "",
          "| # | Ferramenta | Tempo (s) | Depende de (#) |", "| -: | :- | -: | :- |"]
    md += [f"| {n['ordem']} | `{n['ferramenta']}` | {n['segundos']:.0f} | {', '.join(str(j) for j in n['depende_de']) or '—'} |" for n in nos]
    (SAIDA / "mapa_regeneracao.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
