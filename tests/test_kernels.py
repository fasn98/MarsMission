"""orbital.kernels: download e conferência do MD5 (sem rede: URLs file:// em diretório temporário)."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
import yaml

from orbital import kernels


def _config(tmp_path, conteudo: bytes, md5: str | None = None):
    origem = tmp_path / "origem.bin"
    origem.write_bytes(conteudo)
    cfg = tmp_path / "kernels.yaml"
    cfg.write_text(yaml.safe_dump({"diretorio": "kernels", "kernels": [
        {"arquivo": "k.bin", "url": origem.as_uri(), "md5": md5 or hashlib.md5(conteudo).hexdigest()}]}))
    return cfg


def test_baixa_o_que_falta_e_confere(tmp_path):
    cfg = _config(tmp_path, b"kernel")
    avisos = []
    r = kernels.baixar(cfg, tmp_path, avisos.append)
    assert r[0]["ok"] and (tmp_path / "kernels" / "k.bin").read_bytes() == b"kernel"
    assert len(avisos) == 1 and not list((tmp_path / "kernels").glob("*.parcial"))
    avisos.clear()
    kernels.baixar(cfg, tmp_path, avisos.append)
    assert avisos == []   # presente e com o MD5 certo: não baixa de novo


def test_garantir_falha_com_mensagem_clara_se_o_md5_nao_confere(tmp_path):
    cfg = _config(tmp_path, b"kernel", md5="0" * 32)
    with pytest.raises(ValueError, match=r"MD5 dos kernels não confere com kernels\.yaml: k\.bin esperado 0{32}, obtido"):
        kernels.garantir(cfg, tmp_path, lambda _: None)


def test_arquivo_corrompido_e_baixado_de_novo(tmp_path):
    cfg = _config(tmp_path, b"kernel")
    (tmp_path / "kernels").mkdir()
    (tmp_path / "kernels" / "k.bin").write_bytes(b"corrompido")
    assert kernels.garantir(cfg, tmp_path, lambda _: None)[0]["ok"]
    assert (tmp_path / "kernels" / "k.bin").read_bytes() == b"kernel"


def test_config_real_tem_md5_e_url_para_todos_os_kernels():
    cfg = yaml.safe_load(kernels.CONFIG_KERNELS.read_text(encoding="utf-8"))
    assert cfg["kernels"] and all(len(k["md5"]) == 32 and k["url"].startswith("https://") for k in cfg["kernels"])


class _Conexao:
    """Resposta falsa de urlopen: devolve os blocos dados e, depois deles, levanta `erro` (se houver)."""

    def __init__(self, blocos, erro=None):
        self.blocos, self.erro = list(blocos), erro

    def read(self, n):
        if self.blocos:
            return self.blocos.pop(0)
        if self.erro:
            raise self.erro
        return b""

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _destino_antigo(tmp_path):
    (tmp_path / "kernels").mkdir()
    (tmp_path / "kernels" / "k.bin").write_bytes(b"antigo")


def _sem_parcial_e_preservado(tmp_path):
    assert (tmp_path / "kernels" / "k.bin").read_bytes() == b"antigo"
    assert not list((tmp_path / "kernels").glob("*.parcial"))


def test_download_que_falha_no_meio_nao_deixa_parcial_e_preserva_o_destino(tmp_path, monkeypatch):
    cfg = _config(tmp_path, b"kernel")
    _destino_antigo(tmp_path)
    vistos = []

    def urlopen(url, timeout):
        vistos.append(timeout)
        return _Conexao([b"ker"], OSError("conexão interrompida"))   # começa a escrever o .parcial e a conexão cai

    monkeypatch.setattr(kernels.urllib.request, "urlopen", urlopen)
    with pytest.raises(OSError, match="interrompida"):
        kernels.baixar(cfg, tmp_path, lambda _: None)
    assert vistos == [kernels.timeout_padrao()]   # o timeout de rede vem de config/operacional.yaml
    _sem_parcial_e_preservado(tmp_path)


def test_download_lento_passa_do_prazo_por_arquivo(tmp_path, monkeypatch):
    """Conexão que nunca para de mandar dados devagar: o prazo vale para o arquivo inteiro, não só para cada leitura."""
    cfg = _config(tmp_path, b"kernel")
    _destino_antigo(tmp_path)
    relogio = iter(range(0, 10_000, 50))   # cada leitura "leva" 50 s
    monkeypatch.setattr(kernels.time, "monotonic", lambda: next(relogio))
    monkeypatch.setattr(kernels.urllib.request, "urlopen", lambda url, timeout: _Conexao([b"k"] * 100))
    with pytest.raises(TimeoutError, match=r"passou do prazo de 120 s \(config/operacional\.yaml\)"):
        kernels.baixar(cfg, tmp_path, lambda _: None, timeout_s=120)
    _sem_parcial_e_preservado(tmp_path)


def test_timeout_de_rede_vira_a_mesma_mensagem(tmp_path, monkeypatch):
    cfg = _config(tmp_path, b"kernel")
    _destino_antigo(tmp_path)

    def urlopen(url, timeout):
        raise kernels.urllib.error.URLError(TimeoutError("timed out"))   # conexão que não abre

    monkeypatch.setattr(kernels.urllib.request, "urlopen", urlopen)
    with pytest.raises(TimeoutError, match="passou do prazo de 7 s"):
        kernels.baixar(cfg, tmp_path, lambda _: None, timeout_s=7)
    _sem_parcial_e_preservado(tmp_path)


def test_timeout_e_parametro_operacional_fora_das_premissas():
    op = yaml.safe_load(kernels.CONFIG_OPERACIONAL.read_text(encoding="utf-8"))["download_kernels"]["timeout_s"]
    assert op["tipo"] == "parâmetro operacional" and op["justificativa"] and kernels.timeout_padrao() == op["valor"]
    assert "timeout" not in kernels.RAIZ.joinpath("config", "premissas.yaml").read_text(encoding="utf-8").lower()
