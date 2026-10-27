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

from orbital.config import ler, nativo, parametros, v  # noqa: E402
from orbital.dimensionamento import (carga, casos, dimensionar, massa_leo, orcamento, queimas_por_estagio,  # noqa: E402,F401
                                     variantes)

SAIDA = RAIZ / "results" / "etapa1.4"


_ler, _v, _nativo = ler, v, nativo
_queimas = queimas_por_estagio


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
           "regra_projeto": cfg["regra_projeto"], "plataforma_orbitador_kg": _v(cfg["plataforma_orbitador_kg"]),
           "variantes": {}, "sensibilidade": []}

    # 1. Orçamento de Δv por trecho: missão A, mínimos por janela e pior caso por trecho
    colunas = {"A": a, **{f"jan. {k}": c for k, c in janelas.items()}}
    nomes = list(orcamento(a, cfg, p))
    md = ["# Orçamento de Δv por trecho (gerado por tools/dimensionamento.py)", "",
          f"Δv em km/s: ideal (Etapa 1.3) + perdas gravitacionais + parcelas fixas. Margem de {br(100 * margem)} % "
          "aplicada a todos os trechos (P-014, NÃO VALIDADA). Colunas: missão A e o mínimo admissível de cada janela "
          "(ADR 0004). Penúltima coluna: pior caso de cada trecho entre as janelas. Última: Δv de projeto pela regra "
          f"`{cfg['regra_projeto']}` (ADR 0004).", "",
          "| Trecho | " + " | ".join(colunas) + " | Pior caso do trecho |", "| :- |" + " -: |" * (len(colunas) + 1)]
    # Coluna de projeto: cada trecho pelo caso que a regra de projeto atribui ao estágio que o executa.
    reg = vs[cfg["regra_projeto"]]
    estagio_do_trecho = {"saida_terra": "saida_terra", "correcoes_ida": "insercao_marte", "captura_marte": "insercao_marte",
                         "encontro_e_manutencao_marte": "retorno", "saida_marte": "retorno", "correcoes_volta": "retorno",
                         "desvio_orbitador": "retorno"}
    md[-2] = md[-2] + " Projeto (regra de projeto) |"
    md[-1] = md[-1] + " -: |"
    tot = {k: 0.0 for k in colunas}
    tot_pior = tot_proj = 0.0
    for n in nomes:
        vals = {k: orcamento(c, cfg, p)[n] for k, c in colunas.items()}
        pior_n = max(orcamento(c, cfg, p)[n] for c in janelas.values())
        proj_n = orcamento(reg["dv_por_estagio"][estagio_do_trecho[n]], cfg, p)[n]
        tot_pior += pior_n
        tot_proj += proj_n
        for k in colunas:
            tot[k] += vals[k]
        md.append(f"| {n} | " + " | ".join(br(vals[k], 3) for k in colunas) + f" | {br(pior_n, 3)} | {br(proj_n, 3)} |")
    md.append("| **Total sem margem** | " + " | ".join(f"**{br(tot[k], 3)}**" for k in colunas)
              + f" | **{br(tot_pior, 3)}** | **{br(tot_proj, 3)}** |")
    md.append(f"| **Total com margem** | " + " | ".join(f"**{br(tot[k] * (1 + margem), 3)}**" for k in colunas)
              + f" | **{br(tot_pior * (1 + margem), 3)}** | **{br(tot_proj * (1 + margem), 3)}** |")
    (SAIDA / "orcamento_dv.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    out["orcamento_total_km_s"] = ({k: round(v, 4) for k, v in tot.items()}
                                   | {"pior_por_trecho": round(tot_pior, 4), "projeto": round(tot_proj, 4),
                                      "projeto_com_margem": round(tot_proj * (1 + margem), 4)})

    # 2. Variantes no caso base
    md2 = ["# Dimensionamento por estágios (gerado por tools/dimensionamento.py)", "",
           f"Carga útil {base['carga_util']}, margem de Δv {br(100 * margem)} %, acréscimo na cápsula "
           f"{br(100 * acresc)} %, plataforma do orbitador {br(_v(cfg['plataforma_orbitador_kg']))} kg (P-016). "
           f"Massas em kg. Só trechos no espaço (descida, pouso e subida: Fase 2). "
           f"Regra de projeto (ADR 0004): `{cfg['regra_projeto']}`.", ""]
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
                            kw.get("acresc", acresc), kw.get("isp"), kw.get("eps"), kw.get("plataforma"))[0]
               for k, v in vs.items()}
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
    for x in sens["plataforma_orbitador_kg"]:
        linha("Plataforma do orbitador", f"{br(x, 1)} kg", plataforma=x)
    (SAIDA / "dimensionamento.md").write_text("\n".join(md2) + "\n", encoding="utf-8")
    (SAIDA / "dimensionamento.yaml").write_text(yaml.safe_dump(_nativo(out), sort_keys=False, allow_unicode=True),
                                                encoding="utf-8")
    print((SAIDA / "orcamento_dv.md").read_text(encoding="utf-8"))
    print((SAIDA / "dimensionamento.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
