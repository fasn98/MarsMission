"""Manobras impulsivas nos extremos das cônicas emendadas.

Todas as relações saem da conservação de energia específica numa cônica (equação vis-viva,
v² = μ(2/r − 1/a)) e de v∞² = μ/(−a) na hipérbole. Manobras impulsivas e tangenciais, aplicadas
no periapse (inserção/saída) ou no apoapse (elevação do periapse). Sem perdas gravitacionais,
sem perdas de direção, sem rotação da linha das apsides.

Unidades: km, s, km³/s².
"""

from __future__ import annotations

import numpy as np


def v_orbita(mu: float, r: float, rp: float, ra: float) -> float:
    """Velocidade no raio r de uma elipse com periapse rp e apoapse ra (vis-viva)."""
    a = 0.5 * (rp + ra)
    return np.sqrt(mu * (2.0 / r - 1.0 / a))


def v_hiperbole(mu: float, vinf, r: float):
    """Velocidade no raio r de uma hipérbole com excesso v∞ (vis-viva com a = −μ/v∞²)."""
    return np.sqrt(np.asarray(vinf) ** 2 + 2.0 * mu / r)


def dv_hiperbole_orbita(mu: float, vinf, rp: float, ra: float | None = None):
    """Δv no periapse rp entre a hipérbole de v∞ e a órbita (rp, ra); circular se ra é None.

    Serve para inserção (captura) e para saída (injeção), que são simétricas.
    """
    ra = rp if ra is None else ra
    return v_hiperbole(mu, vinf, rp) - v_orbita(mu, rp, rp, ra)


def dv_elevacao_periapse(mu: float, rp_inicial: float, rp_final: float, ra: float) -> float:
    """Δv no apoapse ra para levar o periapse de rp_inicial a rp_final."""
    return v_orbita(mu, ra, rp_final, ra) - v_orbita(mu, ra, rp_inicial, ra)


def dv_captura_aerocaptura(mu: float, rp_atm: float, rp: float, ra: float | None = None) -> float:
    """Δv propulsivo após aerocaptura ideal para a órbita (rp, ra).

    Modelo: a passagem atmosférica (periapse em rp_atm) dissipa a energia necessária para deixar
    o veículo numa elipse (rp_atm, ra_alvo). No apoapse dessa elipse, uma queima eleva o
    periapse até rp. Se a órbita final for circular (ra None), o apoapse da elipse pós-passagem
    é rp e a queima também circulariza. O custo térmico e o controle da passagem atmosférica
    não são modelados.
    """
    ra = rp if ra is None else ra
    return dv_elevacao_periapse(mu, rp_atm, rp, ra)


def velocidade_reentrada(mu: float, vinf, r_interface: float):
    """Velocidade inercial na interface de reentrada, chegada direta pela hipérbole de v∞."""
    return v_hiperbole(mu, vinf, r_interface)


def declinacao_graus(vetor_equatorial) -> float:
    """Declinação (graus) de um vetor dado no frame equatorial J2000."""
    v = np.asarray(vetor_equatorial, dtype=float)
    return float(np.degrees(np.arcsin(v[2] / np.linalg.norm(v))))


def parametro_b(mu: float, vinf: float, h: float) -> float:
    """Parâmetro de impacto B (km) de uma hipérbole de excesso v∞ e momento angular h: B = h / v∞."""
    return h / vinf


def h_entrada(mu: float, vinf: float, r_interface: float, gama_graus: float) -> float:
    """Momento angular da hipérbole que cruza r_interface com ângulo de trajetória γ (negativo na descida)."""
    v = v_hiperbole(mu, vinf, r_interface)
    return float(r_interface * v * np.cos(np.radians(gama_graus)))


def h_periapse(mu: float, vinf: float, rp: float) -> float:
    """Momento angular da hipérbole de excesso v∞ com periapse rp."""
    return float(rp * v_hiperbole(mu, vinf, rp))


def dv_desvio(mu: float, vinf: float, r_interface: float, gama_graus: float, rp_seguro: float,
              antecedencia_s: float) -> float:
    """Δv de desvio do orbitador depois de soltar a cápsula, na aproximação linear do plano B.

    A cápsula segue a hipérbole de entrada (γ na interface); o orbitador precisa passar com
    periapse rp_seguro. Uma queima perpendicular Δv feita `antecedencia_s` antes do encontro
    desloca o ponto no plano B de ≈ Δv·t (aproximação linear, sem foco gravitacional no
    deslocamento, que já está em B). Logo Δv ≈ ΔB / t.
    """
    db = (h_periapse(mu, vinf, rp_seguro) - h_entrada(mu, vinf, r_interface, gama_graus)) / vinf
    return float(abs(db) / antecedencia_s)
