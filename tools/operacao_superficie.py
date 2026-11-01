"""Etapa 4.4: operação de superfície. Linha do tempo mínima, tempestade e conjunção, e dados dos helicópteros.

- Linha do tempo: pouso → saída e mapeamento (conceito SRH [F191]) → busca dos 10 tubos [F193] → transferência tardia ao
  MAV e preparação (P-074) → lançamento do MAV. Distância do lander ao depósito em três casos (P-075, [F190], [F187]);
  ritmo do SRH (4 sóis por tubo [F191], escalado com a distância, P-073) e ritmo real do Ingenuity (intervalo mediano entre
  voos, tabela de voos [F195]).
- Para cada caso: data e Ls do lançamento, probabilidade acumulada de início de tempestade global até ele (catálogo de
  config/energia.yaml, P-061), folga até o início da conjunção (results/etapa4.3).
- Dados dos helicópteros: volume por voo e por sol contra a capacidade de cada caminho (results/etapa4.3), e as opções
  (a) mais autonomia, (b) operação mais lenta, (c) mais comunicação (escala do enlace direto da Etapa 4.3, P-069).
Saída: results/etapa4.4/operacao_superficie.yaml e .md

Uso: python tools/operacao_superficie.py
"""

from __future__ import annotations

import datetime as dt
import math
import statistics
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "tools"))

from orbital import energia as en  # noqa: E402
from orbital.config import ler, nativo, v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa4.4"


def ls_de(data: dt.date) -> float:
    return en.geometria_marte(data.isoformat() + "T00:00:00")[0]


def prob_tempestade_ate(ls_fim: float, catalogo, j0: float, p_ano: float) -> tuple[float, int]:
    """Probabilidade de um início de tempestade global entre o começo da estação (j0) e ls_fim (P-061: a fração dos
    inícios do catálogo nesse intervalo vezes a probabilidade por ano marciano)."""
    n = sum(1 for x in catalogo if j0 <= x["ls"] <= ls_fim)
    return p_ano * n / len(catalogo), n


def main():
    oc, ec, cc = ler("config/operacao_superficie.yaml"), ler("config/energia.yaml"), ler("config/comunicacao.yaml")
    ms = ler("results/etapa1.3/missoes.yaml")
    ref = next(c for c in ms["candidatas"] if c["id"] == ler("config/missao_referencia.yaml")["missao_referencia"]["id"])
    chegada = dt.date.fromisoformat(ref["chegada_marte"][:10])
    hsol = v(ler("config/plataformas.yaml")["lander"]["energia"]["duracao_sol_h"])
    com = ler("results/etapa4.3/comunicacao.yaml")
    conj = dt.date.fromisoformat(com["janelas"]["periodo_conjuncao_graus"][0]["inicio"])
    tg = ec["lander"]["tempestades_globais"]
    cat, j0, p_ano = tg["inicios"], tg["estacao_inicio_ls"]["valor"][0], v(tg["probabilidade_por_ano_marciano"])

    # ritmo real do Ingenuity: intervalo entre voos consecutivos [F195]
    sois = oc["ingenuity"]["voos_sois"]["valor"]
    intervalos = [b - a for a, b in zip(sois, sois[1:])]
    cad = {"voos": len(sois), "sol_primeiro": sois[0], "sol_ultimo": sois[-1], "intervalo_mediano_sois": statistics.median(intervalos),
           "intervalo_medio_sois": statistics.mean(intervalos), "intervalo_min_sois": min(intervalos), "intervalo_max_sois": max(intervalos)}

    srh, dep, op = oc["srh"], oc["deposito"], oc["operacao"]
    n_tubos, alc_srh = v(dep["tubos"]), v(srh["alcance_por_carga_m"])
    alc_ing = v(oc["ingenuity"]["alcance_de_projeto_m"])
    fixos = v(srh["saida_sois"]) + v(srh["mapeamento_sois"]) + v(op["transferencia_e_lancamento_sois"])

    def caso(d_m, ritmo, n_heli):
        if ritmo == "SRH":   # 4 sóis por tubo a ~200 m; cada carga diária extra por perna além do alcance (P-073)
            por_tubo = v(srh["sois_por_tubo"]) + 2 * (math.ceil(d_m / alc_srh) - 1)
            voos_tubo = v(srh["voos_por_tubo"]) * math.ceil(d_m / alc_srh)
        else:                # ritmo do Ingenuity: voos de até 300 m, um voo a cada intervalo mediano
            voos_tubo = v(srh["voos_por_tubo"]) * math.ceil(d_m / alc_ing)
            por_tubo = voos_tubo * cad["intervalo_mediano_sois"]
        busca = n_tubos * por_tubo / n_heli
        total = fixos + busca
        lanc = chegada + dt.timedelta(days=total * hsol / 24)
        ls_l = ls_de(lanc)
        if ls_l < ls_cheg:   # o Ls deu a volta: a estação de início já passou inteira (P-061)
            p, n = prob_tempestade_ate(360.0, cat, j0, p_ano)
        else:
            p, n = prob_tempestade_ate(ls_l, cat, j0, p_ano)
        return {"distancia_m": d_m, "ritmo": ritmo, "helicopteros_em_paralelo": n_heli, "sois_por_tubo": por_tubo,
                "voos_por_tubo": voos_tubo, "busca_sois": busca, "total_sois": total, "lancamento": str(lanc), "ls_lancamento": ls_l,
                "prob_tempestade_ate_lancamento": p, "inicios_do_catalogo_ate_lancamento": n,
                "folga_conjuncao_dias": (conj - lanc).days, "antes_da_conjuncao": lanc < conj, "voos_por_sol": voos_tubo * n_heli / por_tubo}

    ls_cheg = ls_de(chegada)
    dist = {k: v(x) for k, x in op["distancias_m"].items()}
    linha = [caso(d, r, h) for d in dist.values() for r in ("SRH", "Ingenuity") for h in (int(v(srh["helicopteros"])), 1)]
    p_cheg, n_cheg = prob_tempestade_ate(ls_cheg, cat, j0, p_ano)
    ls_partida = ls_de(dt.date.fromisoformat(ref["partida_marte"][:10]))
    p_estada = p_ano   # a estada atravessa a estação inteira (P-061)

    # ---------------- dados dos helicópteros
    hc, hi = cc["helicopteros"], cc["helicopteros_ingenuity"]
    nvoos = v(hi["voos"])
    b_nav = hc["navcam_px"]["valor"][0] * hc["navcam_px"]["valor"][1] * v(hc["bits_por_pixel"])
    b_rte = hi["rte_px"]["valor"][0] * hi["rte_px"]["valor"][1] * v(hi["rte_bits_por_pixel"])
    nav_mbit = v(hi["imagens_navcam"]) / nvoos * b_nav / 1e6   # Navcam sem perdas: razão não publicada, sem compressão
    rte_bruto = v(hi["imagens_rte"]) / nvoos * b_rte / 1e6
    rz = oc["ingenuity"]["rte_jpeg_razao"]
    rte_jpeg = [rte_bruto / rz["max"], rte_bruto / rz["min"]]
    por_voo = {"Navcam + RTE, sem compressão (Etapa 4.3)": [nav_mbit + rte_bruto, nav_mbit + rte_bruto],
               "Navcam sem compressão + RTE em JPEG": [nav_mbit + rte_jpeg[0], nav_mbit + rte_jpeg[1]],
               "(a) mais autonomia: só a RTE em JPEG (a Navcam fica a bordo)": rte_jpeg}
    cam = com["decisao_caminhos"]["caminhos_mbit_sol"]
    lander = com["decisao_caminhos"]["demanda_lander_mbit_sol"]
    ritmos = {"SRH, 2 helicópteros, 200 m": next(x for x in linha if x["distancia_m"] == dist["srh"] and x["ritmo"] == "SRH" and x["helicopteros_em_paralelo"] == 2),
              "(b) ritmo do Ingenuity, 2 helicópteros, 200 m": next(x for x in linha if x["distancia_m"] == dist["srh"] and x["ritmo"] == "Ingenuity" and x["helicopteros_em_paralelo"] == 2)}
    dados = []
    for rnome, rc in ritmos.items():
        for vnome, (a, b) in por_voo.items():
            dados.append({"ritmo": rnome, "volume": vnome, "voos_por_sol": rc["voos_por_sol"],
                          "mbit_por_sol": [a * rc["voos_por_sol"], b * rc["voos_por_sol"]],
                          "total_com_lander": [a * rc["voos_por_sol"] + lander, b * rc["voos_por_sol"] + lander],
                          "duracao_superficie_sois": rc["total_sois"], "folga_conjuncao_dias": rc["folga_conjuncao_dias"],
                          "prob_tempestade": rc["prob_tempestade_ate_lancamento"]})

    # (c) mais comunicação: enlace direto para a maior demanda total do caso base (escala da Etapa 4.3, P-069)
    dm, dte = cc["dte_maior"], com["lander_dte"]
    base = next(x for x in dados if x["ritmo"].startswith("SRH") and x["volume"].startswith("Navcam + RTE"))
    demanda_c = base["total_com_lander"][1]
    taxa = demanda_c * 1e6 / (dte["horas_por_passe"] * 3600)
    fator = taxa / dte["taxa_bps"]
    d100 = dm["msl"]["hga_m"] * math.sqrt(fator / (dm["mro"]["rf_w"] / dm["msl"]["rf_w"]))
    dens = dm["mro"]["refletor_kg"] / (math.pi * (dm["mro"]["hga_m"] / 2) ** 2)
    massa = dens * math.pi * (d100 / 2) ** 2 + dm["mro"]["gimbal_kg"] * (d100 / dm["mro"]["hga_m"]) ** 2 + dm["mro"]["twta_kg"] + dm["mro"]["epc_kg"]
    e_c = dm["mro"]["twta_dc_w"] * dte["horas_por_passe"]
    import arquitetura as arq
    import lancamento as lcm
    plat_l = v(ler("config/superficie.yaml")["lander"]["plataforma_superficie_kg"])
    v0, jan, _ = lcm.veiculos()
    v1 = lcm.veiculos(plat_l + massa)[0]
    lcfg = ler("config/lancadores.yaml")
    m0, m1 = arq.margens(v0, jan, lcfg), arq.margens(v1, jan, lcfg)
    opc_c = {"demanda_mbit_sol": demanda_c, "taxa_bps": taxa, "fator_sobre_msl": fator, "diametro_hga_100w_m": d100, "massa_kg": massa,
             "energia_wh_passe": e_c, "lander_injetado_kg": [v0["lander"]["injetada_kg"], v1["lander"]["injetada_kg"]],
             "margens_lander": {k: [m0["lander"][k], m1["lander"][k]] for k in m0["lander"]},
             "tgo_mais_mro_max_mbit_sol": cam["TGO"][1] + cam["MRO"][1]}

    out = {"gerado_por": "tools/operacao_superficie.py", "chegada": str(chegada), "ls_chegada": ls_cheg, "ls_partida": ls_partida,
           "inicio_conjuncao": str(conj), "tempestade_em_curso_na_chegada": {"probabilidade": p_cheg, "inicios_do_catalogo": n_cheg},
           "prob_tempestade_estada": p_estada, "ingenuity_cadencia": cad, "linha_do_tempo": linha,
           "capacidade_caminhos_mbit_sol": cam, "demanda_lander_mbit_sol": lander, "dados_helicopteros": dados,
           "rte_jpeg_razao": [rz["min"], rz["max"]], "opcao_c": opc_c,
           "pouso": {"elipse_km": oc["pouso"]["elipse_km"]["valor"], "desvio_trn_max_m": v(oc["pouso"]["desvio_trn_max_m"]),
                     "erro_ao_alvo_m": v(oc["pouso"]["erro_ao_alvo_m"]), "erro_de_entrega_m": v(oc["pouso"]["erro_de_entrega_m"]),
                     "alcance_srh_por_carga_m": alc_srh, "alcance_ingenuity_projeto_m": alc_ing,
                     "maior_voo_ingenuity_m": v(oc["ingenuity"]["maior_distancia_m"])}}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "operacao_superficie.yaml").write_text(yaml.safe_dump(nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")
    escreve_md(out)


def escreve_md(o):
    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",").replace("-", "−")  # noqa: E731
    pc = lambda x: f"{100 * x:+.0f} %".replace("-", "−")  # noqa: E731
    p, cad, tc = o["pouso"], o["ingenuity_cadencia"], o["tempestade_em_curso_na_chegada"]
    md = ["# Operação de superfície (gerado por tools/operacao_superficie.py)", "", "## Pouso e alcance", "",
          f"Elipse do Mars 2020: {br(p['elipse_km'][0], 1)} × {br(p['elipse_km'][1], 1)} km [F187]; o TRN desvia até {br(p['desvio_trn_max_m'])} m [F188] "
          f"e pousou a {br(p['erro_ao_alvo_m'])} m do alvo escolhido [F189]; a entrega guiada ficou a {br(p['erro_de_entrega_m'])} m do ponto esperado [F190]. "
          f"Alcance: SRH {br(p['alcance_srh_por_carga_m'])} m por carga diária [F194]; Ingenuity {br(p['alcance_ingenuity_projeto_m'])} m de projeto [F196] "
          f"e {br(p['maior_voo_ingenuity_m'])} m no maior voo [F195].", "",
          "## Chegada e estação de tempestades", "",
          f"Chegada em {o['chegada']}, Ls {br(o['ls_chegada'], 1)}°. Inícios do catálogo na estação antes da chegada: {tc['inicios_do_catalogo']} "
          f"(tempestade possivelmente em curso na chegada: {br(100 * tc['probabilidade'])} %, P-061). Estada inteira: {br(100 * o['prob_tempestade_estada'])} %.", "",
          "## Linha do tempo mínima da superfície", "",
          f"Ritmo real do Ingenuity [F195]: {cad['voos']} voos entre os sóis {cad['sol_primeiro']} e {cad['sol_ultimo']}; intervalo entre voos: mediana "
          f"{br(cad['intervalo_mediano_sois'])} sóis, média {br(cad['intervalo_medio_sois'], 1)}, de {cad['intervalo_min_sois']} a {cad['intervalo_max_sois']}.", "",
          "| Distância ao depósito | Ritmo | Helicópteros em paralelo | Sóis por tubo | Busca (sóis) | Total (sóis) | Lançamento do MAV | Ls | Tempestade até o lançamento | Folga até a conjunção (dias) | Antes da conjunção? |",
          "| -: | :- | -: | -: | -: | -: | :- | -: | -: | -: | :- |"]
    for x in o["linha_do_tempo"]:
        md.append(f"| {br(x['distancia_m'])} m | {x['ritmo']} | {x['helicopteros_em_paralelo']} | {br(x['sois_por_tubo'])} | {br(x['busca_sois'])} | "
                  f"{br(x['total_sois'])} | {x['lancamento']} | {br(x['ls_lancamento'], 1)}° | {br(100 * x['prob_tempestade_ate_lancamento'], 1)} % | {x['folga_conjuncao_dias']} | "
                  + ("sim" if x["antes_da_conjuncao"] else "**não**") + " |")
    md += ["", f"Início da conjunção (SEP ≤ 5°): {o['inicio_conjuncao']} (results/etapa4.3). Tempestade: fração dos inícios do catálogo entre "
           "o começo da estação e o Ls do lançamento, vezes a probabilidade por ano marciano (P-061).", "",
           "## Dados dos helicópteros contra a capacidade dos caminhos", "",
           "Capacidade (Mbit/sol, results/etapa4.3): " + "; ".join(f"{k} {br(a)} a {br(b)}" for k, (a, b) in o["capacidade_caminhos_mbit_sol"].items())
           + f". Lander: {br(o['demanda_lander_mbit_sol'])} Mbit/sol (P-063). RTE em JPEG com razão de {br(o['rte_jpeg_razao'][0], 2)} a "
           f"{br(o['rte_jpeg_razao'][1], 2)} [F198] (P-076).", "",
           "| Ritmo | Volume por voo | Voos por sol | Helicópteros (Mbit/sol) | Com o lander (Mbit/sol) | Superfície (sóis) | Folga até a conjunção (dias) |",
           "| :- | :- | -: | -: | -: | -: | -: |"]
    for x in o["dados_helicopteros"]:
        md.append(f"| {x['ritmo']} | {x['volume']} | {br(x['voos_por_sol'], 2)} | {br(x['mbit_por_sol'][0])} a {br(x['mbit_por_sol'][1])} | "
                  f"{br(x['total_com_lander'][0])} a {br(x['total_com_lander'][1])} | {br(x['duracao_superficie_sois'])} | {x['folga_conjuncao_dias']} |")
    c = o["opcao_c"]
    md += ["", "### (c) Mais capacidade de comunicação", "",
           f"Enlace direto para {br(c['demanda_mbit_sol'])} Mbit/sol num passe de 8 h (P-065): {br(c['taxa_bps'])} bps, {br(c['fator_sobre_msl'])} vezes o "
           f"análogo do MSL; HGA de {br(c['diametro_hga_100w_m'], 2)} m com 100 W (P-069), cerca de {br(c['massa_kg'], 1)} kg, {br(c['energia_wh_passe'])} Wh por passe. "
           f"Lander injetado {br(c['lander_injetado_kg'][0])} → {br(c['lander_injetado_kg'][1])} kg; margens do lander: "
           + "; ".join(f"{k} {pc(a)} → {pc(b)}" for k, (a, b) in c["margens_lander"].items())
           + f" (sensibilidade). TGO + MRO no máximo somam {br(c['tgo_mais_mro_max_mbit_sol'])} Mbit/sol, sem avaliar a sobreposição dos passes."]
    (SAIDA / "operacao_superficie.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
