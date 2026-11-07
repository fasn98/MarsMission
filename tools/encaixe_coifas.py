"""Etapa 7.2b: VERIFICAÇÃO geométrica do modelo nas coifas (não é validação).

- Envelopes de carga útil como FeatureScript (cad/featurescript/envelope.fs, sem dimensões, mais o bloco gerado aqui):
  Vulcan, com as duas leituras da Fig. 4.3.1-1 de [F80] como opção da feature, e Falcon, do perfil lido do STEP de [F82].
- Novas versões dos veículos com um mate connector no plano da interface: os corpos são os de results/etapa7.2 (massa e CG
  não mudam). O lander de 4,5 m é um modelo novo, com a cápsula MSL/M2020 (P-089) e o resto do arranjo igual.
- Folgas mínimas radial e axial entre os corpos e o envelope, onde ocorrem, e a comparação com results/etapa7.2.
- Roteiro numerado para conferir tudo numa Assembly do Onshape.
Saída: results/etapa7.2b/ (envelope_vulcan.fs, envelope_falcon_heavy.fs, orbitador.fs, lander_4_65.fs, lander_4_5.fs,
folgas.yaml, folgas.md, roteiro_onshape.md)

Uso: python tools/encaixe_coifas.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import cad_parametros as cp  # noqa: E402
import envelope_arranjo as ea  # noqa: E402
from conferencia_onshape import _bloco  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2b"
MODELO = RAIZ / "cad" / "featurescript" / "envelope.fs"
# amostragem da superfície dos corpos (escolha numérica, não premissa): os vértices dos perfis entram exatos
N_EIXO, N_ANGULO = 401, 721   # 721 pontos = 720 intervalos de 0,5°: a grade passa por 90° e 180°
_ENC = ler("config/cad.yaml")["encaixe"]
# parâmetros numéricos de implementação; valor e justificativa em config/cad.yaml
EMPATE_M, CASAS_DE_ORDEM = v(_ENC["empate_m"]), int(v(_ENC["casas_de_ordem"]))


# ------------------------------------------------------------------------------------------------- envelopes
def segmentos(alturas, raios, t):
    """Pilhas interna e externa da casca: a face interna é o envelope; a interna passa do plano da interface, para não
    haver faces coplanares, e a externa fecha o topo."""
    z, r = cp.r13(list(alturas)), cp.r13(list(raios))
    interno = [[z[i], z[i + 1], r[i], r[i + 1]] for i in range(len(z) - 1)]
    externo = [[a, b, cp.r13(c + t), cp.r13(d + t)] for a, b, c, d in interno]
    externo.append([z[-1], cp.r13(z[-1] + t), cp.r13(r[-1] + t), cp.r13(r[-1] + t)])
    return {"interno": [[-t, z[0], r[0], r[0]]] + interno, "externo": externo}


def envelope_fs(arq, titulo, feature, origem, nome, cor, opcoes, versao):
    """Modelo + bloco de dados do envelope. Os segmentos ficam em JSON, para a ferramenta ler de volta o que foi escrito."""
    enum = ["export enum LeituraEnvelope", "{", ",\n".join(f'    annotation {{ "Name" : "{cp.ascii_(o["rotulo"])}" }}\n    L{i}' for i, o in enumerate(opcoes)), "}"]
    fmt = lambda s: "[" + ", ".join("[" + ", ".join(cp._num(x) for x in q) + "]" for q in s) + "]"  # noqa: E731
    dados = enum + ["const OPCOES = [" + ", ".join(f"LeituraEnvelope.L{i}" for i in range(len(opcoes))) + "];",
                    "const SEGMENTOS = [", ",\n".join(f'    {{ "interno" : {fmt(o["segmentos"]["interno"])}, "externo" : {fmt(o["segmentos"]["externo"])} }}' for o in opcoes), "];",
                    f'const NOME = "{cp.ascii_(nome)}";', "const COR = " + cp._vec(cor) + ";", "const Z_INTERFACE = 0;"]
    texto = (MODELO.read_text(encoding="utf-8").replace("__VERSAO__", str(versao)).replace("__TITULO__", titulo).replace("__FEATURE__", feature)
             .replace("// __ORIGEM__", "// " + origem).replace("// __DADOS__", "\n".join(dados)))
    (SAIDA / arq).write_text(texto, encoding="utf-8")


def perfil_lido(arq, i):
    """Perfil (alturas, raios) da opção i, lido de volta do arquivo .fs escrito."""
    seg = _bloco((SAIDA / arq).read_text(encoding="utf-8"), "SEGMENTOS")[i]["interno"][1:]
    return [s[0] for s in seg] + [seg[-1][1]], [s[2] for s in seg] + [seg[-1][3]]


# ------------------------------------------------------------------------------------------------- veículos
def veiculo_fs(nome, corpos, materiais, dono, versao):
    """Mesmos corpos da Etapa 7.2, mais o mate connector no plano da interface e a versão do FeatureScript."""
    t = cp.featurescript(nome, corpos, materiais)
    cab, resto = t.split("\n", 2)[:2], t.split("\n", 2)[2]
    t = "\n".join(x.replace("2737", str(versao)) for x in cab) + "\n" + resto
    marca = "// MarsMission - CAD parametrico (Fase 7, Etapa 7.2). ARQUIVO GERADO por tools/cad_parametros.py"
    assert t.count(marca) == 1
    t = t.replace(marca, "// VERIFICACAO geometrica do modelo (Etapa 7.2b), nao validacao: novos dados e conector por tools/encaixe_coifas.py.\n" + marca)
    marca = "    });\n\nfunction vec"
    assert t.count(marca) == 1
    conector = ('        // Etapa 7.2b: mate connector no plano da interface (z = 0 do modelo), preso ao corpo DONO_INTERFACE.\n'
                '        opMateConnector(context, id + "interface", {\n'
                '                    "coordSystem" : coordSystem(vector(0, 0, 0) * meter, vector(1, 0, 0), vector(0, 0, 1)),\n'
                '                    "owner" : qCreatedBy(id + ("c" ~ toString(DONO_INTERFACE)) + "a", EntityType.BODY) });\n')
    t = t.replace(marca, conector + marca)
    marca = 'annotation { "Feature Type Name"'
    assert t.count(marca) == 1
    t = t.replace(marca, f"const DONO_INTERFACE = {dono};\n\n" + marca)
    (SAIDA / f"{nome}.fs").write_text(t, encoding="utf-8")


def massa_cg(corpos, dens):
    m, mom = 0.0, np.zeros(3)
    for c in corpos:
        mc = (c["densidade"] if c["material"] == "equivalente" else dens[c["material"]]) * cp.volume(c)
        m += mc
        mom += mc * cp.centro(c)
    return m, (mom / m).tolist()


def pontos(c, alinhar=True):
    """Pontos da superfície externa de um corpo (m). A grade angular parte da direção radial do corpo (decisão do Fabio,
    2026-11-06): peças simétricas têm a mesma amostragem, e a diferença entre elas não sai da grade. `alinhar=False`
    repete a grade antiga, só para a comparação de results/etapa7.2b/folgas.md."""
    t = c["tipo"]
    if t in ("esfera", "esfera_oca"):
        C = np.array(c["c"], float)
        a = np.linspace(0, 2 * np.pi, N_ANGULO) + (np.arctan2(C[1], C[0]) if alinhar else 0.0)
        b = np.linspace(-np.pi / 2, np.pi / 2, N_EIXO)
        A, B = np.meshgrid(a, b)
        return C + c["r"] * np.stack([np.cos(B) * np.cos(A), np.cos(B) * np.sin(A), np.sin(B)], axis=-1).reshape(-1, 3)
    if t == "caixa":
        c1, c2 = np.array(c["c1"], float), np.array(c["c2"], float)
        zs = np.linspace(c1[2], c2[2], N_EIXO)
        return np.array([[x, y, z] for x in (c1[0], c2[0]) for y in (c1[1], c2[1]) for z in zs])
    p0, p1 = np.array(c["p0"], float), np.array(c["p1"], float)
    r0, r1 = (c["r"], c["r"]) if t in ("cilindro", "tubo") else (c["r0"], c["r1"])
    u = (p1 - p0) / np.linalg.norm(p1 - p0)
    meio = np.array([(p0 + p1)[0] / 2, (p0 + p1)[1] / 2, 0.0])
    radial = meio - u * np.dot(meio, u)
    if alinhar and np.linalg.norm(radial) > 1e-12:
        e1 = radial / np.linalg.norm(radial)
    else:
        e1 = np.cross(u, [1.0, 0.0, 0.0] if abs(u[0]) < 0.9 else [0.0, 1.0, 0.0])
        e1 /= np.linalg.norm(e1)
    e2 = np.cross(u, e1)
    s = np.linspace(0, 1, N_EIXO)[:, None, None]
    a = np.linspace(0, 2 * np.pi, N_ANGULO)[None, :, None]
    r = (r0 + (r1 - r0) * s)
    return (p0 + (p1 - p0) * s + r * (np.cos(a) * e1 + np.sin(a) * e2)).reshape(-1, 3)


def distancia_ao_perfil(rp, zp, perfil):
    """Menor distância (m) do ponto (r, z) à linha do envelope, no plano meridiano: é o que a ferramenta Measure mostra."""
    zs, rs = np.array(perfil[0]), np.array(perfil[1])
    d = np.inf
    for i in range(len(zs) - 1):
        a, b = np.array([rs[i], zs[i]]), np.array([rs[i + 1], zs[i + 1]])
        t = np.clip(np.dot([rp, zp] - a, b - a) / np.dot(b - a, b - a), 0, 1)
        d = min(d, float(np.linalg.norm([rp, zp] - (a + t * (b - a)))))
    return d


def folgas(corpos, perfil, alinhar=True):
    """Menor folga radial e axial dos corpos contra o envelope, e onde ocorrem."""
    rad, axi = None, None
    topo = perfil[0][-1]
    negativos = []
    for c in corpos:
        P = pontos(c, alinhar)
        rr = np.hypot(P[:, 0], P[:, 1])
        fol = np.interp(P[:, 2], perfil[0], perfil[1], right=0.0) - rr
        i = int(np.argmin(fol))
        if fol[i] < 0:
            negativos.append({"corpo": c["nome"], "folga_radial_m": float(fol[i])})
        if rad is None or fol[i] < rad["folga_radial_m"] - EMPATE_M:
            rad = {"folga_radial_m": float(fol[i]), "corpo": c["nome"], "z_m": float(P[i, 2]), "raio_do_corpo_m": float(rr[i]),
                   "distancia_measure_m": distancia_ao_perfil(float(rr[i]), float(P[i, 2]), perfil), "tipo": c["tipo"]}
        j = int(np.argmax(P[:, 2]))
        if axi is None or topo - P[j, 2] < axi["folga_axial_m"] - EMPATE_M:
            axi = {"folga_axial_m": float(topo - P[j, 2]), "corpo": c["nome"], "z_m": float(P[j, 2]), "topo_envelope_m": float(topo)}
    rad["corpos_com_folga_negativa"] = negativos
    return rad, axi


def fora_da_capsula(corpos, perfil, h_cz):
    """Peças internas que passam da face externa da cápsula (m; negativo = atravessa). O estágio de cruzeiro fica fora por
    arranjo (P-095) e os propelentes estão dentro dos tanques, então não entram."""
    L = perfil[0][-1]
    fora = ("Nariz", "Escudo", "Casca", "Tampa", "Propelente", "Tanque cruzeiro", "Circuito", "MAV propelente")
    linhas = []
    for c in corpos:
        if c["nome"].startswith(fora):
            continue
        P = pontos(c)
        P = P[P[:, 2] >= h_cz]
        fol = np.interp(L - (P[:, 2] - h_cz), perfil[0], perfil[1], left=0.0, right=0.0) - np.hypot(P[:, 0], P[:, 1])
        i = int(np.argmin(fol))
        linhas.append({"corpo": c["nome"], "folga_m": float(fol[i]), "z_m": float(P[i, 2])})
    # o MAV entra como um só: a peça dele mais próxima da casca
    pecas_mav = [x for x in linhas if x["corpo"].startswith("MAV")]
    menor = min(round(x["folga_m"], CASAS_DE_ORDEM) for x in pecas_mav)
    empatadas = sorted((x for x in pecas_mav if round(x["folga_m"], CASAS_DE_ORDEM) == menor), key=lambda x: x["corpo"])
    mav = {**empatadas[0], "corpo": "MAV (mais próximas: " + "; ".join(x["corpo"] for x in empatadas) + ")"}
    linhas = [x for x in linhas if not x["corpo"].startswith("MAV")] + [mav]
    return sorted(linhas, key=lambda x: (round(x["folga_m"], CASAS_DE_ORDEM), x["corpo"]))


def com_6_algarismos(corpos):
    """Os corpos como a Etapa 7.2 os exportava, com 6 algarismos: só para a comparação em results/etapa7.2b/folgas.md."""
    r6 = lambda x: [r6(y) for y in x] if isinstance(x, list) else float(f"{float(x):.6g}")  # noqa: E731
    fora = []
    for c in corpos:
        d = {k: (r6(x) if k in ("p0", "p1", "c", "c1", "c2", "r", "t", "r0", "r1", "ri0", "ri1") else x) for k, x in c.items()}
        if c["material"] == "equivalente":
            d["densidade"] = r6(c["densidade"] * cp.volume(c) / cp.volume(d))
        fora.append(d)
    return fora


def propriedades(corpos, dens):
    """Massa (kg), CG (m) e tensor de inércia no CG (kg·m²), pelas fórmulas de tools/cad_parametros.py."""
    m, cg = massa_cg(corpos, dens)
    t = np.zeros((3, 3))
    for c in corpos:
        rho = c["densidade"] if c["material"] == "equivalente" else dens[c["material"]]
        d = cp.centro(c) - np.array(cg)
        t += cp.inercia(c, rho) + rho * cp.volume(c) * (np.dot(d, d) * np.eye(3) - np.outer(d, d))
    return m, cg, t.tolist()


def chave_de_simetria(c):
    """Invariante à rotação em torno do eixo z: peças com a mesma chave são exatamente simétricas."""
    t = c["tipo"]
    raio = lambda p: round(float(np.hypot(p[0], p[1])), CASAS_DE_ORDEM)  # noqa: E731
    if t.startswith("esfera"):
        return (t, raio(c["c"]), c["c"][2], c["r"])
    if t == "caixa":
        return (t, tuple(c["c1"]), tuple(c["c2"]))
    return (t, raio(c["p0"]), c["p0"][2], raio(c["p1"]), c["p1"][2], c.get("r", c.get("r0")), c.get("r1"))


def criterio_de_empate(listas):
    """(a) maior diferença dentro de um grupo de peças simétricas; (b) menor diferença acima de EMPATE_M entre grupos
    distintos; (b') o mesmo, só nos pares que decidem texto: o limitador contra o grupo seguinte e a lista contra a cápsula;
    e os grupos distintos que coincidem até EMPATE_M (a mesma cota, como o ombro compartilhado)."""
    sims, dists, decs, coin = [], [], [], set()
    for onde, lin in listas:
        grupos = {}
        for val, nome, ch in lin:
            grupos.setdefault(ch, []).append((val, nome))
        for g in grupos.values():
            if len(g) > 1:
                sims.append((max(x[0] for x in g) - min(x[0] for x in g), onde, sorted(x[1] for x in g)[:2]))
        # grupos distintos em ordem de valor; vão até EMPATE_M é coincidência, e a coincidência é listada pelos nomes
        rep = sorted((min(x[0] for x in g), min(x[1] for x in g)) for g in grupos.values())
        blocos = [[rep[0]]]
        for item in rep[1:]:
            if item[0] - blocos[-1][-1][0] <= EMPATE_M:
                blocos[-1].append(item)
            else:
                blocos.append([item])
        coin.update(tuple(sorted(n for _, n in b_)) for b_ in blocos if len(b_) > 1)
        distintos = []
        for b0, b1 in zip(blocos, blocos[1:]):
            distintos.append((min(x[0] for x in b1) - max(x[0] for x in b0), onde, [min(n for _, n in b0), min(n for _, n in b1)]))
        dists += distintos
        decs += distintos if "cápsula" in onde else distintos[:1]

    def estavel(itens, sinal):
        """O extremo da lista; entre empatados até EMPATE_M, sempre o mesmo, pelo nome: o texto não depende de ruído."""
        ext = sinal * max(sinal * x[0] for x in itens)
        c = min((x for x in itens if abs(x[0] - ext) <= EMPATE_M / 1e4), key=lambda x: (x[1], x[2]))
        return {"diferenca_m": c[0], "pecas": c[2], "onde": c[1]}
    return estavel(sims, 1), estavel(dists, -1), estavel(decs, -1), sorted(list(x) for x in coin)


# ------------------------------------------------------------------------------------------------- principal
def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    cad, env, par = ler("config/cad.yaml"), ler("results/etapa7.1/envelope.yaml"), ler("results/etapa7.2/parametros.yaml")
    arq, mot = ler("results/etapa2.5/arquitetura.yaml"), ler("config/motores.yaml")
    enc = cad["encaixe"]
    versao, t_casca, cor = int(v(enc["versao_featurescript"])), v(enc["espessura_casca_envelope_m"]), enc["cor_envelope"]["valor"]
    rmin = v(cad["construcao"]["raio_minimo_m"])
    cv, cf = env["coifas"]["vulcan"], env["coifas"]["falcon"]
    # segunda leitura do Vulcan: a mesma regra de tools/cad_parametros.py (o diâmetro menor desde o plano da interface)
    rv2 = [cv["raio_m"][1], cv["raio_m"][1]] + list(cv["raio_m"][2:])
    op_v = [{"rotulo": "Contorno reto entre as cotas", "segmentos": segmentos(cv["altura_m"], cv["raio_m"], t_casca)},
            {"rotulo": "Diametro menor desde o plano da interface", "segmentos": segmentos(cv["altura_m"], rv2, t_casca)}]
    # o topo do Falcon termina em ponta (raio zero); o tronco usa o raio mínimo de construção (P-093)
    rf = [max(r, rmin) for r in cf["raio_m"]]
    op_f = [{"rotulo": "Keep-in do fabricante, faixas de 500 mm", "segmentos": segmentos(cf["altura_m"], rf, t_casca)}]
    envelope_fs("envelope_vulcan.fs", "MarsMission envelope Vulcan", "marsMissionEnvelopeVulcan",
                "Envelope: leitura da figura \"Simplified\" [F80] Fig. 4.3.1-1, p. 4-8, nao e dado do fabricante em CAD. Plano: \"LV STA 2596.66 (1575 Interface)\".",
                "Envelope Vulcan VC4 (referencia, sem material)", cor, op_v, versao)
    envelope_fs("envelope_falcon_heavy.fs", "MarsMission envelope Falcon Heavy", "marsMissionEnvelopeFalconHeavy",
                "Envelope: perfil amostrado do STEP de keep-in do fabricante [F82] p. 16, Tab. 4-1. Plano: origem do arquivo, premissa P-096.",
                "Envelope Falcon Heavy (referencia, sem material)", cor, op_f, versao)
    ve = par["veiculos"]
    _, dens = cp.densidades(cad)
    lan45 = cp.monta_lander(cad, env, arq, mot, "msl_m2020").corpos
    corpos = {"lander_4_65": ve["lander"], "lander_4_5": lan45, "orbitador": ve["orbitador"]}
    donos = {"lander_4_65": "Circuito de fluido", "lander_4_5": "Circuito de fluido", "orbitador": "Cilindro central"}
    veic = {}
    for k, cs in corpos.items():
        i = next(n for n, c in enumerate(cs) if c["nome"].startswith(donos[k]))
        veiculo_fs(k, cs, par["materiais"], i, versao)
        m, cg = massa_cg(cs, dens)
        veic[k] = {"massa_kg": m, "cg_m": cg, "corpos": len(cs), "dono_do_conector": cs[i]["nome"]}

    conf = par["conferencias"]["lander_vulcan"]["por_forma"]
    perfis = {k: ([float(x) for x in c["x_m"]], [float(x) for x in c["r_m"]]) for k, c in cad["capsulas"].items() if isinstance(c, dict) and "x_m" in c}
    h_cz = par["conferencias"]["lander_vulcan"]["altura_estagio_cruzeiro_m"]
    leituras = [("envelope_vulcan.fs", 0, "folga_radial_m"), ("envelope_vulcan.fs", 1, "folga_sem_afunilamento_m")]
    linhas = []
    for veiculo, forma, rot in (("lander_4_5", "msl_m2020", "4,5 m"), ("lander_4_65", "srl_a", "4,65 m")):
        for a, i, chave in leituras:
            perf = perfil_lido(a, i)
            r, ax = folgas(corpos[veiculo], perf)
            # o cálculo da Etapa 7.2 amostra o perfil em 400 pontos, sem passar pelo vértice do ombro
            xs = np.linspace(0, perfis[forma][0][-1], 400)
            grade = min(ea.raio_envelope(perf, h_cz + perfis[forma][0][-1] - x) - cp.capsula_raio(perfis[forma], x) for x in xs)
            linhas.append({"veiculo": veiculo, "rotulo": f"Lander, aeroshell {rot}", "envelope": a, "leitura": op_v[i]["rotulo"], "radial": r, "axial": ax,
                           "referencia_7_2_m": conf[forma][chave], "reproducao_grade_400_m": grade, "diferenca_m": r["folga_radial_m"] - conf[forma][chave]})
    perf_f = perfil_lido("envelope_falcon_heavy.fs", 0)
    r, ax = folgas(corpos["orbitador"], perf_f)
    ref = min(par["conferencias"]["orbitador_falcon"], key=lambda c: c["folga_radial_m"])
    linhas.append({"veiculo": "orbitador", "rotulo": "Orbitador", "envelope": "envelope_falcon_heavy.fs", "leitura": op_f[0]["rotulo"], "radial": r, "axial": ax,
                   "referencia_7_2_m": ref["folga_radial_m"], "referencia_7_2_conjunto": ref["conjunto"], "diferenca_m": r["folga_radial_m"] - ref["folga_radial_m"]})
    # SRL-C: a pior forma da P-089, sem modelo próprio; só o perfil da cápsula, nos vértices
    srlc = {}
    for a, i, chave in leituras:
        perf = perfil_lido(a, i)
        L = perfis["srl_c"][0][-1]
        srlc[chave] = {"vertice_m": min(float(np.interp(h_cz + L - x, perf[0], perf[1])) - r_ for x, r_ in zip(*perfis["srl_c"])), "referencia_7_2_m": conf["srl_c"][chave]}
    # comparação com a grade antiga e os 6 algarismos antigos
    antes = {}
    for li in linhas:
        a_ = li["envelope"]
        i_ = next((i for i, o_ in enumerate(op_v) if o_["rotulo"] == li["leitura"]), 0)
        r_a, ax_a = folgas(com_6_algarismos(corpos[li["veiculo"]]), perfil_lido(a_, i_), alinhar=False)
        antes[(li["veiculo"], li["leitura"])] = {"radial_m": r_a["folga_radial_m"], "measure_m": r_a["distancia_measure_m"], "z_m": r_a["z_m"], "raio_m": r_a["raio_do_corpo_m"], "axial_m": ax_a["folga_axial_m"], "corpo": r_a["corpo"], "z_axial_m": ax_a["z_m"]}
    compara = []
    for li in linhas:
        ant, ra, axx = antes[(li["veiculo"], li["leitura"])], li["radial"], li["axial"]
        for nome, x, y in (("folga radial", ant["radial_m"], ra["folga_radial_m"]), ("distância no Measure", ant["measure_m"], ra["distancia_measure_m"]), ("z da folga radial", ant["z_m"], ra["z_m"]), ("raio do corpo", ant["raio_m"], ra["raio_do_corpo_m"]), ("folga axial", ant["axial_m"], axx["folga_axial_m"]), ("z do topo", ant["z_axial_m"], axx["z_m"])):
            compara.append({"veiculo": li["veiculo"], "leitura": li["leitura"], "grandeza": nome, "antes": x, "agora": y, "diferenca_m": y - x, "igual_em_3_casas": br(x) == br(y)})
    compara.sort(key=lambda x: (-round(abs(x["diferenca_m"]), CASAS_DE_ORDEM), x["veiculo"], x["leitura"], x["grandeza"]))
    props = {}
    for k, cs in {"lander": ve["lander"], "orbitador": ve["orbitador"], "mav": ve["mav"], "lander_4_5": lan45}.items():
        m6, cg6, i6 = propriedades(com_6_algarismos(cs), dens)
        m13, cg13, i13 = propriedades(cs, dens)
        props[k] = {"massa_6_kg": m6, "massa_13_kg": m13, "dif_massa_kg": m13 - m6, "dif_cg_max_m": max(abs(a - b) for a, b in zip(cg6, cg13)),
                    "dif_inercia_max_kg_m2": max(abs(a - b) for x, y in zip(i6, i13) for a, b in zip(x, y)),
                    "acima_p039": any(abs(a - b) > max(1e-9 * abs(b), 1e-10) for a, b in [(m6, m13)] + list(zip(cg6, cg13)) + [(a, b) for x, y in zip(i6, i13) for a, b in zip(x, y)])}
    # tanques de descida: posições gravadas no .fs e diferença entre eles
    td = [c for c in corpos["lander_4_65"] if c["nome"].startswith("Tanque descida")]
    tanques = {"centros_m": [c["c"] for c in td], "raios_do_centro_m": [float(np.hypot(c["c"][0], c["c"][1])) for c in td], "z_iguais": len({c["c"][2] for c in td}) == 1, "r_iguais": len({c["r"] for c in td}) == 1}
    tanques["diferenca_max_raio_m"] = max(tanques["raios_do_centro_m"]) - min(tanques["raios_do_centro_m"])
    # critério de empate: todas as listas que EMPATE_M e CASAS_DE_ORDEM comparam
    listas = []
    for li_cfg in [(v_, a_, i_) for v_ in ("lander_4_5", "lander_4_65") for a_, i_, _ in leituras] + [("orbitador", "envelope_falcon_heavy.fs", 0)]:
        k, a_, i_ = li_cfg
        perf = perfil_lido(a_, i_)
        rad_l, axi_l = [], []
        for c in corpos[k]:
            P = pontos(c)
            f = np.interp(P[:, 2], perf[0], perf[1], right=0.0) - np.hypot(P[:, 0], P[:, 1])
            rad_l.append((float(f.min()), c["nome"], chave_de_simetria(c)))
            axi_l.append((float(perf[0][-1] - P[:, 2].max()), c["nome"], chave_de_simetria(c)))
        listas += [(f"{k}, {a_}, leitura {i_ + 1}, radial", rad_l), (f"{k}, {a_}, leitura {i_ + 1}, axial", axi_l)]
    for k, f_ in (("lander_4_5", "msl_m2020"), ("lander_4_65", "srl_a")):
        L = perfis[f_][0][-1]
        fora = ("Nariz", "Escudo", "Casca", "Tampa", "Propelente", "Tanque cruzeiro", "Circuito", "MAV propelente")
        lin = []
        for c in corpos[k]:
            if c["nome"].startswith(fora):
                continue
            P = pontos(c)
            P = P[P[:, 2] >= h_cz]
            lin.append((float((np.interp(L - (P[:, 2] - h_cz), perfis[f_][0], perfis[f_][1], left=0.0, right=0.0) - np.hypot(P[:, 0], P[:, 1])).min()), c["nome"], chave_de_simetria(c)))
        listas.append((f"{k}, peças contra a cápsula", lin))
    sim, dist, dec, coin = criterio_de_empate(listas)
    crit = enc["criterio_empate"]
    empate = {"simetricas": sim, "distintas": dist, "distintas_que_decidem_texto": dec, "coincidencias": coin, "limite_simetricas_m": crit["simetricas_max_m"], "limite_distintas_m": crit["distintas_min_m"],
              "passa": sim["diferenca_m"] <= crit["simetricas_max_m"] and dist["diferenca_m"] >= crit["distintas_min_m"], "empate_m": EMPATE_M, "casas_de_ordem": CASAS_DE_ORDEM}
    inclinacao = (cv["raio_m"][0] - cv["raio_m"][1]) / (cv["altura_m"][1] - cv["altura_m"][0])
    mav45 = par["conferencias"]["mav_deitado"]["por_forma"]["msl_m2020"][0]
    capsula = {k: fora_da_capsula(corpos[k], perfis[f], h_cz) for k, f in (("lander_4_5", "msl_m2020"), ("lander_4_65", "srl_a"))}
    out = nativo({"gerado_por": "tools/encaixe_coifas.py", "natureza": "VERIFICAÇÃO geométrica do modelo, não validação", "veiculos": veic, "configuracoes": linhas, "srl_c_so_perfil": srlc,
                  "reducao_de_folga_por_metro_de_adaptador_vulcan": inclinacao, "mav_na_capsula_4_5": mav45, "pecas_contra_a_capsula": capsula, "folga_interna_m": par["conferencias"]["mav_deitado"]["folga_interna_m"], "espessura_casca_m": t_casca,
                  "comparacao_grade_e_precisao": compara, "propriedades_6_e_13_algarismos": props, "tanques_descida": tanques, "criterio_empate": empate,
                  "premissas_propostas": enc["premissas_propostas"], "planos": {"vulcan": enc["plano_vulcan"]["fonte"], "falcon": enc["plano_falcon"]["fonte"]}})
    (SAIDA / "folgas.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)
    escreve_roteiro(out)


# ------------------------------------------------------------------------------------------------- relatórios
def ex(x):
    return f"{x:.2e}".replace(".", ",").replace("-", "−")


def br(x, n=3):
    return f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def sg(x, n=3):
    return f"{round(x, n) + 0.0:+,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def escreve_md(o):
    md = ["# Etapa 7.2b: folgas nas coifas (gerado por tools/encaixe_coifas.py)", "",
          "**VERIFICAÇÃO geométrica do modelo, não validação.** O envelope do Vulcan é leitura de uma figura \"Simplified\" do guia. O do Falcon é o STEP do fabricante amostrado em faixas de 500 mm. "
          "Nenhum deles é o CAD de interface do fabricante em voo.", "",
          "## Folgas mínimas", "", "Calculadas com todos os corpos de cada modelo, contra a face interna do envelope gravada no arquivo .fs. Em m.", "",
          "| Configuração | Leitura do envelope | Folga radial | Onde | z (m) | Folga axial | Onde | Etapa 7.2 | Diferença |", "| :- | :- | -: | :- | -: | -: | :- | -: | -: |"]
    for li in o["configuracoes"]:
        r, a = li["radial"], li["axial"]
        md.append(f"| {li['rotulo']} | {li['leitura']} | {sg(r['folga_radial_m'])} | {r['corpo']} | {br(r['z_m'])} | {sg(a['folga_axial_m'])} | {a['corpo']} | {sg(li['referencia_7_2_m'])} | {sg(li['diferenca_m'])} |")
    lander = [x for x in o["configuracoes"] if x["veiculo"] != "orbitador"]
    orb = next(x for x in o["configuracoes"] if x["veiculo"] == "orbitador")
    md += ["", "## Por que as folgas do lander não batem com as da Etapa 7.2", "",
           "**A diferença vem da amostragem da Etapa 7.2.** O `folga_vulcan` de `tools/cad_parametros.py` amostra o perfil da cápsula em 400 pontos, e nenhum cai no vértice do ombro, onde o raio é máximo. "
           "Por isso os valores publicados saem um pouco maiores que os da geometria que o Onshape constrói. A coluna abaixo repete a conta antiga, com o envelope lido do arquivo .fs:", "",
           "| Configuração | Leitura | Conta da 7.2 repetida | Publicado na 7.2 | Geometria, no vértice |", "| :- | :- | -: | -: | -: |"]
    for li in lander:
        md.append(f"| {li['rotulo']} | {li['leitura']} | {sg(li['reproducao_grade_400_m'], 4)} | {sg(li['referencia_7_2_m'], 4)} | {sg(li['radial']['folga_radial_m'], 4)} |")
    sc = o["srl_c_so_perfil"]
    md += ["", f"Com a SRL-C, a pior forma da P-089 e sem modelo próprio, os vértices dão {sg(sc['folga_radial_m']['vertice_m'])} e {sg(sc['folga_sem_afunilamento_m']['vertice_m'])} m, "
           f"contra {sg(sc['folga_radial_m']['referencia_7_2_m'])} e {sg(sc['folga_sem_afunilamento_m']['referencia_7_2_m'])} m publicados.", "",
           "A errata foi aprovada pelo Fabio (2026-11-04) e está em `results/etapa7.2/conferencias.md` e `portao_decisao.md`, com os valores antigos e os novos lado a lado.", "",
           f"**Orbitador:** a Etapa 7.2 dá {sg(orb['referencia_7_2_m'])} m ({orb['referencia_7_2_conjunto']}), porque trata cada conjunto como um cilindro no raio máximo. Aqui as esferas têm a forma real, e a folga é maior. "
           "As duas contas respondem a perguntas diferentes, e a da 7.2 fica do lado seguro.", "",
           "## O que os arquivos têm", "", "| Arquivo | Veículo | Corpos | Massa (kg) | CG x, y, z (m) | Mate connector preso a |", "| :- | :- | -: | -: | :- | :- |"]
    for k, x in o["veiculos"].items():
        md.append(f"| {k}.fs | {k} | {x['corpos']} | {br(x['massa_kg'], 3)} | " + ", ".join(br(c, 4) for c in x["cg_m"]) + f" | {x['dono_do_conector']} |")
    mv = o["mav_na_capsula_4_5"]
    md += ["", "**O que mudou em relação a `results/etapa7.2/orbitador.fs` e `lander.fs`:** a versão do cabeçalho, de 2737 para 3112; a linha de comentário com o rótulo de verificação; a constante `DONO_INTERFACE`; e o bloco `opMateConnector` no fim da feature. "
           "A lista CORPOS é a mesma (`tests/test_cad.py` confere), então massa e CG não mudam. O `mav.fs` não muda: o MAV não tem interface com o adaptador.", "",
           f"**`lander_4_5.fs` é um modelo novo:** cápsula MSL/M2020 e o resto do arranjo igual, com a massa acima. O MAV deitado viola a folga interna de {br(o['folga_interna_m'], 2)} m da P-087 "
           f"(folga de {sg(mv['folga_m'])} m com a base na estação {br(mv['estacao_base_m'], 2)} m), mas não toca a casca. As peças que atravessam a face externa da cápsula são outras:", "",
           "| Peça | Lander 4,5 m: folga até a face externa (m) | z (m) | Lander 4,65 m: folga até a face externa (m) | z (m) |", "| :- | -: | -: | -: | -: |"]
    p465 = {x["corpo"].split(" (")[0]: x for x in o["pecas_contra_a_capsula"]["lander_4_65"]}
    for x in o["pecas_contra_a_capsula"]["lander_4_5"]:
        y = p465[x["corpo"].split(" (")[0]]
        if x["folga_m"] < 0 or y["folga_m"] < 0 or x["corpo"].startswith("MAV"):
            md.append(f"| {x['corpo']} | {sg(x['folga_m'])} | {br(x['z_m'])} | {sg(y['folga_m'])} | {br(y['z_m'])} |")
    md += ["", "Essas interferências entre peças não são corrigidas aqui (P-095): são o conflito do arranjo, e o Onshape vai mostrá-las.", "",
           "## Grade alinhada e 13 algarismos: o que mudou", "",
           "Antes: grade angular fixa e geometria com 6 algarismos, recalculadas aqui. Agora: grade alinhada à direção radial de cada peça, com 721 pontos, e 13 algarismos. A comparação junta os dois efeitos e cobre as folgas e posições do roteiro; a tabela de peças contra a cápsula não entra nela.", "",
           f"**Nas casas mostradas no roteiro (3):** {'nenhuma folga ou posição mudou' if all(x['igual_em_3_casas'] for x in o['comparacao_grade_e_precisao']) else 'mudaram ' + ', '.join(sorted({x['grandeza'] for x in o['comparacao_grade_e_precisao'] if not x['igual_em_3_casas']}))}. **Maiores diferenças nos valores completos:**", "",
           "| Veículo | Leitura | Grandeza | Antes | Agora | Diferença (m) |", "| :- | :- | :- | -: | -: | -: |"]
    md += [f"| {x['veiculo']} | {x['leitura']} | {x['grandeza']} | {br(x['antes'], 9)} | {br(x['agora'], 9)} | " + f"{x['diferenca_m']:+.2e}".replace(".", ",").replace("-", "−") + " |" for x in o["comparacao_grade_e_precisao"][:6]]
    md += ["", "**Massa, CG e inércia (6 × 13 algarismos), contra a tolerância da P-039:**", "", "| Veículo | Massa com 6 (kg) | Massa com 13 (kg) | Diferença (kg) | Maior diferença no CG (m) | Maior diferença na inércia (kg·m²) | Acima da P-039? |", "| :- | -: | -: | -: | -: | -: | :- |"]
    md += [f"| {k} | {br(x['massa_6_kg'], 4)} | {br(x['massa_13_kg'], 4)} | {ex(x['dif_massa_kg'])} | {ex(x['dif_cg_max_m'])} | {ex(x['dif_inercia_max_kg_m2'])} | {'sim' if x['acima_p039'] else 'não'} |" for k, x in o["propriedades_6_e_13_algarismos"].items()]
    td, em = o["tanques_descida"], o["criterio_empate"]
    md += ["", f"**Tanques de descida:** distância do centro ao eixo: " + "; ".join(f"{r_:.15f}" for r_ in td["raios_do_centro_m"]).replace(".", ",") + f" m; maior diferença de {ex(td['diferenca_max_raio_m'])} m. z e raio {'iguais' if td['z_iguais'] and td['r_iguais'] else 'diferentes'}. "
           "Os tanques 2 e 3 são espelhos, bit a bit. O tanque 1 não fica igual a eles bit a bit: a coordenada y dos outros dois, 1,4 · sen 120°, é arredondada a 13 algarismos significativos em decimal.", "",
           "## Parâmetros de desempate", "",
           f"`empate_m` = {ex(em['empate_m'])} m; `casas_de_ordem` = {em['casas_de_ordem']}, em casas decimais de metro. Valor e justificativa em config/cad.yaml.", "",
           "| Item | Valor (m) | Limite (m) | Onde |", "| :- | -: | -: | :- |",
           f"| (a) maior diferença entre peças exatamente simétricas | {ex(em['simetricas']['diferenca_m'])} | ≤ {ex(em['limite_simetricas_m'])} | {'; '.join(em['simetricas']['pecas'])} ({em['simetricas']['onde']}) |",
           f"| (b) menor diferença real entre peças distintas | {ex(em['distintas']['diferenca_m'])} | ≥ {ex(em['limite_distintas_m'])} | {'; '.join(em['distintas']['pecas'])} ({em['distintas']['onde']}) |",
           f"| (b'), só os pares que decidem texto gerado: o limitador contra o seguinte, e a lista de peças contra a cápsula | {ex(em['distintas_que_decidem_texto']['diferenca_m'])} | ≥ {ex(em['limite_distintas_m'])} | {'; '.join(em['distintas_que_decidem_texto']['pecas'])} ({em['distintas_que_decidem_texto']['onde']}) |", "",
           f"**Resultado, com (a) e (b) literais: {'passa nos dois, aprovação registrada em config/cad.yaml' if em['passa'] else 'NÃO passa; os parâmetros precisam de nova decisão do Fabio'}.** Grupos de peças distintas com a mesma cota, até `empate_m`: " + "; ".join(" × ".join(p_) for p_ in em["coincidencias"]) + ".", "",
           "## Planos da interface", "",
           f"- **Vulcan, com fonte:** {o['planos']['vulcan']}.",
           f"- **Falcon, sem fonte direta:** {o['planos']['falcon']}.",
           "- **Veículos, sem fonte:** z = 0 do modelo. Um adaptador real subiria o veículo; as alturas com fonte e as folgas estão em results/etapa7.2/rota_a.md, seção 5. "
           f"Na primeira leitura do Vulcan, cada metro de altura tira {br(o['reducao_de_folga_por_metro_de_adaptador_vulcan'], 4)} m de folga radial.", "",
           "## Premissas propostas (não entraram em config/premissas.yaml; pendentes do Fabio)", "", "| Id | Texto | Evidência |", "| :- | :- | :- |"]
    for p in o["premissas_propostas"]:
        md.append(f"| {p['id']} | {p['texto']} | {p['evidencia']} |")
    md += ["", f"A espessura de {br(o['espessura_casca_m'], 2)} m da casca é escolha de construção, sem efeito nas folgas. Os arquivos .fs não foram compilados nesta máquina: a compilação é o primeiro passo do roteiro."]
    (SAIDA / "folgas.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def escreve_roteiro(o):
    cfg = o["configuracoes"]
    md = ["# Roteiro no Onshape: veículos dentro das coifas (gerado por tools/encaixe_coifas.py)", "",
          "**VERIFICAÇÃO geométrica do modelo, não validação.** O envelope do Vulcan é leitura de figura do guia, e o do Falcon é o STEP do fabricante amostrado.", "",
          "**Nota (2026-11-06):** os arquivos desta página têm 13 algarismos; as massas esperadas abaixo já são as vigentes, e o orbitador passou de 6 506,2 para o valor do passo correspondente (results/etapa7.2b/folgas.md).", "",
          "**Não conferido:** os arquivos não foram compilados aqui, e as páginas de ajuda do Onshape não abriram na consulta. Os nomes de comandos (Commit, Mass Properties, Insert, Group, Measure e os da Assembly) vêm de memória e podem variar. Se algo não bater, anote o que apareceu.", "",
          "## A. Colar os Feature Studios", ""]
    n = 0

    def passo(txt):
        nonlocal n
        n += 1
        md.append(f"{n}. {txt}")
    arqs = ["envelope_vulcan.fs", "envelope_falcon_heavy.fs", "lander_4_65.fs", "lander_4_5.fs", "orbitador.fs"]
    passo("Abra o documento \"MarsMission Fase 7\", ou crie um documento novo só para esta etapa.")
    for a in arqs:
        passo(f"Crie um Feature Studio chamado `{a[:-3]}`.")
        passo("Apague o conteúdo que ele já traz.")
        passo(f"Cole o conteúdo de `results/etapa7.2b/{a}`.")
        passo("Clique em Commit e confira se não há erro.")
    md += ["", "## B. Criar os Part Studios", ""]
    ps = [("Vulcan leitura 1", "MarsMission envelope Vulcan", "Contorno reto entre as cotas"), ("Vulcan leitura 2", "MarsMission envelope Vulcan", "Diametro menor desde o plano da interface"),
          ("Falcon Heavy", "MarsMission envelope Falcon Heavy", None), ("Lander 4,65", "MarsMission lander_4_65", None), ("Lander 4,5", "MarsMission lander_4_5", None), ("Orbitador", "MarsMission orbitador", None)]
    for nome, feat, opc in ps:
        passo(f"Crie um Part Studio chamado `{nome}`.")
        passo(f"Adicione a feature \"{feat}\".")
        if opc:
            passo(f"Em \"Leitura do envelope\", escolha \"{opc}\".")
        elif "envelope" not in feat:
            passo("Marque \"Assign materials\".")
    for k, x in o["veiculos"].items():
        passo(f"Abra `{'Orbitador' if k == 'orbitador' else 'Lander ' + k.split('_', 1)[1].replace('_', ',')}`.")
        passo("Selecione todas as peças.")
        passo("Abra Mass Properties.")
        passo(f"Confira: {br(x['massa_kg'], 1)} kg e CG em " + ", ".join(br(c, 3) for c in x["cg_m"]) + " m.")
    passo("Confira se cada envelope aparece transparente.")
    passo("Se não aparecer, ajuste a aparência à mão; isso não muda nenhum número.")
    md += ["", "## C. Montar uma Assembly para cada configuração", "", "| Assembly | Veículo | Envelope |", "| :- | :- | :- |"]
    nomes_ps = {"lander_4_65": "Lander 4,65", "lander_4_5": "Lander 4,5", "orbitador": "Orbitador"}
    amb = []
    for i, li in enumerate(cfg):
        e = "Falcon Heavy" if li["veiculo"] == "orbitador" else ("Vulcan leitura 1" if li["leitura"].startswith("Contorno") else "Vulcan leitura 2")
        amb.append(f"A{i + 1}")
        md.append(f"| A{i + 1} | {nomes_ps[li['veiculo']]} | {e} |")
    md.append("")
    passo(f"Crie uma Assembly para cada linha da tabela ({', '.join(amb)}).")
    passo("Repita os próximos passos em cada Assembly.")
    passo("Clique em Insert e insira o Part Studio do envelope.")
    passo("Clique com o botão direito no envelope e escolha Fix.")
    passo("Insira o Part Studio do veículo, inteiro.")
    passo("Arraste uma peça do veículo.")
    passo("Se ela sair sozinha, selecione todas as peças do veículo e crie um Group, para que andem juntas.")
    passo("Escolha o mate Fastened.")
    passo("Clique no mate connector do envelope, no plano da interface.")
    passo("Clique no mate connector do veículo, no plano da interface.")
    passo("Confirme o mate.")
    passo("Confira se o veículo ficou dentro do envelope, com o topo para cima.")
    passo("Se o veículo ficar de cabeça para baixo, use a opção de inverter o eixo no diálogo do mate.")
    md += ["", "## D. Medir as folgas (ferramenta Measure)", "",
           "Selecione as duas entidades da tabela e leia a distância mínima. A leitura deve bater com o valor esperado na terceira casa.", "",
           f"**Cuidado:** o envelope é uma casca de {br(o['espessura_casca_m'], 2)} m, e a medida vale na face INTERNA, que fica atrás da externa. Use uma vista em corte (Section view) para selecionar. Medir na externa soma cerca de {br(o['espessura_casca_m'], 2)} m na leitura. As faces do topo são pequenas: aproxime bem a vista.", "",
           "| Assembly | Medida | Selecione no veículo | Selecione no envelope | Esperado (m) | Folga com sinal (m) |", "| :- | :- | :- | :- | -: | -: |"]
    for i, li in enumerate(cfg):
        r, a = li["radial"], li["axial"]
        alvo = "a face da peça, perto do ponto mais próximo" if r["tipo"].startswith("esfera") or r["tipo"] == "caixa" else "a aresta circular"
        md.append(f"| A{i + 1} | radial | {alvo} de `{cp.ascii_(r['corpo'])}`, em z = {br(r['z_m'])} m e raio {br(r['raio_do_corpo_m'])} m | a face interna na mesma altura | {br(r['distancia_measure_m'])} | {sg(r['folga_radial_m'])} |")
        md.append(f"| A{i + 1} | axial | o topo de `{cp.ascii_(a['corpo'])}`, em z = {br(a['z_m'])} m | a face interna plana do topo, em z = {br(a['topo_envelope_m'])} m | {br(a['folga_axial_m'])} | {sg(a['folga_axial_m'])} |")
    md += ["", "O valor esperado é a menor distância entre as superfícies, um pouco menor que a folga horizontal onde o envelope é inclinado. O Measure não mostra o sinal (não conferido): uma folga negativa aparece como valor positivo, e quem diz que há interferência é a seção E.", "",
           "## E. Rodar Check interference", ""]
    passo("Em cada Assembly, use o comando de interferência (Check interference ou o nome equivalente no menu).")
    passo("Só importam os pares que incluem a peça Envelope. Pares entre peças do próprio veículo vão aparecer, como helicópteros e tanques de descida (folgas.md), e não têm valor esperado aqui (P-095).")
    md += ["", "| Assembly | Esperado com a peça Envelope |", "| :- | :- |"]
    for i, li in enumerate(cfg):
        neg = li["radial"]["corpos_com_folga_negativa"]
        md.append(f"| A{i + 1} | " + ("interferência com " + " e ".join(f"`{cp.ascii_(x['corpo'])}`" for x in neg) + ", no ombro" if neg else "nenhuma") + " |")
    md += ["", "## F. Anotar", ""]
    passo("Para cada Assembly, anote o valor lido no Measure e o resultado do Check interference.")
    passo("Mande os valores para registro. O estudo compara cada um com o esperado desta página.")
    (SAIDA / "roteiro_onshape.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
