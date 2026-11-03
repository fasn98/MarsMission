"""Etapa 7.2: parâmetros do CAD paramétrico (FeatureScript do Onshape) e conferências de arranjo.

- Corpos de cada veículo (orbitador, lander em configuração de lançamento, MAV): primitivos (cilindro, tubo, esfera,
  esfera oca, tronco de cone, tronco de cone oco, caixa) com posição, dimensões e material, calculados aqui a partir de
  results/etapa7.1/envelope.yaml, results/etapa2.5/arquitetura.yaml e config/cad.yaml (escolhas do ADR 0022).
- O FeatureScript de cada veículo (results/etapa7.2/*.fs) é o modelo cad/featurescript/modelo.fs, que não tem nenhuma
  dimensão, mais o bloco de dados gerado aqui. Nenhuma dimensão é digitada no FeatureScript.
- Massa e CG esperados de cada veículo pelos volumes dos primitivos (para conferir o que o Onshape constrói). Peças sem
  geometria própria têm densidade equivalente = massa do orçamento / volume (P-094). Nada é ajustado ao orçamento.
- Conferências do portão da 7.1 (ADR 0022): folga radial no Vulcan com o perfil real da cápsula ([F41] Fig. 2, P-089
  e P-091), sem a altura escalada da P-083; e o MAV deitado contra o estreitamento da casca traseira (P-092).
Saída: results/etapa7.2/parametros.yaml, conferencias.md, orbitador.fs, lander.fs, mav.fs e capsula_mav.png

Uso: python tools/cad_parametros.py
"""

from __future__ import annotations

import math
import sys
import unicodedata
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import yaml  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import envelope_arranjo as ea  # noqa: E402
from orbital import motores as om  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"
MODELO = RAIZ / "cad" / "featurescript" / "modelo.fs"
TINTA, TINTA_2, SUPERFICIE, GRADE = "#0b0b0b", "#52514e", "#fcfcfb", "#eceae4"
# cores de aparência no Onshape (r, g, b em 0–1), por material
CORES = {"ti_6al_4v": (0.62, 0.63, 0.66), "al_2219": (0.78, 0.79, 0.81), "al_7075": (0.74, 0.75, 0.78),
         "cfrp_im7_8552": (0.16, 0.17, 0.19), "pica": (0.35, 0.22, 0.12), "sla_561v": (0.85, 0.80, 0.62),
         "mmh": (0.16, 0.47, 0.84), "mon3": (0.92, 0.41, 0.20), "hidrazina": (0.11, 0.69, 0.48), "equivalente": (0.48, 0.37, 0.65)}


# ------------------------------------------------------------------------------------------------- volumes
def vol_tronco(h, r0, r1):
    return math.pi * h / 3 * (r0 * r0 + r0 * r1 + r1 * r1)


def volume(c):
    """Volume (m³) de um corpo primitivo; as mesmas fórmulas que o FeatureScript constrói."""
    t = c["tipo"]
    if t in ("cilindro", "tubo"):
        h = float(np.linalg.norm(np.subtract(c["p1"], c["p0"])))
        ri = c["r"] - c["t"] if t == "tubo" else 0.0
        return math.pi * (c["r"] ** 2 - ri ** 2) * h
    if t == "esfera":
        return 4 / 3 * math.pi * c["r"] ** 3
    if t == "esfera_oca":
        return 4 / 3 * math.pi * (c["r"] ** 3 - (c["r"] - c["t"]) ** 3)
    if t in ("tronco", "tronco_oco"):
        h = float(np.linalg.norm(np.subtract(c["p1"], c["p0"])))
        v0 = vol_tronco(h, c["r0"], c["r1"])
        return v0 - (vol_tronco(h, c["ri0"], c["ri1"]) if t == "tronco_oco" else 0.0)
    if t == "caixa":
        return abs(float(np.prod(np.subtract(c["c2"], c["c1"]))))
    raise ValueError(t)


FATIAS = 4000   # fatias da integração numérica das inércias dos corpos de revolução (escolha numérica, não premissa)


def inercia(c, rho_c):
    """Tensor de inércia (kg·m²) do corpo homogêneo em torno do próprio centro de massa, nos eixos globais."""
    t = c["tipo"]
    if t in ("esfera", "esfera_oca"):
        ri = c["r"] - c["t"] if t == "esfera_oca" else 0.0
        m = rho_c * volume(c)
        i = 2 / 5 * m * (c["r"] ** 5 - ri ** 5) / (c["r"] ** 3 - ri ** 3)
        return np.eye(3) * i
    if t == "caixa":
        a, b, h = np.abs(np.subtract(c["c2"], c["c1"]))
        m = rho_c * volume(c)
        return np.diag([m * (b * b + h * h) / 12, m * (a * a + h * h) / 12, m * (a * a + b * b) / 12])
    # corpos de revolução: fatias ao longo do eixo (raio externo e interno lineares)
    p0, p1 = np.array(c["p0"], float), np.array(c["p1"], float)
    h = float(np.linalg.norm(p1 - p0))
    u = (p1 - p0) / h
    s = (np.arange(FATIAS) + 0.5) / FATIAS * h
    if t in ("cilindro", "tubo"):
        ro = np.full_like(s, c["r"])
        ri = np.full_like(s, c["r"] - c["t"] if t == "tubo" else 0.0)
    else:
        ro = c["r0"] + (c["r1"] - c["r0"]) * s / h
        ri = (c["ri0"] + (c["ri1"] - c["ri0"]) * s / h) if t == "tronco_oco" else np.zeros_like(s)
    dm = rho_c * math.pi * (ro ** 2 - ri ** 2) * (h / FATIAS)
    sc = float((dm * s).sum() / dm.sum())
    i_ax = float((dm * (ro ** 2 + ri ** 2) / 2).sum())
    i_tr = float((dm * ((ro ** 2 + ri ** 2) / 4 + (s - sc) ** 2)).sum())
    return i_tr * np.eye(3) + (i_ax - i_tr) * np.outer(u, u)


def centro(c):
    """Centro de massa (m) do corpo (homogêneo)."""
    t = c["tipo"]
    if t in ("esfera", "esfera_oca"):
        return np.array(c["c"], float)
    if t == "caixa":
        return (np.array(c["c1"], float) + np.array(c["c2"], float)) / 2
    p0, p1 = np.array(c["p0"], float), np.array(c["p1"], float)
    if t in ("cilindro", "tubo"):
        return (p0 + p1) / 2
    h = float(np.linalg.norm(p1 - p0))

    def zc(r0, r1):   # distância do centroide de um tronco à base (r0)
        s = r0 * r0 + r0 * r1 + r1 * r1
        return h * (r0 * r0 + 2 * r0 * r1 + 3 * r1 * r1) / (4 * s) if s > 0 else h / 2
    vo, zo = vol_tronco(h, c["r0"], c["r1"]), zc(c["r0"], c["r1"])
    if t == "tronco_oco":
        vi, zi = vol_tronco(h, c["ri0"], c["ri1"]), zc(c["ri0"], c["ri1"])
        z = (vo * zo - vi * zi) / (vo - vi)
    else:
        z = zo
    return p0 + (p1 - p0) / h * z


def ascii_(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")


# ------------------------------------------------------------------------------------------------- construtores
def r6(x):
    """Arredonda como o FeatureScript recebe (6 algarismos significativos, _num): massa, CG e inércias do script saem da
    mesma geometria que o Onshape constrói."""
    if isinstance(x, (list, tuple)):
        return [r6(y) for y in x]
    return float(f"{float(x):.6g}")


class Veiculo:
    def __init__(self, nome):
        self.nome, self.corpos = nome, []

    def add(self, nome, mat, origem, **g):
        self.corpos.append({"nome": nome, "material": mat, "origem": origem, **{k: r6(x) for k, x in g.items() if k != "tipo"}, "tipo": g["tipo"]})

    def equivalente(self, nome, massa, origem, **g):
        """Corpo de densidade equivalente: massa do orçamento / volume do primitivo (P-094)."""
        c = {"nome": nome, "material": "equivalente", "origem": origem, **{k: r6(x) for k, x in g.items() if k != "tipo"}, "tipo": g["tipo"]}
        c["densidade"] = r6(massa / volume(c))
        self.corpos.append(c)


def esfera_tanque(veic, nome, c, r_ext, t, mat_tq, m_prop, rho_prop, mat_prop):
    """Tanque esférico oco e o propelente como esfera sólida concêntrica de mesmo volume."""
    veic.add(f"Tanque {nome}", mat_tq, "geometria (P-093)", tipo="esfera_oca", c=list(c), r=r_ext, t=t)
    r_p = (3 * m_prop / rho_prop / (4 * math.pi)) ** (1 / 3)
    veic.add(f"Propelente {nome}", mat_prop, "massa do orçamento / densidade", tipo="esfera", c=list(c), r=r_p)


def casca_tronco(x0, r0, x1, r1, t):
    """Raio interno (deslocamento radial) que dá o volume de uma casca de espessura normal t no tronco (x0,r0)–(x1,r1)."""
    h = abs(x1 - x0)
    alvo = math.pi * (r0 + r1) * math.hypot(h, r1 - r0) * t   # área lateral × espessura
    lo, hi = 0.0, max(r0, r1)   # o raio interno já é limitado a ≥ 0 abaixo
    for _ in range(80):   # bissecção no deslocamento radial
        d = (lo + hi) / 2
        vol = vol_tronco(h, r0, r1) - vol_tronco(h, max(r0 - d, 0.0), max(r1 - d, 0.0))
        lo, hi = (d, hi) if vol < alvo else (lo, d)
    return (lo + hi) / 2


def capsula_raio(perfil, x):
    return float(np.interp(x, perfil[0], perfil[1]))


# ------------------------------------------------------------------------------------------------- principal
def main():
    cad, env = ler("config/cad.yaml"), ler("results/etapa7.1/envelope.yaml")
    arq, mot = ler("results/etapa2.5/arquitetura.yaml"), ler("config/motores.yaml")
    esc, mats, cons, pr = cad["escolha"], cad["materiais"], cad["construcao"], cad["propelentes"]
    rho = {"mmh": v(pr["densidade_mmh_kg_m3"]), "mon3": v(pr["densidade_oxidante_kg_m3"]), "hidrazina": v(pr["densidade_hidrazina_kg_m3"])}
    dens = {k: (rho[k] if k in rho else v(m)) for k, m in mats.items()}
    t_tq = v(cons["tanques"]["espessura_m"])
    f_ent, f_rad = v(cad["tanques"]["folga_entre_conjuntos_m"]), v(cad["tanques"]["folga_radial_m"])
    comp_o = {x["item"]: x for x in arq["orbitador"]["composicao"]}
    comp_l = {x["item"]: x for x in arq["lander"]["composicao"]}
    pega = lambda comp, ini: next(x for k, x in comp.items() if k.startswith(ini))  # noqa: E731
    of = v(pr["razao_mistura_r4d11"])

    # ---------------- orbitador (eixo z a partir do plano do PAF)
    eo = env["orbitador"]
    orb = Veiculo("orbitador")
    rc = eo["raio_cilindro_central_m"]
    z, topo_ret = 0.0, 0.0
    for k, rot in (("insercao_marte", "insercao"), ("retorno", "retorno")):
        t = eo["tanques"][k]
        d = t["diametro_esfera_m"]
        rq = rc + f_rad + d / 2
        zc = z + d / 2
        n = t["pares"]
        for i in range(2 * n):   # em quadrado: oxidante e combustível alternados
            a = 2 * math.pi * i / (2 * n)
            ox = i % 2 == 0
            m = (t["oxidante_kg"] if ox else t["combustivel_kg"]) / n
            esfera_tanque(orb, f"{rot} {'MON-3' if ox else 'MMH'} {i // 2 + 1}", (rq * math.cos(a), rq * math.sin(a), zc), d / 2 + t_tq,
                          t_tq, cons["tanques"]["material"], m, rho["mon3" if ox else "mmh"], "mon3" if ox else "mmh")
        topo_ret = z + d
        z += d + f_ent
    orb.add("Cilindro central", cons["cilindro_central"]["material"], "geometria (P-093)", tipo="tubo",
            p0=[0, 0, 0], p1=[0, 0, topo_ret], r=rc, t=v(cons["cilindro_central"]["espessura_m"]))
    eqv = cons["equivalentes"]
    r_plat = eo["conjuntos"][1]["raio_m"]
    h_plat = v(eqv["plataforma_orbitador_altura_m"])
    z_plat = topo_ret + f_ent
    orb.equivalente("Plataforma (P-016)", pega(comp_o, "Plataforma")["massa_kg"], "massa do orçamento (P-094)",
                    tipo="cilindro", p0=[0, 0, z_plat], p1=[0, 0, z_plat + h_plat], r=r_plat)
    cc = eo["ccrs_m"]
    z_cc = z_plat + h_plat + f_ent
    orb.equivalente("CCRS", pega(comp_o, "Carga útil CU-2: CCRS")["massa_kg"], "massa do orçamento (P-094)",
                    tipo="caixa", c1=[-cc[0] / 2, -cc[1] / 2, z_cc], c2=[cc[0] / 2, cc[1] / 2, z_cc + cc[2]])
    r_ees = eo["ees_diametro_m"] / 2
    ang_ees = math.radians(v(cad["orbitador"]["ees_semiangulo_graus"]))
    h_ees = r_ees / math.tan(ang_ees)
    z_ees = z_cc + cc[2]
    orb.equivalente("EES com o contêiner de amostras", pega(comp_o, "Carga útil CU-2: EEV")["massa_kg"], "massa do orçamento (P-094)",
                    tipo="tronco", p0=[0, 0, z_ees], p1=[0, 0, z_ees + h_ees], r0=r_ees, r1=v(eqv["ees_raio_ponta_m"]), ri0=0.0, ri1=0.0)
    perf_f = (env["coifas"]["falcon"]["altura_m"], env["coifas"]["falcon"]["raio_m"])
    conj_orb = [("Tanques de inserção", 0.0, eo["tanques"]["insercao_marte"]["diametro_esfera_m"], eo["conjuntos"][0]["raio_m"] + t_tq),
                ("Tanques de retorno", eo["conjuntos"][1]["h0_m"], topo_ret, eo["conjuntos"][1]["raio_m"] + t_tq),
                ("Plataforma", z_plat, z_plat + h_plat, r_plat),
                ("CCRS", z_cc, z_cc + cc[2], math.hypot(cc[0] / 2, cc[1] / 2)),
                ("EES", z_ees, z_ees + h_ees, r_ees)]
    folga_orb = [{"conjunto": a, "h0_m": b, "h1_m": c, "raio_m": r, "folga_radial_m": ea.margem_conjunto(perf_f, b, c, r)} for a, b, c, r in conj_orb]

    # ---------------- lander: cápsula real (P-089), frente para cima (P-091), MAV deitado ao longo de y
    capsulas = cad["capsulas"]
    perfis = {k: ([float(x) for x in c["x_m"]], [float(x) for x in c["r_m"]]) for k, c in capsulas.items() if isinstance(c, dict) and "x_m" in c}
    forma = capsulas["forma_da_opcao"][esc["aeroshell"]]
    px, prr = perfis[forma]
    L = px[-1]
    al = cad["arranjo_lander"]
    msl_conj = v(cad["aeroshell"]["msl_conjunto"]["altura_m"])
    h_cz = msl_conj - perfis["msl_m2020"][0][-1]   # P-091
    z_aft = h_cz
    zst = lambda x: z_aft + (L - x)  # noqa: E731   estação (distância ao nariz) → altura acima do PAF
    perf_v = (env["coifas"]["vulcan"]["altura_m"], env["coifas"]["vulcan"]["raio_m"])

    def folga_vulcan(perfil, h_aft):
        """Menor folga radial (m) do perfil da cápsula, com a frente para cima e a base a h_aft do PAF, contra o Vulcan."""
        xs = np.linspace(0, perfil[0][-1], 400)
        Lc = perfil[0][-1]
        return min(ea.raio_envelope(perf_v, h_aft + (Lc - x)) - capsula_raio(perfil, x) for x in xs)
    fol_v = {k: {"folga_radial_m": folga_vulcan(p, h_cz), "raio_max_m": max(p[1]), "comprimento_m": p[0][-1]} for k, p in perfis.items()}
    # sensibilidade: envelope sem o afunilamento linear entre as cotas (o diâmetro menor, da estação de cima, desde o PAF)
    perf_v_ref = perf_v
    perf_v = ([perf_v_ref[0][0], perf_v_ref[0][1]] + list(perf_v_ref[0][2:]), [perf_v_ref[1][1], perf_v_ref[1][1]] + list(perf_v_ref[1][2:]))
    for k, p in perfis.items():
        fol_v[k]["folga_sem_afunilamento_m"] = folga_vulcan(p, h_cz)
    perf_v = perf_v_ref

    lan = Veiculo("lander")
    t_pica = v(capsulas["espessura_pica_m"])
    t_sla = v(capsulas["espessura_casca_traseira_m"])
    rmin = v(cons["raio_minimo_m"])
    i_ombro = int(np.argmax(prr))
    segs = list(zip(px[:-1], prr[:-1], px[1:], prr[1:]))
    for i, (x0, r0, x1, r1) in enumerate(segs):
        if x1 == x0:
            continue
        frente = i < i_ombro
        if i == 0:   # ponta do nariz rombudo: tronco maciço de PICA
            lan.add("Nariz do escudo (PICA)", "pica", "geometria: perfil de [F41]", tipo="tronco",
                    p0=[0, 0, zst(x0)], p1=[0, 0, zst(x1)], r0=max(r0, rmin), r1=r1, ri0=0.0, ri1=0.0)
            continue
        t = t_pica if frente else t_sla
        d = casca_tronco(x0, r0, x1, r1, t)
        lan.add("Escudo térmico (PICA)" if frente else f"Casca traseira {i - i_ombro + 1} (SLA-561V)", "pica" if frente else "sla_561v",
                "geometria: perfil de [F41], espessura de [F215]/[F225]", tipo="tronco_oco",
                p0=[0, 0, zst(x0)], p1=[0, 0, zst(x1)], r0=r0, r1=r1, ri0=max(r0 - d, rmin), ri1=max(r1 - d, rmin))
    lan.add("Tampa traseira (SLA-561V)", "sla_561v", "geometria (P-090)", tipo="cilindro", p0=[0, 0, z_aft], p1=[0, 0, z_aft + t_sla], r=prr[-2])
    # estágio de cruzeiro: dois tanques ao lado da casca traseira e o circuito de fluido como disco equivalente
    lc = env["lander"]["cruzeiro"]
    d_cz = lc["diametro_esfera_m"]
    r_tcz = v(al["raio_tanques_cruzeiro_m"])
    for i, (nome, mk, mat) in enumerate((("cruzeiro MON-3", "oxidante_kg", "mon3"), ("cruzeiro MMH", "combustivel_kg", "mmh"))):
        esfera_tanque(lan, nome, (r_tcz * (1 if i == 0 else -1), 0, z_aft + d_cz / 2), d_cz / 2 + t_tq, t_tq, cons["tanques"]["material"],
                      lc[mk], rho[mat], mat)
    lan.equivalente("Circuito de fluido de cruzeiro (P-077)", pega(comp_l, "Circuito de fluido")["massa_kg"], "massa do orçamento (P-094)",
                    tipo="cilindro", p0=[0, 0, 0], p1=[0, 0, h_cz], r=max(prr) - v(cad["aeroshell"]["folga_interna_m"]))
    # descida: três esferas de hidrazina a 120° (P-084, P-095)
    de = env["lander"]["descida"]
    d_de = de["diametro_esfera_m"]
    r_de = v(al["raio_tanques_descida_m"])
    x_ombro = px[i_ombro]
    x_mav0 = v(cad["mav_no_aeroshell"]["estacao_base_referencia_m"])
    for i, a in enumerate(float(x) for x in al["angulos_tanques_descida_graus"]["valor"]):
        a = math.radians(a)
        esfera_tanque(lan, f"descida {i + 1}", (r_de * math.cos(a), r_de * math.sin(a), zst(x_ombro)), d_de / 2 + t_tq, t_tq,
                      cons["tanques"]["material"], de["propelente_kg"] / de["tanques"], rho["hidrazina"], "hidrazina")
    # núcleo do lander (deck) abaixo do MAV, com a massa da plataforma menos braço e helicópteros (separados)
    h_deck = v(eqv["deck_lander_altura_m"])
    fi = v(cad["aeroshell"]["folga_interna_m"])
    r_deck = capsula_raio((px, prr), x_mav0 - h_deck) - fi
    braco = pega(comp_l, "Braço")["massa_kg"]
    heli = pega(comp_l, "Helicópteros")["massa_kg"]
    plat = v(ler("config/superficie.yaml")["lander"]["plataforma_superficie_kg"])   # P-017
    lan.equivalente("Nucleo do lander (P-017 sem braço e helicópteros)", plat - braco - heli, "massa do orçamento (P-094)",
                    tipo="cilindro", p0=[0, 0, zst(x_mav0 - h_deck)], p1=[0, 0, zst(x_mav0)], r=r_deck)
    # MAV deitado ao longo de y, com a base na estação x_mav0 (P-092)
    mv_esc = env["mav"][esc["mav_diametro"]]
    d_mav = mv_esc["diametro_m"]
    z_mav = zst(x_mav0 + d_mav / 2)
    mav_l = monta_mav(Veiculo("mav_no_lander"), mv_esc, env, arq, mot, cad, dens, rho, of, t_tq, eixo="y", origem=(0, -mv_esc["comprimento_m"] / 2, z_mav))
    lan.corpos += mav_l.corpos
    # braço guardado paralelo ao MAV e helicópteros acima dele
    bx, br_ = v(al["braco_posicao_x_m"]), v(al["braco_raio_m"])
    Lb = env["lander"]["braco_m"]
    zb = zst(x_mav0 + br_)
    lan.equivalente("Braço de coleta (guardado)", braco, "massa do orçamento (P-094)", tipo="cilindro",
                    p0=[bx, -Lb / 2, zb], p1=[bx, Lb / 2, zb], r=br_)
    hel = env["lander"]["helicoptero"]
    hy = v(al["helicopteros_posicao_y_m"])
    x_hel = x_mav0 + d_mav + v(al["folga_entre_pecas_m"])
    for s in (-1, 1):
        lan.equivalente(f"Helicóptero {'1' if s < 0 else '2'}", heli / 2, "massa do orçamento (P-094)", tipo="cilindro",
                        p0=[0, s * hy, zst(x_hel)], p1=[0, s * hy, zst(x_hel + hel["altura_m"])], r=hel["diametro_rotor_m"] / 2)

    # MAV deitado contra a casca traseira (estações da base varridas, P-092)
    est = [float(x) for x in cad["mav_no_aeroshell"]["estacao_base_m"]]
    cabe = {}
    for k, p in perfis.items():
        linhas = []
        for x0 in est:
            r_in = capsula_raio(p, x0 + d_mav) - fi
            linhas.append({"estacao_base_m": x0, "comprimento_max_m": 2 * r_in, "folga_m": r_in - mv_esc["comprimento_m"] / 2})
        cabe[k] = linhas

    # ---------------- MAV em pé (para o CAD isolado)
    mav = monta_mav(Veiculo("mav"), mv_esc, env, arq, mot, cad, dens, rho, of, t_tq, eixo="z", origem=(0, 0, 0))

    veics = {"orbitador": orb, "lander": lan, "mav": mav}
    resumo = {}
    for k, ve_ in veics.items():
        massa, mom = 0.0, np.zeros(3)
        por_origem = {}
        for c in ve_.corpos:
            rho_c = c["densidade"] if c["material"] == "equivalente" else dens[c["material"]]
            m = rho_c * volume(c)
            c["massa_kg"] = m
            massa += m
            mom += m * centro(c)
            chave = "densidade equivalente (massa do orçamento)" if c["material"] == "equivalente" else (
                "propelente" if c["material"] in rho else "geometria modelada")
            por_origem[chave] = por_origem.get(chave, 0.0) + m
        cg = mom / massa
        tensor, vol = np.zeros((3, 3)), 0.0
        for c in ve_.corpos:   # teorema dos eixos paralelos até o CG do veículo
            rho_c = c["densidade"] if c["material"] == "equivalente" else dens[c["material"]]
            d = centro(c) - cg
            tensor += inercia(c, rho_c) + c["massa_kg"] * (np.dot(d, d) * np.eye(3) - np.outer(d, d))
            vol += volume(c)
        resumo[k] = {"massa_kg": massa, "cg_m": cg.tolist(), "inercia_cg_kg_m2": tensor.tolist(), "volume_m3": vol,
                     "por_origem_kg": por_origem, "corpos": len(ve_.corpos)}
    resumo["orcamento"] = {"orbitador_injetado_kg": arq["orbitador"]["injetado_kg"], "lander_injetado_kg": arq["lander"]["injetado_kg"],
                           "mav_glom_kg": arq["lander"]["mav"]["estagios"][0]["massa_inicial_kg"]}

    out = {"gerado_por": "tools/cad_parametros.py", "escolha": esc, "materiais": {k: {"nome": mats[k]["nome"], "densidade_kg_m3": dens[k]} for k in mats},
           "conferencias": {"orbitador_falcon": folga_orb,
                            "lander_vulcan": {"forma": forma, "altura_estagio_cruzeiro_m": h_cz, "por_forma": fol_v},
                            "mav_deitado": {"diametro_m": d_mav, "comprimento_m": mv_esc["comprimento_m"], "folga_interna_m": fi, "por_forma": cabe}},
           "resumo": resumo, "veiculos": {k: ve_.corpos for k, ve_ in veics.items()}}
    out = nativo(out)
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "parametros.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    for k, ve_ in veics.items():
        (SAIDA / f"{k}.fs").write_text(featurescript(k, out["veiculos"][k], out["materiais"]), encoding="utf-8")
    escreve_md(out)
    figura(out, perfis, perf_v)


def monta_mav(veic, mv_esc, env, arq, mot, cad, dens, rho, of, t_tq, eixo, origem):
    """Segmentos do MAV (results/etapa7.1) ao longo do eixo dado, a partir da origem: tanques ocos com propelente,
    motores e carga com densidade equivalente (massas de [F106] e do orçamento), interestágio em tubo."""
    d = mv_esc["diametro_m"]
    e = np.array({"z": (0, 0, 1), "y": (0, 1, 0)}[eixo], float)
    o = np.array(origem, float)
    t_env = v(cad["mav"]["espessura_parede_m"])
    r_t = d / 2 - t_env
    est = arq["lander"]["mav"]["estagios"]
    m_r4d = om.catalogo(mot)["R-4D-11"]["massa_kg"]   # [F106], lb → kg pelo NIST (config/motores.yaml)
    carga = v(ler("config/superficie.yaml")["mav"]["carga_util_kg"])
    s = 0.0
    for seg in mv_esc["segmentos"]:
        Ls = seg["comprimento_m"]
        p0, p1 = o + e * s, o + e * (s + Ls)
        nome = seg["item"]
        if seg["tipo"] in ("oxidante", "combustivel"):
            i = 0 if "estágio 1" in nome else 1
            ox = seg["tipo"] == "oxidante"
            m_p = est[i]["propelente_kg"] * (of / (1 + of) if ox else 1 / (1 + of))
            veic.add(f"MAV {nome}", cad["construcao"]["tanques"]["material"], "geometria (P-085, P-093)", tipo="tubo",
                     p0=p0.tolist(), p1=p1.tolist(), r=r_t, t=t_tq)
            ri = r_t - t_tq
            lp = m_p / rho["mon3" if ox else "mmh"] / (math.pi * ri * ri)
            pm = (p0 + p1) / 2
            veic.add(f"MAV propelente {nome[len('Tanque de '):]}", "mon3" if ox else "mmh", "massa do orçamento / densidade", tipo="cilindro",
                     p0=(pm - e * lp / 2).tolist(), p1=(pm + e * lp / 2).tolist(), r=ri)
        elif nome.startswith("Motores do estágio 1"):
            veic.equivalente("MAV motores do estágio 1 (4 x R-4D-11)", 4 * m_r4d, "massa de [F106] (P-094)", tipo="cilindro",
                             p0=p0.tolist(), p1=p1.tolist(), r=r_t)
        elif nome.startswith("Motor do estágio 2"):
            veic.equivalente("MAV motor do estágio 2 (1 x R-4D-11)", m_r4d, "massa de [F106] (P-094)", tipo="cilindro",
                             p0=p0.tolist(), p1=p1.tolist(), r=r_t / 2)
        elif nome.startswith("Interestágio"):
            veic.add("MAV interestágio", cad["construcao"]["cilindro_central"]["material"], "geometria (P-093)", tipo="tubo",
                     p0=p0.tolist(), p1=p1.tolist(), r=d / 2, t=v(cad["construcao"]["cilindro_central"]["espessura_m"]))
        else:
            veic.equivalente("MAV carga (contêiner de amostras)", carga, "massa de [F34] (P-094)", tipo="cilindro",
                             p0=p0.tolist(), p1=p1.tolist(), r=r_t)
        s += Ls
    return veic


# ------------------------------------------------------------------------------------------------- FeatureScript
def _num(x):
    return f"{float(x):.6g}"


def _vec(p):
    return "[" + ", ".join(_num(x) for x in p) + "]"


def extensao_interna(c):
    """Cone interno de um tronco oco estendido além das duas faces (pela espessura da parede), com os raios na mesma reta:
    a subtração não tem faces coplanares e o volume removido dentro do tronco externo é o mesmo."""
    p0, p1 = np.array(c["p0"], float), np.array(c["p1"], float)
    h = float(np.linalg.norm(p1 - p0))
    u = (p1 - p0) / h
    e = max(c["r0"] - c["ri0"], c["r1"] - c["ri1"])
    k = (c["ri1"] - c["ri0"]) / h
    # no lado em que o raio diminui, o prolongamento para antes de o raio chegar a zero: o cone fica na mesma reta.
    # O fator 0,5 é escolha de construção, não premissa: qualquer valor entre 0 e 1 dá o mesmo volume removido dentro do
    # tronco externo (o prolongamento fica fora dele), e portanto a mesma massa, o mesmo CG e a mesma geometria.
    e0 = min(e, 0.5 * c["ri0"] / k) if k > 0 else e
    e1 = min(e, 0.5 * c["ri1"] / -k) if k < 0 else e
    return {"pe0": (p0 - u * e0).tolist(), "pe1": (p1 + u * e1).tolist(), "rie0": c["ri0"] - k * e0, "rie1": c["ri1"] + k * e1}


def featurescript(nome, corpos, materiais):
    """Modelo cad/featurescript/modelo.fs + bloco de dados deste veículo."""
    chaves = list(materiais) + ["equivalente"]
    linhas = ["const MATERIAIS = ["]
    for k in chaves:
        if k == "equivalente":
            continue
        linhas.append(f'    ["{ascii_(materiais[k]["nome"])}", {_num(materiais[k]["densidade_kg_m3"])}]')
    linhas = [linhas[0], ",\n".join(linhas[1:]), "];"]
    corpos_txt = []
    for c in corpos:
        if c["material"] == "equivalente":
            mat = f'"mat" : -1, "densidade" : {_num(c["densidade"])}'
        else:
            mat = f'"mat" : {list(materiais).index(c["material"])}, "densidade" : 0'
        cor = CORES.get(c["material"], CORES["equivalente"])
        g = {k: c[k] for k in ("p0", "p1", "c", "c1", "c2", "r", "t", "r0", "r1", "ri0", "ri1") if k in c}
        if c["tipo"] == "tronco_oco":
            g.update(extensao_interna(c))
        campos = ", ".join(f'"{k}" : ' + (_vec(x) if isinstance(x, list) else _num(x)) for k, x in g.items())
        corpos_txt.append(f'    {{ "tipo" : "{c["tipo"]}", "nome" : "{ascii_(c["nome"])}", {mat}, "cor" : {_vec(cor)}, {campos} }}')
    linhas += ["const CORPOS = [", ",\n".join(corpos_txt), "];"]
    texto = MODELO.read_text(encoding="utf-8")
    return (texto.replace("__FEATURE__", f"marsMission{nome.capitalize()}")
            .replace("__TITULO__", f"MarsMission {ascii_(nome)}")
            .replace("// __DADOS__", "\n".join(linhas)))


# ------------------------------------------------------------------------------------------------- relatório
def escreve_md(o):
    br = lambda x, n=2: f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    cf, rs = o["conferencias"], o["resumo"]
    nomes = {"msl_m2020": "MSL/M2020 (Ø 4,5 m)", "srl_a": "SRL-A", "srl_c": "SRL-C"}
    md = ["# Etapa 7.2: parâmetros do CAD e conferências (gerado por tools/cad_parametros.py)", "",
          f"Escolhas (ADR 0022): aeroshell {o['escolha']['aeroshell']}, MAV {o['escolha']['mav_diametro']}, {o['escolha']['orbitador_pares']} pares de tanques por estágio.", "",
          "## Lander no Vulcan com o perfil real da cápsula (sem a P-083)", "",
          f"Perfis lidos de [F41] Fig. 2 (P-089); frente para cima e estágio de cruzeiro de {br(cf['lander_vulcan']['altura_estagio_cruzeiro_m'])} m "
          "além da cápsula (P-091).", "",
          "| Forma | Raio máximo | Comprimento | Menor folga radial ao envelope do Vulcan | Sem o afunilamento linear entre as cotas |", "| :- | -: | -: | -: | -: |"]
    for k, x in cf["lander_vulcan"]["por_forma"].items():
        md.append(f"| {nomes.get(k, k)} | {br(x['raio_max_m'])} | {br(x['comprimento_m'])} | {br(x['folga_radial_m'], 3)} | {br(x['folga_sem_afunilamento_m'], 3)} |")
    md += ["", "Envelope do Vulcan: [F80] Fig. 4.3.1-1 (\"Simplified\"), cotas de diâmetro nas estações; entre elas o contorno desenhado é reto, "
           "e a interpolação é linear. A última coluna supõe o diâmetro menor (o da estação de cima) desde o plano do PAF."]
    mv = cf["mav_deitado"]
    md += ["", f"Forma usada no CAD: {nomes.get(cf['lander_vulcan']['forma'])}.", "",
           f"## MAV deitado contra a casca traseira (Ø {br(mv['diametro_m'])} m, {br(mv['comprimento_m'])} m; folga interna de "
           f"{br(mv['folga_interna_m'])} m, P-087)", "",
           "Comprimento máximo do MAV deitado com a base na estação dada (distância ao nariz), pelo raio interno no topo do MAV.", "",
           "| Estação da base | " + " | ".join(nomes.get(k, k) for k in mv["por_forma"]) + " |", "| -: |" + " -: |" * len(mv["por_forma"])]
    for i, x0 in enumerate(next(iter(mv["por_forma"].values()))):
        md.append(f"| {br(x0['estacao_base_m'])} | " + " | ".join(
            f"{br(p[i]['comprimento_max_m'])} ({'cabe' if p[i]['folga_m'] >= 0 else 'não cabe'})" for p in mv["por_forma"].values()) + " |")
    md += ["", "## Orbitador no Falcon (com a plataforma e o EES no arranjo do CAD)", "",
           "| Conjunto | Base | Topo | Raio | Folga radial |", "| :- | -: | -: | -: | -: |"]
    for c in cf["orbitador_falcon"]:
        md.append(f"| {c['conjunto']} | {br(c['h0_m'])} | {br(c['h1_m'])} | {br(c['raio_m'])} | {br(c['folga_radial_m'])} |")
    md += ["", "## Massa e CG esperados do CAD (pelos volumes dos primitivos; para conferir o Onshape)", "",
           "| Veículo | Corpos | Massa do CAD | Geometria modelada | Propelente | Densidade equivalente (orçamento) | CG (x, y, z) |",
           "| :- | -: | -: | -: | -: | -: | :- |"]
    for k in ("orbitador", "lander", "mav"):
        r = rs[k]
        po = r["por_origem_kg"]
        md.append(f"| {k} | {r['corpos']} | {br(r['massa_kg'], 1)} | {br(po.get('geometria modelada', 0), 1)} | "
                  f"{br(po.get('propelente', 0), 1)} | {br(po.get('densidade equivalente (massa do orçamento)', 0), 1)} | "
                  + ", ".join(br(x, 3) for x in r["cg_m"]) + " |")
    md += ["", "Geometria modelada: tanques, cilindro central, escudo térmico (PICA [F223]) e casca traseira (SLA-561V, densidade da P-090), "
           "com espessuras das fontes [F215, F225] ou da P-093."]
    oc = rs["orcamento"]
    md += ["", f"Orçamento (results/etapa2.5/arquitetura.yaml): orbitador {br(oc['orbitador_injetado_kg'], 0)} kg, lander {br(oc['lander_injetado_kg'], 0)} kg, "
           f"MAV {br(oc['mav_glom_kg'], 1)} kg. A diferença (estrutura, motores e peças sem geometria nesta etapa) é assunto da Etapa 7.3; "
           "nada é ajustado.", "",
           "Arquivos para o Onshape: orbitador.fs, lander.fs e mav.fs (instruções em docs/etapa7.2_featurescript.md)."]
    (SAIDA / "conferencias.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


def figura(o, perfis, perf_v):
    """Perfis das cápsulas e o MAV deitado na estação de referência (meia seção)."""
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    ax.set_aspect("equal")
    ax.grid(color=GRADE, lw=0.6)
    cores = {"msl_m2020": "#2a78d6", "srl_a": "#eb6834", "srl_c": "#1baf7a"}
    for k, (xs, rs) in perfis.items():
        ax.plot(xs, rs, color=cores.get(k, TINTA), lw=1.2, label=k.replace("_", " ").upper())
    mv = o["conferencias"]["mav_deitado"]
    x0 = next(iter(mv["por_forma"].values()))[0]["estacao_base_m"]
    ax.add_patch(plt.Rectangle((x0, 0), mv["diametro_m"], mv["comprimento_m"] / 2, fc="#7b5ea7", ec=TINTA, alpha=0.5, label="MAV deitado (meio comprimento)"))
    ax.set_xlabel("distância ao nariz (m)")
    ax.set_ylabel("raio (m)")
    ax.set_title("Cápsulas ([F41] Fig. 2) e o MAV deitado (esquema)", fontsize=10)
    ax.legend(fontsize=7, frameon=False, loc="upper right")
    fig.savefig(SAIDA / "capsula_mav.png", dpi=120, facecolor=SUPERFICIE)
    plt.close(fig)


if __name__ == "__main__":
    main()
