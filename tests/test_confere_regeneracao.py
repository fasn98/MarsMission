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
    assert cr.avaliar(tmp_path / "a.npz", tmp_path / "b.npz")["estado"] == "identico"
    # 1 ulp: dentro da tolerância (P-039), listado como abaixo do limite
    r = cr.avaliar(tmp_path / "a.npz", tmp_path / "c.npz")
    assert r["estado"] == "tolerancia" and r["abaixo"][0]["dif_abs"] > 0
    z = x.copy()
    z[1, 1] = 3.0 * (1 + 1e-8)
    np.savez_compressed(tmp_path / "d.npz", c3=z, datas=np.array(["2028-11-24"]))
    assert cr.avaliar(tmp_path / "a.npz", tmp_path / "d.npz")["estado"] == "diferente"
    w = x.copy()
    w[0, 1] = 1.0   # NaN que vira número: nunca tolerado
    np.savez_compressed(tmp_path / "e.npz", c3=w, datas=np.array(["2028-11-24"]))
    assert cr.avaliar(tmp_path / "a.npz", tmp_path / "e.npz")["estado"] == "diferente"


def test_tolerancia_numerica_p039(cr, tmp_path):
    """P-039: passa se |a − b| ≤ max(1e-9 · |b|, 1e-10), a = versionado, b = regenerado (lidos de config/premissas.yaml)."""
    rtol, atol, fpx = cr._tolerancias()
    assert (rtol, atol, fpx) == (1e-9, 1e-10, 1e-3)
    # a forma exata: relativa sobre |b| (regenerado), com piso absoluto
    assert cr._dentro(1000.0 + 0.99e-6, 1000.0, rtol, atol) and not cr._dentro(1000.0 + 1.01e-6, 1000.0, rtol, atol)
    assert cr._dentro(1e-3 + 0.99e-10, 1e-3, rtol, atol) and not cr._dentro(1e-3 + 1.01e-10, 1e-3, rtol, atol)
    assert cr._dentro(0.99e-10, 0.0, rtol, atol) and not cr._dentro(1.01e-10, 0.0, rtol, atol)
    # Nota: com relativa 1e-9, a forma |b| e a forma max(|a|, |b|) só diferem em segunda ordem (~1e-18 relativo), o que
    # o float não representa; a forma |b| está no código (_dentro e o ramo NPZ de avaliar) e nos limites acima.
    a, b, c, z = tmp_path / "a.yaml", tmp_path / "b.yaml", tmp_path / "c.yaml", tmp_path / "z.yaml"
    a.write_text("c3: 9.597990318099248\nrel: -4.685807331155793e-08\nnome: x\n", encoding="utf-8")
    b.write_text("c3: 9.597990318099326\nrel: -4.6858071395951336e-08\nnome: x\n", encoding="utf-8")   # observado no CI
    c.write_text("c3: 9.597990327699248\nrel: -4.685807331155793e-08\nnome: x\n", encoding="utf-8")   # 1e-9 rel acima
    z.write_text("c3: 9.597990318099248\nrel: -4.685807331155793e-08\nnome: y\n", encoding="utf-8")
    r = cr.avaliar(a, b)
    assert r["estado"] == "tolerancia" and len(r["abaixo"]) == 2 and not r["acima"]
    assert cr.avaliar(a, c)["estado"] == "diferente"
    assert cr.avaliar(a, z)["estado"] == "diferente"   # texto nunca é tolerado


def test_png_ate_p040(cr, tmp_path):
    import matplotlib.image as mpimg

    img = np.zeros((100, 100, 3))
    a, b, c = tmp_path / "a.png", tmp_path / "b.png", tmp_path / "c.png"
    mpimg.imsave(a, img)
    img[0, :10] = 1.0       # 10 de 10 000 pixels = 0,1 %: no limite
    mpimg.imsave(b, img)
    img[1, :1] = 1.0        # 11 pixels: acima
    mpimg.imsave(c, img)
    assert cr.avaliar(a, b)["estado"] == "tolerancia"
    assert cr.avaliar(a, c)["estado"] == "diferente"


def test_diferenca_numerica_em_markdown(cr):
    d = cr._difs_texto("| a | 22 768 | 6,372 |\n", "| a | 22 953 | 6,372 |\n")
    assert d == [("linha 1", "22 768", "22 953")]
    linha = cr._linha_dif(*d[0])
    assert linha["dif_abs"] == pytest.approx(185) and linha["dif_rel"] == pytest.approx(185 / 22768)


@pytest.mark.parametrize("caso, a, b, passa", [
    # passa só pelo critério relativo: |a − b| = 5e-7 > piso 1e-10, mas ≤ 1e-9 · |b| = 1e-6
    ("so_relativo", 1000.0 + 5e-7, 1000.0, True),
    # passa só pelo piso absoluto: |a − b| = 5e-11 > 1e-9 · |b| = 1e-12, mas ≤ piso 1e-10
    ("so_piso", 1e-3 + 5e-11, 1e-3, True),
    # falha nos dois: |a − b| = 5e-10 > 1e-9 · |b| = 1e-12 e > piso 1e-10
    ("falha_nos_dois", 1e-3 + 5e-10, 1e-3, False),
])
def test_p039_relativo_piso_e_falha(cr, caso, a, b, passa):
    """Os três casos da P-039 (passa se |a − b| ≤ max(1e-9 · |b|, 1e-10)), com cada critério conferido isoladamente."""
    rtol, atol, _ = cr._tolerancias()
    d = abs(a - b)
    pelo_relativo, pelo_piso = d <= rtol * abs(b), d <= atol
    assert (pelo_relativo, pelo_piso) == {"so_relativo": (True, False), "so_piso": (False, True),
                                          "falha_nos_dois": (False, False)}[caso]
    assert cr._dentro(a, b, rtol, atol) is passa


def test_ambiente_registra_pacotes_do_pyproject_cpu_sistema_e_commit(cr):
    """O relatório lista todas as dependências do pyproject.toml (inclusive o pillow), o Python, a CPU, o sistema e o commit."""
    import tomllib

    proj = tomllib.loads((RAIZ / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    reqs = proj["dependencies"] + [r for extra in proj["optional-dependencies"].values() for r in extra]
    nomes = {r.split(";")[0].split("[")[0].split("=")[0].split(">")[0].split("<")[0].strip().lower() for r in reqs}
    assert set(cr.pacotes()) == nomes and {"pillow", "streamlit", "pandas", "pytest"} <= nomes
    amb = cr.ambiente()
    assert list(amb)[0] == "python" and list(amb)[-1] == "alteracoes_nao_commitadas"
    assert {"cpu", "sistema", "commit"} <= set(amb) and amb["pillow"] and amb["cpu"] and amb["sistema"]
    if amb["commit"] is not None:   # com git disponível, o commit é o SHA do HEAD
        assert len(amb["commit"]) == 40 and isinstance(amb["alteracoes_nao_commitadas"], bool)


def test_linha_de_ambiente_do_markdown(cr):
    amb = {"python": "3.11.18", "pillow": "13.0.0", "pandas": None, "cpu": "X", "sistema": "Linux", "commit": None,
           "alteracoes_nao_commitadas": True}
    assert cr.ambiente_md(amb) == ("python 3.11.18, pillow 13.0.0, pandas ausente, cpu X, sistema Linux "
                                   "(árvore de trabalho com alterações não commitadas)")
    amb.update(commit="a" * 40, alteracoes_nao_commitadas=False)
    assert cr.ambiente_md(amb).endswith(f"commit {'a' * 40}")
