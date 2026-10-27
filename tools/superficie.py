"""Etapa 2.1: arquiteturas de superfície (pouso, subida e encontro), Δv por trecho e dimensionamento.

Entradas: config/superficie.yaml, config/dimensionamento.yaml, config/parametros_orbitais.yaml,
config/premissas.yaml e results/etapa1.3/missoes.yaml.
Saída: results/etapa2.1/arquiteturas.yaml e results/etapa2.1/arquiteturas.md

Uso: python tools/superficie.py
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(RAIZ / "src"), str(RAIZ / "tools")]

import dimensionamento as dm  # noqa: E402
from orbital import foguete as fg  # noqa: E402
from orbital import manobras as mn  # noqa: E402
from orbital import superficie as sf  # noqa: E402
from orbital.config import ler, v  # noqa: E402
from orbital.veiculos import lander_estagios  # noqa: E402

SAIDA = RAIZ / "results" / "etapa2.1"


_ler, _v = ler, v


def mav(dv_total, cfg):
    """MAV sólido de dois estágios (P-019). Devolve (GLOM, resultados por estágio)."""
    m = cfg["mav"]
    f1 = _v(m["fracao_dv_estagio_1"])
    eps = _v(m["fracao_estrutural"])
    e1 = fg.Estagio("mav_1", m["isp_s"]["estagio_1"], eps, [fg.Queima("subida_1", f1 * dv_total)])
    e2 = fg.Estagio("mav_2", m["isp_s"]["estagio_2"], eps, [fg.Queima("subida_2", (1 - f1) * dv_total)])
    r = fg.dimensionar_veiculo([e1, e2], _v(m["carga_util_kg"]))
    return r[0].massa_inicial, r


def lander_leo(chegada, cfg, dcfg, p, caso_saida):
    """Massa na órbita baixa do lander: chegada a Marte + estágio de cruzeiro + estágio de saída da Terra."""
    return lander_estagios(chegada, cfg, dcfg, p, caso_saida)[0].massa_inicial


def main():
    cfg = _ler("config/superficie.yaml")
    dcfg = _ler("config/dimensionamento.yaml")
    po = _ler("config/parametros_orbitais.yaml")
    ms = _ler("results/etapa1.3/missoes.yaml")
    p = dm.parametros()
    mu, R = p.mu_marte, _v(po["raio_marte_km"])
    margem = _v(dcfg["margem_dv"])
    perdas = dcfg["dv"]["perda_gravitacional"]
    r_ei = _v(cfg["marte"]["raio_interface_entrada_km"])
    v_eq = 2 * np.pi * R / _v(cfg["marte"]["periodo_rotacao_s"])
    lat = _v(cfg["sitio_e_encontro"]["latitude_sitio_graus"])
    inc = _v(cfg["sitio_e_encontro"]["inclinacao_encontro_graus"])
    r_baixa = R + _v(cfg["sitio_e_encontro"]["orbita_baixa_alt_km"])
    um_sol = p.orbitas_marte["eliptica_alta"]
    g_marte = mu / R**2
    dv100 = _v(cfg["subida"]["dv_100x100_km_s"])

    cand = {c["id"]: c for c in ms["candidatas"]}
    ref_id = _ler("config/missao_referencia.yaml")["missao_referencia"]["id"]
    a = cand[ref_id]
    janelas = [cand[v["missao"]] for v in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()]

    # Orbitador: descer de 1 sol para a órbita baixa de encontro e o custo extra da injeção trans-Terra
    def extra_orbitador(c3l, por="propulsao"):
        vinf = np.sqrt(c3l)
        if por == "aerofrenagem":
            descer = _v(cfg["aerofrenagem"]["dv_saida_aerofrenagem_km_s"])
        else:
            descer = mn.dv_transferencia_coaxial(mu, um_sol.rp, um_sol.ra, r_baixa, r_baixa)
        tei_1sol = float(mn.dv_hiperbole_orbita(mu, vinf, um_sol.rp, um_sol.ra))
        tei_baixa = float(mn.dv_hiperbole_orbita(mu, vinf, r_baixa))
        subir_e_tei = mn.dv_transferencia_coaxial(mu, r_baixa, r_baixa, um_sol.rp, um_sol.ra) + tei_1sol
        volta = min(tei_baixa, subir_e_tei)
        return descer, volta - tei_1sol, "direto da órbita baixa" if tei_baixa <= subir_e_tei else "subir para 1 sol e partir"

    # Descida propulsiva (só orçamento de Δv)
    dsc = cfg["descida"]
    dv_desc = sf.dv_descida_vertical(_v(dsc["velocidade_inicio_kms"]), g_marte, _v(dsc["tempo_queima_s"]))

    lcfg = cfg["lander"]
    plat = _v(lcfg["plataforma_superficie_kg"])
    out = {"gerado_por": "tools/superficie.py", "margem_dv": margem, "arquiteturas": {}}
    md = ["# Arquiteturas de superfície (gerado por tools/superficie.py)", "",
          f"Δv em km/s, massas em kg. Margem de {margem:.0%} (P-014) nos trechos propulsivos. Missão A ({ref_id}); "
          "\"envelope\" = pior caso entre os mínimos por janela (ADR 0004).", ""]
    for nome, arq in cfg["arquiteturas"].items():
        alvo = (r_baixa, r_baixa) if arq["encontro"] == "orbita_baixa" else (um_sol.rp, um_sol.ra)
        dv_mav = sf.dv_subida(mu, R, dv100, alvo[0], alvo[1], v_eq, inc, lat)
        glom, rmav = mav((1 + margem) * dv_mav, cfg)
        pousada = glom + plat
        trechos = {"subida_MAV": dv_mav, "descida_propulsiva (só orçamento)": dv_desc}
        linha = {"nome": arq["nome"]}
        for rotulo, c in (("missao_A", a), ("envelope", None)):
            if c is None:
                vinf_m = max(x["vinf_chegada_marte_km_s"] for x in janelas)
                c3l = max(x["c3l_partida_marte_km2_s2"] for x in janelas)
            else:
                vinf_m, c3l = c["vinf_chegada_marte_km_s"], c["c3l_partida_marte_km2_s2"]
            reg = {"vinf_chegada_marte_km_s": round(vinf_m, 4)}
            if arq["entrada"] == "direta":
                v_ent = float(mn.v_hiperbole(mu, vinf_m, r_ei))
                entrada = pousada / _v(lcfg["razao_pousada_entrada"]["entrada_direta"])
                chegada = entrada
                reg.update({"v_entrada_km_s": round(v_ent, 4)})
            else:
                cap = float(mn.dv_hiperbole_orbita(mu, vinf_m, um_sol.rp, um_sol.ra)) + _v(perdas["captura_marte"])
                deorb = mn.dv_saida_de_orbita(mu, um_sol.ra, um_sol.rp, r_ei)
                v_ent = mn.v_entrada_de_orbita(mu, um_sol.ra, r_ei)
                entrada = pousada / _v(lcfg["razao_pousada_entrada"]["a_partir_de_orbita"])
                po_ = lcfg["propulsao_orbital"]
                est = fg.Estagio("lander_orbital", _v(po_["isp_s"]), _v(po_["fracao_estrutural"]),
                                 [fg.Queima("captura_lander", (1 + margem) * cap), fg.Queima("saida_de_orbita", (1 + margem) * deorb)])
                r = fg.dimensionar_estagio(est, entrada)
                chegada = r.massa_inicial
                reg.update({"dv_captura_lander_km_s": round(cap, 4), "dv_saida_de_orbita_km_s": round(deorb, 4),
                            "v_entrada_km_s": round(v_ent, 4), "propelente_lander_orbital_kg": round(r.propelente, 1)})
            if arq["encontro"] == "orbita_baixa":
                descer, extra_tei, modo = extra_orbitador(c3l, arq.get("orbitador_desce_por", "propulsao"))
                reg.update({"dv_orbitador_descer_ate_encontro_km_s": round(descer, 4),
                            "dv_orbitador_extra_saida_marte_km_s": round(extra_tei, 4), "modo_saida": modo})
                extra = descer + extra_tei
            else:
                extra = 0.0
            reg.update({"massa_entrada_kg": round(entrada, 1), "massa_lander_na_chegada_kg": round(chegada, 1),
                        "dv_orbitador_extra_total_km_s": round(extra, 4)})
            linha[rotulo] = reg
        # Efeito no orbitador: Δv extra (pior entre janelas) somado ao encontro, regra de projeto (iii)
        extra_env = linha["envelope"]["dv_orbitador_extra_total_km_s"]
        extra_A = linha["missao_A"]["dv_orbitador_extra_total_km_s"]
        cu = _ler("config/carga_util.yaml")
        a_, jan, piores = dm.casos(dcfg, p)
        vs = dm.variantes(a_, jan, piores)
        base = dcfg["caso_base"]

        def leo(extra_dv, var):
            c2 = copy.deepcopy(dcfg)
            c2["dv"]["encontro_orbita_marte"]["valor"] = _v(dcfg["dv"]["encontro_orbita_marte"]) + extra_dv
            return dm.massa_leo(vs[var], c2, cu, base["carga_util"], margem, float(base["acrescimo_capsula"]))[0]

        linha.update({
            "mav_glom_kg": round(glom, 1), "mav_estagios": [{"nome": s.nome, "propelente_kg": round(s.propelente, 1),
                                                             "inerte_kg": round(s.inerte, 1)} for s in rmav],
            "massa_pousada_kg": round(pousada, 1),
            "dv_trechos_km_s": {k: round(v, 4) for k, v in trechos.items()},
            "orbitador_massa_orbita_baixa_kg": {"missao_A": round(leo(extra_A, "missao_A"), 1),
                                                "regra_iii": round(leo(extra_env, dcfg["regra_projeto"]), 1)},
        })
        a_caso, _, _ = dm.casos(dcfg, p)
        lander_A = lander_leo(linha["missao_A"]["massa_lander_na_chegada_kg"], cfg, dcfg, p, a_caso)
        lander_iii = lander_leo(linha["envelope"]["massa_lander_na_chegada_kg"], cfg, dcfg, p, a_caso)
        orb = linha["orbitador_massa_orbita_baixa_kg"]
        linha["lander_massa_orbita_baixa_kg"] = {"missao_A": round(lander_A, 1), "regra_iii": round(lander_iii, 1)}
        linha["total_orbita_baixa_kg"] = {"missao_A": round(orb["missao_A"] + lander_A, 1),
                                          "regra_iii": round(orb["regra_iii"] + lander_iii, 1)}
        out["arquiteturas"][nome] = linha

    # Tabela-resumo
    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    cols = list(out["arquiteturas"])
    md += ["| | " + " | ".join(f"**{k}**: {out['arquiteturas'][k]['nome']}" for k in cols) + " |", "| :- |" + " :- |" * len(cols)]

    def row(rot, f):
        md.append(f"| {rot} | " + " | ".join(f(out["arquiteturas"][k]) for k in cols) + " |")

    row("Δv de subida do MAV (com perdas, sem margem)", lambda x: br(x["dv_trechos_km_s"]["subida_MAV"], 3))
    row("Δv da descida propulsiva (vertical, conservador; só orçamento)", lambda x: br(x["dv_trechos_km_s"]["descida_propulsiva (só orçamento)"], 3))
    row("Δv captura do lander em 1 sol / saída de órbita (missão A)",
        lambda x: (br(x["missao_A"]["dv_captura_lander_km_s"], 3) + " / " + br(x["missao_A"]["dv_saida_de_orbita_km_s"], 3))
        if "dv_captura_lander_km_s" in x["missao_A"] else "—")
    row("Velocidade de entrada (missão A / envelope)", lambda x: br(x["missao_A"]["v_entrada_km_s"], 2) + " / " + br(x["envelope"]["v_entrada_km_s"], 2))
    row("Δv extra do orbitador: descer até o encontro + saída de Marte (missão A / envelope)",
        lambda x: br(x["missao_A"]["dv_orbitador_extra_total_km_s"], 3) + " / " + br(x["envelope"]["dv_orbitador_extra_total_km_s"], 3))
    row("MAV: massa na decolagem", lambda x: br(x["mav_glom_kg"]))
    row("Massa pousada (MAV + plataforma P-017)", lambda x: br(x["massa_pousada_kg"]))
    row("Massa de entrada (missão A)", lambda x: br(x["missao_A"]["massa_entrada_kg"]))
    row("Lander na chegada a Marte (missão A / envelope)", lambda x: br(x["missao_A"]["massa_lander_na_chegada_kg"]) + " / " + br(x["envelope"]["massa_lander_na_chegada_kg"]))
    row("Orbitador na órbita baixa da Terra: missão A / regra (iii)",
        lambda x: br(x["orbitador_massa_orbita_baixa_kg"]["missao_A"]) + " / " + br(x["orbitador_massa_orbita_baixa_kg"]["regra_iii"]))
    row("Lander na órbita baixa da Terra (com cruzeiro e saída da Terra): missão A / regra (iii)",
        lambda x: br(x["lander_massa_orbita_baixa_kg"]["missao_A"]) + " / " + br(x["lander_massa_orbita_baixa_kg"]["regra_iii"]))
    row("**TOTAL na órbita baixa (lançamentos separados): missão A / regra (iii)**",
        lambda x: "**" + br(x["total_orbita_baixa_kg"]["missao_A"]) + " / " + br(x["total_orbita_baixa_kg"]["regra_iii"]) + "**")
    md += ["", "Referência sem superfície (Fase 1): orbitador de 13 587 kg (missão A) e 22 833 kg (regra iii) na órbita baixa.",
           f"S4: a aerofrenagem leva ~{_v(cfg['aerofrenagem']['duracao_dias']):.0f} dias (P-020), dentro da estada em Marte."]
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "arquiteturas.yaml").write_text(yaml.safe_dump(dm._nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")
    (SAIDA / "arquiteturas.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
