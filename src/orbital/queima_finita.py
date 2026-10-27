"""Queima finita em torno de Marte (Etapa 3.1): integração numérica do movimento plano de dois corpos com empuxo
contínuo e massa variável, comparada com o impulso equivalente no periapse (o modelo das Fases 1 e 2).

Modelo:
  - Marte como massa pontual (μ do config); plano da órbita; sem J2, sem atmosfera, sem terceiro corpo.
  - Empuxo constante, sempre tangente à velocidade (contra ela na captura, a favor dela na saída). Não é o
    direcionamento ótimo: a perda calculada é a deste direcionamento.
  - Vazão constante ṁ = T / (Isp · g0); g0 de orbital.foguete.
  - Perda de queima finita = Δv entregue pelo motor (Isp · g0 · ln(m0/mf)) − Δv impulsivo no periapse
    (orbital.manobras.dv_hiperbole_orbita), para a mesma órbita inicial e o mesmo alvo.

Captura: parte da hipérbole de v∞ com periapse no periapse da órbita-alvo; as incógnitas são o início da queima
(relativo à passagem pelo periapse da hipérbole) e a duração, ajustadas para que a órbita final tenha o periapse
e o apoapse do alvo.
Saída: parte da órbita (rp, ra); para cada início da queima, a duração é a que dá a energia de v∞²/2; o início é
o que minimiza o propelente. A direção da assíntota não é imposta (só o módulo de v∞).

Unidades: km, s, kg; empuxo em N.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares, minimize_scalar

from orbital import kepler
from orbital import manobras as mn
from orbital.config import ler, v
from orbital.foguete import G0

_NUM = ler("config/queima_finita.yaml")   # parâmetros numéricos, premissa P-041 (NÃO VALIDADA)
RTOL, ATOL = v(_NUM["integrador"]["rtol"]), v(_NUM["integrador"]["atol_km"])
TOL_ALVO = v(_NUM["tolerancia_alvo"])   # erro relativo máximo no periapse e no apoapse finais da captura


@dataclass(frozen=True)
class Motor:
    """Conjunto de propulsão: empuxo total (N, soma dos motores que queimam juntos) e Isp no vácuo (s)."""
    empuxo_n: float
    isp_s: float

    @property
    def vazao_kg_s(self) -> float:
        return self.empuxo_n / (self.isp_s * G0 * 1e3)   # G0 em km/s² → m/s²


@dataclass(frozen=True)
class Resultado:
    duracao_s: float
    propelente_kg: float
    dv_motor_km_s: float      # Isp · g0 · ln(m0/mf)
    dv_impulsivo_km_s: float
    perda_km_s: float         # dv_motor − dv_impulsivo
    inicio_rel_periapse_s: float
    altitude_minima_km: float  # mínima DURANTE a queima (a órbita final pode descer mais, até o periapse final)
    rp_final_km: float
    ra_final_km: float        # inf se hiperbólica
    vinf_final_km_s: float    # nan se elíptica
    periapse_chegada_alt_km: float = float("nan")   # captura: periapse da hipérbole de chegada escolhido


def _derivadas(mu, motor, sentido):
    a_max = motor.empuxo_n * 1e-3   # N → kg·km/s²
    mdot = motor.vazao_kg_s

    def f(t, s):
        x, y, vx, vy, m = s
        r3 = (x * x + y * y) ** 1.5
        vel = np.hypot(vx, vy)
        a = sentido * a_max / m / vel
        return [vx, vy, -mu * x / r3 + a * vx, -mu * y / r3 + a * vy, -mdot]
    return f


def queimar(mu, motor, r0, v0, m0, duracao_s, sentido, raio_minimo=False):
    """Integra a queima (sentido −1 contra a velocidade, +1 a favor). Devolve (r, v, m, raio mínimo durante a queima);
    o raio mínimo (amostrado em 2000 pontos da solução densa) só é calculado com raio_minimo=True, senão é nan."""
    sol = solve_ivp(_derivadas(mu, motor, sentido), (0.0, duracao_s), [*r0, *v0, m0], method="DOP853",
                    rtol=RTOL, atol=ATOL, dense_output=raio_minimo)
    if not sol.success:
        raise RuntimeError(f"integração falhou: {sol.message}")
    s = sol.y[:, -1]
    rmin = float("nan")
    if raio_minimo:
        xs = sol.sol(np.linspace(0.0, duracao_s, 2000))
        rmin = float(np.min(np.hypot(xs[0], xs[1])))
    return s[0:2], s[2:4], s[4], rmin


def elementos(mu, r, v):
    """(rp, ra, v∞) da órbita osculadora plana; ra = inf e v∞ > 0 se hiperbólica, v∞ = nan se elíptica."""
    rn, vn = np.linalg.norm(r), np.linalg.norm(v)
    energia = vn ** 2 / 2 - mu / rn
    h = r[0] * v[1] - r[1] * v[0]
    p = h * h / mu
    e = np.sqrt(max(0.0, 1 + 2 * energia * h * h / mu ** 2))
    rp = p / (1 + e)
    if energia < 0:
        return rp, p / (1 - e), float("nan")
    return rp, float("inf"), np.sqrt(2 * energia)


def _estado(mu, rp, v_periapse, t_rel):
    """Estado no instante t_rel (s) relativo à passagem pelo periapse, no plano, com o periapse no eixo x."""
    r0, v0 = np.array([rp, 0.0, 0.0]), np.array([0.0, v_periapse, 0.0])
    if t_rel == 0.0:
        return r0[:2], v0[:2]
    r, v = kepler.propagar(mu, r0, v0, t_rel)
    return np.asarray(r)[:2], np.asarray(v)[:2]


def _dv_motor(motor, m0, mf):
    return motor.isp_s * G0 * np.log(m0 / mf)


INVIAVEL = 1e3   # custo (duração/t_imp) atribuído a um início sem solução; muito maior que qualquer solução real
PASSO_CONTINUACAO = v(_NUM["continuacao"]["passo"])               # razão entre empuxos sucessivos (P-041)
DURACAO_INICIAL_S = v(_NUM["continuacao"]["duracao_inicial_s"])  # começo da continuação (P-041)


def _escada(motor, m0, dv):
    """Empuxos da continuação: do maior (queima de até DURACAO_INICIAL_S) ao do motor, em razão PASSO_CONTINUACAO."""
    t_imp = tempo_de_queima_s(motor, m0, dv)
    n = max(0, int(np.ceil(np.log(max(t_imp / DURACAO_INICIAL_S, 1.0)) / np.log(PASSO_CONTINUACAO))))
    return [Motor(motor.empuxo_n * PASSO_CONTINUACAO ** k, motor.isp_s) for k in range(n, -1, -1)]


def _captura_um(mu, raio, motor, m0, vinf, rp_alvo, ra_alvo, chute):
    """Um nível da continuação. `chute` = (início/t_imp, rp_chegada/rp_alvo, duração/t_imp)."""
    dv_imp = float(mn.dv_hiperbole_orbita(mu, vinf, rp_alvo, ra_alvo))
    t_imp = tempo_de_queima_s(motor, m0, dv_imp)

    def final(f_ini, x, raio_minimo=False):
        rp0, dur = rp_alvo * x[0], t_imp * x[1]
        r, v = _estado(mu, rp0, float(mn.v_hiperbole(mu, vinf, rp0)), f_ini * t_imp)
        return (*queimar(mu, motor, r, v, m0, dur, -1, raio_minimo), rp0, dur)

    def ajuste(f_ini, x0):
        def residuo(x):
            rf, vf, *_ = final(f_ini, x)
            rp, ra, _ = elementos(mu, rf, vf)
            if not np.isfinite(ra):
                return [rp / rp_alvo - 1, 1.0 + (1.0 - x[1])]   # ainda hiperbólica: empurra para queima mais longa
            return [rp / rp_alvo - 1, ra / ra_alvo - 1]
        sol = least_squares(residuo, x0=list(x0), bounds=([raio / rp_alvo, 0.5], [20.0, 20.0]),
                            xtol=1e-14, ftol=1e-14, gtol=1e-14)
        if max(abs(np.asarray(sol.fun))) > TOL_ALVO:
            raise RuntimeError(f"captura não convergiu: resíduo {sol.fun}")
        return sol.x

    f0, x0 = chute[0], chute[1:]
    ultimo = [tuple(x0)]   # warm start: parte da última solução bem-sucedida

    def custo(f):
        try:
            x = ajuste(f, ultimo[0])
        except RuntimeError:
            return INVIAVEL   # início sem solução: ponto inviável para o otimizador
        ultimo[0] = tuple(x)
        return x[1]

    opt = minimize_scalar(custo, bounds=(f0 - 0.25, min(f0 + 0.25, 0.0)), method="bounded", options={"xatol": 1e-6})
    f_ini = opt.x
    x = ajuste(f_ini, ultimo[0])
    rf, vf, mf, rmin, rp0, dur = final(f_ini, x, raio_minimo=True)
    rp, ra, _ = elementos(mu, rf, vf)
    dvm = _dv_motor(motor, m0, mf)
    res = Resultado(dur, m0 - mf, dvm, dv_imp, dvm - dv_imp, f_ini * t_imp, rmin - raio, rp - raio, ra - raio,
                    float("nan"), rp0 - raio)
    return res, (f_ini, *x)


def captura(mu, raio, motor, m0, vinf, rp_alvo, ra_alvo):
    """Captura de uma hipérbole de v∞ na órbita (rp_alvo, ra_alvo) com queima contra a velocidade.

    Incógnitas: periapse da hipérbole de chegada (escolhido pela navegação), início da queima (relativo à passagem
    por esse periapse) e duração. Para cada início, periapse de chegada e duração são ajustados para que a órbita final
    tenha o periapse e o apoapse do alvo; o início é o que minimiza o propelente. Com empuxo baixo, a solução é achada
    por continuação: começa num empuxo de queima quase impulsiva e desce até o empuxo do motor."""
    dv_imp = float(mn.dv_hiperbole_orbita(mu, vinf, rp_alvo, ra_alvo))
    chute = (-0.5, 1.0, 1.0)
    for m in _escada(motor, m0, dv_imp):
        res, chute = _captura_um(mu, raio, m, m0, vinf, rp_alvo, ra_alvo, chute)
    return res


def saida(mu, raio, motor, m0, rp, ra, vinf_alvo):
    """Saída da órbita (rp, ra) para a hipérbole de v∞ = vinf_alvo com queima a favor da velocidade; o início da
    queima é o que minimiza o propelente."""
    dv_imp = float(mn.dv_hiperbole_orbita(mu, vinf_alvo, rp, ra))
    t_imp = m0 * (1 - np.exp(-dv_imp / (motor.isp_s * G0))) / motor.vazao_kg_s
    vp = float(mn.v_orbita(mu, rp, rp, ra))
    energia_alvo = vinf_alvo ** 2 / 2

    def energia(dur, r, v):
        rf, vf, _, _ = queimar(mu, motor, r, v, m0, dur, +1)
        return np.dot(vf, vf) / 2 - mu / np.linalg.norm(rf) - energia_alvo

    def duracao(t_ini):
        r, v = _estado(mu, rp, vp, t_ini)
        hi = 1.05 * t_imp
        while energia(hi, r, v) < 0:
            hi *= 1.5
            if hi > 50 * t_imp:
                raise RuntimeError("saída: a queima não atinge a energia de v∞")
        return brentq(lambda d: energia(d, r, v), 0.5 * t_imp, hi, xtol=1e-9, rtol=1e-13), r, v

    opt = minimize_scalar(lambda f: duracao(f * t_imp)[0], bounds=(-1.5, 0.5), method="bounded",
                          options={"xatol": 1e-7})
    t_ini = opt.x * t_imp
    dur, r, v = duracao(t_ini)
    rf, vf, mf, rmin = queimar(mu, motor, r, v, m0, dur, +1, raio_minimo=True)
    rpf, _, vinf_f = elementos(mu, rf, vf)
    dvm = _dv_motor(motor, m0, mf)
    return Resultado(dur, m0 - mf, dvm, dv_imp, dvm - dv_imp, t_ini, rmin - raio, rpf - raio, float("inf"), vinf_f)


def tempo_de_queima_s(motor, m0, dv):
    """Duração para entregar `dv` (km/s) a partir de m0 com o conjunto `motor` (equação do foguete, sem gravidade)."""
    return m0 * (1 - np.exp(-dv / (motor.isp_s * G0))) / motor.vazao_kg_s
