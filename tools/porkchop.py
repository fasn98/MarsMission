"""Gera porkchop plots e mínimos de C3 por tipo para as janelas de config/janelas.yaml.

Saída (só escrita por este script):
  results/etapa1.2/porkchop_<sentido>_<janela>.png
  results/etapa1.2/minimos_<sentido>.yaml

Uso: python tools/porkchop.py terra_marte
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import spiceypy as spice  # noqa: E402
import yaml  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))


def _exclusao():
    """Faixa em torno de 180° excluída da busca de mínimos (premissa P-006)."""
    cfg = yaml.safe_load((RAIZ / "config" / "premissas.yaml").read_text(encoding="utf-8"))
    return next(p["valor"] for p in cfg["premissas"] if p["nome"] == "exclusao_angulo_180_graus")

from orbital import ephemeris as eph  # noqa: E402
from orbital import porkchop as pc  # noqa: E402

SAIDA = RAIZ / "results" / "etapa1.2"

# Paleta: tokens do guia de visualização (rampa azul sequencial; laranja para a 2ª grandeza).
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
SUPERFICIE = "#fcfcfb"
AZUL = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281", "#0d366b"]
LARANJA = "#eb6834"
CINZA = "#8a8985"


def _datas(ets):
    return np.array([np.datetime64(spice.et2utc(t, "ISOC", 0)) for t in ets])


def _utc(et):
    return spice.et2utc(et, "ISOC", 0)


def porkchop(sentido, nome, jan, cfg):
    passo = cfg["passo_dias"]
    t1 = spice.str2et(f"{jan['partida'][0]} TDB")
    t2 = spice.str2et(f"{jan['partida'][1]} TDB")
    a1 = spice.str2et(f"{jan['chegada'][0]} TDB")
    a2 = spice.str2et(f"{jan['chegada'][1]} TDB")
    etp = np.arange(t1, t2 + 1, passo * pc.DIA)
    etc = np.arange(a1, a2 + 1, passo * pc.DIA)
    g = pc.calcular_grade(cfg["partida"], cfg["chegada"], etp, etc)

    minimos = {}
    for tipo in (1, 2):
        m = pc.minimo_c3_por_tipo(cfg["partida"], cfg["chegada"], g, tipo, _exclusao())
        if m is None:
            continue
        minimos[f"tipo_{tipo}"] = {
            "partida_tdb": _utc(m["et_partida"]), "chegada_tdb": _utc(m["et_chegada"]),
            "tof_dias": round(m["tof_dias"], 2), "c3_km2_s2": round(m["c3"], 4),
            "vinf_chegada_km_s": round(m["vinf_chegada"], 4), "angulo_transf_graus": round(m["angulo"], 2),
        }

    dp, dc = _datas(etp), _datas(etc)
    X, Y = np.meshgrid(dp, dc, indexing="ij")
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor=SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    c3 = np.where(g.c3 < cfg["c3_max"], g.c3, np.nan)
    cs = ax.contour(X, Y, c3, levels=cfg["niveis_c3"], colors=AZUL[2], linewidths=1.0)
    ax.clabel(cs, fmt="%g", fontsize=7, colors=TINTA)
    vi = np.where(g.c3 < cfg["c3_max"], g.vinf_chegada, np.nan)
    cv = ax.contour(X, Y, vi, levels=cfg["niveis_vinf"], colors=LARANJA, linewidths=1.0, linestyles="--")
    ax.clabel(cv, fmt="%g", fontsize=7, colors=TINTA)
    ct = ax.contour(X, Y, g.tof_dias, levels=np.arange(100, 600, 50), colors=CINZA, linewidths=0.6, linestyles=":")
    ax.clabel(ct, fmt="%g d", fontsize=6, colors=TINTA_2)
    marcadores = {"tipo_1": ("o", "Mín. C3 tipo I"), "tipo_2": ("s", "Mín. C3 tipo II")}
    for chave, m in minimos.items():
        mk, rot = marcadores[chave]
        ax.plot(np.datetime64(m["partida_tdb"]), np.datetime64(m["chegada_tdb"]), mk, ms=8,
                mfc=TINTA, mec=SUPERFICIE, mew=2, label=f"{rot}: C3 = {m['c3_km2_s2']:.2f} km²/s²")
    ref = cfg.get("referencia")
    if ref:
        dados = yaml.safe_load((RAIZ / ref).read_text(encoding="utf-8"))["janelas"].get(nome, {})
        for chave, (mk, rot) in marcadores.items():
            if chave in dados:
                r = dados[chave]
                ax.plot(np.datetime64(r["partida"]), np.datetime64(r["chegada"]), mk, ms=9, mfc="none",
                        mec=LARANJA, mew=1.5, label=f"{rot}, NASA/TM-2010-216764: C3 = {r['c3']}")
    ax.plot([], [], color=AZUL[2], lw=1, label="C3 de partida [km²/s²]")
    ax.plot([], [], color=LARANJA, lw=1, ls="--", label="v∞ de chegada [km/s]")
    ax.plot([], [], color=CINZA, lw=0.6, ls=":", label="tempo de voo [dias]")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=8, frameon=False, labelcolor=TINTA)
    ax.set_xlabel("Data de partida (TDB)", color=TINTA_2)
    ax.set_ylabel("Data de chegada (TDB)", color=TINTA_2)
    ax.set_title(f"{cfg['titulo']} — janela {nome}", color=TINTA, loc="left")
    for eixo in (ax.xaxis, ax.yaxis):
        eixo.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.tick_params(colors=TINTA_2, labelsize=8)
    for s in ax.spines.values():
        s.set_color("#d6d5d0")
    ax.grid(color="#eceae4", lw=0.5)
    fig.autofmt_xdate()
    fig.text(0.01, 0.005, "Lambert (Izzo, 2015), cônicas emendadas, balístico, efemérides DE440 (de440s.bsp). "
             "Gerado por tools/porkchop.py.", fontsize=6, color=TINTA_2)
    fig.tight_layout()
    fig.savefig(SAIDA / f"porkchop_{sentido}_{nome}.png", dpi=150, facecolor=SUPERFICIE)
    plt.close(fig)
    return minimos


def main():
    sentido = sys.argv[1]
    cfg = yaml.safe_load((RAIZ / "config" / "janelas.yaml").read_text(encoding="utf-8"))[sentido]
    eph.carregar_kernels()
    SAIDA.mkdir(parents=True, exist_ok=True)
    resultado = {"gerado_por": "tools/porkchop.py", "sentido": sentido,
                 "partida": cfg["partida"], "chegada": cfg["chegada"], "janelas": {}}
    for nome, jan in cfg["janelas"].items():
        resultado["janelas"][nome] = porkchop(sentido, nome, jan, cfg)
        print(nome, resultado["janelas"][nome])
    (SAIDA / f"minimos_{sentido}.yaml").write_text(
        yaml.safe_dump(resultado, sort_keys=False, allow_unicode=True), encoding="utf-8")


if __name__ == "__main__":
    main()
