"""Valores de config da época de etapas antigas, aplicados numa cópia do repositório só para regenerá-las como registro
(tools/confere_regeneracao.py, tools/confere_2033.py). Ver antes_etapa_3_1 em config/motores.yaml e antes_etapa_4_5 em
config/lista_massas.yaml."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ARQUIVOS_3_1 = ("config/dimensionamento.yaml", "config/superficie.yaml", "config/mav_propulsao.yaml")


def _trocar(d: Path, origem: str, chave: str) -> None:
    trocas = yaml.safe_load((d / origem).read_text(encoding="utf-8"))[chave]
    for t in trocas:
        p = d / t["arquivo"]
        txt, n = re.subn(t["procura"], lambda _: t["troca"], p.read_text(encoding="utf-8"), flags=re.M)
        if n != 1:
            raise RuntimeError(f"{chave}: {t['arquivo']}: {n} ocorrências de {t['procura']!r} (esperada 1)")
        p.write_text(txt, encoding="utf-8")


def aplicar_antes_etapa_3_1(d: Path) -> None:
    """Volta, na cópia `d`, as linhas do config mudadas no redimensionamento da Etapa 3.1 (ADR 0011) aos valores antigos."""
    _trocar(d, "config/motores.yaml", "antes_etapa_3_1")


def aplicar_antes_etapa_4_5(d: Path) -> None:
    """Volta, na cópia `d`, as linhas do config mudadas no portão da Etapa 4.5 (circuito de fluido no estágio de cruzeiro)."""
    _trocar(d, "config/lista_massas.yaml", "antes_etapa_4_5")
