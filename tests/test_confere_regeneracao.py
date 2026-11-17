"""Regras de comparação de tools/confere_regeneracao.py (verificação de CI da regeneração de results/)."""

from __future__ import annotations

import os
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
    amb = cr.ambiente()   # o git de ambiente() é conferido em test_ambiente_ignora_git_do_hook, num repositório de prova
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


def test_partes_da_regeneracao_paralela(cr):
    """Issue #61: as partes cobrem FASE_ATUAL uma vez, e o workflow declara, para cada parte, as mesmas dependências de
    tools/regeneracao_partes.yaml (needs e entradas)."""
    import yaml
    ps = cr.partes()
    wf = yaml.safe_load((cr.RAIZ / ".github/workflows/regeneracao.yml").read_text(encoding="utf-8"))["jobs"]
    por_parte = {j["with"]["parte"]: j for j in wf.values() if "with" in j}
    assert set(por_parte) == set(ps)
    # portão (verificação obrigatória da main): depende de todos os jobs de parte e roda sempre
    assert set(wf["portao"]["needs"]) == set(wf) - {"portao"} and wf["portao"]["if"] == "always()"
    for nome, p in ps.items():
        j = por_parte[nome]
        assert set(j.get("needs", [])) - {"detecta"} == set(p["depende_de"])   # detecta: test_detector_de_mudanca_relevante
        assert set(j["with"].get("entradas", "").split()) == set(p["depende_de"])


def test_juntar_entradas_recusa_conflito(cr, tmp_path):
    """Duas partes que entregam o mesmo arquivo com conteúdo diferente são erro."""
    a, b, d = tmp_path / "a", tmp_path / "b", tmp_path / "d"
    for x, t in ((a, "1"), (b, "2")):
        (x / "etapa").mkdir(parents=True)
        (x / "etapa" / "r.yaml").write_text(t)
    d.mkdir()
    with pytest.raises(RuntimeError):
        cr.juntar_entradas(d, [a, b])


def test_partes_conferem_com_o_mapa(cr):
    """Issue #61: pelo mapa de dependências (results/conferencia/mapa_regeneracao.yaml), toda ferramenta de que uma parte
    depende está nela ou numa parte declarada em depende_de (cujos resultados ela baixa), e nenhum arquivo é gravado por
    duas partes (o rastreio não registra a leitura de um arquivo que a própria ferramenta regrava)."""
    import yaml
    ps = cr.partes()
    mapa = yaml.safe_load((cr.RAIZ / "results/conferencia/mapa_regeneracao.yaml").read_text(encoding="utf-8"))["ferramentas"]
    parte_de = {f: n for n, p in ps.items() for f in p["ferramentas"]}
    stem = [Path(n["ferramenta"].split()[0]).stem for n in mapa]
    # o mapa precisa ser da ordem atual da regeneração (senão uma ferramenta nova cairia na base sem conferência)
    assert [n["ferramenta"] for n in mapa] == [" ".join(c) for c in cr.FASE_1 + cr.FASE_850 + cr.FASE_ATUAL]
    p_de = [parte_de.get(s, "base") for s in stem]   # fora de FASE_ATUAL: fases históricas, na base
    gravado_por = {}
    for i, n in enumerate(mapa):
        for j in n["depende_de"]:
            assert p_de[j] == p_de[i] or p_de[j] in ps[p_de[i]]["depende_de"], (stem[i], stem[j])
        for f in n["gravados"]:
            assert gravado_por.setdefault(f, p_de[i]) == p_de[i], f


def test_diagnostico_nao_finito(cr):
    for s in ("nan", "NaN", "-inf", "−inf", "+Inf", "infinity", "∞", "diferença: nan."):
        assert cr.NAO_FINITO.search(s), s
    for s in ("Ainf", "1inf", "informação", "nano", "finança", "1,5e-09"):
        assert not cr.NAO_FINITO.search(s), s


def test_logs_das_entradas_com_ambiente(cr, tmp_path):
    import json
    (tmp_path / "a" / "_log").mkdir(parents=True)
    (tmp_path / "a" / "_log" / "base.json").write_text(json.dumps({"ambiente": {"cpu": "x"}, "log": [{"ferramenta": "t", "rodou": True}]}))
    log, amb = cr.logs_das_entradas([tmp_path / "a", tmp_path / "vazia"])
    assert log == [{"ferramenta": "t", "rodou": True}] and amb == {"base": {"cpu": "x"}}


def _wf(cr):
    import yaml
    return yaml.safe_load((cr.RAIZ / ".github/workflows/regeneracao.yml").read_text(encoding="utf-8"))


def test_detector_de_mudanca_relevante(cr):
    """Sem filtro de caminhos no gatilho (decisão do Fabio, 2026-11-17): o job "detecta" decide se a regeneração roda; só a
    base depende dele (as demais partes herdam o pulo), e o portão o lê. Os caminhos são os do antigo filtro."""
    d = _wf(cr)
    assert all("paths" not in (g or {}) and "paths-ignore" not in (g or {}) for g in d[True].values())   # "on" → True
    jobs = d["jobs"]
    assert jobs["base"]["needs"] == ["detecta"] and jobs["base"]["if"] == "needs.detecta.outputs.relevante == 'true'"
    assert [n for n, j in jobs.items() if "detecta" in j.get("needs", [])] == ["base", "portao"]
    passo = next(s for s in jobs["detecta"]["steps"] if s.get("id") == "diff")
    assert passo["env"]["CAMINHOS"].split() == ["src", "tools", "config", "results", "tests/data", "cad/featurescript", "environment.yml", "pyproject.toml",
                                                ".github/workflows/regeneracao.yml", ".github/workflows/regeneracao_parte.yml"]
    # quem lê o modelo de FeatureScript para gerar results/ (decisão do Fabio, 2026-11-17)
    for f in ("tools/cad_parametros.py", "tools/encaixe_coifas.py"):
        assert 'RAIZ / "cad" / "featurescript"' in (cr.RAIZ / f).read_text(encoding="utf-8"), f


def _sem_git(env: dict) -> dict:
    """Ambiente sem GIT_* (no hook de pre-commit vêm GIT_DIR e GIT_INDEX_FILE, que apontariam o git dos repositórios de
    prova para o repositório de verdade), e sem a configuração global e de sistema (hooks, gpgsign, templateDir)."""
    return {**{k: v for k, v in env.items() if not k.startswith("GIT_")}, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}


def _roda_detector(cr, repo, env):
    """Roda o passo do detector (o script do workflow) num repositório de prova; devolve a saída "relevante"."""
    import os
    import subprocess
    passo = next(s for s in _wf(cr)["jobs"]["detecta"]["steps"] if s.get("id") == "diff")
    saida, resumo, tmp = repo.parent / "_saida", repo.parent / "_resumo", repo.parent / "_tmp"   # fora do repositório
    tmp.mkdir(exist_ok=True)
    saida.write_text("")
    fixos = {k: v for k, v in passo["env"].items() if "${{" not in v}   # CAMINHOS; os de evento vêm de env
    amb = {**_sem_git(dict(os.environ)), **fixos, **env, "GITHUB_OUTPUT": str(saida), "GITHUB_STEP_SUMMARY": str(resumo), "RUNNER_TEMP": str(tmp)}
    subprocess.run(["bash", "-c", passo["run"]], cwd=repo, env=amb, check=True, capture_output=True)
    linhas = [x for x in saida.read_text(encoding="utf-8").splitlines() if x.startswith("relevante=")]
    assert len(linhas) == 1
    return linhas[0].split("=", 1)[1]


def _git(repo, *a):
    import os
    import subprocess
    return subprocess.run(["git", "-c", "user.name=x", "-c", "user.email=x@x", *a], cwd=repo, check=True,
                          capture_output=True, text=True, env=_sem_git(dict(os.environ))).stdout.strip()


@pytest.fixture
def repo_prova(tmp_path):
    """Repositório com a main (results/foo.md, docs/a.md) e uma função que cria um PR e o merge sintético do GitHub."""
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q", "-b", "main")
    assert _git(r, "rev-parse", "--show-toplevel") == str(r.resolve())   # o git dos testes age só no repositório de prova
    (r / "results").mkdir()
    (r / "docs").mkdir()
    (r / "results" / "foo.md").write_text("\n".join(map(str, range(50))))
    (r / "docs" / "a.md").write_text("a")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "base")

    n = [0]

    def pr(mudar):
        """Cria um branch a partir da main com a mudança e deixa o HEAD no merge sintético (pais: main, head do PR)."""
        n[0] += 1
        _git(r, "checkout", "-q", "-b", f"pr{n[0]}", "main")
        mudar(r)
        _git(r, "add", "-A")
        _git(r, "commit", "-qm", "pr")
        cabeca = _git(r, "rev-parse", "HEAD")
        _git(r, "checkout", "-q", "--detach", "main")
        _git(r, "merge", "-q", "--no-ff", "-m", "merge sintético", f"pr{n[0]}")
        return cabeca
    return r, pr


def test_detector_so_documentacao(cr, repo_prova):
    r, pr = repo_prova
    cabeca = pr(lambda r: (r / "docs" / "a.md").write_text("b"))
    assert _roda_detector(cr, r, {"EVENTO": "pull_request", "CABECA_PR": cabeca, "ANTES": ""}) == "false"


def test_detector_ferramenta_renomeacao_e_acento(cr, repo_prova):
    """Um arquivo de results/ movido para docs/ (o diff com renomeação só mostraria docs/) e um caminho com acento (que o
    core.quotePath poria entre aspas) contam como relevantes."""
    r, pr = repo_prova

    def mover(r):
        (r / "results" / "foo.md").rename(r / "docs" / "foo.md")
    cabeca = pr(mover)
    assert _roda_detector(cr, r, {"EVENTO": "pull_request", "CABECA_PR": cabeca, "ANTES": ""}) == "true"

    def acento(r):
        (r / "config").mkdir()
        (r / "config" / "órbita.yaml").write_text("x")
    cabeca = pr(acento)
    assert _roda_detector(cr, r, {"EVENTO": "pull_request", "CABECA_PR": cabeca, "ANTES": ""}) == "true"


def test_detector_falha_fechada(cr, repo_prova):
    """Sem base conferida, regenera: head do PR que não é o segundo pai, push sem before, before inexistente."""
    r, pr = repo_prova
    pr(lambda r: (r / "docs" / "a.md").write_text("b"))
    assert _roda_detector(cr, r, {"EVENTO": "pull_request", "CABECA_PR": "0" * 40, "ANTES": ""}) == "true"
    assert _roda_detector(cr, r, {"EVENTO": "pull_request", "CABECA_PR": "", "ANTES": ""}) == "true"
    assert _roda_detector(cr, r, {"EVENTO": "push", "CABECA_PR": "", "ANTES": "0" * 40}) == "true"
    assert _roda_detector(cr, r, {"EVENTO": "push", "CABECA_PR": "", "ANTES": "1" * 40}) == "true"
    # push com before conhecido e só documentação: dispensa
    assert _roda_detector(cr, r, {"EVENTO": "push", "CABECA_PR": "", "ANTES": _git(r, "rev-parse", "HEAD^1")}) == "false"


@pytest.mark.parametrize("detecta, relevante, resultados, passa", [
    ("success", "false", {}, True),                                  # nada relevante: tudo pulado
    ("success", "false", {"base": "success"}, False),                # nada relevante, mas uma parte rodou
    ("success", "true", {}, True),                                   # regeneração completa com sucesso
    ("success", "true", {"inerte_solido": "skipped"}, False),        # pulado com mudança relevante
    ("success", "true", {"base": "failure"}, False),
    ("success", "true", {"regeneracao": "cancelled"}, False),
    ("failure", None, {}, False),                                    # detector falhou
    ("cancelled", None, {}, False),
    ("success", None, {}, False),                                    # saída do detector ausente
])
def test_portao(cr, tmp_path, detecta, relevante, resultados, passa):
    """O script do portão: pulado só conta como sucesso quando o detector disse que nada relevante mudou."""
    import json
    import os
    import shutil
    import subprocess
    if not shutil.which("jq"):
        if os.environ.get("CI"):
            pytest.fail("jq ausente no CI: o portão ficaria sem teste")
        pytest.skip("jq ausente nesta máquina")
    passo = next(s for s in _wf(cr)["jobs"]["portao"]["steps"] if "NEEDS" in s.get("env", {}))
    padrao = "success" if relevante == "true" else "skipped"
    needs = {"detecta": {"result": detecta, "outputs": {} if relevante is None else {"relevante": relevante}}}
    needs |= {j: {"result": resultados.get(j, padrao), "outputs": {}} for j in _wf(cr)["jobs"]["portao"]["needs"] if j != "detecta"}
    r = subprocess.run(["bash", "-c", passo["run"]], env={**os.environ, "NEEDS": json.dumps(needs),
                       "GITHUB_STEP_SUMMARY": str(tmp_path / "resumo")}, capture_output=True, text=True)
    assert (r.returncode == 0) == passa, r.stdout


def test_ambiente_ignora_git_do_hook(cr, repo_prova, monkeypatch, tmp_path):
    """ambiente() descreve o repositório da ferramenta mesmo com GIT_DIR e GIT_INDEX_FILE de um hook no ambiente (regra 9):
    roda num repositório de prova, com as variáveis apontando para uma isca, que não pode ser tocada."""
    r, _ = repo_prova
    isca = tmp_path / "isca"
    isca.mkdir()
    _git(isca, "init", "-q")
    _git(isca, "commit", "-q", "--allow-empty", "-m", "isca")
    antes = (_git(isca, "rev-parse", "HEAD"), sorted(p.name for p in (isca / ".git").iterdir()))
    monkeypatch.setattr(cr, "RAIZ", r)
    monkeypatch.delenv("GITHUB_EVENT_PATH", raising=False)
    monkeypatch.setenv("GIT_DIR", str(isca / ".git"))
    monkeypatch.setenv("GIT_INDEX_FILE", str(isca / ".git" / "index_do_hook"))
    amb = cr.ambiente()
    monkeypatch.delenv("GIT_DIR")
    monkeypatch.delenv("GIT_INDEX_FILE")
    assert amb["commit"] == _git(r, "rev-parse", "HEAD") and amb["alteracoes_nao_commitadas"] is False
    assert (_git(isca, "rev-parse", "HEAD"), sorted(p.name for p in (isca / ".git").iterdir())) == antes
