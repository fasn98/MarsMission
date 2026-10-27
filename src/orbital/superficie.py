"""Relações de Δv para pouso, subida e encontro em Marte (Etapa 2.1).

- Subida: Δv publicado até 100 × 100 km (lançamento equatorial rumo leste) + transferência coaxial
  ideal até a órbita-alvo + déficit de rotação por lançar na inclinação i em vez de rumo leste no
  equador. Com azimute tal que sen(az) = cos(i)/cos(φ), a contribuição da rotação é v_eq·cos(i),
  independente da latitude φ (para i ≥ φ); o déficit é v_eq·(1 − cos i).
- Descida propulsiva: v_inicial + g·t_queima (perda gravitacional na forma vertical, conservadora).
"""

from __future__ import annotations

import numpy as np

from orbital import manobras as mn


def dv_transferencia_de_100(mu: float, r100: float, rp: float, ra: float) -> float:
    """Δv ideal da circular de raio r100 até a órbita (rp, ra), com rp ≥ r100."""
    if rp < r100:
        raise ValueError("periapse da órbita-alvo abaixo da órbita de referência")
    return mn.dv_transferencia_coaxial(mu, r100, r100, rp, ra)


def dv_subida(mu: float, raio: float, dv_100x100: float, rp: float, ra: float, v_eq: float,
              inclinacao_graus: float, latitude_graus: float) -> float:
    """Δv de subida (km/s) até (rp, ra) na inclinação dada, a partir do valor publicado para 100 × 100 km."""
    if inclinacao_graus < latitude_graus:
        raise ValueError("inclinação menor que a latitude do sítio exige mudança de plano (não modelada)")
    deficit = v_eq * (1.0 - np.cos(np.radians(inclinacao_graus)))
    return dv_100x100 + dv_transferencia_de_100(mu, raio + 100.0, rp, ra) + deficit


def dv_descida_vertical(v_inicial: float, gravidade: float, tempo_queima: float) -> float:
    """Δv da descida propulsiva (km/s): velocidade a anular + perda gravitacional vertical g·t."""
    return v_inicial + gravidade * tempo_queima
