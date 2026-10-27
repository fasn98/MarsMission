"""Varredura da órbita de encontro (Etapa 2.1): massa total na órbita baixa × apoapse.

Periapse fixo (config/superficie.yaml, varredura_encontro), apoapse de 380 km até o da órbita de 1 sol.
Em cada ponto: MAV até a órbita de encontro, lander com entrada direta (P-018), lander e orbitador com
estágio próprio de saída da Terra (lançamentos separados), orbitador com o Δv extra para descer da órbita
de 1 sol até a de encontro e para a injeção trans-Terra a partir dela. Duas versões do orbitador: só
químico e com aerofrenagem (P-020) na descida.
Saída: results/etapa2.1/varredura_encontro.yaml, .md e .png

Uso: python tools/varredura_encontro.py
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import yaml  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(RAIZ / "src"), str(RAIZ / "tools")]

import dimensionamento as dm  # noqa: E402
from orbital import manobras as mn  # noqa: E402
from orbital import superficie as sf  # noqa: E402
from superficie import _ler, _v, lander_leo, mav  # noqa: E402

SAIDA = RAIZ / "results" / "etapa2.1"
TINTA, TINTA_2, SUPERFICIE, GRADE = "#0b0b0b", "#52514e", "#fcfcfb", "#eceae4"
AZUL, LARANJA = "#2a78d6", "#eb6834"


def main():
    cfg = _ler("config/superficie.yaml")
    dcfg = _ler("config/dimensionamento.yaml")
    po = _ler("config/parametros_orbitais.yaml")
    cu = _ler("config/carga_util.yaml")
    p = dm.parametros()
    mu, R = p.mu_marte, _v(po["raio_marte_km"])
    margem = _v(dcfg["margem_dv"])
    um_sol = p.orbitas_marte["eliptica_alta"]
    v_eq = 2 * np.pi * R / _v(cfg["marte"]["periodo_rotacao_s"])
    lat = _v(cfg["sitio_e_encontro"]["latitude_sitio_graus"])
    inc = _v(cfg["sitio_e_encontro"]["inclinacao_encontro_graus"])
    dv100 = _v(cfg["subida"]["dv_100x100_km_s"])
    vr = cfg["varredura_encontro"]
    rp = R + vr["periapse_alt_km"]
    if abs(rp - um_sol.rp) > 1e-6:
        raise ValueError("a varredura supõe o mesmo periapse da órbita de 1 sol")
    apos = np.geomspace(vr["apoapse_alt_km"][0], vr["apoapse_alt_km"][1], vr["pontos"])
    walkout = _v(cfg["aerofrenagem"]["dv_saida_aerofrenagem_km_s"])
    plat = _v(cfg["lander"]["plataforma_superficie_kg"])
    razao = _v(cfg["lander"]["razao_pousada_entrada"]["entrada_direta"])

    a_caso, jan, piores = dm.casos(dcfg, p)
    vs = dm.variantes(a_caso, jan, piores)
    base = dcfg["caso_base"]

    def orbitador(extra, var):
        c2 = copy.deepcopy(dcfg)
        c2["dv"]["encontro_orbita_marte"]["valor"] = _v(dcfg["dv"]["encontro_orbita_marte"]) + extra
        try:
            m = dm.massa_leo(vs[var], c2, cu, base["carga_util"], margem, float(base["acrescimo_capsula"]))[0]
        except ValueError:
            return float("inf")
        return m if m == m else float("inf")

    v_p_1sol = mn.v_orbita(mu, rp, um_sol.rp, um_sol.ra)
    linhas = []
    for ap in apos:
        ra = R + ap
        dv_mav = sf.dv_subida(mu, R, dv100, rp, ra, v_eq, inc, lat)
        glom, _ = mav((1 + margem) * dv_mav, cfg)
        chegada = (glom + plat) / razao
        lander = lander_leo(chegada, cfg, dcfg, p, a_caso)
        # Descer (queima no periapse que baixa o apoapse) e o custo extra da injeção trans-Terra, também
        # no periapse: os dois valem v_p(1 sol) − v_p(encontro).
        delta = v_p_1sol - mn.v_orbita(mu, rp, rp, ra)
        reg = {"apoapse_alt_km": round(float(ap), 1), "dv_mav_km_s": round(dv_mav, 4), "mav_glom_kg": round(glom, 1),
               "lander_orbita_baixa_kg": round(lander, 1)}
        for versao, descer in (("quimico", delta), ("aerofrenagem", min(delta, walkout))):
            extra = descer + delta
            oa, oi = orbitador(extra, "missao_A"), orbitador(extra, dcfg["regra_projeto"])
            reg[versao] = {"dv_extra_orbitador_km_s": round(extra, 4), "orbitador_missao_A_kg": round(oa, 1),
                           "orbitador_regra_iii_kg": round(oi, 1), "total_missao_A_kg": round(oa + lander, 1),
                           "total_regra_iii_kg": round(oi + lander, 1)}
        linhas.append(reg)

    minimos = {}
    for versao in ("quimico", "aerofrenagem"):
        for caso in ("total_missao_A_kg", "total_regra_iii_kg"):
            r = min(linhas, key=lambda x: x[versao][caso])
            minimos[f"{versao}/{caso}"] = {"apoapse_alt_km": r["apoapse_alt_km"], "massa_kg": r[versao][caso],
                                           "mav_glom_kg": r["mav_glom_kg"],
                                           "no_extremo": r["apoapse_alt_km"] in (linhas[0]["apoapse_alt_km"], linhas[-1]["apoapse_alt_km"])}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "varredura_encontro.yaml").write_text(yaml.safe_dump(dm._nativo(
        {"gerado_por": "tools/varredura_encontro.py", "periapse_alt_km": vr["periapse_alt_km"],
         "minimos": minimos, "pontos": linhas}), sort_keys=False, allow_unicode=True), encoding="utf-8")

    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    md = ["# Varredura da órbita de encontro (gerado por tools/varredura_encontro.py)", "",
          f"Periapse fixo em {vr['periapse_alt_km']} km; apoapse de {vr['apoapse_alt_km'][0]} a {vr['apoapse_alt_km'][1]} km. "
          "Massa total na órbita baixa da Terra = orbitador + lander (lançamentos separados). Massas em kg.", "",
          "| Versão do orbitador | Caso | Apoapse do mínimo | Massa total no mínimo | MAV no mínimo | Mínimo no extremo da varredura? |",
          "| :- | :- | -: | -: | -: | :- |"]
    for k, m in minimos.items():
        v, c = k.split("/")
        md.append(f"| {v} | {'missão A' if 'missao_A' in c else 'regra (iii)'} | {br(m['apoapse_alt_km'])} km | "
                  f"{br(m['massa_kg'])} | {br(m['mav_glom_kg'])} | {'sim' if m['no_extremo'] else 'não'} |")
    md += ["", "Pontos selecionados:", "",
           "| Apoapse (km) | Δv MAV | MAV (kg) | Lander na órbita baixa | Total químico: A / (iii) | Total com aerofrenagem: A / (iii) |",
           "| -: | -: | -: | -: | -: | -: |"]
    for r in linhas[:: max(1, len(linhas) // 12)] + [linhas[-1]]:
        md.append(f"| {br(r['apoapse_alt_km'])} | {br(r['dv_mav_km_s'], 3)} | {br(r['mav_glom_kg'])} | {br(r['lander_orbita_baixa_kg'])} | "
                  f"{br(r['quimico']['total_missao_A_kg'])} / {br(r['quimico']['total_regra_iii_kg'])} | "
                  f"{br(r['aerofrenagem']['total_missao_A_kg'])} / {br(r['aerofrenagem']['total_regra_iii_kg'])} |")
    (SAIDA / "varredura_encontro.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # Gráfico
    fig, ax = plt.subplots(figsize=(11, 6), facecolor=SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    x = [r["apoapse_alt_km"] for r in linhas]
    estilos = {"quimico": (AZUL, "Orbitador só químico"), "aerofrenagem": (LARANJA, "Orbitador com aerofrenagem (P-020)")}
    for versao, (cor, rot) in estilos.items():
        for caso, ls, rc in (("total_regra_iii_kg", "-", "regra (iii)"), ("total_missao_A_kg", "--", "missão A")):
            y = [r[versao][caso] / 1000 for r in linhas]
            ax.plot(x, y, ls, color=cor, lw=2 if ls == "-" else 1.5, label=f"{rot}, {rc}")
            m = minimos[f"{versao}/{caso}"]
            outro = minimos[f"{'aerofrenagem' if versao == 'quimico' else 'quimico'}/{caso}"]
            coincide = abs(outro["apoapse_alt_km"] - m["apoapse_alt_km"]) < 1 and abs(outro["massa_kg"] - m["massa_kg"]) < 1
            if coincide and versao == "aerofrenagem":
                continue  # mesmo ponto da versão química: um marcador e um rótulo só
            ax.plot(m["apoapse_alt_km"], m["massa_kg"] / 1000, "o", ms=9, mfc=cor, mec=SUPERFICIE, mew=2)
            texto = f"mín. {br(m['massa_kg'] / 1000, 1)} t" + (" (as duas versões)" if coincide else "")
            ax.annotate(texto, (m["apoapse_alt_km"], m["massa_kg"] / 1000), xytext=(-175 if coincide else 8, 10 if coincide else (-16 if ls == "-" else 8)),
                        textcoords="offset points", fontsize=8, color=TINTA)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(top=500)
    ax.set_xlabel("Apoapse da órbita de encontro (km de altitude; periapse fixo em "
                  f"{vr['periapse_alt_km']} km)", color=TINTA_2)
    ax.set_ylabel("Massa total na órbita baixa da Terra (t)", color=TINTA_2)
    ax.set_title("Varredura da órbita de encontro: orbitador + lander", color=TINTA, loc="left")
    fmt_y = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))
    ax.yaxis.set_major_formatter(fmt_y)
    ax.yaxis.set_minor_formatter(fmt_y)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", " ")))
    ax.tick_params(colors=TINTA_2, labelsize=8)
    for s_ in ax.spines.values():
        s_.set_color("#d6d5d0")
    ax.grid(color=GRADE, lw=0.5, which="both")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=8, frameon=False, labelcolor=TINTA)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.text(0.01, 0.01, "Eixo de massa cortado em 500 t (perto da órbita baixa o orbitador químico tende à assíntota da "
             "equação do foguete). Gerado por tools/varredura_encontro.py.", fontsize=6.5, color=TINTA_2)
    fig.savefig(SAIDA / "varredura_encontro.png", dpi=150, facecolor=SUPERFICIE)
    print("\n".join(md))


if __name__ == "__main__":
    main()
