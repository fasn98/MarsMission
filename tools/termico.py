"""Etapa 4.2: controle térmico. Faixas de temperatura dos itens críticos, aquecimento por modo e efeito no orçamento.

- Faixas com fonte (config/termico.yaml): propelentes, baterias, amostras; o MAV do estudo pelo config do MAV (P-027).
- Lander na superfície: aquecimento do MAV (modelo atual, orbital.mav) com o alvo atual e com alvos da prática de
  sistemas MMH/NTO [F159, F160]; efeito na carga de sobrevivência e na área da opção C + RHU (linha de base, ADR 0015).
  Comparação com o projeto publicado do Sample Retrieval Lander [F164, F166, F170].
- Amostras: margem entre a temperatura do MAV e a AFT das amostras [F167].
- Cruzeiro: calor das RHUs dentro do aeroshell (pendência do 2º portão da 4.1) contra MER, SRL e MSL [F165, F168, F169].
- Orbitador: os aquecedores estão dentro da potência da plataforma (P-053); referência do MRO [F171].
Saída: results/etapa4.2/termico.yaml e .md

Uso: python tools/termico.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa4.2"


def main():
    tc, mc = ler("config/termico.yaml"), ler("config/mav_propulsao.yaml")
    en = ler("results/etapa4.1/energia.yaml")
    la = en["lander"]
    aq = mc["aquecimento"]
    op = ler("results/etapa2.2/mav_propulsao.yaml")["melhor_opcao"]
    t_amb, t_mav = v(aq["t_ambiente_c"]), v(aq["t_minima_c"][op])
    p_mav, hsol = la["demanda"]["aquecimento_mav_w"], la["demanda"]["aquecimento_mav_wh_sol"] / la["demanda"]["aquecimento_mav_w"]

    faixas = [dict(x) for x in tc["faixas"]]
    faixas.append({"item": f"MAV {op} do estudo (aquecido)", "tipo": "alvo do aquecimento (P-027)", "min_c": t_mav, "max_c": None,
                   "fonte": "config/mav_propulsao.yaml, aquecimento.t_minima_c"})

    # aquecimento do MAV: P ∝ (T − T_amb) no modelo atual (P-027), mesma área e mesmo ambiente
    vr = la["variante_rhu"]
    sob, c = vr["sobrevivencia"], vr["opcao"]
    base_area_por_sobrevivencia = c["dimensiona_area"] == "sobrevivência"
    alvos = [{"alvo": "atual (P-027)", "t_c": t_mav, "fonte": "config/mav_propulsao.yaml"}]
    alvos += [{"alvo": k, "t_c": v(x), "fonte": x["fonte"]} for k, x in tc["mav"]["alvos_alternativos_c"].items()]
    for a in alvos:
        p = p_mav * (a["t_c"] - t_amb) / (t_mav - t_amb)
        carga = sob["total_wh_sol"] - sob["mav_wh_sol"] + p * hsol
        a.update({"potencia_w": p, "energia_wh_sol": p * hsol, "carga_sobrevivencia_wh_sol": carga,
                  # a área da sobrevivência é linear na carga (mesmo cenário e mesmo pior sol, tools/energia.py)
                  "area_sobrevivencia_m2": vr["dimensionamento_sobrevivencia"]["area_m2"] * carga / sob["total_wh_sol"]})
        a["area_opcao_m2"] = max(a["area_sobrevivencia_m2"], la["solar"][0]["area_m2"])
        a["demanda_operacao_wh_sol"] = la["demanda"]["total_wh_sol"] - la["demanda"]["aquecimento_mav_wh_sol"] + p * hsol

    # amostras: AFT fora de transientes [F167] contra o alvo do MAV
    aft_amostras = next(x["max_c"] for x in tc["faixas"] if x["item"].startswith("Amostras (RSTA), fora"))
    amostras = {"aft_c": aft_amostras, "mav_c": t_mav, "excesso_k": t_mav - aft_amostras,
                "excesso_com_alvos_k": {a["alvo"]: a["t_c"] - aft_amostras for a in alvos[1:]}}

    # comparação com o SRL (projeto publicado): energia de aquecimento por sol, sem o MAV
    cs = tc["comparacao_srl"]
    nosso_sem_mav = sob["aquecedores_lander_wh_sol"]
    srl = {"lamp_e_bateria_aquecedores_wh_sol": v(cs["lamp_sobrevivencia_wh_sol"]) + v(cs["bateria_aquecedor_wh_sol"]),
           "lamp_frio_total_wh_sol": v(cs["lamp_frio_wh_sol"]), "mav_sobrevivencia_w": v(cs["mav_sobrevivencia_w"]),
           "mav_operacao_w": [cs["mav_operacao_w"]["min"], cs["mav_operacao_w"]["max"]],
           "nosso_aquecedores_lander_wh_sol": nosso_sem_mav, "nosso_rhu_w": sob["rhu_lander_w"], "nosso_rhu_wh_sol": sob["rhu_lander_w"] * hsol,
           "nosso_total_wh_sol": nosso_sem_mav + sob["rhu_lander_w"] * hsol, "nosso_mav_w": p_mav}
    srl["razao_nosso_srl"] = srl["nosso_total_wh_sol"] / srl["lamp_e_bateria_aquecedores_wh_sol"]

    # cruzeiro: RHUs dentro do aeroshell
    cz = tc["cruzeiro"]
    rhu_w = vr["rhu_quantidade"] * vr["rhu_w_cada"]
    msl_par = v(cz["msl_mmrtg_termica_w"]) * v(cz["msl_fracao_parasita"])
    cruzeiro = {"rhu_quantidade": vr["rhu_quantidade"], "rhu_w": rhu_w,
                "srl_perda_passiva_max_w": v(cz["srl_perda_passiva_max_w"]), "fracao_do_srl_passivo": rhu_w / v(cz["srl_perda_passiva_max_w"]),
                "mer_dissipacao_w": v(cz["mer_dissipacao_w"]), "fracao_do_mer": rhu_w / v(cz["mer_dissipacao_w"]),
                "msl_parasita_w": msl_par, "fracao_do_msl_parasita": rhu_w / msl_par}

    orb = en["orbitador"]
    orbitador = {"mro_aquecedores_w": v(tc["orbitador"]["mro_aquecedores_w"]), "plataforma_w_por_modo":
                 {m["modo"]: m["carga_w"] for m in orb["modos"]}, "carga_adotada_w": orb["adotada"]["carga_w"]}

    out = {"gerado_por": "tools/termico.py", "mav_opcao": op, "ambiente_mav_c": t_amb,
           "jezero_noite_solo_c": v(tc["ambiente"]["jezero_noite_solo_k"]) - 273.15,
           "faixas": faixas, "aquecimento_mav": alvos, "area_base_dimensionada_pela_sobrevivencia": base_area_por_sobrevivencia,
           "amostras": amostras, "comparacao_srl": srl, "cruzeiro": cruzeiro, "orbitador": orbitador}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "termico.yaml").write_text(yaml.safe_dump(nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    br = lambda x, n=0: "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    md = ["# Controle térmico (gerado por tools/termico.py)", "", "## Faixas de temperatura dos itens críticos (°C)", "",
          "| Item | Tipo | Mínimo | Máximo | Fonte |", "| :- | :- | -: | -: | :- |"]
    md += [f"| {f['item']} | {f['tipo']} | {br(f['min_c'], 1)} | {br(f['max_c'], 1)} | {f['fonte'].split(' ')[0] if f['fonte'].startswith('[') else f['fonte']} |" for f in o["faixas"]]
    md += ["", f"Ambiente do modelo de aquecimento do MAV: {br(o['ambiente_mav_c'], 1)} °C (igloo do SRL [F57]); "
           f"mínima noturna do solo em Jezero: cerca de {br(o['jezero_noite_solo_c'])} °C [F172].", "",
           "## Aquecimento do MAV e efeito no orçamento de energia do lander (C + RHU)", "",
           "O aquecimento escala com (T − T_ambiente) no modelo atual (P-027). A área da sobrevivência é linear na carga "
           "(mesmo cenário, tools/energia.py); a da opção é a maior entre ela e a de operação com céu claro.", "",
           "| Alvo do MAV | T (°C) | Potência (W) | Wh/sol | Sobrevivência (Wh/sol) | Área da opção (m²) | Demanda em operação (Wh/sol) |",
           "| :- | -: | -: | -: | -: | -: | -: |"]
    md += [f"| {a['alvo']} | {br(a['t_c'])} | {br(a['potencia_w'], 1)} | {br(a['energia_wh_sol'])} | {br(a['carga_sobrevivencia_wh_sol'])} | "
           f"{br(a['area_opcao_m2'], 1)} | {br(a['demanda_operacao_wh_sol'])} |" for a in o["aquecimento_mav"]]
    am, s, cz, ob = o["amostras"], o["comparacao_srl"], o["cruzeiro"], o["orbitador"]
    md += ["", "## Amostras", "",
           f"AFT das amostras fora de transientes: {br(am['aft_c'])} °C [F167]. O MAV do estudo é aquecido a {br(am['mav_c'])} °C: "
           f"{br(am['excesso_k'])} K acima da AFT das amostras; com os alvos alternativos, "
           + ", ".join(f"{k} {br(x)} K" for k, x in am["excesso_com_alvos_k"].items()) + ".", "",
           "## Comparação com o projeto publicado do SRL (análise, não medida)", "",
           f"- Aquecedores de sobrevivência do LAMP e da bateria no caso frio: {br(s['lamp_e_bateria_aquecedores_wh_sol'])} Wh/sol; "
           f"energia total do LAMP no caso frio: {br(s['lamp_frio_total_wh_sol'])} Wh/sol [F166]. Aqui: aquecedores do lander "
           f"{br(s['nosso_aquecedores_lander_wh_sol'])} Wh/sol mais {br(s['nosso_rhu_w'], 1)} W de RHUs ({br(s['nosso_rhu_wh_sol'])} Wh/sol), "
           f"total {br(s['nosso_total_wh_sol'])} Wh/sol, {br(100 * s['razao_nosso_srl'])} % do SRL (P-056, ADR 0015). "
           "O SRL é outro veículo, no pior caso frio (Ls 72°), e a comparação não é verificação.",
           f"- MAV: sobrevivência do MAV sólido do SRL de cerca de {br(s['mav_sobrevivencia_w'])} W a −40 °C [F164]; operação a −20 °C "
           f"de {br(s['mav_operacao_w'][0])} a {br(s['mav_operacao_w'][1])} W [F170]. Aqui: {br(s['nosso_mav_w'], 1)} W (MAV líquido).", "",
           "## Cruzeiro: calor das RHUs dentro do aeroshell", "",
           f"{cz['rhu_quantidade']} RHUs, {br(cz['rhu_w'], 1)} W: {br(100 * cz['fracao_do_srl_passivo'])} % da perda passiva máxima do LAMP do SRL "
           f"({br(cz['srl_perda_passiva_max_w'])} W [F165]); {br(100 * cz['fracao_do_mer'])} % dos {br(cz['mer_dissipacao_w'])} W que o MER rejeitou "
           f"por HRS ativo [F168]; {br(100 * cz['fracao_do_msl_parasita'])} % dos {br(cz['msl_parasita_w'])} W da MMRTG que o MSL dissipou "
           f"parasitamente no backshell e no escudo [F169]. A dissipação das aviônicas do lander no cruzeiro não está no estudo.", "",
           "## Orbitador", "",
           f"Os aquecedores estão dentro da potência da plataforma por modo (P-053): "
           + ", ".join(f"{k} {br(x)} W" for k, x in ob["plataforma_w_por_modo"].items())
           + f". Referência: o MRO usa até {br(ob['mro_aquecedores_w'])} W em aquecedores [F171], sem divisão por modo."]
    (SAIDA / "termico.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
