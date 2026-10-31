"""Etapa 4.3: comunicação. Conjunção solar na estada, distância Terra–espaçonave e tempo de luz, enlaces DSN e relé UHF.

- Ângulo Sol–Terra–Marte (SEP) por dia na estada da missão de referência (DE440, baricentro de Marte), e as janelas
  abaixo dos critérios com fonte (config/comunicacao.yaml): período de conjunção, sem telemetria, sem comando.
- Distância Terra–espaçonave e tempo de luz: estada (Marte) e arcos de ida e volta (Lambert da missão de referência).
- Folgas da superfície e do encontro em torno da conjunção: dias da chegada ao início da janela e do fim dela à partida.
- Enlace X do orbitador: taxa do análogo (MRO) escalada com 1/d² (P-064) na distância da estada; capacidade por dia.
- Enlace direto do lander (análogo MSL) e relé UHF: capacidade contra a demanda por sol (P-063); alcance do orbitador na
  órbita de encontro, do periapse ao apoapse, contra a órbita baixa do análogo.
Saída: results/etapa4.3/comunicacao.yaml e .md

Uso: python tools/comunicacao.py
"""

from __future__ import annotations

import datetime as dt
import math
import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital import ephemeris as eph  # noqa: E402
from orbital import kepler, lambert  # noqa: E402
from orbital import porkchop as pc  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402
from orbital.constantes import GM_SOL, UA_KM  # noqa: E402

SAIDA = RAIZ / "results" / "etapa4.3"


def sep_e_distancia(r_alvo_terra, r_sol_terra):
    """Ângulo Sol–Terra–alvo (graus) e distância Terra–alvo (km), a partir dos vetores com origem na Terra."""
    c = r_alvo_terra @ r_sol_terra / (np.linalg.norm(r_alvo_terra) * np.linalg.norm(r_sol_terra))
    return math.degrees(math.acos(max(-1.0, min(1.0, c)))), float(np.linalg.norm(r_alvo_terra))


def janelas(dias, limite):
    """Trechos contíguos de dias com SEP abaixo do limite: [(início, fim, n_dias)]."""
    out, ini = [], None
    for k, (d, s) in enumerate(dias):
        if s <= limite and ini is None:
            ini = d
        if ini is not None and (s > limite or k == len(dias) - 1):
            fim = d if s <= limite else dias[k - 1][0]
            out.append((ini, fim, (fim - ini).days + 1))
            ini = None
    return out


def perda_espaco_livre_db(r_km, f_mhz, c_km_s):
    """Perda de espaço livre (Friis): 20 log10(4π R f / c)."""
    return 20 * math.log10(4 * math.pi * r_km * f_mhz * 1e6 / c_km_s)


def taxa_uhf(r_km, rr, c_km_s):
    """Maior taxa da tabela de limiares do Electra que fecha o enlace com margem (kbps; 0 se nenhuma)."""
    p_rx = (10 * math.log10(v(rr["potencia_tx_w"]) * 1e3) + v(rr["ganhos_antenas_dbi"])
            - perda_espaco_livre_db(r_km, v(rr["frequencia_mhz"]), c_km_s))
    ok = [int(k) for k, lim in rr["limiares_dbm"]["tabela"].items() if p_rx >= lim + v(rr["margem_db"])]
    return max(ok) if ok else 0


def simula_rele(rr, mu, r_marte, rp, ra, arg_peri_graus, rot_graus_s, sol_s, c_km_s):
    """Passes do orbitador sobre o sítio: órbita kepleriana fixa no espaço (sem J2), Marte girando; volume por passe e por sol."""
    a, e = (rp + ra) / 2, (ra - rp) / (ra + rp)
    i, w = math.radians(v(rr["inclinacao_graus"])), math.radians(arg_peri_graus)
    n = math.sqrt(mu / a ** 3)
    lat, lon0 = math.radians(rr["sitio"]["latitude_graus"]), math.radians(rr["sitio"]["longitude_graus"])
    dt_s, t_fim = v(rr["passo_s"]), v(rr["sois_simulados"]) * sol_s
    passes, atual = [], None
    for k in range(int(t_fim / dt_s) + 1):
        t = k * dt_s
        M = (n * t) % (2 * math.pi)
        E = M
        for _ in range(30):
            E -= (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        nu = 2 * math.atan2(math.sqrt(1 + e) * math.sin(E / 2), math.sqrt(1 - e) * math.cos(E / 2))
        r = a * (1 - e * math.cos(E))
        u = w + nu   # argumento da latitude; nodo ascendente fixo em longitude inercial 0
        sat = np.array([r * math.cos(u), r * math.sin(u) * math.cos(i), r * math.sin(u) * math.sin(i)])
        th = lon0 + math.radians(rot_graus_s * t)
        nh = np.array([math.cos(lat) * math.cos(th), math.cos(lat) * math.sin(th), math.sin(lat)])
        d = sat - r_marte * nh
        rng = float(np.linalg.norm(d))
        el = math.degrees(math.asin(d @ nh / rng))
        if el >= v(rr["elevacao_min_graus"]):
            tx = taxa_uhf(rng, rr, c_km_s)
            if atual is None:
                atual = {"inicio_s": t, "duracao_s": 0.0, "fechado_s": 0.0, "mbit": 0.0, "alcance_min_km": rng, "alcance_max_km": rng}
            atual["duracao_s"] += dt_s
            atual["fechado_s"] += dt_s if tx > 0 else 0.0
            atual["mbit"] += tx * dt_s / 1e3
            atual["alcance_min_km"], atual["alcance_max_km"] = min(atual["alcance_min_km"], rng), max(atual["alcance_max_km"], rng)
        elif atual is not None:
            passes.append(atual)
            atual = None
    if atual is not None:
        passes.append(atual)
    sois = v(rr["sois_simulados"])
    uteis = [x for x in passes if x["mbit"] > 0]   # passes em que o enlace fecha em algum momento
    vol = [x["mbit"] for x in uteis]
    dur = [x["duracao_s"] for x in passes]
    return {"argumento_periapse_graus": arg_peri_graus, "passes": len(passes), "passes_por_sol": len(passes) / sois,
            "passes_uteis_por_sol": len(uteis) / sois, "tempo_com_enlace_por_sol_h": sum(x["fechado_s"] for x in passes) / sois / 3600,
            "mbit_por_sol_medio": sum(vol) / sois, "mbit_por_passe_medio": (sum(vol) / len(vol)) if vol else 0.0,
            "mbit_por_passe_max": max(vol) if vol else 0.0, "duracao_media_min": (sum(dur) / len(dur) / 60) if dur else 0.0,
            "tempo_visivel_por_sol_h": sum(dur) / sois / 3600, "alcance_min_km": min(x["alcance_min_km"] for x in passes) if passes else None,
            "alcance_max_km": max(x["alcance_max_km"] for x in passes) if passes else None}


def main():
    cc = ler("config/comunicacao.yaml")
    ms = ler("results/etapa1.3/missoes.yaml")
    ref = next(c for c in ms["candidatas"] if c["id"] == ler("config/missao_referencia.yaml")["missao_referencia"]["id"])
    c_km_s = v(cc["luz_km_s"])
    d0, d1 = (dt.date.fromisoformat(ref[k][:10]) for k in ("chegada_marte", "partida_marte"))

    # estada: Marte (baricentro) visto da Terra, um ponto por dia (meia-noite TDB)
    estada = []
    d = d0
    while d <= d1:
        s = d.isoformat() + "T00:00:00"
        rm, _ = eph.estado(eph.BARICENTRO_MARTE, s, eph.TERRA)
        rs, _ = eph.estado(eph.SOL, s, eph.TERRA)
        a, km = sep_e_distancia(rm, rs)
        estada.append({"data": d, "sep_graus": a, "distancia_km": km})
        d += dt.timedelta(days=1)
    minimo = min(estada, key=lambda x: x["sep_graus"])
    serie = [(x["data"], x["sep_graus"]) for x in estada]
    cj = cc["conjuncao"]
    crit = {k: v(cj[k]) for k in ("periodo_conjuncao_graus", "sem_telemetria_graus", "sem_comando_graus",
                                  "degradacao_banda_x_graus", "retorno_bpsk_ok_graus")}
    jan = {}
    for k, lim in crit.items():
        js = janelas(serie, lim)
        jan[k] = [{"inicio": str(a), "fim": str(b), "dias": n, "dias_desde_chegada": (a - d0).days,
                   "dias_ate_partida": (d1 - b).days} for a, b, n in js]

    # arcos de cruzeiro: espaçonave no arco de Lambert, vista da Terra
    def arco(partida, chegada, corpo_p, corpo_c, n=400):
        t1, t2 = eph.tdb_para_et(partida), eph.tdb_para_et(chegada)
        s1, s2 = pc.estado_corpo(corpo_p, t1), pc.estado_corpo(corpo_c, t2)
        v1 = lambert.resolver(GM_SOL, s1[:3], s2[:3], t2 - t1).v1
        pts = []
        for k in range(n + 1):
            tau = (t2 - t1) * k / n
            r = kepler.propagar(GM_SOL, s1[:3], v1, tau)[0]
            st = pc.estado_corpo(eph.TERRA, t1 + tau)
            with np.errstate(invalid="ignore"):   # nas pontas a espaçonave está na Terra
                pts.append(sep_e_distancia(r - st[:3], -st[:3]))
        # nas pontas a espaçonave está na Terra (ângulo indefinido): fora do mínimo
        return {"distancia_max_km": max(p[1] for p in pts), "sep_min_graus": min(p[0] for p in pts[1:-1] if p[1] > 1e6)}
    ida = arco(ref["partida_terra"], ref["chegada_marte"], eph.TERRA, eph.BARICENTRO_MARTE)
    volta = arco(ref["partida_marte"], ref["chegada_terra"], eph.BARICENTRO_MARTE, eph.TERRA)
    d_max_estada = max(x["distancia_km"] for x in estada)
    d_max = max(d_max_estada, ida["distancia_max_km"], volta["distancia_max_km"])
    distancias = {"estada_max_km": d_max_estada, "estada_min_km": min(x["distancia_km"] for x in estada),
                  "ida_max_km": ida["distancia_max_km"], "volta_max_km": volta["distancia_max_km"], "missao_max_km": d_max,
                  "missao_max_ua": d_max / UA_KM, "tempo_luz_max_min": d_max / c_km_s / 60,
                  "tempo_luz_min_estada_min": min(x["distancia_km"] for x in estada) / c_km_s / 60,
                  "referencia_mro_km": v(cc["orbitador_x"]["distancia_ref_km"])}

    # encontro: as fases do ERO [F121] cabem antes ou depois da janela de conjunção?
    en = cc["encontro"]
    dur_enc = int(v(en["ate_selagem_dias"]) + v(en["fase_raan_dias"]))
    pc5 = jan["periodo_conjuncao_graus"][0] if jan["periodo_conjuncao_graus"] else None
    rec = int(v(cj["dias_de_recuperacao"]))
    folgas = None
    if pc5:
        folgas = {"janela": pc5, "dias_recuperacao_depois": rec,
                  "dias_uteis_antes": pc5["dias_desde_chegada"], "dias_uteis_depois": pc5["dias_ate_partida"] - rec,
                  "encontro_dias": dur_enc}
        folgas["encontro_cabe_depois"] = folgas["dias_uteis_depois"] >= dur_enc
        folgas["folga_encontro_depois_dias"] = folgas["dias_uteis_depois"] - dur_enc

    # enlaces
    ox, lx, uh = cc["orbitador_x"], cc["lander_x"], cc["uhf"]
    p064 = next(p for p in ler("config/premissas.yaml")["premissas"] if p["id"] == "P-064")["valor"]["expoente"]
    taxa = lambda dkm: v(ox["taxa_ref_kbps"]) * (v(ox["distancia_ref_km"]) / dkm) ** p064  # noqa: E731
    horas = v(ox["horas_dsn_por_dia"])
    orb = {"taxa_na_distancia_max_kbps": taxa(d_max_estada), "taxa_na_distancia_min_estada_kbps": taxa(distancias["estada_min_km"]),
           "volume_por_passe_8h_na_distancia_max_mbit": taxa(d_max_estada) * horas * 3600 / 1e3,
           "comparacao_perto": {"taxa_escalada_kbps": taxa(ox["taxa_perto_mbps"]["distancia_km"]),
                                "publicada_mbps": [ox["taxa_perto_mbps"]["min"], ox["taxa_perto_mbps"]["max"]]}}
    demanda = v(uh["requisito_msl_por_sol_mbit"])
    # análogo do MSL: 160 bps na distância máxima dele (2,4 UA), escalado com a mesma P-064 até a distância máxima da estada
    taxa_dte = v(lx["taxa_max_distancia_bps"]) * (v(lx["distancia_ref_ua"]) * UA_KM / d_max_estada) ** p064
    h_dte = v(lx["horas_por_passe"])
    dte = {"taxa_ref_bps": v(lx["taxa_max_distancia_bps"]), "distancia_ref_ua": v(lx["distancia_ref_ua"]), "taxa_bps": taxa_dte,
           "horas_por_passe": h_dte, "volume_por_passe_mbit": taxa_dte * h_dte * 3600 / 1e6}
    dte["fracao_da_demanda"] = dte["volume_por_passe_mbit"] / demanda
    pl = ler("results/etapa2.3/plataformas.yaml")["orbita_encontro"]
    relé = {"periapse_alt_km": pl["periapse_alt_km"], "apoapse_alt_km": pl["apoapse_regra_5pct_km"],
            "perda_extra_no_apoapse_db": 20 * math.log10(pl["apoapse_regra_5pct_km"] / pl["periapse_alt_km"]),
            "demanda_por_sol_mbit": demanda, "msl_por_sol_mbit": [uh["volume_msl_por_sol_mbit"]["min"], uh["volume_msl_por_sol_mbit"]["max"]],
            "taxa_max_kbps": v(uh["taxa_max_kbps"])}
    # ---------------- comparação das saídas para a comunicação do lander (portão da 4.3)
    hc = cc["helicopteros"]
    mbit_voo = v(hc["imagens_por_voo_max"]) * hc["navcam_px"]["valor"][0] * hc["navcam_px"]["valor"][1] * v(hc["bits_por_pixel"]) / 1e6
    heli = {"mbit_por_voo_max": mbit_voo, "voos_por_sol": v(hc["voos_por_sol"]), "mbit_por_sol": mbit_voo * v(hc["voos_por_sol"]),
            "minutos_de_enlace_por_voo": mbit_voo * 1e3 / v(hc["enlace_kbps"]) / 60}
    demanda_total = demanda + heli["mbit_por_sol"]
    # (c) relé próprio: periapse sobre a latitude do sítio (melhor) e apoapse sobre ela (pior); P-067
    rr = cc["rele_proprio"]
    p = __import__("orbital.config", fromlist=["parametros"]).parametros()
    R = v(ler("config/parametros_orbitais.yaml")["raio_marte_km"])
    eph.carregar_kernels()
    import spiceypy as sp
    rot = sp.bodvrd("MARS", "PM", 3)[1][1] / 86400.0   # graus/s, pck00011
    sol_s = v(ler("config/plataformas.yaml")["lander"]["energia"]["duracao_sol_h"]) * 3600
    i_r, lat_r = math.radians(v(rr["inclinacao_graus"])), math.radians(rr["sitio"]["latitude_graus"])
    w_lat = math.degrees(math.asin(math.sin(lat_r) / math.sin(i_r)))   # periapse na latitude do sítio
    casos = [simula_rele(rr, p.mu_marte, R, R + pl["periapse_alt_km"], R + pl["apoapse_regra_5pct_km"], w, rot, sol_s, c_km_s)
             for w in (w_lat, w_lat + 180.0)]
    for x in casos:
        x["cobertura_demanda_lander"] = x["mbit_por_sol_medio"] / demanda
        x["cobertura_demanda_total"] = x["mbit_por_sol_medio"] / demanda_total
        x["energia_transmitindo_wh_sol"] = x["tempo_com_enlace_por_sol_h"] * v(rr["consumo_transmitindo_w"])
    # conferência do modelo de enlace: órbita baixa circular de referência (a do MRO, ~250 km [F177] p. 25)
    conf_baixa = taxa_uhf(250.0, rr, c_km_s)
    cb = rr["conferencia_orbita_baixa"]
    rr_b = dict(rr, inclinacao_graus=cb["inclinacao_graus"])
    hb = R + v(cb["altitude_km"])
    sim_b = simula_rele(rr_b, p.mu_marte, R, hb, hb, 0.0, rot, sol_s, c_km_s)
    conf_mro = {"mbit_por_passe_medio": sim_b["mbit_por_passe_medio"], "mbit_por_passe_max": sim_b["mbit_por_passe_max"],
                "mbit_por_sol_medio": sim_b["mbit_por_sol_medio"],
                "publicado_mbit_por_passe": [cb["publicado_mbit_por_passe"]["min"], cb["publicado_mbit_por_passe"]["max"]],
                "publicado_mbit_por_sol": [cb["publicado_mbit_por_sol"]["min"], cb["publicado_mbit_por_sol"]["max"]]}
    conf_mro["dentro_da_faixa_publicada"] = (conf_mro["publicado_mbit_por_passe"][0] <= conf_mro["mbit_por_passe_medio"] <= conf_mro["publicado_mbit_por_passe"][1]
                                             and conf_mro["publicado_mbit_por_sol"][0] <= conf_mro["mbit_por_sol_medio"] <= conf_mro["publicado_mbit_por_sol"][1])
    alcance_1024 = next(r for r in (x * 10.0 for x in range(1, 10000)) if taxa_uhf(r, rr, c_km_s) < 1024)   # km
    alcance_32 = next(r for r in (x * 10.0 for x in range(1, 100000)) if taxa_uhf(r, rr, c_km_s) < 32)
    # (b) DTE maior: ganho ∝ D², taxa ∝ P_RF (P-069); diâmetro para fechar a demanda num passe (P-065)
    dm = cc["dte_maior"]
    taxa_nec = demanda_total * 1e6 / (dte["horas_por_passe"] * 3600)
    fator = taxa_nec / dte["taxa_bps"]
    msl, mro = dm["msl"], dm["mro"]
    d_15w = msl["hga_m"] * math.sqrt(fator)
    d_100w = msl["hga_m"] * math.sqrt(fator / (mro["rf_w"] / msl["rf_w"]))
    dens = mro["refletor_kg"] / (math.pi * (mro["hga_m"] / 2) ** 2)
    massa_100w = dens * math.pi * (d_100w / 2) ** 2 + mro["gimbal_kg"] * (d_100w / mro["hga_m"]) ** 2 + mro["twta_kg"] + mro["epc_kg"]
    en_ = ler("results/etapa4.1/energia.yaml")["lander"]
    claro = next(x for x in en_["solar"] if x["cenario"] == "claro_jezero" and x["carga"] == "operação normal")
    e_dte = mro["twta_dc_w"] * dte["horas_por_passe"]
    area_op = claro["area_m2"] * (claro["demanda_wh_sol"] + e_dte) / claro["demanda_wh_sol"]
    dte_maior = {"taxa_necessaria_bps": taxa_nec, "fator_sobre_msl": fator, "fator_db": 10 * math.log10(fator),
                 "diametro_com_15w_m": d_15w, "diametro_com_100w_m": d_100w, "massa_com_100w_kg": massa_100w,
                 "massa_msl_kg": msl["hga_kg"] + msl["gimbal_kg"] + msl["sspa_kg"],
                 "energia_por_passe_wh": e_dte, "area_operacao_com_dte_m2": area_op,
                 "area_da_linha_de_base_m2": en_["variante_rhu"]["opcao"]["area_m2"]}
    comparacao = {"demanda_lander_mbit_sol": demanda, "helicopteros": heli, "demanda_total_mbit_sol": demanda_total,
                  "rele_proprio": casos, "conferencia_taxa_orbita_baixa_kbps": conf_baixa,
                  "alcance_max_1024_kbps_km": alcance_1024, "alcance_max_32_kbps_km": alcance_32,
                  "frequencia_mhz": v(rr["frequencia_mhz"]), "conferencia_orbita_baixa": conf_mro, "referencia_maven": rr["referencia_maven"],
                  "conferencia_tgo": rr["conferencia_tgo"], "dte_maior": dte_maior}

    out = {"gerado_por": "tools/comunicacao.py", "estada": [str(d0), str(d1)], "criterios_graus": crit,
           "sep_minimo": {"data": str(minimo["data"]), "graus": minimo["sep_graus"], "distancia_km": minimo["distancia_km"],
                          "dias_desde_chegada": (minimo["data"] - d0).days},
           "janelas": jan, "sep_min_cruzeiro_graus": {"ida": ida["sep_min_graus"], "volta": volta["sep_min_graus"]},
           "distancias": distancias, "folgas": folgas, "moratoria_2021": cj["moratoria_2021"],
           "proximidade": cj["proximidade_nao_afetada"], "orbitador_x": orb, "lander_dte": dte, "rele_uhf": relé,
           "comparacao": comparacao, "orbitadores_existentes": cc["orbitadores_existentes"]}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "comunicacao.yaml").write_text(yaml.safe_dump(nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    nomes = {"periodo_conjuncao_graus": "período de conjunção (MRO)", "sem_telemetria_graus": "sem depender de telemetria (MER)",
             "sem_comando_graus": "sem comandos (MER)", "degradacao_banda_x_graus": "degradação da banda X (MRO)",
             "retorno_bpsk_ok_graus": "abaixo do ângulo em que a DSN 810-005 106 cobre o retorno BPSK padrão"}
    sm, di, f = o["sep_minimo"], o["distancias"], o["folgas"]
    md = ["# Comunicação (gerado por tools/comunicacao.py)", "", "## Conjunção solar na estada", "",
          f"Estada {o['estada'][0]} a {o['estada'][1]}; amostragem diária à meia-noite TDB (datas com ±1 dia de resolução). Ângulo Sol–Terra–Marte mínimo: {br(sm['graus'], 2)}° em {sm['data']}, "
          f"{sm['dias_desde_chegada']} dias depois da chegada (distância {br(sm['distancia_km'] / 1e6, 1)} milhões de km).", "",
          "| Critério | SEP até | Início | Fim | Dias | Dias desde a chegada | Dias até a partida |", "| :- | -: | :- | :- | -: | -: | -: |"]
    for k, lim in o["criterios_graus"].items():
        for j in o["janelas"][k]:
            md.append(f"| {nomes[k]} | {br(lim, 1)}° | {j['inicio']} | {j['fim']} | {j['dias']} | {j['dias_desde_chegada']} | {j['dias_ate_partida']} |")
    md += ["", f"Moratória de comandos de referência: {o['moratoria_2021']}.", "", f"Relé de proximidade: {o['proximidade']}.", "",
           f"SEP mínimo nos arcos de cruzeiro: ida {br(o['sep_min_cruzeiro_graus']['ida'], 1)}°, volta {br(o['sep_min_cruzeiro_graus']['volta'], 1)}°.", "",
           "## Distância e tempo de luz", "",
           f"Distância Terra–espaçonave máxima: estada {br(di['estada_max_km'] / 1e6, 1)}, ida {br(di['ida_max_km'] / 1e6, 1)}, "
           f"volta {br(di['volta_max_km'] / 1e6, 1)} milhões de km; na missão, {br(di['missao_max_ua'], 3)} UA. "
           f"Tempo de luz (uma via): até {br(di['tempo_luz_max_min'], 1)} min; mínimo na estada {br(di['tempo_luz_min_estada_min'], 1)} min. "
           f"Referência do análogo (MRO): distância máxima de {br(di['referencia_mro_km'] / 1e6)} milhões de km [F173].", ""]
    if f:
        md += ["## Folgas em torno da conjunção (período de conjunção, SEP ≤ 5°)", "",
               f"Da chegada ao início da janela: {f['dias_uteis_antes']} dias. Do fim da janela à partida, menos {f['dias_recuperacao_depois']} dias "
               f"de recuperação dos dados [F176]: {f['dias_uteis_depois']} dias. As fases do encontro do ERO somam {f['encontro_dias']} dias "
               f"(da subida do MAV à selagem do contêiner, T0 + 22 d, mais a fase de RAAN, T0 + 46 d [F121]): {'cabem' if f['encontro_cabe_depois'] else 'não cabem'} depois da janela, "
               f"com folga de {f['folga_encontro_depois_dias']} dias.", ""]
    ox, dte, re_ = o["orbitador_x"], o["lander_dte"], o["rele_uhf"]
    md += ["## Enlaces", "",
           f"- Orbitador em banda X (análogo do MRO, 1/d², P-064): {br(ox['taxa_na_distancia_max_kbps'])} kbps na distância máxima da estada "
           f"e {br(ox['taxa_na_distancia_min_estada_kbps'])} kbps na mínima; {br(ox['volume_por_passe_8h_na_distancia_max_mbit'])} Mbit por passe de 8 h "
           f"na distância máxima. Conferência da escala: a 100 milhões de km ela dá {br(ox['comparacao_perto']['taxa_escalada_kbps'])} kbps, "
           f"contra {br(ox['comparacao_perto']['publicada_mbps'][0])} a {br(ox['comparacao_perto']['publicada_mbps'][1])} Mbps publicados [F173] "
           "(a escala superestima perto da Terra).",
           f"- Lander direto à Terra (análogo do MSL: {br(dte['taxa_ref_bps'])} bps a {br(dte['distancia_ref_ua'], 1)} UA [F137], mesma escala da P-064): "
           f"{br(dte['taxa_bps'])} bps na distância máxima da estada; {br(dte['volume_por_passe_mbit'], 1)} Mbit "
           f"num passe de {br(dte['horas_por_passe'])} h (P-065), {br(100 * dte['fracao_da_demanda'], 1)} % da demanda de {br(re_['demanda_por_sol_mbit'])} Mbit por sol (P-063).",
           f"- Relé UHF: até {br(re_['taxa_max_kbps'])} kbps [F137]; o MSL com orbitadores em órbita baixa tinha de {br(re_['msl_por_sol_mbit'][0])} "
           f"a {br(re_['msl_por_sol_mbit'][1])} Mbit por sol [F137]. A órbita de encontro vai de {br(re_['periapse_alt_km'])} a "
           f"{br(re_['apoapse_alt_km'])} km de altitude: no apoapse, {br(re_['perda_extra_no_apoapse_db'], 1)} dB a mais de perda de espaço "
           "livre que no periapse (só pela distância)."]
    cp, hc = o["comparacao"], o["comparacao"]["helicopteros"]
    md += ["", "## Comparação das saídas para a comunicação do lander", "",
           f"Demanda: lander {br(cp['demanda_lander_mbit_sol'])} Mbit/sol (P-063) + helicópteros {br(hc['mbit_por_sol'])} Mbit/sol "
           f"({br(hc['mbit_por_voo_max'])} Mbit por voo, {br(hc['voos_por_sol'])} voos/sol, P-068; {br(hc['minutos_de_enlace_por_voo'])} min de "
           f"enlace helicóptero–base por voo a 250 kbps [F180]) = {br(cp['demanda_total_mbit_sol'])} Mbit/sol.", "",
           "### (a) Orbitadores de relé existentes", "", "| Orbitador | Estado | Fonte |", "| :- | :- | :- |"]
    md += [f"| {x['orbitador']} | {x['estado']} | {x['fonte'].split(']')[0]}] |" for x in o["orbitadores_existentes"]]
    md += ["", "### (c) Relé pelo nosso orbitador na órbita de encontro (simulação dos passes, P-066 e P-067)", "",
           "| Caso | Passes por sol (com enlace) | Duração média (min) | Mbit por passe com enlace (médio / máximo) | Mbit por sol | Cobertura da demanda total | Energia transmitindo (Wh/sol) |",
           "| :- | -: | -: | -: | -: | -: | -: |"]
    for x, nome in zip(cp["rele_proprio"], ("periapse na latitude do sítio", "apoapse na latitude do sítio")):
        md.append(f"| {nome} | {br(x['passes_por_sol'], 2)} ({br(x['passes_uteis_por_sol'], 2)}) | {br(x['duracao_media_min'])} | {br(x['mbit_por_passe_medio'])} / {br(x['mbit_por_passe_max'])} | "
                  f"{br(x['mbit_por_sol_medio'])} | {br(100 * x['cobertura_demanda_total'])} % | {br(x['energia_transmitindo_wh_sol'])} |")
    md += ["", f"Perda de espaço livre por Friis a {br(cp['frequencia_mhz'], 1)} MHz. Com P-066, o enlace fecha a 1 024 kbps até "
           f"{br(cp['alcance_max_1024_kbps_km'])} km e a 32 kbps até {br(cp['alcance_max_32_kbps_km'])} km. Conferência: numa órbita baixa de 250 km "
           f"dá {br(cp['conferencia_taxa_orbita_baixa_kbps'])} kbps (o topo da tabela do Electra); referência publicada: {cp['conferencia_tgo']}. "
           "A energia conta o tempo em que o enlace fecha (envoltória). Órbita sem J2: o periapse migra ao longo dos 60 sóis, e os dois casos "
           "são extremos, não médias.", "",
           f"Comparação com dado publicado: o mesmo modelo numa órbita circular de 250 km [F177] dá {br(cp['conferencia_orbita_baixa']['mbit_por_passe_medio'])} Mbit "
           f"por passe em média (máximo {br(cp['conferencia_orbita_baixa']['mbit_por_passe_max'])}) e {br(cp['conferencia_orbita_baixa']['mbit_por_sol_medio'])} Mbit por sol, "
           f"contra {br(cp['conferencia_orbita_baixa']['publicado_mbit_por_passe'][0])} a {br(cp['conferencia_orbita_baixa']['publicado_mbit_por_passe'][1])} Mbit por passe e "
           f"{br(cp['conferencia_orbita_baixa']['publicado_mbit_por_sol'][0])} a {br(cp['conferencia_orbita_baixa']['publicado_mbit_por_sol'][1])} por sol do MRO com o MSL [F137]: "
           + ("dentro da faixa publicada." if cp["conferencia_orbita_baixa"]["dentro_da_faixa_publicada"] else "fora da faixa publicada."), "",
           f"Referência: {cp['referencia_maven']}.", "", "### (b) Enlace direto maior (P-069)", ""]
    dm = cp["dte_maior"]
    md += [f"Taxa necessária para a demanda total num passe de 8 h: {br(dm['taxa_necessaria_bps'])} bps, {br(dm['fator_sobre_msl'])} vezes o análogo "
           f"do MSL ({br(dm['fator_db'], 1)} dB). HGA de {br(dm['diametro_com_15w_m'], 2)} m com 15 W, ou de {br(dm['diametro_com_100w_m'], 2)} m com "
           f"o TWTA de 100 W do MRO; massa do conjunto com 100 W de cerca de {br(dm['massa_com_100w_kg'], 1)} kg, contra {br(dm['massa_msl_kg'], 1)} kg "
           f"do MSL; {br(dm['energia_por_passe_wh'])} Wh por passe. Área de operação com esse consumo: {br(dm['area_operacao_com_dte_m2'], 1)} m², "
           f"abaixo dos {br(dm['area_da_linha_de_base_m2'], 1)} m² da linha de base (a área continua dada pela sobrevivência). "
           "A escala vale com o mesmo erro de apontamento do MSL (5°); uma HGA desse tamanho tem feixe mais estreito e pede "
           "apontamento melhor. Na conjunção, o enlace direto também para."]
    (SAIDA / "comunicacao.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
