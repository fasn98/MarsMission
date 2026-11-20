"""Etapa 2 do plano (issue #68): verificação do orbitador só elétrico da família 1.

(a) Trechos heliocêntricos de baixo empuxo Terra→Marte e Marte→Terra com as efemérides DE440s (orbital.sims_flanagan,
    conferido contra Kepler, Lambert e [F113] em tests/test_sims_flanagan.py), sem a hipótese de órbita quase circular e
    com o crédito do v∞ do lançador (a margem no Falcon Heavy entra no objetivo, pelo C3 e pela declinação).
(b) Comparação com o caso publicado: os dois exemplos de ida do ERO em Joffre et al. 2018 [F121], Fig. 4, com a massa e
    o empuxo de Yau 2021 [F22] (outra versão do projeto). A captura do ERO é química e não é comparável.
(c) Vida dos propulsores: XIPS-25 (catálogo) e NEXT-C (em paralelo, fora do catálogo), com rodízio para que o xenônio
    por propulsor fique abaixo da vida demonstrada.

Fecho de massa como o da rota B (tools/rotas_mav.py, "só elétrico"), com os trechos heliocêntricos otimizados no lugar
do Δv quase circular: a margem de Δv (P-014) multiplica o logaritmo da razão de massas de cada trecho.

As saídas das otimizações são mínimos locais (CLAUDE.md, regra 6): os números ficam em
results/familia1/diagnostico_orbitador_so_eletrico.md, fora da comparação do CI; results/familia1/orbitador_so_eletrico.md
traz o método e as entradas e cita o diagnóstico.

Uso: python tools/orbitador_so_eletrico.py [--so-caso-publicado]
"""

from __future__ import annotations

import os

# Uma thread de BLAS por processo: os casos rodam em paralelo (ProcessPoolExecutor) e o SLSQP é pequeno.
for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_k, "1")

import argparse  # noqa: E402
import dataclasses  # noqa: E402
import datetime as dt  # noqa: E402
import math  # noqa: E402
import sys  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import orbitador_eletrico as oe  # noqa: E402
from orbital import dimensionamento as dm  # noqa: E402
from orbital import ephemeris as eph  # noqa: E402
from orbital import hibrido as hb  # noqa: E402
from orbital import lambert  # noqa: E402
from orbital import lancamento as lc  # noqa: E402
from orbital import porkchop as pc  # noqa: E402
from orbital import sims_flanagan as sf  # noqa: E402
from orbital.config import ler, parametros, v  # noqa: E402
from orbital.constantes import GM_SOL  # noqa: E402
from orbital.massa_plataformas import plataforma_orbitador  # noqa: E402

SAIDA = RAIZ / "results" / "familia1"
DIA = 86400.0
D = dt.date.fromisoformat


class NaoConverge(RuntimeError):
    pass


def br(x, n=0):
    return f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def _estado(corpo):
    def f(et):
        s = pc.estado_corpo(corpo, et)
        return s[:3], s[3:]
    return f


def _et(data):
    eph.carregar_kernels()
    return eph.tdb_para_et(f"{data}T00:00:00")


def _data(et):
    return eph.data_tdb(et)


def _declinacao(vinf):
    n = float(np.linalg.norm(vinf))
    return math.degrees(math.asin(vinf[2] / n)) if n > 0 else float("nan")


def _chute_u(estado, t0, tof, n, sentido, fracao=0.5):
    """Empuxo na direção da velocidade do planeta de partida propagada (sentido +1: a favor, para subir; −1: contra)."""
    r, v_ = estado(t0)
    u = np.empty((n, 3))
    for i in range(n):
        _, vi = sf.kepler.propagar(GM_SOL, r, v_, (i + 0.5) * tof / n)
        u[i] = sentido * fracao * vi / np.linalg.norm(vi)
    return u


def _datas_lambert(origem, destino, t_ini, t_fim, tof_min, tof_max, passo_t=5.0, passo_tof=10.0):
    """Datas do chute a frio: (partida, duração) em s com a menor soma dos v∞ de Lambert (0 revolução, prograde) na faixa."""
    melhor = None
    for t in np.arange(t_ini, t_fim + 1.0, passo_t * DIA):
        r1, v1 = origem(float(t))
        for tof in np.arange(tof_min, tof_max + 1.0, passo_tof * DIA):
            r2, v2 = destino(float(t + tof))
            try:
                sol = lambert.resolver(GM_SOL, r1, r2, float(tof))
            except (RuntimeError, ValueError):
                continue
            custo = float(np.linalg.norm(sol.v1 - v1) + np.linalg.norm(sol.v2 - v2))
            if melhor is None or custo < melhor[0]:
                melhor = (custo, float(t), float(tof))
    return melhor[1], melhor[2]


def _partida_fria(perna, base, objetivo, oc, origem, sentido, duracoes, lim_et):
    """Partida a frio: com a data de `base` fixa, tenta as durações da lista (P-122) até achar um ponto viável
    (sf.viabilizar) e otimizá-lo com as datas fixas; esse ponto é o chute da otimização com as datas livres."""
    ultimo = None
    for d in duracoes:
        tof = d * DIA
        if lim_et is not None and base["t0"] + tof > lim_et:
            continue
        fixa = dataclasses.replace(perna, t0=(base["t0"], base["t0"]), tof=(tof, tof))
        ch = {**base, "tof": tof, "u": _chute_u(origem, base["t0"], tof, perna.n_segmentos, sentido, 0.5)}
        ch, res = sf.viabilizar(fixa, ch)
        ultimo = (d, res)
        if res > oc["residuo_max"]:
            continue
        s = _resolve(fixa, objetivo, ch, oc, exigir=False)
        if s["convergiu"]:
            return s
    raise NaoConverge(f"partida a frio sem ponto viável nas durações {duracoes} (última: {ultimo})")


def _oc():
    o = ler("config/orbitador_so_eletrico.yaml")["otimizador"]
    return {k: v(o[k]) for k in ("n_segmentos", "ordem", "maxiter", "ftol", "residuo_max")}


def _resolve(perna, objetivo, chute, oc, ineq_extra=None, exigir=True, rodadas=4):
    """SLSQP com reinícios a partir do último ponto (até `rodadas`) enquanto ele para sem convergir. Convergiu quando a
    continuidade e |u| ≤ 1 ficam dentro do resíduo aceito (P-118) e o SLSQP declara sucesso ou o objetivo para de mudar
    entre dois reinícios (mudança relativa ≤ ftol × 10³, P-118)."""
    anterior = None
    for k in range(rodadas):
        s = sf.otimizar(perna, objetivo, chute, maxiter=int(oc["maxiter"]), ftol=oc["ftol"], ineq_extra=ineq_extra)
        viavel = s["residuo_max"] <= oc["residuo_max"] and s["violacao_u"] <= oc["residuo_max"]
        parado = anterior is not None and abs(s["objetivo"] - anterior) <= oc["ftol"] * 1e3 * max(1.0, abs(anterior))
        s["convergiu"], s["viavel"], s["rodadas"] = bool(viavel and (s["sucesso"] or parado)), bool(viavel), k + 1
        s["criterio"] = "sucesso do SLSQP" if s["sucesso"] else ("objetivo estacionário entre reinícios" if parado else "não convergiu")
        if s["convergiu"]:
            break
        anterior = s["objetivo"] if viavel else None
        chute = s
    if exigir and not s["convergiu"]:
        raise NaoConverge(f"otimizador não convergiu: {s['mensagem']}; resíduo {s['residuo_max']:.2e}")
    return s


def _resumo(s, motor, mu=GM_SOL):
    """Grandezas de uma solução: Δv, arcos de empuxo e a conferência pela propagação contínua."""
    u = s["u"]
    a = np.linalg.norm(u, axis=1)
    dt_ = s["tof"] / len(u)
    arcos, m, dv_arco, em_arco = [], s["m0"], 0.0, False
    for ai in a:
        m2 = m - ai * motor.vazao_kg_s * dt_
        d = motor.c_km_s * math.log(m / m2)
        if ai > 1e-3:
            dv_arco, em_arco = dv_arco + d, True
        elif em_arco:
            arcos.append(dv_arco)
            dv_arco, em_arco = 0.0, False
        m = m2
    if em_arco:
        arcos.append(dv_arco)
    return {"dv_km_s": motor.c_km_s * math.log(s["m0"] / s["mf"]), "arcos_dv_km_s": arcos,
            "fracao_tempo_com_empuxo": float(np.mean(a > 1e-3)), "aceleracao_inicial_m_s2": motor.empuxo_n / s["m0"]}


def _confere_continuo(perna, s):
    """Diferença entre o estado final da propagação contínua do mesmo perfil e o alvo (km, km/s)."""
    rp, vp = perna.estado_partida(s["t0"])
    rc, vc = perna.estado_chegada(s["t0"] + s["tof"])
    r, v_, _ = sf.propagar_continuo(perna.mu, rp, vp + s["vinf0"], s["m0"], s["tof"], s["u"], perna.motor)
    return float(np.linalg.norm(r - rc)), float(np.linalg.norm(v_ - (vc + s["vinf1"])))


# ---------------------------------------------------------------- (b) caso publicado

def _polo_marte(et):
    """Eixo de rotação de Marte (IAU_MARS, pck00011) no J2000, na época."""
    import spiceypy as spice
    eph.carregar_kernels()
    return np.asarray(spice.pxform("IAU_MARS", "J2000", et))[:, 2]


def caso_publicado(arg):
    """Varredura de empuxo de um exemplo de [F121], com datas e |v∞| publicados e massa inicial de [F22]. Com
    `declinacoes`, também as declinações publicadas (partida no equador da Terra J2000; chegada no equador de Marte), P-119."""
    nome, declinacoes = arg
    cfg = ler("config/orbitador_so_eletrico.yaml")["caso_publicado"]
    c = cfg["casos"][nome]
    oc = _oc()
    isp = v(cfg["isp_s"]) if nome == "esquerda" else v(cfg["isp_direita_s"])
    m0 = v(cfg["massa_inicial_kg"])
    t0, t1 = _et(c["partida"]["valor"]), _et(c["chegada"]["valor"])
    vi0, vi1 = v(c["vinf_partida_km_s"]), v(c["vinf_chegada_km_s"])
    terra, marte = _estado(eph.TERRA), _estado(eph.BARICENTRO_MARTE)
    n = int(oc["n_segmentos"])
    _, vT = terra(t0)
    extra = None
    if declinacoes:
        d0 = math.radians(v(c["declinacao_partida_graus"]))
        polo = _polo_marte(t1)
        d1 = math.radians(v(c["declinacao_chegada_graus"])) if "declinacao_chegada_graus" in c else None

        def extra(t0_, tof, m0_, mf, a, b):
            g = [a[2] / max(np.linalg.norm(a), 1e-9) - math.sin(d0)]
            if d1 is not None:
                g.append(float(b @ polo) / max(np.linalg.norm(b), 1e-9) - math.sin(d1))
            g = np.array(g) * 100.0
            return np.r_[g + 1e-6, 1e-6 - g]   # igualdade como duas desigualdades com folga de 1e-8 no seno
    chute = {"t0": t0, "tof": t1 - t0, "m0": m0, "mf": 0.85 * m0, "vinf0": vi0 * vT / np.linalg.norm(vT),
             "vinf1": np.zeros(3), "u": _chute_u(terra, t0, t1 - t0, n, +1)}
    linhas = []
    for empuxo in cfg["empuxos_n"]["valor"]:
        motor = sf.Motor(empuxo, isp)
        p = sf.Perna(GM_SOL, terra, marte, motor, n, (t0, t0), (t1 - t0, t1 - t0), (vi0, vi0), (vi1, vi1), (m0, m0),
                     (0.2 * m0, m0))
        s = _resolve(p, lambda t0_, tof, m0_, mf, a, b: -mf / 1000.0, chute, oc, ineq_extra=extra, exigir=False)
        lin = {"empuxo_n": empuxo, "convergiu": s["convergiu"], "viavel": s["viavel"], "mensagem": s["mensagem"],
               "iteracoes": s["iteracoes"], "rodadas": s["rodadas"], "residuo_max": s["residuo_max"]}
        if s["viavel"]:
            erro_r, erro_v = _confere_continuo(p, s)
            lin.update(_resumo(s, motor))
            lin.update({"declinacao_partida_graus": _declinacao(s["vinf0"]), "mf_kg": s["mf"],
                        "declinacao_chegada_marte_graus": (math.degrees(math.asin(float(s["vinf1"] @ _polo_marte(t1)) / np.linalg.norm(s["vinf1"])))
                                                           if np.linalg.norm(s["vinf1"]) > 0 else None),
                        "continuo_erro_km": erro_r, "continuo_erro_km_s": erro_v})
            chute = {**chute, **{k: s[k] for k in ("mf", "vinf0", "vinf1", "u")}}
        linhas.append(lin)
    pub = v(c["dv_publicado_km_s"])
    conv = [x for x in linhas if x["convergiu"]]
    equivalente = None
    for a_, b_ in zip(conv, conv[1:]):   # empuxos em ordem decrescente: o Δv cresce
        if (a_["dv_km_s"] - pub) * (b_["dv_km_s"] - pub) <= 0 and a_["dv_km_s"] != b_["dv_km_s"]:
            equivalente = a_["empuxo_n"] + (pub - a_["dv_km_s"]) * (b_["empuxo_n"] - a_["empuxo_n"]) / (b_["dv_km_s"] - a_["dv_km_s"])
    return {"caso": nome, "declinacoes": declinacoes, "nome": c["nome"], "massa_inicial_kg": m0, "isp_s": isp,
            "dv_publicado_km_s": pub, "linhas": linhas, "empuxo_equivalente_n": equivalente,
            "aceleracao_equivalente_m_s2": equivalente / m0 if equivalente else None,
            "empuxo_max_publicado_n": v(cfg["empuxo_max_publicado_n"])}


# ---------------------------------------------------------------- (a) e (c) família 1

def _entradas():
    p, po = parametros(), ler("config/parametros_orbitais.yaml")
    dcfg, pcfg, ecfg, cu, lcfg = (ler(f"config/{x}.yaml") for x in ("dimensionamento", "plataformas", "eletrica", "carga_util", "lancadores"))
    se_cfg = ler("config/orbitador_so_eletrico.yaml")
    _, _, piores = dm.casos(dcfg, p)
    orc_ret = dm.orcamento(piores["retorno"], dcfg, p)
    ate_marte, capsula, descartado = dm.carga(dcfg["caso_base"]["carga_util"], cu, float(dcfg["caso_base"]["acrescimo_capsula"]))
    est = dcfg["estagios"]
    fm = ler("results/familia1/missao.yaml")
    return {"p": p, "po": po, "dcfg": dcfg, "pcfg": pcfg, "ecfg": ecfg, "lcfg": lcfg, "se": se_cfg, "orc_ret": orc_ret,
            "ate_marte": ate_marte, "capsula": capsula, "descartado": descartado,
            "isp_q": v(est["insercao_marte"]["isp_s"]), "eps_r": v(est["retorno"]["fracao_estrutural"]),
            "f": 1 + v(dcfg["margem_dv"]), "hill": ler("results/etapa3.1/queima_finita.yaml")["raio_hill_km"],
            "missao": fm, "t_enc": v(ecfg["operacao"]["tempo_encontro_dias"]) * DIA}


def _sistema(nome, n, e):
    """SistemaEletrico do catálogo (XIPS-25) ou da avaliação em paralelo (NEXT-C), sem mudar o catálogo."""
    ecfg = dict(e["ecfg"])
    if nome not in ecfg["propulsores"]:
        ecfg = {**ecfg, "propulsores": {**ecfg["propulsores"], nome: e["se"]["propulsores"][nome]}}
    return oe.sistema(nome, n, ecfg, e["pcfg"])


def _capacidade(e):
    """(capacidade oficial, capacidade suave, maior C3 publicado). A oficial é a de orbital.lancamento (interpolação linear
    da curva do ELVPerf [F79], multiplicador de DLA, menos o adaptador da P-097) e dá a margem reportada. A suave troca só
    a interpolação em C3 por uma PCHIP (monótona, nos mesmos pontos) e é usada no objetivo do otimizador, que não converge
    nas quinas da interpolação linear."""
    from scipy.interpolate import PchipInterpolator
    lan = e["lcfg"]["lancadores"][e["se"]["missao"]["lancador"]]
    cfg = e["lcfg"]
    pfm = cfg["centro"]["plataformas"].get(lan.get("plataforma"), {})
    imax = lc.inclinacao(pfm.get("latitude_graus", v(cfg["centro"]["latitude_graus"])), cfg["centro"]["azimute_graus"]["valor"][0])
    adapt = lc.adaptador_p097()[0]
    suave_c3 = PchipInterpolator(lan["c3"]["pontos"], lan["c3"]["massa_kg"])

    def cap(vinf):
        c3 = float(vinf @ vinf)
        k = lc.capacidade_direta(lan, c3, _declinacao(vinf) if c3 > 0 else 0.0, cfg, imax)[0]
        return k - adapt if k == k else float("nan")

    def cap_suave(vinf):
        c3 = float(vinf @ vinf)
        lin = lc.interpolar(c3, lan["c3"]["pontos"], lan["c3"]["massa_kg"])
        if lin != lin or lin <= 0:
            return float("nan")
        k = lc.capacidade_direta(lan, c3, _declinacao(vinf) if c3 > 0 else 0.0, cfg, imax)[0]
        return k * float(suave_c3(c3)) / lin - adapt   # mesmo fator de DLA
    return cap, cap_suave, max(lan["c3"]["pontos"])


def fecho(nome, n, h, e=None, chutes=None):
    """Fecho de massa e linha do tempo do orbitador só elétrico com n propulsores ativos e encontro a h km."""
    e = e or _entradas()
    oc = _oc()
    ms = e["se"]["missao"]
    duty = v(e["se"]["operacao"]["ciclo_trabalho"])
    p, f = e["p"], e["f"]
    mu, R = p.mu_marte, v(e["po"]["raio_marte_km"])
    r_e = R + h
    se0 = _sistema(nome, n, e)
    vida = v(e["se"]["propulsores"][nome]["vida_kg"])
    reservas = int(v(e["ecfg"]["operacao"]["reservas"]))
    motor = sf.Motor(se0.empuxo_total_n * duty, se0.isp_s)
    cx, c = se0.isp_s * sf.G0, e["isp_q"] * sf.G0
    k_r = e["eps_r"] / (1 - e["eps_r"])
    plat = plataforma_orbitador(e["pcfg"], e["po"], h, h)
    carga = e["ate_marte"] - e["descartado"] - e["capsula"] + plat
    orc = e["orc_ret"]
    cap, cap_suave, c3_max = _capacidade(e)
    terra, marte = _estado(eph.TERRA), _estado(eph.BARICENTRO_MARTE)
    nseg = int(oc["n_segmentos"])
    fm = e["missao"]
    ref = ler("results/etapa7.2/rotas_mav.yaml")["missao"]
    conj = [{k: (D(x[k]) if isinstance(x[k], str) else x[k]) for k in x} for x in fm["conjuncoes"]]
    folga, rec = int(fm["folga_conjuncao_dias"]), int(fm["recuperacao_dias"])
    lim_ultimo = max(D(x["lancamento_mav_mais_tarde"]) if isinstance(x["lancamento_mav_mais_tarde"], str) else x["lancamento_mav_mais_tarde"] for x in fm["casos"])
    t0min, t0max = _et(ms["partida_terra"]["valor"]["min"]), _et(ms["partida_terra"]["valor"]["max"])

    def espiral(r_ini, r_fim, m):
        _, t_dec, _, mf_ = hb.tempos_espiral(mu, R, r_ini, r_fim, m, se0, fator_dv=f)
        return t_dec / duty, mf_

    # chutes iniciais
    ida0 = (chutes or {}).get("ida")
    volta0 = (chutes or {}).get("volta")
    if chutes and chutes.get("empuxo_n"):
        # mesma trajetória com outro empuxo máximo: u escala pela razão dos empuxos (a vazão escala junto, Isp igual)
        k = chutes["empuxo_n"] / motor.empuxo_n
        if k <= 1.0 and chutes.get("isp_s") == motor.isp_s:
            ida0, volta0 = {**ida0, "u": ida0["u"] * k}, {**volta0, "u": volta0["u"] * k}
    m_chegada = float(ida0["mf"]) if ida0 is not None else 6000.0   # com chute (n anterior da cadeia), a massa dele
    inst = n + reservas
    hist = []
    for it in range(int(v(ms["iteracoes_fecho"]))):
        # ---- ida: m0 livre, mf = massa na chegada; objetivo: maior margem no lançador
        t_d_est = espiral(e["hill"], r_e, m_chegada)[0] * DIA / DIA
        lim_et = _et(lim_ultimo.isoformat()) - t_d_est
        pi = sf.Perna(GM_SOL, terra, marte, motor, nseg, (t0min, t0max),
                      (ms["ida_dias"]["valor"]["min"] * DIA, ms["ida_dias"]["valor"]["max"] * DIA),
                      (0.0, math.sqrt(c3_max)), (0.0, v(ms["vinf_chegada_marte_km_s"])), (0.3 * m_chegada, 4.0 * m_chegada),
                      (m_chegada, m_chegada))

        def obj_ida(t0, tof, m0, mf, a, b):
            k = cap_suave(a)
            return m0 / k if k > 0 else 1e3
        extra = lambda t0, tof, m0, mf, a, b: np.array([(lim_et - (t0 + tof)) / DIA])  # noqa: E731
        if ida0 is None:
            t0 = min(max(_et(ms["partida_frio"]["valor"]), t0min), t0max)
            _, vT = terra(t0)
            base = {"t0": t0, "m0": 1.6 * m_chegada, "mf": m_chegada, "vinf0": 3.0 * vT / np.linalg.norm(vT), "vinf1": np.zeros(3)}
            ida0 = _partida_fria(pi, base, obj_ida, oc, terra, +1, ms["duracoes_frio_ida_dias"]["valor"], lim_et)
        si = _resolve(pi, obj_ida, {**ida0, "mf": m_chegada}, oc, ineq_extra=extra)
        ida0 = si
        # margem de Δv (P-014) no logaritmo da razão de massas
        razao_ida = (si["m0"] / si["mf"]) ** f
        chegada_et = si["t0"] + si["tof"]
        # ---- Marte e retorno, de trás para a frente
        t_d, _ = espiral(e["hill"], r_e, m_chegada)
        pronto = D(_data(chegada_et)) + dt.timedelta(days=math.ceil(t_d / DIA))
        lanc0 = max(pronto, D(ref["lancamento_mav_mais_cedo"]), D(ref["chegada"]))
        for cj in conj:
            if cj["inicio"] - dt.timedelta(days=folga) <= lanc0 <= cj["fim"] + dt.timedelta(days=rec):
                lanc0 = cj["fim"] + dt.timedelta(days=rec)
        prox = next((cj for cj in conj if cj["inicio"] > lanc0), None)
        lanc_tarde = prox["inicio"] - dt.timedelta(days=folga) if prox else None
        # massas: ponto fixo com a razão da volta da iteração anterior
        razao_volta = (volta0["m0"] / volta0["mf"]) ** f if volta0 else 1.25
        pr = px = 0.0
        for _ in range(200):
            xe_inst = max(inst, math.ceil(px / vida) + reservas) if px > 0 else inst
            se = dataclasses.replace(se0, n_instalados=xe_inst)
            mf_ = carga + se.massa_seca_kg() + k_r * pr + se.inerte_por_kg_xenonio * px
            b_desv = mf_ * math.exp(f * orc["desvio_orbitador"] / c)
            a_cap = b_desv + e["capsula"]
            b_volta = a_cap * razao_volta
            b_sub = b_volta * math.exp(f * hb.dv_circular(mu, r_e, e["hill"]) / cx)
            b_enc = b_sub * math.exp(f * orc["encontro_e_manutencao_marte"] / c)
            a_desc = b_enc + e["descartado"]
            b_desc = a_desc * math.exp(f * hb.dv_circular(mu, e["hill"], r_e) / cx)
            nr = (b_desv - mf_) + (b_enc - b_sub)
            nx = (b_volta - a_cap) + (b_sub - b_volta) + (b_desc - a_desc)   # a ida entra abaixo
            nx += b_desc * (razao_ida - 1)
            if abs(nr - pr) < 1e-9 and abs(nx - px) < 1e-9:
                break
            pr, px = nr, nx
        else:
            raise RuntimeError("massas não convergiram")
        inst = xe_inst
        _, t_s_real, _, _ = hb.tempos_espiral(mu, R, r_e, e["hill"], b_sub, se0, fator_dv=f)
        t_s = t_s_real / duty
        partida_cedo = lanc0 + dt.timedelta(days=math.ceil(e["t_enc"] / DIA + t_s / DIA))
        # ---- volta: m0 = massa no início do trecho heliocêntrico; objetivo: maior massa final
        t2 = _et(partida_cedo.isoformat())
        pv = sf.Perna(GM_SOL, marte, terra, motor, nseg, (t2, t2 + v(ms["espera_retorno_dias"]) * DIA),
                      (ms["volta_dias"]["valor"]["min"] * DIA, ms["volta_dias"]["valor"]["max"] * DIA),
                      (0.0, 0.0), (0.0, v(ms["vinf_chegada_terra_max_km_s"])), (b_volta, b_volta), (0.2 * b_volta, b_volta))
        obj_volta = lambda t0, tof, m0, mf, a, b: -mf / 1000.0  # noqa: E731
        if volta0 is None:
            base = {"t0": t2, "m0": b_volta, "mf": 0.85 * b_volta, "vinf0": np.zeros(3), "vinf1": np.zeros(3)}
            volta0 = _partida_fria(pv, base, obj_volta, oc, marte, -1, ms["duracoes_frio_volta_dias"]["valor"], None)
        sv = _resolve(pv, obj_volta, {**volta0, "m0": b_volta, "t0": max(volta0["t0"], t2)}, oc)
        volta0 = sv
        hist.append({"iteracao": it, "massa_chegada_kg": m_chegada, "orbitador_kg": razao_ida * b_desc, "xenonio_kg": px})
        m_chegada = b_desc
        ida0 = {**si, "mf": m_chegada}
    # resultado da última iteração (ida resolvida para a massa de chegada anterior; a diferença fica no histórico)
    m0_lanc = b_desc * razao_ida
    erro_ida = _confere_continuo(pi, si)
    erro_volta = _confere_continuo(pv, sv)
    margem = cap(si["vinf0"]) / m0_lanc - 1
    se_f = dataclasses.replace(se0, n_instalados=inst)
    partida_marte = D(_data(sv["t0"]))
    return {"propulsor": nome, "n_ativos": n, "altitude_km": h, "n_instalados": inst, "reservas": reservas,
            "potencia_kw": se0.potencia_total_w / 1e3, "vida_kg": vida, "xenonio_kg": px,
            "xenonio_por_propulsor_kg": px / (inst - reservas), "dentro_da_vida": px / (inst - reservas) <= vida,
            "massa_propulsores_e_ppu_kg": inst * (se0.massa_propulsor_kg + se0.massa_ppu_kg),
            "massa_seca_eletrica_kg": se_f.massa_seca_kg(), "orbitador_kg": m0_lanc, "margem_falcon_heavy": margem,
            "c3_km2_s2": float(si["vinf0"] @ si["vinf0"]), "dla_graus": _declinacao(si["vinf0"]),
            "partida_terra": _data(si["t0"]), "ida_dias": si["tof"] / DIA, "chegada_marte": _data(chegada_et),
            "dv_ida_km_s": cx * math.log(si["m0"] / si["mf"]), "descida_dias": t_d / DIA, "pronto_no_encontro": pronto.isoformat(),
            "ultimo_lancamento_mav": lim_ultimo.isoformat(), "pronto_antes_do_ultimo": pronto <= lim_ultimo,
            "lancamento_mav": lanc0.isoformat(), "lancamento_mav_mais_tarde": lanc_tarde.isoformat() if lanc_tarde else None,
            "subida_dias": t_s / DIA, "partida_marte_mais_cedo": partida_cedo.isoformat(), "partida_marte": partida_marte.isoformat(),
            "volta_dias": sv["tof"] / DIA, "chegada_terra": _data(sv["t0"] + sv["tof"]), "vinf_chegada_terra_km_s": float(np.linalg.norm(sv["vinf1"])),
            "dv_volta_km_s": cx * math.log(sv["m0"] / sv["mf"]),
            "fecha": bool(margem >= 0 and pronto <= lim_ultimo and px / (inst - reservas) <= vida),
            "historico": hist, "erro_continuo_ida_km_e_km_s": erro_ida, "erro_continuo_volta_km_e_km_s": erro_volta,
            "otimizador": {"ida": (si["mensagem"], si["iteracoes"], si["residuo_max"]), "volta": (sv["mensagem"], sv["iteracoes"], sv["residuo_max"])},
            "_chutes": {"ida": si, "volta": sv, "empuxo_n": motor.empuxo_n, "isp_s": motor.isp_s}}


def _cadeia(arg):
    """n crescente para um propulsor e uma órbita: cada fecho parte da solução do n anterior (partida a quente). Depois,
    os que não convergiram são refeitos a partir da solução do vizinho convergido seguinte (n + 1, ..., em ordem)."""
    nome, h, ns = arg
    out, chutes, sol = [], None, {}
    for n in ns:
        try:
            r = fecho(nome, n, h, chutes=chutes)
            chutes = sol[n] = r.pop("_chutes")
        except NaoConverge as x:
            r = {"propulsor": nome, "n_ativos": n, "altitude_km": h, "erro": str(x)}
        out.append(r)
    for i, n in enumerate(ns):
        if "erro" not in out[i]:
            continue
        viz = next((m for m in ns[i + 1:] if m in sol), None)
        if viz is None:
            continue
        ch = {**sol[viz], "empuxo_n": None}   # empuxo maior no vizinho: u não escala (|u| ficaria > 1); parte do mesmo u
        try:
            r = fecho(nome, n, h, chutes=ch)
            sol[n] = r.pop("_chutes")
            r["nota"] = f"convergiu na segunda passada, a partir de n = {viz}"
            out[i] = r
        except NaoConverge as x:
            out[i]["erro"] += f"; segunda passada, a partir de n = {viz}: {x}"
    return out


def _sci(x):
    return f"{x:.1e}".replace(".", ",").replace("-", "−")


def escreve(casos, fam):
    cfg = ler("config/orbitador_so_eletrico.yaml")
    cp, ms, pr = cfg["caso_publicado"], cfg["missao"], cfg["propulsores"]
    oc = _oc()
    md = ["# Orbitador só elétrico da família 1: trajetória de baixo empuxo e fecho de massa (gerado por tools/orbitador_so_eletrico.py)", "",
          "Etapa 2 do plano (issue #68). Plano aprovado pelo Fabio em 2026-11-20. **Calculado, NÃO validado.**", "",
          "**Os números estão em `results/familia1/diagnostico_orbitador_so_eletrico.md`**, fora da comparação do CI: as "
          "trajetórias otimizadas são mínimos locais (CLAUDE.md, regra 6). Este arquivo traz o método e as entradas.", "",
          "## Método", "",
          "- **(a) Trechos heliocêntricos:** transcrição de Sims–Flanagan de ordem 4 (`orbital.sims_flanagan`) com as efemérides "
          f"DE440s, {int(oc['n_segmentos'])} segmentos por trecho, otimizada com SLSQP (P-118). Conferências em "
          "`tests/test_sims_flanagan.py`: empuxo zero contra Kepler e Lambert, aceleração tangencial constante contra [F113] p. 31.",
          "- **Ida:** partida da Terra com o v∞ do lançador (variável), chegada ao raio de Hill de Marte com v∞ = 0; objetivo: a "
          f"maior margem no {ms['lancador']} pela curva C3 × massa e pela declinação ([F79]). Restrição: o orbitador fica pronto "
          "no encontro até o último lançamento do MAV da família 1 (`results/familia1/missao.yaml`).",
          "- **Marte:** espirais de descida e de subida como na rota B (`orbital.hibrido`, verificadas na Etapa 3.2), com o motor "
          "desligado no eclipse; MAV lançado pela regra da família 1 (conjunções, recuperação, folga de 60 d).",
          "- **Volta:** partida do raio de Hill com v∞ = 0 a partir da partida mais cedo; objetivo: a maior massa final.",
          "- **Fecho de massa:** o da rota B (`tools/rotas_mav.py`), com a razão de massas de cada trecho heliocêntrico "
          f"otimizado no lugar do Δv quase circular; a margem de Δv (P-014) multiplica o logaritmo da razão. "
          f"{int(v(ms['iteracoes_fecho']))} iterações entre a ida e o fecho (P-122).",
          f"- **Ciclo de trabalho:** {br(v(cfg['operacao']['ciclo_trabalho']) * 100)} % (P-120, valor do Dawn [F279] p. 611).",
          "- **(c) Vida e rodízio:** propulsores além dos ativos até o xenônio por propulsor ficar abaixo da vida demonstrada, "
          "cada um com a sua PPU (P-121).", "",
          "## Propulsores", "",
          "| Propulsor | No catálogo (ADR 0013) | Vida demonstrada (kg de Xe) | Fonte da vida | Voo |", "| :- | :- | -: | :- | :- |",
          f"| XIPS-25 | sim | {br(v(pr['XIPS-25']['vida_kg']))} | {pr['XIPS-25']['vida_kg']['fonte']} | [F119] p. 1 |",
          f"| NEXT-C | não (avaliação em paralelo, decisão do Fabio em 2026-11-20) | {br(v(pr['NEXT-C']['vida_kg']))} | {pr['NEXT-C']['vida_kg']['fonte']} | {pr['NEXT-C']['voo']} |", "",
          "## (b) Caso publicado", "",
          "Joffre et al. 2018 [F121], Fig. 4, p. 5: dois exemplos de ida do ERO. Massa inicial e empuxo de Yau 2021 [F22] "
          "(outra versão do projeto). O ERO não é comparável na captura: ela é química ([F280] p. 6).", "",
          "| Exemplo | Partida | Chegada | v∞ de partida (km/s) | v∞ de chegada (km/s) | Δv publicado (km/s) |", "| :- | :- | :- | -: | -: | -: |"]
    for k, c in cp["casos"].items():
        md.append(f"| {c['nome']} | {c['partida']['valor']} | {c['chegada']['valor']} | {br(v(c['vinf_partida_km_s']), 2)} | "
                  f"{br(v(c['vinf_chegada_km_s']), 2)} | {br(v(c['dv_publicado_km_s']), 2)} |")
    md += ["", "Configurações da família 1 avaliadas: " + "; ".join(
        f"{k}: {', '.join(str(x) for x in ns)} ativos" for k, ns in ms["n_ativos"]["valor"].items())
        + f"; encontro a {' e '.join(str(x) for x in ms['altitudes_km']['valor'])} km.", ""]
    (SAIDA / "orbitador_so_eletrico.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    d = ["# Diagnóstico do orbitador só elétrico da família 1 (gerado por tools/orbitador_so_eletrico.py)", "",
         "Fora da comparação do CI (regra 6): soluções de otimização (mínimos locais). Calculado, NÃO validado.", "",
         "## (b) Caso publicado: Joffre 2018 [F121] com massa e empuxo de Yau 2021 [F22]", ""]
    for c in casos:
        var = "com as declinações publicadas impostas" if c["declinacoes"] else "só com os módulos de v∞ publicados"
        eq = (f"empuxo em que o Δv calculado iguala o publicado: {br(c['empuxo_equivalente_n'], 3)} N "
              f"({_sci(c['aceleracao_equivalente_m_s2'])} m/s² com {br(c['massa_inicial_kg'])} kg), contra o máximo de "
              f"{br(c['empuxo_max_publicado_n'], 2)} N de [F22]") if c["empuxo_equivalente_n"] else \
             "o Δv publicado não fica entre dois empuxos convergidos da varredura"
        d += [f"### {c['nome']}, {var}", "", f"Δv publicado {br(c['dv_publicado_km_s'], 2)} km/s; Isp {br(c['isp_s'])} s; {eq}.", "",
              "| Empuxo (N) | Convergiu | Critério | Δv (km/s) | Δv dos arcos (km/s) | δ partida (°) | δ chegada, equador de Marte (°) | Erro contínuo (km; km/s) |",
              "| -: | :- | :- | -: | :- | -: | -: | :- |"]
        for x in c["linhas"]:
            if x.get("dv_km_s") is None:
                d.append(f"| {br(x['empuxo_n'], 2)} | não | {x['mensagem']} | — | — | — | — | — |")
                continue
            dch = "—" if x["declinacao_chegada_marte_graus"] is None else br(x["declinacao_chegada_marte_graus"], 2)
            d.append(f"| {br(x['empuxo_n'], 2)} | {'sim' if x['convergiu'] else 'não'} | {x['mensagem']} | {br(x['dv_km_s'], 3)} | "
                     f"{', '.join(br(a, 3) for a in x['arcos_dv_km_s'])} | {br(x['declinacao_partida_graus'], 2)} | {dch} | "
                     f"{br(x['continuo_erro_km'])}; {_sci(x['continuo_erro_km_s'])} |")
        d.append("")
    d += ["## (a) e (c) Família 1", "",
          "| Propulsor | Ativos | Encontro (km) | Instalados | Potência (kW) | Xe (kg) | Xe por propulsor (kg) | Vida (kg) | Propulsores + PPU (kg) | Orbitador (kg) | Margem no Falcon Heavy | C3 (km²/s²) | DLA (°) | Partida da Terra | Ida (d) | Chegada a Marte | Descida (d) | Pronto no encontro | Último lançamento do MAV | Lançamento do MAV | Subida (d) | Partida de Marte | Volta (d) | Chegada à Terra | Fecha? |",
          "| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- | -: | :- | :- | :- | -: | :- | -: | :- | :- |"]
    for r in fam:
        if "erro" in r:
            d.append(f"| {r['propulsor']} | {r['n_ativos']} | {br(r['altitude_km'])} | " + " | ".join(["—"] * 21) + f" | **{r['erro']}** |")
            continue
        d.append(f"| {r['propulsor']} | {r['n_ativos']} | {br(r['altitude_km'])} | {r['n_instalados']} | {br(r['potencia_kw'], 1)} | {br(r['xenonio_kg'])} | "
                 f"{br(r['xenonio_por_propulsor_kg'])} | {br(r['vida_kg'])} | {br(r['massa_propulsores_e_ppu_kg'])} | {br(r['orbitador_kg'])} | "
                 f"{br(r['margem_falcon_heavy'] * 100, 1)} % | {br(r['c3_km2_s2'], 2)} | {br(r['dla_graus'], 1)} | {r['partida_terra']} | {br(r['ida_dias'])} | "
                 f"{r['chegada_marte']} | {br(r['descida_dias'])} | {r['pronto_no_encontro']} | {r['ultimo_lancamento_mav']} | {r['lancamento_mav']} | "
                 f"{br(r['subida_dias'])} | {r['partida_marte']} | {br(r['volta_dias'])} | {r['chegada_terra']} | {'**sim**' if r['fecha'] else 'não'} |")
    d += ["", "### Convergência", "",
          "| Propulsor | Ativos | Encontro (km) | Δv ida (km/s) | Δv volta (km/s) | v∞ na Terra (km/s) | Mudança do orbitador na última iteração do fecho | Erro contínuo da ida (km; km/s) | Erro contínuo da volta (km; km/s) | Otimizador (ida; volta) | Nota |",
          "| :- | -: | -: | -: | -: | -: | -: | :- | :- | :- | :- |"]
    for r in fam:
        if "erro" in r:
            continue
        h = r["historico"]
        mud = abs(h[-1]["orbitador_kg"] - h[-2]["orbitador_kg"]) / h[-1]["orbitador_kg"] if len(h) > 1 else float("nan")
        oi, ov = r["otimizador"]["ida"], r["otimizador"]["volta"]
        d.append(f"| {r['propulsor']} | {r['n_ativos']} | {br(r['altitude_km'])} | {br(r['dv_ida_km_s'], 3)} | {br(r['dv_volta_km_s'], 3)} | "
                 f"{br(r['vinf_chegada_terra_km_s'], 2)} | {_sci(mud)} | {br(r['erro_continuo_ida_km_e_km_s'][0])}; {_sci(r['erro_continuo_ida_km_e_km_s'][1])} | "
                 f"{br(r['erro_continuo_volta_km_e_km_s'][0])}; {_sci(r['erro_continuo_volta_km_e_km_s'][1])} | {oi[0]}, {oi[1]} it.; {ov[0]}, {ov[1]} it. | {r.get('nota', '—')} |")
    (SAIDA / "diagnostico_orbitador_so_eletrico.md").write_text("\n".join(d) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--so-caso-publicado", action="store_true")
    a = ap.parse_args()
    ms = ler("config/orbitador_so_eletrico.yaml")["missao"]
    variantes = [("esquerda", False), ("esquerda", True), ("direita", False), ("direita", True)]
    cadeias = [] if a.so_caso_publicado else [(nome, float(h), ns) for h in ms["altitudes_km"]["valor"]
                                               for nome, ns in ms["n_ativos"]["valor"].items()]
    with ProcessPoolExecutor(max_workers=max(1, min(os.cpu_count() or 1, len(variantes) + len(cadeias)))) as ex:
        ff = [ex.submit(_cadeia, x) for x in cadeias]
        fc = [ex.submit(caso_publicado, x) for x in variantes]
        casos, fam = [f.result() for f in fc], [r for f in ff for r in f.result()]
    SAIDA.mkdir(parents=True, exist_ok=True)
    escreve(casos, fam)


if __name__ == "__main__":
    main()
