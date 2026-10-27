"""Relações do estudo de ISRU (Etapa 2.2): divisão do propelente pela razão O/F, escala de uma planta
a partir de um ponto de referência e massa de fonte de energia.

Todas as escalas são lei de potência a partir de um ponto de referência publicado:
    y = y_ref · (x / x_ref)^α
com o expoente α declarado como premissa. Não há física de processo aqui.
"""

from __future__ import annotations

import numpy as np


def divisao_of(m_propelente: float, of: float) -> tuple[float, float]:
    """(oxidante, combustível) para uma massa de propelente e razão de mistura O/F em massa."""
    m_ox = m_propelente * of / (1.0 + of)
    return m_ox, m_propelente - m_ox


def escala(y_ref: float, x: float, x_ref: float, expoente: float) -> float:
    """y = y_ref · (x / x_ref)^expoente."""
    return float(y_ref * (x / x_ref) ** expoente)


def potencia_rtg_fim(p_inicio: float, degradacao_anual: float, anos: float) -> float:
    """Potência elétrica de um gerador a radioisótopo após `anos`, com degradação anual composta."""
    return float(p_inicio * (1.0 - degradacao_anual) ** anos)


def massa_rtg(potencia_necessaria: float, p_inicio: float, massa_unidade: float, degradacao_anual: float,
              anos: float) -> tuple[float, int]:
    """(massa, número de unidades) para entregar `potencia_necessaria` ao fim de `anos`."""
    n = int(np.ceil(potencia_necessaria / potencia_rtg_fim(p_inicio, degradacao_anual, anos)))
    return n * massa_unidade, n
