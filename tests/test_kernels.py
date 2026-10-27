"""orbital.kernels: download e conferência do MD5 (sem rede: URLs file:// em diretório temporário)."""

from __future__ import annotations

import hashlib

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


def test_download_que_falha_nao_deixa_parcial_e_preserva_o_destino(tmp_path):
    cfg = _config(tmp_path, b"kernel")
    (tmp_path / "origem.bin").unlink()   # URL file:// inexistente: o download falha
    (tmp_path / "kernels").mkdir()
    (tmp_path / "kernels" / "k.bin").write_bytes(b"antigo")
    with pytest.raises(OSError):
        kernels.baixar(cfg, tmp_path, lambda _: None)
    assert (tmp_path / "kernels" / "k.bin").read_bytes() == b"antigo"
    assert not list((tmp_path / "kernels").glob("*.parcial"))
