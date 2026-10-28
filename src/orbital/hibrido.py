"""Orbitador híbrido (Etapa 3.3, opção c): captura química, espiral elétrica até a órbita de encontro baixa e de volta,
saída química para a Terra.

Concepção (c2): a captura química leva da hipérbole de chegada a uma órbita CIRCULAR de raio r_c; a espiral elétrica
tangencial (orbital.baixo_empuxo, verificada na Etapa 3.2, ADR 0012) desce de r_c até a órbita circular de encontro
(raio r_e); depois do encontro, sobe de r_e até r_c; a saída química para a Terra parte da circular r_c.
A espiral é a quase circular: Δv = |√(μ/r_e) − √(μ/r_c)| (conferida contra a numérica na Etapa 3.2; diferença ~ε²) e
tempo com o motor ligado pela equação do foguete com empuxo e vazão constantes. Com o motor desligado no eclipse
(sombra cilíndrica no plano da órbita, o mesmo pior caso de orbital.plataforma), o tempo decorrido é a integral de
dt / (1 − fração em eclipse no raio r(t)), com r(t) da velocidade circular (quase circular).

Massas (de trás para a frente, como orbital.dimensionamento, mesmas queimas e descartes):
  inserção (química, descartada após a captura): correções da ida, captura até r_c;
  elétrica (xenônio): descida r_c → r_e; subida r_e → r_c;
  retorno (química): encontro e manutenção (descarte antes), saída de Marte a partir de r_c, correções da volta,
  desvio (descarte da cápsula antes).
O sistema elétrico (propulsores, PPU, alimentação, painel dedicado) fica no orbitador até o fim.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from scipy.integrate import quad

from orbital.foguete import G0


@dataclass(frozen=True)
class SistemaEletrico:
    n_ativos: int            # propulsores que queimam juntos
    n_instalados: int        # inclui reservas
    empuxo_n: float          # por propulsor
    isp_s: float
    potencia_w: float        # de entrada, por propulsor
    massa_propulsor_kg: float
    massa_ppu_kg: float      # por propulsor instalado
    massa_alimentacao_kg: float   # alimentação de xenônio, por propulsor instalado
    inerte_por_kg_xenonio: float  # tanque + resíduo inutilizável, por kg de xenônio usado
    w_kg_painel: float       # potência específica do painel no afélio, já com as perdas (W/kg)
    mga_eletronica: float    # margem de crescimento de propulsores, PPU e alimentação
    mga_painel: float

    @property
    def empuxo_total_n(self):
        return self.n_ativos * self.empuxo_n

    @property
    def vazao_kg_s(self):
        return self.empuxo_total_n / (self.isp_s * G0 * 1e3)

    @property
    def potencia_total_w(self):
        return self.n_ativos * self.potencia_w

    def massa_seca_kg(self):
        """Propulsores, PPU, alimentação e painel dedicado, com as margens de crescimento (sem tanque)."""
        el = self.n_instalados * (self.massa_propulsor_kg + self.massa_ppu_kg + self.massa_alimentacao_kg) * (1 + self.mga_eletronica)
        painel = self.potencia_total_w / self.w_kg_painel * (1 + self.mga_painel)
        return el + painel


def dv_circular(mu, r1, r2):
    return abs(math.sqrt(mu / r1) - math.sqrt(mu / r2))


def fracao_eclipse_circular(raio_planeta, r):
    """Fração do período em sombra cilíndrica, órbita circular com o Sol no plano (pior caso)."""
    return math.asin(min(1.0, raio_planeta / r)) / math.pi


def tempos_espiral(mu, raio_planeta, r_ini, r_fim, m0_kg, se):
    """(tempo com o motor ligado [s], tempo decorrido com o motor desligado no eclipse [s], Δv [km/s], massa final)."""
    dv = dv_circular(mu, r_ini, r_fim)
    c = se.isp_s * G0
    mdot = se.vazao_kg_s
    t_on = m0_kg / mdot * (1 - math.exp(-dv / c))
    v0 = math.sqrt(mu / r_ini)
    s = 1.0 if r_fim < r_ini else -1.0   # descer aumenta a velocidade circular

    def r_de(t):
        vc = v0 + s * c * math.log(m0_kg / (m0_kg - mdot * t))
        return mu / vc ** 2

    t_dec, _ = quad(lambda t: 1.0 / (1.0 - fracao_eclipse_circular(raio_planeta, r_de(t))), 0.0, t_on, limit=200)
    return t_on, t_dec, dv, m0_kg - mdot * t_on


def dv_hiperbole_circular(mu, vinf, r):
    """Δv impulsivo entre a hipérbole de v∞ e a órbita circular de raio r (periapse em r)."""
    return math.sqrt(vinf ** 2 + 2 * mu / r) - math.sqrt(mu / r)


def massas(dv, se, isp_quimico, eps_ins, eps_ret, carga_final_kg, descartado_kg, capsula_kg, n_iter=60):
    """Massas do orbitador híbrido. `dv` (km/s, já com a margem): correcoes_ida, captura, descida, encontro, subida,
    saida, correcoes_volta, desvio. Devolve o detalhe; 'injetada_kg' é a massa no início da inserção."""
    c, cx = isp_quimico * G0, se.isp_s * G0
    k_r, k_x, k_i = eps_ret / (1 - eps_ret), se.inerte_por_kg_xenonio, eps_ins / (1 - eps_ins)
    seco_el = se.massa_seca_kg()
    p_r = p_x = 0.0
    for _ in range(n_iter):
        m6 = carga_final_kg + seco_el + k_r * p_r + k_x * p_x
        b6 = m6 * math.exp(dv["desvio"] / c)
        a5 = b6 + capsula_kg
        b5 = a5 * math.exp(dv["correcoes_volta"] / c)
        b4 = b5 * math.exp(dv["saida"] / c)
        b3 = b4 * math.exp(dv["subida"] / cx)
        b2 = b3 * math.exp(dv["encontro"] / c)
        a1 = b2 + descartado_kg
        b1 = a1 * math.exp(dv["descida"] / cx)
        novo_r = (b6 - m6) + (b5 - a5) + (b4 - b5) + (b2 - b3)
        novo_x = (b3 - b4) + (b1 - a1)
        if abs(novo_r - p_r) < 1e-9 and abs(novo_x - p_x) < 1e-9:
            break
        p_r, p_x = novo_r, novo_x
    x = math.exp((dv["correcoes_ida"] + dv["captura"]) / c) - 1
    p_i = b1 * x / (1 - k_i * x)
    m_ins = b1 + k_i * p_i + p_i
    return {"injetada_kg": m_ins, "insercao": {"propelente_kg": p_i, "inerte_kg": k_i * p_i},
            "retorno": {"propelente_kg": p_r, "inerte_kg": k_r * p_r},
            "eletrico": {"xenonio_kg": p_x, "tanque_e_residuo_kg": k_x * p_x, "seco_kg": seco_el},
            "massa_antes_descida_kg": b1, "massa_antes_subida_kg": b3, "massa_final_kg": m6}
