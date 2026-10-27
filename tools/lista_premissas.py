"""Lista as premissas de config/premissas.yaml em results/fase1/premissas.md (sem edição à mão).

Uso: python tools/lista_premissas.py
"""

from __future__ import annotations

from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]


def main():
    ps = yaml.safe_load((RAIZ / "config/premissas.yaml").read_text(encoding="utf-8"))["premissas"]
    md = ["# Premissas da Fase 1 (gerado por tools/lista_premissas.py a partir de config/premissas.yaml)", "",
          "| Id | Nome | Valor | Unidade | Status | Uso |", "| :- | :- | :- | :- | :- | :- |"]
    for p in ps:
        valor = p["valor"]
        if isinstance(valor, dict):
            valor = "; ".join(f"{k}: {v}" for k, v in valor.items())
        md.append(f"| {p['id']} | {p['nome']} | {valor} | {p.get('unidade', '')} | {p['status']} | {p['uso']} |")
    nv = sum(p["status"] == "NÃO VALIDADA" for p in ps)
    md += ["", f"Total: {len(ps)} premissas, {nv} com status NÃO VALIDADA. Justificativas em config/premissas.yaml."]
    saida = RAIZ / "results/fase1/premissas.md"
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[-1:]))


if __name__ == "__main__":
    main()
