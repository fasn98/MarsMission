"""Etapa 7.2, portão: alternativas para os bocais do estágio 1 do MAV (dados para a decisão do Fabio; não escolhe).

Para cada alternativa: se as saídas cabem no diâmetro (círculo mínimo de n círculos iguais), empuxo/peso em Marte, efeito
do Isp no Δv do estágio com as massas atuais, comprimento do motor contra a P-086 e folga do MAV deitado no aeroshell.
Nada é redimensionado, e nenhuma premissa muda. Geometria dos motores: [F228], em config/cad.yaml.
Saída: results/etapa7.2/bocais_alternativas.yaml e .md

Uso: python tools/bocais_estagio1.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital import motores as om  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"
POL = 0.0254   # [F112] Apêndice B.8, PDF p. 62: polegada em metros
FATOR = {1: 1.0, 2: 2.0, 3: 1 + 2 / math.sqrt(3), 4: 1 + math.sqrt(2)}   # círculo mínimo de n círculos iguais, sobre o diâmetro


def br(x, n=3):
    return f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def sg(x, n=2):
    return f"{round(x, n) + 0.0:+,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def main():
    cad, por, ma = ler("config/cad.yaml"), ler("results/etapa7.2/portao_decisao.yaml"), ler("results/etapa7.2/mav_arranjo.yaml")
    q = ler("results/etapa3.1/queima_finita.yaml")
    est = ler("results/etapa2.5/arquitetura.yaml")["lander"]["mav"]["estagios"][0]
    cat = om.catalogo()
    g = q["g_marte_m_s2"]
    rd, ge = cad["r4d11_variantes"], cad["motores_geometria_mav"]
    frente = v(rd["a_frente_da_flange_pol"])
    d_mav = v(cad["mav"]["diametro_opcoes_m"][cad["escolha"]["mav_diametro"]])
    t_par = v(cad["mav"]["espessura_parede_m"])
    p086 = v(cad["mav"]["comprimento_nao_tanque_m"]["motores_estagio_1"])
    varredura = [c["diametro_m"] for c in ma["casos"]]

    def r4d(k):
        return {"motor": "R-4D-11", "variante": k, "saida_m": rd[k]["diametro_saida_pol"] * POL, "comprimento_motor_m": (rd[k]["flange_a_saida_pol"] + frente) * POL, "fonte": rd[k]["fonte"]}

    def outro(m):
        x = ge[m]
        return {"motor": m, "variante": x["expansao"], "saida_m": x["diametro_saida_pol"] * POL, "comprimento_motor_m": sum(x["comprimento_pol"]) * POL, "fonte": x["fonte"]}
    alts = [("A", "4 × R-4D-11 164:1, Ø maior (a combinação atual)", r4d("164:1"), 4, cat["R-4D-11"]["isp_s"]), ("B", "4 × R-4D-11 44:1", r4d("44:1"), 4, None),
            ("C", "2 × R-4D-11 164:1", r4d("164:1"), 2, cat["R-4D-11"]["isp_s"]), ("D", "3 × R-4D-11 164:1", r4d("164:1"), 3, cat["R-4D-11"]["isp_s"]),
            ("E", "2 × R-42 (M1)", outro("R-42"), 2, cat["R-42"]["isp_s"]), ("F", "1 × R-40B (M3)", outro("R-40B"), 1, cat["R-40B"]["isp_s"])]
    empuxo_cat = {"R-4D-11": cat["R-4D-11"]["empuxo_n"], "R-42": cat["R-42"]["empuxo_n"], "R-40B": cat["R-40B"]["empuxo_n"]}
    linhas = []
    for id_, nome, m, n, isp in alts:
        minimo = FATOR[n] * m["saida_m"]
        empuxo = n * empuxo_cat[m["motor"]]
        de_sweep = next((d for d in varredura if d >= minimo), None)
        de_parede = next((d for d in varredura if d - 2 * t_par >= minimo), None)
        delta_l = max(0.0, m["comprimento_motor_m"] - p086)
        fol = []
        for d in dict.fromkeys(x for x in ([d_mav] if minimo <= d_mav else []) + [de_sweep, de_parede] if x is not None):
            caso = next(c for c in ma["casos"] if c["diametro_m"] == d)
            pega = lambda forma: next(x for x in por["linhas"] if x["forma"] == forma and x["diametro_m"] == d and x["orientacao"] == "deitado" and x["estacao"] == "ombro")["folga_m"]  # noqa: E731
            # folga deitado = (disponível − comprimento) / 2: o motor mais longo que a P-086 tira a metade do excesso
            fol.append({"diametro_m": d, "comprimento_m": caso["comprimento_m"] + delta_l, "variacao_massa_tanques_kg": caso["variacao_massa_tanques_kg"],
                        "folga_4_5_m": pega("msl_m2020") - delta_l / 2, "folga_4_65_m": pega("srl_a") - delta_l / 2})
        linhas.append({"id": id_, "nome": nome, **{k: m[k] for k in ("motor", "variante", "saida_m", "comprimento_motor_m", "fonte")}, "n": n,
                       "circulo_minimo_m": minimo, "cabe_em_d_mav": minimo <= d_mav, "cabe_em_d_mav_com_parede": minimo <= d_mav - 2 * t_par,
                       "menor_d_varredura_m": de_sweep, "menor_d_varredura_com_parede_m": de_parede, "empuxo_n": empuxo, "empuxo_peso_marte": empuxo / (est["massa_inicial_kg"] * g),
                       "isp_s": isp, "variacao_dv_estagio_m_s": (1e3 * est["dv_km_s"] * (isp / est["isp_s"] - 1)) if isp else None,
                       "excesso_sobre_p086_m": delta_l, "sobra_na_p086_m": p086 - m["comprimento_motor_m"], "folgas": fol})
    fontes_massa = {m: {"catalogo_massa_kg": cat[m]["massa_kg"], "f228_massa_kg": ge[m]["massa_kg"], "catalogo_isp_s": cat[m]["isp_s"], "f228_isp_s": ge[m]["isp_s"], "producao": ge[m]["producao"]} for m in ge}
    out = nativo({"gerado_por": "tools/bocais_estagio1.py", "diametro_mav_m": d_mav, "espessura_parede_m": t_par, "p086_motores_estagio_1_m": p086, "g_marte_m_s2": g,
                  "isp_dimensionamento_s": est["isp_s"], "dv_estagio_1_m_s": 1e3 * est["dv_km_s"], "m0_kg": est["massa_inicial_kg"], "maior_d_varredura_m": varredura[-1], "aeroshell": {k: por["aeroshell"][k]["rotulo"] for k in ("msl_m2020", "srl_a")}, "decisoes": cad["bocais_decisoes"], "alternativas": linhas, "motores": fontes_massa})
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "bocais_alternativas.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    d, t, dec = o["diametro_mav_m"], o["espessura_parede_m"], o["decisoes"]
    rot = lambda i: f" ({dec[i]['situacao']})" if i in dec else ""  # noqa: E731
    md = ["# Portão da 7.2: alternativas para os bocais do estágio 1 do MAV (gerado por tools/bocais_estagio1.py)", "",
          "Esta página não escolhe, e nenhuma premissa muda. Nada foi redimensionado: as massas são as atuais. A decisão é do Fabio.", "",
          "**Decisões do Fabio (2026-11-04):**",
          f"- **C: {dec['C']['situacao']}.** Empuxo/peso de {br(next(a['empuxo_peso_marte'] for a in o['alternativas'] if a['id'] == 'C'), 2)}, abaixo de 1 em Marte.",
          f"- **F: {dec['F']['situacao']}.** {dec['F']['motivo']}: {dec['F']['fonte']}.", "",
          "## 1. Cabe, e sobe?", "",
          f"Saídas em círculo mínimo, sem folga entre elas. \"Com parede\" desconta {br(t, 2)} m de cada lado, a parede que a P-085 define para os tanques, aqui estendida à região dos motores. Empuxo/peso em Marte com {br(o['m0_kg'], 1)} kg e g = {br(o['g_marte_m_s2'], 3)} m/s². "
          f"Δv: efeito só do Isp no estágio 1 ({br(o['dv_estagio_1_m_s'], 0)} m/s a {br(o['isp_dimensionamento_s'], 0)} s), com as mesmas massas.", "",
          "| Opção | Variante | Saída (m) | Círculo mínimo (m) | " + f"Cabe em Ø {br(d, 2)} m? | Empuxo/peso | Isp do catálogo (s) | Variação do Δv (m/s) | Motor (m) | Além da P-086 (m) |", "| :- | :- | -: | -: | :- | -: | -: | -: | -: | -: |"]
    for a in o["alternativas"]:
        cabe = ("sim" if a["cabe_em_d_mav_com_parede"] else "só sem parede") if a["cabe_em_d_mav"] else "não"
        isp = br(a["isp_s"], 0) if a["isp_s"] else "não dado"
        dv = sg(a["variacao_dv_estagio_m_s"], 0) if a["isp_s"] else "não calculável"
        md.append(f"| {a['id']}{rot(a['id'])}: {a['nome']} | {a['variante']} | {br(a['saida_m'])} | {br(a['circulo_minimo_m'])} | {cabe} | {br(a['empuxo_peso_marte'], 2)} | {isp} | {dv} | {br(a['comprimento_motor_m'])} | {br(a['excesso_sobre_p086_m'])} |")
    md += ["", "## 2. Folga do MAV deitado, com a base no ombro", "",
           "Mesma conta de results/etapa7.2/portao_decisao.md, menos a metade do que o motor passa da P-086. Motor mais curto que a P-086 não dá crédito, porque ela não muda aqui. "
           "Folga em m; positivo = cabe nesta estação, a mais favorável; nas outras estações ela é menor (portao_decisao.md). Os diâmetros são pontos da varredura.", "",
           "| Opção | Ø (m) | Comprimento (m) | Tanques, variação de massa (kg) | " + f"{o['aeroshell']['msl_m2020']} | {o['aeroshell']['srl_a']} |", "| :- | -: | -: | -: | -: | -: |"]
    for a in o["alternativas"]:
        if not a["folgas"]:
            md.append(f"| {a['id']} | fora da varredura (até {br(o['maior_d_varredura_m'], 2)} m) | — | — | — | — |")
        for f in a["folgas"]:
            md.append(f"| {a['id']}{rot(a['id'])} | {br(f['diametro_m'], 2)} | {br(f['comprimento_m'])} | {sg(f['variacao_massa_tanques_kg'], 1)} | {sg(f['folga_4_5_m'], 3)} | {sg(f['folga_4_65_m'], 3)} |")
    al = {a["id"]: a for a in o["alternativas"]}
    A, B, C, D, E, F = (al[k] for k in "ABCDEF")
    md += ["", "## 3. Prós e contras", "", "| Opção | Prós | Contras |", "| :- | :- | :- |",
           f"| A | mantém o motor e o Isp da variante do Orion ([F107] p. 5, motor \"modified\") | muda o Ø do ADR 0022: mínimo de {br(A['circulo_minimo_m'])} m sem parede, {br(A['circulo_minimo_m'] + 2 * t)} m com parede; {br(A['menor_d_varredura_m'], 2)} e {br(A['menor_d_varredura_com_parede_m'], 2)} m pela varredura |",
           f"| B | cabe em Ø {br(d, 2)} m, e o motor é {br(B['sobra_na_p086_m'])} m mais curto que a P-086 | [F228] não dá Isp nem massa do 44:1, então a perda não é calculável (na folha, o Isp sobe do 164:1 para o 300:1); disponibilidade não conferida: a folha só cita o 44:1 no desenho, e \"Expansion Ratio\" lista 164:1 e 300:1; o empuxo/peso supõe o mesmo empuxo das outras variantes (não conferido) |",
           f"| C ({dec['C']['situacao']}) | cabe em Ø {br(d, 2)} m, por {br(d - C['circulo_minimo_m'])} m, só sem parede | **empuxo/peso de {br(C['empuxo_peso_marte'], 2)}, abaixo de 1: não decola na vertical** |",
           f"| D | empuxo/peso de {br(D['empuxo_peso_marte'], 2)} | não cabe; o empuxo quase não vence o peso; Ø de {br(D['menor_d_varredura_m'], 2)} m pela varredura |",
           f"| E | em produção, combinação já no catálogo | pior no diâmetro: pede {br(E['circulo_minimo_m'])} m, além da varredura; motor {br(E['excesso_sobre_p086_m'])} m além da P-086 |",
           f"| F ({dec['F']['situacao']}) | cabe em Ø {br(d, 2)} m com sobra de {br(d - F['circulo_minimo_m'])} m; maior empuxo/peso, {br(F['empuxo_peso_marte'], 2)} | fora de produção; {sg(F['variacao_dv_estagio_m_s'], 0)} m/s pelo Isp; motor {br(F['excesso_sobre_p086_m'])} m além da P-086; um só motor, sem redundância e com controle de atitude a definir |",
           "", "## 4. Diferenças entre fontes (nada foi trocado)", "", "O R-4D-11 está em portao_decisao.md, seção 7.", "", "| Motor | Massa no catálogo [F106] (kg) | Massa em [F228] (kg) | Isp no catálogo (s) | Isp em [F228] (s) | Situação em [F228] |", "| :- | -: | -: | -: | -: | :- |"]
    for k, m in o["motores"].items():
        md.append(f"| {k} | {br(m['catalogo_massa_kg'], 2)} | {br(m['f228_massa_kg'], 2)} | {br(m['catalogo_isp_s'], 0)} | {br(m['f228_isp_s'], 0)} | {m['producao']} |")
    md += ["", "## 5. Não calculado", "",
           "- **Redimensionamento:** nenhuma opção fechou de novo a massa. O Δv acima é só o efeito do Isp, e os motores de outra massa não entraram.",
           "- **Saídas escalonadas no eixo ou bocais além do corpo:** o contorno dos bocais não é publicado com cotas suficientes.",
           "- **Base alargada só na região dos motores:** muda a folga no aeroshell de um jeito que esta conta não representa.",
           "- **Controle de atitude:** não está modelado em nenhuma opção. No estudo de Bowles, um só motor usa \"a single gimbaled engine with pneumatic thrust vectoring control\" ([F46] PDF p. 30).",
           "- **Estágio 2:** não entra aqui; a questão do comprimento dele está na seção 7 de portao_decisao.md.", "",
           "## 6. Fontes da geometria", ""]
    vistos = set()
    for a in o["alternativas"]:
        if a["fonte"] not in vistos:
            vistos.add(a["fonte"])
            md.append(f"- {a['motor']} {a['variante']}: {a['fonte']}")
    (SAIDA / "bocais_alternativas.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
