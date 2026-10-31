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
        if s < limite and ini is None:
            ini = d
        if ini is not None and (s >= limite or k == len(dias) - 1):
            fim = d if s < limite else dias[k - 1][0]
            out.append((ini, fim, (fim - ini).days + 1))
            ini = None
    return out


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
    dur_enc = int(v(en["captura_dias"]) + v(en["fase_raan_dias"]))
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
    taxa = lambda dkm: v(ox["taxa_ref_kbps"]) * (v(ox["distancia_ref_km"]) / dkm) ** 2  # noqa: E731  (P-064)
    horas = v(ox["horas_dsn_por_dia"])
    orb = {"taxa_na_distancia_max_kbps": taxa(d_max_estada), "taxa_na_distancia_min_estada_kbps": taxa(distancias["estada_min_km"]),
           "volume_por_dia_na_distancia_max_mbit": taxa(d_max_estada) * horas * 3600 / 1e3,
           "comparacao_perto": {"taxa_escalada_kbps": taxa(ox["taxa_perto_mbps"]["distancia_km"]),
                                "publicada_mbps": [ox["taxa_perto_mbps"]["min"], ox["taxa_perto_mbps"]["max"]]}}
    demanda = v(uh["requisito_msl_por_sol_mbit"])
    dte = {"taxa_bps": v(lx["taxa_max_distancia_bps"]), "volume_por_passe_mbit": v(lx["taxa_max_distancia_bps"]) * horas * 3600 / 1e6}
    dte["fracao_da_demanda"] = dte["volume_por_passe_mbit"] / demanda
    pl = ler("results/etapa2.3/plataformas.yaml")["orbita_encontro"]
    relé = {"periapse_alt_km": pl["periapse_alt_km"], "apoapse_alt_km": pl["apoapse_regra_5pct_km"],
            "perda_extra_no_apoapse_db": 20 * math.log10(pl["apoapse_regra_5pct_km"] / pl["periapse_alt_km"]),
            "demanda_por_sol_mbit": demanda, "msl_por_sol_mbit": [uh["volume_msl_por_sol_mbit"]["min"], uh["volume_msl_por_sol_mbit"]["max"]],
            "taxa_max_kbps": v(uh["taxa_max_kbps"])}
    out = {"gerado_por": "tools/comunicacao.py", "estada": [str(d0), str(d1)], "criterios_graus": crit,
           "sep_minimo": {"data": str(minimo["data"]), "graus": minimo["sep_graus"], "distancia_km": minimo["distancia_km"],
                          "dias_desde_chegada": (minimo["data"] - d0).days},
           "janelas": jan, "sep_min_cruzeiro_graus": {"ida": ida["sep_min_graus"], "volta": volta["sep_min_graus"]},
           "distancias": distancias, "folgas": folgas, "moratoria_2021": cj["moratoria_2021"],
           "proximidade": cj["proximidade_nao_afetada"], "orbitador_x": orb, "lander_dte": dte, "rele_uhf": relé}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "comunicacao.yaml").write_text(yaml.safe_dump(nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    nomes = {"periodo_conjuncao_graus": "período de conjunção (MRO)", "sem_telemetria_graus": "sem depender de telemetria (MER)",
             "sem_comando_graus": "sem comandos (MER)", "degradacao_banda_x_graus": "degradação da banda X (MRO)",
             "retorno_bpsk_ok_graus": "retorno BPSK padrão garantido (DSN 810-005 106)"}
    sm, di, f = o["sep_minimo"], o["distancias"], o["folgas"]
    md = ["# Comunicação (gerado por tools/comunicacao.py)", "", "## Conjunção solar na estada", "",
          f"Estada {o['estada'][0]} a {o['estada'][1]}. Ângulo Sol–Terra–Marte mínimo: {br(sm['graus'], 2)}° em {sm['data']}, "
          f"{sm['dias_desde_chegada']} dias depois da chegada (distância {br(sm['distancia_km'] / 1e6, 1)} milhões de km).", "",
          "| Critério | SEP abaixo de | Início | Fim | Dias | Dias desde a chegada | Dias até a partida |", "| :- | -: | :- | :- | -: | -: | -: |"]
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
               f"(captura e fase de RAAN [F121]): {'cabem' if f['encontro_cabe_depois'] else 'não cabem'} depois da janela, "
               f"com folga de {f['folga_encontro_depois_dias']} dias.", ""]
    ox, dte, re_ = o["orbitador_x"], o["lander_dte"], o["rele_uhf"]
    md += ["## Enlaces", "",
           f"- Orbitador em banda X (análogo do MRO, 1/d², P-064): {br(ox['taxa_na_distancia_max_kbps'])} kbps na distância máxima da estada "
           f"e {br(ox['taxa_na_distancia_min_estada_kbps'])} kbps na mínima; {br(ox['volume_por_dia_na_distancia_max_mbit'])} Mbit por passe de 8 h "
           f"na distância máxima. Conferência da escala: a 100 milhões de km ela dá {br(ox['comparacao_perto']['taxa_escalada_kbps'])} kbps, "
           f"contra {br(ox['comparacao_perto']['publicada_mbps'][0])} a {br(ox['comparacao_perto']['publicada_mbps'][1])} Mbps publicados [F173] "
           "(a escala superestima perto da Terra).",
           f"- Lander direto à Terra (análogo do MSL): {br(dte['taxa_bps'])} bps na distância máxima; {br(dte['volume_por_passe_mbit'], 1)} Mbit "
           f"num passe de 8 h, {br(100 * dte['fracao_da_demanda'], 1)} % da demanda de {br(re_['demanda_por_sol_mbit'])} Mbit por sol (P-063).",
           f"- Relé UHF: até {br(re_['taxa_max_kbps'])} kbps [F137]; o MSL com orbitadores em órbita baixa tinha de {br(re_['msl_por_sol_mbit'][0])} "
           f"a {br(re_['msl_por_sol_mbit'][1])} Mbit por sol [F137]. A órbita de encontro vai de {br(re_['periapse_alt_km'])} a "
           f"{br(re_['apoapse_alt_km'])} km de altitude: no apoapse, {br(re_['perda_extra_no_apoapse_db'], 1)} dB a mais de perda de espaço "
           "livre que no periapse (só pela distância, sem a geometria do passe)."]
    (SAIDA / "comunicacao.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
