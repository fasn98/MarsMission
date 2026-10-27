"""Captura e saída de Marte em várias queimas no periapse (Etapa 3.1, portão de captura e retorno).

Física que manda na divisão: o excesso hiperbólico (v∞) só pode ser tirado (captura) ou dado (saída) numa única
passagem pelo periapse; uma queima que não captura deixa a nave escapar. Por isso a divisão (premissa P-042) é:
  - Captura em N queimas: a 1ª leva a hipérbole de v∞ a uma órbita alta, de apoapse ra_1 = f_H · raio de Hill (periapse de
    chegada livre, orbital.queima_finita.captura); as N−1 seguintes, no periapse, baixam o apoapse até o alvo em partes
    iguais de velocidade no periapse; o periapse que deriva nas queimas é corrigido no fim por um impulso no apoapse,
    contado na perda. N = 1 é a queima única direto ao alvo.
  - Saída em N queimas: as N−1 primeiras sobem o apoapse até ra_1 = f_H · raio de Hill, em partes iguais de velocidade no
    periapse; a última leva à hipérbole de v∞ (orbital.queima_finita.saida).
Cada queima é integrada com o mesmo modelo de orbital.queima_finita (empuxo tangente, massa variável).
A sequência leva, entre as queimas, um período de cada órbita intermediária (aproximação: os inícios das queimas
antes do periapse não são descontados). O apoapse intermediário é comparado com o raio de Hill de Marte.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import brentq, minimize_scalar

from orbital import manobras as mn
from orbital import queima_finita as qf
from orbital.foguete import G0


@dataclass(frozen=True)
class Sequencia:
    n: int
    viavel: bool
    motivo: str                       # "" se viável
    duracoes_s: list = field(default_factory=list)
    propelente_kg: float = float("nan")
    dv_motor_km_s: float = float("nan")    # soma das queimas + correção de periapse (captura)
    dv_impulsivo_km_s: float = float("nan")
    perda_km_s: float = float("nan")
    correcao_periapse_km_s: float = 0.0
    apoapses_intermediarios_km: list = field(default_factory=list)   # altitudes
    duracao_sequencia_dias: float = float("nan")
    altitude_minima_km: float = float("nan")
    apsides_finais_km: tuple = (float("nan"), float("nan"))   # altitudes (periapse, apoapse) ao fim, já com a correção


def raio_hill(mu_planeta, mu_sol, semieixo_km):
    """Raio de Hill: a · (μ_p / (3 μ_s))^(1/3)."""
    return semieixo_km * (mu_planeta / (3 * mu_sol)) ** (1 / 3)


def _ra_de_vp(mu, rp, vp):
    """Apoapse (raio) da órbita com periapse rp e velocidade vp no periapse; inf se não ligada."""
    energia = vp ** 2 / 2 - mu / rp
    if energia >= 0:
        return float("inf")
    return 2 * (-mu / (2 * energia)) - rp


def _periodo_s(mu, rp, ra):
    a = (rp + ra) / 2
    return 2 * math.pi * math.sqrt(a ** 3 / mu)


def queima_apoapse(mu, raio, motor, m0, rp, ra, ra_alvo, sentido):
    """Uma queima no periapse da órbita (rp, ra) que leva o apoapse a ra_alvo (sentido −1 baixa, +1 sobe); o início
    minimiza o propelente. Devolve (r_final, v_final, m_final, duração, raio mínimo)."""
    dv_imp = abs(float(mn.v_orbita(mu, rp, rp, ra_alvo)) - float(mn.v_orbita(mu, rp, rp, ra)))
    t_imp = qf.tempo_de_queima_s(motor, m0, dv_imp)
    vp = float(mn.v_orbita(mu, rp, rp, ra))

    def g(d, r, v):
        rf, vf, _, _ = qf.queimar(mu, motor, r, v, m0, d, sentido)
        _, raf, _ = qf.elementos(mu, rf, vf)
        raf = 1e12 if not np.isfinite(raf) else raf
        return (raf - ra_alvo) / ra_alvo

    def duracao(f):
        r, v = qf._estado(mu, rp, vp, f * t_imp)
        lo, hi = 0.3 * t_imp, 1.05 * t_imp
        while g(hi, r, v) * sentido < 0:   # ainda não chegou ao alvo
            hi *= 1.5
            if hi > qf._OT["saida_duracao_max"] * t_imp:
                raise RuntimeError("queima de apoapse não atinge o alvo")
        return brentq(lambda d: g(d, r, v), lo, hi, xtol=qf._OT["saida_brentq"]["xtol_s"],
                      rtol=qf._OT["saida_brentq"]["rtol"]), r, v

    lim = qf._OT["saida_limites_inicio"]
    opt = minimize_scalar(lambda f: duracao(f)[0], bounds=tuple(lim), method="bounded", options={"xatol": qf._OT["xatol_inicio"]})
    d, r, v = duracao(opt.x)
    rf, vf, mf, rmin = qf.queimar(mu, motor, r, v, m0, d, sentido, raio_minimo=True)
    return rf, vf, mf, d, rmin


def _apoapses_iguais(mu, rp, ra_ini, ra_fim, n):
    """n apoapses entre ra_ini e ra_fim (o último é ra_fim), em passos iguais de velocidade no periapse."""
    v0, v1 = float(mn.v_orbita(mu, rp, rp, ra_ini)), float(mn.v_orbita(mu, rp, rp, ra_fim))
    return [_ra_de_vp(mu, rp, v0 + k * (v1 - v0) / n) for k in range(1, n + 1)]


def captura_multipla(mu, raio, motor, m0, vinf, rp_alvo, ra_alvo, n, r_hill, f_hill):
    """Captura em n queimas no periapse (ver o docstring do módulo)."""
    dv_imp = float(mn.dv_hiperbole_orbita(mu, vinf, rp_alvo, ra_alvo))
    if n == 1:
        r = qf.captura(mu, raio, motor, m0, vinf, rp_alvo, ra_alvo)
        return Sequencia(1, True, "", [r.duracao_s], r.propelente_kg, r.dv_motor_km_s, dv_imp, r.perda_km_s, 0.0, [], 0.0,
                         r.altitude_minima_km)
    ra1 = f_hill * r_hill
    if ra1 <= ra_alvo:
        return Sequencia(n, False, "órbita de captura (f_H · raio de Hill) abaixo do apoapse-alvo", dv_impulsivo_km_s=dv_imp)
    ras = [ra1] + _apoapses_iguais(mu, rp_alvo, ra1, ra_alvo, n - 1)
    r1 = qf.captura(mu, raio, motor, m0, vinf, rp_alvo, ra1)
    m, duracoes, hmin = m0 - r1.propelente_kg, [r1.duracao_s], r1.altitude_minima_km
    rp_c, ra_c = r1.rp_final_km + raio, r1.ra_final_km + raio
    espera = 0.0
    for ra_k in ras[1:]:
        espera += _periodo_s(mu, rp_c, ra_c)
        rf, vf, mf, d, rmin = queima_apoapse(mu, raio, motor, m, rp_c, ra_c, ra_k, -1)
        rp_c, ra_c, _ = qf.elementos(mu, rf, vf)
        m, hmin = mf, min(hmin, rmin - raio)
        duracoes.append(d)
    # periapse que derivou nas queimas: impulso no apoapse para voltar a rp_alvo (mesmo apoapse)
    corr = abs(float(mn.v_orbita(mu, ra_c, rp_alvo, ra_c)) - float(mn.v_orbita(mu, ra_c, rp_c, ra_c)))
    m_fim = m * math.exp(-corr / (motor.isp_s * G0))
    dv_mot = motor.isp_s * G0 * math.log(m0 / m_fim)
    return Sequencia(n, True, "", duracoes, m0 - m_fim, dv_mot, dv_imp, dv_mot - dv_imp, corr,
                     [x - raio for x in ras[:-1]], espera / 86400, hmin, (rp_alvo - raio, ra_c - raio))


def saida_multipla(mu, raio, motor, m0, rp, ra, vinf, n, r_hill, f_hill):
    """Saída em n queimas no periapse (ver o docstring do módulo)."""
    dv_imp = float(mn.dv_hiperbole_orbita(mu, vinf, rp, ra))
    if n == 1:
        r = qf.saida(mu, raio, motor, m0, rp, ra, vinf)
        return Sequencia(1, True, "", [r.duracao_s], r.propelente_kg, r.dv_motor_km_s, dv_imp, r.perda_km_s, 0.0, [], 0.0,
                         r.altitude_minima_km)
    ra1 = f_hill * r_hill
    if ra1 <= ra:
        return Sequencia(n, False, "órbita alta (f_H · raio de Hill) abaixo do apoapse inicial", dv_impulsivo_km_s=dv_imp)
    ras = _apoapses_iguais(mu, rp, ra, ra1, n - 1)
    m, duracoes, hmin, espera = m0, [], float("inf"), 0.0
    rp_c, ra_c = rp, ra
    for ra_k in ras:
        rf, vf, mf, d, rmin = queima_apoapse(mu, raio, motor, m, rp_c, ra_c, ra_k, +1)
        rp_c, ra_c, _ = qf.elementos(mu, rf, vf)
        espera += _periodo_s(mu, rp_c, ra_c)
        m, hmin = mf, min(hmin, rmin - raio)
        duracoes.append(d)
    rN = qf.saida(mu, raio, motor, m, rp_c, ra_c, vinf)
    duracoes.append(rN.duracao_s)
    m_fim = m - rN.propelente_kg
    dv_mot = motor.isp_s * G0 * math.log(m0 / m_fim)
    return Sequencia(n, True, "", duracoes, m0 - m_fim, dv_mot, dv_imp, dv_mot - dv_imp, 0.0,
                     [x - raio for x in ras], espera / 86400, min(hmin, rN.altitude_minima_km))
