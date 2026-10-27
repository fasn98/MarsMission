"""Etapa 2.2b: propulsão do MAV — sólido (O1), LOX/CH4 da Terra (O2) e hipergólico armazenável (O4).

Comparação pela massa total na órbita baixa da Terra (regra iii e missão A) na órbita de encontro do
ADR 0005, com armazenamento criogênico no cruzeiro e na superfície para o LOX/CH4, e critérios
operacionais do MSR ao lado. Depois, refaz a varredura da órbita de encontro com a opção de menor massa
e aplica a regra dos 5 % do ADR 0005.
Saída: results/etapa2.2/mav_propulsao.yaml e .md; results/etapa2.1/varredura_encontro_rp300_<opção>.*

Uso: python tools/mav_propulsao.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(RAIZ / "src"), str(RAIZ / "tools")]

import dimensionamento as dm  # noqa: E402
import varredura_encontro as ve  # noqa: E402
from isru import energia, zbo  # noqa: E402
from orbital import foguete as fg  # noqa: E402
from orbital import isru  # noqa: E402
from superficie import _ler, _v, lander_leo  # noqa: E402

SAIDA = RAIZ / "results" / "etapa2.2"


def mav_generico(dv, op, scfg):
    f1 = _v(scfg["mav"]["fracao_dv_estagio_1"])
    eps = _v(op["fracao_estrutural"])
    e1 = fg.Estagio("mav_1", op["isp_s"][0], eps, [fg.Queima("subida_1", f1 * dv)])
    e2 = fg.Estagio("mav_2", op["isp_s"][1], eps, [fg.Queima("subida_2", (1 - f1) * dv)])
    r = fg.dimensionar_veiculo([e1, e2], _v(scfg["mav"]["carga_util_kg"]))
    prop = sum(s.propelente for s in r)
    return r[0].massa_inicial, prop


def massas_opcao(dv, nome, mcfg, scfg, icfg, fonte_energia):
    """(massa pousada do MAV + equipamentos de armazenamento e energia, massa extra no cruzeiro, detalhe)."""
    op = mcfg["opcoes"][nome]
    glom, prop = mav_generico(dv, op, scfg)
    det = {"mav_glom_kg": glom, "mav_propelente_kg": prop}
    if not op["criogenico"]:
        return glom, 0.0, det
    m_ox, m_ch4 = isru.divisao_of(prop, _v(op["razao_of"]))
    # Superfície: armazenamento sem evaporação + fonte de energia (como na Etapa 2.2)
    p_sup, m_sup = zbo(icfg, m_ch4, m_ox)
    m_en, desc = energia(icfg, p_sup, fonte_energia)
    # Cruzeiro: armazenamento sem evaporação (P-026) alimentado por painéis no cruzeiro (descartados antes da entrada)
    cz = mcfg["cruzeiro"]
    z = cz["zbo_transito"]
    p_cz = sum(isru.escala(z["potencia_w"], m, z["referencia_kg"], z["expoente"]) for m in (m_ch4, m_ox))
    m_cz_hw = sum(isru.escala(z["massa_ativa_kg"] + z["massa_passiva_kg"], m, z["referencia_kg"], z["expoente"]) for m in (m_ch4, m_ox))
    w_kg_marte = _v(cz["solar_w_kg_1ua"]) / _v(cz["distancia_marte_ua"]) ** 2
    m_paineis = p_cz / w_kg_marte
    # O hardware de cruzeiro e o de superfície servem aos mesmos tanques: conta-se o maior dos dois.
    m_hw = max(m_sup, m_cz_hw)
    det.update({"o2_kg": m_ox, "ch4_kg": m_ch4, "zbo_superficie_w": p_sup, "zbo_superficie_kg": m_sup,
                "energia_superficie_kg": m_en, "energia_superficie": desc, "zbo_cruzeiro_w": p_cz,
                "zbo_cruzeiro_kg": m_cz_hw, "paineis_cruzeiro_kg": m_paineis, "armazenamento_pousado_kg": m_hw})
    return glom + m_hw + m_en, m_paineis, det


def main():
    scfg, icfg, mcfg = _ler("config/superficie.yaml"), _ler("config/isru.yaml"), _ler("config/mav_propulsao.yaml")
    dcfg = _ler("config/dimensionamento.yaml")
    p = dm.parametros()
    a_caso, _, _ = dm.casos(dcfg, p)
    vz = _ler("results/etapa2.1/varredura_encontro_rp300.yaml")
    esc = vz["escolha"]
    ponto = next(x for x in vz["pontos"] if x["apoapse_alt_km"] == esc["apoapse_alt_km"])
    orbit = {"regra_iii": ponto["quimico"]["orbitador_regra_iii_kg"], "missao_A": ponto["quimico"]["orbitador_missao_A_kg"]}
    dv = (1 + _v(dcfg["margem_dv"])) * ponto["dv_mav_km_s"]
    plat = _v(scfg["lander"]["plataforma_superficie_kg"])
    razao = _v(scfg["lander"]["razao_pousada_entrada"]["entrada_direta"])

    linhas = []
    for nome in ("O1", "O4", "O2"):
        fontes = ("mmrtg", "solar") if mcfg["opcoes"][nome]["criogenico"] else ("-",)
        for f in fontes:
            pousado, cruz, det = massas_opcao(dv, nome, mcfg, scfg, icfg, f)
            lander = lander_leo((pousado + plat) / razao + cruz, scfg, dcfg, p, a_caso)
            linhas.append({"opcao": nome, "nome": mcfg["opcoes"][nome]["nome"], "energia": f, **det,
                           "massa_pousada_kg": pousado + plat, "lander_orbita_baixa_kg": lander,
                           "total_regra_iii_kg": orbit["regra_iii"] + lander, "total_missao_A_kg": orbit["missao_A"] + lander})
    melhor = min(linhas, key=lambda x: x["total_regra_iii_kg"])

    # Varredura da órbita de encontro com a opção de menor massa (mesma regra dos 5 %)
    vr = scfg["varreduras_encontro"]["rp300"]
    po = _ler("config/parametros_orbitais.yaml")
    R = _v(po["raio_marte_km"])
    ms = _ler("results/etapa1.3/missoes.yaml")
    cand = {c["id"]: c for c in ms["candidatas"]}
    ref = _ler("config/missao_referencia.yaml")["missao_referencia"]["id"]
    janelas = [cand[v["missao"]] for v in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()]
    import numpy as np
    vs = dm.variantes(a_caso, *dm.casos(dcfg, p)[1:])
    ctx = (2 * np.pi * R / _v(scfg["marte"]["periodo_rotacao_s"]), _v(scfg["sitio_e_encontro"]["latitude_sitio_graus"]),
           _v(scfg["sitio_e_encontro"]["inclinacao_encontro_graus"]), _v(scfg["subida"]["dv_100x100_km_s"]), plat, razao,
           _v(scfg["aerofrenagem"]["dv_saida_aerofrenagem_km_s"]), vs, a_caso,
           {"missao_A": cand[ref]["c3l_partida_marte_km2_s2"], "regra_iii": max(x["c3l_partida_marte_km2_s2"] for x in janelas)})
    fonte_m = melhor["energia"]
    ve.varrer("rp300", vr, scfg, dcfg, _ler("config/carga_util.yaml"), p, R, ctx,
              mav_massas=lambda d: massas_opcao(d, melhor["opcao"], mcfg, scfg, icfg, fonte_m)[:2], sufixo=f"_{melhor['opcao']}")
    nova = _ler(f"results/etapa2.1/varredura_encontro_rp300_{melhor['opcao']}.yaml")["escolha"]

    out = {"gerado_por": "tools/mav_propulsao.py", "orbita_encontro_apoapse_km": esc["apoapse_alt_km"], "dv_mav_com_margem_km_s": dv,
           "orbitador_kg": orbit, "opcoes": linhas, "melhor_opcao": melhor["opcao"],
           "varredura_com_melhor_opcao": {"apoapse_escolhido_km": nova["apoapse_alt_km"], "apoapse_anterior_km": esc["apoapse_alt_km"],
                                          "total_regra_iii_kg": nova["massa_regra_iii_kg"], "total_missao_A_kg": nova["massa_missao_A_kg"],
                                          "mav_kg": nova["mav_glom_kg"], "minimo_regra_iii_kg": nova["minimo_kg"]}}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "mav_propulsao.yaml").write_text(yaml.safe_dump(dm._nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")
    br = lambda x, n=0: "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    md = ["# Propulsão do MAV (gerado por tools/mav_propulsao.py)", "",
          f"Órbita de encontro 300 × {br(esc['apoapse_alt_km'])} km (ADR 0005); Δv com margem {br(dv, 3)} km/s; carga útil 16 kg; "
          f"orbitador {br(orbit['regra_iii'])} kg (iii) / {br(orbit['missao_A'])} kg (A). Massas em kg.", "",
          "| Opção | Energia (superfície) | MAV | Armazenamento pousado | Energia pousada | Painéis no cruzeiro | Massa pousada | Lander na órbita baixa | **Total (iii)** | Total (A) |",
          "| :- | :- | -: | -: | -: | -: | -: | -: | -: | -: |"]
    for r in linhas:
        md.append(f"| {r['opcao']}: {r['nome']} | {r.get('energia_superficie') or r['energia']} | {br(r['mav_glom_kg'])} | "
                  f"{br(r.get('armazenamento_pousado_kg'))} | {br(r.get('energia_superficie_kg'))} | {br(r.get('paineis_cruzeiro_kg'))} | "
                  f"{br(r['massa_pousada_kg'])} | {br(r['lander_orbita_baixa_kg'])} | **{br(r['total_regra_iii_kg'])}** | {br(r['total_missao_A_kg'])} |")
    v = out["varredura_com_melhor_opcao"]
    md += ["", f"**Varredura da órbita de encontro com {melhor['opcao']}** (periapse 300 km, regra dos 5 % do ADR 0005): "
           f"apoapse escolhido {br(v['apoapse_escolhido_km'])} km (antes, com o MAV sólido: {br(v['apoapse_anterior_km'])} km); "
           f"total {br(v['total_regra_iii_kg'])} kg (iii) / {br(v['total_missao_A_kg'])} kg (A); mínimo pela regra (iii) {br(v['minimo_regra_iii_kg'])} kg; MAV {br(v['mav_kg'])} kg."]
    (SAIDA / "mav_propulsao.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
