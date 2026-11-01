"""Lista as premissas de config/premissas.yaml em results/fase1/premissas.md e, só as NÃO VALIDADAS, em
results/fase2/, results/fase3/ e results/fase4/premissas_nao_validadas.md (sem edição à mão). As listas das Fases 3 e 4
marcam as premissas criadas nelas: as premissas são numeradas em ordem de criação; a primeira da Fase 3 é a P-041
(Etapa 3.1) e a primeira da Fase 4 é a P-050 (Etapa 4.1).

Uso: python tools/lista_premissas.py
"""

from __future__ import annotations

from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
PRIMEIRA_DA_FASE_3 = 41
PRIMEIRA_DA_FASE_4 = 50


def main():
    ps = yaml.safe_load((RAIZ / "config/premissas.yaml").read_text(encoding="utf-8"))["premissas"]
    md = ["# Premissas da Fase 1 (gerado por tools/lista_premissas.py a partir de config/premissas.yaml)", "",
          "| Id | Nome | Valor | Unidade | Status | Uso |", "| :- | :- | :- | :- | :- | :- |"]
    for p in ps:
        valor = p["valor"]
        if isinstance(valor, dict):
            valor = "; ".join(f"{k}: {v}" for k, v in valor.items())
        md.append(f"| {p['id']} | {p['nome']}{' (CRÍTICA)' if p.get('critica') else ''} | {valor} | {p.get('unidade', '')} | {p['status']} | {p['uso']} |")
    nv = sum(p["status"] == "NÃO VALIDADA" for p in ps)
    md += ["", f"Total: {len(ps)} premissas, {nv} com status NÃO VALIDADA. Justificativas em config/premissas.yaml."]
    saida = RAIZ / "results/fase1/premissas.md"
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(md) + "\n", encoding="utf-8")
    nao = [p for p in ps if p["status"] == "NÃO VALIDADA"]
    md2 = ["# Premissas NÃO VALIDADAS ao fim da Fase 2 (gerado por tools/lista_premissas.py)", "",
           "Só o Fabio altera o status. Justificativas completas em config/premissas.yaml.", "",
           "| Id | Nome | Valor | Unidade | Uso |", "| :- | :- | :- | :- | :- |"]
    for p in nao:
        valor = p["valor"]
        if isinstance(valor, dict):
            valor = "; ".join(f"{k}: {v}" for k, v in valor.items())
        md2.append(f"| {p['id']} | {p['nome']}{' (CRÍTICA)' if p.get('critica') else ''} | {valor} | {p.get('unidade', '')} | {p['uso']} |")
    md2 += ["", f"Total: {len(nao)} de {len(ps)} premissas com status NÃO VALIDADA."]
    s2 = RAIZ / "results/fase2/premissas_nao_validadas.md"
    s2.parent.mkdir(parents=True, exist_ok=True)
    s2.write_text("\n".join(md2) + "\n", encoding="utf-8")
    md3 = ["# Premissas NÃO VALIDADAS ao fim da Fase 3 (gerado por tools/lista_premissas.py)", "",
           "Só o Fabio altera o status. Justificativas completas em config/premissas.yaml. \"Fase 3\" marca as criadas nela.", "",
           "| Id | Nome | Valor | Unidade | Uso | Fase 3 |", "| :- | :- | :- | :- | :- | :- |"]
    novas = 0
    for p in nao:
        valor = p["valor"]
        if isinstance(valor, dict):
            valor = "; ".join(f"{k}: {v}" for k, v in valor.items())
        f3 = int(p["id"][2:]) >= PRIMEIRA_DA_FASE_3
        novas += f3
        md3.append(f"| {p['id']} | {p['nome']}{' (CRÍTICA)' if p.get('critica') else ''} | {valor} | {p.get('unidade', '')} | {p['uso']} | {'sim' if f3 else ''} |")
    md3 += ["", f"Total: {len(nao)} de {len(ps)} premissas com status NÃO VALIDADA; {novas} criadas na Fase 3."]
    s3 = RAIZ / "results/fase3/premissas_nao_validadas.md"
    s3.parent.mkdir(parents=True, exist_ok=True)
    s3.write_text("\n".join(md3) + "\n", encoding="utf-8")
    md4 = ["# Premissas NÃO VALIDADAS ao fim da Fase 4 (gerado por tools/lista_premissas.py)", "",
           "Só o Fabio altera o status. Justificativas completas em config/premissas.yaml. \"Fase 4\" marca as criadas nela.", "",
           "| Id | Nome | Valor | Unidade | Uso | Fase 4 |", "| :- | :- | :- | :- | :- | :- |"]
    novas4 = 0
    for p in nao:
        valor = p["valor"]
        if isinstance(valor, dict):
            valor = "; ".join(f"{k}: {v}" for k, v in valor.items())
        f4 = int(p["id"][2:]) >= PRIMEIRA_DA_FASE_4
        novas4 += f4
        md4.append(f"| {p['id']} | {p['nome']}{' (CRÍTICA)' if p.get('critica') else ''} | {valor} | {p.get('unidade', '')} | {p['uso']} | {'sim' if f4 else ''} |")
    md4 += ["", f"Total: {len(nao)} de {len(ps)} premissas com status NÃO VALIDADA; {novas4} criadas na Fase 4."]
    s4 = RAIZ / "results/fase4/premissas_nao_validadas.md"
    s4.parent.mkdir(parents=True, exist_ok=True)
    s4.write_text("\n".join(md4) + "\n", encoding="utf-8")
    print("\n".join(md[-1:]))


if __name__ == "__main__":
    main()
