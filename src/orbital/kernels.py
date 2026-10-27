"""Download e conferência (MD5) dos kernels SPICE listados num arquivo de config (padrão: config/kernels.yaml).

Usado por tools/fetch_kernels.py (linha de comando) e pelo painel, que baixa os kernels na primeira execução quando
eles faltam (Streamlit Community Cloud). Só baixa o que falta ou não confere com o MD5 do config; o download vai para
um arquivo temporário no mesmo diretório e só substitui o destino depois de completo.
"""

from __future__ import annotations

import hashlib
import os
import urllib.request
from pathlib import Path
from typing import Callable

import yaml

from orbital.ephemeris import CONFIG_KERNELS, RAIZ


def md5(caminho: Path) -> str:
    h = hashlib.md5()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def baixar(config: Path = CONFIG_KERNELS, raiz: Path = RAIZ, avisar: Callable[[str], None] = print) -> list[dict]:
    """Baixa os kernels do config que faltam ou cujo MD5 não confere e devolve, por kernel, o MD5 esperado e o obtido.
    O diretório do config ("diretorio") é relativo a `raiz`."""
    cfg = yaml.safe_load(Path(config).read_text(encoding="utf-8"))
    diretorio = raiz / cfg["diretorio"]
    diretorio.mkdir(parents=True, exist_ok=True)
    out = []
    for k in cfg["kernels"]:
        destino = diretorio / k["arquivo"]
        esperado = str(k["md5"])   # texto: um MD5 só de dígitos, sem aspas no YAML, seria lido como inteiro
        if not destino.exists() or md5(destino) != esperado:
            avisar(f"baixando {k['url']}")
            parcial = destino.with_name(destino.name + ".parcial")
            try:
                urllib.request.urlretrieve(k["url"], parcial)
                os.replace(parcial, destino)
            finally:
                parcial.unlink(missing_ok=True)
        obtido = md5(destino)
        out.append({"arquivo": k["arquivo"], "md5_esperado": esperado, "md5_obtido": obtido, "ok": obtido == esperado})
    return out


def garantir(config: Path = CONFIG_KERNELS, raiz: Path = RAIZ, avisar: Callable[[str], None] = print) -> list[dict]:
    """Como `baixar`, mas levanta ValueError se algum MD5 não conferir (o painel mostra a mensagem e não carrega)."""
    res = baixar(config, raiz, avisar)
    falhas = [r for r in res if not r["ok"]]
    if falhas:
        raise ValueError("MD5 dos kernels não confere com " + Path(config).name + ": " + "; ".join(
            f"{r['arquivo']} esperado {r['md5_esperado']}, obtido {r['md5_obtido']}" for r in falhas))
    return res
