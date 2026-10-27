"""Interface do painel: cada página roda sem exceção (Streamlit AppTest). Pulado se o Streamlit não estiver instalado."""

from __future__ import annotations

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

PAGINAS = ["visao_geral", "pagina_trajetoria", "pagina_porkchops", "pagina_orcamento", "pagina_premissas"]


def _pagina(nome):
    """Roda uma página isolada: st.navigation vira um no-op só durante a importação de painel.app."""
    import sys

    import streamlit as st

    original = st.navigation
    st.navigation = lambda paginas, **k: type("SemNavegacao", (), {"run": lambda self: None})()
    try:
        sys.modules.pop("painel.app", None)
        import painel.app as app
    finally:
        st.navigation = original
    getattr(app, nome)()


@pytest.mark.parametrize("nome", PAGINAS)
def test_pagina_roda_sem_erro(nome):
    at = AppTest.from_function(_pagina, args=(nome,), default_timeout=180)
    at.run()
    assert not at.exception, [e.value for e in at.exception]
    assert not at.error, [e.value for e in at.error]


def test_orcamento_no_limite_superior_perde_lancadores():
    """Plataforma do lander em 2500 kg (SRL 2024 − MAV): o lander deixa de ter o Falcon Heavy com recuperação e o VC2."""
    at = AppTest.from_function(_pagina, args=("pagina_orcamento",), default_timeout=180)
    at.run()
    at.slider(key="plataforma_lander_kg").set_value(at.slider(key="plataforma_lander_kg").max).run()
    lander = next(m.value for m in at.markdown if m.value.startswith("**Lander**"))
    perdidos = lander.split("deixam de servir:**")[1]
    assert "Falcon Heavy (recuperação)" in perdidos and "Vulcan VC2" in perdidos and "Vulcan VC4" not in perdidos
