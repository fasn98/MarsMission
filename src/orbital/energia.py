"""Energia (Etapa 4.1): geometria solar em Marte, energia de painel na superfície, MMRTG e bateria.

Geometria (SPICE, DE440 + pck00011): longitude solar areocêntrica Ls (lspcn), declinação do Sol = latitude do ponto
subsolar (subslr) e distância Marte–Sol. Insolação diária no topo da atmosfera numa superfície horizontal à latitude φ:
    Q = S/r² · (T_sol/π) · (h0 sen φ sen δ + cos φ cos δ sen h0),  cos h0 = −tg φ tg δ   (Wh/m² por sol)
(fórmula da geometria esférica, derivada aqui; S a 1 UA e T_sol do config).

Insolação diária global numa superfície horizontal (Appelbaum & Landis, NASA TM-105216 [F130]): integral, do nascer ao
pôr do Sol, de G_h = G_ob cos z f(z,τ,al)/(1 − al), com f pelo ajuste polinomial da Eq. (20) (coeficientes no config).

Energia do painel horizontal na superfície, calibrado no 1º sol do InSight:
    E = A · H_h(φ, data, τ) · η · (1 − p)^n,   η = E_ref / (A_ref · H_h,ref)
com (1 − p)^n a poeira acumulada nos painéis depois de n sóis (Lorenz et al. 2020).
"""

from __future__ import annotations

import math

import numpy as np
import spiceypy as spice

from orbital import ephemeris as eph
from orbital.constantes import UA_KM


def geometria_marte(tdb_iso):
    """(Ls [graus], declinação do Sol [graus], distância Marte–Sol [UA]) na data (TDB).

    O de440s só traz o baricentro de Marte (a diferença para o centro do planeta é desprezível aqui). Declinação:
    asen(ŝ·p), com ŝ a direção Marte→Sol e p o polo de Marte (IAU_MARS). Ls: longitude do Sol no plano da órbita a
    partir do equinócio vernal de Marte, direção p × h (h = normal da órbita)."""
    eph.carregar_kernels()
    et = eph.tdb_para_et(tdb_iso)
    st, _ = spice.spkezr(eph.BARICENTRO_MARTE, et, "J2000", "NONE", eph.SOL)
    r, v = np.array(st[:3]), np.array(st[3:])
    s = -r / np.linalg.norm(r)                                   # Marte → Sol
    p = np.array(spice.pxform("IAU_MARS", "J2000", et))[:, 2]    # polo de Marte no J2000
    h = np.cross(r, v)
    h /= np.linalg.norm(h)
    x = np.cross(p, h)
    x /= np.linalg.norm(x)
    y = np.cross(h, x)
    ls = math.degrees(math.atan2(s @ y, s @ x))
    return ls % 360.0, math.degrees(math.asin(s @ p)), float(np.linalg.norm(r)) / UA_KM


def insolacao_topo(lat_graus, dec_graus, dist_ua, s_1ua, horas_sol):
    """Insolação diária no topo da atmosfera, superfície horizontal (Wh/m² por sol)."""
    phi, d = math.radians(lat_graus), math.radians(dec_graus)
    x = -math.tan(phi) * math.tan(d)
    h0 = math.pi if x <= -1 else 0.0 if x >= 1 else math.acos(x)
    return s_1ua / dist_ua ** 2 * horas_sol / math.pi * (h0 * math.sin(phi) * math.sin(d) + math.cos(phi) * math.cos(d) * math.sin(h0))


def fluxo_liquido_normalizado(z_graus, tau, albedo, k0, k1):
    """f(z, τ, al) pela Eq. (20) de [F130]: [Σ p(i,j,k) τ^i (z/100)^j al^k] (1 − al); k0 e k1 em linhas j, colunas i."""
    s = 0.0
    for k, tab in ((0, k0), (1, k1)):
        for j, linha in enumerate(tab):
            for i, p in enumerate(linha):
                s += p * tau ** i * (z_graus / 100.0) ** j * albedo ** k
    return s * (1.0 - albedo)


def insolacao_superficie(lat_graus, dec_graus, dist_ua, s_1ua, horas_sol, tau, albedo, k0, k1, z_max_graus, n=400):
    """Insolação diária global numa superfície horizontal (Wh/m² por sol): integral de G_h no ângulo horário, com z
    limitado a z_max (limite das tabelas da fonte) no cálculo de f."""
    phi, d = math.radians(lat_graus), math.radians(dec_graus)
    x = -math.tan(phi) * math.tan(d)
    if x >= 1:
        return 0.0
    h0 = math.pi if x <= -1 else math.acos(x)
    g_ob = s_1ua / dist_ua ** 2
    hs = np.linspace(-h0, h0, n + 1)
    cz = math.sin(phi) * math.sin(d) + math.cos(phi) * math.cos(d) * np.cos(hs)
    cz = np.clip(cz, 0.0, 1.0)
    z = np.minimum(np.degrees(np.arccos(cz)), z_max_graus)
    g = np.array([g_ob * c * fluxo_liquido_normalizado(zz, tau, albedo, k0, k1) / (1.0 - albedo) for c, zz in zip(cz, z)])
    return float(np.trapezoid(g, hs)) * horas_sol / (2 * math.pi)


def energia_painel(area_m2, h_h, eta, perda_por_sol, sois_de_poeira):
    """Energia de um sol (Wh) do painel horizontal: área × insolação na superfície × η × poeira acumulada."""
    return area_m2 * h_h * eta * (1.0 - perda_por_sol) ** sois_de_poeira


def potencia_mmrtg(p_inicio_w, degradacao_anual, anos):
    """Potência elétrica do MMRTG depois de `anos` (degradação composta)."""
    return p_inicio_w * (1.0 - degradacao_anual) ** anos


def bateria_kg(energia_wh, profundidade_descarga, wh_kg):
    return energia_wh / profundidade_descarga / wh_kg
