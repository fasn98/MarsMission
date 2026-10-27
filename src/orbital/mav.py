"""MAV e equipamentos que pousam com ele: dimensionamento genérico de dois estágios, armazenamento criogênico sem
evaporação (ZBO) e fonte de energia (Etapas 2.2 e 2.2b), usados pelas Etapas 2.3 a 2.5 e pelo painel.

Movido de tools/mav_propulsao.py e tools/isru.py sem mudança de física (prova: results/conferencia/regeneracao_painel.md,
tools/confere_regeneracao.py).
"""

from __future__ import annotations

from orbital import foguete as fg
from orbital import isru
from orbital.config import v


def zbo(icfg, m_ch4, m_lox):
    z = icfg["armazenamento_zbo"]
    a = v(z["expoente"])
    p = m = 0.0
    if m_ch4 > 0:
        p += isru.escala(z["ch4"]["potencia_w"], m_ch4, v(z["referencia_ch4_kg"]), a)
        m += isru.escala(z["ch4"]["massa_kg"], m_ch4, v(z["referencia_ch4_kg"]), a)
    if m_lox > 0:
        p += isru.escala(z["lox"]["potencia_w"], m_lox, v(z["referencia_lox_kg"]), a)
        m += isru.escala(z["lox"]["massa_kg"], m_lox, v(z["referencia_lox_kg"]), a)
    return p, m


def energia(icfg, potencia_w, fonte):
    e = icfg["energia"]
    if potencia_w <= 0:
        return 0.0, ""
    if fonte == "mmrtg":
        r = e["mmrtg"]
        m, n = isru.massa_rtg(potencia_w, v(r["potencia_inicio_w"]), v(r["massa_kg"]), v(r["degradacao_anual"]),
                              e["anos_ate_fim_da_estada"])
        return m, f"{n} MMRTG"
    s = e["solar"]
    return isru.escala(v(s["massa_kg"]), potencia_w, v(s["potencia_continua_w"]), v(s["expoente"])), "solar"


def mav_generico(dv, op, scfg):
    f1 = v(scfg["mav"]["fracao_dv_estagio_1"])
    eps = v(op["fracao_estrutural"])
    e1 = fg.Estagio("mav_1", op["isp_s"][0], eps, [fg.Queima("subida_1", f1 * dv)])
    e2 = fg.Estagio("mav_2", op["isp_s"][1], eps, [fg.Queima("subida_2", (1 - f1) * dv)])
    r = fg.dimensionar_veiculo([e1, e2], v(scfg["mav"]["carga_util_kg"]))
    prop = sum(s.propelente for s in r)
    return r[0].massa_inicial, prop


def massas_opcao(dv, nome, mcfg, scfg, icfg, fonte_energia):
    """(massa pousada do MAV + equipamentos de armazenamento e energia, massa extra no cruzeiro, detalhe)."""
    op = mcfg["opcoes"][nome]
    glom, prop = mav_generico(dv, op, scfg)
    det = {"mav_glom_kg": glom, "mav_propelente_kg": prop}
    if not op["criogenico"]:
        aq = mcfg["aquecimento"]
        dt = v(aq["t_minima_c"][nome]) - v(aq["t_ambiente_c"])
        dt_ref = v(aq["t_referencia_c"]) - v(aq["t_ambiente_c"])
        p_aq = isru.escala(v(aq["referencia_w"]) * dt / dt_ref, prop, v(aq["m_prop_referencia_kg"]), v(aq["expoente_area"]))
        m_en, desc = energia(icfg, p_aq, fonte_energia)
        det.update({"aquecimento_w": p_aq, "energia_superficie_kg": m_en, "energia_superficie": desc})
        return glom + m_en, 0.0, det
    m_ox, m_ch4 = isru.divisao_of(prop, v(op["razao_of"]))
    # Superfície: armazenamento sem evaporação + fonte de energia (como na Etapa 2.2)
    p_sup, m_sup = zbo(icfg, m_ch4, m_ox)
    m_en, desc = energia(icfg, p_sup, fonte_energia)
    # Cruzeiro: armazenamento sem evaporação (P-026) alimentado por painéis no cruzeiro (descartados antes da entrada)
    cz = mcfg["cruzeiro"]
    z = cz["zbo_transito"]
    p_cz = sum(isru.escala(z["potencia_w"], m, z["referencia_kg"], z["expoente"]) for m in (m_ch4, m_ox))
    m_cz_hw = sum(isru.escala(z["massa_ativa_kg"] + z["massa_passiva_kg"], m, z["referencia_kg"], z["expoente"]) for m in (m_ch4, m_ox))
    w_kg_marte = v(cz["solar_w_kg_1ua"]) / v(cz["distancia_marte_ua"]) ** 2
    m_paineis = p_cz / w_kg_marte
    # O hardware de cruzeiro e o de superfície servem aos mesmos tanques: conta-se o maior dos dois.
    m_hw = max(m_sup, m_cz_hw)
    det.update({"o2_kg": m_ox, "ch4_kg": m_ch4, "zbo_superficie_w": p_sup, "zbo_superficie_kg": m_sup,
                "energia_superficie_kg": m_en, "energia_superficie": desc, "zbo_cruzeiro_w": p_cz,
                "zbo_cruzeiro_kg": m_cz_hw, "paineis_cruzeiro_kg": m_paineis, "armazenamento_pousado_kg": m_hw})
    return glom + m_hw + m_en, m_paineis, det
