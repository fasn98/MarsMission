"""Orçamento de Δv por trecho e dimensionamento por estágios (Etapa 1.4, Parte B), usados pelas Etapas 2.x e pelo painel.

Movido de tools/dimensionamento.py sem mudança de física (prova: results/conferencia/regeneracao_refatoracao.md,
tools/confere_regeneracao.py). Lê config/ e results/etapa1.3/missoes.yaml pela raiz do repositório (orbital.config).

Arquitetura (só trechos no espaço):
  1. Estágio de saída da Terra: injeção trans-Marte a partir da órbita baixa. Descartado.
  2. Módulo de inserção em Marte: correções da ida e captura. Descartado em Marte.
  3. Estágio de retorno: encontro e manutenção em órbita de Marte, injeção trans-Terra, correções
     da volta; solta a cápsula e faz o desvio. Leva a carga útil até o fim.
"""

from __future__ import annotations

from orbital import foguete as fg
from orbital import manobras as mn
from orbital.config import ler, parametros, v


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
        "saida_terra": ideal["saida_terra"] + v(dvc["perda_gravitacional"]["saida_terra"]),
        "correcoes_ida": v(dvc["correcao_trajetoria_por_trecho"]) + v(dvc["atitude_cruzeiro_por_trecho"]),
        "captura_marte": ideal["captura_marte"] + v(dvc["perda_gravitacional"]["captura_marte"]),
        "encontro_e_manutencao_marte": v(dvc["encontro_orbita_marte"]) + v(dvc["manutencao_orbita_marte"]),
        "saida_marte": ideal["saida_marte"] + v(dvc["perda_gravitacional"]["saida_marte"]),
        "correcoes_volta": v(dvc["correcao_trajetoria_por_trecho"]) + v(dvc["atitude_cruzeiro_por_trecho"]),
        "desvio_orbitador": caso["desvio"],
    }
    return linhas


def queimas_por_estagio(dv, f, descartado, capsula):
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


def dimensionar(variante, cfg, cu, opcao, margem, acrescimo, isp=None, eps=None, plataforma=None):
    """Dimensiona uma variante. `variante` = {"tipo": "estagios"|"unico", "dv_por_estagio": {estágio: caso}}.

    Em "estagios", cada estágio usa as queimas do caso indicado para ele (permite pior caso por trecho).
    Em "unico", um só estágio (parâmetros de `estagios.sistema_unico`) faz todas as queimas.
    """
    p = parametros()
    f = 1.0 + margem
    est = cfg["estagios"]
    ate_marte, capsula, descartado = carga(opcao, cu, acrescimo)
    plat = v(cfg["plataforma_orbitador_kg"]) if plataforma is None else plataforma
    carga_final = ate_marte - descartado - capsula + plat   # o que fica no orbitador até o fim

    def e(nome, queimas):
        s_ = est[nome]
        i_ = v(s_["isp_s"]) if isp is None else isp[nome]
        x_ = v(s_["fracao_estrutural"]) if eps is None else eps[nome]
        return fg.Estagio(nome, i_, x_, queimas)

    if variante["tipo"] == "unico":
        # Saída da Terra com estágio próprio; captura e retorno num só estágio de Marte que
        # compartilha o propelente (mesmo Isp e mesma fração estrutural dos estágios de Marte).
        dv = orcamento(variante["caso"], cfg, p)
        q = queimas_por_estagio(dv, f, descartado, capsula)
        r = fg.dimensionar_veiculo([e("saida_terra", q["saida_terra"]),
                                    e("marte_unico", q["insercao_marte"] + q["retorno"])], carga_final)
        return {"saida_terra": dv, "marte_unico": dv}, r
    dvs = {n: orcamento(c, cfg, p) for n, c in variante["dv_por_estagio"].items()}
    estagios = [e(n, queimas_por_estagio(dvs[n], f, descartado, capsula)[n]) for n in ("saida_terra", "insercao_marte", "retorno")]
    return dvs, fg.dimensionar_veiculo(estagios, carga_final)


def casos(cfg, p):
    """Missão A, envelope total (ADR 0004) e envelope por estágio (maior Δv de cada trecho)."""
    ms = ler("results/etapa1.3/missoes.yaml")
    ref = ler("config/missao_referencia.yaml")
    orb = ref["missao_referencia"]["orbita_marte"]
    pd = cfg["dv"]["desvio"]
    gama, h_seg, ant = v(pd["gama_entrada_graus"]), v(pd["periapse_seguro_alt_km"]), v(pd["antecedencia_dias"]) * 86400

    def ideal(c):
        q = c["por_orbita_marte"][orb]
        return {"saida_terra": c["dv_saida_terra_km_s"], "captura_marte": q["dv_captura_propulsiva_km_s"],
                "saida_marte": q["dv_saida_marte_km_s"]}

    raio_terra = v(ler("config/parametros_orbitais.yaml")["raio_terra_km"])

    def desvio(vinf):
        return mn.dv_desvio(p.mu_terra, vinf, p.r_interface_terra, gama, raio_terra + h_seg, ant)

    cand = {c["id"]: c for c in ms["candidatas"]}

    def caso(c):
        return {"descricao": c["id"], "ideal": ideal(c), "desvio": desvio(c["vinf_chegada_terra_km_s"])}

    a = caso(cand[ref["missao_referencia"]["id"]])
    janelas = {j_: caso(cand[w["missao"]]) for j_, w in ms["envelope_dimensionamento"]["minimo_admissivel_por_janela"].items()}

    def pior(chave):
        return max(janelas.values(), key=lambda c: c["ideal"][chave] if chave != "desvio" else c["desvio"])

    ret = {"descricao": "pior trecho: saída de Marte de " + pior("saida_marte")["descricao"] + ", desvio de "
           + pior("desvio")["descricao"],
           "ideal": {**pior("saida_marte")["ideal"]}, "desvio": pior("desvio")["desvio"]}
    ins = pior("captura_marte")
    sai = pior("saida_terra")
    return a, janelas, {"insercao_marte": ins, "retorno": ret, "saida_terra_pior": sai}


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


def massa_leo(var, cfg, cu, opcao, margem, acresc, isp=None, eps=None, plataforma=None):
    """(massa na órbita baixa, detalhe). Para o sistema único, o pior caso entre as janelas."""
    if var["tipo"] == "unico":
        res = {}
        for j_, c in var["por_janela"].items():
            try:
                res[j_] = dimensionar({"tipo": "unico", "caso": c}, cfg, cu, opcao, margem, acresc, isp, eps, plataforma)[1]
            except ValueError:
                return float("nan"), None, None
        j_pior = max(res, key=lambda j_: res[j_][0].massa_inicial)
        return res[j_pior][0].massa_inicial, res[j_pior], j_pior
    r = dimensionar(var, cfg, cu, opcao, margem, acresc, isp, eps, plataforma)[1]
    return r[0].massa_inicial, r, None
