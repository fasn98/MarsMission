"""Painel do MarsMission (Streamlit). Só interface: os dados vêm de painel.dados, as figuras de painel.graficos.

Executar (na raiz do repositório): python -m streamlit run src/painel/app.py
"""

from __future__ import annotations

import http.client

import pandas as pd
import streamlit as st

from painel import dados as d
from painel import graficos as gr
from painel.graficos import br

st.set_page_config(page_title="MarsMission", page_icon="🪐", layout="wide")

NOTA_ROTULOS = ("Cada número traz o seu rótulo: **verificado contra dados publicados**, **calculado** (saída das "
                "ferramentas do estudo ou de `src/orbital`) ou **premissa** com o status lido de `config/premissas.yaml`. "
                "Entradas que vêm de fonte publicada aparecem como **dado de fonte publicada [Fnn]** (`docs/fontes.md`), e os "
                "valores das tabelas de referência na verificação, como **dado publicado**.")


def metrica(rotulo: str, x: d.Valor, casas: int = 2, sufixo: str | None = None, ajuda: str | None = None):
    """Número grande com unidade, e o rótulo e a origem sempre visíveis logo abaixo."""
    u = x.unidade if sufixo is None else sufixo
    st.metric(rotulo, f"{br(x.valor, casas)} {u}".strip(), help=ajuda)
    st.caption(f"{x.rotulo} · {x.origem}")


# Colunas de texto com largura fixa (TextColumn não quebra linha): "Origem" cabe um caminho de results/ inteiro; "Item"
# fica larga, e um item mais longo que ela aparece cortado. Nas tabelas estreitas (meia largura, no Orçamento) o "Item"
# fica com a largura automática, para não empurrar as outras colunas para a rolagem horizontal.
COLUNAS = {"Origem": st.column_config.TextColumn("Origem", width=320, help="De onde vem o número: arquivo de results/, "
                                                 "item de config/ ou função de src/orbital recalculada no painel"),
           "Item": st.column_config.TextColumn("Item", width="large")}


def tabela(linhas: list[dict], estreita: bool = False):
    df = pd.DataFrame(linhas)
    cfg = {k: c for k, c in COLUNAS.items() if k in df.columns and not (estreita and k == "Item")}
    st.dataframe(df, hide_index=True, width="stretch", column_config=cfg)


def linha_valor(nome: str, x: d.Valor | None, casas: int = 1) -> dict:
    if x is None:
        return {"Item": nome, "Valor": "—", "Unidade": "", "Rótulo": "", "Origem": ""}
    return {"Item": nome, "Valor": br(x.valor, casas), "Unidade": x.unidade, "Rótulo": x.rotulo, "Origem": x.origem}


# ------------------------------------------------------------------------------------------------- páginas

def visao_geral():
    st.title("MarsMission — retorno robótico de amostras de Marte (Pré-Fase A)")
    st.markdown(NOTA_ROTULOS)
    m, a = d.missao_referencia(), d.arquitetura()

    st.header(f"Missão de referência: {d.nome_missao(m['id'])}")
    om = d.orbita_marte(m["orbita_marte"])
    st.caption(f"Órbita em Marte: {om['nome']}, {br(om['periapse'].valor, 0)} × {br(om['apoapse'].valor, 0)} km de altitude "
               f"({om['periapse'].rotulo}, `{om['periapse'].origem}`); captura {m['captura']} (ADR 0003). Datas em TDB, de "
               f"`results/etapa1.3/missoes.yaml`, missão `{m['id']}` (rótulo: calculado).")
    tabela([{"Evento": e, "Data (TDB)": dt, "Rótulo": d.CALCULADO} for e, dt in m["eventos"]])
    cols = st.columns(4)
    for c, (nome, x) in zip(cols, m["duracoes"].items()):
        with c:
            metrica(nome, x, 0)
    st.subheader("Δv da missão (a partir das órbitas de estacionamento)")
    cols = st.columns(4)
    for c, (nome, x) in zip(cols, m["dv"].items()):
        with c:
            metrica(nome, x, 3)
    st.subheader("Partida e reentrada")
    cols = st.columns(3)
    for c, (nome, x) in zip(cols, list(m["partida"].items())):
        with c:
            metrica(nome, x, 2)
    cols = st.columns(3)
    for c, (nome, x) in zip(cols, m["reentrada"].items()):
        with c:
            metrica(nome, x, 2)
    st.caption(f"Envelope de dimensionamento (ADR 0004): {br(m['envelope'].valor, 3)} km/s, definido por "
               f"{d.nome_missao(m['envelope_missao'])} — {m['envelope'].rotulo}.")

    st.header("Arquitetura final (Etapa 2.5)")
    cols = st.columns(4)
    with cols[0]:
        metrica("Orbitador injetado", a["orbitador"]["injetado"], 0)
    with cols[1]:
        metrica("Lander injetado", a["lander"]["injetado"], 0)
    with cols[2]:
        metrica("Lançamentos", a["lancamentos"], 0, "")
    with cols[3]:
        ra, rb = a["orbita_encontro_km"]   # altitudes de periapse e apoapse (tools/arquitetura.py)
        metrica("Encontro: periapse", ra, 0, ajuda="Altitude do periapse da órbita de encontro")
        metrica("Encontro: apoapse", rb, 0, ajuda="Altitude do apoapse da órbita de encontro")
    for veic, titulo in (("orbitador", "Orbitador (regra iii)"), ("lander", "Lander (MAV, helicópteros e braço a bordo)")):
        st.subheader(titulo)
        linhas = []
        for x in a[veic]["composicao"]:
            for k in ("propelente", "inerte", "massa"):
                if k in x:
                    linhas.append(linha_valor(f"{x['item']} — {k}", x[k], 1))
        linhas.append(linha_valor("Massa injetada (soma)", a[veic]["injetado"], 1))
        tabela(linhas)
    st.caption(f"Lander: massa de entrada {br(a['lander']['entrada'].valor, 0)} kg; pousada {br(a['lander']['pousada'].valor, 0)} kg "
               f"({d.CALCULADO}).")

    st.header("Lançadores e margens (injeção direta, ADR 0008)")
    jan = m["janelas_envelope"]
    st.caption(f"Margem = capacidade / massa injetada − 1, na pior das {len(jan)} janelas do envelope ({', '.join(jan)}).")
    linhas = [{"Veículo": veic.capitalize(), "Lançador": n, "Pior margem": f"{br(100 * x.valor, 0)} %", "Rótulo": x.rotulo, "Origem": x.origem}
              for veic, dd in a["margens"].items() for n, x in dd.items()]
    tabela(linhas)

    st.header("Verificação contra dados publicados (Etapa 1.2)")
    st.caption("C3 e v∞ calculados nas datas impressas nas fontes, comparados com os valores publicados.")
    tabela([{"Fonte": x["fonte"], "Janela": x["janela"], "Tipo": x["tipo"], "Grandeza": x["grandeza"], "Datas": x["datas"],
             "Publicado": f"{br(x['publicado'].valor, 3)} {x['publicado'].unidade}", "Rótulo do publicado": x["publicado"].rotulo,
             "Calculado aqui": f"{br(x['calculado'].valor, 4)} {x['calculado'].unidade}",
             "Diferença": f"{br(100 * x['dif_rel'], 2)} %", "Rótulo": x["calculado"].rotulo} for x in d.verificacoes()])


@st.cache_resource(show_spinner="Baixando e conferindo os kernels SPICE de config/kernels.yaml (só na primeira execução)…")
def _kernels() -> list[dict]:
    """Uma vez por processo do servidor: baixa o que falta e confere o MD5. Exceção não entra no cache (nova tentativa
    na próxima execução da página)."""
    return d.garantir_kernels()


def pagina_trajetoria():
    st.title("Trajetória heliocêntrica da missão de referência")
    try:
        _kernels()
    except (ValueError, OSError, http.client.HTTPException) as e:   # OSError inclui URLError e TimeoutError
        st.error(f"Não foi possível obter os kernels SPICE: {e}. Nada foi calculado.")
        st.button("Tentar de novo", key="kernels_tentar_de_novo")   # o clique roda a página de novo; a falha não ficou no cache
        return
    t = st.cache_data(show_spinner="Calculando com DE440 e Lambert…")(lambda: d.trajetoria())()
    st.plotly_chart(gr.trajetoria(t), width="stretch")
    st.caption(f"Terra e Marte (baricentro) nas datas reais pela DE440 (de440s.bsp); arcos de Lambert (Izzo, 2015) "
               f"propagados por Kepler — {d.CALCULADO} com `src/orbital`. Referencial: {t['referencial']}. Fechamento do "
               f"arco na chegada: ida {br(t['erro_chegada_ida_km'], 3)} km, volta {br(t['erro_chegada_volta_km'], 3)} km "
               f"({d.CALCULADO}). Projeção no plano x–y da eclíptica J2000: a componente z não aparece.")
    tabela([{"Evento": e["evento"], "Data (TDB)": e["data_tdb"], "Rótulo": d.CALCULADO} for e in t["eventos"]])


def pagina_porkchops():
    st.title("Porkchops (ida e volta)")
    idx = d.porkchops()["sentidos"]
    c1, c2 = st.columns(2)
    with c1:
        sentido = st.radio("Sentido", list(idx), format_func=lambda s: idx[s]["titulo"], horizontal=True)
    with c2:
        janela = st.selectbox("Janela", list(idx[sentido]["janelas"]))
    info = idx[sentido]
    g = st.cache_data(show_spinner=False)(d.porkchop)(sentido, janela)
    masc = d.mascara_porkchop(g, info["c3_max"])
    mins = d.minimos(sentido).get(janela, {})
    m = d.missao_referencia()
    ev = dict(m["eventos"])
    marcas = []
    if sentido == "terra_marte" and g["partida_tdb"][0] <= ev["Partida da Terra"] <= g["partida_tdb"][-1]:
        marcas.append((f"Missão de referência ({d.nome_missao(m['id'])})", ev["Partida da Terra"], ev["Chegada a Marte"]))
    if sentido == "marte_terra" and g["partida_tdb"][0] <= ev["Partida de Marte"] <= g["partida_tdb"][-1]:
        marcas.append((f"Missão de referência ({d.nome_missao(m['id'])})", ev["Partida de Marte"], ev["Chegada à Terra"]))
    st.plotly_chart(gr.porkchop(g, masc, info["niveis_c3"], info["niveis_vinf"], f"{info['titulo']} — janela {janela}", mins, marcas),
                    width="stretch")
    p6 = d.premissa("P-006")
    st.caption(f"Grade de `results/painel` (tools/exporta_painel.py), mesmo domínio e passo de tools/porkchop.py — {d.CALCULADO}. "
               f"Escondidos no desenho: C3 > {br(info['c3_max'], 0)} km²/s² (enquadramento do gráfico, `config/janelas.yaml`) e a faixa de ±{br(p6['valor'], 0)}° em torno de 180° "
               f"de ângulo de transferência (P-006, {d.rotulo_premissa('P-006')}). Mínimos de `results/etapa1.2/minimos_{sentido}.yaml`.")
    if mins:
        tabela([{"Mínimo": d.nome_minimo(k), "Partida (TDB)": x["partida_tdb"], "Chegada (TDB)": x["chegada_tdb"],
                 "C3 [km²/s²]": br(x["c3_km2_s2"], 3), "v∞ chegada [km/s]": br(x["vinf_chegada_km_s"], 3),
                 "Tempo de voo [d]": br(x["tof_dias"], 1), "Na borda do domínio": "sim" if x["na_borda_do_dominio"] else "não",
                 "Rótulo": d.CALCULADO} for k, x in mins.items()])


def pagina_orcamento():
    st.title("Orçamento de massa por veículo")
    ra, rb = d.arquitetura()["orbita_encontro_km"]
    st.markdown("Recalcula orbitador e lander com `orbital.veiculos` e as margens de injeção direta (ADR 0008) com "
                "`orbital.lancamento`. Uma premissa por vez ou várias juntas; a órbita de encontro fica a de base "
                f"({br(ra.valor, 0)} × {br(rb.valor, 0)} km, {ra.rotulo}, {ra.origem}), como na sensibilidade da Etapa 2.5. "
                "Faixas dos controles lidas de `results/` e `config/`.")
    cb = d.controles_base()
    vals = {}
    nomes = {"plataforma_lander_kg": ("Plataforma do lander [kg]", 1.0, 1),
             "margem_dv": ("Margem de Δv [%]", 100.0, 1),
             "isp_armazenavel_s": ("Isp dos estágios MMH/MON [s]", 1.0, 1),
             "fracao_estrutural_armazenavel": ("Fração estrutural dos estágios MMH/MON", 1.0, 3)}
    cols = st.columns(2)
    for i, (k, (rot, esc, casas)) in enumerate(nomes.items()):
        c = cb[k]
        lo, hi = c["faixa"]
        base = c["base"].valor
        with cols[i % 2]:
            x = st.slider(rot, min_value=round(lo * esc, casas), max_value=round(hi * esc, casas),
                          value=round(base * esc, casas), step=10 ** -casas if casas else 1.0, key=k)
            st.caption(f"Base {br(base * esc, casas)}: {c['base'].rotulo} · {c['base'].origem}. Faixa: {c['faixa_origem']}.")
            vals[k] = None if abs(x - round(base * esc, casas)) < 1e-12 else x / esc
    if any(x is not None for x in vals.values()):
        st.info("Valores fora da base: os resultados abaixo são **calculados** com a escolha feita nos controles.")
    r = st.cache_data(show_spinner="Recalculando…")(d.orcamento)(**vals)
    if not r["viavel"]:
        st.error(f"Inviável com esses valores: {r['erro']}")
        return
    cols = st.columns(2)
    for c, veic in zip(cols, ("orbitador", "lander")):
        with c:
            x = r["veiculos"][veic]
            metrica(f"{veic.capitalize()}: massa injetada", x["injetado"], 0)
            linhas = []
            for e in x["estagios"]:
                linhas += [linha_valor(f"{e['nome']} — propelente", e["propelente"]), linha_valor(f"{e['nome']} — inerte", e["inerte"])]
            for k in ("entrada", "pousada", "mav", "plataforma"):
                if k in x:
                    linhas.append(linha_valor({"entrada": "Massa de entrada", "pousada": "Massa pousada",
                                               "mav": "MAV + energia do aquecimento", "plataforma": "Plataforma de superfície"}[k], x[k]))
            tabela(linhas, estreita=True)
    st.header("Lançadores que continuam servindo")
    for veic in ("orbitador", "lander"):
        servem = [x["lancador"] + (" (desempenho anunciado, não demonstrado)" if x["categoria"] == "anunciado" else "")
                  for x in r["lancadores"] if x["veiculo"] == veic and x["serve"]]
        perdidos = [x["lancador"] for x in r["lancadores"] if x["veiculo"] == veic and x["escolhido"] and not x["serve"]]
        st.markdown(f"**{veic.capitalize()}** — servem ({len(servem)}): {', '.join(servem) or 'NENHUM'}."
                    + (f" **Escolhidos que deixam de servir:** {', '.join(perdidos)}." if perdidos else " Todos os escolhidos servem."))
        st.plotly_chart(gr.margens(r["lancadores"], veic, len(d.missao_referencia()["janelas_envelope"])), width="stretch")
    with st.expander("Tabela completa de margens"):
        tabela([{"Veículo": x["veiculo"].capitalize(), "Lançador": x["lancador"], "Categoria": x["categoria"],
                 "Escolhido (ADR 0008)": "sim" if x["escolhido"] else "", "Pior margem": "sem dado" if x["margem"] is None
                 else f"{br(100 * x['margem'].valor, 1)} %", "Janela mais restritiva": x["janela"] or "",
                 "Serve": "sim" if x["serve"] else "não", "Rótulo": d.CALCULADO} for x in r["lancadores"]])


def pagina_premissas():
    st.title("Premissas e decisões")
    ps = d.premissas()
    n_nv = sum(p["status"] == "NÃO VALIDADA" for p in ps)
    st.markdown(f"**{len(ps)} premissas** em `config/premissas.yaml`; **{n_nv} NÃO VALIDADAS**. Só o Fabio altera o status.")
    filtro = st.text_input("Filtrar (id, nome ou uso)")
    linhas = [{"Id": p["id"], "Nome": p["nome"], "Valor": str(p["valor"]), "Unidade": p.get("unidade", ""),
               "Status": p["status"], "Uso": p.get("uso", "")} for p in ps]
    if filtro:
        linhas = [x for x in linhas if any(filtro.lower() in str(v).lower() for v in x.values())]
    tabela(linhas)
    with st.expander("Justificativas"):
        for p in ps:
            st.markdown(f"**{p['id']} — {p['nome']}** ({p['status']}): {p.get('justificativa', '')}")
    st.header("Decisões (ADRs)")
    for a in d.adrs():
        with st.expander(f"{a['titulo']} — {a['status']}"):
            st.markdown(f"[Abrir no GitHub]({a['url']}) · `{a['caminho']}`")
            st.markdown(a["texto"])


def pagina_propulsao():
    st.title("Propulsão (Fase 3)")
    p = d.propulsao()
    st.markdown("Comparação de propulsão da Fase 3 (`docs/fase3_relatorio.md`; ADRs 0011, 0012 e 0013). Números de "
                "`results/etapa3.1` a `results/etapa3.3`.")
    st.header("Motores químicos e perdas de queima finita (Etapa 3.1)")
    tabela([{"Manobra": x["manobra"], "Motores": x["combinacao"], "Queimas": x["queimas"],
             "Perda calculada": f"{br(x['perda'].valor, 1)} m/s", "DRA (P-015)": f"{br(x['p015'].valor, 1)} m/s",
             "Rótulo": x["perda"].rotulo, "Origem": x["perda"].origem} for x in p["perdas"]])
    st.header("Modelo de baixo empuxo (Etapa 3.2)")
    v_ = p["verificacao"]
    st.markdown(f"Verificação contra Schwenzfeger, NASA TM X-64836, p. 31 [F113]: critério declarado de "
                f"{br(100 * v_['tolerancia'], 2)} % por componente. **{'Passa' if v_['verificado'] else 'Não passa'}**"
                + ("" if v_["verificado"] else f" em {', '.join(v_['fora_da_tolerancia'])}") +
                " (ADR 0012: atribuído provavelmente à integração publicada, não confirmado).")
    c = st.columns(3)
    with c[0]:
        metrica("Maior diferença em u", d.Valor(100 * v_["maior_dif_u"].valor, "%", v_["maior_dif_u"].rotulo, v_["maior_dif_u"].origem), 3)
    with c[1]:
        metrica("Erro do vetor posição", d.Valor(100 * v_["maior_erro_posicao"].valor, "%", v_["maior_erro_posicao"].rotulo, v_["maior_erro_posicao"].origem), 4)
    with c[2]:
        metrica("Erro do vetor velocidade", d.Valor(100 * v_["maior_erro_velocidade"].valor, "%", v_["maior_erro_velocidade"].rotulo, v_["maior_erro_velocidade"].origem), 4)
    st.header("Orbitador químico × elétrico × híbrido (Etapa 3.3)")
    st.markdown("Estada em Marte por janela: " + ", ".join(f"{k} {br(x, 0)} d" for k, x in p["estada_dias"].items())
                + ". Decisão: **orbitador químico** (ADR 0013).")
    tabela([{"Opção": x["opcao"], "Orbitador injetado": f"{br(x['orbitador'].valor, 0)} kg", "Total (iii)": f"{br(x['total'].valor, 0)} kg",
             "Descida + encontro + subida": "—" if x["tempo"] is None else f"{br(x['tempo'].valor, 0)} d", "Situação": x["situacao"],
             "Rótulo": x["total"].rotulo, "Origem": x["total"].origem} for x in p["opcoes"]])
    st.subheader("(c1) Descida em arcos em torno do periapse (só a descida)")
    st.markdown(f"Periapse mínimo do encontro: {br(p['periapse_minimo_km'], 0)} km (ADR 0005).")
    tabela([{"Opção": x["opcao"], "Tempo decorrido": f"{br(x['descida'].valor, 0)} d", "Periapse final": f"{br(x['periapse'].valor, 0)} km",
             "Situação": x["situacao"], "Rótulo": x["descida"].rotulo, "Origem": x["descida"].origem} for x in p["c1"]], estreita=True)
    st.subheader("(b) Elétrico: empuxo da ida no trecho heliocêntrico (calculado, não verificado)")
    st.markdown(f"Ida da missão de referência: {br(p['ida_referencia_dias'], 0)} d.")
    tabela([{"Opção": x["opcao"], "Empuxo da ida": f"{br(x['ida'].valor, 0)} d", "Rótulo": x["ida"].rotulo, "Origem": x["ida"].origem}
            for x in p["b"]], estreita=True)


def pagina_subsistemas():
    st.title("Subsistemas (Fase 4)")
    s = d.subsistemas()
    st.markdown("Resumo integrado da Fase 4 (`docs/fase4_relatorio.md`; ADRs 0015 a 0020). Números de "
                f"`{s['origem']}`, gerado por `tools/fase4.py` a partir de `results/etapa4.1` a `results/etapa4.5`.")
    st.header("Massas e lançadores")
    m = s["massas"]
    c = st.columns(3)
    with c[0]:
        metrica("Orbitador injetado", m["orbitador_injetado"], 0)
    with c[1]:
        metrica("Lander injetado", m["lander_injetado"], 0)
    with c[2]:
        metrica("Total na órbita baixa (regra iii)", m["total_leo"], 0)
    tabela([linha_valor("Plataforma de superfície (P-017, caso B)", m["plataforma"]),
            linha_valor("Circuito de fluido no estágio de cruzeiro (P-077)", m["circuito"]),
            linha_valor("Massa de entrada do lander", m["lander_entrada"], 0),
            linha_valor("Massa pousada do lander", m["lander_pousado"], 0),
            linha_valor("MAV + energia do aquecimento", m["mav"], 0),
            linha_valor(f"Lander injetado na referência otimista ({m['caso_a']['caso']})", m["caso_a"]["lander_injetado"], 0)], estreita=True)
    st.subheader("Lançadores de base (ADR 0020)")
    tabela([{"Veículo": x["veiculo"], "Lançador": x["lancador"], "Margem na base": f"{100 * x['margem'].valor:+.0f} %".replace("-", "−"),
             "Pior margem nas sensibilidades": f"{100 * x['pior'].valor:+.0f} %".replace("-", "−"), "Caso da pior margem": x["caso_pior"],
             "Rótulo": x["margem"].rotulo, "Origem": x["margem"].origem} for x in s["lancadores"]])
    st.header("Energia, térmico e comunicação")
    en, te, co = s["energia"], s["termico"], s["comunicacao"]
    op = en["lander_opcao"]
    st.markdown(f"- **Lander, C + RHU (ADR 0015):** {br(op['area_m2'], 1)} m² de painel e bateria de {br(op['bateria_kg'], 1)} kg, "
                f"total {br(op['total_kg'], 1)} kg; {en['rhu_quantidade']} RHUs ({br(en['pu238_g'], 1)} g de Pu-238).\n"
                f"- **Orbitador:** carga de {br(en['orbitador']['carga_w'], 0)} W, painel de {br(en['orbitador']['painel_w_afelio'], 0)} W no afélio.\n"
                f"- **MAV a {br(te['mav_alvo_c'], 0)} °C:** {br(te['mav_potencia_w'], 1)} W. **Amostras:** {te['amostras']}.\n"
                f"- **Cruzeiro do lander:** {br(te['cruzeiro_calor_w'], 0)} W contra {br(te['cruzeiro_passivo_max_w'], 0)} W passivos: "
                f"rejeição {'ativa' if te['rejeicao_ativa'] else 'passiva'} (ADR 0019).\n"
                f"- **Conjunção solar (SEP ≤ 5°):** {co['conjuncao']['inicio']} a {co['conjuncao']['fim']} ({co['conjuncao']['dias']} dias).\n"
                f"- **Caminhos de comunicação (Mbit/sol; ADR 0017):** "
                + "; ".join(f"{k} {br(v[0], 0)} a {br(v[1], 0)}" for k, v in co["caminhos_mbit_sol"].items())
                + f". Demanda do lander {br(co['demanda_lander_mbit_sol'], 0)} Mbit/sol.\n\n"
                f"Rótulo: {d.CALCULADO}. Origem: `{s['origem']}`.")
    st.header("Operação de superfície (ADR 0018)")
    su = s["superficie"]
    st.markdown(f"Chegada {su['chegada']}; início da conjunção {su['inicio_conjuncao']}. Folga mínima de "
                f"{br(su['requisitos']['folga_min'], 0)} dias antes da conjunção; alvo de {br(su['requisitos']['alvo'][0], 0)} a "
                f"{br(su['requisitos']['alvo'][1], 0)} dias.")
    tabela([{"Distância ao depósito": f"{br(x['distancia_m'], 0)} m", "Ritmo": x["ritmo"], "Helicópteros": x["helicopteros_em_paralelo"],
             "Sóis": br(x["total_sois"], 0), "Lançamento do MAV": x["lancamento"] or "—",
             "Folga até a conjunção": "—" if x["folga"] is None else f"{br(x['folga'].valor, 0)} d",
             "Folga mínima": "sim" if x["atende_folga_minima"] else "não", "Alvo": "sim" if x["dentro_do_alvo"] else "não",
             "Rótulo": d.CALCULADO, "Origem": s["origem"]} for x in su["linha_do_tempo"]])
    pr = s["premissas"]
    st.markdown(f"**Premissas:** {pr['total']}, {pr['nao_validadas']} NÃO VALIDADAS; {len(pr['criadas_na_fase_4'])} criadas na Fase 4; "
                f"críticas: {', '.join(pr['criticas'])}.")


# A página padrão fica na raiz "/"; a cópia oculta faz o endereço /visao-geral (links salvos) abrir a mesma página.
pg = st.navigation([st.Page(visao_geral, title="Visão geral", default=True),
                    st.Page(visao_geral, title="Visão geral", url_path="visao-geral", visibility="hidden"),
                    st.Page(pagina_trajetoria, title="Trajetória", url_path="trajetoria"),
                    st.Page(pagina_porkchops, title="Porkchops", url_path="porkchops"),
                    st.Page(pagina_orcamento, title="Orçamento de massa", url_path="orcamento"),
                    st.Page(pagina_propulsao, title="Propulsão", url_path="propulsao"),
                    st.Page(pagina_subsistemas, title="Subsistemas", url_path="subsistemas"),
                    st.Page(pagina_premissas, title="Premissas e decisões", url_path="premissas")])
pg.run()
