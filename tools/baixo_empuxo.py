"""Etapa 3.2: modelo de baixo empuxo, verificado.

  1. Verificação: a espiral numérica com aceleração tangencial constante (orbital.baixo_empuxo) contra a integração
     numérica publicada por Schwenzfeger (NASA TM X-64836, 1973) [F113], ε = 0,01, nos pontos da listagem da p. 31.
  2. Conferência: espiral numérica contra a solução analítica quase circular (Edelbaum, forma coplanar), para ε em
     config/baixo_empuxo.yaml, em dois casos adimensionais: descida em Marte e subida heliocêntrica Terra → Marte. O
     trecho heliocêntrico fica como "calculado, não verificado" (nenhum caso publicado comparável).
Saída: results/etapa3.2/baixo_empuxo.yaml e baixo_empuxo.md

Uso: python tools/baixo_empuxo.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital import baixo_empuxo as be  # noqa: E402
from orbital.config import ler, nativo, parametros, v  # noqa: E402
from orbital.constantes import GM_SOL, UA_KM  # noqa: E402

SAIDA = RAIZ / "results" / "etapa3.2"
VARS = ("r", "phi", "u", "v", "h")


def main():
    cfg = ler("config/baixo_empuxo.yaml")
    arr = {k: v(x) for k, x in cfg["arredondamento_resultados"].items()}
    rd = lambda x, q: round(round(x / q) * q, 12)  # noqa: E731

    # 1. Verificação contra [F113]
    vs = cfg["verificacao_schwenzfeger"]
    tol = v(vs["tolerancia_relativa"])
    calc = be.trajetoria_aceleracao_constante(v(vs["eps"]), [p["t"] for p in vs["pontos"]])
    pontos = []
    for p, c in zip(vs["pontos"], calc):
        dif = {k: (c[k] - p[k]) / abs(p[k]) for k in VARS}
        # informativo (não é o critério declarado): erro dos vetores posição e velocidade relativo ao módulo de cada um
        e_pos = math.hypot(c["r"] - p["r"], p["r"] * (c["phi"] - p["phi"])) / p["r"]
        e_vel = math.hypot(c["u"] - p["u"], c["v"] - p["v"]) / math.hypot(p["u"], p["v"])
        pontos.append({"t": p["t"], "publicado": {k: p[k] for k in VARS}, "calculado": c, "diferenca_relativa": dif,
                       "erro_relativo_vetor_posicao": e_pos, "erro_relativo_vetor_velocidade": e_vel,
                       "dentro_da_tolerancia": all(abs(d) <= tol for d in dif.values()),
                       "fora_da_tolerancia": [k for k in VARS if abs(dif[k]) > tol]})
    verif = {"fonte": "[F113] p. 31", "eps": v(vs["eps"]), "tolerancia_relativa": tol, "pontos": pontos,
             "verificado": all(p["dentro_da_tolerancia"] for p in pontos)}

    # 2. Conferência Edelbaum × numérico
    p = parametros()
    R = v(ler("config/parametros_orbitais.yaml")["raio_marte_km"])
    enc = ler("results/etapa2.3/plataformas.yaml")["orbita_encontro"]
    a_enc = R + (enc["periapse_alt_km"] + enc["apoapse_regra_5pct_km"]) / 2
    r_baixa = R + enc["periapse_alt_km"]
    hc = cfg["conferencia_edelbaum"]["casos"]["heliocentrico"]
    r_terra = v(hc["raio_terra_ua"]) * UA_KM
    r_marte = v(ler("config/mav_propulsao.yaml")["cruzeiro"]["distancia_marte_ua"]) * UA_KM
    casos = {"marte": (cfg["conferencia_edelbaum"]["casos"]["marte"]["nome"], p.mu_marte, a_enc, r_baixa),
             "heliocentrico": (hc["nome"], GM_SOL, r_terra, r_marte)}
    conf = {}
    for k, (nome, mu, r0, r1) in casos.items():
        v0 = math.sqrt(mu / r0)
        ed = be.dv_edelbaum_coplanar(1.0, 1.0, r1 / r0)
        linhas = []
        for eps in cfg["conferencia_edelbaum"]["eps"]["valor"]:
            e = be.espiral(1.0, 1.0, r1 / r0, aceleracao=eps)
            linhas.append({"eps": eps, "dv_numerico_adim": e.dv, "dv_edelbaum_adim": ed, "diferenca_relativa": (e.dv - ed) / ed,
                           "duracao_adim": e.duracao, "voltas": rd(e.revolucoes, arr["voltas"]),
                           "raio_final_adim": rd(e.raio_final, arr["raio_e_excentricidade"]),
                           "excentricidade_final": rd(e.excentricidade_final, arr["raio_e_excentricidade"])})
        conf[k] = {"nome": nome, "mu_km3_s2": mu, "r0_km": r0, "r1_km": r1, "razao_r1_r0": r1 / r0,
                   "v0_km_s": v0, "dv_edelbaum_km_s": ed * v0, "unidade_de_tempo_s": math.sqrt(r0 ** 3 / mu),
                   "aceleracao_de_referencia_km_s2": mu / r0 ** 2, "linhas": linhas}

    out = {"gerado_por": "tools/baixo_empuxo.py", "verificacao_schwenzfeger": verif, "conferencia_edelbaum": conf}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "baixo_empuxo.yaml").write_text(yaml.safe_dump(nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")

    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    ex = lambda x: f"{x:+.1e}".replace(".", ",").replace("-", "−")  # noqa: E731
    ab = lambda x: f"{x:.1e}".replace(".", ",").replace("-", "−")  # noqa: E731
    md = ["# Modelo de baixo empuxo (gerado por tools/baixo_empuxo.py)", "",
          "## 1. Verificação contra Schwenzfeger, NASA TM X-64836 (1973), p. 31 [F113]", "",
          f"Subida com aceleração tangencial constante ε = {br(verif['eps'], 2)} a partir de órbita circular, adimensional "
          "(r0 = v0 = μ = 1). u = r·ṙ, v = r·v_θ, h = energia por massa. Diferença relativa = (calculado − publicado) / "
          f"|publicado|, por componente; tolerância {br(tol * 100, 2)} % (P-046). **Verificado: {'sim' if verif['verificado'] else 'NÃO'}"
          + ("" if verif["verificado"] else f" (fora da tolerância: {', '.join(sorted({k for q in pontos for k in q['fora_da_tolerancia']}))})") + ".**",
          "As duas últimas colunas (informativas, não são o critério declarado) dão o erro dos vetores posição e velocidade "
          "relativo ao módulo de cada um.", "",
          "| t | r publicado | r calculado | Dif. r | Dif. φ | Dif. u | Dif. v | Dif. h | Vetor posição | Vetor velocidade |",
          "| -: | -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
    for q in pontos:
        d = q["diferenca_relativa"]
        md.append(f"| {br(q['t'], 4)} | {br(q['publicado']['r'], 7)} | {br(q['calculado']['r'], 7)} | "
                  + " | ".join(ex(d[k]) for k in VARS) + f" | {ab(q['erro_relativo_vetor_posicao'])} | {ab(q['erro_relativo_vetor_velocidade'])} |")
    md += ["", "## 2. Conferência: espiral numérica × solução analítica quase circular (Edelbaum, coplanar)", "",
           "Não é verificação: as duas soluções são deste estudo. ε = aceleração / (μ/r0²); tempo em unidades de "
           "√(r0³/μ). A espiral para quando a energia chega à da órbita circular de raio r1.", ""]
    for k, c in conf.items():
        md += [f"### {c['nome']}", "",
               f"r0 = {br(c['r0_km'])} km, r1 = {br(c['r1_km'])} km (r1/r0 = {br(c['razao_r1_r0'], 4)}); "
               f"Δv de Edelbaum = {br(c['dv_edelbaum_km_s'], 3)} km/s; unidade de tempo {br(c['unidade_de_tempo_s'])} s; "
               f"aceleração de referência μ/r0² = {br(c['aceleracao_de_referencia_km_s2'] * 1e3, 4)} m/s².", "",
               "| ε | Δv numérico (adim.) | Δv Edelbaum (adim.) | Diferença relativa | Duração (adim.) | Voltas | Raio final / r0 | Excentricidade final |",
               "| -: | -: | -: | -: | -: | -: | -: | -: |"]
        for x in c["linhas"]:
            md.append(f"| {x['eps']:.0e} | {br(x['dv_numerico_adim'], 7)} | {br(x['dv_edelbaum_adim'], 7)} | {ex(x['diferenca_relativa'])} | "
                      f"{br(x['duracao_adim'], 1)} | {br(x['voltas'], 1)} | {br(x['raio_final_adim'], 4)} | {br(x['excentricidade_final'], 4)} |")
        md.append("")
    md += ["O trecho heliocêntrico é **calculado, não verificado**: não foi encontrado caso publicado comparável "
           "(docs/etapa3.2_baixo_empuxo.md)."]
    (SAIDA / "baixo_empuxo.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
