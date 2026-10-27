"""Regras de comparação de tools/confere_regeneracao.py (verificação de CI da regeneração de results/)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parents[1]


@pytest.fixture
def cr(monkeypatch):
    monkeypatch.syspath_prepend(str(RAIZ / "tools"))
    import confere_regeneracao

    return confere_regeneracao


def test_png_pixel_a_pixel_ignora_a_compressao(cr, tmp_path):
    import matplotlib.image as mpimg

    img = np.random.default_rng(0).random((20, 30, 3))
    a, b, c = tmp_path / "a.png", tmp_path / "b.png", tmp_path / "c.png"
    mpimg.imsave(a, img, pil_kwargs={"compress_level": 1})
    mpimg.imsave(b, img, pil_kwargs={"compress_level": 9})
    img2 = img.copy()
    img2[0, 0, 0] = 1.0 - img2[0, 0, 0]
    mpimg.imsave(c, img2)
    assert a.read_bytes() != b.read_bytes()
    assert cr._identicos(a, b)
    assert not cr._identicos(a, c)


def test_controle_compara_sem_o_hash(cr, tmp_path):
    a, b, c = tmp_path / "a.yaml", tmp_path / "b.yaml", tmp_path / "c.yaml"
    a.write_text("gerado_por: x\ncommit: 6eff417\nregenerados: 15\n", encoding="utf-8")
    b.write_text("gerado_por: x\ncommit: f7b4706\nregenerados: 15\n", encoding="utf-8")
    c.write_text("gerado_por: x\ncommit: f7b4706\nregenerados: 18\n", encoding="utf-8")
    rel = "results/etapa2.5/conferencia_2033.yaml"
    assert cr._identicos(a, b, rel) and not cr._identicos(a, c, rel)
    assert not cr._identicos(a, b, "results/outro.yaml")   # fora da lista de controle, byte a byte
    m1, m2 = tmp_path / "a.md", tmp_path / "b.md"
    m1.write_text("# t\n\nCommit 6eff417; plataformas 850\n", encoding="utf-8")
    m2.write_text("# t\n\nCommit f7b4706; plataformas 850\n", encoding="utf-8")
    assert cr._identicos(m1, m2, "results/etapa2.5/conferencia_2033.md")


def test_npz_array_a_array(cr, tmp_path):
    x = np.array([[1.0, np.nan], [2.0, 3.0]])
    np.savez_compressed(tmp_path / "a.npz", c3=x, datas=np.array(["2028-11-24"]))
    np.savez_compressed(tmp_path / "b.npz", c3=x.copy(), datas=np.array(["2028-11-24"]))
    y = x.copy()
    y[1, 1] = np.nextafter(3.0, 4.0)
    np.savez_compressed(tmp_path / "c.npz", c3=y, datas=np.array(["2028-11-24"]))
    assert cr._identicos(tmp_path / "a.npz", tmp_path / "b.npz")
    assert not cr._identicos(tmp_path / "a.npz", tmp_path / "c.npz")


def test_diferenca_numerica_em_markdown(cr):
    d = cr._difs_texto("| a | 22 768 | 6,372 |\n", "| a | 22 953 | 6,372 |\n")
    assert d == [("linha 1", "22 768", "22 953")]
    linha = cr._linha_dif(*d[0])
    assert linha["dif_abs"] == pytest.approx(185) and linha["dif_rel"] == pytest.approx(185 / 22768)
