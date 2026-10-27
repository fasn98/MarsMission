"""Regenera TODO o results/ numa cópia da árvore de trabalho e compara com o results/ versionado.

Serve para provar que uma mudança de ambiente (ex.: conda-forge → wheels do PyPI) ou uma refatoração sem mudança
de física não altera nenhum resultado. A ordem e as plataformas seguem a história do estudo:
  1. Fase 1 (Etapas 1.1 a 1.3) e lista de premissas, com o config atual;
  2. Etapas 1.4, 2.1 e 2.2 com as plataformas da época (P-016 = P-017 = 850 kg, histórico em config/plataformas.yaml,
     "antes_etapa_2_3"), como em tools/confere_2033.py;
  3. Etapas 2.3 a 2.5 com o config atual.
"Idêntico" significa dentro das tolerâncias declaradas (decisão do Fabio, 2026-10-27; premissas NÃO VALIDADAS):
  - números (YAML, Markdown, NPZ): a (versionado) e b (regenerado) passam se |a − b| ≤ max(relativa · |b|, piso
    absoluto), P-039. O limite vem da precisão relevante do estudo (~1e-4 relativo), com folga para o ruído entre CPUs
    amplificado por cálculos mal condicionados; diferença acima dele é problema a investigar, não motivo para alargá-lo;
  - PNG: até a fração de pixels diferentes da P-040 (os dados de origem das figuras são conferidos pela P-039).
Cada arquivo sai em um de três estados: "idêntico" (byte a byte; PNG pixel a pixel; NPZ array a array; controle sem
o hash), "dentro da tolerância" (as diferenças abaixo do limite ficam listadas no relatório, com o tamanho) ou
"diferente" (alguma diferença acima do limite, ou de texto). Texto, estrutura ou forma diferentes nunca são tolerados.
Os arquivos de controle que gravam o hash do commit em que rodaram (CONTROLE) são comparados com o hash mascarado.
efeito_efemeride só roda se data/kernels/de200.bsp existir (config/kernels_verificacao.yaml); sem ele, o arquivo dele
conta como não regenerado.
Saída: results/conferencia/regeneracao_<rótulo>.yaml e .md (rótulo identifica o ambiente, ex.: conda, pip)
O relatório registra o ambiente: Python, versões das dependências do pyproject.toml, CPU, sistema e commit (e se a
árvore de trabalho regenerada tinha alterações não commitadas).

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
import tomllib
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "results" / "conferencia"
PYPROJECT = RAIZ / "pyproject.toml"   # fonte única das dependências (ADR 0010): os pacotes do relatório saem daqui
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


def _tolerancias():
    """(relativa, piso absoluto, fração de pixels) das premissas P-039 e P-040 de config/premissas.yaml."""
    ps = {x["id"]: x["valor"] for x in yaml.safe_load((RAIZ / "config/premissas.yaml").read_text(encoding="utf-8"))["premissas"]}
    return float(ps["P-039"]["relativa"]), float(ps["P-039"]["piso_absoluto"]), float(ps["P-040"])


def _dentro(a, b, rtol, atol) -> bool:
    """P-039: a (versionado) e b (regenerado) passam se |a − b| ≤ max(rtol · |b|, atol)."""
    return abs(a - b) <= max(rtol * abs(b), atol)


def _eh_num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def avaliar(p: Path, q: Path, rel: str = "") -> dict:
    """Estado do arquivo regenerado q contra o versionado p: {"estado": "identico" | "tolerancia" | "diferente", ...}.

    "abaixo" lista as diferenças dentro da tolerância e "acima", as que a excedem (com tamanho absoluto e relativo)."""
    rtol, atol, fpx = _tolerancias()
    if rel in CONTROLE:
        if _sem_hash(p) == _sem_hash(q):
            return {"estado": "identico"}
        return {"estado": "diferente", "acima": [_linha_dif(*x) for x in (
            _difs_yaml(yaml.safe_load(p.read_text(encoding="utf-8")), yaml.safe_load(q.read_text(encoding="utf-8")))
            if p.suffix == ".yaml" else _difs_texto(p.read_text(encoding="utf-8"), q.read_text(encoding="utf-8")))]}
    if p.suffix == ".png":
        import matplotlib.image as mpimg
        a, b = mpimg.imread(p), mpimg.imread(q)
        if a.shape != b.shape or a.dtype != b.dtype:
            return {"estado": "diferente", "png": {"forma": [list(a.shape), list(b.shape)]}}
        d = np.abs(a.astype(float) - b.astype(float))
        info = {"max_dif_pixel": float(d.max()), "fracao_pixels_diferentes": float((d.max(axis=-1) > 0).mean()),
                "limite_fracao": fpx}
        estado = "identico" if info["fracao_pixels_diferentes"] == 0 else (
            "tolerancia" if info["fracao_pixels_diferentes"] <= fpx else "diferente")
        return {"estado": estado, "png": info}
    if _sha(p) == _sha(q):
        return {"estado": "identico"}
    if p.suffix == ".npz":
        abaixo, acima = [], []
        with np.load(p) as a, np.load(q) as b:
            for k in sorted(set(a.files) | set(b.files)):
                if k not in a.files or k not in b.files or a[k].shape != b[k].shape or a[k].dtype != b[k].dtype:
                    acima.append({"onde": k, "versionado": "ausente, outra forma ou outro tipo", "regenerado": ""})
                    continue
                x, y = a[k], b[k]
                if x.dtype.kind != "f":
                    if not np.array_equal(x, y):
                        acima.append({"onde": k, "versionado": "conteúdo diferente", "regenerado": ""})
                    continue
                if np.array_equal(x, y, equal_nan=True):
                    continue
                if not np.array_equal(np.isnan(x), np.isnan(y)):
                    acima.append({"onde": k, "versionado": "NaN em posições diferentes", "regenerado": ""})
                    continue
                ok = ~np.isnan(x)
                dif = np.abs(x[ok] - y[ok])
                lim = np.maximum(rtol * np.abs(y[ok]), atol)   # P-039: max(rtol · |regenerado|, atol)
                rel_ = dif / np.where(np.abs(x[ok]) > 0, np.abs(x[ok]), np.inf)
                r = {"onde": f"{k} ({int((dif > 0).sum())} elementos)", "versionado": "", "regenerado": "",
                     "dif_abs": float(dif.max()), "dif_rel": float(rel_.max())}
                (abaixo if bool((dif <= lim).all()) else acima).append(r)
        return {"estado": "diferente" if acima else ("tolerancia" if abaixo else "identico"), "abaixo": abaixo, "acima": acima}
    if p.suffix == ".yaml":
        difs = _difs_yaml(yaml.safe_load(p.read_text(encoding="utf-8")), yaml.safe_load(q.read_text(encoding="utf-8")))
        pares = [(o, x, y, x, y) for o, x, y in difs]
    else:
        difs = _difs_texto(p.read_text(encoding="utf-8"), q.read_text(encoding="utf-8"))
        pares = [(o, x, y, _num(x) if isinstance(x, str) else None, _num(y) if isinstance(y, str) else None)
                 for o, x, y in difs]
    abaixo, acima = [], []
    for o, x, y, nx, ny in pares:
        dentro = _eh_num(nx) and _eh_num(ny) and "(texto)" not in o and _dentro(nx, ny, rtol, atol)
        (abaixo if dentro else acima).append(_linha_dif(o, x, y))
    if not difs:   # bytes diferentes, valores iguais (ex.: formatação): conta como dentro da tolerância
        return {"estado": "tolerancia", "abaixo": [{"onde": "bytes diferentes, mesmos valores", "versionado": "", "regenerado": ""}],
                "acima": []}
    return {"estado": "diferente" if acima else "tolerancia", "abaixo": abaixo, "acima": acima}


def _identicos(p: Path, q: Path, rel: str = "") -> bool:
    """Idêntico pelo critério do estudo (dentro das tolerâncias P-039 e P-040)."""
    return avaliar(p, q, rel)["estado"] != "diferente"


def _cpu():
    """Modelo da CPU (o numpy e a OpenBLAS escolhem o código pela CPU em tempo de execução): registrado no relatório."""
    try:
        for linha in Path("/proc/cpuinfo").read_text().splitlines():
            if linha.startswith("model name"):
                return linha.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or platform.machine()


def pacotes() -> list[str]:
    """Nomes das dependências do pyproject.toml (obrigatórias e extras, na ordem do arquivo), para o relatório."""
    proj = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]
    reqs = list(proj.get("dependencies", [])) + [r for extra in proj.get("optional-dependencies", {}).values() for r in extra]
    nomes = []
    for r in reqs:
        m = re.match(r"\s*([A-Za-z0-9][A-Za-z0-9_.\-]*)", r)
        if m is None:
            raise ValueError(f"requisito do pyproject.toml sem nome de pacote: {r!r}")
        nomes.append(m.group(1).lower())
    return list(dict.fromkeys(nomes))


def _git(*args):
    try:
        r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True)
    except OSError:
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def _commit_do_pr():
    """No CI de pull_request o checkout é o merge sintético (refs/pull/N/merge); o head do PR vem do evento do GitHub."""
    import json
    import os
    evento = os.environ.get("GITHUB_EVENT_PATH")
    try:
        return json.loads(Path(evento).read_text(encoding="utf-8"))["pull_request"]["head"]["sha"] if evento else None
    except (OSError, ValueError, KeyError, TypeError):
        return None


def ambiente() -> dict:
    """Ambiente da regeneração: Python, versões dos pacotes do pyproject.toml, CPU, sistema e commit da árvore regenerada.
    Lido antes da cópia, para descrever o que foi regenerado (e não as escritas de --atualizar). A cópia é a árvore de
    trabalho, não o HEAD: "alteracoes_nao_commitadas" diz se havia arquivos rastreados modificados ou não rastreados (fora
    do .gitignore); None sem git. No CI de pull_request, "commit" é o merge sintético e "commit_head_do_pr" o head do PR."""
    status = _git("status", "--porcelain")
    amb = {"python": platform.python_version(), **{k: _versao(k) for k in pacotes()}, "cpu": _cpu(),
           "sistema": platform.platform(), "commit": _git("rev-parse", "HEAD")}
    pr = _commit_do_pr()
    if pr:
        amb["commit_head_do_pr"] = pr
    amb["alteracoes_nao_commitadas"] = None if status is None else bool(status)
    return amb


def ambiente_md(amb: dict) -> str:
    """Linha "Ambiente" do relatório em Markdown: pacote ausente aparece como "ausente"; commit sem git é omitido."""
    partes = [f"{k} {'ausente' if v is None else v}" for k, v in amb.items()
              if k != "alteracoes_nao_commitadas" and not (v is None and k.startswith("commit"))]
    aviso = " (árvore de trabalho com alterações não commitadas)" if amb.get("alteracoes_nao_commitadas") else ""
    return ", ".join(partes) + aviso


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
    amb = ambiente()   # antes da cópia: descreve a árvore regenerada
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
                item.update(avaliar(p, q, str(rel)))
                item["identico"] = item["estado"] != "diferente"
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
           "ambiente": amb,
           "ferramentas": log, "versionados": len(arquivos),
           "regenerados": sum(a["regenerado"] for a in arquivos),
           "tolerancias": {"P-039": {"relativa": _tolerancias()[0], "piso_absoluto": _tolerancias()[1]},
                           "P-040": {"fracao_pixels": _tolerancias()[2]}},
           "identicos": sum(a.get("estado") == "identico" for a in arquivos),
           "dentro_da_tolerancia": [a["arquivo"] for a in arquivos if a.get("estado") == "tolerancia"],
           "nao_regenerados": [a["arquivo"] for a in arquivos if not a["regenerado"]],
           "diferentes": [a["arquivo"] for a in arquivos if a["regenerado"] and not a["identico"]],
           "gerados_sem_versao": novos, "atualizados": atualizar, "arquivos": arquivos}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / f"regeneracao_{rotulo}.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    amb_md = ambiente_md(out["ambiente"])
    md = [f"# Regeneração de results/ — ambiente \"{rotulo}\" (gerado por tools/confere_regeneracao.py)", "",
          f"Ambiente: {amb_md}. Comparado com: {out['comparado_com']}.", "",
          f"**Versionados: {out['versionados']}; regenerados: {out['regenerados']}; idênticos: {out['identicos']}; "
          f"dentro da tolerância: {len(out['dentro_da_tolerancia'])}; diferentes: {len(out['diferentes'])}.**", "",
          f"Não regenerados: {', '.join(out['nao_regenerados']) or 'nenhum'}.", "",
          f"Gerados sem versão no repositório: {', '.join(novos) or 'nenhum'}.", "",
          f"Copiados sobre os versionados (--atualizar): {', '.join(atualizar) or 'nenhum'}.", "",
          f"Critério (\"idêntico\" = dentro das tolerâncias): números com |a − b| ≤ max({_tolerancias()[0]:g} · |b|, "
          f"{_tolerancias()[1]:g}), a versionado e b regenerado (P-039); PNG com até {100 * _tolerancias()[2]:g} % de pixels diferentes (P-040); "
          f"arquivos de controle ({', '.join(sorted(CONTROLE))}) sem o hash do commit. Premissas NÃO VALIDADAS.", "",
          "Ferramentas não rodadas: " + (", ".join(f"{x['ferramenta']} ({x['motivo']})" for x in log if not x["rodou"]) or "nenhuma") + ".", "",
          "## Arquivos diferentes (acima do limite)", ""]

    def tabela(vals):
        esc = lambda x: str(x).replace("|", "\\|")  # noqa: E731
        g = lambda x: "" if x is None else format(x, ".3g")  # noqa: E731
        t = ["| Onde | Versionado | Regenerado | Dif. absoluta | Dif. relativa |", "| :- | :- | :- | -: | -: |"]
        t += [f"| {esc(v['onde'])} | {esc(v['versionado'])} | {esc(v['regenerado'])} | {g(v.get('dif_abs'))} | "
              f"{g(v.get('dif_rel'))} |" for v in vals[:40]]
        if len(vals) > 40:
            t.append(f"| … mais {len(vals) - 40} (ver o .yaml) | | | | |")
        return t

    if not out["diferentes"]:
        md.append("Nenhum.")
    for a in arquivos:
        if a.get("estado") != "diferente":
            continue
        md += [f"### {a['arquivo']}", ""] + ([f"PNG: {a['png']}"] if "png" in a else tabela(a.get("acima", [])))
        if a.get("abaixo"):
            md += ["", "Também abaixo do limite neste arquivo:", ""] + tabela(a["abaixo"])
        md.append("")
    md += ["## Diferenças abaixo do limite (dentro da tolerância)", ""]
    if not out["dentro_da_tolerancia"]:
        md.append("Nenhuma.")
    for a in arquivos:
        if a.get("estado") != "tolerancia":
            continue
        md += [f"### {a['arquivo']}", ""]
        if "png" in a:
            md.append(f"PNG: {100 * a['png']['fracao_pixels_diferentes']:.4g} % dos pixels diferentes (limite "
                      f"{100 * a['png']['limite_fracao']:g} %); maior diferença de pixel {a['png']['max_dif_pixel']:.3g}.")
        else:
            vals = a["abaixo"]
            mx_a = max((v.get("dif_abs") or 0 for v in vals), default=0)
            mx_r = max((v.get("dif_rel") or 0 for v in vals), default=0)
            md += [f"{len(vals)} diferença(s); maior absoluta {mx_a:.3g}, maior relativa {mx_r:.3g}.", ""] + tabela(vals)
        md.append("")
    (SAIDA / f"regeneracao_{rotulo}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    if ci and (out["diferentes"] or out["nao_regenerados"] or novos):
        sys.exit(1)


if __name__ == "__main__":
    main()
