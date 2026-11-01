"""Etapa 4.5: lista de massas do lander de baixo para cima, rejeição de calor no cruzeiro, totais, margens e MAV.

- Itens que as Etapas 4.1 a 4.4 acrescentaram (energia C + RHU, RHUs, enlace direto mínimo, câmera do TRN), mais os já
  listados (UHF, radar, braço, helicópteros), com a margem de crescimento E1 (config/plataformas.yaml).
- Núcleo sem lista publicada: o L3 (P-017) é a alocação de cima para baixo; confere-se se o L3 comporta os itens e se o
  que sobra para o núcleo é compatível com a descida seca do Mars 2020 [F204].
- Rejeição de calor no cruzeiro: dissipação máxima do LAMP do SRL contra a perda passiva máxima do LAMP [F165]
  (config/termico.yaml, cruzeiro); circuito de fluido com massa escalada do MPF (P-077), sem margem E1 (o MPF dá um máximo).
  Conservador: entra na plataforma de superfície, embora no MSL e no Mars 2020 o radiador fique no estágio de
  cruzeiro, descartado antes da entrada [F206].
- Totais e margens dos lançadores em três casos de plataforma; dependência do orbitador em relação ao Falcon Heavy.
- MAV: margem de lançador, lançador maior e Isp maior (config/lista_massas.yaml). A sensibilidade troca só o Isp:
  empuxo, número e massa dos motores e o propelente ficam os do R-4D-11.
Saída: results/etapa4.5/lista_massas.yaml e .md

Uso: python tools/lista_massas_lander.py
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

import arquitetura as arq  # noqa: E402
from orbital import veiculos as ve  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402
from orbital.massa_plataformas import lander_base, mga  # noqa: E402

SAIDA = RAIZ / "results" / "etapa4.5"


def main():
    lm, pcfg, lcfg = ler("config/lista_massas.yaml"), ler("config/plataformas.yaml"), ler("config/lancadores.yaml")
    scfg, mcfg, tcfg = ler("config/superficie.yaml"), ler("config/mav_propulsao.yaml"), ler("config/termico.yaml")
    en = ler("results/etapa4.1/energia.yaml")["lander"]
    com = ler("results/etapa4.3/comunicacao.yaml")["decisao_caminhos"]["dte_minimo"]
    arqr = ler("results/etapa2.5/arquitetura.yaml")
    sub = pcfg["lander"]["subsistemas"]
    m = lambda cat: mga(cat, pcfg, "e1_medio")  # noqa: E731

    it = lm["itens_novos"]
    vr = en["variante_rhu"]
    itens = [
        {"item": "Energia: painel e bateria da C + RHU (Etapas 4.1 e 4.2)", "prevista_kg": vr["opcao"]["total_kg"], "novo": True,
         "fonte": "results/etapa4.1/energia.yaml (já com margem)"},
        {"item": f"RHUs ({vr['rhu_quantidade']} × {v(it['rhu_massa_g']):g} g, máximo por unidade)", "basica_kg": vr["rhu_quantidade"] * v(it["rhu_massa_g"]) / 1e3,
         "categoria": "estrutura_secundaria", "novo": True, "fonte": "[F152]"},
        {"item": "Enlace direto mínimo (Etapa 4.3)", "prevista_kg": com["massa_prevista_kg"], "novo": True, "fonte": "results/etapa4.3/comunicacao.yaml (já com margem)"},
        {"item": "Câmera do TRN (LCAM do Mars 2020)", "basica_kg": v(it["lvs_camera_kg"]), "categoria": it["lvs_camera_kg"]["categoria"], "novo": True, "fonte": "[F203]"},
        {"item": "UHF (Phoenix)", "basica_kg": sub["uhf"]["massa_kg"], "categoria": sub["uhf"]["categoria"], "novo": False, "fonte": "[F74]"},
        {"item": "Radar (Phoenix)", "basica_kg": sub["radar"]["massa_kg"], "categoria": sub["radar"]["categoria"], "novo": False, "fonte": "[F74]"},
        {"item": "Braço de coleta (reserva)", "basica_kg": sub["amostras"]["massa_kg"], "categoria": sub["amostras"]["categoria"], "novo": False, "fonte": "[F40]"},
        {"item": "Helicópteros (2)", "basica_kg": sub["helicopteros"]["massa_kg"], "categoria": sub["helicopteros"]["categoria"], "novo": False, "fonte": "[F98]"},
    ]
    # rejeição de calor no cruzeiro: dissipação máxima do LAMP do SRL [F165] + RHUs (Etapa 4.2) contra a perda passiva
    # máxima do LAMP [F165]; as duas são do LAMP
    rc, srl = lm["rejeicao_calor_cruzeiro"], tcfg["cruzeiro"]
    calor = v(srl["srl_dissipacao_max_lamp_w"]) + ler("results/etapa4.2/termico.yaml")["cruzeiro"]["rhu_w"]
    hrs_kg = v(rc["mpf_massa_max_kg"]) * calor / v(rc["mpf_calor_w"])   # P-077
    # no estágio de cruzeiro, descartado antes da entrada (decisão do portão da 4.5): fica fora da plataforma de superfície
    cruz_cfg = v(scfg["lancamento"]["cruzeiro_lander"]["circuito_fluido_kg"])
    itens.append({"item": "Circuito de fluido de cruzeiro (rejeição ativa; no estágio de cruzeiro)", "prevista_kg": hrs_kg, "novo": True,
                  "cruzeiro": True, "fonte": "P-077 ([F205], [F165])"})
    for x in itens:
        if "prevista_kg" not in x:
            x["margem"] = m(x["categoria"])
            x["prevista_kg"] = x["basica_kg"] * (1 + x["margem"])
    # somas da plataforma de superfície (sem o circuito, que vai no estágio de cruzeiro)
    novos = sum(x["prevista_kg"] for x in itens if x["novo"] and not x.get("cruzeiro"))
    todos = sum(x["prevista_kg"] for x in itens if not x.get("cruzeiro"))

    # energia do aquecimento do MAV contada também no item do MAV (dupla contagem com a C + RHU)
    mav_total = next(x["massa_kg"] for x in arqr["lander"]["composicao"] if x["item"].startswith("MAV"))
    mav_glom = arqr["lander"]["mav"]["estagios"][0]["massa_inicial_kg"]
    dupla = mav_total - mav_glom

    l3 = (v(pcfg["lander"]["topo_para_baixo"]["srl_seco_superficie_kg"]) - v(pcfg["lander"]["topo_para_baixo"]["srl_mav_kg"])
          - v(pcfg["lander"]["topo_para_baixo"]["srl_sfr_kg"]))
    plat = lander_base(pcfg)   # L3 + braço + helicópteros (P-017 até a Etapa 4.5; referência otimista)
    p017 = v(scfg["lander"]["plataforma_superficie_kg"])   # P-017 vigente (caso B, portão da 4.5)
    # itens dentro do L3: todos menos braço e helicópteros; a energia do aquecimento do MAV (dupla) fica no item do MAV
    nucleo_folga = l3 - (todos - sum(x["prevista_kg"] for x in itens if x["item"].startswith(("Braço", "Helicópteros")))) + dupla
    ds = v(lm["referencias_nucleo"]["m2020_descida_seca_kg"])

    # casos de plataforma: (A) L3 + braço + helicópteros; (B) A + itens novos − dupla contagem (P-017 vigente);
    # (C) descida seca do Mars 2020 + todos os itens. Os três com o circuito de fluido no estágio de cruzeiro.
    casos = {"A: L3 + braço + helicópteros (referência otimista)": plat, "B: A + itens novos, sem a dupla contagem (P-017 vigente)": plat + novos - dupla,
             "C: núcleo = descida seca do Mars 2020 + todos os itens": ds + todos - dupla}
    v0, jan, _ = ve.veiculos()
    linhas = []
    for nome, p in casos.items():
        vv = ve.veiculos(p)[0]
        mg = arq.margens(vv, jan, lcfg)
        linhas.append({"caso": nome, "plataforma_kg": p, "lander_injetado_kg": vv["lander"]["injetada_kg"],
                       "orbitador_injetado_kg": vv["orbitador_regra_iii"]["injetada_kg"], "margens": mg})
    # MAV: Isp maior (sensibilidade no caso B)
    op = arqr["lander"]["mav"]["opcao"]
    isp = []
    for mo in lm["mav_isp"]:
        m2 = copy.deepcopy(mcfg)
        m2["opcoes"][op]["isp_s"] = [mo["isp_s"], mo["isp_s"]]
        vv = ve.veiculos(casos["B: A + itens novos, sem a dupla contagem (P-017 vigente)"], mcfg=m2)[0]
        mg = arq.margens(vv, jan, lcfg)
        isp.append({**mo, "lander_injetado_kg": vv["lander"]["injetada_kg"], "margens_lander": mg["lander"]})
    for x in isp:   # ganho em pontos percentuais sobre o motor de base (primeiro da lista), por lançador
        x["ganho_pp"] = {n: 100 * (x["margens_lander"][n] - isp[0]["margens_lander"][n]) for n in x["margens_lander"]}
    # antes e depois das decisões do portão da 4.5 (sem o circuito no estágio de cruzeiro = como estava)
    s0 = copy.deepcopy(scfg)
    s0["lancamento"]["cruzeiro_lander"]["circuito_fluido_kg"]["valor"] = 0.0
    b0 = plat + novos - dupla
    ad = []
    for nome, p, s in (("Antes: A, sem circuito (P-017 anterior)", plat, s0), ("B com o circuito na plataforma", b0 + hrs_kg, s0),
                       ("Depois: B, circuito no estágio de cruzeiro (vigente)", b0, scfg)):
        vv = ve.veiculos(p, scfg=s)[0]
        ad.append({"caso": nome, "plataforma_kg": p, "lander_injetado_kg": vv["lander"]["injetada_kg"],
                   "massa_entrada_kg": vv["lander"]["massa_entrada_kg"], "margens": arq.margens(vv, jan, lcfg)})
    out = {"gerado_por": "tools/lista_massas_lander.py", "itens": itens, "itens_novos_kg": novos, "itens_todos_kg": todos,
           "dupla_contagem_energia_mav_kg": dupla, "l3_kg": l3, "folga_para_o_nucleo_kg": nucleo_folga,
           "m2020_descida_seca_kg": ds, "calor_cruzeiro_w": calor, "passivo_max_w": v(srl["srl_perda_passiva_max_w"]),
           "rejeicao_ativa_necessaria": calor > v(srl["srl_perda_passiva_max_w"]), "circuito_fluido_kg": hrs_kg,
           "circuito_fluido_config_kg": cruz_cfg, "p017_config_kg": p017, "antes_depois": ad, "lancadores_base": lcfg["base"],
           "casos": linhas, "mav_isp": isp, "margem_sistema_jpl": v(lm["margem_sistema_jpl"]),
           "escolha_lancadores": {k: lcfg["escolha"][k] for k in ("orbitador", "lander")}}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "lista_massas.yaml").write_text(yaml.safe_dump(nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    pc = lambda x: "—" if x is None else f"{100 * x:+.0f} %".replace("-", "−")  # noqa: E731
    pp = lambda x: f"{x:+.1f} pp".replace(".", ",").replace("-", "−")  # noqa: E731
    md = ["# Lista de massas do lander (gerado por tools/lista_massas_lander.py)", "",
          "Nenhuma fonte primária pública publica a massa de um lander de Marte por subsistema: o núcleo (estrutura, pernas, "
          "propulsão de descida seca, térmico, aviônica, cabeamento, sistema de lançamento do MAV) fica de cima para baixo (L3).", "",
          f"P-017 vigente (decisão do portão da 4.5, caso B): {br(o['p017_config_kg'], 1)} kg. Circuito de fluido no estágio de cruzeiro, descartado "
          f"antes da entrada: {br(o['circuito_fluido_config_kg'], 1)} kg (config/superficie.yaml, P-077).", "",
          "## Itens identificados", "", "| Item | Básica (kg) | Margem E1 | Prevista (kg) | Novo nas Etapas 4.1–4.4? | Fonte |", "| :- | -: | -: | -: | :- | :- |"]
    for x in o["itens"]:
        md.append(f"| {x['item']} | {br(x['basica_kg'], 2) if 'basica_kg' in x else '—'} | {br(100 * x['margem'], 1) + ' %' if 'margem' in x else '—'} | "
                  f"{br(x['prevista_kg'], 1)} | {'sim' if x['novo'] else 'não'} | {x['fonte']} |")
    md += ["", f"Na plataforma de superfície (sem o circuito, que vai no estágio de cruzeiro): itens novos {br(o['itens_novos_kg'], 1)} kg; "
           f"todos os itens {br(o['itens_todos_kg'], 1)} kg. A câmera do TRN entra; o computador "
           "de visão (VCE) não tem massa publicada e não está na lista.", "",
           f"Dupla contagem: o item do MAV traz {br(o['dupla_contagem_energia_mav_kg'], 1)} kg de energia do aquecimento, que a energia C + RHU "
           "também cobre.", "",
           "## O L3 comporta os itens?", "",
           f"L3 = {br(o['l3_kg'])} kg (SRL seco − MAV − rover de busca). Tirando os itens que estão dentro do L3 (todos menos braço e helicópteros, "
           f"que somam fora dele), sobram {br(o['folga_para_o_nucleo_kg'])} kg para o núcleo, contra {br(o['m2020_descida_seca_kg'], 1)} kg da descida "
           "seca do Mars 2020 [F204] (descent stage de sky crane, sem pernas nem plataforma de superfície). A energia do aquecimento do MAV, que fica no item do MAV, não é descontada do L3.", "",
           "## Rejeição de calor no cruzeiro (lander)", "",
           f"Dissipação: {br(o['calor_cruzeiro_w'])} W (máximo do LAMP do SRL [F165] + RHUs, Etapa 4.2), contra {br(o['passivo_max_w'])} W de perda passiva "
           f"máxima do LAMP [F165]: rejeição {'ativa' if o['rejeicao_ativa_necessaria'] else 'passiva'}. Circuito de fluido, como no MSL e no Mars 2020 [F206, F207]: "
           f"cerca de {br(o['circuito_fluido_kg'], 1)} kg (P-077, escala do MPF [F205], sem margem E1), no estágio de cruzeiro, descartado antes da "
           "entrada, como no MSL e no Mars 2020 [F206].", "",
           "## Antes e depois das decisões do portão da 4.5", "",
           "| Caso | Plataforma (kg) | Massa de entrada (kg) | Lander injetado (kg) | " + " | ".join(o["escolha_lancadores"]["lander"]) + " |",
           "| :- | -: | -: | -: |" + " -: |" * len(o["escolha_lancadores"]["lander"])]
    for c in o["antes_depois"]:
        md.append(f"| {c['caso']} | {br(c['plataforma_kg'], 1)} | {br(c['massa_entrada_kg'])} | {br(c['lander_injetado_kg'])} | "
                  + " | ".join(pc(c["margens"]["lander"][n]) for n in o["escolha_lancadores"]["lander"]) + " |")
    b = o["lancadores_base"]
    md += ["", f"Lançadores de base (ADR 0020): lander no {b['lander']} (reserva: {b['lander_reserva']}); orbitador no {b['orbitador']}.", "",
           "## Totais e margens dos lançadores", "",
           "| Caso | Plataforma (kg) | Lander injetado (kg) | " + " | ".join(f"Lander: {n}" for n in o["escolha_lancadores"]["lander"]) + " | "
           + " | ".join(f"Orbitador: {n}" for n in o["escolha_lancadores"]["orbitador"]) + " |",
           "| :- | -: | -: |" + " -: |" * (len(o["escolha_lancadores"]["lander"]) + len(o["escolha_lancadores"]["orbitador"]))]
    for c in o["casos"]:
        md.append(f"| {c['caso']} | {br(c['plataforma_kg'])} | {br(c['lander_injetado_kg'])} | "
                  + " | ".join(pc(c["margens"]["lander"][n]) for n in o["escolha_lancadores"]["lander"]) + " | "
                  + " | ".join(pc(c["margens"]["orbitador"][n]) for n in o["escolha_lancadores"]["orbitador"]) + " |")
    md += ["", "## MAV: Isp maior (caso B; só o Isp muda)", "",
           "Empuxo, número e massa dos motores e o propelente ficam os do R-4D-11. Ganho em pontos sobre o motor de base entre parênteses.", "",
           "| Motor | Isp (s) | Propelente | Voo | Lander injetado (kg) | " + " | ".join(o["escolha_lancadores"]["lander"]) + " |",
           "| :- | -: | :- | :- | -: |" + " -: |" * len(o["escolha_lancadores"]["lander"])]
    for x in o["mav_isp"]:
        md.append(f"| {x['motor']} | {br(x['isp_s'])} | {x['propelente']} | {x['voo']} | {br(x['lander_injetado_kg'])} | "
                  + " | ".join(f"{pc(x['margens_lander'][n])} ({pp(x['ganho_pp'][n])})" for n in o["escolha_lancadores"]["lander"]) + " |")
    md += ["", f"Margem de sistema do JPL para um conceito nesta fase: {br(100 * o['margem_sistema_jpl'])} % [F210] (margem de massa do sistema, "
           "não margem do lançador)."]
    (SAIDA / "lista_massas.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
