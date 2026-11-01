"""Etapa 2.5, item 1: as Etapas 2.1 e 2.2 mudam com a trajetória nova de 2033 (|DLA| ≤ 50°)?

Exporta o commit atual (git archive) para um diretório temporário, copia os kernels, volta as plataformas
para os valores com que as Etapas 2.1 e 2.2 foram geradas (P-016 = P-017 = 850 kg, histórico em
config/plataformas.yaml) e a propulsão de antes da Etapa 3.1 (config/motores.yaml, antes_etapa_3_1) e roda de novo
as ferramentas dessas etapas. Compara cada arquivo gerado, byte a byte
(SHA-256), com o que está em results/. Isola o efeito da trajetória de 2033 (e da errata das datas, que não
aparece nesses arquivos).
Saída: results/etapa2.5/conferencia_2033.yaml e .md

Uso: python tools/confere_2033.py
"""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from orbital.historico import aplicar_antes_etapa_3_1, aplicar_antes_etapa_4_5  # noqa: E402
SAIDA = RAIZ / "results" / "etapa2.5"
FERRAMENTAS = ["tools/superficie.py", "tools/varredura_encontro.py", "tools/isru.py", "tools/mav_propulsao.py"]
PASTAS = ["results/etapa2.1", "results/etapa2.2"]


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    antes = yaml.safe_load((RAIZ / "config/plataformas.yaml").read_text(encoding="utf-8"))["antes_etapa_2_3"]
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=RAIZ, capture_output=True, text=True).stdout.strip()
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        arq = subprocess.run(["git", "archive", "HEAD"], cwd=RAIZ, capture_output=True, check=True).stdout
        subprocess.run(["tar", "-x", "-C", str(d)], input=arq, check=True)
        shutil.copytree(RAIZ / "data" / "kernels", d / "data" / "kernels", dirs_exist_ok=True)
        for pasta in PASTAS:  # sem os resultados antigos: o que não for regenerado aparece como "não regenerado"
            shutil.rmtree(d / pasta)
        for arq_cfg, chave, valor in (("config/dimensionamento.yaml", r"^plataforma_orbitador_kg: \{valor: [\d.]+,", antes["orbitador_kg"]),
                                      ("config/superficie.yaml", r"^  plataforma_superficie_kg: \{valor: [\d.]+,", antes["lander_kg"])):
            p = d / arq_cfg
            txt, n = re.subn(chave, lambda m: re.sub(r"[\d.]+,$", f"{valor},", m.group(0)), p.read_text(encoding="utf-8"), flags=re.M)
            assert n == 1, arq_cfg
            p.write_text(txt, encoding="utf-8")
        aplicar_antes_etapa_3_1(d)   # propulsão de antes da Etapa 3.1 (ADR 0011), com que as Etapas 2.1 e 2.2 foram geradas
        aplicar_antes_etapa_4_5(d)   # e sem o circuito de fluido no estágio de cruzeiro (Etapa 4.5)
        for f in FERRAMENTAS:
            subprocess.run([sys.executable, f], cwd=d, check=True, capture_output=True)
        linhas = []
        for pasta in PASTAS:
            for p in sorted((RAIZ / pasta).iterdir()):
                q = d / pasta / p.name
                linhas.append({"arquivo": f"{pasta}/{p.name}", "regenerado": q.exists(),
                               "igual": (_sha(p) == _sha(q)) if q.exists() else None})
    out = {"gerado_por": "tools/confere_2033.py", "commit": commit,
           "plataformas_usadas_kg": {"orbitador": antes["orbitador_kg"], "lander": antes["lander_kg"]},
           "ferramentas": FERRAMENTAS, "arquivos": linhas,
           "regenerados": sum(x["regenerado"] for x in linhas),
           "todos_regenerados_iguais": any(x["regenerado"] for x in linhas) and all(x["igual"] for x in linhas if x["regenerado"]),
           "nao_regenerados": [x["arquivo"] for x in linhas if not x["regenerado"]]}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "conferencia_2033.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    md = ["# Conferência das Etapas 2.1 e 2.2 com a 2033 nova (gerado por tools/confere_2033.py)", "",
          f"Commit {commit}; plataformas de {antes['orbitador_kg']} / {antes['lander_kg']} kg (as da época); "
          f"ferramentas: {', '.join(FERRAMENTAS)}.", "",
          f"**Arquivos regenerados pelas ferramentas atuais: {out['regenerados']} de {len(linhas)}; todos iguais byte a byte: "
          f"{'sim' if out['todos_regenerados_iguais'] else 'NÃO'}.** Não regenerados (legado de versões anteriores das "
          f"ferramentas, não conferidos): {', '.join(out['nao_regenerados']) or 'nenhum'}.", "",
          "| Arquivo | Regenerado | Igual |", "| :- | :- | :- |"] + [
          f"| {x['arquivo']} | {'sim' if x['regenerado'] else 'não'} | {'—' if x['igual'] is None else ('sim' if x['igual'] else '**não**')} |" for x in linhas]
    (SAIDA / "conferencia_2033.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:5]))


if __name__ == "__main__":
    main()
