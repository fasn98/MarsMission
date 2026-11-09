"""Portão do MAV (Fabio, 2026-11-07): conclusão de sistema e famílias de arquitetura, sem cálculo novo.

Lê só resultados existentes (results/) e textos com fonte (config/cad.yaml, bloco portao_mav).
Saída: results/etapa7.2/portao_mav.md (conclusão e achados) e results/etapa7.2/opcoes_arquitetura.md (famílias).

Uso: python tools/opcoes_arquitetura.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from orbital.config import ler  # noqa: E402

SAIDA = RAIZ / "results" / "etapa7.2"


def br(x, n=3):
    return f"{round(x, n) + 0.0:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def sg(x, n=3):
    return f"{round(x, n) + 0.0:+,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def dados():
    ra, su, rb = ler("results/etapa7.2/rota_a.yaml"), ler("results/etapa7.2/subida_mav.yaml"), ler("results/etapa7.2/rotas_mav.yaml")
    so, arq, fo = ler("results/etapa7.2/mav_solido.yaml"), ler("results/etapa2.5/arquitetura.yaml"), ler("results/etapa7.2b/folgas.yaml")
    bo = ler("results/etapa7.2/bocais_alternativas.yaml")
    cen = next(c for c in ra["dimensionamento"]["casos"] if c["origem"] == "calculado, central")
    calc = [c for c in ra["dimensionamento"]["casos"] if c["origem"].startswith("calculado")]
    a_sem = [c for c in su["casos"] if c["variante"] == "44:1"]
    pf = [x["pedido_menos_usado_m_s"] for c in a_sem for x in c.get("ponto_fixo", []) if x.get("pedido_menos_usado_m_s") is not None]
    base = next(c for c in su["casos"] if c["variante"] == "164:1")
    eletr = [p["eletrico_primeiro_que_fecha"] for x in rb["rota_b"] for p in x["propulsores"].values() if p.get("eletrico_primeiro_que_fecha")]
    ad465 = {li["leitura"]: next(x["radial_m"] for x in li["por_altura"] if x["altura_m"] == ra["adaptador"]["altura_base_m"]) for li in ra["adaptador"]["linhas"] if li["veiculo"].startswith("Lander 4,65")}
    hib = [p["c2_mais_leve"] for x in rb["rota_b"] for p in x["propulsores"].values()]
    return {
        "dv_km_s": arq["lander"]["mav"]["dv_com_margem_km_s"], "orbita_km": arq["orbita_encontro_km"],
        "a_com_deck": {"isp_s": ra["isp_calculado"]["s"]["central"], "folgas_m": [x["folga_deck_real_m"] for x in cen["por_geometria"].values()], "alvo_m": ra["fecha"]["alvo_m"],
                       "massa_por_area": [c["massa_por_area_kg_m2"] for c in calc]},
        "a_sem_deck": {"convergiu": any(c["convergiu"] for c in a_sem), "pedido_menos_usado_m_s": [min(pf), max(pf)], "motivos": [c.get("motivo") for c in a_sem]},
        "b": {"mav": [{"altitude_km": x["altitude_km"], "folga_sem_deck_m": x["mav"]["folga_deitado_m"], "folga_com_deck_m": x["mav"]["folga_deitado_com_deck_m"], "glom_kg": x["mav"]["glom_kg"],
                       "dv_m_s": x["mav"]["dv_mav_com_margem_m_s"], "empuxo_peso": x["mav"]["empuxo_peso"], "massa_por_area": x["mav"]["massa_por_area_kg_m2"]} for x in rb["rota_b"]],
              "eletrico_margem": [min(e["margem_falcon_heavy"] for e in eletr), max(e["margem_falcon_heavy"] for e in eletr)],
              "eletrico_kg": [min(e["orbitador_injetado_kg"] for e in eletr), max(e["orbitador_injetado_kg"] for e in eletr)],
              "hibrido_margem": [min(h["margem_falcon_heavy"] for h in hib), max(h["margem_falcon_heavy"] for h in hib)], "estada_dias": rb["missao"]["estada_minima_dias"],
              "eletrico_fecha_estada": all(e["fecha_estada_e_lancador"] for e in eletr), "eletrico_folga_estada_dias": [min(e["folga_estada_dias"] for e in eletr), max(e["folga_estada_dias"] for e in eletr)],
              "eletrico_pronto": sorted(e["pronto_no_encontro"] for e in eletr), "eletrico_a_tempo": any(e["pronto_antes_do_ultimo_lancamento"] for e in eletr),
              "eletrico_vida_conhecida": any(e["vida_conhecida"] for e in eletr), "ultimo_lancamento_mav": rb["missao"]["lancamento_mav_mais_tarde"]},
        "solido": {"glom_kg": [c["glom_kg"] for c in so["casos"]], "melhor_folga_sem_deck_m": max(x["folga_sem_deck_m"] for c in so["casos"] for x in c["comprimentos"])},
        "base": {"glom_kg": base.get("glom_kg"), "empuxo_peso": base.get("empuxo_peso"), "vigente_kg": su["base_vigente_glom_kg"], "folga_sem_deck_m": base["comprimentos"]["sem aninhar"]["folga_sem_deck_m"],
                 "dv_100_m_s": base.get("dv_100x100_m_s"), "f37_m_s": su["referencia"]["f37_m_s"]},
        "aeroshell_465": ad465, "altura_adaptador_m": ra["adaptador"]["altura_base_m"],
        "m2020_kg_m2": rb["referencia_m2020_kg_m2"],
        "r40b": next(a for a in bo["alternativas"] if a["motor"] == "R-40B"), "r42": next(a for a in bo["alternativas"] if a["motor"] == "R-42"),
    }


def portao(d, cfg):
    a, b, s, ba = d["a_com_deck"], d["b"], d["solido"], d["base"]
    md = ["# Portão do MAV: conclusão de sistema (gerado por tools/opcoes_arquitetura.py)", "",
          "Decisão do Fabio (2026-11-07), registrada também no ADR 0023. Números de results/; nada novo calculado aqui.", "",
          f"> {cfg['conclusao_de_sistema']}", "",
          f"Δv do MAV com margem, no vigente: {br(d['dv_km_s'], 3)} km/s (results/etapa2.5/arquitetura.yaml); órbita de encontro {br(d['orbita_km'][0], 0)} × {br(d['orbita_km'][1], 0)} km.", "",
          "| Rota | Resultado | Fonte |", "| :- | :- | :- |",
          f"| A com deck | Isp calculado de {br(a['isp_s'], 1)} s: folga com deck de {sg(min(a['folgas_m']))} a {sg(max(a['folgas_m']))} m nas quatro geometrias, contra o alvo de {sg(a['alvo_m'], 2)} m | results/etapa7.2/rota_a.md, seção 0 |",
          f"| A sem deck | " + ("não converge: com o empuxo/peso real, o Δv pedido passa do usado em toda a varredura (de " + sg(d['a_sem_deck']['pedido_menos_usado_m_s'][0], 0) + " a " + sg(d['a_sem_deck']['pedido_menos_usado_m_s'][1], 0) + " m/s), até o MAV não decolar" if not d["a_sem_deck"]["convergiu"] else "convergiu") + " | results/etapa7.2/subida_mav.md |",
          "| B (orbitador elétrico, encontro em órbita baixa) | MAV com folga sem deck de " + " e ".join(f"{sg(m['folga_sem_deck_m'])} m ({br(m['altitude_km'], 0)} km)" for m in b["mav"]) + f", abaixo do alvo, e com deck negativa; orbitador híbrido com margem no Falcon Heavy de {sg(100 * b['hibrido_margem'][0], 1)} a {sg(100 * b['hibrido_margem'][1], 1)} %; o só elétrico (calculado, não verificado) fecha massa ({sg(100 * b['eletrico_margem'][0], 1)} a {sg(100 * b['eletrico_margem'][1], 1)} %) e estada, mas fica pronto em {' e '.join(b['eletrico_pronto'])}, depois do último lançamento do MAV ({b['ultimo_lancamento_mav']}) | results/etapa7.2/rotas_mav.md; ADR 0013, adendo |",
          f"| Sólido | GLOM de {br(min(s['glom_kg']), 0)} a {br(max(s['glom_kg']), 0)} kg; melhor folga sem deck {sg(s['melhor_folga_sem_deck_m'])} m, no limite do Δv ideal | results/etapa7.2/mav_solido.md |",
          "", "## Achado: GLOM da base com o empuxo/peso real (não aplicado)", "",
          f"Com a subida simulada no empuxo/peso real ({br(ba['empuxo_peso'], 2)}), a base com o 164:1 converge em GLOM de {br(ba['glom_kg'], 1)} kg, contra {br(ba['vigente_kg'], 1)} kg vigentes, com Δv de 100 × 100 km de {br(ba['dv_100_m_s'], 1)} m/s contra {br(ba['f37_m_s'], 1)} m/s de [F37] (results/etapa7.2/subida_mav.md). A folga sem deck da base segue negativa ({sg(ba['folga_sem_deck_m'])} m). **Decisão do Fabio: não substituir o vigente agora; decidir junto com a arquitetura.**",
          "", "As famílias de arquitetura para a próxima decisão estão em results/etapa7.2/opcoes_arquitetura.md."]
    (SAIDA / "portao_mav.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def opcoes(d, cfg):
    b, r40, r42, fo = d["b"], d["r40b"], d["r42"], d["aeroshell_465"]
    md = ["# Famílias de arquitetura para o portão do MAV (gerado por tools/opcoes_arquitetura.py)", "",
          "Pedido do Fabio (2026-11-07): sem cálculo novo, só resultados existentes e fontes com página. Não é recomendação. A opinião do agente está separada e rotulada no fim.", "",
          "## Para onde a NASA convergiu no MSR", "",
          "A NASA não chegou a escolher uma arquitetura. Em 2024, apontou o MAV como o fator principal de complexidade, custo e risco; em janeiro de 2025, as duas opções de pouso levavam \"a smaller version of the Mars Ascent Vehicle\"; a proposta de orçamento de 2026 propõe encerrar o programa por custo. O plano de gastos de julho de 2026 ainda tem uma linha do MSR, sem dizer o uso; a situação depois disso não foi conferida.", "",
          "| Quando | O que a fonte diz |", "| :- | :- |"]
    md += [f"| {x['quando']} | {x['fonte']} |" for x in cfg["msr_rumo"]]
    md += ["", "## Família 1: estada longa e orbitador elétrico", "",
           "- **O que muda:** a missão de referência passa a ter estada longa em Marte, como a do ERO; o orbitador usa propulsão elétrica para espiralar até uma órbita baixa de encontro, e o MAV sobe só até ela.",
           "- **ADRs que reabre:** 0003 (missão de referência), 0005 (órbita de encontro), 0013 (propulsão do orbitador), e 0008/0020 (lançadores) se a massa mudar. O ADR 0013 já registra: \"Uma missão de estada longa, como a do ERO, poderia mudar isso\".",
           f"- **Ordem de grandeza (rota B, results/etapa7.2/rotas_mav.md):** o MAV vai a {br(b['mav'][0]['dv_m_s'], 0)} a {br(b['mav'][-1]['dv_m_s'], 0)} m/s de Δv com margem, contra {br(1000 * d['dv_km_s'], 0)} m/s no vigente, e a GLOM de {br(b['mav'][0]['glom_kg'], 0)} a {br(b['mav'][-1]['glom_kg'], 0)} kg. Mesmo assim, a folga sem deck fica em " + " e ".join(f"{sg(m['folga_sem_deck_m'])} m" for m in b["mav"]) + f", abaixo do alvo de +0,05 m. O orbitador só elétrico (calculado, NÃO verificado, só com o XIPS-25" + (", sem vida conhecida" if not b["eletrico_vida_conhecida"] else "") + f") fecha a massa ({br(b['eletrico_kg'][0], 0)} a {br(b['eletrico_kg'][1], 0)} kg, margem de {sg(100 * b['eletrico_margem'][0], 1)} a {sg(100 * b['eletrico_margem'][1], 1)} % no Falcon Heavy) e" + (f" a estada de {br(b['estada_dias'], 0)} dias (folga de {br(b['eletrico_folga_estada_dias'][0], 1)} a {br(b['eletrico_folga_estada_dias'][1], 1)} dias)" if b["eletrico_fecha_estada"] else " não a estada") + f", mas fica pronto no encontro em {' e '.join(b['eletrico_pronto'])}, depois do último lançamento do MAV na referência ({b['ultimo_lancamento_mav']}); rotas_mav.md registra isso como ordem de grandeza, que não decide.",
           "- **ERO, a estada longa de referência:** " + "; ".join(cfg["ero"]) + ".",
           "- **Riscos:** missão mais longa (o ERO leva cerca de cinco anos na volta completa, pela fonte); propulsão elétrica de alta potência; o MAV ainda precisa de embalagem que caiba.",
           "- **Para decidir, calcular:** a missão de referência com estada longa, a guiagem elétrica otimizada e o MAV para a órbita baixa com o empuxo/peso real (a subida de results/etapa7.2/subida_mav.md com o alvo da órbita baixa).",
           "", "## Família 2: aeroshell maior que 4,65 m, com outro lançador", "",
           "- **O que muda:** a cápsula cresce, o MAV deitado ganha comprimento, e o lançador precisa de coifa com envelope maior.",
           "- **ADRs que reabre:** 0022 (arranjo e aeroshell), 0008 e 0020 (lançadores), e o portão da Etapa 7.3 (entrada).",
           f"- **Ordem de grandeza:** no Vulcan, com o adaptador da P-097 ({br(d['altura_adaptador_m'], 3)} m), o lander de 4,65 m tem folga radial de " + " e ".join(f"{sg(v)} m ({k})" for k, v in fo.items()) + f" (results/etapa7.2/rota_a.md, seção 5). A massa por área da rota A fica de {br(min(d['a_com_deck']['massa_por_area']), 0)} a {br(max(d['a_com_deck']['massa_por_area']), 0)} kg/m², contra {br(d['m2020_kg_m2'], 0)} do Mars 2020 (risco aberto na 7.3); um diâmetro maior reduz esse número, mas sai da herança de voo de 4,5 m ([F251] PDF p. 6).",
           "- **Fontes do MSR:** [F254] PDF p. 13: \"Capsule diameter (m)\" de 4.65 e >5.4 nas duas colunas do SRL.",
           "- **Lançadores com coifa maior (voos e situação de operação não conferidos em fonte oficial nesta etapa):**"]
    md += [f"  - **{x['lancador']}:** {x['texto']}." for x in cfg["lancadores"]]
    md += ["- **O que muda na entrada (fontes da NASA):**"]
    md += [f"  - {x}." for x in cfg["entrada_maior"]]
    md += [
           "- **Riscos:** entrada fora da herança de voo (paraquedas, aquecimento, guiagem); só o New Glenn tem envelope publicado bem acima de 4,65 m, com guia anterior ao primeiro voo; o MAV continua com o mesmo Δv.",
           "- **Para decidir, calcular:** o envelope do lançador candidato com a cápsula maior, o MAV deitado na cápsula maior e a entrada (massa por área, abertura do paraquedas).",
           "", "## Família 3: MAV hipergólico com motor de estágio 1 de 1 a 4 kN", "",
           "- **O que muda:** o empuxo/peso do MAV sobe e a perda gravitacional cai. Indício, sem cálculo dos candidatos: a base com empuxo/peso maior convergiu, e a rota A, perto de 1, não.",
           "- **ADRs que reabre:** 0011 (motores) e 0023 (rota do MAV).",
           f"- **Ordem de grandeza (results/etapa7.2/bocais_alternativas.md):** um R-40B sozinho cabe em Ø {br(r40['menor_d_varredura_com_parede_m'], 2)} m com parede, com empuxo/peso de {br(r40['empuxo_peso_marte'], 2)} em Marte, mas o motor passa a P-086 em {br(r40['excesso_sobre_p086_m'], 3)} m, o MAV fica com folga deitado de {sg(r40['folgas'][0]['folga_4_5_m'])} m no aeroshell de 4,5 m e {sg(r40['folgas'][0]['folga_4_65_m'])} m no de 4,65 m, e o Isp usado é {br(r40['isp_s'], 0)} s (de [F106]; [F228] dá 293 s); dois R-42 dão empuxo/peso de {br(r42['empuxo_peso_marte'], 2)}, mas não cabem em Ø 0,57 m. Na subida simulada, a base com empuxo/peso de {br(d['base']['empuxo_peso'], 2)} converge (results/etapa7.2/subida_mav.md).",
           "- **Candidatos com fonte** (motores de 1 a 4 kN, e, como referência de voo, o de 800 N do Chandrayaan-3, abaixo da faixa; o R-42, de 890 N e em produção por [F228] PDF p. 25, entra só na ordem de grandeza, porque dois não cabem em Ø 0,57 m):"]
    md += [f"  - **{x['motor']}** ({x['situacao']}): {x['fonte']}" for x in cfg["motores_1_4_kn"]]
    md += [f"  - Não conferidos: {cfg['motores_nao_conferidos']}.",
           "- **Riscos:** pelas fontes, nenhum candidato de 1 a 4 kN tem produção confirmada (R-40B \"Not in Production\"; LEROS 4 \"In development, TRL6\", ficha de 2021, situação atual não conferida; os motores da ISRO e do Tianwen-1 sem dado de produção); o R-40B exige atualização de componentes obsoletos pela própria folha; o Isp do R-40B é menor que o do R-4D-11.",
           "- **Para decidir, calcular:** a subida e o comprimento com cada candidato (o mesmo método de results/etapa7.2/subida_mav.md e rota_a.md).",
           "", "## Família 4: três lançamentos, com o orbitador à parte, como no MSR original", "",
           "- **Nota sobre o título:** o título é o do pedido. Nas fontes deste PR, dois landers mais o orbitador foram estudados pelo MSR (2021 e 2023) e rejeitados uma vez; nenhuma delas dá três lançamentos como linha de base do MSR.",
           "- **O que muda:** o lander se divide em dois (um com o MAV e outro com a coleta), além do orbitador. O MAV ganha um lander próprio.",
           "- **ADRs que reabre:** 0005 e 0008 (lançamentos separados), 0009 (coleta), 0020 (lançadores) e 0022 (arranjo).",
           "- **Ordem de grandeza:** o Δv do MAV não muda, então o problema de embalagem só muda se o lander dedicado permitir outro arranjo do MAV (por exemplo, sem a carga de coleta ao lado). Não há cálculo disso no estudo.",
           "- **Fontes do MSR:** [F254] PDF p. 8: \"The project currently is considering whether to deliver the Sample Fetch Rover (SFR) and Mars Ascent Vehicle (MAV) in one or two launches\", \"Two launches: Entry system heavier than MSL and Mars 2020, probably no new technologies needed, but more costly\"; PDF p. 13: cápsula de 4.65 m no SRL de dois lançamentos, contra >5.4 m no de um lançamento; [F255] PDF p. 7: o segundo lander foi \"eventually rejected because of added complexity/cost\"; PDF p. 45: \"MSR MAV Lander (MML), which includes the MAV and a MAV landing/launch system using a scaled-up Skycrane EDL\".",
           "- **Riscos:** custo e complexidade de um terceiro lançamento e de um segundo pouso (a razão da rejeição no MSR); dependência entre os pousos.",
           "- **Para decidir, calcular:** a massa e o arranjo do lander só com o MAV, e as margens dos três lançamentos.",
           "", "## Decisão do Fabio (2026-11-09): família 1 calculada; 2, 3 e 4 em reserva", "", "| Família em reserva | Motivo |", "| :- | :- |",
           *[f"| {x['familia']} | {x['motivo']} |" for x in cfg["reservas"]], "", "Resultados da família 1: results/familia1/missao.md e results/familia1/mavs.md.",
           "", "## Opinião do agente (separada dos dados; não é fato nem recomendação como fato)", "",
           "- A causa comum é o Δv. A família 1 é a única que ataca o Δv do MAV diretamente; as famílias 2 e 4 tratam a embalagem, e a 3 trata a perda na subida.",
           "- Os dados sugerem que uma combinação pode ser necessária: a rota B sozinha chega perto de caber sem deck, e mais empuxo no estágio 1 reduziria o MAV.",
           "- O próprio MSR terminou apontando o MAV como o fator principal; isso é coerente com o que este estudo achou."]
    (SAIDA / "opcoes_arquitetura.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def main():
    cfg = ler("config/cad.yaml")["portao_mav"]
    d = dados()
    SAIDA.mkdir(parents=True, exist_ok=True)
    portao(d, cfg)
    opcoes(d, cfg)


if __name__ == "__main__":
    main()
