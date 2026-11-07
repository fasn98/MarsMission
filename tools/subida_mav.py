"""Perda gravitacional na subida do MAV com o empuxo/peso real (portão da rota A, Fabio, 2026-11-07).

Para cada caso (base com o 164:1; rota A com o Isp calculado do 44:1, nos três valores de results/etapa7.2/isp_44.yaml), simula
a subida até 100 × 100 km (src/orbital/subida.py), troca o Δv de 100 × 100 km de [F37] pelo do caso e redimensiona o MAV até
convergir (GLOM, empuxo/peso, comprimento). O Δv do caso é o de [F37] somado à diferença entre a simulação do caso e a do veículo
de referência (empuxo/peso 2,5), com o mesmo modelo: o erro sistemático do modelo se cancela em parte. A simulação do veículo
de referência, comparada com [F37], é a verificação do modelo.
Saída: results/etapa7.2/subida_mav.yaml e .md

Uso: python tools/subida_mav.py
"""

from __future__ import annotations

import copy
import math
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import comprimento_mav as cmv  # noqa: E402
import rota_a_dimensiona as rad  # noqa: E402
from orbital import motores as om  # noqa: E402
from orbital import subida as sb  # noqa: E402
from orbital import veiculos as ve  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"
POL = 0.0254   # [F112] Apêndice B.8, PDF p. 62: polegada em metros


def br(x, n=3):
    return f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def sg(x, n=3):
    return f"{round(x, n) + 0.0:+,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def contexto():
    sc, po, scfg = ler("config/subida.yaml"), ler("config/parametros_orbitais.yaml"), ler("config/superficie.yaml")
    atm = {k: v(x) for k, x in sc["atmosfera"].items()}
    pl = sb.Planeta(v(po["gm_marte"]) * 1e9, v(po["raio_marte_km"]) * 1e3, 2 * math.pi / v(scfg["marte"]["periodo_rotacao_s"]))
    nu = sc["numerico"]
    num = {"limites": [tuple(x) for x in nu["limites_guia"]["valor"]], "grade": {"t_v_s": nu["grade_t_v_s"]["valor"], "theta0_rad": nu["grade_theta0_rad"]["valor"], "c_1_s": nu["grade_c_1_s"]["valor"]}, "tol_m": v(nu["tol_altitude_m"]),
           "tol_m_s": v(nu["tol_vr_m_s"]), "tol_kg": v(nu["tol_glom_kg"]), "iter": int(v(nu["iteracoes_max"])), "varredura": nu["varredura_ponto_fixo_m_s"]["valor"], "integrador": nu["integrador"]["valor"]}
    return sc, scfg, atm, pl, num


def voo(ctx, estagios, area_cd):
    sc, _, atm, pl, num = ctx
    it = num["integrador"]
    return sb.otimiza(pl, estagios, area_cd, atm, v(sc["alvo_altitude_m"]), num["grade"], num["limites"], num["tol_m"], num["tol_m_s"], it["pontos_de_partida"], it)


def referencia(ctx, cd):
    sc, _, _, pl, _ = ctx
    r = sc["referencia"]
    m0 = v(r["massa_kg"])
    g = pl.mu / pl.raio ** 2
    est = [sb.Estagio(m0, m0, v(r["empuxo_peso"]) * m0 * g, v(r["isp_s"]))]
    x = voo(ctx, est, cd * v(r["area_m2"]))
    return {**x, "diferenca_para_f37_m_s": x["dv_m_s"] - v(r["dv_100x100_m_s"]), "dv_ideal_m_s": sb.dv_ideal(pl, v(sc["alvo_altitude_m"]))}


def veiculo(ctx, m, isp, empuxo_motor, dv100):
    """MAV dimensionado para o Δv de 100 × 100 km dado: (lander, estágios da simulação, empuxo/peso)."""
    _, scfg, _, pl, _ = ctx
    m2 = copy.deepcopy(m.mcfg)
    m2["opcoes"][m.op]["isp_s"] = [isp, isp]
    s2 = copy.deepcopy(scfg)
    s2["subida"]["dv_100x100_km_s"]["valor"] = dv100 / 1000.0
    lan = ve.lander(m.R + m.h0p, m.R + m.h0a, mcfg=m2, scfg=s2, detalhe=True)
    est = [sb.Estagio(e["massa_inicial_kg"], e["propelente_kg"], n * empuxo_motor, isp) for e, n in zip(lan["mav_estagios"], m.n_mot)]
    return lan, est, est[0].empuxo_n / (est[0].massa_inicial_kg * pl.mu / pl.raio ** 2)


def ponto_fixo(ctx, m, isp, empuxo_motor, cd, ref):
    """Varre o Δv de 100 × 100 km usado no dimensionamento e devolve o Δv que a simulação pede para esse MAV. Há ponto fixo
    onde a diferença troca de sinal; com empuxo/peso ≤ 1 o MAV não decola."""
    sc, _, _, _, num = ctx
    out = []
    for dv in num["varredura"]:
        lan, est, tw = veiculo(ctx, m, isp, empuxo_motor, dv)
        x = {"dv_100x100_usado_m_s": dv, "glom_kg": est[0].massa_inicial_kg, "empuxo_peso": tw}
        if tw <= 1.0:
            out.append({**x, "decola": False})
            break
        y = voo(ctx, est, cd * math.pi * m.d_alvo ** 2 / 4)
        pede = v(sc["referencia"]["dv_100x100_m_s"]) + y["dv_m_s"] - ref["dv_m_s"] if y else None
        out.append({**x, "decola": True, "dv_100x100_pedido_m_s": pede, "pedido_menos_usado_m_s": pede - dv if pede is not None else None})
    return out


def converge(ctx, m, isp, empuxo_motor, cd, ref):
    """Redimensiona o MAV até o GLOM convergir; devolve o caso final e o histórico."""
    sc, scfg, _, pl, num = ctx
    area = math.pi * m.d_alvo ** 2 / 4
    m2 = copy.deepcopy(m.mcfg)
    m2["opcoes"][m.op]["isp_s"] = [isp, isp]
    dv100 = v(sc["referencia"]["dv_100x100_m_s"])
    hist, glom_ant = [], None
    g = pl.mu / pl.raio ** 2
    for _ in range(num["iter"]):
        s2 = copy.deepcopy(scfg)
        s2["subida"]["dv_100x100_km_s"]["valor"] = dv100 / 1000.0
        lan = ve.lander(m.R + m.h0p, m.R + m.h0a, mcfg=m2, scfg=s2, detalhe=True)
        e_ = lan["mav_estagios"]
        est = [sb.Estagio(e["massa_inicial_kg"], e["propelente_kg"], n * empuxo_motor, isp) for e, n in zip(e_, m.n_mot)]
        x = voo(ctx, est, cd * area)
        glom = e_[0]["massa_inicial_kg"]
        hist.append({"glom_kg": glom, "empuxo_peso": est[0].empuxo_n / (glom * g), "dv_100x100_usado_m_s": dv100, "dv_simulado_m_s": x["dv_m_s"] if x else None})
        if x is None:
            tw = est[0].empuxo_n / (glom * g)
            return {"convergiu": False, "motivo": f"diverge: no passo {len(hist)}, GLOM de {br(glom, 1)} kg e empuxo/peso de {br(tw, 2)}" + (", abaixo de 1: o MAV não decola" if tw <= 1 else ": a simulação não chegou a 100 × 100 km"), "historico": hist}
        novo = v(sc["referencia"]["dv_100x100_m_s"]) + x["dv_m_s"] - ref["dv_m_s"]
        if glom_ant is not None and abs(glom - glom_ant) < num["tol_kg"]:
            return {"convergiu": True, "iteracoes": len(hist), "lander": lan, "estagios": e_, "voo": x, "dv_100x100_m_s": dv100, "glom_kg": glom,
                    "empuxo_peso": est[0].empuxo_n / (glom * g), "empuxo_peso_estagio_2": est[1].empuxo_n / (est[1].massa_inicial_kg * g),
                    "dv_subida_com_margem_km_s": (1 + v(ler("config/dimensionamento.yaml")["margem_dv"])) * lan["dv_subida_mav_km_s"], "historico": hist}
        glom_ant, dv100 = glom, novo
    return {"convergiu": False, "motivo": f"sem convergência em {num['iter']} iterações", "historico": hist}


def main():
    ctx = contexto()
    sc = ctx[0]
    m = rad.modelo()
    cal = ler("results/etapa7.2/isp_44.yaml")
    rd = ler("config/cad.yaml")["r4d11_variantes"]
    nt = {k: v(x) for k, x in ler("config/cad.yaml")["mav"]["comprimento_nao_tanque_m"].items()}
    nt164 = {**nt, "motores_estagio_1": (rd["164:1"]["flange_a_saida_pol"] + v(rd["a_frente_da_flange_pol"])) * POL, "motor_estagio_2": (rd["164:1"]["flange_a_saida_pol"] + v(rd["a_frente_da_flange_pol"])) * POL}
    f164 = om.catalogo()["R-4D-11"]["empuxo_n"]
    isp_base = float(m.mcfg["opcoes"][m.op]["isp_s"][0])
    cd0 = v(sc["arrasto"]["cd_base"])
    refs = {cd: referencia(ctx, cd) for cd in sc["arrasto"]["cd_varredura"]["valor"]}
    alvo = m.alvo
    casos = []
    defs = [("Base: R-4D-11 164:1, sem aninhar", isp_base, f164, "164:1")]
    defs += [(f"Rota A sem deck, Isp calculado {k}", cal["isp_44_s"][k], cal["empuxo_164_n"] * cal["fator_empuxo_por_caso"][k], "44:1") for k in ("baixo", "central", "alto")]
    for rot, isp, f_m, var in defs:
        c = converge(ctx, m, isp, f_m, cd0, refs[cd0])
        linha = {"rotulo": rot, "isp_s": isp, "empuxo_motor_n": f_m, "variante": var, **{k: c[k] for k in ("convergiu", "historico")}}
        if c["convergiu"]:
            e_ = c["estagios"]
            linha.update({k: c[k] for k in ("iteracoes", "glom_kg", "empuxo_peso", "empuxo_peso_estagio_2", "dv_100x100_m_s", "dv_subida_com_margem_km_s")})
            linha["voo"] = {k: c["voo"][k] for k in ("dv_m_s", "t_corte_s", "estagio_no_corte", "guia")}
            linha["massa_por_area_kg_m2"] = c["lander"]["massa_entrada_kg"] / (math.pi * v(ler("config/cad.yaml")["aeroshell"]["opcoes"]["m2020"]["diametro_m"]) ** 2 / 4)
            if var == "164:1":
                L = cmv.comprimento(m.d0, e_, nt164, m.cad)
                linha["comprimentos"] = {"sem aninhar": {"comprimento_m": L, "folga_sem_deck_m": (m.lim_ombro[m.d0] - L) / 2, "folga_com_deck_m": (m.lim_deck[m.d0] - L) / 2}}
            else:
                linha["limite_otimista_m"] = cmv.comprimento(m.d_alvo, e_, m.nt44, m.cad, aninhado=True)
                linha["comprimentos"] = {}
                for f in m.fams:
                    L = m.real(e_, m.d_alvo, m.g0, m.k_b, f)[0]
                    linha["comprimentos"][f] = {"comprimento_m": L, "folga_sem_deck_m": (m.lim_ombro[m.d_alvo] - L) / 2, "folga_com_deck_m": (m.lim_deck[m.d_alvo] - L) / 2}
        else:
            linha["motivo"] = c["motivo"]
            linha["ponto_fixo"] = ponto_fixo(ctx, m, isp, f_m, cd0, refs[cd0])
        casos.append(linha)
    # sensibilidade ao arrasto, no caso central da rota A
    sens = []
    for cd, ref in refs.items():
        c = converge(ctx, m, cal["isp_44_s"]["central"], cal["empuxo_164_n"] * cal["fator_empuxo_por_caso"]["central"], cd, ref)
        x = {"cd": cd, "referencia_dv_m_s": ref["dv_m_s"], "referencia_diferenca_m_s": ref["diferenca_para_f37_m_s"], "convergiu": c["convergiu"]}
        if c["convergiu"]:
            Ls = [m.real(c["estagios"], m.d_alvo, m.g0, m.k_b, f)[0] for f in m.fams]
            x.update({"glom_kg": c["glom_kg"], "dv_100x100_m_s": c["dv_100x100_m_s"], "melhor_folga_sem_deck_m": (m.lim_ombro[m.d_alvo] - min(Ls)) / 2, "pior_folga_sem_deck_m": (m.lim_ombro[m.d_alvo] - max(Ls)) / 2})
        sens.append(x)
    out = nativo({"gerado_por": "tools/subida_mav.py", "status": "NÃO VALIDADO", "alvo_folga_m": alvo, "cd_base": cd0,
                  "referencia": {**{k: refs[cd0][k] for k in ("dv_m_s", "diferenca_para_f37_m_s", "t_corte_s", "guia", "dv_ideal_m_s")}, "f37_m_s": v(sc["referencia"]["dv_100x100_m_s"]),
                                 **{k: v(sc["referencia"][k]) for k in ("empuxo_peso", "isp_s", "area_m2", "massa_kg")}},
                  "base_vigente_glom_kg": ler("results/etapa2.5/arquitetura.yaml")["lander"]["mav"]["estagios"][0]["massa_inicial_kg"],
                  "limites": {"diametro_m": m.d_alvo, "sem_deck_m": m.lim_ombro[m.d_alvo], "com_deck_m": m.lim_deck[m.d_alvo]}, "casos": casos, "sensibilidade_cd": sens})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "subida_mav.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    ref, alvo = o["referencia"], o["alvo_folga_m"]
    rot = [c for c in o["casos"] if c["variante"] == "44:1"]
    fecha = [(c["isp_s"], f) for c in rot if c["convergiu"] for f, x in c["comprimentos"].items() if x["folga_sem_deck_m"] >= alvo]
    total = sum(len(c.get("comprimentos", {})) for c in rot)
    md = ["# Subida do MAV com o empuxo/peso real (gerado por tools/subida_mav.py)", "",
          "**NÃO VALIDADO.** Simulação plana da subida até 100 × 100 km, com redimensionamento do MAV até convergir. Modelo em src/orbital/subida.py; premissas P-104 a P-107.", "",
          "## Resposta", "",
          ("**A iteração não convergiu na rota A:** ver a busca do ponto fixo abaixo. " if any(not c["convergiu"] for c in rot) else "") + (f"**A rota A sem deck continua com folga ≥ {sg(alvo, 2)} m em {len(fecha)} de {total} combinações de Isp e geometria**" if fecha else f"**A rota A sem deck NÃO fecha: nenhum MAV da rota A convergiu, então nenhuma geometria chega a folga ≥ {sg(alvo, 2)} m**")
          + (" (" + "; ".join(f"{br(i, 1)} s, {f}" for i, f in fecha) + ")." if fecha else ".") + " " + ("Todos os casos convergiram." if all(c["convergiu"] for c in o["casos"]) else "Há caso que não convergiu: ver a tabela."), "",
          "## Verificação do modelo contra [F37]", "",
          f"Veículo de referência, de um estágio, com empuxo/peso {br(ref['empuxo_peso'], 1)} ([F46] PDF p. 9), Isp {br(ref['isp_s'], 0)} s e área de {br(ref['area_m2'], 3)} m² ([F37]); massa de {br(ref['massa_kg'], 1)} kg (P-105); CD {br(o['cd_base'], 2)} (P-104). Simulado: **{br(ref['dv_m_s'], 1)} m/s**, contra {br(ref['f37_m_s'], 1)} m/s de [F37] Tab. 1: {sg(ref['diferenca_para_f37_m_s'], 1)} m/s ({sg(100 * ref['diferenca_para_f37_m_s'] / ref['f37_m_s'], 1)} %). O Δv ideal, sem perdas, é {br(ref['dv_ideal_m_s'], 1)} m/s. [F37] otimizou no POST II o ângulo de ataque, a inclinação e o próprio empuxo/peso de decolagem (PDF p. 20), com Mars-GRAM 2001 e com o Isp e a área de saída do motor; aqui o guiamento é linear-tangente, o empuxo é o de vácuo e a atmosfera é a de [F245]. Esse desvio entra só pela diferença entre casos, porque o Δv de cada caso é o de [F37] mais a diferença entre a simulação do caso e a da referência.", "",
          "## Casos, convergidos", "", "| Caso | Isp (s) | Empuxo por motor (N) | Iterações | GLOM (kg) | Empuxo/peso | Empuxo/peso do estágio 2 | Δv 100 × 100 km (m/s) | Δv de subida com margem (km/s) | Massa por área (kg/m²) |", "| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
    for c in o["casos"]:
        if c["convergiu"]:
            md.append(f"| {c['rotulo']} | {br(c['isp_s'], 1)} | {br(c['empuxo_motor_n'], 0)} | {c['iteracoes']} | {br(c['glom_kg'], 1)} | {br(c['empuxo_peso'], 2)} | {br(c['empuxo_peso_estagio_2'], 2)} | {br(c['dv_100x100_m_s'], 1)} | {br(c['dv_subida_com_margem_km_s'], 3)} | {br(c['massa_por_area_kg_m2'], 0)} |")
        else:
            md.append(f"| {c['rotulo']} | {br(c['isp_s'], 1)} | {br(c['empuxo_motor_n'], 0)} | não convergiu: {c['motivo']} | | | | | | |")
    md += ["", f"Antes, todos os casos usavam {br(ref['f37_m_s'], 1)} m/s. **A linha da base é só conferência e não foi aplicada:** o GLOM vigente segue {br(o['base_vigente_glom_kg'], 1)} kg (results/etapa2.5/arquitetura.yaml). A base sai com Δv menor que o de [F37] porque a referência tem massa por área bem menor que a do nosso MAV e porque a inserção direta penaliza mais o empuxo/peso alto da referência (ver Limitações).", ""]
    pfs = [c for c in o["casos"] if "ponto_fixo" in c]
    if pfs:
        md += ["## Busca do ponto fixo nos casos que não convergiram", "",
               "Para cada Δv de 100 × 100 km usado no dimensionamento, o Δv que a simulação pede para o MAV resultante. Há ponto fixo onde a diferença troca de sinal. Se a diferença é positiva em toda a varredura, até o empuxo/peso cair abaixo de 1, não há MAV que feche dentro da varredura.", "",
               "| Caso | Δv usado (m/s) | GLOM (kg) | Empuxo/peso | Δv pedido (m/s) | Pedido − usado (m/s) |", "| :- | -: | -: | -: | -: | -: |"]
        for c in pfs:
            for x in c["ponto_fixo"]:
                md.append(f"| {c['rotulo']} | {br(x['dv_100x100_usado_m_s'], 0)} | {br(x['glom_kg'], 1)} | {br(x['empuxo_peso'], 2)} | " + ((f"{br(x['dv_100x100_pedido_m_s'], 1)} | {sg(x['pedido_menos_usado_m_s'], 1)} |" if x["dv_100x100_pedido_m_s"] is not None else "não chegou | |") if x["decola"] else "não decola | |"))
            difs = [x["pedido_menos_usado_m_s"] for x in c["ponto_fixo"] if x.get("pedido_menos_usado_m_s") is not None]
            troca = any(a * b <= 0 for a, b in zip(difs, difs[1:])) or any(d_ <= 0 for d_ in difs)
            md.append(f"| **{c['rotulo']}** | **{'há troca de sinal: pode existir ponto fixo' if troca else 'sem ponto fixo na varredura'}** | | | | |")
        md += [""]
    md += [
           "## Comprimento e folga deitado", "", f"Limites em Ø {br(o['limites']['diametro_m'], 2)} m: {br(o['limites']['sem_deck_m'], 3)} m sem deck e {br(o['limites']['com_deck_m'], 3)} m com deck. Alvo de folga: {sg(alvo, 2)} m. A base usa o seu próprio Ø.", "",
           "| Caso | Geometria do estágio 2 | Comprimento (m) | Folga sem deck (m) | Folga com deck (m) |", "| :- | :- | -: | -: | -: |"]
    for c in o["casos"]:
        for f, x in c.get("comprimentos", {}).items():
            md.append(f"| {c['rotulo']} | {f} | {br(x['comprimento_m'])} | {sg(x['folga_sem_deck_m'])} | {sg(x['folga_com_deck_m'])} |")
    md += ["", "## Sensibilidade ao coeficiente de arrasto (rota A, Isp central)", "", "A referência é simulada de novo com o mesmo CD.", "",
           "| CD | Referência (m/s) | Referência − [F37] (m/s) | GLOM (kg) | Δv 100 × 100 km (m/s) | Folga sem deck, melhor e pior geometria (m) |", "| -: | -: | -: | -: | -: | -: |"]
    for x in o["sensibilidade_cd"]:
        md.append(f"| {br(x['cd'], 2)} | {br(x['referencia_dv_m_s'], 1)} | {sg(x['referencia_diferenca_m_s'], 1)} | " + (f"{br(x['glom_kg'], 1)} | {br(x['dv_100x100_m_s'], 1)} | {sg(x['melhor_folga_sem_deck_m'])} e {sg(x['pior_folga_sem_deck_m'])} |" if x["convergiu"] else "não convergiu | | |"))
    md += ["", "## Limitações", "",
           "- **Viés:** a inserção direta penaliza mais o empuxo/peso alto da referência que o empuxo/peso baixo dos nossos casos, então o método do incremento subestima a penalidade do empuxo/peso baixo. A conclusão \"sem ponto fixo\" da rota A é, por isso, conservadora a favor da rota A (não conferido com outro modelo neste repositório).",
           "- Inserção direta, com queima contínua. Sem costa entre os estágios e sem queima de circularização separada: o MAV do MSR usa costa longa ([F57] PDF p. 2: \"the MAV remains in a coast period\"), que este modelo não explora.",
           "- Sem perda por pressão no bocal (empuxo no vácuo nos dois lados da diferença); a de [F37] está dentro dos 4.027,9 m/s.",
           "- Plano equatorial rumo leste, como [F37]; a latitude do sítio e a inclinação continuam no déficit de rotação de config/superficie.yaml.",
           "- Atmosfera de página educacional ([F245]); densidade zero acima de 80 km (P-106); CD constante (P-104).",
           "- A fração estrutural e a divisão de Δv entre os estágios são as de antes (P-019 e ε 0,230); a massa dos tanques da rota A não entra no GLOM.",
           "- O estágio 2 também faz a transferência até a órbita de encontro, que não é simulada: entra pelo Δv ideal, como antes."]
    (SAIDA / "subida_mav.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
