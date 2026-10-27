"""Etapa 2.5: tabela integrada da arquitetura (veículos, estágios, massas, lançadores, margens e cronograma da
missão de referência, datas em TDB) e sensibilidade às premissas de maior efeito.

Tudo vem das cadeias das etapas anteriores: tools/lancamento.py (veículos e margens, ADR 0008), tools/plataformas.py
(plataformas, Etapa 2.3 e 2.5), results/etapa1.3/missoes.yaml (datas e envelope). A sensibilidade muda uma premissa
por vez e mantém a órbita de encontro de base (300 × 24.992 km), sem reaplicar a regra dos 5 %.
Saída: results/etapa2.5/arquitetura.yaml e arquitetura.md

Uso: python tools/arquitetura.py
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(RAIZ / "src"), str(RAIZ / "tools")]

import dimensionamento as dm  # noqa: E402
import lancamento as lc  # noqa: E402
from superficie import _ler, _v  # noqa: E402

SAIDA = RAIZ / "results" / "etapa2.5"


def margens(vei, janelas, lcfg):
    esc = lcfg["escolha"]
    return {"orbitador": {n: lc.pior_margem_a(n, vei["orbitador_regra_iii"]["injetada_kg"], janelas, lcfg)[0] for n in esc["orbitador"]},
            "lander": {n: lc.pior_margem_a(n, vei["lander"]["injetada_kg"], janelas, lcfg)[0] for n in esc["lander"]}}


def main():
    dcfg, scfg, lcfg = _ler("config/dimensionamento.yaml"), _ler("config/superficie.yaml"), _ler("config/lancadores.yaml")
    cu, pl, ms = _ler("config/carga_util.yaml"), _ler("results/etapa2.3/plataformas.yaml"), _ler("results/etapa1.3/missoes.yaml")
    pcfg = _ler("config/plataformas.yaml")
    vei, janelas, ref = lc.veiculos()
    base_m = margens(vei, janelas, lcfg)

    # Composição dos veículos
    o = vei["orbitador_regra_iii"]
    est = {e["nome"]: e for e in o["estagios"]}
    cu_itens = cu["opcoes"][dcfg["caso_base"]["carga_util"]]["ate_orbita_marte"]
    orbitador = [
        {"item": "Estágio de inserção em Marte (MMH/MON)", "propelente_kg": est["insercao_marte"]["propelente_kg"], "inerte_kg": est["insercao_marte"]["inerte_kg"]},
        {"item": "Estágio de retorno (MMH/MON)", "propelente_kg": est["retorno"]["propelente_kg"], "inerte_kg": est["retorno"]["inerte_kg"]},
        *[{"item": f"Carga útil CU-2: {x['item']}", "massa_kg": float(x["massa"])} for x in cu_itens],
        {"item": "Plataforma (P-016, lista por subsistema + sensores de encontro)", "massa_kg": _v(dcfg["plataforma_orbitador_kg"])},
    ]
    soma_o = sum(x.get("massa_kg", 0) + x.get("propelente_kg", 0) + x.get("inerte_kg", 0) for x in orbitador)
    la_ = vei["lander"]
    el = {e["nome"]: e for e in la_["estagios"]}
    s = pcfg["lander"]["subsistemas"]
    mga = lambda k: float(s[k]["massa_kg"]) * (1 + __import__("plataformas")._mga(s[k]["categoria"], pcfg, "e1_medio"))  # noqa: E731
    lander = [
        {"item": "Estágio de cruzeiro (correções de trajetória)", "propelente_kg": el["cruzeiro_lander"]["propelente_kg"], "inerte_kg": el["cruzeiro_lander"]["inerte_kg"]},
        {"item": "Sistema de entrada, descida e pouso (aeroshell, paraquedas, propelente de descida; P-018)", "massa_kg": la_["massa_entrada_kg"] - la_["massa_pousada_kg"]},
        {"item": "Plataforma de superfície L3 (lander do MSR sem MAV e sem rover de busca)", "massa_kg": __import__("plataformas").lander_l3(pcfg)},
        {"item": "Braço de coleta de reserva (P-034, com margem)", "massa_kg": mga("amostras")},
        {"item": "Helicópteros de recuperação (ADR 0009, com margem)", "massa_kg": mga("helicopteros")},
        {"item": "MAV hipergólico + energia do aquecimento (ADR 0007)", "massa_kg": la_["mav_e_aquecimento_kg"]},
    ]
    soma_l = sum(x.get("massa_kg", 0) + x.get("propelente_kg", 0) + x.get("inerte_kg", 0) for x in lander)

    # Cronograma da missão de referência (datas em TDB, Etapa 1.3 com a errata da 2.4)
    cand = {c["id"]: c for c in ms["candidatas"]}[ref]
    crono = [
        {"evento": "Lançamentos do orbitador e do lander (injeção direta, lançamentos separados)", "data_tdb": cand["partida_terra"]},
        {"evento": "Chegada a Marte: captura do orbitador; entrada direta e pouso do lander", "data_tdb": cand["chegada_marte"]},
        {"evento": f"Estada em Marte ({cand['em_marte_dias']:.0f} d): recuperação dos tubos, coleta de reserva, subida do MAV, encontro",
         "data_tdb": f"{cand['chegada_marte']} a {cand['partida_marte']}"},
        {"evento": "Partida de Marte (injeção trans-Terra)", "data_tdb": cand["partida_marte"]},
        {"evento": f"Chegada à Terra (reentrada a {cand['v_reentrada_km_s']:.2f} km/s)".replace(".", ","), "data_tdb": cand["chegada_terra"]},
    ]

    # Sensibilidade: uma premissa por vez
    pv = pl["orbitador"]["prevista_kg"]
    lb = pl["lander"]["base_L3_mais_amostras"]["prevista_kg"]
    casos = []

    def caso(nome, premissa, plat_o=None, plat_l=None, margem_dv=None, razao=None, lcfg2=None):
        d2, s2 = copy.deepcopy(dcfg), copy.deepcopy(scfg)
        if plat_o is not None:
            d2["plataforma_orbitador_kg"]["valor"] = plat_o
        if margem_dv is not None:
            d2["margem_dv"]["valor"] = margem_dv
        if razao is not None:
            s2["lander"]["razao_pousada_entrada"]["entrada_direta"]["valor"] = razao
        v = lc.veiculos(plat_l, d2, s2)[0]
        m = margens(v, janelas, lcfg2 or lcfg)
        casos.append({"caso": nome, "premissa": premissa, "orbitador_injetado_kg": v["orbitador_regra_iii"]["injetada_kg"],
                      "lander_injetado_kg": v["lander"]["injetada_kg"], "margens": m})

    caso("Base", "—")
    caso("Margem de massa GSFC (+15 % da básica) nas duas plataformas", "P-033", pv["e1_medio_mais_gsfc"], lb["e1_medio_mais_gsfc"])
    caso("Margem de massa ESA (20 % × 20 %) nas duas plataformas", "P-033", pv["esa"], lb["esa"])
    caso("Plataforma do lander no limite inferior (L1)", "P-017, P-035", plat_l=pl["lander"]["L1"]["prevista_kg"]["e1_medio"])
    caso("Plataforma do lander no limite superior (SRL 2024 − MAV)", "P-017, P-035", plat_l=pl["lander"]["limite_superior_srl_2024_kg"])
    alt = _v(scfg["lander"]["razao_pousada_entrada"]["a_partir_de_orbita"])
    caso(f"Razão pousada/entrada {alt:g} (Viking, a partir de órbita) em vez de {_v(scfg['lander']['razao_pousada_entrada']['entrada_direta']):g}".replace(".", ","), "P-018", razao=alt)
    for mdv in (0.05, 0.20):
        caso(f"Margem de Δv {100 * mdv:.0f} % (base {100 * _v(dcfg['margem_dv']):.0f} %)", "P-014", margem_dv=mdv)
    l2 = copy.deepcopy(lcfg)
    l2["dla"]["multiplicador_nordeste"]["fator"] = [1.0] * len(l2["dla"]["multiplicador_nordeste"]["fator"])
    caso("Sem penalidade de DLA (multiplicador 1)", "P-036", lcfg2=l2)

    out = {"gerado_por": "tools/arquitetura.py", "missao_referencia": ref,
           "orbita_encontro_km": [pl["orbita_encontro"]["periapse_alt_km"], pl["orbita_encontro"]["apoapse_regra_5pct_km"]],
           "envelope_dv_km_s": ms["envelope_dimensionamento"]["dv_total_km_s"],
           "orbitador": {"composicao": orbitador, "injetado_kg": o["injetada_kg"], "soma_kg": soma_o},
           "lander": {"composicao": lander, "injetado_kg": la_["injetada_kg"], "soma_kg": soma_l,
                      "massa_entrada_kg": la_["massa_entrada_kg"], "massa_pousada_kg": la_["massa_pousada_kg"]},
           "lancadores": {"orbitador": lcfg["escolha"]["orbitador"], "lander": lcfg["escolha"]["lander"], "margens_base": base_m},
           "lancamentos": 2, "cronograma": crono, "sensibilidade": casos}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "arquitetura.yaml").write_text(yaml.safe_dump(dm._nativo(out), sort_keys=False, allow_unicode=True), encoding="utf-8")

    br = lambda x, n=0: "—" if x is None else f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    pc = lambda x: "—" if x is None else f"{100 * x:+.0f} %".replace("-", "−")  # noqa: E731
    md = ["# Arquitetura integrada (gerado por tools/arquitetura.py)", "",
          f"Missão de referência {ref}; órbita de encontro {br(out['orbita_encontro_km'][0])} × {br(out['orbita_encontro_km'][1])} km; "
          f"envelope de Δv {br(out['envelope_dv_km_s'], 3)} km/s; injeção direta (ADR 0008); 2 lançamentos. Massas em kg.", "",
          "## Orbitador (regra iii)", "", "| Item | Propelente | Inerte / massa |", "| :- | -: | -: |"]
    for x in orbitador:
        md.append(f"| {x['item']} | {br(x.get('propelente_kg'))} | {br(x.get('inerte_kg', x.get('massa_kg')))} |")
    md += [f"| **Massa injetada** | | **{br(o['injetada_kg'])}** |", "", "## Lander", "", "| Item | Propelente | Inerte / massa |", "| :- | -: | -: |"]
    for x in lander:
        md.append(f"| {x['item']} | {br(x.get('propelente_kg'))} | {br(x.get('inerte_kg', x.get('massa_kg')))} |")
    md += [f"| **Massa injetada** | | **{br(la_['injetada_kg'])}** |", "",
           f"Massa de entrada {br(la_['massa_entrada_kg'])} kg; massa pousada {br(la_['massa_pousada_kg'])} kg.", "",
           "## Lançadores (forma a): pior margem nas quatro janelas", "", "| Veículo | Lançador | Pior margem |", "| :- | :- | -: |"]
    for v, d in base_m.items():
        for n, mg in d.items():
            md.append(f"| {v} | {n} | {pc(mg)} |")
    md += ["", "## Cronograma da missão de referência (datas em TDB)", "", "| Evento | Data |", "| :- | :- |"]
    md += [f"| {c['evento']} | {c['data_tdb']} |" for c in crono]
    md += ["", "## Sensibilidade (uma premissa por vez; órbita de encontro de base)", "",
           "| Caso | Premissa | Orbitador injetado | Lander injetado | " + " | ".join(f"Orb.: {n}" for n in lcfg["escolha"]["orbitador"])
           + " | Lander: menor margem |", "| :- | :- | -: | -: |" + " -: |" * (len(lcfg["escolha"]["orbitador"]) + 1)]
    for c in casos:
        ml = min(v for v in c["margens"]["lander"].values() if v is not None)
        nl = min((v, k) for k, v in c["margens"]["lander"].items() if v is not None)[1]
        md.append(f"| {c['caso']} | {c['premissa']} | {br(c['orbitador_injetado_kg'])} | {br(c['lander_injetado_kg'])} | "
                  + " | ".join(pc(c["margens"]["orbitador"][n]) for n in lcfg["escolha"]["orbitador"]) + f" | {pc(ml)} ({nl}) |")
    (SAIDA / "arquitetura.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
