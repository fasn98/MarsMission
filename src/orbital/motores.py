"""Catálogo de motores (config/motores.yaml, Etapa 3.1) e conjuntos de propulsão das combinações propostas."""

from __future__ import annotations

import math
from dataclasses import dataclass

from orbital.config import ler, v
from orbital.queima_finita import Motor


def _valor_si(item: dict, conversao: dict) -> float:
    """Valor em N ou kg: `valor` direto, ou `valor_original` em lbf/lb convertido pelos fatores do NIST SP 811."""
    if "valor" in item:
        return float(item["valor"])
    fator = {"lbf": "lbf_para_n", "lb": "lb_para_kg"}[item["unidade_original"]]
    return float(item["valor_original"]) * v(conversao[fator])


@dataclass(frozen=True)
class Conjunto:
    """Motores de uma combinação que queimam juntos (mesmo Isp em todos, como nas combinações do config)."""
    nome: str
    descricao: str
    motor: Motor              # empuxo total e Isp
    massa_kg: float           # soma das massas dos motores
    queima_unica_max_s: float # a menor entre os motores do conjunto (nan se nenhuma fonte)
    nota: str


def catalogo(cfg: dict | None = None) -> dict:
    """Motores do catálogo com empuxo (N), Isp (s), massa (kg) e queima única máxima (s) em unidades SI."""
    cfg = ler("config/motores.yaml") if cfg is None else cfg
    conv = cfg["conversao"]
    out = {}
    for nome, m in cfg["motores"].items():
        out[nome] = {"nome": m["nome"], "propelentes": m["propelentes"], "empuxo_n": _valor_si(m["empuxo_n"], conv),
                     "isp_s": float(m["isp_s"]["valor"]), "massa_kg": _valor_si(m["massa_kg"], conv),
                     "queima_unica_max_s": float(m["queima_unica_max_s"]["valor"]) if "queima_unica_max_s" in m else float("nan"),
                     "sem_combinacao": "fora_das_combinacoes" in m}
    return out


def conjuntos(funcao: str, cfg: dict | None = None) -> list[Conjunto]:
    """Conjuntos das combinações propostas para uma função (captura, retorno, cruzeiro, mav_1, mav_2)."""
    cfg = ler("config/motores.yaml") if cfg is None else cfg
    cat = catalogo(cfg)
    out = []
    for nome, c in cfg["combinacoes"][funcao].items():
        partes = [(cat[p["motor"]], int(p["quantidade"]), p["motor"]) for p in c["motores"]]
        isps = {m["isp_s"] for m, _, _ in partes}
        if len(isps) != 1:
            raise ValueError(f"combinação {nome}: motores com Isp diferentes não são tratados")
        empuxo = sum(m["empuxo_n"] * q for m, q, _ in partes)
        massa = sum(m["massa_kg"] * q for m, q, _ in partes)
        desc = " + ".join(f"{q} × {chave}" for _, q, chave in partes)
        out.append(Conjunto(nome, desc, Motor(empuxo, isps.pop()), massa,
                            min((m["queima_unica_max_s"] for m, _, _ in partes), key=lambda x: (math.isnan(x), x)), c.get("nota", "")))
    return out
