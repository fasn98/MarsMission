"""Lei de massa inerte do MAV sólido ancorada em motores reais (Fabio, 2026-11-10, PR #60, itens 3 e 4).

Item 3: ajuste inerte × propelente dos motores sólidos de estágio superior do catálogo [F270]; comparação com a P-019 e a
P-111; a lei proposta (P-113, NÃO VALIDADA) em duas variantes do nível do motor:
  inerte do estágio i = N_i + c_i · P_i^b
  b: expoente do ajuste do catálogo; N_i: inerte não propulsivo do MAV do MSR ([F269]), fixo na escala;
  A: c_i pelo inerte do motor do MSR ([F269]); B: c_i pela divisão do inerte que a verificação da P-110 escolheu.
Item 4: cada variante na verificação (órbita publicada do MSR), na varredura da escala a 380 km (P-110), no caso com a
margem da P-014 simulado com o modelo de subida do sólido, e as folgas com deck no aeroshell de 4,65 m.
Saída: results/familia1/inerte_solido.yaml e .md

Uso: python tools/inerte_solido.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import mav_familia1 as mf  # noqa: E402
import subida_mav as sm  # noqa: E402
from orbital import subida as sb  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "familia1"
br, sg = sm.br, sm.sg


def ajuste(P, I):
    """Ajuste de mínimos quadrados de ln I = ln a + b ln P: (a, b, erro-padrão de b, resíduos em ln)."""
    x, y = np.log(P), np.log(I)
    A = np.vstack([np.ones_like(x), x]).T
    (la, b), *_ = np.linalg.lstsq(A, y, rcond=None)
    r = y - (la + b * x)
    s2 = float(r @ r) / (len(x) - 2)
    se_b = math.sqrt(s2 / float(((x - x.mean()) ** 2).sum()))
    return math.exp(la), float(b), se_b, r


def estagios(s, lei, mp, f, isp, carga):
    """Estágios e inertes do sólido na escala s do propelente e do empuxo do MSR, com o inerte da lei (N, c, b)."""
    N, c, b = lei
    P = [s * x for x in mp]
    ine = [n + ci * p ** b for n, ci, p in zip(N, c, P)]
    m0 = carga + sum(P) + sum(ine)
    return [sb.Estagio(m0, P[0], s * f[0], isp[0]), sb.Estagio(m0 - P[0] - ine[0], P[1], s * f[1], isp[1])], ine


def main():
    cad, fc, scfg = ler("config/cad.yaml"), ler("config/familia1.yaml"), ler("config/superficie.yaml")
    dcfg, mv, a4 = ler("config/dimensionamento.yaml"), ler("results/familia1/mavs.yaml"), ler("results/familia1/aeroshell_465.yaml")
    cfg = fc["inerte_solido"]
    lb = v(ler("config/motores.yaml")["conversao"]["lb_para_kg"])
    mot = [{"nome": m["nome"], "envelope": m["envelope"], "propelente_kg": m["propelente_lbm"] * lb, "inerte_kg": m["inerte_lbm"] * lb, "pagina_pdf": m["pagina_pdf"]} for m in cfg["motores"]]
    P = np.array([m["propelente_kg"] for m in mot])
    I = np.array([m["inerte_kg"] for m in mot])
    a, b, se_b, r = ajuste(P, I)
    for m, ri in zip(mot, r):
        m["residuo_fator"] = math.exp(ri)
        m["inerte_sobre_propelente"] = m["inerte_kg"] / m["propelente_kg"]
    lk = float(np.mean(np.log(I / P)))   # ajuste proporcional (b = 1), para comparar com as leis lineares
    rk = np.log(I / P) - lk
    ajuste_cat = {"a": a, "b": b, "erro_padrao_b": se_b, "n": len(P), "faixa_propelente_kg": [float(P.min()), float(P.max())],
                  "rms_ln": float(np.sqrt(r @ r / (len(P) - 2))), "fator_rms": math.exp(float(np.sqrt(r @ r / (len(P) - 2)))),
                  "fator_max": math.exp(float(np.abs(r).max())),
                  "proporcional": {"k": math.exp(lk), "fator_rms": math.exp(float(np.sqrt(rk @ rk / (len(P) - 1)))), "fator_max": math.exp(float(np.abs(rk).max()))}}
    # ---------------- MSR, P-019, P-111 e as duas variantes
    msd = cad["mav_solido"]
    mp, isp, tq = msd["propelente_kg"]["valor"], msd["isp_s"]["valor"], msd["tempo_queima_s"]["valor"]
    f = [m_ * i * sb.G0_M / t for m_, i, t in zip(mp, isp, tq)]
    carga = v(scfg["mav"]["carga_util_kg"])
    msr = cfg["msr"]
    Nm, Im, Pm = (msr[k]["valor"] for k in ("inerte_nao_propulsivo_kg", "inerte_motor_kg", "propelente_kg"))
    eps = v(ler("config/mav_propulsao.yaml")["opcoes"]["O1"]["fracao_estrutural"])
    ine_v = mv["verificacao"]["base"]["inertes_kg"]
    leis = {"A (nível do motor pelo [F269])": ([float(x) for x in Nm], [im / pm ** b for im, pm in zip(Im, Pm)], b),
            "B (nível pela divisão verificada da P-110)": ([float(x) for x in Nm], [(iv - n) / p ** b for iv, n, p in zip(ine_v, Nm, mp)], b)}
    comparacao = []
    for i_, nome in enumerate(("estágio 1", "estágio 2")):
        comparacao.append({"estagio": nome, "propelente_kg": mp[i_], "catalogo_motor_kg": a * mp[i_] ** b, "msr_motor_kg": Im[i_], "msr_nao_propulsivo_kg": Nm[i_],
                           "msr_estagio_kg": Im[i_] + Nm[i_], "p019_estagio_kg": eps / (1 - eps) * mp[i_], "p111_estagio_kg": ine_v[i_],
                           **{f"lei_{k[0]}_estagio_kg": l[0][i_] + l[1][i_] * mp[i_] ** l[2] for k, l in leis.items()}})
    # ---------------- subida: verificação, varredura a 380 km, caso com margem
    ctx = sm.contexto()
    sc, _, atm, pl0, _ = ctx
    g = fc["mav_solido"]["guia"]
    vf = fc["mav_solido"]["verificacao"]
    t_v, partidas, limites, tol = v(g["t_v_s"]), g["partidas"]["valor"], [tuple(t) for t in g["limites"]["valor"]], v(g["tol_custo"])
    d_s = mv["limites"]["solido"]["diametro_m"]
    area = v(sc["arrasto"]["cd_base"]) * math.pi * d_s ** 2 / 4
    pl_v = sb.Planeta(pl0.mu, pl0.raio, sb.omega_efetivo(pl0.omega, v(vf["inclinacao_graus"])))
    pl_e = sb.Planeta(pl0.mu, pl0.raio, sb.omega_efetivo(pl0.omega, v(scfg["sitio_e_encontro"]["inclinacao_encontro_graus"])))
    h = v(cfg["altitude_km"])
    margem = v(dcfg["margem_dv"])
    lo, hi = g["escala_busca"]["valor"]
    passo = v(g["passo_varredura_escala"])
    l465, l45 = a4["limites_465"][str(d_s)], a4["limites_45"][str(d_s)]

    def voo(pl, est, ine, h_m):
        c_, vo, gu = sb.ajusta_solido(pl, est, ine, area, atm, h_m, t_v, partidas, limites)
        return {"custo": c_, "fecha": c_ < tol, "periapse_km": vo["periapse_m"] / 1000, "apoapse_km": vo["apoapse_m"] / 1000, "costa_s": vo["costa_s"]}

    def geometria(est):
        mpt = sum(e.propelente_kg for e in est)
        Ls = [lf + (v(msd["comprimento_m"]) - lf) * mpt / sum(mp) for lf in msd["escala"]["comprimento_fixo_m"]["valor"]]
        return {"comprimento_m": [min(Ls), max(Ls)], "folga_465_com_deck_m": [(l465["com_deck_m"] - max(Ls)) / 2, (l465["com_deck_m"] - min(Ls)) / 2],
                "folga_465_sem_deck_m": [(l465["sem_deck_m"] - max(Ls)) / 2, (l465["sem_deck_m"] - min(Ls)) / 2],
                "folga_45_com_deck_m": [(l45["com_deck_m"] - max(Ls)) / 2, (l45["com_deck_m"] - min(Ls)) / 2]}

    casos = []
    for nome, lei in leis.items():
        e1, i1 = estagios(1.0, lei, mp, f, isp, carga)
        x = {"lei": nome, "N_kg": lei[0], "c": lei[1], "b": lei[2], "verificacao": {**voo(pl_v, e1, i1, 1000 * v(vf["orbita_km"])), "inertes_kg": i1, "glom_kg": e1[0].massa_inicial_kg}}
        s_, a_, ok = lo, lo, None
        while s_ <= hi + 1e-9:
            e_, i_ = estagios(s_, lei, mp, f, isp, carga)
            if voo(pl_e, e_, i_, 1000 * h)["fecha"]:
                ok = s_
                break
            a_, s_ = s_, s_ + passo
        x["fecha_na_varredura"] = ok is not None
        if ok is not None:
            b_ = ok
            for _ in range(int(v(g["passos_escala"]))):
                m_ = (a_ + b_) / 2
                e_, i_ = estagios(m_, lei, mp, f, isp, carga)
                a_, b_ = (a_, m_) if voo(pl_e, e_, i_, 1000 * h)["fecha"] else (m_, b_)
            e0, i0 = estagios(b_, lei, mp, f, isp, carga)
            cap0 = mf.capacidade(e0, i0, carga)
            # escala do caso com a margem: a capacidade cresce sem limite com a escala (o inerte cresce menos que o propelente)
            s1, s2 = b_, b_
            while mf.capacidade(*estagios(s2, lei, mp, f, isp, carga), carga) < (1 + margem) * cap0:
                s1, s2 = s2, 2 * s2
            while s2 - s1 > 1e-12 * s2:
                m_ = (s1 + s2) / 2
                s1, s2 = (m_, s2) if mf.capacidade(*estagios(m_, lei, mp, f, isp, carga), carga) < (1 + margem) * cap0 else (s1, m_)
            em, im = estagios(s2, lei, mp, f, isp, carga)
            x["sem_margem"] = {"escala": b_, "capacidade_m_s": cap0, "glom_kg": e0[0].massa_inicial_kg, "propelente_kg": [e.propelente_kg for e in e0], "inertes_kg": i0,
                               "voo": voo(pl_e, e0, i0, 1000 * h), **geometria(e0)}
            x["com_margem"] = {"escala": s2, "capacidade_m_s": mf.capacidade(em, im, carga), "glom_kg": em[0].massa_inicial_kg, "propelente_kg": [e.propelente_kg for e in em],
                               "inertes_kg": im, "voo": voo(pl_e, em, im, 1000 * h), **geometria(em)}
        casos.append(x)
    out = nativo({"gerado_por": "tools/inerte_solido.py", "status": "NÃO VALIDADO", "lb_para_kg": lb, "motores": mot, "ajuste": ajuste_cat, "comparacao_msr": comparacao,
                  "p019_k": eps / (1 - eps), "p111_k": [i / x for i, x in zip(ine_v, mp)], "altitude_km": h, "margem_dv": margem, "tol_custo": tol, "passo": passo,
                  "orbita_verificacao_km": v(vf["orbita_km"]), "criterio_selecao": cfg["criterio_selecao"],
                  "fracao_2_f269": (Im[1] + Nm[1]) / (sum(Im) + sum(Nm)), "fracao_2_p110": mv["verificacao"]["base"]["fracao_inerte_2"], "costa_publicada_s": v(vf["costa_publicada_s"]), "alvo_folga_m": a4["alvo_folga_m"], "casos": casos})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "inerte_solido.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def faixa(par, f=sg):
    a, b = par
    return f(a) if abs(a - b) < 5e-4 else f"{f(a)} a {f(b)}"


def escreve_md(o):
    aj = o["ajuste"]
    lim2 = (aj["b"] - 2 * aj["erro_padrao_b"], aj["b"] + 2 * aj["erro_padrao_b"])
    md = ["# Lei de massa inerte do MAV sólido (gerado por tools/inerte_solido.py)", "", "**NÃO VALIDADO.** Premissas P-014, P-019, P-108, P-110, P-111 e P-113 (nova, para aprovação).", "",
          "## Motores do catálogo [F270] (inerte total impresso, salvo o Orion 38)", "", "Critério: " + o["criterio_selecao"], "",
          "| Motor | Envelope | Propelente (kg) | Inerte (kg) | Inerte/propelente | Fator do resíduo | PDF p. |", "| :- | :- | -: | -: | -: | -: | -: |"]
    md += [f"| {m['nome']} | {m['envelope']} | {br(m['propelente_kg'], 1)} | {br(m['inerte_kg'], 1)} | {br(m['inerte_sobre_propelente'], 3)} | {br(m['residuo_fator'], 2)} | {m['pagina_pdf']} |" for m in o["motores"]]
    md += ["", f"Massas do catálogo em lbm; 1 lb = {br(o['lb_para_kg'], 7)} kg ([F112] p. 65 do PDF).", "",
           "## Ajuste", "",
           f"- Forma: potência, inerte = a · propelente^b, mínimos quadrados em ln, {aj['n']} motores de {br(aj['faixa_propelente_kg'][0], 1)} a {br(aj['faixa_propelente_kg'][1], 0)} kg de propelente.",
           f"- a = {br(aj['a'], 3)}, b = {br(aj['b'], 3)} (erro-padrão {br(aj['erro_padrao_b'], 3)}; ±2 erros-padrão: {br(lim2[0], 3)} a {br(lim2[1], 3)}).",
           f"- Erro do ajuste: fator rms {br(aj['fator_rms'], 2)} (resíduo rms em ln {br(aj['rms_ln'], 3)}); maior desvio, fator {br(aj['fator_max'], 2)}.",
           f"- Proporcional (b = 1, a forma da P-019 e da P-111): k = {br(aj['proporcional']['k'], 3)}, fator rms {br(aj['proporcional']['fator_rms'], 2)}, maior desvio {br(aj['proporcional']['fator_max'], 2)}.",
           "", "## Comparação no tamanho do MSR (kg)", "",
           "| Estágio | Propelente | Motor pelo catálogo | Motor do MSR [F269] | Não propulsivo do MSR | Estágio do MSR | P-019 | P-111 | Lei A | Lei B |", "| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
    md += [f"| {c['estagio']} | {br(c['propelente_kg'], 1)} | {br(c['catalogo_motor_kg'], 1)} | {br(c['msr_motor_kg'], 0)} | {br(c['msr_nao_propulsivo_kg'], 0)} | {br(c['msr_estagio_kg'], 0)} | {br(c['p019_estagio_kg'], 1)} | {br(c['p111_estagio_kg'], 1)} | {br(c['lei_A_estagio_kg'], 1)} | {br(c['lei_B_estagio_kg'], 1)} |" for c in o["comparacao_msr"]]
    linear = lim2[0] <= 1.0 <= lim2[1]
    md += ["", "## O que os dados sustentam", "",
           f"- **Escala.** A P-019 (k = {br(o['p019_k'], 3)} nos dois estágios) e a P-111 (k = {br(o['p111_k'][0], 3)} e {br(o['p111_k'][1], 3)}) são proporcionais: o inerte cresce como o propelente (b = 1). "
           + ("O catálogo é compatível com b = 1 dentro de ±2 erros-padrão." if linear else f"O catálogo dá b = {br(aj['b'], 2)}, e b = 1 fica fora de ±2 erros-padrão: **para o motor, os dados não sustentam a escala proporcional de nenhuma das duas**; ao crescer, a fração inerte do motor cai. Para o estágio inteiro, isso depende também de como cresce o inerte não propulsivo, que não tem fonte (a P-113 o fixa). O catálogo junta projetos diferentes: a dispersão entre eles não é a escala de um único projeto."),
           "- **Erro-padrão.** Supõe resíduos independentes; há variantes do mesmo motor (STAR 26/26B/26C, 30BP/30C/30C-BP/30E, 37FM/37FMV), então o erro-padrão está subestimado. A distância de b a 1 é de " + f"{br((1 - aj['b']) / aj['erro_padrao_b'], 1)} erros-padrão.",
           "- **Nível.** No tamanho do MSR, o motor do catálogo é mais leve que o motor do MSR [F269] (tabela acima). A verificação da P-110 reproduz o inerte total do MSR e a órbita publicada, não a divisão por estágio: a P-111 dá " + f"{br(o['comparacao_msr'][0]['p111_estagio_kg'], 1)} e {br(o['comparacao_msr'][1]['p111_estagio_kg'], 1)} kg, contra {br(o['comparacao_msr'][0]['msr_estagio_kg'], 0)} e {br(o['comparacao_msr'][1]['msr_estagio_kg'], 0)} kg do [F269]. A P-019 dá outra divisão. Nenhuma das duas separa o inerte não propulsivo (aviônica, RCS, estrutura da carga), que o [F269] dá à parte.",
           "- **Conflito com a P-110 (não resolvido aqui).** A justificativa da P-110 diz que a divisão do inerte por estágio não tem fonte; o [F269] publica uma (fração do estágio 2 = " + f"{br(o['fracao_2_f269'], 3)}, contra {br(o['fracao_2_p110'], 2)} escolhida pela verificação da P-110). Com o modelo de subida e o guiamento atuais, a divisão do [F269] não chega à órbita publicada (variante A, abaixo). A P-110 não foi mudada; a decisão é do Fabio.",
           "- **Proposta (P-113, NÃO VALIDADA, para aprovação):** inerte do estágio = N + c · P^b, com b do catálogo e N, o não propulsivo do [F269], fixo. Duas variantes do nível c: A, pelo motor do MSR [F269]; B, pela divisão que a verificação da P-110 escolheu. A escolha é do Fabio.",
           "", f"## Subida com cada variante (modelo de subida do sólido; tolerância {o['tol_custo']:.0e}, passo da varredura {br(o['passo'], 2)}, os da P-110)".replace(".0e", "e"), ""]
    for c in o["casos"]:
        vf = c["verificacao"]
        md += [f"### Lei {c['lei']}", "",
               f"- N = {br(c['N_kg'][0], 0)} e {br(c['N_kg'][1], 0)} kg; c = {br(c['c'][0], 3)} e {br(c['c'][1], 3)}; b = {br(c['b'], 3)}." + (" O c da variante A é calibrado no propelente do [F269] (216 e 54 kg) e aplicado ao do MSR usado no estudo (216 e 54,4 kg, config/cad.yaml), daí o estágio 2 com um pouco mais que 48 kg." if c["lei"].startswith("A") else ""),
               f"- Verificação com o MAV do MSR (órbita publicada de {br(o['orbita_verificacao_km'], 0)} km): inertes {br(vf['inertes_kg'][0], 1)} e {br(vf['inertes_kg'][1], 1)} kg; órbita {br(vf['periapse_km'], 0)} × {br(vf['apoapse_km'], 0)} km; costa {br(vf['costa_s'], 0)} s (publicada {br(o['costa_publicada_s'], 0)} s); "
               + ("**chega à órbita publicada**." if vf["fecha"] else f"**não chega à órbita publicada** (resíduo {vf['custo']:.1e}).".replace(".", ",", 1))]
        if not c["fecha_na_varredura"]:
            md += [f"- {br(o['altitude_km'], 0)} km: não fecha na varredura da P-110.", ""]
            continue
        md += ["", f"| Caso, {br(o['altitude_km'], 0)} km | Escala | Capacidade (m/s) | GLOM (kg) | Propelente (kg) | Inertes (kg) | Órbita simulada (km) | Chega? | Comprimento (m) | 4,65 m com deck | 4,65 m sem deck | 4,5 m com deck |",
               "| :- | -: | -: | -: | -: | -: | :- | :- | -: | -: | -: | -: |"]
        for rot, k in (("sem margem (o menor que chega)", "sem_margem"), ("com a margem da P-014 na capacidade", "com_margem")):
            y = c[k]
            md.append(f"| {rot} | {br(y['escala'], 3)} | {br(y['capacidade_m_s'], 0)} | {br(y['glom_kg'], 1)} | {br(y['propelente_kg'][0], 1)} + {br(y['propelente_kg'][1], 1)} | {br(y['inertes_kg'][0], 1)} + {br(y['inertes_kg'][1], 1)} | "
                      f"{br(y['voo']['periapse_km'], 0)} × {br(y['voo']['apoapse_km'], 0)} | {'sim' if y['voo']['fecha'] else 'não'} | {faixa(y['comprimento_m'], lambda z: br(z, 2))} | {faixa(y['folga_465_com_deck_m'])} | {faixa(y['folga_465_sem_deck_m'])} | {faixa(y['folga_45_com_deck_m'])} |")
        md.append("")
    if all(c["fecha_na_varredura"] for c in o["casos"]):
        md += ["As duas variantes fecham a 380 km com o passo e a tolerância da P-110: não foi preciso refiná-los.", ""]
    md += [f"Alvo de folga: {sg(o['alvo_folga_m'], 2)} m. O caso com a margem foi simulado com o mesmo guiamento (subida vertical, tangente linear, costa e queima do estágio 2 antes do apoapse): o sólido não regula o empuxo, então a capacidade a mais só chega à órbita de {br(o['altitude_km'], 0)} km se o guiamento conseguir gastá-la; \"não\" na coluna \"Chega?\" quer dizer que ele passa da órbita com esse guiamento, não que falta Δv."]
    (SAIDA / "inerte_solido.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
