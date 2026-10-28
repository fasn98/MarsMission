"""Geometria das assíntotas em Marte (Etapa 3.3): declinação do v∞ de chegada e de partida no equador de Marte.

Uma órbita de inclinação i (em relação ao equador de Marte) só contém a assíntota de declinação δ se i ≥ |δ|
(e i ≤ 180° − |δ|). Se a captura e a partida puderem ser feitas na inclinação da órbita de encontro, as espirais de
baixo empuxo ficam coplanares (ADR 0012, item 2). Frame IAU_MARS do pck00011.tpc [F17] (IAU WGCCRE 2015).
A orientação do nodo na partida (que depende da precessão da órbita durante a estada) não é tratada aqui.
"""

from __future__ import annotations

import math

import numpy as np
import spiceypy as spice

from orbital import ephemeris as eph
from orbital import lambert
from orbital import porkchop as pc
from orbital.constantes import GM_SOL


def declinacao_marte_graus(vetor_j2000, et):
    """Declinação (graus) de um vetor dado no J2000, no frame equatorial IAU_MARS na época et."""
    w = np.array(spice.pxform("J2000", "IAU_MARS", et)) @ np.asarray(vetor_j2000, dtype=float)
    return math.degrees(math.asin(w[2] / np.linalg.norm(w)))


def vinf_marte(missao):
    """(v∞ de chegada, v∞ de partida) em Marte, vetores J2000 (km/s), e as épocas (et) de chegada e de partida, pelo
    Lambert de 0 revoluções entre as datas da missão (as mesmas de results/etapa1.3)."""
    eph.carregar_kernels()
    t = [eph.tdb_para_et(missao[k]) for k in ("partida_terra", "chegada_marte", "partida_marte", "chegada_terra")]
    s1, s2 = pc.estado_corpo(eph.TERRA, t[0]), pc.estado_corpo(eph.BARICENTRO_MARTE, t[1])
    s3, s4 = pc.estado_corpo(eph.BARICENTRO_MARTE, t[2]), pc.estado_corpo(eph.TERRA, t[3])
    va = lambert.resolver(GM_SOL, s1[:3], s2[:3], t[1] - t[0]).v2 - s2[3:]
    vd = lambert.resolver(GM_SOL, s3[:3], s4[:3], t[3] - t[2]).v1 - s3[3:]
    return va, vd, t[1], t[2]


def mudanca_de_plano_kms(v_kms, delta_i_graus):
    """Δv de uma mudança de plano impulsiva de delta_i com velocidade v: 2 v sen(Δi/2)."""
    return 2 * v_kms * math.sin(math.radians(delta_i_graus) / 2)
