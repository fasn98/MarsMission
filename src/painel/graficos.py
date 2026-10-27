"""Figuras Plotly do painel. Recebem os dados prontos de painel.dados; não leem arquivos nem calculam física.

Paleta: os mesmos tokens de tools/porkchop.py (rampa azul para C3, laranja para v∞ e para a volta, cinza para o resto).
"""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
SUPERFICIE = "#fcfcfb"
GRADE = "#eceae4"
AZUL = "#2a78d6"
AZUL_ESCURO = "#104281"
LARANJA = "#eb6834"
CINZA = "#8a8985"
VERDE = "#2f8f4e"
VERMELHO = "#c2410c"


def br(x, casas=2):
    """Número com vírgula decimal e espaço fino de milhar, como nos relatórios do estudo."""
    if x is None or (isinstance(x, float) and x != x):
        return "—"
    return f"{x:,.{casas}f}".replace(",", " ").replace(".", ",")


def _layout(fig, titulo, x, y, altura=560):
    fig.update_layout(title={"text": titulo, "x": 0, "font": {"color": TINTA, "size": 16}},
                      paper_bgcolor=SUPERFICIE, plot_bgcolor=SUPERFICIE, height=altura,
                      font={"color": TINTA_2, "size": 12}, margin={"l": 60, "r": 20, "t": 60, "b": 50},
                      legend={"orientation": "h", "y": -0.18, "x": 0, "font": {"size": 11}},
                      hoverlabel={"bgcolor": "white", "font": {"color": TINTA}})
    fig.update_xaxes(title=x, gridcolor=GRADE, zeroline=False, linecolor="#d6d5d0")
    fig.update_yaxes(title=y, gridcolor=GRADE, zeroline=False, linecolor="#d6d5d0")
    return fig


def porkchop(g, mascara, niveis_c3, niveis_vinf, titulo, minimos=None, marcas=None):
    """Contornos de C3 (azul) e v∞ de chegada (laranja, tracejado) sobre datas TDB, com hover em cada ponto da grade.

    `g`: grade de painel.dados.porkchop; `mascara`: pontos escondidos (painel.dados.mascara_porkchop);
    `minimos`: mínimos de results/etapa1.2; `marcas`: [(rótulo, partida, chegada)] (ex.: missão de referência)."""
    xp, yc = g["partida_tdb"].astype(str), g["chegada_tdb"].astype(str)
    c3 = np.where(mascara, np.nan, g["c3_km2_s2"]).T          # z[linha = chegada, coluna = partida]
    vi = np.where(mascara, np.nan, g["vinf_chegada_km_s"]).T
    tof = g["tof_dias"].T
    extra = [vi, tof] + ([g["dla_graus"].T] if "dla_graus" in g else [])
    custom = np.dstack(extra)
    hover = ("partida %{x}<br>chegada %{y}<br>C3 %{z:.2f} km²/s²<br>v∞ chegada %{customdata[0]:.2f} km/s"
             "<br>tempo de voo %{customdata[1]:.0f} d" + ("<br>DLA %{customdata[2]:.1f}°" if "dla_graus" in g else "")
             + "<extra>calculado (results/painel)</extra>")
    fig = go.Figure()
    fig.add_trace(go.Contour(x=xp, y=yc, z=c3, customdata=custom, hovertemplate=hover, name="C3 de partida [km²/s²]",
                             contours={"coloring": "lines", "showlabels": True, "start": min(niveis_c3), "end": max(niveis_c3),
                                       "labelfont": {"size": 10, "color": TINTA}},
                             autocontour=False, ncontours=len(niveis_c3),
                             line={"width": 1.2}, colorscale=[[0, AZUL], [1, AZUL]], showscale=False, showlegend=True))
    fig.add_trace(go.Contour(x=xp, y=yc, z=vi, hoverinfo="skip", name="v∞ de chegada [km/s]",
                             contours={"coloring": "lines", "showlabels": True, "start": min(niveis_vinf), "end": max(niveis_vinf),
                                       "labelfont": {"size": 10, "color": TINTA}},
                             autocontour=False, ncontours=len(niveis_vinf),
                             line={"width": 1.0, "dash": "dash"}, colorscale=[[0, LARANJA], [1, LARANJA]],
                             showscale=False, showlegend=True))
    simbolos = {"tipo_1": ("circle", "Mín. C3 tipo I"), "tipo_2": ("square", "Mín. C3 tipo II")}
    for chave, m in (minimos or {}).items():
        if chave not in simbolos:
            continue
        s, rot = simbolos[chave]
        fig.add_trace(go.Scatter(x=[m["partida_tdb"][:10]], y=[m["chegada_tdb"][:10]], mode="markers",
                                 marker={"symbol": s, "size": 11, "color": TINTA, "line": {"color": SUPERFICIE, "width": 2}},
                                 name=f"{rot}: C3 = {br(m['c3_km2_s2'])} km²/s² (calculado)",
                                 hovertemplate=f"{rot}<br>C3 {br(m['c3_km2_s2'])} km²/s²<br>"
                                               f"partida {m['partida_tdb'][:10]}<br>chegada {m['chegada_tdb'][:10]}"
                                               "<extra>calculado (results/etapa1.2)</extra>"))
    for rot, xd, yd in marcas or []:
        fig.add_trace(go.Scatter(x=[xd], y=[yd], mode="markers", name=rot,
                                 marker={"symbol": "star", "size": 15, "color": AZUL_ESCURO, "line": {"color": SUPERFICIE, "width": 1.5}},
                                 hovertemplate=f"{rot}<br>partida {xd}<br>chegada {yd}<extra>calculado (results/etapa1.3)</extra>"))
    return _layout(fig, titulo, "Data de partida (TDB)", "Data de chegada (TDB)")


def trajetoria(t):
    """Trajetória heliocêntrica 2D: órbitas de Terra e Marte no período da missão, arcos de ida e volta e os eventos."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker={"size": 14, "color": "#e3a008"}, name="Sol",
                             hoverinfo="name"))
    for corpo, cor, nome in (("terra", AZUL, "Terra"), ("marte", VERMELHO, "Marte")):
        r = t[corpo]
        fig.add_trace(go.Scatter(x=r[:, 0], y=r[:, 1], mode="lines", line={"color": cor, "width": 1, "dash": "dot"},
                                 name=f"Órbita de {nome} (DE440)", customdata=t["datas_planetas"],
                                 hovertemplate=nome + " em %{customdata}<br>x %{x:.3f} UA, y %{y:.3f} UA<extra>calculado</extra>"))
    for arco, cor, nome in (("ida", AZUL_ESCURO, "Ida (Lambert)"), ("volta", LARANJA, "Volta (Lambert)")):
        r = t[arco]
        fig.add_trace(go.Scatter(x=r[:, 0], y=r[:, 1], mode="lines", line={"color": cor, "width": 2.5}, name=nome,
                                 hovertemplate=nome + "<br>x %{x:.3f} UA, y %{y:.3f} UA<extra>calculado</extra>"))
    for e in t["eventos"]:
        for corpo, cor, simb in (("terra", AZUL, "circle"), ("marte", VERMELHO, "circle")):
            p = e[corpo]
            fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode="markers", showlegend=False,
                                     marker={"size": 9, "color": cor, "symbol": simb, "line": {"color": SUPERFICIE, "width": 1.5}},
                                     hovertemplate=f"{'Terra' if corpo == 'terra' else 'Marte'} — {e['evento']}<br>{e['data_tdb']} (TDB)"
                                                   "<extra>calculado</extra>"))
    fig = _layout(fig, "Trajetória heliocêntrica da missão de referência (plano da eclíptica J2000)", "x [UA]", "y [UA]", 640)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


def margens(linhas, veiculo, n_janelas):
    """Barras horizontais da pior margem de injeção direta por lançador (verde: serve; cinza: não serve ou sem dado)."""
    sel = [x for x in linhas if x["veiculo"] == veiculo and x["margem"] is not None]
    sel.sort(key=lambda x: x["margem"].valor)
    fig = go.Figure(go.Bar(
        x=[100 * x["margem"].valor for x in sel], y=[x["lancador"] + (" ★" if x["escolhido"] else "") for x in sel],
        orientation="h", marker={"color": [VERDE if x["serve"] else CINZA for x in sel]},
        customdata=[[x["janela"], x["categoria"]] for x in sel],
        hovertemplate="%{y}<br>pior margem %{x:.0f} %<br>janela mais restritiva %{customdata[0]}<br>"
                      "categoria: %{customdata[1]}<extra>calculado</extra>"))
    fig.add_vline(x=0, line={"color": TINTA, "width": 1})
    return _layout(fig, f"{veiculo.capitalize()}: pior margem de injeção direta nas {n_janelas} janelas (★ = escolhido no ADR 0008)",
                   "Margem [%]", "", 80 + 34 * max(len(sel), 1))
