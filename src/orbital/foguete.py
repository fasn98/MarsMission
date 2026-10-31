"""Equação do foguete (Tsiolkovsky) por estágio, com fração estrutural e várias queimas.

Um estágio tem propelente m_p, massa inerte m_s e uma lista de queimas. A fração estrutural
ε = m_s / (m_s + m_p) fixa m_s = k·m_p, com k = ε / (1 − ε). Cada queima i leva a massa de
m_antes a m_depois = m_antes / exp(Δv_i / (g0·Isp)). Entre queimas, cargas podem ser
descartadas (por exemplo, a cápsula solta antes do desvio do orbitador). Perdas e margens entram
como Δv adicional, nunca embutidas aqui.

Unidades: kg, km/s, s.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

G0 = 9.80665e-3  # km/s², gravidade padrão: 3ª CGPM (1901), NIST SP 330 p. 46 [F31]


@dataclass(frozen=True)
class Queima:
    nome: str
    dv: float                 # km/s
    descarta_antes: float = 0.0  # kg de carga soltos imediatamente ANTES desta queima


@dataclass
class Estagio:
    nome: str
    isp: float                # s
    fracao_estrutural: float  # ε = m_s / (m_s + m_p)
    queimas: list = field(default_factory=list)


@dataclass(frozen=True)
class ResultadoEstagio:
    nome: str
    propelente: float
    inerte: float
    massa_inicial: float      # estágio cheio + tudo o que ele carrega
    propelente_por_queima: dict
    massa_antes_por_queima: dict = field(default_factory=dict)   # kg, logo antes de cada queima (já sem os descartes)


def _massa_final_por_inicial(isp, queimas, m_ini, k_mp, antes=None):
    """Massa ao fim das queimas, dado m_ini; devolve (m_fim, propelente consumido por queima). Se `antes` for um dict,
    recebe a massa logo antes de cada queima (já sem os descartes)."""
    m = m_ini
    gastos = {}
    for q in queimas:
        m -= q.descarta_antes
        if antes is not None:
            antes[q.nome] = m
        m_dep = m / np.exp(q.dv / (G0 * isp))
        gastos[q.nome] = m - m_dep
        m = m_dep
    return m, gastos


def dimensionar_estagio(est: Estagio, carga_final: float):
    """Dimensiona o estágio para levar `carga_final` (kg) ao fim da última queima.

    `carga_final` é o que sobra depois de todas as queimas e descartes (sem o inerte do estágio).
    A massa inicial é função linear do propelente m_p (o inerte é k·m_p), então m_p sai de uma
    equação linear, sem iteração. Inviável se k·(R−1) ≥ 1, com R a razão de massas total.
    """
    eps = est.fracao_estrutural
    if not 0.0 <= eps < 1.0:
        raise ValueError("fração estrutural fora de [0, 1)")
    k = eps / (1.0 - eps)
    descartes = sum(q.descarta_antes for q in est.queimas)

    def m_inicial(mp):
        m = carga_final + k * mp  # massa ao fim da última queima
        for q in reversed(est.queimas):
            m = m * np.exp(q.dv / (G0 * est.isp)) + q.descarta_antes
        return m

    def residuo(mp):  # m_inicial − (carga + inerte + propelente + descartes)
        return m_inicial(mp) - (carga_final + k * mp + mp + descartes)

    # resíduo linear em mp: inclinação por diferença num passo da escala da carga (com passo de 1 kg, cargas grandes,
    # como nos pontos quase inviáveis das varreduras, perdem a precisão por cancelamento)
    passo = max(1.0, carga_final)
    r0, r1 = residuo(0.0), residuo(passo)
    inclinacao = (r1 - r0) / passo
    if inclinacao >= 0.0:
        raise ValueError(f"estágio {est.nome} inviável: Δv alto demais para Isp e fração estrutural dados")
    mp = -r0 / inclinacao
    ms = k * mp
    m_ini = carga_final + ms + mp + descartes
    antes = {}
    m_fim, gastos = _massa_final_por_inicial(est.isp, est.queimas, m_ini, k * mp, antes)
    assert abs(m_fim - (carga_final + ms)) <= 1e-9 * m_ini
    return ResultadoEstagio(est.nome, mp, ms, m_ini, gastos, antes)


def dimensionar_veiculo(estagios, carga_final_ultimo: float):
    """Dimensiona estágios em série, do último (o que termina a missão) para o primeiro.

    `estagios` em ordem de uso (primeiro a queimar primeiro). A carga de cada estágio é a massa
    inicial do estágio seguinte (que é carregado inteiro até ser separado).
    """
    carga = carga_final_ultimo
    resultados = []
    for est in reversed(estagios):
        r = dimensionar_estagio(est, carga)
        resultados.append(r)
        carga = r.massa_inicial
    return list(reversed(resultados))
