"""Etapa 4.6: integração da Fase 4 (subsistemas). Junta os números das Etapas 4.1 a 4.5 e da arquitetura vigente.

- Energia (4.1), térmico (4.2), comunicação (4.3), operação de superfície (4.4) e massas (4.5): lidos de results/.
- Massas e LEO dos veículos: orbital.veiculos sobre config/ (P-017 no caso B, circuito no estágio de cruzeiro; ADR 0019).
- Lançadores de base (ADR 0020): margem na base e a pior margem nas sensibilidades de results/etapa2.5/arquitetura.yaml.
- Premissas: contagem por status, criadas na Fase 4 (a partir da P-050) e críticas.
Saída: results/fase4/resumo.yaml e .md

Uso: python tools/fase4.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import arquitetura as arq  # noqa: E402
from orbital import veiculos as ve  # noqa: E402
from orbital.config import ler, nativo  # noqa: E402

SAIDA = RAIZ / "results" / "fase4"
from lista_premissas import PRIMEIRA_DA_FASE_4  # noqa: E402


def main():
    lcfg = ler("config/lancadores.yaml")
    en, te = ler("results/etapa4.1/energia.yaml"), ler("results/etapa4.2/termico.yaml")
    co, op = ler("results/etapa4.3/comunicacao.yaml"), ler("results/etapa4.4/operacao_superficie.yaml")
    lm, ar = ler("results/etapa4.5/lista_massas.yaml"), ler("results/etapa2.5/arquitetura.yaml")

    vei, jan, _ = ve.veiculos()
    o, la = vei["orbitador_regra_iii"], vei["lander"]
    mg = arq.margens(vei, jan, lcfg)
    base = lcfg["base"]
    # pior margem de cada lançador de base nas sensibilidades da arquitetura (uma premissa por vez)
    sens = ar["sensibilidade"]

    def pior(veic, nome):
        x = min(sens, key=lambda c: c["margens"][veic][nome])
        return {"margem": x["margens"][veic][nome], "caso": x["caso"]}

    lancadores = {
        "orbitador": {"lancador": base["orbitador"], "margem_base": mg["orbitador"][base["orbitador"]], "pior": pior("orbitador", base["orbitador"])},
        "lander": {"lancador": base["lander"], "margem_base": mg["lander"][base["lander"]], "pior": pior("lander", base["lander"])},
        "lander_reserva": {"lancador": base["lander_reserva"], "margem_base": mg["lander"][base["lander_reserva"]],
                           "pior": pior("lander", base["lander_reserva"])},
        "todas_as_margens_base": mg,
    }
    massas = {"orbitador_injetado_kg": o["injetada_kg"], "orbitador_leo_kg": o["leo_modelo_kg"],
              "lander_injetado_kg": la["injetada_kg"], "lander_leo_kg": la["leo_modelo_kg"],
              "total_leo_kg": o["leo_modelo_kg"] + la["leo_modelo_kg"],
              "lander_entrada_kg": la["massa_entrada_kg"], "lander_pousado_kg": la["massa_pousada_kg"],
              "plataforma_superficie_kg": la["plataforma_kg"], "mav_e_aquecimento_kg": la["mav_e_aquecimento_kg"],
              "circuito_fluido_cruzeiro_kg": la["circuito_fluido_cruzeiro_kg"],
              "caso_a_referencia_otimista": next(c for c in lm["casos"] if c["caso"].startswith("A:"))}

    vr = en["lander"]["variante_rhu"]
    ob = en["orbitador"]["adotada"]
    energia = {"lander_opcao": vr["opcao"], "rhu_quantidade": vr["rhu_quantidade"], "pu238_g": vr["pu238_g"],
               "orbitador": {k: ob[k] for k in ("carga_w", "painel_w_afelio", "bateria_wh", "plataforma_kg")}}
    mav = next(x for x in te["aquecimento_mav"] if x["alvo"].startswith("atual"))
    termico = {"mav_alvo_c": mav["t_c"], "mav_potencia_w": mav["potencia_w"], "mav_energia_wh_sol": mav["energia_wh_sol"],
               "amostras": te["amostras"]["decisao"], "cruzeiro_calor_w": lm["calor_cruzeiro_w"], "cruzeiro_passivo_max_w": lm["passivo_max_w"],
               "rejeicao_ativa": lm["rejeicao_ativa_necessaria"], "circuito_fluido_kg": lm["circuito_fluido_kg"]}
    dc = co["decisao_caminhos"]
    comunicacao = {"conjuncao": co["janelas"]["periodo_conjuncao_graus"][0], "sem_comando": co["janelas"]["sem_comando_graus"][0],
                   "sep_minimo": co["sep_minimo"], "tempo_luz_max_min": co["distancias"]["tempo_luz_max_min"],
                   "demanda_lander_mbit_sol": dc["demanda_lander_mbit_sol"], "helicopteros_envoltoria_mbit_sol": dc["helicopteros_envoltoria_mbit_sol"],
                   "caminhos_mbit_sol": dc["caminhos_mbit_sol"], "dte_minimo_kg": dc["dte_minimo"]["massa_prevista_kg"]}
    superficie = {"chegada": op["chegada"], "inicio_conjuncao": op["inicio_conjuncao"], "prob_tempestade_estada": op["prob_tempestade_estada"],
                  "requisitos": op["requisitos"], "pouso": op["pouso"],
                  "linha_do_tempo": [{k: x[k] for k in ("distancia_m", "ritmo", "helicopteros_em_paralelo", "total_sois", "lancamento",
                                                       "folga_conjuncao_dias", "atende_folga_minima", "dentro_do_alvo")} for x in op["linha_do_tempo"]]}

    ps = ler("config/premissas.yaml")["premissas"]
    nao = [p for p in ps if p["status"] == "NÃO VALIDADA"]
    premissas = {"total": len(ps), "nao_validadas": len(nao),
                 "criadas_na_fase_4": [p["id"] for p in ps if int(p["id"][2:]) >= PRIMEIRA_DA_FASE_4],
                 "criticas": [p["id"] for p in ps if p.get("critica")]}

    out = {"gerado_por": "tools/fase4.py", "massas": massas, "lancadores": lancadores, "energia": energia, "termico": termico,
           "comunicacao": comunicacao, "superficie": superficie, "premissas": premissas}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "resumo.yaml").write_text(yaml.safe_dump(nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(nativo(out))


def escreve_md(o):
    br = lambda x, n=0: "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    pc = lambda x: f"{100 * x:+.0f} %".replace("-", "−")  # noqa: E731
    m, lc, en, te, co, su, pr = (o[k] for k in ("massas", "lancadores", "energia", "termico", "comunicacao", "superficie", "premissas"))
    a = m["caso_a_referencia_otimista"]
    md = ["# Fase 4: resumo integrado (gerado por tools/fase4.py)", "",
          "Números das Etapas 4.1 a 4.5 (results/etapa4.*) e da arquitetura vigente (orbital.veiculos sobre config/). Massas em kg.", "",
          "## Massas (ADR 0019)", "",
          "| Item | Valor |", "| :- | -: |",
          f"| Orbitador injetado (regra iii) | {br(m['orbitador_injetado_kg'])} |",
          f"| Lander injetado | {br(m['lander_injetado_kg'])} |",
          f"| Massa de entrada do lander | {br(m['lander_entrada_kg'])} |",
          f"| Massa pousada do lander | {br(m['lander_pousado_kg'])} |",
          f"| Plataforma de superfície (P-017, caso B) | {br(m['plataforma_superficie_kg'], 1)} |",
          f"| MAV + energia do aquecimento | {br(m['mav_e_aquecimento_kg'])} |",
          f"| Circuito de fluido no estágio de cruzeiro (P-077) | {br(m['circuito_fluido_cruzeiro_kg'], 1)} |",
          f"| Total na órbita baixa da Terra, regra (iii) (orbitador + lander) | {br(m['total_leo_kg'])} |",
          "", f"Referência otimista ({a['caso']}): plataforma {br(a['plataforma_kg'], 1)}, lander injetado {br(a['lander_injetado_kg'])}.", "",
          "## Lançadores de base (ADR 0020)", "",
          "| Veículo | Lançador | Margem na base | Pior margem nas sensibilidades | Caso da pior margem |", "| :- | :- | -: | -: | :- |"]
    for k, rot in (("orbitador", "Orbitador"), ("lander", "Lander"), ("lander_reserva", "Lander (reserva)")):
        x = lc[k]
        md.append(f"| {rot} | {x['lancador']} | {pc(x['margem_base'])} | {pc(x['pior']['margem'])} | {x['pior']['caso']} |")
    md += ["", "Margem na pior janela, injeção direta; sensibilidades de results/etapa2.5/arquitetura.md (uma premissa por vez).", "",
           "## Energia (Etapa 4.1, ADR 0015)", "",
           f"- **Lander, C + RHU:** {br(en['lander_opcao']['area_m2'], 1)} m² de painel ({br(en['lander_opcao']['painel_kg'], 1)} kg) e bateria de "
           f"{br(en['lander_opcao']['bateria_kg'], 1)} kg, total {br(en['lander_opcao']['total_kg'], 1)} kg; {en['rhu_quantidade']} RHUs "
           f"({br(en['pu238_g'], 1)} g de Pu-238).",
           f"- **Orbitador:** carga de {br(en['orbitador']['carga_w'])} W; painel de {br(en['orbitador']['painel_w_afelio'])} W no afélio; bateria de "
           f"{br(en['orbitador']['bateria_wh'])} Wh; plataforma de {br(en['orbitador']['plataforma_kg'], 1)} kg.", "",
           "## Térmico (Etapa 4.2) e rejeição de calor no cruzeiro (Etapa 4.5)", "",
           f"- **MAV a {br(te['mav_alvo_c'])} °C (P-027):** {br(te['mav_potencia_w'], 1)} W, {br(te['mav_energia_wh_sol'])} Wh/sol.",
           f"- **Amostras:** {te['amostras']}.",
           f"- **Cruzeiro do lander:** {br(te['cruzeiro_calor_w'])} W contra {br(te['cruzeiro_passivo_max_w'])} W de perda passiva máxima: rejeição "
           f"{'ativa' if te['rejeicao_ativa'] else 'passiva'}, circuito de fluido de {br(te['circuito_fluido_kg'], 1)} kg no estágio de cruzeiro.", "",
           "## Comunicação (Etapa 4.3, ADR 0017)", "",
           f"- **Conjunção solar (SEP ≤ 5°):** {co['conjuncao']['inicio']} a {co['conjuncao']['fim']} ({co['conjuncao']['dias']} dias); sem comando "
           f"de {co['sem_comando']['inicio']} a {co['sem_comando']['fim']}; SEP mínimo {br(co['sep_minimo']['graus'], 2)}° em {co['sep_minimo']['data']}.",
           f"- **Tempo-luz máximo:** {br(co['tempo_luz_max_min'], 1)} min.",
           f"- **Demanda do lander:** {br(co['demanda_lander_mbit_sol'])} Mbit/sol; helicópteros (envoltória) {br(co['helicopteros_envoltoria_mbit_sol'])} Mbit/sol.",
           "- **Capacidade dos caminhos (Mbit/sol):** " + "; ".join(f"{k} {br(v[0])} a {br(v[1])}" for k, v in co["caminhos_mbit_sol"].items()) + ".",
           f"- **Enlace direto mínimo:** {br(co['dte_minimo_kg'], 1)} kg.", "",
           "## Operação de superfície (Etapa 4.4, ADR 0018)", "",
           f"Chegada {su['chegada']}; início da conjunção {su['inicio_conjuncao']}; probabilidade de tempestade global na estada "
           f"{br(100 * su['prob_tempestade_estada'])} %. Requisitos: folga mínima de {br(su['requisitos']['folga_min'])} dias, alvo de "
           f"{br(su['requisitos']['alvo'][0])} a {br(su['requisitos']['alvo'][1])} dias; pouso de precisão "
           f"{'obrigatório' if su['requisitos']['pouso_de_precisao'] else 'não exigido'}.", "",
           "| Distância ao depósito (m) | Ritmo | Helicópteros | Sóis | Lançamento do MAV | Folga até a conjunção (d) | Folga mínima | Alvo |",
           "| -: | :- | -: | -: | :- | -: | :- | :- |"]
    for x in su["linha_do_tempo"]:
        md.append(f"| {br(x['distancia_m'])} | {x['ritmo']} | {x['helicopteros_em_paralelo']} | {br(x['total_sois'])} | {x['lancamento'] or '—'} | "
                  f"{br(x['folga_conjuncao_dias'])} | {'sim' if x['atende_folga_minima'] else 'não'} | {'sim' if x['dentro_do_alvo'] else 'não'} |")
    p = su["pouso"]
    md += ["", f"Pouso: erro de entrega do Mars 2020 {br(p['erro_de_entrega_m'])} m; desvio máximo do TRN {br(p['desvio_trn_max_m'])} m; "
           f"alcance do SRH {br(p['alcance_srh_por_carga_m'])} m por carga; alcance de projeto do Ingenuity {br(p['alcance_ingenuity_projeto_m'])} m.", "",
           "## Premissas", "",
           f"{pr['total']} premissas, {pr['nao_validadas']} NÃO VALIDADAS; {len(pr['criadas_na_fase_4'])} criadas na Fase 4 "
           f"({pr['criadas_na_fase_4'][0]} a {pr['criadas_na_fase_4'][-1]}); críticas: {', '.join(pr['criticas'])}. "
           "Lista em results/fase4/premissas_nao_validadas.md."]
    (SAIDA / "resumo.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
