"""Lançamento (Etapa 2.4): geometria da DLA, inclinação da órbita de estacionamento e saída fora do plano.

Relações de geometria esférica e de velocidade (sem constantes empíricas):
- inclinação de uma subida coplanar a partir da latitude φ com azimute Σ: cos i = cos φ · sen Σ;
- a saída coplanar exige que o plano da órbita de estacionamento contenha a assíntota: |δ∞| ≤ i;
- se |δ∞| > i, a assíntota precisa sair β = |δ∞| − i do plano da órbita de estacionamento. Com um único
  impulso no perigeu (sem dogleg do lançador), o plano gira em torno do vetor posição do perigeu; a assíntota
  fica a ν∞ = arccos(−1/e) do perigeu, então o giro necessário é θ = arcsin(sen β / sen ν∞) (≈ 2β para ν∞ ≈ 150°).
"""

from __future__ import annotations

import numpy as np


def inclinacao(latitude_graus, azimute_graus):
    """Inclinação (graus) da órbita alcançada com subida coplanar: cos i = cos φ · sen Σ."""
    c = np.cos(np.radians(latitude_graus)) * np.sin(np.radians(azimute_graus))
    return float(np.degrees(np.arccos(np.clip(c, -1.0, 1.0))))


def delta_plano(dla_graus, inclinacao_graus):
    """β (graus): quanto a assíntota precisa sair do plano da órbita de estacionamento (|DLA| − i, ou 0)."""
    return max(0.0, abs(dla_graus) - inclinacao_graus)


def anomalia_assintota(mu, r, c3):
    """ν∞ (graus): ângulo entre o perigeu e a assíntota de saída, ν∞ = arccos(−1/e), e = 1 + r·v∞²/μ."""
    e = 1.0 + r * c3 / mu
    return float(np.degrees(np.arccos(-1.0 / e)))


def giro_no_perigeu(beta_graus, mu, r, c3):
    """Giro do plano no perigeu (graus) para tirar a assíntota β graus do plano original; NaN se impossível."""
    if beta_graus <= 0:
        return 0.0
    x = np.sin(np.radians(beta_graus)) / np.sin(np.radians(anomalia_assintota(mu, r, c3)))
    return float(np.degrees(np.arcsin(x))) if x <= 1.0 else float("nan")


def dv_saida(mu, r, c3, delta_i_graus=0.0):
    """Δv (km/s) de saída impulsiva de órbita circular de raio r para a hipérbole de C3, com giro de plano no perigeu.

    Lei dos cossenos entre a velocidade circular e a do perigeu da hipérbole; com Δi = 0 dá v_h − v_c."""
    v_c = np.sqrt(mu / r)
    v_h = np.sqrt(c3 + 2 * mu / r)
    di = np.radians(delta_i_graus)
    return float(np.sqrt(v_h**2 + v_c**2 - 2 * v_h * v_c * np.cos(di)))


def interpolar(x, xs, ys):
    """Interpolação linear em tabela (sem extrapolar: fora da faixa devolve NaN)."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    if x < xs[0] - 1e-12 or x > xs[-1] + 1e-12:
        return float("nan")
    return float(np.interp(x, xs, ys))
