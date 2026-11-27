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

Verificar, não reotimizar (decisão do Fabio, 2026-11-24): as otimizações (mínimos locais, que mudam entre CPUs) rodam
fora do CI e as soluções vão para data/orbitador_so_eletrico/ (--salva-solucoes); a regeneração só as verifica
(--verifica: propaga os comandos gravados e confere continuidade, restrições e conclusões). O arquivo comparado traz a
existência de trajetória verificada que fecha e as margens como limites inferiores; os números ficam em
results/familia1/diagnostico_orbitador_so_eletrico.md, fora da comparação (CLAUDE.md, regra 6).

Uso: python tools/orbitador_so_eletrico.py [--caso-publicado | --verifica | --bloco PROPULSOR ALTITUDE N_MAX-N_MIN |
     --salva-solucoes ROTULO PASTA DESCRICAO [--salva-solucoes ...]]
(sem argumentos: a otimização local, as cadeias em paralelo e o caso publicado; depois, --salva-solucoes com as pastas
dos blocos e --verifica atualizam data/ e results/)
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
import time  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import yaml  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import orbitador_eletrico as oe  # noqa: E402
from orbital import dimensionamento as dm  # noqa: E402
from orbital import ephemeris as eph  # noqa: E402
from orbital import hibrido as hb  # noqa: E402
from orbital import lancamento as lc  # noqa: E402
from orbital import porkchop as pc  # noqa: E402
from orbital import sims_flanagan as sf  # noqa: E402
from orbital.config import ler, nativo, parametros, v  # noqa: E402
from orbital.constantes import GM_SOL  # noqa: E402
from orbital.massa_plataformas import plataforma_orbitador  # noqa: E402

SAIDA = RAIZ / "results" / "familia1"
DIA = 86400.0
D = dt.date.fromisoformat


class NaoConverge(RuntimeError):
    """Sem solução convergida; `residuo` é o menor resíduo de continuidade alcançado (None se nenhum ponto foi avaliado)."""

    def __init__(self, msg, residuo=None):
        super().__init__(msg)
        self.residuo = residuo


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


def _ecl_para_eq():
    """Rotação de ECLIPJ2000 (referencial dos estados, orbital.porkchop) para J2000 (equador da Terra); constante."""
    import spiceypy as spice
    eph.carregar_kernels()
    return np.asarray(spice.pxform(pc.FRAME, "J2000", 0.0))


def _declinacao(vinf):
    """Declinação (graus) do vetor v∞ no equador da Terra (J2000), a partir do vetor em ECLIPJ2000."""
    n = float(np.linalg.norm(vinf))
    return math.degrees(math.asin(float((_ecl_para_eq() @ vinf)[2]) / n)) if n > 0 else float("nan")


def _chute_u(estado, t0, tof, n, sentido, fracao=0.5):
    """Empuxo na direção da velocidade do planeta de partida propagada (sentido +1: a favor, para subir; −1: contra)."""
    r, v_ = estado(t0)
    u = np.empty((n, 3))
    for i in range(n):
        _, vi = sf.kepler.propagar(GM_SOL, r, v_, (i + 0.5) * tof / n)
        u[i] = sentido * fracao * vi / np.linalg.norm(vi)
    return u


def _partida_fria(perna, base, objetivo, oc, origem, sentido, duracoes, lim_et, ineq_extra=None):
    """Partida a frio: com a data de `base` fixa, tenta as durações da lista (P-122) até achar um ponto viável
    (sf.viabilizar) e otimizá-lo com as datas fixas; esse ponto é o chute da otimização com as datas livres."""
    ultimo, menor = None, None
    for d in duracoes:
        tof = d * DIA
        if lim_et is not None and base["t0"] + tof > lim_et:
            continue
        fixa = dataclasses.replace(perna, t0=(base["t0"], base["t0"]), tof=(tof, tof))
        ch = {**base, "tof": tof, "u": _chute_u(origem, base["t0"], tof, perna.n_segmentos, sentido, 0.5)}
        ch, res = sf.viabilizar(fixa, ch)
        ultimo = (d, res)
        menor = res if menor is None else min(menor, res)
        if res > oc["residuo_max"]:
            continue
        s = _resolve(fixa, objetivo, ch, oc, ineq_extra=ineq_extra, exigir=False)
        menor = min(menor, max(s["residuo_max"], s["violacao_u"]))
        if s["convergiu"]:
            return s
    raise NaoConverge(f"partida a frio sem ponto viável nas durações {duracoes} (última: {ultimo})", menor)


def _oc():
    o = ler("config/orbitador_so_eletrico.yaml")["otimizador"]
    return {k: v(o[k]) for k in ("n_segmentos", "ordem", "maxiter", "ftol", "residuo_max")}


def _lc():
    """Limites das massas, chutes a frio, limiar de arco e restrição de declinação do otimizador (P-118)."""
    o = ler("config/orbitador_so_eletrico.yaml")["limites_e_chutes"]
    return {k: (o[k]["valor"]) for k in o}


def _resolve(perna, objetivo, chute, oc, ineq_extra=None, exigir=True, rodadas=4):
    """SLSQP com reinícios a partir do último ponto (até `rodadas`) enquanto ele para sem convergir. Convergiu quando a
    continuidade e |u| ≤ 1 ficam dentro do resíduo aceito (P-118) e o SLSQP declara sucesso ou o objetivo para de mudar
    entre dois reinícios (mudança relativa ≤ ftol × 10³, P-118)."""
    anterior, menor = None, None
    for k in range(rodadas):
        s = sf.otimizar(perna, objetivo, chute, maxiter=int(oc["maxiter"]), ftol=oc["ftol"], ineq_extra=ineq_extra)
        viavel = s["residuo_max"] <= oc["residuo_max"] and s["violacao_u"] <= oc["residuo_max"]
        menor = max(s["residuo_max"], s["violacao_u"]) if menor is None else min(menor, max(s["residuo_max"], s["violacao_u"]))
        parado = anterior is not None and abs(s["objetivo"] - anterior) <= oc["ftol"] * 1e3 * max(1.0, abs(anterior))
        s["convergiu"], s["viavel"], s["rodadas"] = bool(viavel and (s["sucesso"] or parado)), bool(viavel), k + 1
        s["criterio"] = "sucesso do SLSQP" if s["sucesso"] else ("objetivo estacionário entre reinícios" if parado else "não convergiu")
        if s["convergiu"]:
            break
        anterior = s["objetivo"] if viavel else None
        chute = s
    if exigir and not s["convergiu"]:
        raise NaoConverge(f"otimizador não convergiu: {s['mensagem']}; resíduo {s['residuo_max']:.2e}", menor)
    return s


def _resumo(s, motor, mu=GM_SOL):
    """Grandezas de uma solução: Δv e arcos de empuxo (segmentos com |u| acima do limiar, P-118)."""
    lc_ = _lc()
    u = s["u"]
    a = np.linalg.norm(u, axis=1)
    dt_ = s["tof"] / len(u)
    arcos, m, dv_arco, em_arco = [], s["m0"], 0.0, False
    for ai in a:
        m2 = m - ai * motor.vazao_kg_s * dt_
        d = motor.c_km_s * math.log(m / m2)
        if ai > lc_["limiar_arco"]:
            dv_arco, em_arco = dv_arco + d, True
        elif em_arco:
            arcos.append(dv_arco)
            dv_arco, em_arco = 0.0, False
        m = m2
    if em_arco:
        arcos.append(dv_arco)
    return {"dv_km_s": motor.c_km_s * math.log(s["m0"] / s["mf"]), "arcos_dv_km_s": arcos,
            "fracao_tempo_com_empuxo": float(np.mean(a > lc_["limiar_arco"])), "aceleracao_inicial_m_s2": motor.empuxo_n / s["m0"]}


def _nao_finitos(valores):
    """Nomes das grandezas com algum valor NaN ou inf. Nenhuma conferência pode aprovar por comparação com NaN (em Python,
    NaN <= limite e NaN > limite dão os dois False): a verificação recusa explicitamente (decisão do Fabio, 2026-11-25)."""
    return sorted(k for k, x in valores.items() if not all(math.isfinite(y) for y in np.ravel(np.asarray(x, dtype=float))))


def _avaliada(perna, s, ineq_extra=None):
    """Uma solução gravada, sem otimizar, com o resultado de sf.avaliar (no lugar do que _resolve devolve)."""
    a = sf.avaliar(perna, s, ineq_extra)
    return {**{k: s[k] for k in SEMENTE}, **a, "mensagem": "verificada sem otimizar", "iteracoes": 0}


def _confere_continuo(perna, s):
    """Diferença entre o estado final da propagação contínua do mesmo perfil e o alvo (km, km/s)."""
    rp, vp = perna.estado_partida(s["t0"])
    rc, vc = perna.estado_chegada(s["t0"] + s["tof"])
    r, v_, _ = sf.propagar_continuo(perna.mu, rp, vp + s["vinf0"], s["m0"], s["tof"], s["u"], perna.motor)
    return float(np.linalg.norm(r - rc)), float(np.linalg.norm(v_ - (vc + s["vinf1"])))


# ---------------------------------------------------------------- (b) caso publicado

def _polo_marte(et):
    """Eixo de rotação de Marte (IAU_MARS, pck00011) no referencial dos estados (ECLIPJ2000), na época."""
    import spiceypy as spice
    eph.carregar_kernels()
    return np.asarray(spice.pxform("IAU_MARS", pc.FRAME, et))[:, 2]


def caso_publicado(arg):
    """Varredura de empuxo de um exemplo de [F121], com datas e |v∞| publicados e massa inicial de [F22]. Com
    `declinacoes`, também as declinações publicadas (partida no equador da Terra J2000; chegada no equador de Marte), P-119."""
    nome, declinacoes = arg
    cfg = ler("config/orbitador_so_eletrico.yaml")["caso_publicado"]
    lc_ = _lc()
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
        polo, rot = _polo_marte(t1), _ecl_para_eq()
        d1 = math.radians(v(c["declinacao_chegada_graus"])) if "declinacao_chegada_graus" in c else None

        def extra(t0_, tof, m0_, mf, a, b):
            g = [float((rot @ a)[2]) / max(np.linalg.norm(a), 1e-9) - math.sin(d0)]
            if d1 is not None:
                g.append(float(b @ polo) / max(np.linalg.norm(b), 1e-9) - math.sin(d1))
            g = np.array(g) * lc_["escala_restricao_declinacao"]
            fo = lc_["folga_restricao_declinacao"]
            return np.r_[g + fo, fo - g]   # igualdade como duas desigualdades com folga (P-118)
    chute = {"t0": t0, "tof": t1 - t0, "m0": m0, "mf": lc_["mf_chute_fracao"] * m0, "vinf0": vi0 * vT / np.linalg.norm(vT),
             "vinf1": np.zeros(3), "u": _chute_u(terra, t0, t1 - t0, n, +1)}
    linhas = []
    for empuxo in cfg["empuxos_n"]["valor"]:
        motor = sf.Motor(empuxo, isp)
        p = sf.Perna(GM_SOL, terra, marte, motor, n, (t0, t0), (t1 - t0, t1 - t0), (vi0, vi0), (vi1, vi1), (m0, m0),
                     (lc_["mf_min_fracao"] * m0, m0))
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
    base = e["se"]["propulsores"][nome].get("base", nome)   # variante de vida de um propulsor do catálogo
    if base not in ecfg["propulsores"]:
        ecfg = {**ecfg, "propulsores": {**ecfg["propulsores"], base: e["se"]["propulsores"][base]}}
    return oe.sistema(base, n, ecfg, e["pcfg"])


def _capacidade(e):
    """(capacidade oficial, capacidade do objetivo, limite de DLA sem penalidade em graus, maior C3 publicado).

    A oficial é a de orbital.lancamento (interpolação linear da curva do ELVPerf [F79], multiplicador de DLA da P-036, menos
    o adaptador da P-097) e dá a margem reportada. A do objetivo depende da formulação (P-118): a curva de C3 por PCHIP
    (monótona, nos mesmos pontos) e
      - "suave": o multiplicador de DLA também por PCHIP, com derivada zero no limite da faixa sem penalidade (um ponto
        auxiliar com fator 1 abaixo dele), igual a 1 dentro da faixa; a P-036 não muda;
      - "restricao": sem multiplicador (a DLA fica na faixa sem penalidade por uma restrição explícita do SLSQP).
    O SLSQP não converge nas quinas das interpolações lineares (o ótimo cai no limite de 28,5°)."""
    from scipy.interpolate import PchipInterpolator
    lan = e["lcfg"]["lancadores"][e["se"]["missao"]["lancador"]]
    cfg = e["lcfg"]
    pfm = cfg["centro"]["plataformas"].get(lan.get("plataforma"), {})
    imax = lc.inclinacao(pfm.get("latitude_graus", v(cfg["centro"]["latitude_graus"])), cfg["centro"]["azimute_graus"]["valor"][0])
    adapt = lc.adaptador_p097()[0]
    suave_c3 = PchipInterpolator(lan["c3"]["pontos"], lan["c3"]["massa_kg"])
    lim_dla = v(cfg["dla"]["faixa_sem_penalidade_graus"])
    mult = cfg["dla"]["multiplicador_nordeste"]
    passo = mult["dla_graus"][1] - mult["dla_graus"][0]
    suave_dla = PchipInterpolator([mult["dla_graus"][0] - passo] + list(mult["dla_graus"]), [1.0] + list(mult["fator"]))
    formulacao = e["se"]["otimizador"]["formulacao_dla"]["valor"]

    def cap(vinf):
        c3 = float(vinf @ vinf)
        k = lc.capacidade_direta(lan, c3, _declinacao(vinf) if c3 > 0 else 0.0, cfg, imax)[0]
        return k - adapt if k == k else float("nan")

    def cap_objetivo(vinf):
        c3 = float(vinf @ vinf)
        if c3 > max(lan["c3"]["pontos"]) * (1 + 1e-12):
            return float("nan")
        c3 = min(c3, max(lan["c3"]["pontos"]))
        k = float(suave_c3(c3))
        if formulacao == "restricao":
            return k - adapt
        d = abs(_declinacao(vinf)) if c3 > 0 else 0.0
        if d > (imax if imax is not None else 90.0) or d > mult["dla_graus"][-1] + 1e-9:
            return float("nan")
        return k * (1.0 if d <= lim_dla else float(suave_dla(d))) - adapt
    return cap, cap_objetivo, lim_dla, max(lan["c3"]["pontos"])


def fecho(nome, n, h, e=None, chutes=None, com_prazo=True, verificar=False):
    """Fecho de massa e linha do tempo do orbitador só elétrico com n propulsores ativos e encontro a h km. Com
    `com_prazo`, a ida tem a restrição de ficar pronta no encontro até o último lançamento do MAV; sem ela, a data sai
    livre e o "pronto antes" é conferido depois.

    Com `verificar` (decisão do Fabio, 2026-11-24: verificar, não reotimizar), `chutes` é uma solução gravada e nada é
    otimizado: os dois trechos são propagados como gravados (sf.avaliar) e o fecho de massa é feito uma vez, com as razões
    de massas deles; a verificação (resíduo, desigualdades e limites dentro do resíduo aceito da P-118; descasamento do
    fecho de massa dentro da P-125) vai em "verificacao"."""
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
    cap, cap_obj, lim_dla, c3_max = _capacidade(e)
    formulacao = e["se"]["otimizador"]["formulacao_dla"]["valor"]
    rot = _ecl_para_eq()
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
    if chutes and chutes.get("empuxo_n") and not verificar:
        # mesma trajetória com outro empuxo máximo: u escala pela razão dos empuxos (a vazão escala junto, Isp igual)
        k = chutes["empuxo_n"] / motor.empuxo_n
        if chutes.get("isp_s") == motor.isp_s:
            def esc(u):
                u = u * k
                a = np.linalg.norm(u, axis=1)
                return u / np.maximum(1.0, a)[:, None]   # com empuxo menor, |u| acima de 1 fica em 1
            ida0, volta0 = {**ida0, "u": esc(ida0["u"])}, {**volta0, "u": esc(volta0["u"])}
    lc_ = _lc()
    if verificar:
        if chutes is None or chutes["empuxo_n"] != motor.empuxo_n or chutes["isp_s"] != motor.isp_s:
            raise ValueError("solução gravada com outro empuxo ou Isp que o do config")
        nf = _nao_finitos({f"{k}.{c}": chutes[k][c] for k in ("ida", "volta") for c in SEMENTE})
        if nf:
            raise ValueError(f"solução gravada com valor não finito: {', '.join(nf)}")
        com_prazo = False   # o prazo entra só na conclusão
    # massa na chegada: a do chute (n anterior da cadeia) ou a do chute a frio (P-118)
    m_chegada = float(ida0["mf"]) if ida0 is not None else float(lc_["massa_chegada_chute_kg"])
    hist = []
    for it in range(1 if verificar else int(v(ms["iteracoes_fecho"]))):
        # ---- ida: m0 livre, mf = massa na chegada; objetivo: maior margem no lançador
        t_d_est = espiral(e["hill"], r_e, m_chegada)[0]
        lim_et = _et(lim_ultimo.isoformat()) - t_d_est
        pi = sf.Perna(GM_SOL, terra, marte, motor, nseg, (t0min, t0max),
                      (ms["ida_dias"]["valor"]["min"] * DIA, ms["ida_dias"]["valor"]["max"] * DIA),
                      (0.0, math.sqrt(c3_max)), (0.0, v(ms["vinf_chegada_marte_km_s"])), (lc_["m0_ida_fracao"][0] * m_chegada, lc_["m0_ida_fracao"][1] * m_chegada),
                      (m_chegada, m_chegada))

        def obj_ida(t0, tof, m0, mf, a, b):
            # 1 / (1 + margem), com a massa injetada do fecho: mf · (m0/mf)^f (margem de Δv, P-014)
            k = cap_obj(a)
            return mf * (m0 / mf) ** f / k if k > 0 else 1e3

        def extra(t0, tof, m0, mf, a, b):
            g = [(lim_et - (t0 + tof)) / DIA] if com_prazo else []
            if formulacao == "restricao":
                sd = float((rot @ a)[2]) / max(float(np.linalg.norm(a)), 1e-9)   # seno da DLA
                g += [math.sin(math.radians(lim_dla)) - sd, sd + math.sin(math.radians(lim_dla))]
            return np.array(g if g else [1.0])
        if ida0 is None and not verificar:
            t0 = min(max(_et(ms["partida_frio"]["valor"]), t0min), t0max)
            _, vT = terra(t0)
            base = {"t0": t0, "m0": lc_["m0_chute_fracao"] * m_chegada, "mf": m_chegada,
                    "vinf0": lc_["vinf_partida_chute_km_s"] * vT / np.linalg.norm(vT), "vinf1": np.zeros(3)}
            ida0 = _partida_fria(pi, base, obj_ida, oc, terra, +1, ms["duracoes_frio_ida_dias"]["valor"],
                                 lim_et if com_prazo else None, extra)
        si = _avaliada(pi, ida0, extra) if verificar else _resolve(pi, obj_ida, {**ida0, "mf": m_chegada}, oc, ineq_extra=extra)
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
        razao_volta = (volta0["m0"] / volta0["mf"]) ** f if volta0 else lc_["razao_volta_chute"]
        pr = px = 0.0
        tol_m = v(e["ecfg"]["varredura"]["convergencia_massas_kg"])   # P-049, como em tools/rotas_mav.py
        for _ in range(int(lc_["max_iteracoes_massas"])):
            # instalados: os ativos ou os que bastam para a vida (o que for maior), mais as reservas (P-121)
            xe_inst = max(n, math.ceil(px / vida)) + reservas
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
            if abs(nr - pr) < tol_m and abs(nx - px) < tol_m:
                break
            pr, px = nr, nx
        else:
            raise RuntimeError("massas não convergiram")
        inst = xe_inst
        if px / (inst - reservas) > vida * (1 + 1e-12):
            raise RuntimeError("ponto fixo das massas terminou com xenônio por propulsor acima da vida")
        _, t_s_real, _, _ = hb.tempos_espiral(mu, R, r_e, e["hill"], b_sub, se0, fator_dv=f)
        t_s = t_s_real / duty
        partida_cedo = lanc0 + dt.timedelta(days=math.ceil(e["t_enc"] / DIA + t_s / DIA))
        # ---- volta: m0 = massa no início do trecho heliocêntrico; objetivo: maior massa final
        t2 = _et(partida_cedo.isoformat())
        pv = sf.Perna(GM_SOL, marte, terra, motor, nseg, (t2, t2 + v(ms["espera_retorno_dias"]) * DIA),
                      (ms["volta_dias"]["valor"]["min"] * DIA, ms["volta_dias"]["valor"]["max"] * DIA),
                      (0.0, 0.0), (0.0, v(ms["vinf_chegada_terra_max_km_s"])), (b_volta, b_volta), (lc_["mf_min_fracao"] * b_volta, b_volta))
        obj_volta = lambda t0, tof, m0, mf, a, b: -mf / 1000.0  # noqa: E731
        if volta0 is None:
            base = {"t0": t2, "m0": b_volta, "mf": lc_["mf_chute_fracao"] * b_volta, "vinf0": np.zeros(3), "vinf1": np.zeros(3)}
            volta0 = _partida_fria(pv, base, obj_volta, oc, marte, -1, ms["duracoes_frio_volta_dias"]["valor"], None)
        sv = _avaliada(pv, volta0) if verificar else _resolve(pv, obj_volta, {**volta0, "m0": b_volta, "t0": max(volta0["t0"], t2)}, oc)
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
    ver = None
    if verificar:
        # as massas fixas dos trechos (mf da ida e m0 da volta) vêm do fecho, que usa as razões de massas (método da Etapa 2):
        # a diferença para as massas gravadas é o descasamento do fecho, conferido em termos relativos (P-125)
        lim_i = {k: x for k, x in si["violacao_limites"].items() if k != "mf"}
        lim_v = {k: x for k, x in sv["violacao_limites"].items() if k != "m0"}
        pior = max(si["residuo_max"], sv["residuo_max"], si["violacao_u"], sv["violacao_u"], *lim_i.values(), *lim_v.values())
        tol_f = v(ler("config/orbitador_so_eletrico.yaml")["verificacao"]["descasamento_fecho_relativo_max"])
        desc = max(abs(b_volta - sv["m0"]) / sv["m0"], abs(b_desc - si["mf"]) / si["mf"])
        # tudo o que as conferências e as conclusões usam tem de ser finito (as datas saem dos tempos e das durações)
        nf = _nao_finitos({**{f"{k}.{c}": x[c] for k, x in (("ida", si), ("volta", sv)) for c in SEMENTE},
                           **{f"{k}.residuo": x["residuo_max"] for k, x in (("ida", si), ("volta", sv))},
                           **{f"{k}.violacao_u": x["violacao_u"] for k, x in (("ida", si), ("volta", sv))},
                           **{f"{k}.limite_{c}": y for k, x in (("ida", si), ("volta", sv)) for c, y in x["violacao_limites"].items()},
                           "residuo_aceito": oc["residuo_max"], "descasamento_max": tol_f, "descasamento": desc,
                           "margem_falcon_heavy": margem, "c3": float(si["vinf0"] @ si["vinf0"]), "dla": _declinacao(si["vinf0"]),
                           "vinf_chegada_terra": float(np.linalg.norm(sv["vinf1"])), "orbitador_kg": m0_lanc,
                           "massa_chegada_marte_kg": b_desc, "massa_volta_kg": b_volta, "xenonio_kg": px,
                           "xenonio_por_propulsor_kg": px / (inst - reservas), "vida_kg": vida,
                           "descida_s": t_d, "subida_s": t_s, "encontro_s": e["t_enc"]})
        ok = not nf and pior <= oc["residuo_max"] and desc <= tol_f
        ver = {"verificada": bool(ok), "nao_finitos": nf, "pior": pior, "descasamento_relativo": desc,
               "residuo_ida": si["residuo_max"], "residuo_volta": sv["residuo_max"],
               "violacao_ida": si["violacao_u"], "violacao_volta": sv["violacao_u"],
               "limites_ida": lim_i, "limites_volta": lim_v,
               "descasamento_m0_volta_kg": b_volta - sv["m0"], "descasamento_chegada_marte_kg": b_desc - si["mf"]}
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
            "descida_cruza_conjuncao": any(pronto - dt.timedelta(days=math.ceil(t_d / DIA)) <= cj["fim"] and cj["inicio"] <= pronto for cj in conj),
            "subida_cruza_conjuncao": any(lanc0 <= cj["fim"] and cj["inicio"] <= partida_marte for cj in conj),
            "com_prazo": com_prazo, "formulacao_dla": formulacao,
            "fecha": bool(margem >= 0 and pronto <= lim_ultimo and px / (inst - reservas) <= vida),
            "historico": hist, "erro_continuo_ida_km_e_km_s": erro_ida, "erro_continuo_volta_km_e_km_s": erro_volta,
            "otimizador": {"ida": (si["mensagem"], si["iteracoes"], si["residuo_max"]), "volta": (sv["mensagem"], sv["iteracoes"], sv["residuo_max"])},
            "_chutes": {"ida": si, "volta": sv, "empuxo_n": motor.empuxo_n, "isp_s": motor.isp_s},
            **({"verificacao": ver} if verificar else {})}


SEMENTE = ("t0", "tof", "m0", "mf", "vinf0", "vinf1", "u")   # o que a partida a quente usa de uma solução


def _semente(ch):
    """Só as grandezas da partida a quente, como listas: a cadeia continua igual a partir de um bloco gravado (o YAML
    guarda os floats com repr, sem perda)."""
    return {"empuxo_n": float(ch["empuxo_n"]), "isp_s": float(ch["isp_s"]),
            **{k: {c: (np.asarray(ch[k][c]).tolist() if c in ("vinf0", "vinf1", "u") else float(ch[k][c])) for c in SEMENTE}
               for k in ("ida", "volta")}}


def _de_semente(sm):
    return {"empuxo_n": sm["empuxo_n"], "isp_s": sm["isp_s"],
            **{k: {c: (np.asarray(sm[k][c], dtype=float) if c in ("vinf0", "vinf1", "u") else float(sm[k][c])) for c in SEMENTE}
               for k in ("ida", "volta")}}


def _cadeia(nome, h, ns, anteriores=None):
    """Um bloco da cadeia de n decrescente de um propulsor numa órbita (o maior n tem mais empuxo e parte a frio com mais
    facilidade). Cada fecho parte da solução convergida mais recente (partida a quente), começando pelas sementes dos
    blocos anteriores (`anteriores`: n → semente), ou a frio no primeiro bloco. Se não converge com a restrição de prazo,
    refaz sem ela (o "pronto antes" sai falso, com a data). Depois, os que não convergiram são refeitos a partir do vizinho
    convergido mais próximo, entre os deste bloco e os dos anteriores (empate: o de n maior). Sem convergir, a configuração
    é classificada pelo menor resíduo alcançado (P-118): acima do aceito, "nenhuma solução viável encontrada" (sem afirmar
    inviabilidade); abaixo, "sem convergência do otimizador". Devolve (configurações, sementes deste bloco)."""
    ns = sorted(ns, reverse=True)
    oc = _oc()
    sol = {int(k): _de_semente(x) for k, x in (anteriores or {}).items()}
    proprias = {}
    out = []

    def tenta(n, ch):
        t = time.perf_counter()
        res = []
        try:
            r = fecho(nome, n, h, chutes=ch)
        except (NaoConverge, RuntimeError, ValueError) as x1:
            res.append(getattr(x1, "residuo", None))
            try:
                r = fecho(nome, n, h, chutes=ch, com_prazo=False)
                r["nota"] = f"sem a restrição de prazo (com ela: {type(x1).__name__})"
            except (NaoConverge, RuntimeError, ValueError) as x2:
                res.append(getattr(x2, "residuo", None))
                rs = [x for x in res if x is not None]
                return {"propulsor": nome, "n_ativos": n, "altitude_km": h, "falha": f"{type(x2).__name__}: {x2}",
                        "residuo_minimo": min(rs) if rs else None, "segundos": time.perf_counter() - t}
        sem = _semente(r.pop("_chutes"))
        sol[n] = _de_semente(sem)
        proprias[n] = sem
        r["segundos"] = time.perf_counter() - t
        return r

    ultimo = min(sol) if sol else None   # o menor n dos blocos anteriores: o vizinho de cima deste bloco
    for n in ns:
        r = tenta(n, sol[ultimo] if ultimo is not None else None)
        if "falha" not in r:
            ultimo = n
        out.append(r)
    for i, n in enumerate(ns):
        if "falha" not in out[i]:
            continue
        viz = min(sorted(sol, reverse=True), key=lambda m: abs(m - n), default=None)
        if viz is None:
            continue
        r = tenta(n, sol[viz])
        if "falha" in r:
            a = out[i]
            a["falha"] += f"; segunda passada, a partir de n = {viz}: {r['falha']}"
            rs = [x for x in (a["residuo_minimo"], r["residuo_minimo"]) if x is not None]
            a["residuo_minimo"] = min(rs) if rs else None
            a["segundos"] += r["segundos"]
        else:
            r["nota"] = (r.get("nota", "") + f"; segunda passada, a partir de n = {viz}").lstrip("; ")
            out[i] = r
    for r in out:
        if "falha" in r:
            if r["residuo_minimo"] is None:   # falha fora do otimizador (fecho de massa, vida, erro): sem resíduo
                r["situacao"] = "falha fora do otimizador"
            elif r["residuo_minimo"] <= oc["residuo_max"]:
                r["situacao"] = "sem convergência do otimizador"
            else:
                r["situacao"] = "nenhuma solução viável encontrada"
    return sorted(out, key=lambda r: r["n_ativos"]), proprias


def _conclusoes(r, cfg):
    """(converge, margem, prazo, vida) em três estados, com as bandas de P-123."""
    if "falha" in r:
        return [f"não ({r['situacao']})", "—", "—", "—"]
    c = cfg["conclusoes"]
    m, lim, bm = r["margem_falcon_heavy"], v(c["margem_minima"]), v(c["banda_margem"])
    if not all(math.isfinite(x) for x in (m, lim, bm)):
        raise ValueError(f"margem ou banda não finita: {m}, {lim}, {bm}")
    margem = "sim" if m >= lim + bm else "não" if m < lim - bm else "indeterminado"
    folga = (D(r["ultimo_lancamento_mav"]) - D(r["pronto_no_encontro"])).days
    bp = v(c["banda_prazo_dias"])
    prazo = "sim" if folga >= bp else "não" if folga < -bp else "indeterminado"
    return ["sim", margem, prazo, "sim" if r["dentro_da_vida"] else "não"]


def _fecha_propulsor(rs, cfg):
    """Existência (decisão do Fabio, 2026-11-24): (existe trajetória verificada que fecha?, ativos) de um propulsor numa
    órbita. "sim" se alguma solução verificada dá "sim" nas quatro conclusões; senão "indeterminado" se alguma verificada
    fica sem "não" (na banda); senão "não demonstrado" (o otimizador é local: não prova inexistência)."""
    cs = [(r["n_ativos"], _conclusoes(r, cfg)) for r in rs if "falha" not in r]
    sim = sorted(n for n, c in cs if c == ["sim"] * 4)
    if sim:
        return ["sim", ", ".join(str(n) for n in sim)]
    ind = sorted(n for n, c in cs if "não" not in c)
    if ind:
        return ["indeterminado", ", ".join(str(n) for n in ind)]
    return ["não demonstrado", "—"]


def _pelo_menos(m):
    """Margem como limite inferior (o otimizador é local), em pontos percentuais inteiros arredondados para baixo: a
    verificação reproduz a margem a ~1e-12 entre CPUs, e só um valor a essa distância de um inteiro mudaria (P-123)."""
    return f"{math.floor(m * 100):d}".replace("-", "−") + " %"


def _sci(x):
    return f"{x:.1e}".replace(".", ",").replace("-", "−")


def escreve(casos, fam):
    cfg = ler("config/orbitador_so_eletrico.yaml")
    cp, ms, pr = cfg["caso_publicado"], cfg["missao"], cfg["propulsores"]
    oc = _oc()
    md = ["# Orbitador só elétrico da família 1: trajetória de baixo empuxo e fecho de massa (gerado por tools/orbitador_so_eletrico.py)", "",
          "Etapa 2 do plano (issue #68). Plano aprovado pelo Fabio em 2026-11-20. **Calculado, NÃO validado.**", "",
          "**Verificar, não reotimizar** (decisão do Fabio, 2026-11-24): as trajetórias são otimizadas fora do CI (mínimos "
          "locais, que mudam entre CPUs) e gravadas em `data/orbitador_so_eletrico/`; a regeneração só as verifica. Este "
          "arquivo traz o método, as entradas, a existência de trajetória verificada que fecha e as margens como limites "
          "inferiores; os demais números estão em `results/familia1/diagnostico_orbitador_so_eletrico.md`, fora da "
          "comparação do CI (CLAUDE.md, regra 6).", "",
          "## Método", "",
          "- **(a) Trechos heliocêntricos:** transcrição de Sims–Flanagan de ordem 4 (`orbital.sims_flanagan`) com as efemérides "
          f"DE440s, {int(oc['n_segmentos'])} segmentos por trecho, otimizada com SLSQP (P-118). Conferências em "
          "`tests/test_sims_flanagan.py`: empuxo zero contra Kepler e Lambert, aceleração tangencial constante contra [F113] p. 31.",
          "- **Ida:** partida da Terra com o v∞ do lançador (variável), chegada ao raio de Hill de Marte com v∞ = 0; objetivo: a "
          f"maior margem no {ms['lancador']} pela curva C3 × massa e pela declinação ([F79]). Restrições: DLA ≤ "
          f"{br(v(ler('config/lancadores.yaml')['dla']['faixa_sem_penalidade_graus']), 1)}° (formulação \""
          f"{ler('config/orbitador_so_eletrico.yaml')['otimizador']['formulacao_dla']['valor']}\", P-118) e o orbitador pronto no encontro até o último lançamento "
          "do MAV da família 1 (`results/familia1/missao.yaml`); se a tentativa com o prazo falha, tenta-se sem ele, e o "
          "prazo entra só na conclusão.",
          "- **Marte:** espirais de descida e de subida como na rota B (`orbital.hibrido`, verificadas na Etapa 3.2), com o motor "
          "desligado no eclipse; MAV lançado pela regra da família 1 (conjunções, recuperação, "
          f"folga de {ler('results/familia1/missao.yaml')['folga_conjuncao_dias']} d).",
          "- **Volta:** partida do raio de Hill com v∞ = 0 a partir da partida mais cedo; objetivo: a maior massa final.",
          "- **Fecho de massa:** o da rota B (`tools/rotas_mav.py`), com a razão de massas de cada trecho heliocêntrico "
          f"otimizado no lugar do Δv quase circular; a margem de Δv (P-014) multiplica o logaritmo da razão. "
          f"{int(v(ms['iteracoes_fecho']))} iterações entre a ida e o fecho (P-122).",
          "- **Otimização (fora do CI):** uma cadeia de n decrescente por propulsor e órbita, em blocos (P-122), no notebook e "
          "no CI do PR #74 (as partes que terminaram); as soluções e as falhas de cada origem estão em "
          "`data/orbitador_so_eletrico/`.",
          "- **Verificação (no CI):** cada solução gravada é propagada com a mesma transcrição (`sf.avaliar`), sem otimizar: "
          "resíduo de continuidade, |u| ≤ 1, v∞ dentro dos limites (na chegada à Terra, ≤ "
          f"{br(v(ms['vinf_chegada_terra_max_km_s']))} km/s), DLA ≤ "
          f"{br(v(ler('config/lancadores.yaml')['dla']['faixa_sem_penalidade_graus']), 1)}° e os limites das datas e das "
          f"durações, tudo dentro do resíduo aceito ({_sci(v(cfg['otimizador']['residuo_max']))}, P-118); depois, o fecho "
          "de massa e a linha do tempo com as razões de massas das trajetórias gravadas, com a massa que o fecho pede a até "
          f"{br(v(cfg['verificacao']['descasamento_fecho_relativo_max']) * 100, 1)} % da gravada nos trechos (P-125). Por "
          "configuração fica a melhor solução verificada (a que fecha; depois, a de maior margem), com a origem.",
          f"- **Ciclo de trabalho:** {br(v(cfg['operacao']['ciclo_trabalho']) * 100)} % (P-120, valor do Dawn [F279] p. 611).",
          "- **(c) Vida e rodízio:** propulsores além dos ativos até o xenônio por propulsor ficar abaixo da vida demonstrada, "
          "cada um com a sua PPU (P-121).", "",
          "## Propulsores", "",
          "| Propulsor | No catálogo (ADR 0013) | Vida usada (kg de Xe por propulsor) | Fonte da vida | Voo |", "| :- | :- | -: | :- | :- |",
          f"| XIPS-25 | sim | {br(v(pr['XIPS-25']['vida_kg']))} | {pr['XIPS-25']['vida_kg']['fonte']} | [F119] p. 1 |",
          f"| XIPS-25 (87 kg) | sim (o mesmo propulsor) | {br(v(pr['XIPS-25 (87 kg)']['vida_kg']))} | {pr['XIPS-25 (87 kg)']['vida_kg']['fonte']} | [F119] p. 1 |",
          f"| NEXT-C | não (avaliação em paralelo, decisão do Fabio em 2026-11-20) | {br(v(pr['NEXT-C']['vida_kg']))} | {pr['NEXT-C']['vida_kg']['fonte']} | {pr['NEXT-C']['voo']} |", "",
          "- **XIPS-25, vida a ~4,5 kW:** o teste de vida [F274] processou 4 + 40 kg em alta potência e 114 kg a 2 kW (Tab. 3, "
          "p. 4). A plena potência, [F275] p. 10 avalia por modelo (não por teste) o limite em 134 kg e recomenda 87 kg com a "
          "margem de 50 %; e diz (p. 1) que vazões maiores são possíveis em trajetórias com muito tempo em baixa potência. Por "
          "isso a base de 158 kg (P-121) é carregada ao lado da variante de 87 kg; a aplicação de cada uma a 4,5 kW é premissa "
          "NÃO VALIDADA (P-121).",
          "- **NEXT-C, herança de voo limitada:** no DART, o sistema foi ativado em 18/12/2021 e operou cerca de 2 h, com 21 "
          "reciclagens; um aumento de corrente na eletrônica de potência da nave, atribuído à interferência de um arco, mostrou "
          "teste elétrico insuficiente entre propulsor e nave antes do lançamento e levou à suspensão das operações do NEXT-C "
          "([F278] p. 2). A vida usada é a do NEXT de engenharia em solo ([F277] p. 2).", "",
          "## Conclusões", "",
          "Três estados (P-123): \"sim\" e \"não\" só fora da banda; dentro dela, \"indeterminado\". Xe por propulsor ≤ "
          "vida: por construção do rodízio (P-121). **O otimizador é local:** as margens são limites inferiores (a melhor "
          "solução verificada achada), e uma configuração sem solução verificada (\"nenhuma solução verificada\") não "
          "demonstra inviabilidade; as situações do otimizador em cada origem (\"nenhuma solução viável encontrada\", "
          "\"sem convergência do otimizador\", P-118) estão no diagnóstico.", ""]
    principal = float(min(ms["altitudes_km"]["valor"]))
    md += [f"### Conclusão principal: o orbitador só elétrico fecha a {br(principal)} km?", "",
           f"Na família 1, o MAV sólido só fecha com encontro a {br(principal)} km (decisão do Fabio, 2026-11-22). Existe "
           "trajetória verificada que fecha: \"sim\" se alguma solução verificada dá \"sim\" nas quatro conclusões; senão, "
           "\"indeterminado\" se alguma fica na banda sem nenhum \"não\"; senão, \"não demonstrado\". Ativos: os das "
           "soluções nesse estado.", "",
           "| Propulsor | Existe trajetória verificada que fecha? | Ativos |", "| :- | :- | :- |"]
    for nome in ms["n_ativos"]["valor"]:
        md.append(f"| {nome} | " + " | ".join(_fecha_propulsor([r for r in fam if r["propulsor"] == nome and r["altitude_km"] == principal], cfg)) + " |")
    cab = [f"| Propulsor | Ativos | Encontro (km) | Trajetória verificada | Origem | Margem no Falcon Heavy, pelo menos | "
           f"Margem ≥ {br(v(cfg['conclusoes']['margem_minima']) * 100)} % (banda ± {br(v(cfg['conclusoes']['banda_margem']) * 100)} pontos) | "
           f"Pronto até o último lançamento do MAV (banda ± {int(v(cfg['conclusoes']['banda_prazo_dias']))} d) | Xe por propulsor ≤ vida |",
           "| :- | -: | -: | :- | :- | -: | :- | :- | :- |"]
    for titulo, sel in ((f"### Por configuração, encontro a {br(principal)} km", lambda r: r["altitude_km"] == principal),
                        ("### Sensibilidade: as outras órbitas de encontro", lambda r: r["altitude_km"] != principal)):
        md += ["", titulo, ""] + cab
        for r in fam:
            if sel(r):
                c = _conclusoes(r, cfg)
                ori, mar = ("—", "—") if "falha" in r else (r["origem"], _pelo_menos(r["margem_falcon_heavy"]))
                md.append(f"| {r['propulsor']} | {r['n_ativos']} | {br(r['altitude_km'])} | {c[0]} | {ori} | {mar} | " + " | ".join(c[1:]) + " |")
    md += ["", "## (b) Caso publicado", "",
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
         "Fora da comparação do CI (regra 6): soluções de otimização (mínimos locais), verificadas sem reotimizar. Calculado, "
         "NÃO validado.", "",
         "## (b) Caso publicado: Joffre 2018 [F121] com massa e empuxo de Yau 2021 [F22]", ""]
    for c in casos:
        var = "com as declinações publicadas impostas" if c["declinacoes"] else "só com os módulos de v infinito publicados"
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
    d += ["## (a) e (c) Família 1: a melhor solução verificada de cada configuração", "",
          "| Propulsor | Ativos | Encontro (km) | Instalados | Potência (kW) | Xe (kg) | Xe por propulsor (kg) | Vida (kg) | Propulsores + PPU (kg) | Orbitador (kg) | Margem no Falcon Heavy | C3 (km²/s²) | DLA (°) | Partida da Terra | Ida (d) | Chegada a Marte | Descida (d) | Pronto no encontro | Último lançamento do MAV | Lançamento do MAV | Subida (d) | Partida de Marte | Volta (d) | Chegada à Terra | Descida cruza conjunção | Encontro e subida cruzam conjunção | Fecha? |",
          "| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: | :- | -: | :- | -: | :- | :- | :- | -: | :- | -: | :- | :- | :- | :- |"]
    for r in fam:
        if "falha" in r:
            d.append(f"| {r['propulsor']} | {r['n_ativos']} | {br(r['altitude_km'])} | " + " | ".join(["—"] * 23)
                     + f" | **{r['situacao']}** |")
            continue
        d.append(f"| {r['propulsor']} | {r['n_ativos']} | {br(r['altitude_km'])} | {r['n_instalados']} | {br(r['potencia_kw'], 1)} | {br(r['xenonio_kg'])} | "
                 f"{br(r['xenonio_por_propulsor_kg'])} | {br(r['vida_kg'])} | {br(r['massa_propulsores_e_ppu_kg'])} | {br(r['orbitador_kg'])} | "
                 f"{br(r['margem_falcon_heavy'] * 100, 1)} % | {br(r['c3_km2_s2'], 2)} | {br(r['dla_graus'], 1)} | {r['partida_terra']} | {br(r['ida_dias'])} | "
                 f"{r['chegada_marte']} | {br(r['descida_dias'])} | {r['pronto_no_encontro']} | {r['ultimo_lancamento_mav']} | {r['lancamento_mav']} | "
                 f"{br(r['subida_dias'])} | {r['partida_marte']} | {br(r['volta_dias'])} | {r['chegada_terra']} | {'sim' if r['descida_cruza_conjuncao'] else 'não'} | "
                 f"{'sim' if r['subida_cruza_conjuncao'] else 'não'} | {'**sim**' if r['fecha'] else 'não'} |")
    d += ["", "### Verificação das soluções gravadas", "",
          "Todas as tentativas de cada configuração, por origem. Pior: o maior entre os resíduos de continuidade, as violações "
          f"das desigualdades e as dos limites, contra o aceito ({_sci(_oc()['residuo_max'])}, P-118). Descasamento: massa do "
          "fecho menos a massa gravada no trecho (m0 da volta; chegada a Marte), de o fecho por razões de massas (método da "
          "Etapa 2) não ter fechado por completo nas iterações da otimização; o relativo (o maior dos dois) contra a P-125 ("
          f"{_sci(v(cfg['verificacao']['descasamento_fecho_relativo_max']))}).", "",
          "| Propulsor | Ativos | Encontro (km) | Origem | Situação | Pior | Resíduo ida; volta | Descasamento m0 da volta (kg) | Descasamento chegada a Marte (kg) | Descasamento relativo | Margem no Falcon Heavy | Pronto no encontro | Escolhida |",
          "| :- | -: | -: | :- | :- | -: | :- | -: | -: | -: | -: | :- | :- |"]
    for r in fam:
        esc = None if "falha" in r else (r["origem"], r["margem_falcon_heavy"])
        for x in r["sem_solucao"]:
            res = "—" if x["residuo_minimo"] is None else _sci(x["residuo_minimo"])
            d.append(f"| {r['propulsor']} | {r['n_ativos']} | {br(r['altitude_km'])} | {x['origem']} | otimizador: {x['situacao']} "
                     f"(menor resíduo {res}) | — | — | — | — | — | — | — | — |")
        for x in r["candidatas"]:
            if "erro" in x:
                d.append(f"| {r['propulsor']} | {r['n_ativos']} | {br(r['altitude_km'])} | {x['origem']} | não verificada: {x['erro']} "
                         "| — | — | — | — | — | — | — | — |")
                continue
            vv = x["verificacao"]
            d.append(f"| {r['propulsor']} | {r['n_ativos']} | {br(r['altitude_km'])} | {x['origem']} | "
                     f"{'verificada' if vv['verificada'] else 'não verificada'}{' (não finito: ' + ', '.join(vv['nao_finitos']) + ')' if vv['nao_finitos'] else ''} | {_sci(vv['pior'])} | {_sci(vv['residuo_ida'])}; {_sci(vv['residuo_volta'])} | "
                     f"{br(vv['descasamento_m0_volta_kg'], 3)} | {br(vv['descasamento_chegada_marte_kg'], 3)} | {_sci(vv['descasamento_relativo'])} | {br(x['margem_falcon_heavy'] * 100, 2)} % | "
                     f"{x['pronto_no_encontro']} | {'**sim**' if esc == (x['origem'], x['margem_falcon_heavy']) else '—'} |")
    d += estocagem_mav(fam)
    (SAIDA / "diagnostico_orbitador_so_eletrico.md").write_text("\n".join(d) + "\n", encoding="utf-8")


def estocagem_mav(fam):
    """Estocagem do MAV na superfície (decisão do Fabio, 2026-11-20, item 6): do pouso do lander ao lançamento do MAV, com
    o aquecimento (o mesmo modelo da P-027, independente do tempo), a energia, os RHUs no ano do lançamento ([F155]) e a
    longitude solar Ls nas duas pontas (orbital.energia.geometria_marte). O sólido vem da sua fonte única, a lei nominal da
    P-113 (results/familia1/inerte_solido.yaml); o hipergólico, de results/familia1/mavs.yaml. As linhas do sólido da P-111
    (mavs.yaml) ficam na tabela, marcadas como substituídas, para comparação (errata da issue #77, 2026-11-27)."""
    from orbital import energia as en
    mv = ler("results/familia1/mavs.yaml")
    ins = ler("results/familia1/inerte_solido.yaml")
    tf = ler("config/familia1.yaml")["termico"]
    ref = ler("results/etapa7.2/rotas_mav.yaml")["missao"]
    pouso = D(ref["chegada"])
    nom = next(c for c in ins["casos"] if c["lei"] == ins["variante_nominal"])
    SUBST = " (P-111, substituído pela P-113; errata da issue #77)"
    mavs = ([(f"Sólido, lei {nom['lei'][0]} da P-113, {ins['altitude_km']:.0f} km, {rot}", ins["altitude_km"], nom[k]["termico"]["temperatura_c"],
              nom[k]["termico"]["potencia_w"]) for rot, k in (("sem margem", "sem_margem"), ("com a margem da P-014", "com_margem"))]
            + [(x["rotulo"], x["altitude_km"], x["termico"]["temperatura_c"], x["termico"]["potencia_w"]) for x in mv["hipergolico"] if "termico" in x]
            + [(x["rotulo"] + SUBST, x["altitude_km"], x["termico"]["temperatura_c"], x["termico"]["potencia_w"]) for x in mv["solido"] if "termico" in x])
    ls_pouso = en.geometria_marte(pouso.isoformat() + "T00:00:00")[0]
    ls_a, ls_b = ler("config/orbitador_so_eletrico.yaml")["estocagem_mav"]["estacao_tempestades_ls"]["valor"]

    def temporadas(d0, d1):
        """Temporadas de tempestade (P-124) tocadas entre d0 e d1, contadas pelas entradas na janela de Ls (passo de 1 d)."""
        n, dentro, d = 0, False, d0
        while d <= d1:
            ls = en.geometria_marte(d.isoformat() + "T00:00:00")[0]
            agora = ls_a <= ls <= ls_b
            n += agora and not dentro
            dentro, d = agora, d + dt.timedelta(days=1)
        return n
    lanc_ref = D(ref["lancamento_mav_mais_cedo"])
    out = ["", "## Estocagem do MAV na superfície", "",
           f"Pouso do lander em {pouso.isoformat()} (Ls {br(ls_pouso, 1)}°). Aquecimento (modelo da P-027) do sólido de "
           "results/familia1/inerte_solido.yaml (lei nominal da P-113) e do hipergólico de results/familia1/mavs.yaml; RHU com a potência do ano do lançamento do MAV ([F155] p. 1: 0,90 W em 2014, menos 0,01 W por "
           "ano). Teto oferecido ao New Frontiers: " + br(v(tf["rhu_teto_new_frontiers"])) + " RHUs ([F155] p. 2).",
           f"Temporadas de tempestade global (Ls {ls_a}° a {ls_b}°, P-124) tocadas entre o pouso e o lançamento do MAV; na "
           f"missão de referência (MAV no lançamento mais cedo, {lanc_ref.isoformat()}): {temporadas(pouso, lanc_ref)}.",
           "Envelhecimento do propelente sólido: só há resultado publicado da fase de vácuo ([F263] PDF p. 1, perda de massa "
           "abaixo de 0,1 %); a fase de um ano em condições de superfície de Marte estava planejada ([F263] PDF p. 1) e não há "
           "resultado publicado achado; o projeto do MSR previa cerca de um ano na superfície ([F35] PDF p. 1).", "",
           "| Propulsor | Ativos | Encontro (km) | Lançamento do MAV | Dias na superfície | Ls no lançamento (°) | Temporadas de tempestade | MAV | Temperatura mantida (°C) | Aquecimento (W) | Energia (kWh) | RHUs |",
           "| :- | -: | -: | :- | -: | -: | -: | :- | -: | -: | -: | -: |"]
    cache_temp = {}
    for r in fam:
        if "falha" in r:
            continue
        lanc = D(r["lancamento_mav"])
        dias = (lanc - pouso).days
        ls = en.geometria_marte(lanc.isoformat() + "T00:00:00")[0]
        rhu_w = v(tf["rhu_w_2014"]) - v(tf["rhu_queda_w_ano"]) * (lanc.year - v(tf["rhu_ano_referencia"]))
        if lanc not in cache_temp:
            cache_temp[lanc] = temporadas(pouso, lanc)
        for rot, h, tc, p in mavs:
            if h != r["altitude_km"]:
                continue
            out.append(f"| {r['propulsor']} | {r['n_ativos']} | {br(h)} | {lanc.isoformat()} | {dias} | {br(ls, 1)} | {cache_temp[lanc]} | {rot} | "
                       f"{br(tc)} | {br(p, 1)} | {br(p * 24 * dias / 1000)} | {math.ceil(p / rhu_w)} |")
    teto = br(v(tf["rhu_teto_new_frontiers"]))
    out += ["", "### Errata (2026-11-27, issue #77): o sólido passou da P-111 para a P-113", "",
            "- **O que estava escrito:** até o PR #74, esta seção lia o aquecimento dos dois sólidos de results/familia1/mavs.yaml, "
            "com o inerte proporcional ao propelente da P-111 (as linhas marcadas \"substituído pela P-113\" na tabela acima). O "
            f"relatório do ponto de parada de 2026-11-26 e o PR #74 concluíram daí que, com o teto de {teto} RHUs, nenhum dos dois "
            "MAVs, com a margem da P-014, se mantinha aquecido só com RHUs na espera.",
            "- **O erro:** a conclusão vigente da família 1 (results/etapa7.2/portao_mav.md, portão de 2026-11-12) usa para o sólido "
            "a lei A da P-113 (results/familia1/inerte_solido.md), com outra massa de propelente; esta seção herdou de mavs.yaml o "
            "modelo que não é o da conclusão.",
            "- **O que muda:** o sólido vem agora da sua fonte única, a lei nominal da P-113 (results/familia1/inerte_solido.yaml), com "
            "o mesmo modelo de aquecimento (orbital.mav.aquecimento); os RHUs vigentes do sólido são os das linhas \"lei A da "
            "P-113\". As linhas da P-111 ficam só para comparação.",
            "- **O que não muda:** o fecho a 380 km por propulsor (não lê os MAVs; usa results/familia1/missao.yaml e "
            "results/etapa7.2/rotas_mav.yaml) e o hipergólico; a geometria do sólido com margem segue com as pendências do "
            "próprio resultado (results/familia1/inerte_solido.md: \"Chega?\" e a energia que sobra na subida)."]
    return out


# Caso publicado e blocos da otimização local, fora da comparação. Os blocos não são versionados desde 2026-11-25: as
# soluções ficam em data/orbitador_so_eletrico/ (--salva-solucoes).
PARCIAIS = RAIZ / "results" / "conferencia" / "orbitador_so_eletrico"
VARIANTES = [("esquerda", False), ("esquerda", True), ("direita", False), ("direita", True)]


def blocos():
    """Blocos da otimização local (fora do CI desde 2026-11-24), em ordem fixa: por órbita e propulsor (ou variante de vida), uma cadeia de n
    decrescente (decisão do Fabio, 2026-11-22), dividida em blocos de até `bloco_cadeia` valores (P-122) quando não cabe
    num job; cada bloco continua do anterior da mesma cadeia. Devolve (propulsor, altitude, n do bloco, blocos anteriores)."""
    ms = ler("config/orbitador_so_eletrico.yaml")["missao"]
    out = []
    for h in ms["altitudes_km"]["valor"]:
        for nome, ns in ms["n_ativos"]["valor"].items():
            k = int(ms["bloco_cadeia"]["valor"][nome])
            ns = sorted(ns, reverse=True)
            cad = [ns[i:i + k] for i in range(0, len(ns), k)]
            out += [(nome, float(h), b, cad[:i]) for i, b in enumerate(cad)]
    return out


def _rotulo_bloco(ns):
    return f"{max(ns)}-{min(ns)}"


def _arquivo_bloco(nome, h, ns):
    slug = "".join(ch if ch.isalnum() else "_" for ch in nome.lower()).strip("_")
    return PARCIAIS / f"bloco_{slug}_{int(h)}_{_rotulo_bloco(ns)}.yaml"


def _grava(caminho, obj):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(yaml.safe_dump(nativo(obj), sort_keys=False, allow_unicode=True, default_flow_style=None), encoding="utf-8")


def roda_caso_publicado():
    with ProcessPoolExecutor(max_workers=max(1, min(os.cpu_count() or 1, len(VARIANTES)))) as ex:
        casos = list(ex.map(caso_publicado, VARIANTES))
    _grava(PARCIAIS / "caso_publicado.yaml", {"gerado_por": "tools/orbitador_so_eletrico.py --caso-publicado", "casos": casos})


def roda_bloco(nome, h, rotulo):
    nome_, h_, ns, ant = next(x for x in blocos() if x[0] == nome and x[1] == float(h) and _rotulo_bloco(x[2]) == rotulo)
    sementes = {}
    for b in ant:   # gravados pelos blocos anteriores da mesma cadeia (no CI, artefatos das partes de que este depende)
        sementes.update(ler(str(_arquivo_bloco(nome_, h_, b).relative_to(RAIZ)))["sementes"])
    confs, proprias = _cadeia(nome_, h_, ns, sementes)
    _grava(_arquivo_bloco(nome_, h_, ns), {"gerado_por": f"tools/orbitador_so_eletrico.py --bloco {nome} {int(h)} {rotulo}",
                                          "configuracoes": confs, "sementes": proprias})


def roda_cadeia(nome, h):
    """Os blocos de uma cadeia, em sequência (o mesmo que os jobs encadeados do CI)."""
    for nome_, h_, ns, _ in blocos():
        if nome_ == nome and h_ == h:
            roda_bloco(nome, h, _rotulo_bloco(ns))


SOLUCOES = RAIZ / "data" / "orbitador_so_eletrico"   # soluções gravadas (versionadas): o CI só as verifica


def _slug(nome):
    return "".join(ch if ch.isalnum() else "_" for ch in nome.lower()).strip("_")


def _arquivo_solucoes(nome, h):
    return SOLUCOES / f"solucoes_{_slug(nome)}_{int(h)}.yaml"


def _ambiente_da_parte(bloco):
    """Ambiente gravado pela regeneração do CI ao lado do bloco (artefato: <parte>/_log/<parte>.json), se houver."""
    import json
    for pasta in list(bloco.parents)[:4]:
        for j in sorted((pasta / "_log").glob("*.json")) if (pasta / "_log").is_dir() else []:
            a = json.loads(j.read_text(encoding="utf-8")).get("ambiente", {})
            return {k: a[k] for k in ("cpu", "commit", "commit_head_do_pr", "python", "numpy", "scipy") if k in a}
    return None


def salva_solucoes(fontes):
    """Junta as soluções das rodadas de otimização (blocos das cadeias, de uma ou mais máquinas) em
    data/orbitador_so_eletrico/solucoes_<propulsor>_<altitude>.yaml, um arquivo por propulsor e órbita (decisão do
    Fabio, 2026-11-24). `fontes`: [(rótulo, pasta, descrição)], na ordem em que as tentativas são gravadas.

    Formato (versão 1): por configuração (n_ativos), a lista de tentativas, cada uma com a origem (rótulo, descrição,
    arquivo do bloco, comando e, quando gravado pela regeneração, o ambiente) e ou a solução (empuxo_n, isp_s e, para a
    ida e a volta, t0 e tof em s ET, m0 e mf em kg, vinf0 e vinf1 em km/s no ECLIPJ2000 e u, os comandos por segmento,
    N × 3, fração do empuxo máximo), ou a falha do otimizador (com a situação e o menor resíduo). Os floats saem com repr:
    a volta pelo YAML é exata."""
    ms = ler("config/orbitador_so_eletrico.yaml")["missao"]
    for h in ms["altitudes_km"]["valor"]:
        for nome, ns in ms["n_ativos"]["valor"].items():
            tent = {int(n): [] for n in sorted(ns)}
            for rot, pasta, desc in fontes:
                for arq in sorted(Path(pasta).rglob(f"bloco_{_slug(nome)}_{int(h)}_*.yaml")):
                    d = yaml.safe_load(arq.read_text(encoding="utf-8"))
                    amb = _ambiente_da_parte(arq)
                    origem = {"rotulo": rot, "descricao": desc, "arquivo": arq.name, "gerado_por": d["gerado_por"],
                              **({"ambiente": amb} if amb else {})}
                    for c in d["configuracoes"]:
                        n = int(c["n_ativos"])
                        if "falha" in c:
                            tent[n].append({"origem": origem, "falha": c["falha"], "situacao": c["situacao"],
                                            "residuo_minimo": c["residuo_minimo"]})
                        else:
                            tent[n].append({"origem": origem, "solucao": d["sementes"][n]})
            _grava(_arquivo_solucoes(nome, h), {
                "gerado_por": "tools/orbitador_so_eletrico.py --salva-solucoes", "formato": 1, "propulsor": nome,
                "altitude_km": float(h), "formulacao_dla": ler("config/orbitador_so_eletrico.yaml")["otimizador"]["formulacao_dla"]["valor"],
                "configuracoes": [{"n_ativos": n, "tentativas": x} for n, x in tent.items()]})


def _nota_fecho(r, cfg):
    """Ordem das soluções verificadas de uma configuração: fecha (as quatro conclusões "sim") > na banda (sem "não") > não."""
    c = _conclusoes(r, cfg)
    return 2 if c == ["sim"] * 4 else 1 if "não" not in c else 0


def _verifica_uma(nome, n, h, solucao):
    """Uma solução gravada verificada (fecho com verificar=True), ou {"erro": ...} se a verificação falha antes do fim
    (valor não finito, massas que não convergem, xenônio acima da vida, conta impossível)."""
    try:
        r = fecho(nome, n, h, chutes=_de_semente(solucao), verificar=True)
    except (RuntimeError, ValueError, ArithmeticError) as x:
        return {"erro": f"{type(x).__name__}: {x}"}
    r.pop("_chutes")
    return r


def verifica():
    """Verifica as soluções gravadas, sem reotimizar (decisão do Fabio, 2026-11-24): por configuração, cada solução é
    propagada (fecho com verificar=True) e fica a melhor das verificadas (_nota_fecho, depois a maior margem), com a
    origem. Sem solução verificada: "nenhuma solução verificada" (o que não demonstra inviabilidade)."""
    cfg = ler("config/orbitador_so_eletrico.yaml")
    ms = cfg["missao"]
    t_ini = time.perf_counter()
    fam = []
    for h in ms["altitudes_km"]["valor"]:
        for nome in ms["n_ativos"]["valor"]:
            arq = ler(str(_arquivo_solucoes(nome, h).relative_to(RAIZ)))
            if arq["formulacao_dla"] != cfg["otimizador"]["formulacao_dla"]["valor"]:
                raise ValueError(f"{_arquivo_solucoes(nome, h).name}: soluções da formulação {arq['formulacao_dla']!r}, "
                                 f"config com {cfg['otimizador']['formulacao_dla']['valor']!r}")
            for c in arq["configuracoes"]:
                n, cands, sem = int(c["n_ativos"]), [], []
                for tn in c["tentativas"]:
                    rot = tn["origem"]["rotulo"]
                    if "solucao" not in tn:
                        sem.append({"origem": rot, "situacao": tn["situacao"], "residuo_minimo": tn["residuo_minimo"]})
                        continue
                    cands.append({**_verifica_uma(nome, n, float(h), tn["solucao"]), "origem": rot})
                ok = [r for r in cands if "erro" not in r and r["verificacao"]["verificada"]]
                base = {"candidatas": cands, "sem_solucao": sem}
                if ok:
                    fam.append({**max(ok, key=lambda r: (_nota_fecho(r, cfg), r["margem_falcon_heavy"])), **base})
                else:
                    fam.append({"propulsor": nome, "n_ativos": n, "altitude_km": float(h), "falha": "nenhuma solução verificada",
                                "situacao": "nenhuma solução verificada", **base})
    print(f"verificação: {sum(len(r['candidatas']) for r in fam)} soluções em {time.perf_counter() - t_ini:.1f} s", flush=True)
    casos = ler("results/conferencia/orbitador_so_eletrico/caso_publicado.yaml")["casos"]
    SAIDA.mkdir(parents=True, exist_ok=True)
    escreve(casos, fam)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--caso-publicado", action="store_true")
    ap.add_argument("--bloco", nargs=3, metavar=("PROPULSOR", "ALTITUDE_KM", "N_MAX-N_MIN"))
    ap.add_argument("--verifica", action="store_true")
    ap.add_argument("--salva-solucoes", nargs=3, action="append", metavar=("ROTULO", "PASTA", "DESCRICAO"))
    a = ap.parse_args()
    if a.caso_publicado:
        roda_caso_publicado()
    elif a.bloco:
        roda_bloco(a.bloco[0], float(a.bloco[1]), a.bloco[2])
    elif a.verifica:
        verifica()
    elif a.salva_solucoes:
        salva_solucoes(a.salva_solucoes)
    else:   # otimização local (fora do CI): as cadeias (cada uma com os seus blocos em sequência) e o caso publicado em paralelo
        cads = list(dict.fromkeys((b[0], b[1]) for b in blocos()))
        with ProcessPoolExecutor(max_workers=max(1, min(os.cpu_count() or 1, len(cads) + 1))) as ex:
            fs = [ex.submit(roda_cadeia, nome, h) for nome, h in cads] + [ex.submit(roda_caso_publicado)]
            for f in fs:
                f.result()


if __name__ == "__main__":
    main()
