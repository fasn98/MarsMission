"""Download e conferência (MD5) dos kernels SPICE listados num arquivo de config (padrão: config/kernels.yaml).

Usado por tools/fetch_kernels.py (linha de comando) e pelo painel, que baixa os kernels na primeira execução quando
eles faltam (Streamlit Community Cloud). Só baixa o que falta ou não confere com o MD5 do config; o download vai para
um arquivo temporário no mesmo diretório e só substitui o destino depois de completo.
"""

from __future__ import annotations

import hashlib
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable

import yaml

from orbital.ephemeris import CONFIG_KERNELS, RAIZ

CONFIG_OPERACIONAL = RAIZ / "config" / "operacional.yaml"


def timeout_padrao() -> float:
    """Prazo por arquivo, em segundos (parâmetro operacional de config/operacional.yaml, não premissa científica)."""
    return float(yaml.safe_load(CONFIG_OPERACIONAL.read_text(encoding="utf-8"))["download_kernels"]["timeout_s"]["valor"])


def _baixar_arquivo(url: str, destino: Path, timeout_s: float) -> None:
    """Copia `url` para `destino` em blocos. `timeout_s` vale para cada operação de rede e para o arquivo inteiro:
    passou do prazo, TimeoutError com mensagem clara (uma conexão lenta que nunca para também é interrompida)."""
    erro = TimeoutError(f"o download de {url} passou do prazo de {timeout_s:g} s (config/operacional.yaml)")
    inicio = time.monotonic()
    try:
        with urllib.request.urlopen(url, timeout=timeout_s) as r, destino.open("wb") as f:
            while bloco := r.read(1 << 20):
                f.write(bloco)
                if time.monotonic() - inicio > timeout_s:
                    raise erro
    except TimeoutError as e:
        raise erro from e
    except urllib.error.URLError as e:
        if isinstance(e.reason, TimeoutError):
            raise erro from e
        raise


def md5(caminho: Path) -> str:
    h = hashlib.md5()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def baixar(config: Path = CONFIG_KERNELS, raiz: Path = RAIZ, avisar: Callable[[str], None] = print,
           timeout_s: float | None = None) -> list[dict]:
    """Baixa os kernels do config que faltam ou cujo MD5 não confere e devolve, por kernel, o MD5 esperado e o obtido.
    O diretório do config ("diretorio") é relativo a `raiz`. `timeout_s` (padrão: config/operacional.yaml) é o prazo
    por arquivo; passou dele, TimeoutError."""
    timeout_s = timeout_padrao() if timeout_s is None else timeout_s
    cfg = yaml.safe_load(Path(config).read_text(encoding="utf-8"))
    diretorio = raiz / cfg["diretorio"]
    diretorio.mkdir(parents=True, exist_ok=True)
    out = []
    for k in cfg["kernels"]:
        destino = diretorio / k["arquivo"]
        esperado = str(k["md5"])   # um MD5 só de dígitos sem aspas vira inteiro no YAML (e perde zeros à esquerda: não confere)
        if not destino.exists() or md5(destino) != esperado:
            avisar(f"baixando {k['url']}")
            parcial = destino.with_name(destino.name + ".parcial")
            try:
                _baixar_arquivo(k["url"], parcial, timeout_s)
                os.replace(parcial, destino)
            finally:
                parcial.unlink(missing_ok=True)
        obtido = md5(destino)
        out.append({"arquivo": k["arquivo"], "md5_esperado": esperado, "md5_obtido": obtido, "ok": obtido == esperado})
    return out


def garantir(config: Path = CONFIG_KERNELS, raiz: Path = RAIZ, avisar: Callable[[str], None] = print,
             timeout_s: float | None = None) -> list[dict]:
    """Como `baixar`, mas levanta ValueError se algum MD5 não conferir (o painel mostra a mensagem e não carrega)."""
    res = baixar(config, raiz, avisar, timeout_s)
    falhas = [r for r in res if not r["ok"]]
    if falhas:
        raise ValueError("MD5 dos kernels não confere com " + Path(config).name + ": " + "; ".join(
            f"{r['arquivo']} esperado {r['md5_esperado']}, obtido {r['md5_obtido']}" for r in falhas))
    return res
