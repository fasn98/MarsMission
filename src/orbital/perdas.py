"""Perdas de queima finita do projeto (Etapa 3.1, ADR 0011): captura e saída de Marte com os motores escolhidos
(config/motores.yaml, "escolha"), em várias queimas no periapse (orbital.queima_multipla), nas massas do dimensionamento.

Caso de projeto, como no dimensionamento (regra iii, ADR 0004): captura na janela de maior Δv de captura e saída na de
maior Δv de saída do envelope. O número de queimas é o de menor propelente entre os de config/queima_finita.yaml que
respeitam queima única, vida acumulada, partidas e tempo de estada. Usado por tools/redimensiona.py (ponto fixo) e por
tools/queima_finita.py.
"""

from __future__ import annotations

import math

from orbital import manobras as mn
from orbital import motores as mt
from orbital import queima_multipla as qm
from orbital.config import ler, parametros, v
from orbital.constantes import UA_KM, GM_SOL


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


def limites_ok(seq, conjunto, estada_dias):
    """Restrições de uma sequência: (queima única, vida acumulada, partidas, tempo); None quando o motor não tem o dado."""
    ok = lambda lim, x: None if math.isnan(lim) else bool(x <= lim)  # noqa: E731
    return {"queima_unica_ok": ok(conjunto.queima_unica_max_s, max(seq.duracoes_s)),
            "vida_acumulada_ok": ok(conjunto.vida_acumulada_s, sum(seq.duracoes_s)),
            "partidas_ok": ok(conjunto.partidas, seq.n), "tempo_ok": bool(seq.duracao_sequencia_dias <= estada_dias)}


def melhor(sequencias, conjunto, estada_dias):
    """A sequência viável de menor propelente que não viola nenhum limite conhecido; None se nenhuma."""
    boas = [s for s in sequencias if s.viavel and all(x is not False for x in limites_ok(s, conjunto, estada_dias).values())]
    return min(boas, key=lambda s: s.propelente_kg) if boas else None


def geometria():
    """(μ de Marte, raio de Marte, órbita de 1 sol, raio de Hill, fração do raio de Hill, lista de N)."""
    p = parametros()
    R = v(ler("config/parametros_orbitais.yaml")["raio_marte_km"])
    qcfg = ler("config/queima_finita.yaml")["varias_queimas"]
    a_marte = v(ler("config/mav_propulsao.yaml")["cruzeiro"]["distancia_marte_ua"]) * UA_KM
    return (p.mu_marte, R, p.orbitas_marte["eliptica_alta"], qm.raio_hill(p.mu_marte, GM_SOL, a_marte),
            v(qcfg["fracao_raio_hill"]), list(qcfg["numero_de_queimas"]["valor"]))


def orbita_de_saida(mu, R, um, vinf):
    """(rp, ra) de onde parte a injeção trans-Terra: a órbita de encontro (results/etapa2.3/plataformas.yaml) ou a de
    1 sol, a que for mais barata, como orbital.veiculos.dv_extra_orbitador."""
    pl = ler("results/etapa2.3/plataformas.yaml")["orbita_encontro"]
    rp_e, ra_e = R + pl["periapse_alt_km"], R + pl["apoapse_regra_5pct_km"]
    tei_e = float(mn.dv_hiperbole_orbita(mu, vinf, rp_e, ra_e))
    voltar = mn.dv_transferencia_coaxial(mu, rp_e, ra_e, um.rp, um.ra) + float(mn.dv_hiperbole_orbita(mu, vinf, um.rp, um.ra))
    return (rp_e, ra_e) if tei_e <= voltar else (um.rp, um.ra)


def perdas_projeto(vei):
    """Perdas de captura e de saída do caso de projeto com os motores escolhidos, nas massas de `vei`
    (orbital.veiculos.veiculos(detalhe=True)[0]). Devolve o detalhe e as perdas em km/s."""
    mu, R, um, r_h, f_h, ns = geometria()
    esc = ler("config/motores.yaml")["escolha"]
    cap = next(c for c in mt.conjuntos("captura") if c.nome == esc["captura"])
    ret = next(c for c in mt.conjuntos("retorno") if c.nome == esc["retorno"])
    orb = vei["orbitador_regra_iii"]["estagios"]
    q = {e["nome"]: {x["nome"]: x for x in e["queimas"]} for e in orb}
    m_cap, m_sai = q["insercao_marte"]["captura_marte"]["massa_antes_kg"], q["retorno"]["saida_marte"]["massa_antes_kg"]
    cs = casos()
    _, mc = cs["captura"][0]
    _, ms = cs["saida"][0]
    seq_c = [qm.captura_multipla(mu, R, cap.motor, m_cap, mc["vinf_chegada_marte_km_s"], um.rp, um.ra, n, r_h, f_h) for n in ns]
    vinf_s = math.sqrt(ms["c3l_partida_marte_km2_s2"])
    rp_s, ra_s = orbita_de_saida(mu, R, um, vinf_s)
    seq_s = [qm.saida_multipla(mu, R, ret.motor, m_sai, rp_s, ra_s, vinf_s, n, r_h, f_h) for n in ns]
    bc, bs = melhor(seq_c, cap, mc["em_marte_dias"]), melhor(seq_s, ret, ms["em_marte_dias"])
    if bc is None or bs is None:
        raise RuntimeError("nenhum número de queimas respeita os limites dos motores escolhidos")
    return {"perda_km_s": {"captura_marte": bc.perda_km_s, "saida_marte": bs.perda_km_s},
            "captura": {"combinacao": cap.nome, "motores": cap.descricao, "missao": mc["id"], "n": bc.n, "m0_kg": m_cap,
                        "propelente_kg": bc.propelente_kg, "dv_impulsivo_km_s": bc.dv_impulsivo_km_s, "duracoes_s": bc.duracoes_s},
            "saida": {"combinacao": ret.nome, "motores": ret.descricao, "missao": ms["id"], "n": bs.n, "m0_kg": m_sai,
                      "propelente_kg": bs.propelente_kg, "dv_impulsivo_km_s": bs.dv_impulsivo_km_s, "duracoes_s": bs.duracoes_s}}
