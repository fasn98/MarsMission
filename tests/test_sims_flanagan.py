"""Trajetória heliocêntrica de baixo empuxo (Etapa 2, issue #68, item a): conferências do propagador e da transcrição de
Sims–Flanagan (orbital.sims_flanagan), decididas pelo Fabio no portão de 2026-11-20:
  - empuxo zero contra Kepler (orbital.kepler, [F11]) e contra Lambert (orbital.lambert, [F9]);
  - aceleração tangencial constante contra a listagem de Schwenzfeger [F113], a mesma da Etapa 3.2.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from orbital import baixo_empuxo as be
from orbital import kepler, lambert
from orbital import sims_flanagan as sf
from orbital.config import ler, v
from orbital.constantes import GM_SOL, UA_KM

CFG = ler("config/baixo_empuxo.yaml")
TOL = v(CFG["verificacao_schwenzfeger"]["tolerancia_relativa"])   # 1e-4, precisão relevante do estudo (P-046)
DIA = 86400.0


def _tol_lambert():
    return next(p["valor"] for p in ler("config/premissas.yaml")["premissas"] if p["nome"] == "tolerancia_lambert_vs_kepler_rel")


def _orbitas(n, semente):
    """Estados heliocêntricos elípticos variados (valores de teste, não do estudo)."""
    rng = np.random.default_rng(semente)
    r = rng.normal(size=(n, 3)) * UA_KM
    vc = np.sqrt(GM_SOL / np.linalg.norm(r, axis=1))
    v_ = rng.normal(size=(n, 3)) * 0.4 * vc[:, None] + np.cross([0, 0, 1.0], r) / np.linalg.norm(r, axis=1)[:, None] * vc[:, None]
    return r, v_


@pytest.mark.parametrize("dt", [17.0 * DIA, -230.0 * DIA])
def test_kepler_em_lote_igual_ao_escalar(dt):
    r, v_ = _orbitas(40, 1)
    rl, vl = kepler.propagar_lote(GM_SOL, r, v_, dt)
    for i in range(len(r)):
        re, ve = kepler.propagar(GM_SOL, r[i], v_[i], dt)
        assert np.linalg.norm(rl[i] - re) <= 1e-12 * np.linalg.norm(re)
        assert np.linalg.norm(vl[i] - ve) <= 1e-12 * np.linalg.norm(ve)


def test_newton_converge_com_o_chute_perturbado():
    """Órbita 20 do lote acima (elíptica, dt = −230 d, cerca de 1,5 volta): o chute inicial cai longe da raiz e o Newton sem
    proteção salta de forma caótica, com o número de iterações conforme o arredondamento; numa CPU do CI ele passou de 200
    iterações (main em 86b39e9). Aqui o dt é perturbado em ~1e-15 relativo, o que basta para mudar o caminho do Newton (com
    o kepler.py da main em 86b39e9, cerca de 4 % dos casos escalares e o lote falham). Todos têm de convergir, e o estado
    tem de ficar igual ao do dt sem perturbação dentro de 1e-12 (o efeito da perturbação no estado é ~1e-15)."""
    r, v_ = _orbitas(40, 1)
    dt = -230.0 * DIA * (1.0 + 1e-15 * np.random.default_rng(0).normal(size=5000))
    re, ve = kepler.propagar(GM_SOL, r[20], v_[20], -230.0 * DIA)
    rl, vl = kepler.propagar_lote(GM_SOL, np.repeat(r[20:21], len(dt), 0), np.repeat(v_[20:21], len(dt), 0), dt)
    for i, d in enumerate(dt):
        for rp, vp in (kepler.propagar(GM_SOL, r[20], v_[20], d), (rl[i], vl[i])):
            assert np.linalg.norm(rp - re) <= 1e-12 * np.linalg.norm(re)
            assert np.linalg.norm(vp - ve) <= 1e-12 * np.linalg.norm(ve)


def test_newton_com_tol_zero_para_no_intervalo_esgotado():
    """Com tol = 0, o critério |passo| ≤ tol·max(1, |χ|) só é atingido com passo nulo; o Newton tem de parar quando o
    intervalo que contém a raiz não encolhe mais (extremos vizinhos em ponto flutuante), com o mesmo estado do tol de
    1e-13. Órbitas 19 a 21 do lote acima, com dt positivo e negativo."""
    r, v_ = _orbitas(40, 1)
    for dt in (17.0 * DIA, -230.0 * DIA):
        ref = [kepler.propagar(GM_SOL, r[i], v_[i], dt) for i in (19, 20, 21)]
        rl, vl = kepler.propagar_lote(GM_SOL, r[19:22], v_[19:22], dt, tol=0.0)
        esc = [kepler.propagar(GM_SOL, r[i], v_[i], dt, tol=0.0) for i in (19, 20, 21)]
        for (rp, vp), (rr, vr) in zip([*zip(rl, vl), *esc], [*ref, *ref]):
            assert np.linalg.norm(rp - rr) <= 1e-12 * np.linalg.norm(rr)
            assert np.linalg.norm(vp - vr) <= 1e-12 * np.linalg.norm(vr)


def test_derivada_e_o_raio():
    """df/dχ = r > 0 é o que garante a raiz única e o intervalo: na raiz, a derivada do código é o raio do estado propagado."""
    r, v_ = _orbitas(40, 1)
    for i in (3, 20, 33):
        dt = -230.0 * DIA
        rp, _ = kepler.propagar(GM_SOL, r[i], v_[i], dt)
        r0n = np.linalg.norm(r[i])
        vr0 = r[i] @ v_[i] / r0n
        alpha = 2.0 / r0n - v_[i] @ v_[i] / GM_SOL
        smu = math.sqrt(GM_SOL)
        lo, hi = kepler._intervalo(lambda x: sum(kepler._termos(r0n, vr0, smu, alpha, x, *kepler._cs(alpha * x**2), dt)),
                                   -smu * abs(alpha) * 230.0 * DIA, dt, smu * dt / r0n, 200)
        assert lo < hi <= 0.0
        chi = 0.5 * (lo + hi)
        for _ in range(200):   # bisseção simples dentro do intervalo, independente do Newton do código
            m = 0.5 * (lo + hi)
            if not lo < m < hi:
                break
            fm = sum(kepler._termos(r0n, vr0, smu, alpha, m, *kepler._cs(alpha * m**2), dt))
            lo, hi = (m, hi) if fm < 0 else (lo, m)
            chi = m
        z = alpha * chi**2
        df = kepler._derivada(r0n, vr0, smu, alpha, chi, z, *kepler._cs(z))
        assert df == pytest.approx(np.linalg.norm(rp), rel=1e-9)


def test_residuo_no_intervalo_esgotado():
    """Conferência do resíduo com o intervalo esgotado: aceita resíduo de arredondamento, reprova resíduo grande e NaN."""
    assert kepler._residuo_ok((1.0, 2.0, -3.0 + 1e-15, 0.0))
    assert not kepler._residuo_ok((1.0, 2.0, -3.0 + 1e-9, 0.0))
    assert not kepler._residuo_ok((1.0, float("nan"), -3.0, 0.0))
    assert not kepler._residuo_ok((np.array([1.0, 1.0]), np.array([-1.0, -1.0 + 1e-9]), np.zeros(2), np.zeros(2)))


def test_newton_falha_se_esgota_o_intervalo_com_residuo_grande(monkeypatch):
    """Caso construído (numa órbita real, com o intervalo esgotado, o resíduo é arredondamento): f ganha um degrau de
    1e3·√μ·|dt| com o sinal de f, o que mantém f crescente e com a mesma mudança de sinal, mas sem zero. O intervalo
    encolhe até os extremos vizinhos em volta do degrau e o resíduo fica do tamanho do degrau; os dois propagadores têm de
    levantar o RuntimeError em vez de devolver esse χ. Com tol = 0, porque com o tol de 1e-13 a bisseção pararia pelo tol,
    que não confere o resíduo (como antes da correção)."""
    r, v_ = _orbitas(40, 1)
    termos = kepler._termos

    def com_degrau(r0n, vr0, smu, alpha, chi, c, s, dt):
        t = termos(r0n, vr0, smu, alpha, chi, c, s, dt)
        return (*t[:3], t[3] + 1e3 * smu * np.abs(dt) * np.sign(sum(t)))

    monkeypatch.setattr(kepler, "_termos", com_degrau)
    with pytest.raises(RuntimeError, match="esgotou o intervalo com resíduo acima do limite"):
        kepler.propagar(GM_SOL, r[20], v_[20], -230.0 * DIA, tol=0.0)
    with pytest.raises(RuntimeError, match="esgotou o intervalo com resíduo acima do limite"):
        kepler.propagar_lote(GM_SOL, r[19:22], v_[19:22], -230.0 * DIA, tol=0.0)


def test_propagacao_continua_sem_empuxo_igual_a_kepler():
    r, v_ = _orbitas(5, 2)
    for i in range(len(r)):
        rc, vc, m = sf.propagar_lei(GM_SOL, r[i], v_[i], 400.0 * DIA, lambda t, s: np.zeros(3))
        rk, vk = kepler.propagar(GM_SOL, r[i], v_[i], 400.0 * DIA)
        assert np.linalg.norm(rc - rk) <= TOL * 1e-3 * np.linalg.norm(rk)
        assert np.linalg.norm(vc - vk) <= TOL * 1e-3 * np.linalg.norm(vk)
        assert m == 1.0


def test_transcricao_sem_empuxo_fecha_o_arco_de_lambert():
    """Com u = 0, a transcrição (Kepler para a frente e para trás) liga as pontas de um arco de Lambert sem resíduo, e a
    propagação contínua sem empuxo chega ao alvo de Lambert."""
    tol = _tol_lambert()
    motor = sf.Motor(0.5, 3000.0)
    r, v_ = _orbitas(12, 3)
    rng = np.random.default_rng(4)
    for i in range(0, len(r), 2):
        r1, r2, tof = r[i], r[i + 1], rng.uniform(150.0, 600.0) * DIA
        sol = lambert.resolver(GM_SOL, r1, r2, tof)
        (rf, vf, mf), (rb, vb, mb) = sf.transcricao(GM_SOL, r1, sol.v1, 1000.0, r2, sol.v2, 1000.0, tof, np.zeros((20, 3)), motor)
        assert np.linalg.norm(rf - rb) / np.linalg.norm(rf) < tol
        assert np.linalg.norm(vf - vb) / np.linalg.norm(vf) < tol
        assert mf == mb == 1000.0
        rc, vc, _ = sf.propagar_continuo(GM_SOL, r1, sol.v1, 1000.0, tof, np.zeros((20, 3)), motor)
        assert np.linalg.norm(rc - r2) / np.linalg.norm(r2) < tol
        assert np.linalg.norm(vc - sol.v2) / np.linalg.norm(sol.v2) < tol


def test_aceleracao_tangencial_constante_contra_schwenzfeger():
    """O propagador contínuo em 3D, com a lei tangencial, reproduz os pontos publicados de [F113] p. 31 (os mesmos da
    Etapa 3.2) em r, φ, v = r·v_θ e energia, dentro da tolerância declarada (P-046). Problema adimensional (μ = 1, r0 = 1)."""
    vs = CFG["verificacao_schwenzfeger"]
    eps = v(vs["eps"])

    def tang(t, s):
        return eps * s[3:6] / np.linalg.norm(s[3:6])
    for p in vs["pontos"]:
        r, vv, _ = sf.propagar_lei(1.0, [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], p["t"], tang)
        rn = float(np.linalg.norm(r))
        calc = {"r": rn, "phi": None, "v": float(np.cross(r, vv)[2]), "h": 0.5 * float(vv @ vv) - 1.0 / rn}
        for k in ("r", "v", "h"):
            assert abs(calc[k] - p[k]) <= TOL * abs(p[k]), (p["t"], k)
        # φ acumulado: o ângulo módulo 2π tem de bater com o publicado
        fi = math.atan2(r[1], r[0]) % (2 * math.pi)
        assert abs((fi - p["phi"] + math.pi) % (2 * math.pi) - math.pi) <= TOL * abs(p["phi"]), p["t"]


def test_aceleracao_tangencial_igual_a_da_etapa_3_2():
    """Mesmo problema pelo integrador plano já verificado (orbital.baixo_empuxo): os dois coincidem muito abaixo da
    tolerância."""
    eps, tempos = 0.01, [1.0, 10.0, 40.0]
    plano = be.trajetoria_aceleracao_constante(eps, tempos)
    for t, q in zip(tempos, plano):
        r, vv, _ = sf.propagar_lei(1.0, [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], t, lambda tt, s: eps * s[3:6] / np.linalg.norm(s[3:6]))
        assert abs(float(np.linalg.norm(r)) - q["r"]) <= 1e-8 * q["r"]


def test_impulso_para_tras_desfaz_o_para_frente():
    motor = sf.Motor(0.8, 3500.0)
    r, v_ = _orbitas(2, 5)
    u = np.random.default_rng(6).uniform(-0.5, 0.5, size=(10, 3))
    tof = 300.0 * DIA
    (rf, vf, mf), _ = sf.transcricao(GM_SOL, r[0], v_[0], 2000.0, r[1], v_[1], 1.0, tof, u, motor, n_frente=10)
    _, (rb, vb, mb) = sf.transcricao(GM_SOL, r[1], v_[1], 1.0, rf, vf, mf, tof, u, motor, n_frente=0)
    assert np.linalg.norm(rb - r[0]) <= 1e-9 * np.linalg.norm(r[0])
    assert np.linalg.norm(vb - v_[0]) <= 1e-9 * np.linalg.norm(v_[0])
    assert mb == pytest.approx(2000.0, rel=1e-12)
    # massa gasta exata para empuxo constante e Δv pela equação do foguete
    assert 2000.0 - mf == pytest.approx(np.linalg.norm(u, axis=1).sum() * motor.vazao_kg_s * tof / 10, rel=1e-12)
    assert sf.dv_total(u, tof, 2000.0, motor) == pytest.approx(motor.c_km_s * math.log(2000.0 / mf), rel=1e-12)


@pytest.mark.parametrize("ordem,razao", [(2, 3.0), (4, 12.0)])
def test_transcricao_converge_para_a_propagacao_continua(ordem, razao):
    """Mesmo perfil de empuxo, discretizado em N segmentos: o erro da transcrição contra a propagação contínua cai com N,
    como N⁻² na composição de ordem 2 e como N⁻⁴ na de ordem 4 (razão ≥ 3 e ≥ 12 ao dobrar N). Conferência interna (não
    é verificação)."""
    motor = sf.Motor(0.6, 3500.0)
    r0, v0 = np.array([UA_KM, 0, 0]), np.array([0, math.sqrt(GM_SOL / UA_KM), 0.3])
    tof = 400.0 * DIA
    erros = []
    for n in (10, 20, 40):
        t = (np.arange(n) + 0.5) / n
        u = np.c_[-np.sin(2 * t), np.cos(2 * t), 0.1 * t] * 0.8
        (rf, vf, _), _ = sf.transcricao(GM_SOL, r0, v0, 3000.0, r0, v0, 1.0, tof, u, motor, n_frente=n, ordem=ordem)
        rc, vc, _ = sf.propagar_continuo(GM_SOL, r0, v0, 3000.0, tof, u, motor)
        erros.append(float(np.linalg.norm(rf - rc)))
    assert erros[1] < erros[0] / razao and erros[2] < erros[1] / razao, erros
