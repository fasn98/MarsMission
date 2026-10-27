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


def test_visao_geral_mostra_nomes_legiveis_e_orbita_sem_truncar():
    """Nomes por extenso no cabeçalho e as duas altitudes da órbita de encontro como métricas separadas."""
    at = AppTest.from_function(_pagina, args=("visao_geral",), default_timeout=180)
    at.run()
    assert any(h.value == "Missão de referência: conjunção de 2028" for h in at.header)
    rotulos = [m.label for m in at.metric]
    assert "Encontro: periapse" in rotulos and "Encontro: apoapse" in rotulos
    assert not any("eliptica_alta" in c.value for c in at.caption)


def test_visao_geral_tambem_em_visao_geral():
    """A página padrão fica na raiz; uma cópia oculta atende /visao-geral (links salvos), com o mesmo conteúdo."""
    import ast
    from pathlib import Path

    arvore = ast.parse((Path(__file__).resolve().parents[1] / "src" / "painel" / "app.py").read_text(encoding="utf-8"))
    paginas = [c for c in ast.walk(arvore) if isinstance(c, ast.Call) and getattr(c.func, "attr", "") == "Page"]
    kw = [{k.arg: ast.literal_eval(k.value) for k in c.keywords if k.arg in ("url_path", "default", "visibility")}
          for c in paginas if c.args and getattr(c.args[0], "id", "") == "visao_geral"]
    assert {"default": True} in kw
    assert {"url_path": "visao-geral", "visibility": "hidden"} in kw


def test_item_tem_largura_automatica_so_nas_tabelas_estreitas():
    """Visão geral (largura total): "Item" com largura fixa. Orçamento (meia largura): "Item" automático, "Origem" fixa."""
    import json

    def colunas(nome):
        at = AppTest.from_function(_pagina, args=(nome,), default_timeout=180)
        at.run()
        return [json.loads(df.proto.columns) for df in at.dataframe]

    largas = [c for c in colunas("visao_geral") if "Origem" in c]
    assert largas and all("width" in c.get("Item", {}) for c in largas if "Item" in c)
    estreitas = [c for c in colunas("pagina_orcamento") if "Origem" in c]
    assert len(estreitas) == 2   # orbitador e lander
    assert all("Item" not in c and c["Origem"]["width"] == 320 for c in estreitas)


def _trajetoria_com_falha_no_download():
    """Página Trajetória com garantir_kernels trocado: levanta TimeoutError enquanto painel.dados._teste_falhar for
    verdadeiro (estado no módulo, compartilhado com o teste no mesmo processo; AppTest só serializa esta função)."""
    import sys

    import streamlit as st

    from painel import dados

    if not hasattr(dados, "_garantir_original"):
        dados._garantir_original = dados.garantir_kernels

    def garantir():
        if dados._teste_falhar:
            raise TimeoutError("o download de X passou do prazo de 120 s (config/operacional.yaml)")
        return dados._garantir_original()

    dados.garantir_kernels = garantir
    original = st.navigation
    st.navigation = lambda paginas, **k: type("SemNavegacao", (), {"run": lambda self: None})()
    try:
        sys.modules.pop("painel.app", None)
        import painel.app as app
    finally:
        st.navigation = original
    app._kernels.clear()
    app.pagina_trajetoria()


def test_trajetoria_mostra_erro_do_download_e_tentar_de_novo_funciona():
    from painel import dados

    dados._teste_falhar = True
    try:
        at = AppTest.from_function(_trajetoria_com_falha_no_download, default_timeout=180)
        at.run()
        assert not at.exception
        assert "passou do prazo de 120 s" in at.error[0].value and "Nada foi calculado" in at.error[0].value
        botao = at.button(key="kernels_tentar_de_novo")
        assert botao.label == "Tentar de novo"
        dados._teste_falhar = False   # a rede voltou
        botao.click().run()
        assert not at.exception and not at.error
        assert any("Partida da Terra" in str(df.value) for df in at.dataframe)   # a trajetória foi calculada
    finally:
        if hasattr(dados, "_garantir_original"):
            dados.garantir_kernels = dados._garantir_original
            del dados._garantir_original
        del dados._teste_falhar
