"""Veículos da arquitetura (Etapas 2.3 a 2.5): massas injetadas do orbitador (regra iii e missão A) e do lander,
com o detalhe por estágio. Usado por tools/lancamento.py, tools/arquitetura.py, tools/coleta.py e pelo painel.

Movido de tools/lancamento.py, tools/superficie.py e tools/varredura_encontro.py sem mudança de física (prova:
results/conferencia/regeneracao_painel.md, tools/confere_regeneracao.py). Lê config/ e os resultados das Etapas 1.3, 2.2 e 2.3.
"""

from __future__ import annotations

import copy

import numpy as np

from orbital import dimensionamento as dm
from orbital import foguete as fg
from orbital import manobras as mn
from orbital import superficie as sf
from orbital.config import ler, parametros, v
from orbital.mav import massas_opcao, mav_estagios


def _estagio(e, detalhe):
    """Detalhe de um estágio dimensionado; com `detalhe`, também a massa logo antes de cada queima e o propelente dela
    (Etapa 3.1). Sem `detalhe`, as chaves são as de antes (tools/lancamento.py grava este dicionário em results/)."""
    d = {"nome": e.nome, "massa_inicial_kg": e.massa_inicial, "propelente_kg": e.propelente, "inerte_kg": e.inerte}
    if detalhe:
        d["queimas"] = [{"nome": n, "massa_antes_kg": e.massa_antes_por_queima[n], "propelente_kg": e.propelente_por_queima[n]}
                        for n in e.propelente_por_queima]
    return d


def lander_estagios(chegada, cfg, dcfg, p, caso_saida):
    """Estágios do lander [saída da Terra, cruzeiro]; [1].massa_inicial é a massa injetada na trajetória.

    O estágio de cruzeiro leva, além de `chegada`, o circuito de fluido de rejeição de calor (Etapa 4.5, P-077), que é
    descartado com ele antes da entrada."""
    margem = v(dcfg["margem_dv"])
    dv = dm.orcamento(caso_saida, dcfg, p)
    cz = cfg["lancamento"]["cruzeiro_lander"]
    st = dcfg["estagios"]["saida_terra"]
    cruz = fg.Estagio("cruzeiro_lander", v(cz["isp_s"]), v(cz["fracao_estrutural"]),
                      [fg.Queima("correcoes_ida", (1 + margem) * dv["correcoes_ida"])])
    saida = fg.Estagio("saida_terra_lander", v(st["isp_s"]), v(st["fracao_estrutural"]),
                       [fg.Queima("saida_terra", (1 + margem) * dv["saida_terra"])])
    return fg.dimensionar_veiculo([saida, cruz], chegada + circuito_fluido(cfg))


def circuito_fluido(cfg):
    """Massa do circuito de fluido no estágio de cruzeiro do lander (kg; 0 nas etapas anteriores à 4.5)."""
    c = cfg["lancamento"]["cruzeiro_lander"].get("circuito_fluido_kg")
    return 0.0 if c is None else v(c)


def dv_extra_orbitador(mu, um_sol, rp, ra, c3l, descer):
    """Δv extra do orbitador para usar a órbita de encontro rp × ra em vez da de 1 sol (km/s).

    Descer da órbita de 1 sol até a de encontro, mais o custo extra da injeção trans-Terra: o menor entre
    partir da órbita de encontro ou voltar à de 1 sol."""
    vinf = np.sqrt(c3l)
    tei_1sol = float(mn.dv_hiperbole_orbita(mu, vinf, um_sol.rp, um_sol.ra))
    tei_alvo = float(mn.dv_hiperbole_orbita(mu, vinf, rp, ra))
    voltar = mn.dv_transferencia_coaxial(mu, rp, ra, um_sol.rp, um_sol.ra) + tei_1sol
    return descer + min(tei_alvo, voltar) - tei_1sol


def veiculos(plataforma_lander_kg=None, dcfg=None, scfg=None, detalhe=False, mcfg=None):
    """Massas injetadas (sem estágio de saída) do orbitador (iii e A) e do lander, no caso de base da Etapa 2.3.

    `plataforma_lander_kg` substitui a plataforma do lander do config (opções de coleta, Etapa 2.5); `dcfg` e `scfg`
    substituem config/dimensionamento.yaml e config/superficie.yaml (sensibilidade da Etapa 2.5); `mcfg`, o
    config/mav_propulsao.yaml. Cada veículo traz
    também o detalhe por estágio ("estagios") e, no lander, as massas de chegada, pouso e MAV. Com `detalhe=True`
    (Etapa 3.1), cada estágio traz as queimas (massa antes e propelente) e o lander traz os estágios do MAV."""
    dcfg = ler("config/dimensionamento.yaml") if dcfg is None else dcfg
    scfg = ler("config/superficie.yaml") if scfg is None else scfg
    cu = ler("config/carga_util.yaml")
    mcfg = ler("config/mav_propulsao.yaml") if mcfg is None else mcfg
    icfg, po = ler("config/isru.yaml"), ler("config/parametros_orbitais.yaml")
    p = parametros()
    a_caso, jan, piores = dm.casos(dcfg, p)
    vs = dm.variantes(a_caso, jan, piores)
    pl = ler("results/etapa2.3/plataformas.yaml")
    mp = ler("results/etapa2.2/mav_propulsao.yaml")
    op_mav = mp["melhor_opcao"]
    fonte_mav = min((x for x in mp["opcoes"] if x["opcao"] == op_mav), key=lambda x: x["total_regra_iii_kg"])["energia"]
    R, mu, um = v(po["raio_marte_km"]), p.mu_marte, p.orbitas_marte["eliptica_alta"]
    rp, ra = R + pl["orbita_encontro"]["periapse_alt_km"], R + pl["orbita_encontro"]["apoapse_regra_5pct_km"]
    ms = ler("results/etapa1.3/missoes.yaml")
    cand = {c["id"]: c for c in ms["candidatas"]}
    ref = ler("config/missao_referencia.yaml")["missao_referencia"]["id"]
    janelas = [cand[w["missao"]] for w in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].values()]
    c3l = {"missao_A": cand[ref]["c3l_partida_marte_km2_s2"], "regra_iii": max(x["c3l_partida_marte_km2_s2"] for x in janelas)}
    descer = mn.dv_transferencia_coaxial(mu, um.rp, um.ra, rp, ra)
    margem = v(dcfg["margem_dv"])
    out = {}
    for caso, var in (("missao_A", "missao_A"), ("regra_iii", dcfg["regra_projeto"])):
        extra = dv_extra_orbitador(mu, um, rp, ra, c3l[caso], descer)
        c2 = copy.deepcopy(dcfg)
        c2["dv"]["encontro_orbita_marte"]["valor"] = v(dcfg["dv"]["encontro_orbita_marte"]) + extra
        m, r, _ = dm.massa_leo(vs[var], c2, cu, dcfg["caso_base"]["carga_util"], margem, float(dcfg["caso_base"]["acrescimo_capsula"]))
        out[f"orbitador_{caso}"] = {"injetada_kg": r[1].massa_inicial, "leo_modelo_kg": m,
                                    "estagios": [_estagio(e, detalhe) for e in r]}
    out["lander"] = lander(rp, ra, dcfg, scfg, mcfg, plataforma_lander_kg, detalhe)
    return out, janelas, ref


def lander(rp, ra, dcfg=None, scfg=None, mcfg=None, plataforma_lander_kg=None, detalhe=False):
    """Lander do caso de base com o MAV subindo até a órbita de encontro rp × ra (raios, km). Usado por `veiculos` e
    pela comparação de propulsão do orbitador (Etapa 3.3), que muda a órbita de encontro."""
    dcfg = ler("config/dimensionamento.yaml") if dcfg is None else dcfg
    scfg = ler("config/superficie.yaml") if scfg is None else scfg
    mcfg = ler("config/mav_propulsao.yaml") if mcfg is None else mcfg
    icfg, po = ler("config/isru.yaml"), ler("config/parametros_orbitais.yaml")
    p = parametros()
    a_caso, _, _ = dm.casos(dcfg, p)
    mp = ler("results/etapa2.2/mav_propulsao.yaml")
    op_mav = mp["melhor_opcao"]
    fonte_mav = min((x for x in mp["opcoes"] if x["opcao"] == op_mav), key=lambda x: x["total_regra_iii_kg"])["energia"]
    R, mu = v(po["raio_marte_km"]), p.mu_marte
    margem = v(dcfg["margem_dv"])
    v_eq = 2 * np.pi * R / v(scfg["marte"]["periodo_rotacao_s"])
    dv = sf.dv_subida(mu, R, v(scfg["subida"]["dv_100x100_km_s"]), rp, ra, v_eq,
                      v(scfg["sitio_e_encontro"]["inclinacao_encontro_graus"]), v(scfg["sitio_e_encontro"]["latitude_sitio_graus"]))
    pous, cruz, _ = massas_opcao((1 + margem) * dv, op_mav, mcfg, scfg, icfg, fonte_mav)
    est_mav = [{"nome": e.nome, "isp_s": isp, "dv_km_s": d, "massa_inicial_kg": e.massa_inicial, "propelente_kg": e.propelente}
               for e, d, isp in mav_estagios((1 + margem) * dv, mcfg["opcoes"][op_mav], scfg)]
    plat = v(scfg["lander"]["plataforma_superficie_kg"]) if plataforma_lander_kg is None else plataforma_lander_kg
    chegada = (pous + plat) / v(scfg["lander"]["razao_pousada_entrada"]["entrada_direta"]) + cruz
    r = lander_estagios(chegada, scfg, dcfg, p, a_caso)
    out = {"injetada_kg": r[1].massa_inicial, "leo_modelo_kg": r[0].massa_inicial,
           "estagios": [_estagio(e, detalhe) for e in r],
           "massa_entrada_kg": chegada - cruz, "massa_pousada_kg": pous + plat, "mav_e_aquecimento_kg": pous,
           "plataforma_kg": plat, "paineis_cruzeiro_kg": cruz, "circuito_fluido_cruzeiro_kg": circuito_fluido(scfg)}
    if detalhe:
        out.update({"mav_opcao": op_mav, "mav_estagios": est_mav, "dv_subida_mav_km_s": dv})
    return out
