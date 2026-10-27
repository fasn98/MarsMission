"""Orçamento de Δv por trecho e dimensionamento por estágios (Etapa 1.4, Parte B).

Entradas: config/dimensionamento.yaml (estágios, Isp, frações estruturais, parcelas de Δv,
margens), config/carga_util.yaml (CU-1/2/3), config/missao_referencia.yaml,
config/parametros_orbitais.yaml e results/etapa1.3/missoes.yaml (Δv ideais por trecho).
Saídas: results/etapa1.4/orcamento_dv.md, results/etapa1.4/dimensionamento.yaml e .md,


Arquitetura (só trechos no espaço; descida, pouso e subida ficam para a Fase 2):
  1. Estágio de saída da Terra: injeção trans-Marte a partir da órbita baixa. Descartado.
  2. Módulo de inserção em Marte: correções da ida e captura. Descartado em Marte.
  3. Estágio de retorno: encontro e manutenção em órbita de Marte, injeção trans-Terra, correções
     da volta; solta a cápsula e faz o desvio. Leva a carga útil até o fim.

Uso: python tools/dimensionamento.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(RAIZ / "src"), str(RAIZ / "tools")]

from missoes import parametros  # noqa: E402
from orbital import foguete as fg  # noqa: E402
from orbital import manobras as mn  # noqa: E402

SAIDA = RAIZ / "results" / "etapa1.4"


def _ler(caminho):
    return yaml.safe_load((RAIZ / caminho).read_text(encoding="utf-8"))


def _v(item):
    return float(item["valor"])


def carga(opcao, cu, acrescimo_capsula):
    """(massa até a órbita de Marte, massa da cápsula que volta), com acréscimo na cápsula."""
    o = cu["opcoes"][opcao]
    capsula = sum(i["massa"] for i in o["volta_a_terra"])
    ate_marte = sum(i["massa"] for i in o["ate_orbita_marte"])
    descartado = sum(i["massa"] for i in o["ate_orbita_marte"] if any(d in i["item"] for d in o.get("descartado_em_marte", [])))
    extra = capsula * acrescimo_capsula
    return ate_marte + extra, capsula + extra, descartado


def orcamento(caso, cfg, p):
    """Δv por trecho (km/s): ideal + perdas gravitacionais + parcelas fixas, e a margem percentual."""
    dvc = cfg["dv"]
    ideal = caso["ideal"]
    linhas = {
        "saida_terra": ideal["saida_terra"] + _v(dvc["perda_gravitacional"]["saida_terra"]),
        "correcoes_ida": _v(dvc["correcao_trajetoria_por_trecho"]) + _v(dvc["atitude_cruzeiro_por_trecho"]),
        "captura_marte": ideal["captura_marte"] + _v(dvc["perda_gravitacional"]["captura_marte"]),
        "encontro_e_manutencao_marte": _v(dvc["encontro_orbita_marte"]) + _v(dvc["manutencao_orbita_marte"]),
        "saida_marte": ideal["saida_marte"] + _v(dvc["perda_gravitacional"]["saida_marte"]),
        "correcoes_volta": _v(dvc["correcao_trajetoria_por_trecho"]) + _v(dvc["atitude_cruzeiro_por_trecho"]),
        "desvio_orbitador": caso["desvio"],
    }
    return linhas


def _queimas(dv, f, descartado, capsula):
    """Queimas por estágio (em ordem de uso), com descartes de carga."""
    return {
        "saida_terra": [fg.Queima("saida_terra", f * dv["saida_terra"])],
        "insercao_marte": [fg.Queima("correcoes_ida", f * dv["correcoes_ida"]),
                           fg.Queima("captura_marte", f * dv["captura_marte"])],
        "retorno": [fg.Queima("encontro_e_manutencao_marte", f * dv["encontro_e_manutencao_marte"], descarta_antes=descartado),
                    fg.Queima("saida_marte", f * dv["saida_marte"]),
                    fg.Queima("correcoes_volta", f * dv["correcoes_volta"]),
                    fg.Queima("desvio_orbitador", f * dv["desvio_orbitador"], descarta_antes=capsula)],
    }


def dimensionar(variante, cfg, cu, opcao, margem, acrescimo, isp=None, eps=None):
    """Dimensiona uma variante. `variante` = {"tipo": "estagios"|"unico", "dv_por_estagio": {estágio: caso}}.

    Em "estagios", cada estágio usa as queimas do caso indicado para ele (permite pior caso por trecho).
    Em "unico", um só estágio (parâmetros de `estagios.sistema_unico`) faz todas as queimas.
    """
    p = parametros()
    f = 1.0 + margem
    est = cfg["estagios"]
    ate_marte, capsula, descartado = carga(opcao, cu, acrescimo)
    carga_final = ate_marte - descartado - capsula      # o que fica no orbitador até o fim

    def e(nome, queimas):
        s_ = est[nome]
        i_ = _v(s_["isp_s"]) if isp is None else isp[nome]
        x_ = _v(s_["fracao_estrutural"]) if eps is None else eps[nome]
        return fg.Estagio(nome, i_, x_, queimas)

    if variante["tipo"] == "unico":
        # Saída da Terra com estágio próprio; captura e retorno num só estágio de Marte que
        # compartilha o propelente (mesmo Isp e mesma fração estrutural dos estágios de Marte).
        dv = orcamento(variante["caso"], cfg, p)
        q = _queimas(dv, f, descartado, capsula)
        r = fg.dimensionar_veiculo([e("saida_terra", q["saida_terra"]),
                                    e("marte_unico", q["insercao_marte"] + q["retorno"])], carga_final)
        return {"saida_terra": dv, "marte_unico": dv}, r
    dvs = {n: orcamento(c, cfg, p) for n, c in variante["dv_por_estagio"].items()}
    estagios = [e(n, _queimas(dvs[n], f, descartado, capsula)[n]) for n in ("saida_terra", "insercao_marte", "retorno")]
    return dvs, fg.dimensionar_veiculo(estagios, carga_final)


def casos(cfg, p):
    """Missão A, envelope total (ADR 0004) e envelope por estágio (maior Δv de cada trecho)."""
    ms = _ler("results/etapa1.3/missoes.yaml")
    ref = _ler("config/missao_referencia.yaml")
    orb = ref["missao_referencia"]["orbita_marte"]
    pd = cfg["dv"]["desvio"]
    gama, h_seg, ant = _v(pd["gama_entrada_graus"]), _v(pd["periapse_seguro_alt_km"]), _v(pd["antecedencia_dias"]) * 86400

    def ideal(c):
        q = c["por_orbita_marte"][orb]
        return {"saida_terra": c["dv_saida_terra_km_s"], "captura_marte": q["dv_captura_propulsiva_km_s"],
                "saida_marte": q["dv_saida_marte_km_s"]}

    raio_terra = _v(_ler("config/parametros_orbitais.yaml")["raio_terra_km"])

    def desvio(vinf):
        return mn.dv_desvio(p.mu_terra, vinf, p.r_interface_terra, gama, raio_terra + h_seg, ant)

    cand = {c["id"]: c for c in ms["candidatas"]}

    def caso(c):
        return {"descricao": c["id"], "ideal": ideal(c), "desvio": desvio(c["vinf_chegada_terra_km_s"])}

    a = caso(cand[ref["missao_referencia"]["id"]])
    janelas = {j_: caso(cand[v["missao"]]) for j_, v in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].items()}

    def pior(chave):
        return max(janelas.values(), key=lambda c: c["ideal"][chave] if chave != "desvio" else c["desvio"])

    ret = {"descricao": "pior trecho: saída de Marte de " + pior("saida_marte")["descricao"] + ", desvio de "
           + pior("desvio")["descricao"],
           "ideal": {**pior("saida_marte")["ideal"]}, "desvio": pior("desvio")["desvio"]}
    ins = pior("captura_marte")
    sai = pior("saida_terra")
    return a, janelas, {"insercao_marte": ins, "retorno": ret, "saida_terra_pior": sai}


def _nativo(x):
    """Converte tipos do numpy para tipos nativos (para o YAML)."""
    if isinstance(x, dict):
        return {k: _nativo(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_nativo(v) for v in x]
    if hasattr(x, "item"):
        return x.item()
    return x


def variantes(a, janelas, piores):
    """Missão A e as três regras de envelope pedidas no portão (ADR 0004)."""
    return {
        "missao_A": {"tipo": "estagios", "descricao": "missão A em todos os estágios",
                     "dv_por_estagio": {"saida_terra": a, "insercao_marte": a, "retorno": a}},
        "i_sistema_unico": {"tipo": "unico",
                            "descricao": "(i) saída da Terra com estágio próprio + um só estágio para captura e retorno; "
                                         "cada janela com a sua missão, projeto pela pior janela",
                            "por_janela": janelas},
        "ii_estagios_pior_trecho": {"tipo": "estagios", "descricao": "(ii) cada estágio pelo pior caso do seu trecho",
                                    "dv_por_estagio": {"saida_terra": piores["saida_terra_pior"],
                                                       "insercao_marte": piores["insercao_marte"],
                                                       "retorno": piores["retorno"]}},
        "iii_marte_pior_terra_ref": {"tipo": "estagios",
                                     "descricao": "(iii) estágios de Marte pelo pior caso; saída da Terra pela janela de referência (A)",
                                     "dv_por_estagio": {"saida_terra": a, "insercao_marte": piores["insercao_marte"],
                                                        "retorno": piores["retorno"]}},
    }


def massa_leo(var, cfg, cu, opcao, margem, acresc, isp=None, eps=None):
    """(massa na órbita baixa, detalhe). Para o sistema único, o pior caso entre as janelas."""
    if var["tipo"] == "unico":
        res = {}
        for j_, c in var["por_janela"].items():
            try:
                res[j_] = dimensionar({"tipo": "unico", "caso": c}, cfg, cu, opcao, margem, acresc, isp, eps)[1]
            except ValueError:
                return float("nan"), None, None
        j_pior = max(res, key=lambda j_: res[j_][0].massa_inicial)
        return res[j_pior][0].massa_inicial, res[j_pior], j_pior
    r = dimensionar(var, cfg, cu, opcao, margem, acresc, isp, eps)[1]
    return r[0].massa_inicial, r, None


def main():
    cfg = _ler("config/dimensionamento.yaml")
    cu = _ler("config/carga_util.yaml")
    p = parametros()
    base = cfg["caso_base"]
    margem, acresc = _v(cfg["margem_dv"]), float(base["acrescimo_capsula"])
    a, janelas, piores = casos(cfg, p)
    vs = variantes(a, janelas, piores)
    SAIDA.mkdir(parents=True, exist_ok=True)
    br = lambda x, n=0: f"{x:,.{n}f}".replace(",", " ").replace(".", ",")  # noqa: E731
    out = {"gerado_por": "tools/dimensionamento.py", "caso_base": base, "margem_dv": margem,
           "variantes": {}, "sensibilidade": []}

    # 1. Orçamento de Δv por trecho: missão A, mínimos por janela e pior caso por trecho
    colunas = {"A": a, **{f"jan. {k}": c for k, c in janelas.items()}}
    nomes = list(orcamento(a, cfg, p))
    md = ["# Orçamento de Δv por trecho (gerado por tools/dimensionamento.py)", "",
          f"Δv em km/s: ideal (Etapa 1.3) + perdas gravitacionais + parcelas fixas. Margem de {br(100 * margem)} % "
          "aplicada a todos os trechos (P-014, NÃO VALIDADA). Colunas: missão A e o mínimo admissível de cada janela "
          "(ADR 0004). A última coluna é o pior caso de cada trecho entre as janelas.", "",
          "| Trecho | " + " | ".join(colunas) + " | Pior caso do trecho |", "| :- |" + " -: |" * (len(colunas) + 1)]
    tot = {k: 0.0 for k in colunas}
    tot_pior = 0.0
    for n in nomes:
        vals = {k: orcamento(c, cfg, p)[n] for k, c in colunas.items()}
        pior_n = max(orcamento(c, cfg, p)[n] for c in janelas.values())
        tot_pior += pior_n
        for k in colunas:
            tot[k] += vals[k]
        md.append(f"| {n} | " + " | ".join(br(vals[k], 3) for k in colunas) + f" | {br(pior_n, 3)} |")
    md.append("| **Total sem margem** | " + " | ".join(f"**{br(tot[k], 3)}**" for k in colunas) + f" | **{br(tot_pior, 3)}** |")
    md.append(f"| **Total com margem** | " + " | ".join(f"**{br(tot[k] * (1 + margem), 3)}**" for k in colunas)
              + f" | **{br(tot_pior * (1 + margem), 3)}** |")
    (SAIDA / "orcamento_dv.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    out["orcamento_total_km_s"] = {k: round(v, 4) for k, v in tot.items()} | {"pior_por_trecho": round(tot_pior, 4)}

    # 2. Variantes no caso base
    md2 = ["# Dimensionamento por estágios (gerado por tools/dimensionamento.py)", "",
           f"Carga útil {base['carga_util']}, margem de Δv {br(100 * margem)} %, acréscimo na cápsula "
           f"{br(100 * acresc)} %. Massas em kg. Só trechos no espaço (descida, pouso e subida: Fase 2).", ""]
    for k, var in vs.items():
        m, r, j_pior = massa_leo(var, cfg, cu, base["carga_util"], margem, acresc)
        reg = {"descricao": var["descricao"], "massa_orbita_baixa_kg": None if r is None else round(m, 1)}
        md2 += [f"## {k}: {var['descricao']}" + (f" (janela que define: {j_pior})" if j_pior else ""), ""]
        if r is None:
            md2 += ["**Inviável** com o Isp e a fração estrutural do sistema único.", ""]
        else:
            reg["estagios"] = [{"nome": s_.nome, "propelente_kg": round(s_.propelente, 1), "inerte_kg": round(s_.inerte, 1),
                                "massa_inicial_kg": round(s_.massa_inicial, 1)} for s_ in r]
            md2 += ["| Estágio | Propelente | Inerte | Massa inicial (com o que carrega) |", "| :- | -: | -: | -: |"]
            md2 += [f"| {s_.nome} | {br(s_.propelente)} | {br(s_.inerte)} | {br(s_.massa_inicial)} |" for s_ in r]
            md2 += [f"| **Massa na órbita baixa da Terra** | | | **{br(m)}** |", ""]
        if j_pior:
            reg["janela_que_define"] = j_pior
        out["variantes"][k] = reg

    # 3. Sensibilidade
    sens = cfg["sensibilidade"]
    md2 += ["## Sensibilidade da massa na órbita baixa (kg)", "",
            "Cada linha muda um parâmetro e mantém os demais no caso base.", "",
            "| Parâmetro | Valor | " + " | ".join(vs) + " |", "| :- | :- |" + " -: |" * len(vs)]

    def linha(rotulo, valor, **kw):
        res = {k: massa_leo(v, cfg, cu, kw.get("opcao", base["carga_util"]), kw.get("margem", margem),
                            kw.get("acresc", acresc), kw.get("isp"), kw.get("eps"))[0] for k, v in vs.items()}
        out["sensibilidade"].append({"parametro": rotulo, "valor": valor,
                                     "massa_orbita_baixa_kg": {k: (round(v, 1) if v == v else None) for k, v in res.items()}})
        md2.append(f"| {rotulo} | {valor} | " + " | ".join(br(res[k]) if res[k] == res[k] else "inviável" for k in vs) + " |")

    for op in sens["carga_util"]:
        linha("Carga útil", op, opcao=op)
    for m in sens["margem_dv"]:
        linha("Margem de Δv", f"{br(100 * m)} %", margem=m)
    for x in sens["acrescimo_capsula"]:
        linha("Acréscimo na massa da cápsula", f"{br(100 * x)} %", acresc=x)
    isp0 = {n: _v(s_["isp_s"]) for n, s_ in cfg["estagios"].items()}
    eps0 = {n: _v(s_["fracao_estrutural"]) for n, s_ in cfg["estagios"].items()}
    for d in sens["delta_isp_relativo"]:
        linha("Isp de todos os estágios", f"{'+' if d >= 0 else ''}{br(100 * d)} %", isp={n: v * (1 + d) for n, v in isp0.items()})
    for x in sens["fracao_estrutural_multiplicador"]:
        linha("Frações estruturais × fator", br(x, 2), eps={n: v * x for n, v in eps0.items()})
    (SAIDA / "dimensionamento.md").write_text("\n".join(md2) + "\n", encoding="utf-8")
    (SAIDA / "dimensionamento.yaml").write_text(yaml.safe_dump(_nativo(out), sort_keys=False, allow_unicode=True),
                                                encoding="utf-8")
    print((SAIDA / "orcamento_dv.md").read_text(encoding="utf-8"))
    print((SAIDA / "dimensionamento.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
