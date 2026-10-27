"""Varredura da órbita de encontro (Etapa 2.1): massa total na órbita baixa × apoapse.

Periapse fixo (config/superficie.yaml, varredura_encontro), apoapse de 380 km até o da órbita de 1 sol.
Em cada ponto: MAV até a órbita de encontro, lander com entrada direta (P-018), lander e orbitador com
estágio próprio de saída da Terra (lançamentos separados), orbitador com o Δv extra para descer da órbita
de 1 sol até a de encontro e para a injeção trans-Terra a partir dela. Duas versões do orbitador: só
químico e com aerofrenagem (P-020) na descida.
Saída: results/etapa2.1/varredura_encontro_<nome>.yaml, .md e .png (nome = rp250, rp300; com sufixo da opção do MAV em
tools/mav_propulsao.py). Os arquivos sem sufixo de uma versão anterior foram removidos (nota de 2026-10-27 em docs/etapa2.1_superficie.md).

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


def dv_extra_orbitador(mu, um_sol, rp, ra, c3l, descer):
    """Δv extra do orbitador para usar a órbita de encontro rp × ra em vez da de 1 sol (km/s).

    Descer da órbita de 1 sol até a de encontro, mais o custo extra da injeção trans-Terra: o menor entre
    partir da órbita de encontro ou voltar à de 1 sol."""
    vinf = np.sqrt(c3l)
    tei_1sol = float(mn.dv_hiperbole_orbita(mu, vinf, um_sol.rp, um_sol.ra))
    tei_alvo = float(mn.dv_hiperbole_orbita(mu, vinf, rp, ra))
    voltar = mn.dv_transferencia_coaxial(mu, rp, ra, um_sol.rp, um_sol.ra) + tei_1sol
    return descer + min(tei_alvo, voltar) - tei_1sol


def varrer(nome, vr, cfg, dcfg, cu, p, R, ctx, mav_massas=None, sufixo="", saida=None, gravar=True):
    """`mav_massas(dv)` → (massa pousada do MAV e equipamentos, massa extra no cruzeiro); padrão: MAV sólido.

    Devolve (pontos, mínimos, escolha). Com `gravar=False` não escreve arquivos (usado pela Etapa 2.3)."""
    saida = SAIDA if saida is None else saida
    mu, margem, um_sol = p.mu_marte, _v(dcfg["margem_dv"]), p.orbitas_marte["eliptica_alta"]
    v_eq, lat, inc, dv100, plat, razao, walkout, vs, a_caso, c3l = ctx
    rp = R + vr["periapse_alt_km"]
    apos = np.geomspace(vr["apoapse_alt_km"][0], vr["apoapse_alt_km"][1], vr["pontos"])
    base = dcfg["caso_base"]

    def orbitador(extra, var):
        c2 = copy.deepcopy(dcfg)
        c2["dv"]["encontro_orbita_marte"]["valor"] = _v(dcfg["dv"]["encontro_orbita_marte"]) + extra
        try:
            m = dm.massa_leo(vs[var], c2, cu, base["carga_util"], margem, float(base["acrescimo_capsula"]))[0]
        except ValueError:
            return float("inf")
        return m if m == m else float("inf")

    linhas = []
    for ap in apos:
        ra = R + ap
        dv_mav = sf.dv_subida(mu, R, dv100, rp, ra, v_eq, inc, lat)
        if mav_massas is None:
            glom, _ = mav((1 + margem) * dv_mav, cfg)
            cruz = 0.0
        else:
            glom, cruz = mav_massas((1 + margem) * dv_mav)
        lander = lander_leo((glom + plat) / razao + cruz, cfg, dcfg, p, a_caso)
        # Orbitador: da órbita de 1 sol até a de encontro (baixa o apoapse no periapse; ajusta o periapse no
        # apoapse) e custo extra da injeção trans-Terra (o menor entre partir da órbita de encontro ou voltar a 1 sol).
        descer_q = mn.dv_transferencia_coaxial(mu, um_sol.rp, um_sol.ra, rp, ra)
        reg = {"apoapse_alt_km": round(float(ap), 1), "dv_mav_km_s": round(dv_mav, 4), "mav_glom_kg": round(glom, 1),
               "lander_orbita_baixa_kg": round(lander, 1)}
        for versao in vr["versoes"]:
            descer = min(descer_q, walkout) if versao == "aerofrenagem" else descer_q
            res = {}
            for caso, var in (("missao_A", "missao_A"), ("regra_iii", dcfg["regra_projeto"])):
                extra = dv_extra_orbitador(mu, um_sol, rp, ra, c3l[caso], descer)
                m = orbitador(extra, var)
                res[f"dv_extra_orbitador_{caso}_km_s"] = round(extra, 4)
                res[f"orbitador_{caso}_kg"] = round(m, 1)
                res[f"total_{caso}_kg"] = round(m + lander, 1)
            reg[versao] = res
        linhas.append(reg)

    minimos = {}
    for versao in vr["versoes"]:
        for caso in ("total_missao_A_kg", "total_regra_iii_kg"):
            r = min(linhas, key=lambda x: x[versao][caso])
            minimos[f"{versao}/{caso}"] = {"apoapse_alt_km": r["apoapse_alt_km"], "massa_kg": r[versao][caso],
                                           "mav_glom_kg": r["mav_glom_kg"],
                                           "no_extremo": r is linhas[0] or r is linhas[-1]}
    escolha = None
    if "regra_escolha" in vr:
        tol, caso = vr["regra_escolha"]["tolerancia_relativa"], vr["regra_escolha"]["caso"]
        versao = vr["versoes"][0]
        mmin = min(x[versao][caso] for x in linhas)
        r = next(x for x in linhas if x[versao][caso] <= (1 + tol) * mmin)  # apoapses em ordem crescente
        escolha = {"regra": f"menor apoapse com {caso} ≤ (1 + {tol}) × mínimo", "versao": versao,
                   "minimo_kg": mmin, "apoapse_alt_km": r["apoapse_alt_km"], "massa_regra_iii_kg": r[versao]["total_regra_iii_kg"],
                   "massa_missao_A_kg": r[versao]["total_missao_A_kg"], "acima_do_minimo": r[versao][caso] / mmin - 1,
                   "mav_glom_kg": r["mav_glom_kg"], "dv_mav_km_s": r["dv_mav_km_s"],
                   "lander_orbita_baixa_kg": r["lander_orbita_baixa_kg"]}
    if not gravar:
        return linhas, minimos, escolha
    saida.mkdir(parents=True, exist_ok=True)
    nome = nome + sufixo
    (saida / f"varredura_encontro_{nome}.yaml").write_text(yaml.safe_dump(dm._nativo(
        {"gerado_por": "tools/varredura_encontro.py", "periapse_alt_km": vr["periapse_alt_km"],
         "minimos": minimos, "escolha": escolha, "pontos": linhas}), sort_keys=False, allow_unicode=True), encoding="utf-8")

    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    md = [f"# Varredura da órbita de encontro, periapse {vr['periapse_alt_km']} km (gerado por tools/varredura_encontro.py)", "",
          f"Apoapse de {vr['apoapse_alt_km'][0]} a {vr['apoapse_alt_km'][1]} km, {vr['pontos']} pontos. Massa total na órbita "
          "baixa da Terra = orbitador + lander (lançamentos separados). Massas em kg.", "",
          "| Versão do orbitador | Caso | Apoapse do mínimo | Massa total no mínimo | MAV no mínimo | No extremo? |",
          "| :- | :- | -: | -: | -: | :- |"]
    for k, m in minimos.items():
        v, c = k.split("/")
        md.append(f"| {v} | {'missão A' if 'missao_A' in c else 'regra (iii)'} | {br(m['apoapse_alt_km'])} km | "
                  f"{br(m['massa_kg'])} | {br(m['mav_glom_kg'])} | {'sim' if m['no_extremo'] else 'não'} |")
    if escolha:
        md += ["", f"**Regra de escolha (ADR 0005):** {escolha['regra']}. Resultado: apoapse de **{br(escolha['apoapse_alt_km'])} km**, "
               f"total de {br(escolha['massa_regra_iii_kg'])} kg pela regra (iii) ({br(100 * escolha['acima_do_minimo'], 1)} % acima do mínimo "
               f"de {br(escolha['minimo_kg'])} kg) e {br(escolha['massa_missao_A_kg'])} kg na missão A; MAV de {br(escolha['mav_glom_kg'])} kg."]
    v0 = vr["versoes"][0]
    md += ["", "Pontos selecionados:", "",
           "| Apoapse (km) | Δv MAV | MAV (kg) | Lander | " + " | ".join(f"Total {v}: A / (iii)" for v in vr["versoes"]) + " |",
           "| -: | -: | -: | -: |" + " -: |" * len(vr["versoes"])]
    for r in linhas[:: max(1, len(linhas) // 15)] + [linhas[-1]]:
        md.append(f"| {br(r['apoapse_alt_km'])} | {br(r['dv_mav_km_s'], 3)} | {br(r['mav_glom_kg'])} | {br(r['lander_orbita_baixa_kg'])} | "
                  + " | ".join(f"{br(r[v]['total_missao_A_kg'])} / {br(r[v]['total_regra_iii_kg'])}" for v in vr["versoes"]) + " |")
    (saida / f"varredura_encontro_{nome}.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(11, 6), facecolor=SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    x = [r["apoapse_alt_km"] for r in linhas]
    estilos = {"quimico": (AZUL, "Orbitador só químico"), "aerofrenagem": (LARANJA, "Orbitador com aerofrenagem (P-020)")}
    for versao in vr["versoes"]:
        cor, rot = estilos[versao]
        for caso, ls, rc in (("total_regra_iii_kg", "-", "regra (iii)"), ("total_missao_A_kg", "--", "missão A")):
            ax.plot(x, [r[versao][caso] / 1000 for r in linhas], ls, color=cor, lw=2 if ls == "-" else 1.5, label=f"{rot}, {rc}")
            m = minimos[f"{versao}/{caso}"]
            outro = minimos.get(f"{'aerofrenagem' if versao == 'quimico' else 'quimico'}/{caso}")
            coincide = outro is not None and abs(outro["apoapse_alt_km"] - m["apoapse_alt_km"]) < 1 and abs(outro["massa_kg"] - m["massa_kg"]) < 1
            if coincide and versao == "aerofrenagem":
                continue
            ax.plot(m["apoapse_alt_km"], m["massa_kg"] / 1000, "o", ms=9, mfc=cor, mec=SUPERFICIE, mew=2)
            texto = f"mín. {br(m['massa_kg'] / 1000, 1)} t" + (" (as duas versões)" if coincide else "")
            ax.annotate(texto, (m["apoapse_alt_km"], m["massa_kg"] / 1000),
                        xytext=(-175 if coincide else 8, 10 if coincide else (-16 if ls == "-" else 8)),
                        textcoords="offset points", fontsize=8, color=TINTA)
    if escolha:
        ax.axvline(escolha["apoapse_alt_km"], color=TINTA_2, lw=1, ls=":")
        ax.plot(escolha["apoapse_alt_km"], escolha["massa_regra_iii_kg"] / 1000, "D", ms=8, mfc=TINTA, mec=SUPERFICIE, mew=1.5,
                label="Escolha pela regra do ADR 0005 (≤ 5 % acima do mínimo)")
        ax.annotate(f"escolha: {br(escolha['apoapse_alt_km'])} km, {br(escolha['massa_regra_iii_kg'] / 1000, 1)} t",
                    (escolha["apoapse_alt_km"], escolha["massa_regra_iii_kg"] / 1000), xytext=(-150, 16),
                    textcoords="offset points", fontsize=8, color=TINTA)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(top=500)
    ax.set_xlabel(f"Apoapse da órbita de encontro (km de altitude; periapse fixo em {vr['periapse_alt_km']} km)", color=TINTA_2)
    ax.set_ylabel("Massa total na órbita baixa da Terra (t)", color=TINTA_2)
    ax.set_title(f"Varredura da órbita de encontro, periapse {vr['periapse_alt_km']} km: orbitador + lander", color=TINTA, loc="left")
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
    fig.savefig(saida / f"varredura_encontro_{nome}.png", dpi=150, facecolor=SUPERFICIE)
    plt.close(fig)
    print("\n".join(md[:12 + (2 if escolha else 0)]))
    return linhas, minimos, escolha


def main():
    cfg = _ler("config/superficie.yaml")
    dcfg = _ler("config/dimensionamento.yaml")
    po = _ler("config/parametros_orbitais.yaml")
    cu = _ler("config/carga_util.yaml")
    ms = _ler("results/etapa1.3/missoes.yaml")
    p = dm.parametros()
    R = _v(po["raio_marte_km"])
    a_caso, jan, piores = dm.casos(dcfg, p)
    vs = dm.variantes(a_caso, jan, piores)
    cand = {c["id"]: c for c in ms["candidatas"]}
    ref = _ler("config/missao_referencia.yaml")["missao_referencia"]["id"]
    janelas = [cand[v["missao"]] for v in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()]
    c3l = {"missao_A": cand[ref]["c3l_partida_marte_km2_s2"], "regra_iii": max(x["c3l_partida_marte_km2_s2"] for x in janelas)}
    ctx = (2 * np.pi * R / _v(cfg["marte"]["periodo_rotacao_s"]), _v(cfg["sitio_e_encontro"]["latitude_sitio_graus"]),
           _v(cfg["sitio_e_encontro"]["inclinacao_encontro_graus"]), _v(cfg["subida"]["dv_100x100_km_s"]),
           _v(cfg["lander"]["plataforma_superficie_kg"]), _v(cfg["lander"]["razao_pousada_entrada"]["entrada_direta"]),
           _v(cfg["aerofrenagem"]["dv_saida_aerofrenagem_km_s"]), vs, a_caso, c3l)
    for nome, vr in cfg["varreduras_encontro"].items():
        varrer(nome, vr, cfg, dcfg, cu, p, R, ctx)


if __name__ == "__main__":
    main()
