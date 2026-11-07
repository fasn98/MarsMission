"""Isp esperado do R-4D-11 com bocal de 44:1, pedido pelo Fabio (2026-11-07): mesmo motor, razão de expansão menor.

Modelo: Isp = K · CF(ε, γ), com CF o coeficiente de empuxo no vácuo de bocal ideal e K = η c* / g0. Os dois pontos com fonte
do mesmo motor, 164:1 e 300:1 ([F228]), fixam γ e K. NASA CEA não está no workspace. Resultado NÃO VALIDADO.
Saída: results/etapa7.2/isp_44.yaml e .md

Uso: python tools/isp_44_bocal.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital import motores as om  # noqa: E402
from orbital.config import ler, nativo  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"
PASSOS = 200   # bisseções em γ e na razão de pressão (escolha numérica)


def br(x, n=1):
    return f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def gama_termo(g):
    return math.sqrt(g) * (2 / (g + 1)) ** ((g + 1) / (2 * (g - 1)))


def razao_area(x, g):
    """ε para a razão de pressão x = pe/pc, escoamento isentrópico de gás ideal."""
    return gama_termo(g) / math.sqrt(2 * g / (g - 1) * x ** (2 / g) * (1 - x ** ((g - 1) / g)))


def razao_pressao(eps, g):
    """pe/pc supersônico para a razão de áreas ε; a razão de áreas cresce quando pe/pc cai."""
    lo, hi = 1e-12, (2 / (g + 1)) ** (g / (g - 1))
    for _ in range(PASSOS):
        m = math.sqrt(lo * hi)
        lo, hi = (m, hi) if razao_area(m, g) > eps else (lo, m)
    return math.sqrt(lo * hi)


def cf_vacuo(eps, g):
    """Coeficiente de empuxo no vácuo de bocal ideal: parcela de quantidade de movimento mais ε · pe/pc."""
    x = razao_pressao(eps, g)
    return gama_termo(g) * math.sqrt(2 * g / (g - 1) * (1 - x ** ((g - 1) / g))) + eps * x


def ajusta_gama(i1, e1, i2, e2, faixa):
    """γ com CF(e2)/CF(e1) = i2/i1; a razão de CF cai quando γ sobe."""
    lo, hi = faixa
    for _ in range(PASSOS):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if cf_vacuo(e2, m) / cf_vacuo(e1, m) > i2 / i1 else (lo, m)
    return (lo + hi) / 2


def calibra(i1, e1, i2, e2, faixa, alvos):
    g = ajusta_gama(i1, e1, i2, e2, faixa)
    k = i1 / cf_vacuo(e1, g)
    return {"gama": g, "k_s": k, "cf": {str(e): cf_vacuo(e, g) for e in sorted({e1, e2, *alvos})}, "isp_s": {str(e): k * cf_vacuo(e, g) for e in alvos}}


def main():
    cad = ler("config/cad.yaml")
    c, rd = cad["isp_44_calibracao"], cad["r4d11_variantes"]
    i1, i2 = rd["164:1"]["isp_s"], rd["300:1"]["isp_s"]
    e1, e2, e44, e40 = 164, 300, 44, c["apollo"]["razao_expansao"]
    faixa = c["faixa_gama_busca"]["valor"]
    m1, m2 = c["meia_resolucao_s"]["164:1"], c["meia_resolucao_s"]["300:1"]
    alvos = [e44, e40]
    central = calibra(i1, e1, i2, e2, faixa, alvos)
    baixo = calibra(i1 - m1, e1, i2 + m2, e2, faixa, alvos)
    alto = calibra(i1 + m1, e1, i2 - m2, e2, faixa, alvos)
    varre = []
    for g in c["gamas_varredura"]["valor"]:
        q = cf_vacuo(e44, g)
        varre.append({"gama": g, "cf_44": q, "isp_ancora_164_s": i1 * q / cf_vacuo(e1, g), "isp_ancora_300_s": i2 * q / cf_vacuo(e2, g), "razao_300_164": cf_vacuo(e2, g) / cf_vacuo(e1, g)})
    tm = om.catalogo()["R-4D-11"]["empuxo_n"]
    out = nativo({"gerado_por": "tools/isp_44_bocal.py", "status": "NÃO VALIDADO", "natureza": "cálculo sobre dois pontos com fonte; não é dado do fabricante", "pontos": {"164:1": i1, "300:1": i2, "fonte": rd["164:1"]["fonte"]},
                  "razao_observada_300_164": i2 / i1, "central": central, "baixo": baixo, "alto": alto, "isp_44_s": {"baixo": baixo["isp_s"]["44"], "central": central["isp_s"]["44"], "alto": alto["isp_s"]["44"]},
                  "empuxo_164_n": tm, "fator_empuxo_44": central["cf"]["44"] / central["cf"]["164"], "empuxo_44_n": tm * central["cf"]["44"] / central["cf"]["164"],
                  "varredura_gama": varre, "apollo": {**c["apollo"], "isp_calculado_s": central["isp_s"][str(e40)], "baixo_s": baixo["isp_s"][str(e40)], "alto_s": alto["isp_s"][str(e40)]}})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "isp_44.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out, c)


def escreve_md(o, c):
    ce, ba, al, ap = o["central"], o["baixo"], o["alto"], o["apollo"]
    md = ["# Isp esperado do R-4D-11 com bocal de 44:1 (gerado por tools/isp_44_bocal.py)", "",
          f"**NÃO VALIDADO.** Isp esperado: **{br(ce['isp_s']['44'])} s**, de {br(ba['isp_s']['44'])} a {br(al['isp_s']['44'])} s com o arredondamento dos dados. É cálculo, não dado do fabricante. NASA CEA não está no workspace.", "",
          "## Modelo", "", "Mesmo motor: câmara, pressão e mistura iguais; muda só a razão de expansão ε. Com bocal ideal, para gás de γ constante:", "",
          "- Γ = √γ · (2/(γ+1))^((γ+1)/(2(γ−1)))",
          "- ε = Γ / √( 2γ/(γ−1) · x^(2/γ) · (1 − x^((γ−1)/γ)) ), com x = pe/pc",
          "- CF = Γ · √( 2γ/(γ−1) · (1 − x^((γ−1)/γ)) ) + ε · x",
          "- Isp = K · CF, com K = η c* / g0", "",
          f"Os dois pontos fixam as duas incógnitas: Isp(300:1)/Isp(164:1) = {br(o['pontos']['300:1'], 1)}/{br(o['pontos']['164:1'], 0)} = {br(o['razao_observada_300_164'], 5)} dá γ, e o 164:1 dá K. Fonte: {o['pontos']['fonte']}. γ e K são efetivos: absorvem perdas que variam com ε, e γ não é o do gás real. O γ ajustado não foi comparado com um cálculo de equilíbrio.", "",
          "## Conta", "", "| Caso | Isp 164:1 (s) | Isp 300:1 (s) | γ efetivo | K (s) | CF 44:1 | CF 164:1 | CF 300:1 | Isp 44:1 (s) | Isp 40:1 (s) |", "| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
    m1, m2 = c["meia_resolucao_s"]["164:1"], c["meia_resolucao_s"]["300:1"]
    for nome, x, a, b in (("Central", ce, 0, 0), ("Baixo: extremos do arredondamento", ba, -m1, m2), ("Alto: extremos do arredondamento", al, m1, -m2)):
        md.append(f"| {nome} | {br(o['pontos']['164:1'] + a, 2)} | {br(o['pontos']['300:1'] + b, 2)} | {br(x['gama'], 4)} | {br(x['k_s'], 2)} | {br(x['cf']['44'], 4)} | {br(x['cf']['164'], 4)} | {br(x['cf']['300'], 4)} | {br(x['isp_s']['44'], 2)} | {br(x['isp_s']['40'], 2)} |")
    md += ["", f"A meia resolução dos dados (±{br(m1, 2)} s e ±{br(m2, 2)} s) é leitura do último dígito publicado, sem fonte, NÃO VALIDADA.", "",
           "## Empuxo", "", f"Com a mesma câmara e a mesma vazão, o empuxo escala com CF: {br(o['empuxo_164_n'], 0)} N × {br(o['fator_empuxo_44'], 4)} = **{br(o['empuxo_44_n'], 0)} N** (NÃO VALIDADO). O desenho de [F228] dá as cotas do 44:1, mas nenhum Isp, massa ou empuxo. A massa segue sem fonte.", "",
           "## Sensibilidade a γ", "", "γ imposto (NÃO VALIDADO), com K calibrado em um só ponto. A diferença entre as âncoras mostra quanto o γ imposto deixa de reproduzir os dois pontos.", "",
           "| γ | Razão CF 300/164 | Isp 44:1, âncora 164:1 (s) | Isp 44:1, âncora 300:1 (s) |", "| -: | -: | -: | -: |"]
    md += [f"| {br(x['gama'], 2)} | {br(x['razao_300_164'], 5)} | {br(x['isp_ancora_164_s'])} | {br(x['isp_ancora_300_s'])} |" for x in o["varredura_gama"]]
    md += ["", "## Comparação com o R-4D do Apollo", "",
           f"O modelo dá {br(ap['isp_calculado_s'])} s em ε = {ap['razao_expansao']}, de {br(ap['baixo_s'])} a {br(ap['alto_s'])} s. {ap['fonte']}. O valor calculado fica dentro do que a fonte relata para 295 a 300 s.", "",
           f"**Isto é uma comparação, não uma verificação.** {ap['ressalva']}", "",
           "## Os análogos de 304 a 314 s", "", "Decisão do Fabio (2026-11-07): não são coerentes com o R-4D-11. Têm câmara de irídio e rênio, ou só o resumo cita essa tecnologia, ou outro injetor ([F239], [F240]; results/etapa7.2/rotas_mav.md). Ficam na rota A só como comparação."]
    (SAIDA / "isp_44.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
