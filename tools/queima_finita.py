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
from orbital import queima_multipla as qm  # noqa: E402
from orbital.constantes import GM_SOL, UA_KM  # noqa: E402
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
    out.update(varias_queimas(mu, R, um, rp_enc, ra_enc, orb, cs))
    out["g_marte_m_s2"] = g_marte
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "queima_finita.yaml").write_text(yaml.safe_dump(nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")
    (SAIDA / "queima_finita.md").write_text(_md(out), encoding="utf-8")


def _arredondar(x, passo):
    """Arredonda ao múltiplo de `passo` (campos mal condicionados; config/queima_finita.yaml, P-041)."""
    return None if x is None or np.isnan(x) else round(round(x / passo) * passo, 10)


def _seq(s, c, prop_dim, estada_dias):
    """Linha de uma sequência de várias queimas, com as restrições de vida do motor e de tempo."""
    arr = ler("config/queima_finita.yaml")["arredondamento_resultados"]
    ok = lambda lim, x: None if math.isnan(lim) else bool(x <= lim)  # noqa: E731
    d = {"n": s.n, "viavel": s.viavel, "motivo": s.motivo}
    if not s.viavel:
        return d
    return {**d, "duracoes_s": s.duracoes_s, "maior_queima_s": max(s.duracoes_s), "soma_queimas_s": sum(s.duracoes_s),
            "propelente_kg": s.propelente_kg, "dv_motor_km_s": s.dv_motor_km_s, "dv_impulsivo_km_s": s.dv_impulsivo_km_s,
            "perda_km_s": _arredondar(s.perda_km_s, v(arr["perda_varias_queimas_km_s"])),
            "correcao_periapse_km_s": _arredondar(s.correcao_periapse_km_s, v(arr["perda_varias_queimas_km_s"])),
            "apoapses_intermediarios_km": s.apoapses_intermediarios_km, "duracao_sequencia_dias": s.duracao_sequencia_dias,
            "estada_dias": estada_dias, "altitude_minima_km": _arredondar(s.altitude_minima_km, v(arr["altitude_km"])),
            "cabe_no_dimensionado": bool(s.propelente_kg <= prop_dim),
            "queima_unica_ok": ok(c.queima_unica_max_s, max(s.duracoes_s)),
            "vida_acumulada_ok": ok(c.vida_acumulada_s, sum(s.duracoes_s)), "partidas_ok": ok(c.partidas, s.n),
            "tempo_ok": bool(s.duracao_sequencia_dias <= estada_dias)}


def _melhor(linhas):
    """Menor propelente entre os N viáveis que respeitam queima única, vida acumulada, partidas e tempo (None se nenhum)."""
    boas = [x for x in linhas if x["viavel"] and all(x[k] is not False for k in ("queima_unica_ok", "vida_acumulada_ok", "partidas_ok", "tempo_ok"))]
    return min(boas, key=lambda x: x["propelente_kg"])["n"] if boas else None


def varias_queimas(mu, R, um, rp_enc, ra_enc, orb, cs):
    """Captura e saída em 1..N queimas (P-042), sensibilidade à fração do raio de Hill e conferência com o ERO (P-043)."""
    qcfg = ler("config/queima_finita.yaml")
    vq, ero = qcfg["varias_queimas"], qcfg["verificacao_ero"]
    ns, f_h = vq["numero_de_queimas"]["valor"], v(vq["fracao_raio_hill"])
    a_marte = v(ler("config/mav_propulsao.yaml")["cruzeiro"]["distancia_marte_ua"]) * UA_KM
    r_h = qm.raio_hill(mu, GM_SOL, a_marte)
    q_cap = _queima(orb["estagios"], "insercao_marte", "captura_marte")
    q_sai = _queima(orb["estagios"], "retorno", "saida_marte")
    out = {"raio_hill_km": r_h, "fracao_raio_hill": f_h, "varias_queimas": {"captura": [], "saida": []},
           "sensibilidade_fracao_hill": [], "conferencia_ero": []}
    for c in mt.conjuntos("captura"):
        for rotulo, mis in cs["captura"]:
            linhas = [_seq(qm.captura_multipla(mu, R, c.motor, q_cap["massa_antes_kg"], mis["vinf_chegada_marte_km_s"], um.rp, um.ra,
                                               n, r_h, f_h), c, q_cap["propelente_kg"], mis["em_marte_dias"]) for n in ns]
            out["varias_queimas"]["captura"].append({"combinacao": c.nome, "motores": c.descricao, "caso": rotulo, "missao": mis["id"],
                                                     "propelente_dimensionado_kg": q_cap["propelente_kg"], "queima_unica_max_s": c.queima_unica_max_s,
                                                     "por_n": linhas, "melhor_n": _melhor(linhas)})
    for c in mt.conjuntos("retorno"):
        for rotulo, mis in cs["saida"]:
            vinf = math.sqrt(mis["c3l_partida_marte_km2_s2"])
            tei_enc = float(mn.dv_hiperbole_orbita(mu, vinf, rp_enc, ra_enc))
            voltar = mn.dv_transferencia_coaxial(mu, rp_enc, ra_enc, um.rp, um.ra) + float(mn.dv_hiperbole_orbita(mu, vinf, um.rp, um.ra))
            rp, ra = (rp_enc, ra_enc) if tei_enc <= voltar else (um.rp, um.ra)
            linhas = [_seq(qm.saida_multipla(mu, R, c.motor, q_sai["massa_antes_kg"], rp, ra, vinf, n, r_h, f_h), c,
                           q_sai["propelente_kg"], mis["em_marte_dias"]) for n in ns]
            out["varias_queimas"]["saida"].append({"combinacao": c.nome, "motores": c.descricao, "caso": rotulo, "missao": mis["id"],
                                                   "propelente_dimensionado_kg": q_sai["propelente_kg"], "queima_unica_max_s": c.queima_unica_max_s,
                                                   "por_n": linhas, "melhor_n": _melhor(linhas)})
    # Sensibilidade à fração do raio de Hill: combinações de 400 N, caso de projeto, maior N
    proj_cap, proj_sai = cs["captura"][0][1], cs["saida"][0][1]
    for f in vq["fracao_raio_hill_sensibilidade"]["valor"]:
        c = next(x for x in mt.conjuntos("captura") if x.nome == "C1")
        s = qm.captura_multipla(mu, R, c.motor, q_cap["massa_antes_kg"], proj_cap["vinf_chegada_marte_km_s"], um.rp, um.ra, max(ns), r_h, f)
        arr = ler("config/queima_finita.yaml")["arredondamento_resultados"]
        out["sensibilidade_fracao_hill"].append({"fracao_raio_hill": f, "combinacao": "C1", "n": max(ns),
                                                  "perda_km_s": _arredondar(s.perda_km_s, v(arr["perda_varias_queimas_km_s"])),
                                                  "maior_queima_s": max(s.duracoes_s) if s.viavel else None, "viavel": s.viavel})
    # Conferência de coerência com o ERO [F22, F29] (P-043)
    cat = mt.catalogo()
    me = cat[ero["motor"]["valor"]]
    motor = qf.Motor(me["empuxo_n"] * ero["motor"]["quantidade"], me["isp_s"])
    m0, prop = v(ero["massa_kg"]), v(ero["propelente_kg"])
    vinfs = list(ero["vinf_km_s"]["valor"]) + [cs["captura"][1][1]["vinf_chegada_marte_km_s"]]
    for vinf in vinfs:
        for nome_orb, ra_alvo in (("órbita de 1 sol", um.ra), ("órbita alta (f_H · raio de Hill)", f_h * r_h)):
            melhor = None
            for n in ns:
                if nome_orb.startswith("órbita alta") and n > 1:
                    break   # a órbita alta já é a da 1ª queima
                s = qm.captura_multipla(mu, R, motor, m0, vinf, um.rp, ra_alvo, n, r_h, f_h)
                if s.viavel and (melhor is None or s.propelente_kg < melhor.propelente_kg):
                    melhor = s
            arr = ler("config/queima_finita.yaml")["arredondamento_resultados"]
            out["conferencia_ero"].append({"vinf_km_s": vinf, "orbita": nome_orb, "n": melhor.n, "dv_impulsivo_km_s": melhor.dv_impulsivo_km_s,
                                           "perda_km_s": _arredondar(melhor.perda_km_s, v(arr["perda_varias_queimas_km_s"])), "propelente_kg": melhor.propelente_kg, "propelente_ero_kg": prop,
                                           "fecha": bool(melhor.propelente_kg <= prop), "maior_queima_s": max(melhor.duracoes_s),
                                           "queima_unica_max_s": me["queima_unica_max_s"],
                                           "queima_unica_ok": bool(max(melhor.duracoes_s) <= me["queima_unica_max_s"])})
    out["dv_motor_ero_km_s"] = me["isp_s"] * qf.G0 * math.log(m0 / (m0 - prop))
    return out


def _res(r):
    arr = ler("config/queima_finita.yaml")["arredondamento_resultados"]
    p_t, p_h = v(arr["inicio_s"]), v(arr["altitude_km"])
    return {"duracao_s": r.duracao_s, "propelente_kg": r.propelente_kg, "dv_motor_km_s": r.dv_motor_km_s,
            "dv_impulsivo_km_s": r.dv_impulsivo_km_s, "perda_km_s": r.perda_km_s,
            "inicio_rel_periapse_s": _arredondar(r.inicio_rel_periapse_s, p_t),
            "altitude_minima_km": _arredondar(r.altitude_minima_km, p_h), "periapse_final_km": _arredondar(r.rp_final_km, p_h),
            "apoapse_final_km": None if np.isinf(r.ra_final_km) else _arredondar(r.ra_final_km, p_h),
            "vinf_final_km_s": None if np.isnan(r.vinf_final_km_s) else r.vinf_final_km_s,
            "periapse_chegada_alt_km": _arredondar(r.periapse_chegada_alt_km, p_h)}


def _md_varias(out, br, sim, nao):
    """Seções de várias queimas, sensibilidade à fração do raio de Hill e conferência com o ERO."""
    ok = lambda x: "—" if x is None else ("sim" if x else "**não**")  # noqa: E731
    md = ["", "## Várias queimas no periapse (P-042)", "",
          f"A 1ª queima da captura (a última da saída) leva o excesso hiperbólico numa única passagem, até uma órbita alta de "
          f"apoapse = {br(out['fracao_raio_hill'], 3)} × raio de Hill de Marte ({br(out['raio_hill_km'])} km); as demais dividem o "
          "resto em partes iguais de velocidade no periapse. \"Cabe?\" compara com o propelente dimensionado; \"Queima única\", "
          "\"Vida\" e \"Partidas\" comparam com os limites do motor no catálogo (— = sem fonte); \"Tempo\" compara a duração "
          "da sequência com a estada em Marte da missão. N = 1 é a queima única das tabelas acima.", ""]
    for k, titulo in (("captura", "Captura"), ("saida", "Saída de Marte")):
        md += [f"### {titulo}", "",
               "| Combinação | Caso | N | Perda (m/s) | Propelente (kg) | Cabe? | Maior queima (s) | Queima única máx. (s) | Queima única | Vida | Partidas | Sequência (d) | Tempo |",
               "| :- | :- | -: | -: | -: | :- | -: | -: | :- | :- | :- | -: | :- |"]
        for x in out["varias_queimas"][k]:
            for l in x["por_n"]:
                if not l["viavel"]:
                    md.append(f"| {x['combinacao']}: {x['motores']} | {x['caso']} ({x['missao']}) | {l['n']} | inviável: {l['motivo']} | | | | | | | | | |")
                    continue
                md.append(f"| {x['combinacao']}: {x['motores']} | {x['caso']} ({x['missao']}) | {l['n']} | {br(1e3 * l['perda_km_s'], 1)} | "
                          f"{br(l['propelente_kg'])} | {nao(l['cabe_no_dimensionado'])} | {br(l['maior_queima_s'])} | {br(x['queima_unica_max_s'])} | "
                          f"{ok(l['queima_unica_ok'])} | {ok(l['vida_acumulada_ok'])} | {ok(l['partidas_ok'])} | {br(l['duracao_sequencia_dias'], 1)} | {ok(l['tempo_ok'])} |")
        md.append("")
    md += ["### Sensibilidade à fração do raio de Hill (C1, caso de projeto, maior N)", "",
           "| Fração | Perda (m/s) | Maior queima (s) |", "| -: | -: | -: |"]
    for x in out["sensibilidade_fracao_hill"]:
        md.append(f"| {br(x['fracao_raio_hill'], 2)} | {br(1e3 * x['perda_km_s'], 1)} | {br(x['maior_queima_s'])} |")
    md += ["", "## Conferência de coerência com o ERO da ESA (P-043; não é verificação)", "",
           f"ERO: massa úmida de ~6,5 t e 1.900 kg de propelente no módulo de inserção [F22], 2 × 400 N [F29]. Admitidos (P-043): a massa "
           f"úmida como massa na captura e todo o propelente do módulo na captura; assim, Δv do motor = "
           f"{br(1e3 * out['dv_motor_ero_km_s'])} m/s. As fontes não publicam v∞, órbita-alvo nem Δv da captura: "
           "a tabela varre o v∞ (o último é o da missão de referência) e mostra o melhor N.", "",
           "| v∞ (km/s) | Órbita-alvo | N | Δv impulsivo (m/s) | Perda (m/s) | Propelente (kg) | Fecha com 1.900 kg? | Maior queima (s) | Dentro da queima única? |",
           "| -: | :- | -: | -: | -: | -: | :- | -: | :- |"]
    for x in out["conferencia_ero"]:
        md.append(f"| {br(x['vinf_km_s'], 3)} | {x['orbita']} | {x['n']} | {br(1e3 * x['dv_impulsivo_km_s'])} | {br(1e3 * x['perda_km_s'])} | "
                  f"{br(x['propelente_kg'])} | {nao(x['fecha'])} | {br(x['maior_queima_s'])} | {nao(x['queima_unica_ok'])} |")
    return md


def _md(out):
    br = lambda x, n=0: "—" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    sim = lambda b: "**sim**" if b else "não"  # noqa: E731
    nao = lambda b: "sim" if b else "**não**"  # noqa: E731
    p15 = out["p015_km_s"]
    md = ["# Etapa 3.1 — motores reais e queima finita (gerado por tools/queima_finita.py)", "",
          f"Modelo: {out['modelo']}. Perda = Δv entregue pelo motor − Δv impulsivo no periapse. "
          "Rótulo: calculado (não verificado contra caso publicado).", "",
          "O mínimo do propelente no início da queima é plano: o início, a altitude mínima durante a queima e o periapse de "
          "chegada são mal condicionados, e as apsides finais da captura carregam o resíduo do ajuste ao alvo; vão "
          "arredondados (config/queima_finita.yaml, P-041). A perda, a duração e o propelente não.", "",
          "Massa no início de cada queima e propelente dimensionado: dimensionamento atual (regra iii, Isp de 321 s, perdas da P-015 e "
          "margem de Δv da P-014), sem refazer com o Isp de cada combinação. \"Cabe?\" compara o propelente da queima finita com o "
          "dimensionado para aquela queima; o caso de referência usa o mesmo veículo.", "",
          f"Perdas do DRA usadas hoje (P-015, NÃO VALIDADA): captura {br(1e3 * p15['captura_marte'])} m/s; "
          f"saída de Marte {br(1e3 * p15['saida_marte'])} m/s.", "",
          "## Captura em Marte (órbita de 1 sol)", "",
          "| Combinação | Empuxo (N) | Isp (s) | Caso | v∞ (km/s) | m0 (kg) | Queima (s) | Propelente (kg) | Δv impulsivo (m/s) | Perda (m/s) | Perda (% do Δv) | Perda / P-015 | Periapse de chegada (km) | Altitude mínima durante a queima (km) | Propelente dimensionado (kg) | Cabe? | Queima única máx. (s) | Excede? |",
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
    md += _md_varias(out, br, sim, nao)
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
