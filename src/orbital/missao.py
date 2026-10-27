"""Missões completas Terra→Marte→Terra por combinação de grades de transferência.

Usa só o código verificado na Etapa 1.2 (orbital.porkchop / orbital.lambert) para as grades e
orbital.manobras para os Δv. Uma missão é (partida da Terra, chegada a Marte, partida de Marte,
chegada à Terra), com as duas datas em Marte no mesmo eixo de datas para que as grades de ida e
de volta se encaixem.

Custo de cada missão (Δv propulsivo, km/s):
  injeção trans-Marte a partir da órbita baixa terrestre
  + captura em Marte (propulsiva, ou elevação de periapse após aerocaptura)
  + injeção trans-Terra a partir da órbita marciana
A chegada à Terra é por reentrada direta: não há Δv, só a velocidade na interface é reportada.

Busca: para cada par (chegada a Marte a, partida de Marte d) com permanência d − a dentro da
faixa da classe, minimiza o custo sobre a data de partida da Terra e a de chegada à Terra,
respeitando a duração total máxima da classe. Resolução = passo da grade, sem refinamento
contínuo.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import spiceypy as spice

from orbital import manobras as mn
from orbital import porkchop as pc

DIA = pc.DIA


@dataclass(frozen=True)
class Orbita:
    """Órbita de estacionamento: periapse e apoapse (km, a partir do centro)."""
    rp: float
    ra: float


@dataclass(frozen=True)
class Parametros:
    mu_terra: float
    mu_marte: float
    leo: Orbita                  # órbita baixa terrestre (circular: rp = ra)
    orbitas_marte: dict          # nome -> Orbita
    rp_aerocaptura_marte: float  # raio do periapse na passagem atmosférica
    r_interface_terra: float     # raio da interface de reentrada
    exclusao_180: float          # premissa P-006
    v_reentrada_max: float = np.inf  # limite de velocidade de reentrada (km/s), premissa P-011


def custo_saida_terra(p: Parametros, c3):
    return mn.dv_hiperbole_orbita(p.mu_terra, np.sqrt(c3), p.leo.rp, p.leo.ra)


def custo_captura_marte(p: Parametros, vinf, orbita: str, aerocaptura: bool):
    o = p.orbitas_marte[orbita]
    if aerocaptura:
        return np.full_like(np.asarray(vinf, dtype=float),
                            mn.dv_captura_aerocaptura(p.mu_marte, p.rp_aerocaptura_marte, o.rp, o.ra))
    return mn.dv_hiperbole_orbita(p.mu_marte, vinf, o.rp, o.ra)


def custo_saida_marte(p: Parametros, c3l, orbita: str):
    o = p.orbitas_marte[orbita]
    return mn.dv_hiperbole_orbita(p.mu_marte, np.sqrt(c3l), o.rp, o.ra)


def _mascara_180(grade: pc.Grade, excl: float):
    a = np.nan_to_num(grade.angulo_transf, nan=180.0)
    return (np.abs(a - 180.0) <= excl) | ~np.isfinite(grade.c3)


def melhor_combinacao(p: Parametros, ida: pc.Grade, volta: pc.Grade, permanencia_dias, duracao_max_dias,
                      orbita: str, aerocaptura: bool, tof_max_dias: float = np.inf):
    """Melhor missão (menor Δv propulsivo) para uma classe. Devolve índices e custo, ou None.

    `tof_max_dias` limita o tempo de voo de cada trecho (ida e volta). Retornos com velocidade
    na interface de reentrada acima de `p.v_reentrada_max` são excluídos.

    `ida.et_chegada` e `volta.et_partida` precisam ser o mesmo eixo de datas em Marte.
    """
    assert np.array_equal(ida.et_chegada, volta.et_partida), "eixos de datas em Marte diferentes"
    custo_ida = custo_saida_terra(p, ida.c3) + custo_captura_marte(p, ida.vinf_chegada, orbita, aerocaptura)
    custo_ida = np.where(_mascara_180(ida, p.exclusao_180) | (ida.tof_dias > tof_max_dias), np.inf, custo_ida)
    custo_volta = custo_saida_marte(p, volta.c3, orbita)
    v_ei = mn.velocidade_reentrada(p.mu_terra, volta.vinf_chegada, p.r_interface_terra)
    excede = np.nan_to_num(v_ei, nan=np.inf) > p.v_reentrada_max
    custo_volta = np.where(_mascara_180(volta, p.exclusao_180) | (volta.tof_dias > tof_max_dias) | excede,
                           np.inf, custo_volta)

    # Mínimo cumulativo da volta ao longo da data de chegada à Terra (para limitar a duração).
    cum = np.minimum.accumulate(custo_volta, axis=1)
    arg = np.zeros_like(custo_volta, dtype=int)
    for k in range(custo_volta.shape[1]):
        arg[:, k] = np.where(custo_volta[:, k] <= cum[:, k], k, arg[:, k - 1] if k else 0)

    et_dep, et_M, et_arr = ida.et_partida, ida.et_chegada, volta.et_chegada
    lim = et_dep + duracao_max_dias * DIA                       # chegada à Terra máxima por partida
    k_lim = np.searchsorted(et_arr, lim, side="right") - 1      # (n_dep,)
    smin, smax = permanencia_dias
    melhor = (np.inf, None)
    for a in range(len(et_M)):
        ds = np.where((et_M - et_M[a] >= smin * DIA) & (et_M - et_M[a] <= smax * DIA))[0]
        if ds.size == 0 or not np.isfinite(custo_ida[:, a]).any():
            continue
        valido = k_lim >= 0
        for d in ds:
            ret = np.where(valido, cum[d, np.clip(k_lim, 0, None)], np.inf)
            total = custo_ida[:, a] + ret
            i = int(np.argmin(total))
            if total[i] < melhor[0]:
                melhor = (float(total[i]), (i, a, int(d), int(arg[d, k_lim[i]])))
    return None if melhor[1] is None else melhor


def detalhar(p: Parametros, et_dep, et_M1, et_M2, et_arr):
    """Linha completa da missão, recalculada nas datas escolhidas com orbital.porkchop."""
    from orbital import ephemeris as eph

    c3, vinf_m, ang1, vinf1 = pc.transferencia(eph.TERRA, eph.BARICENTRO_MARTE, et_dep, et_M1)
    c3l, vinf_t, ang2, _ = pc.transferencia(eph.BARICENTRO_MARTE, eph.TERRA, et_M2, et_arr)
    rot = np.array(spice.pxform(pc.FRAME, "J2000", et_dep))
    linha = {
        "partida_terra": spice.et2utc(et_dep, "ISOC", 0)[:10],
        "chegada_marte": spice.et2utc(et_M1, "ISOC", 0)[:10],
        "partida_marte": spice.et2utc(et_M2, "ISOC", 0)[:10],
        "chegada_terra": spice.et2utc(et_arr, "ISOC", 0)[:10],
        "ida_dias": (et_M1 - et_dep) / DIA, "em_marte_dias": (et_M2 - et_M1) / DIA,
        "volta_dias": (et_arr - et_M2) / DIA, "total_dias": (et_arr - et_dep) / DIA,
        "c3_km2_s2": c3, "dla_graus": mn.declinacao_graus(rot @ vinf1),
        "angulo_ida_graus": ang1, "angulo_volta_graus": ang2,
        "vinf_chegada_marte_km_s": vinf_m, "c3l_partida_marte_km2_s2": c3l,
        "vinf_chegada_terra_km_s": vinf_t,
        "v_reentrada_km_s": float(mn.velocidade_reentrada(p.mu_terra, vinf_t, p.r_interface_terra)),
        "dv_saida_terra_km_s": float(custo_saida_terra(p, c3)),
        "por_orbita_marte": {},
    }
    for nome in p.orbitas_marte:
        cap_p = float(custo_captura_marte(p, vinf_m, nome, False))
        cap_a = float(custo_captura_marte(p, vinf_m, nome, True))
        sai = float(custo_saida_marte(p, c3l, nome))
        linha["por_orbita_marte"][nome] = {
            "dv_captura_propulsiva_km_s": cap_p, "dv_captura_aerocaptura_km_s": cap_a,
            "dv_saida_marte_km_s": sai,
            "dv_total_sem_aerocaptura_km_s": linha["dv_saida_terra_km_s"] + cap_p + sai,
            "dv_total_com_aerocaptura_km_s": linha["dv_saida_terra_km_s"] + cap_a + sai,
        }
    return linha


def envelope_dimensionamento(candidatas, janelas, classes, orbita: str, captura: str):
    """Envelope de Δv (ADR 0004): para cada janela, o menor Δv entre as candidatas admissíveis das
    classes dadas; o envelope é o maior desses mínimos. Devolve (valor, id que define, mínimos por janela).

    As candidatas já respeitam as restrições aplicadas na busca (p. ex. limite de reentrada).
    """
    chave = "dv_total_sem_aerocaptura_km_s" if captura == "propulsiva" else "dv_total_com_aerocaptura_km_s"
    minimos = {}
    for j in janelas:
        cs = [c for c in candidatas if c["janela_ida"] == j and c["classe"] in classes]
        if cs:
            m = min(cs, key=lambda c: c["por_orbita_marte"][orbita][chave])
            minimos[j] = (m["id"], float(m["por_orbita_marte"][orbita][chave]))
    j_pior = max(minimos, key=lambda j: minimos[j][1])
    return minimos[j_pior][1], minimos[j_pior][0], minimos
