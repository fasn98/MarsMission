"""Regenera TODO o results/ numa cópia da árvore de trabalho e compara com o results/ versionado.

Serve para provar que uma mudança de ambiente (ex.: conda-forge → wheels do PyPI) ou uma refatoração sem mudança
de física não altera nenhum resultado. A ordem e as plataformas seguem a história do estudo:
  1. Fase 1 (Etapas 1.1 a 1.3) e lista de premissas, com o config atual;
  2. Etapas 1.4, 2.1 e 2.2 com as plataformas da época (P-016 = P-017 = 850 kg, histórico em config/plataformas.yaml,
     "antes_etapa_2_3"), como em tools/confere_2033.py;
  3. Etapas 2.3 a 2.5 com o config atual.
Critério de "idêntico" por tipo:
  - YAML e Markdown: byte a byte (SHA-256). Se diferir, o relatório traz valor a valor (YAML) ou número a número em cada
    linha (Markdown), com diferença absoluta e relativa.
  - PNG: pixel a pixel (mesma forma e mesmos valores). A compressão do PNG muda com a build da libpng/zlib (conda ou
    wheel) sem mudar a imagem; os bytes iguais ficam registrados em "igual_bytes", só para informação.
  - NPZ (grades do painel): array a array, porque o zip grava a hora de escrita.
  - Arquivos de controle que gravam o hash do commit em que rodaram (CONTROLE): comparados com o hash mascarado.
efeito_efemeride só roda se data/kernels/de200.bsp existir (config/kernels_verificacao.yaml); sem ele, o arquivo dele
conta como não regenerado.
Saída: results/conferencia/regeneracao_<rótulo>.yaml e .md (rótulo identifica o ambiente, ex.: conda, pip)

Com --referencia DIR, compara com uma regeneração anterior guardada (--guardar DIR) em vez do results/ versionado: isola
o efeito da mudança (ambiente ou código) do que já diferia antes dela.

Com --ci, a saída é 1 se algum arquivo versionado diferir ou não for regenerado, ou se a regeneração gerar arquivo sem
versão (verificação de CI: .github/workflows/regeneracao.yml). Com --atualizar ARQ [ARQ ...] (caminhos em results/),
copia só esses arquivos regenerados sobre os versionados: é assim que um resultado que ficou para trás é regenerado,
pela mesma rotina e na ordem histórica, sem edição à mão.

Uso: python tools/confere_regeneracao.py <rótulo> [--guardar DIR] [--referencia DIR] [--ci] [--atualizar ARQ ...]
"""

from __future__ import annotations

import hashlib
import importlib.metadata as md_
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "results" / "conferencia"
PACOTES = ("numpy", "scipy", "matplotlib", "pyyaml", "spiceypy", "streamlit", "plotly")
FASE_1 = [["tools/baricentro_marte.py"], ["tools/porkchop.py", "terra_marte"], ["tools/porkchop.py", "marte_terra"],
          ["tools/verifica_burke2010.py"], ["tools/verifica_jpl8243.py"], ["tools/efeito_efemeride.py"],
          ["tools/missoes.py"], ["tools/compara_dra5.py"], ["tools/grafico_missoes.py"], ["tools/lista_premissas.py"]]
FASE_850 = [["tools/dimensionamento.py"], ["tools/compara_msr.py"], ["tools/superficie.py"],
            ["tools/varredura_encontro.py"], ["tools/isru.py"], ["tools/mav_propulsao.py"]]
FASE_ATUAL = [["tools/plataformas.py"], ["tools/lancamento.py"], ["tools/coleta.py"], ["tools/arquitetura.py"],
              ["tools/confere_2033.py"], ["tools/exporta_painel.py"]]
_SO_NA_RAIZ = {".git", "data", "results", "hanatrial", ".venv", ".pythonlibs", ".cache", ".claude"}


def _ignorar(pasta, nomes):
    """Pastas que não entram na cópia: as de _SO_NA_RAIZ só no topo (tests/data entra) e caches em qualquer nível."""
    na_raiz = Path(pasta) == RAIZ
    return [n for n in nomes if (na_raiz and n in _SO_NA_RAIZ) or n in ("__pycache__", ".pytest_cache") or n.endswith(".egg-info")]
NUM = re.compile(r"[−-]?\d{1,3}(?:[  ]\d{3})+(?:,\d+)?|[−-]?\d+(?:[.,]\d+)?(?:e[+-]?\d+)?")  # 22 768 | 6,372 | 1.2e-3


CONTROLE = {"results/etapa2.5/conferencia_2033.yaml", "results/etapa2.5/conferencia_2033.md"}
HASH_YAML = re.compile(r"^commit: \S+$", flags=re.M)
HASH_MD = re.compile(r"^Commit [0-9a-f]+;", flags=re.M)


def _sem_hash(p: Path) -> bytes:
    """Conteúdo de um arquivo de controle com o hash do commit mascarado."""
    t = p.read_text(encoding="utf-8")
    return HASH_MD.sub("Commit #;", HASH_YAML.sub("commit: #", t)).encode("utf-8")


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _identicos(p: Path, q: Path, rel: str = "") -> bool:
    """Byte a byte; .png pixel a pixel; .npz array a array (bit a bit, NaN igual a NaN); controle sem o hash."""
    if rel in CONTROLE:
        return _sem_hash(p) == _sem_hash(q)
    if p.suffix == ".png":
        import matplotlib.image as mpimg
        a, b = mpimg.imread(p), mpimg.imread(q)
        return a.shape == b.shape and a.dtype == b.dtype and np.array_equal(a, b)
    if p.suffix != ".npz":
        return _sha(p) == _sha(q)
    with np.load(p) as a, np.load(q) as b:
        return sorted(a.files) == sorted(b.files) and all(
            a[k].dtype == b[k].dtype and a[k].shape == b[k].shape and
            (np.array_equal(a[k], b[k], equal_nan=a[k].dtype.kind == "f")) for k in a.files)


def _cpu():
    """Modelo da CPU (o numpy e a OpenBLAS escolhem o código pela CPU em tempo de execução): registrado no relatório."""
    try:
        for linha in Path("/proc/cpuinfo").read_text().splitlines():
            if linha.startswith("model name"):
                return linha.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or platform.machine()


def _versao(pacote):
    try:
        return md_.version(pacote)
    except md_.PackageNotFoundError:
        return None


def _patch_850(d: Path, antes):
    for arq, chave, valor in (("config/dimensionamento.yaml", r"^plataforma_orbitador_kg: \{valor: [\d.]+,", antes["orbitador_kg"]),
                              ("config/superficie.yaml", r"^  plataforma_superficie_kg: \{valor: [\d.]+,", antes["lander_kg"])):
        p = d / arq
        txt, n = re.subn(chave, lambda m: re.sub(r"[\d.]+,$", f"{valor},", m.group(0)), p.read_text(encoding="utf-8"), flags=re.M)
        assert n == 1, arq
        p.write_text(txt, encoding="utf-8")


def _num(s):
    """Número de um token (vírgula decimal e espaço de milhar do estudo, ou formato Python)."""
    t = s.replace("−", "-").replace(" ", "").replace(" ", "")
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def _difs_yaml(a, b, caminho=""):
    """Folhas diferentes entre dois objetos YAML: [(caminho, a, b)]."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in list(a) + [k for k in b if k not in a]:
            out += _difs_yaml(a.get(k), b.get(k), f"{caminho}/{k}")
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in _difs_yaml(x, y, f"{caminho}[{i}]")]
    if a == b or (isinstance(a, float) and isinstance(b, float) and a != a and b != b):
        return []
    return [(caminho, a, b)]


def _difs_texto(a: str, b: str):
    la, lb = a.splitlines(), b.splitlines()
    if len(la) != len(lb):
        return [(f"linhas: {len(la)} vs {len(lb)}", None, None)]
    out = []
    for i, (x, y) in enumerate(zip(la, lb), 1):
        if x == y:
            continue
        nx, ny = NUM.findall(x), NUM.findall(y)
        if len(nx) == len(ny) and NUM.sub("#", x) == NUM.sub("#", y):
            out += [(f"linha {i}", p, q) for p, q in zip(nx, ny) if p != q]
        else:
            out.append((f"linha {i} (texto)", x[:120], y[:120]))
    return out


def _linha_dif(onde, a, b):
    na = _num(a) if isinstance(a, str) else a
    nb = _num(b) if isinstance(b, str) else b
    r = {"onde": onde, "versionado": a, "regenerado": b}
    if isinstance(na, (int, float)) and isinstance(nb, (int, float)) and not isinstance(na, bool):
        r["dif_abs"] = abs(nb - na)
        r["dif_rel"] = abs(nb - na) / abs(na) if na else None
    return r


def comparar(p: Path, q: Path):
    """Detalhe da diferença entre o arquivo versionado p e o regenerado q."""
    if p.suffix == ".png":
        import matplotlib.image as mpimg
        a, b = mpimg.imread(p), mpimg.imread(q)
        if a.shape != b.shape:
            return {"png": {"forma": [list(a.shape), list(b.shape)]}}
        d = np.abs(a.astype(float) - b.astype(float))
        return {"png": {"max_dif_pixel": float(d.max()), "fracao_pixels_diferentes": float((d.max(axis=-1) > 0).mean())}}
    if p.suffix == ".npz":
        with np.load(p) as a, np.load(q) as b:
            difs = []
            for k in sorted(set(a.files) | set(b.files)):
                if k not in a.files or k not in b.files or a[k].shape != b[k].shape:
                    difs.append({"onde": k, "versionado": "ausente ou outra forma", "regenerado": ""})
                elif a[k].dtype.kind == "f":
                    d = np.abs(a[k] - b[k])
                    difs.append({"onde": k, "versionado": "", "regenerado": "", "dif_abs": float(np.nanmax(d)),
                                 "dif_rel": float(np.nanmax(d / np.abs(a[k])))})
                elif not np.array_equal(a[k], b[k]):
                    difs.append({"onde": k, "versionado": "texto diferente", "regenerado": ""})
        return {"valores": difs}
    if p.suffix == ".yaml":
        difs = _difs_yaml(yaml.safe_load(p.read_text(encoding="utf-8")), yaml.safe_load(q.read_text(encoding="utf-8")))
    else:
        difs = _difs_texto(p.read_text(encoding="utf-8"), q.read_text(encoding="utf-8"))
    return {"valores": [_linha_dif(*d) for d in difs]}


def regenerar(d: Path):
    """Roda todas as ferramentas em d, na ordem histórica. Devolve [(ferramenta, ok, motivo)]."""
    log = []

    def rodar(cmd):
        if not (d / cmd[0]).exists():
            log.append({"ferramenta": " ".join(cmd), "rodou": False, "motivo": "ferramenta ausente nesta versão do código"})
            return
        if cmd[0] == "tools/efeito_efemeride.py" and not (d / "data/kernels/de200.bsp").exists():
            log.append({"ferramenta": " ".join(cmd), "rodou": False, "motivo": "data/kernels/de200.bsp ausente"})
            return
        r = subprocess.run([sys.executable, *cmd], cwd=d, capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f"{' '.join(cmd)} falhou:\n{r.stderr[-3000:]}")
        log.append({"ferramenta": " ".join(cmd), "rodou": True})

    antes = yaml.safe_load((d / "config/plataformas.yaml").read_text(encoding="utf-8"))["antes_etapa_2_3"]
    for c in FASE_1:
        rodar(c)
    originais = {a: (d / a).read_text(encoding="utf-8") for a in ("config/dimensionamento.yaml", "config/superficie.yaml")}
    _patch_850(d, antes)
    for c in FASE_850:
        rodar(c)
    for a, t in originais.items():
        (d / a).write_text(t, encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=d, check=True)
    subprocess.run(["git", "-c", "user.name=x", "-c", "user.email=x@x", "commit", "-qm", "config atual"], cwd=d, check=True)
    for c in FASE_ATUAL:
        rodar(c)
    return log


def main():
    rotulo = sys.argv[1]
    guardar = Path(sys.argv[sys.argv.index("--guardar") + 1]) if "--guardar" in sys.argv else None
    referencia = Path(sys.argv[sys.argv.index("--referencia") + 1]) if "--referencia" in sys.argv else None
    ci = "--ci" in sys.argv
    atualizar = []
    if "--atualizar" in sys.argv:
        atualizar = [a for a in sys.argv[sys.argv.index("--atualizar") + 1:] if not a.startswith("--")]
        if not atualizar or not all(a.startswith("results/") and ".." not in Path(a).parts for a in atualizar):
            sys.exit("--atualizar exige caminhos em results/")
    base = referencia if referencia else RAIZ / "results"
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "repo"
        shutil.copytree(RAIZ, d, ignore=_ignorar)
        shutil.copytree(RAIZ / "data", d / "data")
        (d / "results").mkdir()
        # confere_2033 exporta o HEAD com git archive: a cópia vira um repositório com a árvore de trabalho atual
        subprocess.run(["git", "init", "-q"], cwd=d, check=True)
        subprocess.run(["git", "add", "-A"], cwd=d, check=True)
        subprocess.run(["git", "-c", "user.name=x", "-c", "user.email=x@x", "commit", "-qm", "copia"], cwd=d, check=True)
        log = regenerar(d)
        versionados = sorted(x for x in base.rglob("*") if x.is_file() and x.name != ".gitkeep"
                             and "conferencia" not in x.relative_to(base).parts)
        arquivos = []
        for p in versionados:
            rel = Path("results") / p.relative_to(base)
            q = d / rel
            item = {"arquivo": str(rel), "regenerado": q.exists()}
            if q.exists():
                item["identico"] = _identicos(p, q, str(rel))
                if p.suffix == ".png" or str(rel) in CONTROLE:
                    item["igual_bytes"] = _sha(p) == _sha(q)
                if not item["identico"]:
                    item.update(comparar(p, q))
            arquivos.append(item)
        novos = sorted(str(x.relative_to(d)) for x in (d / "results").rglob("*")
                       if x.is_file() and not (base / x.relative_to(d / "results")).exists())
        for a in atualizar:
            if not (d / a).exists():
                sys.exit(f"{a} não foi regenerado: nada copiado")
        for a in atualizar:
            (RAIZ / a).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(d / a, RAIZ / a)
        if guardar:
            shutil.rmtree(guardar, ignore_errors=True)
            shutil.copytree(d / "results", guardar)
    out = {"gerado_por": "tools/confere_regeneracao.py", "rotulo": rotulo,
           "comparado_com": "regeneração guardada em " + referencia.name if referencia else "results/ versionado",
           "ambiente": {"python": platform.python_version(), **{k: _versao(k) for k in PACOTES}, "cpu": _cpu()},
           "ferramentas": log, "versionados": len(arquivos),
           "regenerados": sum(a["regenerado"] for a in arquivos),
           "identicos": sum(bool(a.get("identico")) for a in arquivos),
           "nao_regenerados": [a["arquivo"] for a in arquivos if not a["regenerado"]],
           "diferentes": [a["arquivo"] for a in arquivos if a["regenerado"] and not a["identico"]],
           "gerados_sem_versao": novos, "atualizados": atualizar, "arquivos": arquivos}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / f"regeneracao_{rotulo}.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    amb = ", ".join(f"{k} {v}" for k, v in out["ambiente"].items() if v)
    md = [f"# Regeneração de results/ — ambiente \"{rotulo}\" (gerado por tools/confere_regeneracao.py)", "",
          f"Ambiente: {amb}. Comparado com: {out['comparado_com']}.", "",
          f"**Versionados: {out['versionados']}; regenerados: {out['regenerados']}; idênticos pelo critério abaixo: {out['identicos']}.**", "",
          f"Não regenerados: {', '.join(out['nao_regenerados']) or 'nenhum'}.", "",
          f"Gerados sem versão no repositório: {', '.join(novos) or 'nenhum'}.", "",
          f"Copiados sobre os versionados (--atualizar): {', '.join(atualizar) or 'nenhum'}.", "",
          "Critério: YAML e Markdown byte a byte; PNG pixel a pixel; NPZ array a array; arquivos de controle "
          f"({', '.join(sorted(CONTROLE))}) sem o hash do commit.", "",
          "Ferramentas não rodadas: " + (", ".join(f"{x['ferramenta']} ({x['motivo']})" for x in log if not x["rodou"]) or "nenhuma") + ".", "",
          "## Arquivos diferentes", ""]
    if not out["diferentes"]:
        md.append("Nenhum.")
    for a in arquivos:
        if not a["regenerado"] or a["identico"]:
            continue
        md += [f"### {a['arquivo']}", ""]
        if "png" in a:
            md.append(f"PNG: {a['png']}")
        else:
            md += ["| Onde | Versionado | Regenerado | Dif. absoluta | Dif. relativa |", "| :- | :- | :- | -: | -: |"]
            for v in a["valores"][:40]:
                esc = lambda x: str(x).replace("|", "\\|")  # noqa: E731
                g = lambda x: "" if x is None else format(x, ".3g")  # noqa: E731
                md.append(f"| {esc(v['onde'])} | {esc(v['versionado'])} | {esc(v['regenerado'])} | "
                          f"{g(v.get('dif_abs'))} | {g(v.get('dif_rel'))} |")
            if len(a["valores"]) > 40:
                md.append(f"| … mais {len(a['valores']) - 40} diferenças (ver o .yaml) | | | | |")
        md.append("")
    (SAIDA / f"regeneracao_{rotulo}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    if ci and (out["diferentes"] or out["nao_regenerados"] or novos):
        sys.exit(1)


if __name__ == "__main__":
    main()
