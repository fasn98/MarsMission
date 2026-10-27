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

from orbital import foguete as fg
from orbital.config import v


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


def pior_margem_a(nome, m_inj, janelas, cfg):
    """(pior margem, janela) da injeção direta do lançador `nome` para a massa dada, entre as janelas."""
    lan = cfg["lancadores"][nome]
    if lan.get("plataforma") == "ELA-4":
        return None, None
    pfm = cfg["centro"]["plataformas"].get(lan.get("plataforma"), {})
    imax = inclinacao(pfm.get("latitude_graus", v(cfg["centro"]["latitude_graus"])), cfg["centro"]["azimute_graus"]["valor"][0])
    vals = []
    for j in janelas:
        cap = capacidade_direta(lan, j["c3_km2_s2"], j["dla_graus"], cfg, imax)[0]
        if cap != cap:
            return None, j["id"]
        vals.append((cap / m_inj - 1, j["id"]))
    return min(vals)


def capacidade_direta(lan, c3, dla, cfg, i_max):
    """(capacidade kg ou NaN, nota) da injeção direta no C3 e na DLA."""
    if "pontos" not in lan["c3"]:
        return float("nan"), "sem curva de C3 publicada"
    cap = interpolar(c3, lan["c3"]["pontos"], lan["c3"]["massa_kg"])
    if cap != cap:
        return cap, "C3 fora da faixa publicada"
    if i_max is not None and abs(dla) > i_max:
        return 0.0, f"|DLA| > {i_max:.2f}° (azimute 40°): exige dogleg ou plano quebrado".replace(".", ",")
    m = cfg["dla"]["multiplicador_nordeste"]
    f = 1.0 if abs(dla) <= v(cfg["dla"]["faixa_sem_penalidade_graus"]) else interpolar(abs(dla), m["dla_graus"], m["fator"])
    return cap * f, ("" if f == 1.0 else f"multiplicador de DLA {f:.3f}".replace(".", ","))


def leo_por_janela(m_inj, cand, dcfg, po, i_graus):
    """(massa na órbita baixa kg, β graus, giro no perigeu θ graus, Δv extra do giro km/s), com o estágio de saída
    próprio redimensionado para a janela."""
    mu = v(po["gm_terra"])
    r = v(po["raio_terra_km"]) + v(po["leo_altitude_km"])
    c3 = cand["c3_km2_s2"]
    beta = delta_plano(cand["dla_graus"], i_graus)
    theta = giro_no_perigeu(beta, mu, r, c3)
    if theta != theta:
        return float("nan"), beta, theta, float("nan")
    extra = dv_saida(mu, r, c3, theta) - dv_saida(mu, r, c3, 0.0)
    dv_ideal = cand["dv_saida_terra_km_s"] + extra
    dv = (1 + v(dcfg["margem_dv"])) * (dv_ideal + v(dcfg["dv"]["perda_gravitacional"]["saida_terra"]))
    st = dcfg["estagios"]["saida_terra"]
    e = fg.Estagio("saida_terra", v(st["isp_s"]), v(st["fracao_estrutural"]), [fg.Queima("saida_terra", dv)])
    try:
        return fg.dimensionar_veiculo([e], m_inj)[0].massa_inicial, beta, theta, extra
    except ValueError:  # Δv alto demais para o estágio (giro grande): inviável
        return float("inf"), beta, theta, extra
