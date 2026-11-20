"""Trajetória heliocêntrica de baixo empuxo (Etapa 2 do plano, issue #68, item a): transcrição de Sims–Flanagan,
otimização com scipy e propagação contínua para conferência.

Transcrição (método de Sims–Flanagan, forma usual):
  - a perna, de duração `tof`, é dividida em N segmentos iguais de duração Δt;
  - em cada segmento, o empuxo tem direção û_i fixa e fração |u_i| ≤ 1 do empuxo máximo; a massa gasta é
    |u_i| · ṁ_max · Δt, exata para empuxo constante;
  - o segmento compõe dois fluxos exatos: o voo kepleriano (orbital.kepler.propagar, conferido na Fase 1) e o do empuxo
    sozinho (posição parada, Δv = c · ln(m_antes / m_depois), equação do foguete). A forma usual de Sims–Flanagan é a
    composição de ordem 2 (voo Δt/2, impulso, voo Δt/2); o padrão aqui é a de ordem 4 (Yoshida), que aproxima o empuxo
    contínuo com erro muito menor no mesmo N (conferido contra a propagação contínua nos testes);
  - os primeiros `n_frente` segmentos são propagados para a frente a partir da partida, e os demais para trás a partir da
    chegada; a perna é contínua quando posição, velocidade e massa coincidem no ponto de encontro (7 restrições).

Propagação contínua (conferência da transcrição): o mesmo perfil, com empuxo constante em cada segmento, integrado com
solve_ivp (DOP853). A diferença entre o estado final contínuo e o alvo mede o erro da transcrição; ela cai com N.

Modelo: Sol como massa pontual (problema de dois corpos), sem perturbação dos planetas, partida e chegada nos centros dos
planetas (a fuga e a captura ficam fora da perna heliocêntrica), empuxo máximo constante (potência disponível constante
na faixa de distâncias da perna) e ciclo de trabalho aplicado como redução do empuxo médio.

Unidades: km, s, kg; empuxo em N (aceleração em km/s² = N / kg / 1000).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

from orbital import kepler
from orbital.foguete import G0


@dataclass(frozen=True)
class Motor:
    empuxo_n: float     # empuxo máximo total (todos os propulsores ativos), já com o ciclo de trabalho
    isp_s: float

    @property
    def c_km_s(self):
        return self.isp_s * G0

    @property
    def vazao_kg_s(self):
        return self.empuxo_n / (self.isp_s * G0 * 1e3)


def _impulso(v, m, u, motor, dt, sentido):
    """Fluxo exato só do empuxo (posição parada) por uma duração dt (k,), que pode ser negativa na composição de ordem 4.
    v (k, 3), m (k,), u (k, 3). sentido = +1: de antes para depois; −1: de depois para antes (a inversa)."""
    a = np.linalg.norm(u, axis=1)
    dm = a * motor.vazao_kg_s * dt
    m2 = m - dm if sentido > 0 else m + dm
    if np.any(m2 <= 0):
        raise ValueError("massa não positiva no segmento")
    dirn = np.divide(u, a[:, None], out=np.zeros_like(u), where=a[:, None] > 0)
    if sentido > 0:
        return v + (motor.c_km_s * np.log(m / m2))[:, None] * dirn, m2
    return v - (motor.c_km_s * np.log(m2 / m))[:, None] * dirn, m2


def _propagar_um(mu, r, v, dt):
    r1, v1 = kepler.propagar(mu, r[0], v[0], float(dt[0]))
    return r1[None, :], v1[None, :]


# Composição dos dois fluxos exatos (Kepler e empuxo) em cada segmento: frações (voo, empuxo, voo, ..., voo).
# Ordem 2: Strang (voo Δt/2, empuxo Δt, voo Δt/2), a forma usual de Sims–Flanagan (impulso no meio do segmento).
# Ordem 4: Yoshida (1990), com w1 = 1 / (2 − 2^(1/3)) e w0 = −2^(1/3) / (2 − 2^(1/3)); a soma das frações de empuxo é 1,
# então a massa gasta no segmento é a mesma da ordem 2.
_W1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
_W0 = -(2.0 ** (1.0 / 3.0)) * _W1
_COMPOSICAO = {2: ((0.5, 0.5), (1.0,)),
               4: ((_W1 / 2, (_W0 + _W1) / 2, (_W0 + _W1) / 2, _W1 / 2), (_W1, _W0, _W1))}


def transcricao_lote(mu, r0, v0, m0, r1, v1, m1, tof, u, motor, n_frente=None, ordem=4):
    """Transcrição de um lote de k pernas: r0, v0, r1, v1 (k, 3); m0, m1, tof (k,); u (k, N, 3).
    Devolve ((r, v, m) pela frente, (r, v, m) por trás) no ponto de encontro, cada um com primeira dimensão k."""
    u = np.asarray(u, dtype=float)
    n = u.shape[1]
    n_frente = n // 2 if n_frente is None else n_frente
    dt = np.asarray(tof, dtype=float) / n
    voo, emp = _COMPOSICAO[ordem]
    prop = kepler.propagar_lote if len(u) > 1 else _propagar_um   # um só ponto: o propagador escalar é mais rápido
    r, v, m = np.asarray(r0, float), np.asarray(v0, float), np.asarray(m0, float)
    for i in range(n_frente):
        for j, e in enumerate(emp):
            r, v = prop(mu, r, v, voo[j] * dt)
            v, m = _impulso(v, m, u[:, i], motor, e * dt, +1)
        r, v = prop(mu, r, v, voo[-1] * dt)
    rb, vb, mb = np.asarray(r1, float), np.asarray(v1, float), np.asarray(m1, float)
    for i in range(n - 1, n_frente - 1, -1):
        rb, vb = prop(mu, rb, vb, -voo[-1] * dt)
        for j in range(len(emp) - 1, -1, -1):
            vb, mb = _impulso(vb, mb, u[:, i], motor, emp[j] * dt, -1)
            rb, vb = prop(mu, rb, vb, -voo[j] * dt)
    return (r, v, m), (rb, vb, mb)


def transcricao(mu, r0, v0, m0, r1, v1, m1, tof, u, motor, n_frente=None, ordem=4):
    """Uma perna: (estado no encontro pela frente, estado no encontro por trás), cada um (r, v, m).

    (r0, v0, m0): partida, já com o v∞; (r1, v1, m1): chegada, já com o v∞; u: (N, 3), |u_i| ≤ 1."""
    (r, v, m), (rb, vb, mb) = transcricao_lote(mu, np.atleast_2d(r0), np.atleast_2d(v0), np.atleast_1d(float(m0)),
                                               np.atleast_2d(r1), np.atleast_2d(v1), np.atleast_1d(float(m1)),
                                               np.atleast_1d(float(tof)), np.asarray(u, float).reshape(1, -1, 3), motor,
                                               n_frente, ordem)
    return (r[0], v[0], float(m[0])), (rb[0], vb[0], float(mb[0]))


def propagar_continuo(mu, r0, v0, m0, tof, u, motor, rtol=1e-11):
    """Estado final (r, v, m) com empuxo constante em cada segmento (direção û_i, empuxo |u_i| · T_max)."""
    u = np.asarray(u, dtype=float).reshape(-1, 3)
    dt = tof / len(u)
    y = np.r_[np.asarray(r0, float), np.asarray(v0, float), float(m0)]
    for ui in u:
        a = float(np.linalg.norm(ui))
        dirn = ui / a if a > 0 else np.zeros(3)
        y = _integra(mu, y, dt, lambda t, s, d=dirn, k=a: d * k * motor.empuxo_n / (s[6] * 1e3), a * motor.vazao_kg_s, rtol)
    return y[:3], y[3:6], float(y[6])


def propagar_lei(mu, r0, v0, tempo, aceleracao, m0=1.0, vazao=0.0, rtol=1e-11):
    """Estado final (r, v, m) com aceleração dada por `aceleracao(t, estado)` (vetor, nas unidades de r/tempo²).

    Serve para as conferências: aceleração nula (contra Kepler e Lambert) e tangencial constante (contra [F113])."""
    y = _integra(mu, np.r_[np.asarray(r0, float), np.asarray(v0, float), float(m0)], tempo, aceleracao, vazao, rtol)
    return y[:3], y[3:6], float(y[6])


def _integra(mu, y0, tempo, aceleracao, vazao, rtol):
    escala_r = float(np.linalg.norm(y0[:3]))
    escala_v = float(np.linalg.norm(y0[3:6])) or math.sqrt(mu / escala_r)

    def f(t, s):
        r = s[:3]
        a = -mu * r / float(np.linalg.norm(r)) ** 3 + aceleracao(t, s)
        return np.r_[s[3:6], a, -vazao]
    atol = np.r_[[escala_r * rtol * 1e-1] * 3, [escala_v * rtol * 1e-1] * 3, max(abs(y0[6]), 1.0) * rtol * 1e-1]
    sol = solve_ivp(f, (0.0, tempo), y0, method="DOP853", rtol=rtol, atol=atol)
    if not sol.success:
        raise RuntimeError(f"integração não convergiu: {sol.message}")
    return sol.y[:, -1]


# ---------------------------------------------------------------- otimização

@dataclass
class Perna:
    """Perna heliocêntrica com partida e chegada em planetas (estados por `estado_partida(et)` e `estado_chegada(et)`).

    Variáveis: época de partida t0 (s, ET), duração tof (s), v∞ de partida e de chegada (vetores, km/s), massas m0 e mf
    (kg) e o perfil de empuxo u (N × 3). Variável com limites iguais fica fixa."""
    mu: float
    estado_partida: object
    estado_chegada: object
    motor: Motor
    n_segmentos: int
    t0: tuple            # (mín, máx) em s ET
    tof: tuple           # (mín, máx) em s
    vinf_partida: tuple  # (mín, máx) do módulo, km/s
    vinf_chegada: tuple  # (mín, máx) do módulo, km/s
    m0: tuple            # (mín, máx) kg
    mf: tuple            # (mín, máx) kg
    escala_m: float = field(default=1000.0)


_DIA = 86400.0


class _Avaliador:
    """Desfaz a escala das variáveis e guarda a última transcrição (objetivo e restrições usam o mesmo ponto)."""

    def __init__(self, p: Perna):
        self.p = p
        self.ua = 1.495978707e8
        self.vref = math.sqrt(p.mu / self.ua)
        self._z = None
        self._res = None

    def desfaz(self, z):
        p, n = self.p, self.p.n_segmentos
        t0, tof = z[0] * _DIA, z[1] * _DIA
        m0, mf = z[2] * p.escala_m, z[3] * p.escala_m
        vi0, vi1 = z[4:7], z[7:10]
        u = z[10:10 + 3 * n].reshape(n, 3)
        return t0, tof, m0, mf, vi0, vi1, u

    def lote(self, zs):
        """Resíduos de continuidade (k, 7) de um lote de pontos zs (k, n_variaveis)."""
        zs = np.atleast_2d(zs)
        n = self.p.n_segmentos
        t0, tof = zs[:, 0] * _DIA, zs[:, 1] * _DIA
        m0, mf = zs[:, 2] * self.p.escala_m, zs[:, 3] * self.p.escala_m
        u = zs[:, 10:10 + 3 * n].reshape(len(zs), n, 3)
        cache = {}
        rp, vp, rc, vc = (np.empty((len(zs), 3)) for _ in range(4))
        for i in range(len(zs)):
            kp, kc = ("p", float(t0[i])), ("c", float(t0[i] + tof[i]))
            if kp not in cache:
                cache[kp] = self.p.estado_partida(kp[1])
            if kc not in cache:
                cache[kc] = self.p.estado_chegada(kc[1])
            rp[i], vp[i] = cache[kp]
            rc[i], vc[i] = cache[kc]
        try:
            (r, v, m), (rb, vb, mb) = transcricao_lote(self.p.mu, rp, vp + zs[:, 4:7], m0, rc, vc + zs[:, 7:10], mf, tof, u,
                                                       self.p.motor)
            return np.c_[(r - rb) / self.ua, (v - vb) / self.vref, (m - mb) / self.p.escala_m]
        except (ValueError, RuntimeError):
            return np.vstack([self.avalia_um(z) for z in zs]) if len(zs) > 1 else np.full((1, 7), 1e3)

    def avalia_um(self, z):
        return self.lote(np.atleast_2d(z))[0]

    def avalia(self, z):
        if self._z is not None and np.array_equal(z, self._z):
            return self._res
        res = self.avalia_um(z)
        self._z, self._res = np.array(z, copy=True), res
        return res

    def jacobiano(self, z):
        """Diferenças finitas para a frente, com todas as perturbações propagadas num lote."""
        h = 1.4901161193847656e-08 * np.maximum(1.0, np.abs(z))
        zs = np.vstack([z, z + np.diag(h)])
        res = self.lote(zs)
        return ((res[1:] - res[0]) / h[:, None]).T


def otimizar(p: Perna, objetivo, chute, maxiter=500, ftol=1e-10, ineq_extra=None):
    """Minimiza `objetivo(t0, tof, m0, mf, vinf0, vinf1)` sujeito à continuidade da perna, |u_i| ≤ 1, aos limites e,
    se dada, a `ineq_extra(t0, tof, m0, mf, vinf0, vinf1) ≥ 0` (vetor).

    `chute`: dicionário com t0, tof (s), m0, mf (kg), vinf0, vinf1 (vetores) e u (N × 3). Devolve um dicionário com a
    solução, o resíduo de continuidade e o estado do otimizador."""
    av = _Avaliador(p)
    n = p.n_segmentos
    z0 = np.r_[chute["t0"] / _DIA, chute["tof"] / _DIA, chute["m0"] / p.escala_m, chute["mf"] / p.escala_m,
               np.asarray(chute["vinf0"], float), np.asarray(chute["vinf1"], float), np.asarray(chute["u"], float).ravel()]
    lim = ([(p.t0[0] / _DIA, p.t0[1] / _DIA), (p.tof[0] / _DIA, p.tof[1] / _DIA),
            (p.m0[0] / p.escala_m, p.m0[1] / p.escala_m), (p.mf[0] / p.escala_m, p.mf[1] / p.escala_m)]
           + [(-p.vinf_partida[1], p.vinf_partida[1])] * 3 + [(-p.vinf_chegada[1], p.vinf_chegada[1])] * 3
           + [(-1.0, 1.0)] * (3 * n))
    z0 = np.clip(z0, [a for a, _ in lim], [b for _, b in lim])

    def f(z):
        t0, tof, m0, mf, vi0, vi1, _ = av.desfaz(z)
        return objetivo(t0, tof, m0, mf, vi0, vi1)

    def ineq(z):
        _, _, _, _, vi0, vi1, u = av.desfaz(z)
        g = [1.0 - np.sum(u * u, axis=1)]
        a0, a1 = float(vi0 @ vi0), float(vi1 @ vi1)
        g.append([p.vinf_partida[1] ** 2 - a0, a0 - p.vinf_partida[0] ** 2, p.vinf_chegada[1] ** 2 - a1,
                  a1 - p.vinf_chegada[0] ** 2])
        if ineq_extra is not None:
            t0, tof, m0, mf, _, _, _ = av.desfaz(z)
            g.append(np.atleast_1d(ineq_extra(t0, tof, m0, mf, vi0, vi1)))
        return np.concatenate(g)

    sol = minimize(f, z0, method="SLSQP", bounds=lim,
                   constraints=[{"type": "eq", "fun": av.avalia, "jac": av.jacobiano}, {"type": "ineq", "fun": ineq}],
                   options={"maxiter": maxiter, "ftol": ftol})
    t0, tof, m0, mf, vi0, vi1, u = av.desfaz(sol.x)
    res = av.avalia(sol.x)
    return {"t0": t0, "tof": tof, "m0": m0, "mf": mf, "vinf0": vi0, "vinf1": vi1, "u": u, "sucesso": bool(sol.success),
            "mensagem": str(sol.message), "iteracoes": int(sol.nit), "residuo": res, "residuo_max": float(np.max(np.abs(res))),
            "violacao_u": float(max(0.0, -np.min(ineq(sol.x)))), "objetivo": float(sol.fun)}


def dv_total(u, tof, m0, motor):
    """Δv entregue pelo perfil (km/s): soma de c · ln(m_antes / m_depois) nos segmentos."""
    u = np.asarray(u, dtype=float).reshape(-1, 3)
    dt = tof / len(u)
    m, dv = float(m0), 0.0
    for ui in u:
        m2 = m - float(np.linalg.norm(ui)) * motor.vazao_kg_s * dt
        dv += motor.c_km_s * math.log(m / m2)
        m = m2
    return dv


def viabilizar(p: Perna, chute, max_nfev=300):
    """Ponto viável com as datas do chute fixas: mínimos quadrados (scipy least_squares, método trf) no resíduo de
    continuidade, com o empuxo em coordenadas esféricas (fração em [0, 1], dois ângulos livres) e os v∞ em módulo (nos
    limites da perna) e direção; a massa livre (m0 ou mf, a que tiver limites diferentes) fica nos seus limites.
    Devolve o chute atualizado e o maior resíduo; serve de partida para `otimizar`, que precisa de um ponto viável."""
    from scipy.optimize import least_squares
    av = _Avaliador(p)
    n = p.n_segmentos
    t0, tof = chute["t0"], chute["tof"]
    m0_livre = p.m0[0] < p.m0[1]

    def esf(x):
        x = np.asarray(x, float)
        a = float(np.linalg.norm(x))
        if a == 0:
            return 0.0, 0.0, 0.0
        return a, math.atan2(x[1], x[0]), math.asin(max(-1.0, min(1.0, x[2] / a)))

    def cart(a, th, fi):
        return a * np.array([math.cos(fi) * math.cos(th), math.cos(fi) * math.sin(th), math.sin(fi)])

    u = np.asarray(chute["u"], float)
    q0, lo, hi = [], [], []
    m_ini = chute["m0"] if m0_livre else chute["mf"]
    mlim = p.m0 if m0_livre else p.mf
    q0.append(min(max(m_ini, mlim[0]), mlim[1]) / p.escala_m); lo.append(mlim[0] / p.escala_m); hi.append(mlim[1] / p.escala_m)
    for vi, lim in ((chute["vinf0"], p.vinf_partida), (chute["vinf1"], p.vinf_chegada)):
        a, th, fi = esf(vi)
        q0 += [min(max(a, lim[0]), lim[1]), th, fi]
        lo += [lim[0], -np.inf, -np.inf]
        hi += [lim[1] + (1e-12 if lim[1] == lim[0] else 0.0), np.inf, np.inf]
    for ui in u:
        a, th, fi = esf(ui)
        q0 += [min(a, 1.0), th, fi]
        lo += [0.0, -np.inf, -np.inf]
        hi += [1.0, np.inf, np.inf]
    q0 = np.clip(np.array(q0), np.array(lo), np.array(hi))

    def z_de(q):
        m = q[0] * p.escala_m
        m0, mf = (m, chute["mf"]) if m0_livre else (chute["m0"], m)
        vi0 = cart(*q[1:4])
        vi1 = cart(*q[4:7])
        uu = np.array([cart(*q[7 + 3 * i:10 + 3 * i]) for i in range(n)])
        return np.r_[t0 / _DIA, tof / _DIA, m0 / p.escala_m, mf / p.escala_m, vi0, vi1, uu.ravel()]

    def jac(q):
        h = 1.4901161193847656e-08 * np.maximum(1.0, np.abs(q))
        qs = [q] + [q + np.eye(len(q))[k] * h[k] for k in range(len(q))]
        res = av.lote(np.vstack([z_de(x) for x in qs]))
        return ((res[1:] - res[0]) / h[:, None]).T

    sol = least_squares(lambda q: av.lote(z_de(q)[None, :])[0], q0, jac=jac, bounds=(lo, hi), method="trf",
                        max_nfev=max_nfev, xtol=1e-15, ftol=1e-15, gtol=1e-15)
    z = z_de(sol.x)
    t0_, tof_, m0, mf, vi0, vi1, uu = av.desfaz(z)
    return {**chute, "m0": m0, "mf": mf, "vinf0": vi0, "vinf1": vi1, "u": uu}, float(np.max(np.abs(sol.fun)))
