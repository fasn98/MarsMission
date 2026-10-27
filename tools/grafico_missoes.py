"""Gráfico Δv total × duração das missões candidatas (results/etapa1.3/dv_x_duracao.png).

Lê results/etapa1.3/missoes.yaml (gerado por tools/missoes.py). Δv propulsivo total com a órbita
de Marte do critério de seleção, sem aerocaptura (linha cheia) e com aerocaptura (vazado).

Uso: python tools/grafico_missoes.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import yaml  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
TINTA, TINTA_2, SUPERFICIE, GRADE = "#0b0b0b", "#52514e", "#fcfcfb", "#eceae4"
CORES = {"oposicao": "#eb6834", "conjuncao": "#2a78d6", "conjuncao_transito_curto": "#1baf7a"}
NOMES = {"oposicao": "Oposição (estada 30–90 d, total ≤ 650 d)", "conjuncao": "Conjunção",
         "conjuncao_transito_curto": "Conjunção, trânsitos ≤ 210 d"}


def _rotular(fig, ax, pontos):
    """Rótulos com posicionamento guloso em pixels: evita outros rótulos e marcadores."""
    fig.canvas.draw()
    tr = ax.transData
    marcas = [tr.transform((x, y)) for x, y, _ in pontos]
    caixas = []
    candidatos = [(8, 6), (8, -16), (-34, 6), (-34, -16), (8, 20), (8, -30), (-34, 20), (-34, -30)]
    for (x, y, txt), (px, py) in zip(pontos, marcas):
        for dx, dy in candidatos:
            # caixa aproximada do texto em pixels (dpi da figura)
            esc = fig.dpi / 72
            bx0, by0 = px + dx * esc, py + dy * esc
            caixa = (bx0, by0, bx0 + 26 * esc, by0 + 10 * esc)
            colide = any(not (caixa[2] < c[0] or caixa[0] > c[2] or caixa[3] < c[1] or caixa[1] > c[3]) for c in caixas)
            colide |= any(caixa[0] - 6 * esc < mx < caixa[2] + 6 * esc and caixa[1] - 6 * esc < my < caixa[3] + 6 * esc
                          for mx, my in marcas)
            if not colide:
                break
        caixas.append(caixa)
        ax.annotate(txt, (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=8, color=TINTA,
                    arrowprops={"arrowstyle": "-", "color": TINTA_2, "lw": 0.5, "shrinkA": 0, "shrinkB": 5})


def main():
    d = yaml.safe_load((RAIZ / "results/etapa1.3/missoes.yaml").read_text(encoding="utf-8"))
    orb = d["criterio_selecao"]["orbita_marte"]
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    pontos = []  # (x, y, rótulo) de todos os marcadores cheios
    for classe, cor in CORES.items():
        cs = [c for c in d["candidatas"] if c["classe"] == classe]
        x = [c["total_dias"] for c in cs]
        y = [c["por_orbita_marte"][orb]["dv_total_sem_aerocaptura_km_s"] for c in cs]
        ya = [c["por_orbita_marte"][orb]["dv_total_com_aerocaptura_km_s"] for c in cs]
        ax.plot(x, y, "o", ms=9, mfc=cor, mec=SUPERFICIE, mew=2, label=f"{NOMES[classe]}: sem aerocaptura")
        ax.plot(x, ya, "o", ms=9, mfc="none", mec=cor, mew=1.5, label=f"{NOMES[classe]}: com aerocaptura")
        for c, xi, yi in zip(cs, x, y):
            if not any(abs(xi - a) < 1 and abs(yi - b) < 1e-3 for a, b, _ in pontos):  # mesma missão: um rótulo
                pontos.append((xi, yi, c["janela_ida"]))
    _rotular(fig, ax, pontos)
    ax.set_xlabel("Duração total da missão (dias)", color=TINTA_2)
    ax.set_ylabel("Δv propulsivo total (km/s)", color=TINTA_2)
    ax.set_title("Missões candidatas: Δv total × duração", color=TINTA, loc="left")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",")))
    ax.tick_params(colors=TINTA_2, labelsize=8)
    for s in ax.spines.values():
        s.set_color("#d6d5d0")
    ax.grid(color=GRADE, lw=0.5)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=8, frameon=False, labelcolor=TINTA)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.text(0.01, 0.01, f"Órbita de Marte: {orb}. Impulsivo ideal, sem perdas gravitacionais, cônicas emendadas, "
             "DE440. Gerado por tools/grafico_missoes.py.", fontsize=6.5, color=TINTA_2)
    fig.savefig(RAIZ / "results/etapa1.3/dv_x_duracao.png", dpi=150, facecolor=SUPERFICIE)


if __name__ == "__main__":
    main()
