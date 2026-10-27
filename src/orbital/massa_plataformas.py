"""Plataformas do orbitador e do lander por subsistema, com margem de crescimento de massa (Etapas 2.3 e 2.5).

Orbitador: subsistemas do Mars Odyssey [F33], energia dimensionada para o afélio de Marte e o pior eclipse
na órbita de encontro do ADR 0005, cabeamento pela regra da ESA [F71]. Lander: L1/L2 (Phoenix [F74]), L3 (lander
do MSR sem MAV e sem rover de busca), base = L3 + braço (P-034) + helicópteros (ADR 0009). Margem: AIAA S-120A,
categoria E1 [F70], ponto médio; GSFC e ESA na sensibilidade.
Movido de tools/plataformas.py sem mudança de física (prova: results/conferencia/regeneracao_refatoracao.md,
tools/confere_regeneracao.py).
"""

from __future__ import annotations

from orbital import plataforma as pf
from orbital.config import v

MARGENS = ("e1_medio", "e1_minimo", "e1_maximo", "e1_medio_mais_gsfc", "esa")


def mga(cat, cfg, qual):
    """Margem de crescimento (fração) da categoria E1 para o critério `qual`."""
    lo, hi = cfg["margem_crescimento"]["categorias_e1"][cat]
    valores = {"e1_minimo": lo, "e1_maximo": hi, "e1_medio": 0.5 * (lo + hi), "e1_medio_mais_gsfc": 0.5 * (lo + hi)}
    if qual not in valores:
        raise ValueError(f"critério de margem desconhecido: {qual}")
    return valores[qual] / 100.0


def prevista(itens, cfg, qual):
    """Massa prevista da lista para um critério de margem. `itens`: [(nome, básica, categoria)]."""
    basica = sum(m for _, m, _ in itens)
    if qual == "esa":
        a = cfg["margem_crescimento"]["alternativas"]["esa"]
        return basica * (1 + a["equipamento"]) * (1 + a["sistema"])
    if qual not in MARGENS:
        raise ValueError(f"critério de margem desconhecido: {qual}")
    tot = sum(pf.com_margem(m, mga(c, cfg, qual)) for _, m, c in itens)
    if qual == "e1_medio_mais_gsfc":
        tot += cfg["margem_crescimento"]["alternativas"]["gsfc"]["sistema_sobre_basica"] * basica
    return tot


def orbitador(cfg, po, apoapse_km, rp_alt_km):
    """(itens [(nome, básica, categoria)], energia) da plataforma do orbitador na órbita de encontro rp × ra."""
    o = cfg["orbitador"]
    e = o["energia"]
    R, mu = v(po["raio_marte_km"]), v(po["gm_marte"])
    t_ecl, periodo = pf.eclipse_maximo(mu, R, R + rp_alt_km, R + apoapse_km)
    t_sol = periodo - t_ecl
    carga = v(e["carga_w"])
    d_af = v(e["distancia_ua"]["semieixo"]) * (1 + v(e["distancia_ua"]["excentricidade"]))
    p_sa = pf.potencia_painel(carga, t_sol, t_ecl, v(e["eficiencia_recarga"]))
    m_sa = pf.massa_painel(p_sa, v(e["painel_w_kg_1ua"]), d_af, v(e["fator_perdas_painel"]))
    e_ecl = carga * t_ecl / 3600.0
    cap, m_bat = pf.bateria(e_ecl, v(e["profundidade_descarga"]), v(e["energia_especifica_bateria_wh_kg"]))
    s = o["subsistemas"]
    er = s["energia_restante"]
    m_rest = v(er["massa_energia_odyssey_kg"]) - v(er["painel_odyssey_w_1ua"]) / v(e["painel_w_kg_1ua"])
    itens = [(k, float(s[k]["massa_kg"]), s[k]["categoria"]) for k in
             ("estrutura", "termico", "comunicacao", "comando_e_dados", "gnc", "mecanismos", "rss_nac", "rss_lidar")]
    itens += [("painel_solar", m_sa, "painel_solar"), ("bateria", m_bat, "baterias"),
              ("energia_restante", m_rest, er["categoria"])]
    f = v(o["cabeamento"]["fracao"])
    m_cab = f / (1 - f) * sum(m for _, m, _ in itens)  # base: só a plataforma (P-031)
    itens.append(("cabeamento", m_cab, "cabeamento"))
    energia = {"eclipse_max_h": t_ecl / 3600, "periodo_h": periodo / 3600, "carga_w": carga, "afelio_ua": d_af,
               "painel_w_afelio": p_sa, "energia_eclipse_wh": e_ecl, "bateria_wh_nominal": cap,
               "w_kg_painel_afelio": v(e["painel_w_kg_1ua"]) * v(e["fator_perdas_painel"]) / d_af**2}
    return itens, energia


def lander(cfg, opcao, mav_bloco_kg):
    """(itens, energia) das referências L1 (núcleo do Phoenix) e L2 (núcleo escalado pela massa pousada)."""
    la = cfg["lander"]
    e = la["energia"]
    ph = la["phoenix"]
    s = la["subsistemas"]
    sol_h = v(e["duracao_sol_h"])
    e_sol = v(e["energia_por_sol_wh"])
    carga = e_sol / sol_h
    e_noite = carga * v(e["noite_fracao_sol"]) * sol_h
    oc = cfg["orbitador"]["energia"]
    cap, m_bat = pf.bateria(e_noite, v(oc["profundidade_descarga"]), v(oc["energia_especifica_bateria_wh_kg"]))
    rend = v(e["rendimento_painel_wh_sol_m2"]["energia_wh"]) / v(e["rendimento_painel_wh_sol_m2"]["area_m2"])
    area = e_sol / rend
    m_sa = area * v(e["densidade_area_painel_w_m2"]) / v(oc["painel_w_kg_1ua"])
    itens = [(k, float(s[k]["massa_kg"]), s[k]["categoria"]) for k in ("uhf", "banda_x_cruzeiro", "radar", "amostras")]
    itens += [("painel_solar", m_sa, "painel_solar"), ("bateria", m_bat, "baterias")]
    seco_ph = v(ph["lander_kg"]) - v(ph["combustivel_kg"])
    nucleo_ph = seco_ph - v(ph["instrumentos_kg"]) - sum(float(s[k]["massa_kg"]) for k in ("uhf", "banda_x_cruzeiro", "radar"))
    if opcao == "L1":
        nucleo = nucleo_ph
    else:  # L2: núcleo = k × massa pousada seca, com k do Phoenix
        k = nucleo_ph / seco_ph
        nucleo = k / (1 - k) * (sum(m for _, m, _ in itens) + mav_bloco_kg)
    itens.insert(0, ("nucleo", nucleo, s["nucleo"]["categoria"]))
    energia = {"energia_por_sol_wh": e_sol, "carga_media_w": carga, "energia_noite_wh": e_noite, "bateria_wh_nominal": cap,
               "area_painel_m2": area, "rendimento_wh_sol_m2": rend, "nucleo_phoenix_kg": nucleo_ph,
               "fracao_nucleo_phoenix": nucleo_ph / seco_ph}
    return itens, energia


def lander_l3(cfg):
    """L3: lander do MSR sem MAV e sem rover de busca (alocação, sem MGA adicional no caso de base)."""
    t = cfg["lander"]["topo_para_baixo"]
    return v(t["srl_seco_superficie_kg"]) - v(t["srl_mav_kg"]) - v(t["srl_sfr_kg"])


def l3_com_margem(m, cfg, qual):
    a = cfg["margem_crescimento"]["alternativas"]
    if qual == "esa":
        return m * (1 + a["esa"]["equipamento"]) * (1 + a["esa"]["sistema"])
    if qual == "e1_medio_mais_gsfc":
        return m * (1 + a["gsfc"]["sistema_sobre_basica"])
    if qual == "e1_medio":
        return m
    raise ValueError(f"critério de margem sem uso no L3: {qual}")


def lander_base(cfg, qual="e1_medio"):
    """Base do lander: L3 + braço de coleta (item "amostras", P-034) + helicópteros de recuperação (ADR 0009),
    cada item com a sua margem E1."""
    s = cfg["lander"]["subsistemas"]
    itens = [(k, float(s[k]["massa_kg"]), s[k]["categoria"]) for k in ("amostras", "helicopteros") if k in s]
    return l3_com_margem(lander_l3(cfg), cfg, qual) + prevista(itens, cfg, qual)


def limite_srl_2024(cfg):
    """Limite superior da faixa do lander: SRL de 2024 menos o MAV (comparabilidade não confirmada)."""
    t = cfg["lander"]["topo_para_baixo"]
    return v(t["srl_2024_pousado_kg"]) - v(t["srl_mav_kg"])


def plataforma_orbitador(cfg, po, apoapse_km, rp_alt_km, qual="e1_medio"):
    return prevista(orbitador(cfg, po, apoapse_km, rp_alt_km)[0], cfg, qual)
