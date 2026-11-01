"""Etapa 7.1: envelope e arranjo dos veículos (Fase 7, CAD paramétrico).

- Tanques: volume a partir das massas de propelente (results/etapa2.5/arquitetura.yaml), da razão de mistura, das
  densidades e da fração de ullage (config/cad.yaml); diâmetro das esferas (orbitador, cruzeiro e descida do lander) e
  comprimento dos tanques cilíndricos do MAV.
- Aeroshell: opções de diâmetro com fonte (Mars 2020 e SRL de lançamento duplo [F202]); altura do conjunto de cruzeiro
  e aeroshell escalada do MSL (P-083).
- MAV: comprimento de baixo para cima (tanques + motores + interestágio + carga, P-085 e P-086), contra o limite do MSR
  [F35], a restrição de 2019 [F216] e o análogo de Bowles [F46].
- Painéis: área do lander (results/etapa4.1) em duas asas (P-088); área do orbitador pela potência no afélio e pela
  densidade de potência por área [F55] com o fator de perdas (P-030).
- Encaixe nas coifas: orbitador no volume útil do Falcon (arquivo STEP do fabricante, [F82]) e lander no envelope do
  Vulcan de 15,5 m [F80], com a margem radial em cada conjunto.
Saída: results/etapa7.1/envelope.yaml e .md, e as vistas 2D results/etapa7.1/*.png

Uso: python tools/envelope_arranjo.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import yaml  # noqa: E402
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.1"
TINTA, TINTA_2, SUPERFICIE, GRADE = "#0b0b0b", "#52514e", "#fcfcfb", "#eceae4"
COR = {"oxidante": "#eb6834", "combustivel": "#2a78d6", "hidrazina": "#1baf7a", "estrutura": "#8a8781", "carga": "#7b5ea7"}


def volumes(m_p, of, rho_ox, rho_fu, ull):
    """Volumes dos tanques de oxidante e de combustível (m³) para m_p kg de propelente bipropelente."""
    m_ox, m_fu = m_p * of / (1 + of), m_p / (1 + of)
    return {"oxidante_kg": m_ox, "combustivel_kg": m_fu,
            "tanque_oxidante_m3": m_ox / rho_ox / (1 - ull), "tanque_combustivel_m3": m_fu / rho_fu / (1 - ull)}


def esfera(vol):
    """Diâmetro interno (m) de uma esfera de volume vol (m³)."""
    return (6 * vol / math.pi) ** (1 / 3)


def tanque_cilindrico(vol, d_int):
    """Comprimento interno (m) de um tanque cilíndrico com tampos hemisféricos de diâmetro d_int e volume vol; se o
    volume cabe numa esfera menor que d_int, o tanque é essa esfera."""
    if vol <= math.pi * d_int ** 3 / 6:
        return esfera(vol)
    return d_int + (vol - math.pi * d_int ** 3 / 6) / (math.pi * d_int ** 2 / 4)


def raio_envelope(perfil, h):
    """Raio do envelope (m) na altura h por interpolação linear do perfil (altura, raio); 0 acima do topo."""
    hs, rs = perfil
    return float(np.interp(h, hs, rs, right=0.0))


def margem_conjunto(perfil, h0, h1, r):
    """Menor folga radial (m) de um conjunto de raio r entre as alturas h0 e h1 (o envelope é amostrado no trecho)."""
    hs = np.linspace(h0, h1, 41)
    return min(raio_envelope(perfil, h) for h in hs) - r


def main():
    cad, arq = ler("config/cad.yaml"), ler("results/etapa2.5/arquitetura.yaml")
    en, pcfg = ler("results/etapa4.1/energia.yaml"), ler("config/plataformas.yaml")
    pr, tq, ae, ds, mv, la, ob = (cad[k] for k in ("propelentes", "tanques", "aeroshell", "descida", "mav", "lander", "orbitador"))
    rho_ox, rho_fu, rho_hz = v(pr["densidade_oxidante_kg_m3"]), v(pr["densidade_mmh_kg_m3"]), v(pr["densidade_hidrazina_kg_m3"])
    ull, of = v(pr["fracao_ullage"]), v(pr["razao_mistura_r4d11"])
    f_ent, f_rad = v(tq["folga_entre_conjuntos_m"]), v(tq["folga_radial_m"])

    # ---------------- orbitador: dois estágios MMH/MON (P-082) + CCRS no topo
    comp_o = {x["item"]: x for x in arq["orbitador"]["composicao"]}
    est_o = {"insercao_marte": next(x for k, x in comp_o.items() if k.startswith("Estágio de inserção")),
             "retorno": next(x for k, x in comp_o.items() if k.startswith("Estágio de retorno"))}
    pares = int(v(tq["pares_por_estagio_orbitador"]))
    rc = v(ob["cilindro_central_diametro_m"]) / 2
    tanques_o = {}
    for nome, x in est_o.items():
        vol = volumes(x["propelente_kg"], of, rho_ox, rho_fu, ull)
        d = esfera(max(vol["tanque_oxidante_m3"], vol["tanque_combustivel_m3"]) / pares)
        d1 = esfera(max(vol["tanque_oxidante_m3"], vol["tanque_combustivel_m3"]))
        tanques_o[nome] = {**vol, "propelente_kg": x["propelente_kg"], "pares": pares, "diametro_esfera_m": d,
                           "raio_conjunto_m": rc + f_rad + d,
                           "alternativa_um_par": {"diametro_esfera_m": d1, "raio_conjunto_m": d1 + f_rad / 2}}
    cc = [float(x) for x in ob["ccrs_m"]["dimensoes"]["valor"]]
    conj_o, h = [], 0.0
    for nome, rot in (("insercao_marte", "Estágio de inserção em Marte"), ("retorno", "Estágio de retorno")):
        t = tanques_o[nome]
        conj_o.append({"conjunto": rot, "h0_m": h, "h1_m": h + t["diametro_esfera_m"], "raio_m": t["raio_conjunto_m"]})
        h += t["diametro_esfera_m"] + f_ent
    conj_o.append({"conjunto": "CCRS (3,4 × 0,5 × 2 m, deitado)", "h0_m": h, "h1_m": h + cc[2], "raio_m": math.hypot(cc[0] / 2, cc[1] / 2)})
    fal = cad["coifas"]["falcon_padrao"]["perfil"]
    perf_f = ([float(x) for x in fal["altura_m"]], [float(x) for x in fal["raio_m"]])
    for c in conj_o:
        c["margem_radial_m"] = margem_conjunto(perf_f, c["h0_m"], c["h1_m"], c["raio_m"])
    oe = pcfg["orbitador"]["energia"]
    d_af = en["orbitador"]["afelio_marte_ua"]
    area_o = (en["orbitador"]["adotada"]["painel_w_afelio"] * d_af ** 2
              / (v(pcfg["lander"]["energia"]["densidade_area_painel_w_m2"]) * v(oe["fator_perdas_painel"])))
    orbitador = {"tanques": tanques_o, "conjuntos": conj_o, "altura_total_m": conj_o[-1]["h1_m"],
                 "topo_envelope_m": perf_f[0][-1], "cabe": all(c["margem_radial_m"] >= 0 for c in conj_o) and conj_o[-1]["h1_m"] <= perf_f[0][-1],
                 "area_paineis_m2": area_o, "ees_diametro_m": v(ob["ees_diametro_m"]), "ccrs_m": cc}

    # ---------------- lander: estágio de cruzeiro + aeroshell (opções de diâmetro) no Vulcan de 15,5 m
    vul = cad["coifas"]["vulcan_15_5"]["perfil"]
    perf_v = ([(s - vul["estacao_interface_pol"]) * 0.0254 for s in vul["estacao_pol"]], [d / 2000 for d in vul["diametro_mm"]])
    m_ent = arq["lander"]["massa_entrada_kg"]
    msl = ae["msl_conjunto"]
    opcoes = {}
    for k, o in ae["opcoes"].items():
        dmt = v(o["diametro_m"])
        alt = v(msl["altura_m"]) * dmt / v(msl["diametro_m"])   # P-083
        opcoes[k] = {"diametro_m": dmt, "altura_conjunto_m": alt,
                     "margem_radial_vulcan_m": margem_conjunto(perf_v, 0.0, alt, dmt / 2),
                     "diametro_util_interno_m": dmt - 2 * v(ae["folga_interna_m"]),
                     "massa_entrada_referencia_kg": v(o["massa_entrada_kg"]) if "massa_entrada_kg" in o else v(o["massa_entrada_min_kg"]),
                     "referencia_e_minimo": "massa_entrada_min_kg" in o}
        # massa por área de referência (kg/m²): a do lander nesse diâmetro e a da referência no mesmo diâmetro
        area = math.pi * dmt ** 2 / 4
        opcoes[k]["massa_por_area_lander_kg_m2"] = m_ent / area
        opcoes[k]["massa_por_area_referencia_kg_m2"] = opcoes[k]["massa_entrada_referencia_kg"] / area
    cz = next(x for x in arq["lander"]["composicao"] if x["item"].startswith("Estágio de cruzeiro"))
    vol_cz = volumes(cz["propelente_kg"], v(pr["razao_mistura_cruzeiro_lander"]), rho_ox, rho_fu, ull)
    m_desc = v(ds["msl_propelente_kg"]) * m_ent / v(ds["msl_massa_entrada_kg"])   # P-084
    n_desc = int(v(ds["msl_tanques"]))
    vol_desc = m_desc / rho_hz / (1 - ull)
    a_l = en["lander"]["variante_rhu"]["opcao"]["area_m2"]
    n_asas = int(v(la["asas_paineis"]))
    lander = {"massa_entrada_kg": m_ent, "opcoes_aeroshell": opcoes, "semiangulo_graus": v(ae["semiangulo_frente_graus"]),
              "cruzeiro": {**vol_cz, "propelente_kg": cz["propelente_kg"], "diametro_esfera_m": esfera(max(vol_cz["tanque_oxidante_m3"], vol_cz["tanque_combustivel_m3"]))},
              "descida": {"propelente_kg": m_desc, "tanques": n_desc, "volume_total_m3": vol_desc, "diametro_esfera_m": esfera(vol_desc / n_desc)},
              "paineis": {"area_m2": a_l, "asas": n_asas, "diametro_asa_m": math.sqrt(4 * a_l / (n_asas * math.pi)),
                          "phoenix_envergadura_m": v(la["phoenix"]["envergadura_paineis_m"]), "phoenix_deck_m": v(la["phoenix"]["deck_diametro_m"])},
              "helicoptero": {"diametro_rotor_m": 2 * v(la["helicoptero"]["raio_rotor_m"]), "altura_m": v(la["helicoptero"]["altura_m"])},
              "braco_m": v(la["braco_comprimento_m"])}

    # ---------------- MAV: dois estágios R-4D-11 (ADR 0011), tanques cilíndricos no diâmetro do veículo
    est_m = arq["lander"]["mav"]["estagios"]
    t_par = v(mv["espessura_parede_m"])
    nt = {k: v(x) for k, x in mv["comprimento_nao_tanque_m"].items()}
    mavs = {}
    for k, o in mv["diametro_opcoes_m"].items():
        dmav = v(o)
        di = dmav - 2 * t_par
        segs = []
        for i, e in enumerate(est_m):
            vol = volumes(e["propelente_kg"], of, rho_ox, rho_fu, ull)
            if i == 0:
                segs.append(("Motores do estágio 1 (4 × R-4D-11)", nt["motores_estagio_1"], "estrutura"))
            else:
                segs.append(("Interestágio", nt["interestagio"], "estrutura"))
                segs.append(("Motor do estágio 2 (1 × R-4D-11)", nt["motor_estagio_2"], "estrutura"))
            segs.append((f"Tanque de oxidante do estágio {i + 1}", tanque_cilindrico(vol["tanque_oxidante_m3"], di) + 2 * t_par, "oxidante"))
            segs.append((f"Tanque de combustível do estágio {i + 1}", tanque_cilindrico(vol["tanque_combustivel_m3"], di) + 2 * t_par, "combustivel"))
        segs.append(("Carga (contêiner de amostras)", nt["carga_os"], "carga"))
        comp = sum(s[1] for s in segs)
        mavs[k] = {"diametro_m": dmav, "segmentos": [{"item": a, "comprimento_m": b, "tipo": c} for a, b, c in segs], "comprimento_m": comp,
                   "dentro_do_diametro_util": {kk: comp <= oo["diametro_util_interno_m"] for kk, oo in opcoes.items()}}
    ref_mav = {"limite_src_m": v(mv["comprimento_max_src_m"]), "limite_2019_m": v(mv["comprimento_max_2019_m"]),
               "bowles_comprimento_m": v(mv["bowles_analogo"]["comprimento_m"]), "bowles_diametro_m": v(mv["bowles_analogo"]["diametro_m"]),
               "bowles_glow_kg": v(mv["bowles_analogo"]["glow_kg"]), "glom_kg": est_m[0]["massa_inicial_kg"]}

    out = {"gerado_por": "tools/envelope_arranjo.py", "orbitador": orbitador, "lander": lander, "mav": mavs, "mav_referencias": ref_mav,
           "coifas": {"falcon": {"nome": cad["coifas"]["falcon_padrao"]["nome"], "altura_m": perf_f[0], "raio_m": perf_f[1]},
                      "vulcan": {"nome": cad["coifas"]["vulcan_15_5"]["nome"], "altura_m": perf_v[0], "raio_m": perf_v[1]}}}
    out = nativo(out)
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "envelope.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)
    vistas(out)


# ------------------------------------------------------------------------------------------------- relatório
def escreve_md(o):
    br = lambda x, n=2: f"{x:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    ob, la, mv, rf = o["orbitador"], o["lander"], o["mav"], o["mav_referencias"]
    md = ["# Envelope e arranjo dos veículos (gerado por tools/envelope_arranjo.py)", "",
          "Dimensões derivadas de results/ e config/cad.yaml (fontes e premissas). Comprimentos em m, volumes em m³, massas em kg.", "",
          "## Orbitador no Falcon Heavy (coifa padrão, volume útil com mantas)", "",
          "| Estágio | Propelente | Oxidante | Combustível | Tanque de oxidante | Tanque de combustível | Pares | Ø da esfera | Ø da esfera com 1 par |",
          "| :- | -: | -: | -: | -: | -: | -: | -: | -: |"]
    for k, rot in (("insercao_marte", "Inserção em Marte"), ("retorno", "Retorno")):
        t = ob["tanques"][k]
        md.append(f"| {rot} | {br(t['propelente_kg'], 0)} | {br(t['oxidante_kg'], 0)} | {br(t['combustivel_kg'], 0)} | {br(t['tanque_oxidante_m3'], 3)} | "
                  f"{br(t['tanque_combustivel_m3'], 3)} | {t['pares']} | {br(t['diametro_esfera_m'])} | {br(t['alternativa_um_par']['diametro_esfera_m'])} |")
    md += ["", "| Conjunto | Altura da base | Altura do topo | Raio do conjunto | Folga radial ao envelope |", "| :- | -: | -: | -: | -: |"]
    for c in ob["conjuntos"]:
        md.append(f"| {c['conjunto']} | {br(c['h0_m'])} | {br(c['h1_m'])} | {br(c['raio_m'])} | {br(c['margem_radial_m'])} |")
    md += ["", f"Altura do conjunto empilhado {br(ob['altura_total_m'])} m, contra {br(ob['topo_envelope_m'])} m do topo do volume útil: "
           f"**{'cabe' if ob['cabe'] else 'não cabe'}**. Painéis do orbitador: {br(ob['area_paineis_m2'], 1)} m² (dobrados no lançamento; empacotamento na 7.2). "
           f"EES: Ø {br(ob['ees_diametro_m'], 3)} m, dentro do CCRS. A plataforma (614 kg) não tem volume dimensionado nesta etapa.", "",
           "## Lander no Vulcan de 15,5 m (estágio de cruzeiro + aeroshell)", "",
           f"Massa de entrada do lander: {br(la['massa_entrada_kg'], 0)} kg. Semiângulo da frente do aeroshell: {br(la['semiangulo_graus'], 0)}°.", "",
           "| Opção de aeroshell | Diâmetro | Massa de entrada da referência | Massa por área: lander / referência (kg/m²) | Altura do conjunto (P-083) | Folga radial no Vulcan | Diâmetro útil interno |",
           "| :- | -: | -: | -: | -: | -: | -: |"]
    nomes = {"m2020": "Mars 2020", "srl_duplo": "SRL, lançamento duplo"}
    for k, x in la["opcoes_aeroshell"].items():
        ref = ("> " if x["referencia_e_minimo"] else "") + br(x["massa_entrada_referencia_kg"], 0)
        mpa = f"{br(x['massa_por_area_lander_kg_m2'], 0)} / {'> ' if x['referencia_e_minimo'] else ''}{br(x['massa_por_area_referencia_kg_m2'], 0)}"
        md.append(f"| {nomes.get(k, k)} | {br(x['diametro_m'])} | {ref} | {mpa} | {br(x['altura_conjunto_m'])} | {br(x['margem_radial_vulcan_m'], 3)} | {br(x['diametro_util_interno_m'])} |")
    cz, de, pa, he = la["cruzeiro"], la["descida"], la["paineis"], la["helicoptero"]
    md += ["", f"- **Estágio de cruzeiro:** {br(cz['propelente_kg'], 1)} kg de MMH/MON; tanques de {br(cz['tanque_oxidante_m3'], 3)} e "
           f"{br(cz['tanque_combustivel_m3'], 3)} m³ (Ø {br(cz['diametro_esfera_m'])} m).",
           f"- **Descida (P-084):** {br(de['propelente_kg'], 0)} kg de hidrazina em {de['tanques']} esferas de Ø {br(de['diametro_esfera_m'])} m "
           f"({br(de['volume_total_m3'], 3)} m³ no total).",
           f"- **Painéis (P-088):** {br(pa['area_m2'], 1)} m² em {pa['asas']} asas circulares de Ø {br(pa['diametro_asa_m'])} m abertas "
           f"(Phoenix: envergadura de {br(pa['phoenix_envergadura_m'])} m e deck de {br(pa['phoenix_deck_m'])} m).",
           f"- **Helicópteros:** rotor de Ø {br(he['diametro_rotor_m'])} m, altura {br(he['altura_m'])} m. **Braço:** {br(la['braco_m'])} m.", "",
           "## MAV (dois estágios, R-4D-11)", "",
           "| Segmento | " + " | ".join(f"Ø {br(x['diametro_m'])} m" for x in mv.values()) + " |", "| :- |" + " -: |" * len(mv)]
    ks = list(mv)
    for i, s in enumerate(mv[ks[0]]["segmentos"]):
        md.append(f"| {s['item']} | " + " | ".join(br(mv[k]["segmentos"][i]["comprimento_m"]) for k in ks) + " |")
    md.append("| **Comprimento total** | " + " | ".join(f"**{br(mv[k]['comprimento_m'])}**" for k in ks) + " |")
    md += ["", f"Referências: limite do MAV do MSR {br(rf['limite_src_m'])} m × Ø 0,50 m [F35]; restrição de 2019 {br(rf['limite_2019_m'])} m × Ø 0,57 m [F216]; "
           f"Bowles, MAV de {br(rf['bowles_glow_kg'], 1)} kg: {br(rf['bowles_comprimento_m'])} m × Ø {br(rf['bowles_diametro_m'])} m [F46]. "
           f"GLOM do nosso MAV: {br(rf['glom_kg'], 1)} kg."]
    for k in ks:
        md.append(f"- Ø {br(mv[k]['diametro_m'])} m: cabe deitado no diâmetro útil interno do aeroshell? "
                  + "; ".join(f"{nomes.get(kk, kk)}: {'sim' if ok else 'não'}" for kk, ok in mv[k]["dentro_do_diametro_util"].items()))
    md += ["", "Vistas: orbitador_na_coifa.png, lander_na_coifa.png, lander_superficie.png, mav.png (esquemas, não desenho de projeto)."]
    (SAIDA / "envelope.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


# ------------------------------------------------------------------------------------------------- vistas 2D
def _eixo(titulo, figsize=(6, 8)):
    fig, ax = plt.subplots(figsize=figsize, facecolor=SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    ax.set_aspect("equal")
    ax.grid(color=GRADE, lw=0.6)
    ax.set_title(titulo, color=TINTA, fontsize=10)
    ax.tick_params(colors=TINTA_2, labelsize=8)
    for s in ax.spines.values():
        s.set_color(GRADE)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"{x:g}".replace(".", ",").replace("-", "−")))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"{x:g}".replace(".", ",").replace("-", "−")))
    return fig, ax


def _envelope(ax, c, rotulo):
    h, r = np.array(c["altura_m"]), np.array(c["raio_m"])
    ax.plot(r, h, color=TINTA_2, lw=1.2, label=rotulo)
    ax.plot(-r, h, color=TINTA_2, lw=1.2)
    ax.plot([-r[0], r[0]], [0, 0], color=TINTA_2, lw=0.8, ls=":")


def vistas(o):
    ob, la, mv = o["orbitador"], o["lander"], o["mav"]
    # orbitador na coifa do Falcon (corte lateral)
    fig, ax = _eixo("Orbitador no volume útil da coifa do Falcon (esquema)")
    _envelope(ax, o["coifas"]["falcon"], "volume útil (STEP do fabricante)")
    rc = (ob["conjuntos"][0]["raio_m"] - ob["tanques"]["insercao_marte"]["diametro_esfera_m"]) - 0.05
    for c, k in zip(ob["conjuntos"][:2], ("insercao_marte", "retorno")):
        d = ob["tanques"][k]["diametro_esfera_m"]
        for s, cor in ((-1, COR["oxidante"]), (1, COR["combustivel"])):
            ax.add_patch(Circle((s * (c["raio_m"] - d / 2), c["h0_m"] + d / 2), d / 2, fc=cor, ec=TINTA, lw=0.6, alpha=0.85))
    ax.add_patch(Rectangle((-rc, 0), 2 * rc, ob["conjuntos"][1]["h1_m"], fc="none", ec=COR["estrutura"], lw=1, ls="--"))
    cc = ob["conjuntos"][2]
    ax.add_patch(Rectangle((-ob["ccrs_m"][0] / 2, cc["h0_m"]), ob["ccrs_m"][0], cc["h1_m"] - cc["h0_m"], fc=COR["carga"], ec=TINTA, lw=0.6, alpha=0.6))
    ax.text(0, (cc["h0_m"] + cc["h1_m"]) / 2, "CCRS", ha="center", va="center", color=SUPERFICIE, fontsize=8)
    ax.text(0, -0.5, "plano do PAF de 1575 mm", ha="center", color=TINTA_2, fontsize=7)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-1, 12)
    ax.set_xlabel("m")
    ax.set_ylabel("altura acima do PAF (m)")
    ax.legend(loc="upper right", fontsize=7, frameon=False)
    fig.savefig(SAIDA / "orbitador_na_coifa.png", dpi=120, facecolor=SUPERFICIE)
    plt.close(fig)

    # lander na coifa do Vulcan (corte lateral), as duas opções de aeroshell
    fig, ax = _eixo("Lander (cruzeiro + aeroshell) no envelope do Vulcan de 15,5 m (esquema)")
    _envelope(ax, o["coifas"]["vulcan"], "envelope estático do Vulcan")
    estilos = {"m2020": ("--", COR["combustivel"]), "srl_duplo": ("-", COR["oxidante"])}
    for k, x in la["opcoes_aeroshell"].items():
        ls, cor = estilos.get(k, ("-", TINTA))
        r, hh = x["diametro_m"] / 2, x["altura_conjunto_m"]
        ax.add_patch(Rectangle((-r, 0), 2 * r, hh, fc="none", ec=cor, lw=1.2, ls=ls, label=f"Ø {x['diametro_m']:g} m".replace(".", ",")))
        # frente do aeroshell (semiângulo da frente) apontada para cima, no topo do conjunto
        alt_cone = r / math.tan(math.radians(la["semiangulo_graus"]))
        ax.add_patch(Polygon([(-r, hh - alt_cone), (0, hh), (r, hh - alt_cone)], closed=False, fill=False, ec=cor, lw=0.8, ls=ls))
    ax.set_xlim(-3, 3)
    ax.set_ylim(-1, 14)
    ax.set_xlabel("m")
    ax.set_ylabel("altura acima do PAF (m)")
    ax.legend(loc="upper right", fontsize=7, frameon=False)
    fig.savefig(SAIDA / "lander_na_coifa.png", dpi=120, facecolor=SUPERFICIE)
    plt.close(fig)

    # lander na superfície (vista de cima): diâmetro útil interno, asas abertas, MAV deitado, helicópteros e braço
    fig, ax = _eixo("Lander na superfície, vista de cima (esquema)", figsize=(9, 6))
    op = la["opcoes_aeroshell"]["srl_duplo"]
    ru = op["diametro_util_interno_m"] / 2
    rot_ae = f"diâmetro útil interno (Ø {op['diametro_util_interno_m']:.2f} m) do aeroshell de Ø {op['diametro_m']:.2f} m".replace(".", ",")
    ax.add_patch(Circle((0, 0), ru, fc="none", ec=COR["estrutura"], lw=1, ls="--", label=rot_ae))
    da = la["paineis"]["diametro_asa_m"]
    for s in (-1, 1):
        ax.add_patch(Circle((s * (ru + da / 2), 0), da / 2, fc="#f2c94c", ec=TINTA, lw=0.6, alpha=0.7))
    ax.text(ru + da / 2, 0, "asa de painel", ha="center", va="center", fontsize=7, color=TINTA)
    m = mv[list(mv)[-1]]
    ax.add_patch(Rectangle((-m["comprimento_m"] / 2, -m["diametro_m"] / 2), m["comprimento_m"], m["diametro_m"], fc=COR["carga"], ec=TINTA, lw=0.6, alpha=0.7))
    ax.text(0, 0, f"MAV deitado (Ø {m['diametro_m']:.2f} m)".replace(".", ","), ha="center", va="center", color=SUPERFICIE, fontsize=7)
    dr = la["helicoptero"]["diametro_rotor_m"]
    for s in (-1, 1):
        ax.add_patch(Circle((s * 0.9, -ru + dr / 2 + 0.1), dr / 2, fc="none", ec=COR["hidrazina"], lw=1))
    ax.text(0, -ru + dr / 2 + 0.1, "helicópteros", ha="center", va="center", fontsize=7, color=TINTA_2)
    ax.plot([0.6, 0.6 + la["braco_m"]], [ru * 0.6, ru * 0.6 + 0.4], color=TINTA, lw=2)
    ax.text(0.6, ru * 0.6 + 0.15, "braço", fontsize=7, color=TINTA)
    lim = ru + da + 0.3
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-3.2, 3.2)
    ax.set_xlabel("m")
    ax.legend(loc="upper left", fontsize=7, frameon=False)
    fig.savefig(SAIDA / "lander_superficie.png", dpi=120, facecolor=SUPERFICIE)
    plt.close(fig)

    # MAV: segmentos empilhados, uma coluna por opção de diâmetro
    fig, ax = _eixo("MAV: segmentos de baixo para cima (esquema)", figsize=(6, 8))
    for j, (k, x) in enumerate(mv.items()):
        x0, hh = j * 1.6, 0.0
        for s in x["segmentos"]:
            ax.add_patch(Rectangle((x0 - x["diametro_m"] / 2, hh), x["diametro_m"], s["comprimento_m"], fc=COR[s["tipo"]], ec=TINTA, lw=0.5, alpha=0.8))
            hh += s["comprimento_m"]
        ax.text(x0, -0.25, f"Ø {x['diametro_m']:g} m".replace(".", ","), ha="center", fontsize=8, color=TINTA)
        ax.text(x0, hh + 0.08, f"{hh:.2f} m".replace(".", ","), ha="center", fontsize=8, color=TINTA)
    lim_src = o["mav_referencias"]["limite_src_m"]
    ax.axhline(lim_src, color=TINTA_2, lw=0.8, ls=":")
    ax.text(1.6 * len(mv) - 1.05, lim_src + 0.05, "limite do MAV do MSR [F35]", fontsize=7, color=TINTA_2, ha="right")
    for nome, cor in (("oxidante", COR["oxidante"]), ("combustível", COR["combustivel"]), ("motores e estrutura", COR["estrutura"]), ("carga", COR["carga"])):
        ax.plot([], [], lw=6, color=cor, label=nome)
    ax.set_xlim(-1, 1.6 * len(mv))
    ax.set_ylim(-0.5, max(x["comprimento_m"] for x in mv.values()) + 0.6)
    ax.set_ylabel("m")
    ax.set_xticks([])
    ax.legend(loc="upper right", fontsize=7, frameon=False)
    fig.savefig(SAIDA / "mav.png", dpi=120, facecolor=SUPERFICIE)
    plt.close(fig)


if __name__ == "__main__":
    main()
