"""Etapa 3.1: motores reais e queima finita.

Para cada combinação de motores proposta em config/motores.yaml:
  - captura em Marte e injeção trans-Terra: tempo de queima e perda de queima finita por integração numérica
    (orbital.queima_finita), comparadas com as perdas do DRA usadas hoje (P-015, config/dimensionamento.yaml);
  - correções do cruzeiro do lander e os dois estágios do MAV: tempo de queima pela equação do foguete, e empuxo/peso
    do MAV na decolagem em Marte. A perda de subida do MAV já está no Δv da Etapa 2.1 (Bowles et al. 2013) e não é
    recalculada aqui.
Massas no início de cada queima: o dimensionamento atual (orbital.veiculos, regra iii, órbita de encontro da Etapa
2.3). Os Δv são os do caso de projeto (pior janela do envelope, ADR 0004) e os da missão de referência (2028).
O Isp de cada combinação é o do motor; o dimensionamento NÃO é refeito com ele (isso fica para depois do portão).
Saída: results/etapa3.1/queima_finita.yaml e queima_finita.md

Uso: python tools/queima_finita.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital import manobras as mn  # noqa: E402
from orbital import motores as mt  # noqa: E402
from orbital import queima_finita as qf  # noqa: E402
from orbital import veiculos as ve  # noqa: E402
from orbital.config import ler, nativo, parametros, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa3.1"


def _queima(estagios, estagio, queima):
    e = next(x for x in estagios if x["nome"] == estagio)
    return next(q for q in e["queimas"] if q["nome"] == queima)


def casos():
    """Missões de cálculo: pior janela do envelope por trecho (como no dimensionamento, regra iii) e a de referência."""
    ms = ler("results/etapa1.3/missoes.yaml")
    ref = ler("config/missao_referencia.yaml")["missao_referencia"]
    orb = ref["orbita_marte"]
    cand = {c["id"]: c for c in ms["candidatas"]}
    jan = [cand[w["missao"]] for w in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()]
    pior_cap = max(jan, key=lambda c: c["por_orbita_marte"][orb]["dv_captura_propulsiva_km_s"])
    pior_sai = max(jan, key=lambda c: c["por_orbita_marte"][orb]["dv_saida_marte_km_s"])
    a = cand[ref["id"]]
    return {"captura": [("projeto (pior janela)", pior_cap), ("referência", a)],
            "saida": [("projeto (pior janela)", pior_sai), ("referência", a)]}


def main():
    p = parametros()
    po, dcfg = ler("config/parametros_orbitais.yaml"), ler("config/dimensionamento.yaml")
    mu, R = p.mu_marte, v(po["raio_marte_km"])
    g_marte = mu / R ** 2 * 1e3   # m/s², Marte como massa pontual (o mesmo μ e raio do estudo)
    um = p.orbitas_marte["eliptica_alta"]
    pl = ler("results/etapa2.3/plataformas.yaml")["orbita_encontro"]
    rp_enc, ra_enc = R + pl["periapse_alt_km"], R + pl["apoapse_regra_5pct_km"]
    perda_p015 = {k: v(x) for k, x in dcfg["dv"]["perda_gravitacional"].items()}
    vei, _, _ = ve.veiculos(detalhe=True)
    orb, lan = vei["orbitador_regra_iii"], vei["lander"]
    cs = casos()
    out = {"gerado_por": "tools/queima_finita.py",
           "modelo": "plano, dois corpos (Marte pontual), empuxo constante tangente à velocidade, vazão T/(Isp g0)",
           "p015_km_s": {"captura_marte": perda_p015["captura_marte"], "saida_marte": perda_p015["saida_marte"]},
           "captura": [], "saida": [], "cruzeiro": [], "mav": []}

    # Captura: hipérbole de v∞ → órbita de 1 sol (ADR 0003)
    q_cap = _queima(orb["estagios"], "insercao_marte", "captura_marte")
    m0, prop_dim = q_cap["massa_antes_kg"], q_cap["propelente_kg"]
    for c in mt.conjuntos("captura"):
        for rotulo, mis in cs["captura"]:
            vinf = mis["vinf_chegada_marte_km_s"]
            r = qf.captura(mu, R, c.motor, m0, vinf, um.rp, um.ra)
            out["captura"].append({"combinacao": c.nome, "motores": c.descricao, "empuxo_n": c.motor.empuxo_n, "isp_s": c.motor.isp_s,
                                   "massa_motores_kg": c.massa_kg, "caso": rotulo, "missao": mis["id"], "vinf_km_s": vinf, "m0_kg": m0,
                                   **_res(r), "propelente_dimensionado_kg": prop_dim, "cabe_no_dimensionado": bool(r.propelente_kg <= prop_dim),
                                   "queima_unica_max_s": c.queima_unica_max_s,
                                   "excede_queima_unica": bool(r.duracao_s > c.queima_unica_max_s), "nota": c.nota})

    # Saída de Marte: da órbita de encontro (ou da de 1 sol, se for mais barato: orbital.veiculos.dv_extra_orbitador)
    q_sai = _queima(orb["estagios"], "retorno", "saida_marte")
    m0, prop_dim = q_sai["massa_antes_kg"], q_sai["propelente_kg"]
    for c in mt.conjuntos("retorno"):
        for rotulo, mis in cs["saida"]:
            vinf = math.sqrt(mis["c3l_partida_marte_km2_s2"])
            tei_enc = float(mn.dv_hiperbole_orbita(mu, vinf, rp_enc, ra_enc))
            voltar = mn.dv_transferencia_coaxial(mu, rp_enc, ra_enc, um.rp, um.ra) + float(mn.dv_hiperbole_orbita(mu, vinf, um.rp, um.ra))
            rp, ra, de = (rp_enc, ra_enc, "órbita de encontro") if tei_enc <= voltar else (um.rp, um.ra, "órbita de 1 sol")
            r = qf.saida(mu, R, c.motor, m0, rp, ra, vinf)
            out["saida"].append({"combinacao": c.nome, "motores": c.descricao, "empuxo_n": c.motor.empuxo_n, "isp_s": c.motor.isp_s,
                                 "massa_motores_kg": c.massa_kg, "caso": rotulo, "missao": mis["id"], "vinf_km_s": vinf,
                                 "orbita_inicial": de, "m0_kg": m0, **_res(r), "propelente_dimensionado_kg": prop_dim,
                                 "cabe_no_dimensionado": bool(r.propelente_kg <= prop_dim), "queima_unica_max_s": c.queima_unica_max_s,
                                 "excede_queima_unica": bool(r.duracao_s > c.queima_unica_max_s), "nota": c.nota})

    # Cruzeiro do lander: todas as correções da ida (Δv do dimensionamento, com margem), somadas
    q = _queima(lan["estagios"], "cruzeiro_lander", "correcoes_ida")
    isp_cz = v(ler("config/superficie.yaml")["lancamento"]["cruzeiro_lander"]["isp_s"])
    dv_cz = isp_cz * qf.G0 * math.log(q["massa_antes_kg"] / (q["massa_antes_kg"] - q["propelente_kg"]))
    for c in mt.conjuntos("cruzeiro"):
        t = qf.tempo_de_queima_s(c.motor, q["massa_antes_kg"], dv_cz)
        out["cruzeiro"].append({"combinacao": c.nome, "motores": c.descricao, "empuxo_n": c.motor.empuxo_n, "isp_s": c.motor.isp_s,
                                "massa_motores_kg": c.massa_kg, "m0_kg": q["massa_antes_kg"], "dv_total_km_s": dv_cz,
                                "duracao_total_s": t, "queima_unica_max_s": c.queima_unica_max_s,
                                "excede_queima_unica": bool(t > c.queima_unica_max_s)})

    # MAV: dois estágios
    for est, funcao in zip(lan["mav_estagios"], ("mav_1", "mav_2")):
        for c in mt.conjuntos(funcao):
            t = qf.tempo_de_queima_s(c.motor, est["massa_inicial_kg"], est["dv_km_s"])
            peso = est["massa_inicial_kg"] * g_marte
            out["mav"].append({"estagio": est["nome"], "combinacao": c.nome, "motores": c.descricao, "empuxo_n": c.motor.empuxo_n,
                               "isp_s": c.motor.isp_s, "isp_dimensionamento_s": est["isp_s"], "massa_motores_kg": c.massa_kg,
                               "m0_kg": est["massa_inicial_kg"], "dv_km_s": est["dv_km_s"], "duracao_s": t,
                               "empuxo_peso_marte": c.motor.empuxo_n / peso, "aceleracao_inicial_m_s2": c.motor.empuxo_n / est["massa_inicial_kg"],
                               "queima_unica_max_s": c.queima_unica_max_s, "excede_queima_unica": bool(t > c.queima_unica_max_s),
                               "nota": c.nota})
    out["g_marte_m_s2"] = g_marte
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "queima_finita.yaml").write_text(yaml.safe_dump(nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")
    (SAIDA / "queima_finita.md").write_text(_md(out), encoding="utf-8")


def _res(r):
    return {"duracao_s": r.duracao_s, "propelente_kg": r.propelente_kg, "dv_motor_km_s": r.dv_motor_km_s,
            "dv_impulsivo_km_s": r.dv_impulsivo_km_s, "perda_km_s": r.perda_km_s, "inicio_rel_periapse_s": r.inicio_rel_periapse_s,
            "altitude_minima_km": r.altitude_minima_km, "periapse_final_km": r.rp_final_km,
            "apoapse_final_km": None if np.isinf(r.ra_final_km) else r.ra_final_km,
            "vinf_final_km_s": None if np.isnan(r.vinf_final_km_s) else r.vinf_final_km_s,
            "periapse_chegada_alt_km": None if np.isnan(r.periapse_chegada_alt_km) else r.periapse_chegada_alt_km}


def _md(out):
    br = lambda x, n=0: "—" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    sim = lambda b: "**sim**" if b else "não"  # noqa: E731
    nao = lambda b: "sim" if b else "**não**"  # noqa: E731
    p15 = out["p015_km_s"]
    md = ["# Etapa 3.1 — motores reais e queima finita (gerado por tools/queima_finita.py)", "",
          f"Modelo: {out['modelo']}. Perda = Δv entregue pelo motor − Δv impulsivo no periapse. "
          "Rótulo: calculado (não verificado contra caso publicado).", "",
          "Massa no início de cada queima e propelente dimensionado: dimensionamento atual (regra iii, Isp de 321 s, perdas da P-015 e "
          "margem de Δv da P-014), sem refazer com o Isp de cada combinação. \"Cabe?\" compara o propelente da queima finita com o "
          "dimensionado para aquela queima; o caso de referência usa o mesmo veículo.", "",
          f"Perdas do DRA usadas hoje (P-015, NÃO VALIDADA): captura {br(1e3 * p15['captura_marte'])} m/s; "
          f"saída de Marte {br(1e3 * p15['saida_marte'])} m/s.", "",
          "## Captura em Marte (órbita de 1 sol)", "",
          "| Combinação | Empuxo (N) | Isp (s) | Caso | v∞ (km/s) | m0 (kg) | Queima (s) | Propelente (kg) | Δv impulsivo (m/s) | Perda (m/s) | Perda (% do Δv) | Perda / P-015 | Periapse de chegada (km) | Altitude mínima (km) | Propelente dimensionado (kg) | Cabe? | Queima única máx. (s) | Excede? |",
          "| :- | -: | -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- |"]
    for x in out["captura"]:
        md.append(f"| {x['combinacao']}: {x['motores']} | {br(x['empuxo_n'])} | {br(x['isp_s'], 1)} | {x['caso']} ({x['missao']}) | "
                  f"{br(x['vinf_km_s'], 3)} | {br(x['m0_kg'])} | {br(x['duracao_s'])} | {br(x['propelente_kg'])} | {br(1e3 * x['dv_impulsivo_km_s'])} | "
                  f"{br(1e3 * x['perda_km_s'], 1)} | {br(100 * x['perda_km_s'] / x['dv_impulsivo_km_s'], 1)} | {br(x['perda_km_s'] / p15['captura_marte'], 1)}× | "
                  f"{br(x['periapse_chegada_alt_km'])} | {br(x['altitude_minima_km'])} | {br(x['propelente_dimensionado_kg'])} | "
                  f"{nao(x['cabe_no_dimensionado'])} | {br(x['queima_unica_max_s'])} | {sim(x['excede_queima_unica'])} |")
    md += ["", "## Saída de Marte (injeção trans-Terra)", "",
           "| Combinação | Empuxo (N) | Isp (s) | Caso | v∞ (km/s) | Órbita inicial | m0 (kg) | Queima (s) | Propelente (kg) | Δv impulsivo (m/s) | Perda (m/s) | Perda (% do Δv) | Perda / P-015 | Propelente dimensionado (kg) | Cabe? | Queima única máx. (s) | Excede? |",
           "| :- | -: | -: | :- | -: | :- | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- |"]
    for x in out["saida"]:
        md.append(f"| {x['combinacao']}: {x['motores']} | {br(x['empuxo_n'])} | {br(x['isp_s'], 1)} | {x['caso']} ({x['missao']}) | "
                  f"{br(x['vinf_km_s'], 3)} | {x['orbita_inicial']} | {br(x['m0_kg'])} | {br(x['duracao_s'])} | {br(x['propelente_kg'])} | "
                  f"{br(1e3 * x['dv_impulsivo_km_s'])} | {br(1e3 * x['perda_km_s'], 1)} | {br(100 * x['perda_km_s'] / x['dv_impulsivo_km_s'], 1)} | "
                  f"{br(x['perda_km_s'] / p15['saida_marte'], 1)}× | {br(x['propelente_dimensionado_kg'])} | {nao(x['cabe_no_dimensionado'])} | "
                  f"{br(x['queima_unica_max_s'])} | {sim(x['excede_queima_unica'])} |")
    md += ["", "## Cruzeiro do lander (todas as correções da ida, somadas)", "",
           "Perda de queima finita não calculada: Δv pequeno, longe de qualquer planeta.", "",
           "| Combinação | Empuxo (N) | Isp (s) | m0 (kg) | Δv total (m/s) | Tempo total de queima (s) | Queima única máx. (s) |",
           "| :- | -: | -: | -: | -: | -: | -: |"]
    for x in out["cruzeiro"]:
        md.append(f"| {x['combinacao']}: {x['motores']} | {br(x['empuxo_n'])} | {br(x['isp_s'])} | {br(x['m0_kg'])} | {br(1e3 * x['dv_total_km_s'], 1)} | "
                  f"{br(x['duracao_total_s'])} | {br(x['queima_unica_max_s'])} |")
    md += ["", "## MAV (dois estágios)", "",
           f"Empuxo/peso na superfície de Marte, g = {br(out['g_marte_m_s2'], 3)} m/s². Perda de subida já incluída no Δv "
           "(Etapa 2.1); não recalculada. O dimensionamento usa Isp de 343 s (Bowles et al. 2013, motor com turbobomba). "
           "O estágio 2 acende em voo: o empuxo/peso dele em Marte é só referência.", "",
           "| Estágio | Combinação | Empuxo (N) | Isp (s) | m0 (kg) | Δv (m/s) | Queima (s) | Empuxo/peso em Marte | Aceleração inicial (m/s²) | Queima única máx. (s) | Excede? |",
           "| :- | :- | -: | -: | -: | -: | -: | -: | -: | -: | :- |"]
    for x in out["mav"]:
        md.append(f"| {x['estagio']} | {x['combinacao']}: {x['motores']} | {br(x['empuxo_n'])} | {br(x['isp_s'])} | {br(x['m0_kg'], 1)} | "
                  f"{br(1e3 * x['dv_km_s'])} | {br(x['duracao_s'])} | {br(x['empuxo_peso_marte'], 2)} | {br(x['aceleracao_inicial_m_s2'], 2)} | "
                  f"{br(x['queima_unica_max_s'])} | {sim(x['excede_queima_unica'])} |")
    return "\n".join(md) + "\n"


if __name__ == "__main__":
    main()
