"""Camada de dados do painel: lê results/ e config/ e chama funções testadas de src/orbital. Sem Streamlit aqui.

Regra do painel: nenhum número é digitado aqui. Cada número exibido sai como `Valor`, com um rótulo:
  - "verificado contra dados publicados": comparação com uma fonte publicada (results/etapa1.2/verificacao_*);
  - "calculado": saída das ferramentas do estudo ou de src/orbital;
  - "premissa <status>": valor de config/premissas.yaml, com o status lido do arquivo (hoje, todas NÃO VALIDADAS).
"""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np

from orbital import ephemeris as eph
from orbital import kepler, lambert
from orbital import porkchop as pc
from orbital.config import RAIZ, ler, v
from orbital.constantes import GM_SOL, UA_KM
from orbital.lancamento import pior_margem_a
from orbital.veiculos import veiculos

VERIFICADO = "verificado contra dados publicados"
CALCULADO = "calculado"
REPO_GITHUB = "https://github.com/fasn98/MarsMission/blob/main/"


@dataclass(frozen=True)
class Valor:
    """Número exibido no painel com unidade, rótulo e origem (arquivo de results/, item do config ou premissa)."""
    valor: float
    unidade: str
    rotulo: str
    origem: str
    premissas: tuple = field(default=())


# ---------------------------------------------------------------- premissas e decisões

@lru_cache(maxsize=1)
def premissas() -> tuple:
    """As premissas de config/premissas.yaml, na ordem do arquivo."""
    return tuple(ler("config/premissas.yaml")["premissas"])


def premissa(pid: str) -> dict:
    for p in premissas():
        if p["id"] == pid:
            return p
    raise KeyError(pid)


def rotulo_premissa(pid: str) -> str:
    """Rótulo de um valor que é premissa: "premissa " + status lido do arquivo (ex.: "premissa NÃO VALIDADA")."""
    return f"premissa {premissa(pid)['status']}"


def premissas_citadas(texto: str) -> tuple:
    return tuple(sorted(set(re.findall(r"P-\d{3}", texto))))


def adrs() -> list[dict]:
    """ADRs de docs/adr/: número, título, status (linha "Status:"), caminho, link no GitHub e texto."""
    out = []
    for p in sorted((RAIZ / "docs" / "adr").glob("[0-9][0-9][0-9][0-9]-*.md")):
        txt = p.read_text(encoding="utf-8")
        titulo = txt.splitlines()[0].lstrip("# ").strip()
        st = re.search(r"^Status:\s*(.+)$", txt, flags=re.M)
        rel = p.relative_to(RAIZ).as_posix()
        out.append({"numero": p.name[:4], "titulo": titulo, "status": st.group(1).strip() if st else "",
                    "caminho": rel, "url": REPO_GITHUB + rel, "texto": txt})
    return out


def valor_config(item: dict, unidade: str, origem: str) -> Valor:
    """Valor de um item do config: rótulo de premissa se o item cita uma; senão, dado de fonte publicada."""
    if "premissa" in item:
        return Valor(v(item), unidade, rotulo_premissa(item["premissa"]), origem, (item["premissa"],))
    fonte = re.search(r"\[F\d+\]", str(item.get("fonte", "")))   # a primeira citada é a do valor; as demais são comparações
    if fonte is None:
        raise ValueError(f"item de {origem} sem premissa e sem fonte citada")
    return Valor(v(item), unidade, "dado de fonte publicada " + fonte.group(0), origem)


# ---------------------------------------------------------------- missão de referência

def missao_referencia() -> dict:
    """Cronograma (TDB), durações, Δv e reentrada da missão de referência (results/etapa1.3/missoes.yaml)."""
    ms = ler("results/etapa1.3/missoes.yaml")
    ref = ms["missao_referencia"]
    c = next(x for x in ms["candidatas"] if x["id"] == ref["id"])
    orb = c["por_orbita_marte"][ref["orbita_marte"]]
    o = "results/etapa1.3/missoes.yaml"
    calc = lambda x, u: Valor(float(x), u, CALCULADO, o)  # noqa: E731
    return {
        "id": ref["id"], "orbita_marte": ref["orbita_marte"], "captura": ref["captura"],
        "eventos": [("Partida da Terra", c["partida_terra"]), ("Chegada a Marte", c["chegada_marte"]),
                    ("Partida de Marte", c["partida_marte"]), ("Chegada à Terra", c["chegada_terra"])],
        "duracoes": {"Ida": calc(c["ida_dias"], "d"), "Em Marte": calc(c["em_marte_dias"], "d"),
                     "Volta": calc(c["volta_dias"], "d"), "Total": calc(c["total_dias"], "d")},
        "dv": {"Saída da Terra (da órbita baixa)": calc(c["dv_saida_terra_km_s"], "km/s"),
               "Captura em Marte (propulsiva)": calc(orb["dv_captura_propulsiva_km_s"], "km/s"),
               "Saída de Marte": calc(orb["dv_saida_marte_km_s"], "km/s"),
               "Total propulsivo": calc(orb["dv_total_sem_aerocaptura_km_s"], "km/s")},
        "partida": {"C3": calc(c["c3_km2_s2"], "km²/s²"), "DLA": calc(c["dla_graus"], "°"),
                    "C3L de partida de Marte": calc(c["c3l_partida_marte_km2_s2"], "km²/s²")},
        "reentrada": {"v∞ de chegada à Terra": calc(c["vinf_chegada_terra_km_s"], "km/s"),
                      "Velocidade de reentrada": calc(c["v_reentrada_km_s"], "km/s"),
                      "Limite de reentrada (P-011)": Valor(float(ms["parametros"]["v_reentrada_max_km_s"]), "km/s",
                                                           rotulo_premissa("P-011"), o + " (parametros, de config/parametros_orbitais.yaml)",
                                                           ("P-011",))},
        "envelope": Valor(float(ms["envelope_dimensionamento"]["dv_total_km_s"]), "km/s", CALCULADO, o),
        "envelope_missao": ms["envelope_dimensionamento"]["missao_que_define"],
        "janelas_envelope": list(ms["envelope_dimensionamento"]["regra"]["janelas"]),
    }


def verificacoes() -> list[dict]:
    """Comparações com dados publicados (Etapa 1.2): NASA/TM-2010-216764 e JPL 82-43 Parte 5, nas datas publicadas."""
    out = []
    b = ler("results/etapa1.2/verificacao_burke2010.yaml")
    for x in b["linhas"]:
        for g, u in (("c3", "km²/s²"), ("vinf", "km/s")):
            pub, calc = float(x["nasa"][g]), float(x["nas_datas_nasa"][g])
            out.append({"fonte": f"{b['fonte']}, tabela {x['nasa']['tabela']}, p. {x['nasa']['pagina']}",
                        "janela": x["janela"], "tipo": x["tipo"], "grandeza": "C3" if g == "c3" else "v∞ de chegada",
                        "datas": f"{x['nasa']['partida']} → {x['nasa']['chegada']}",
                        "publicado": Valor(pub, u, "dado publicado", b["fonte"]),
                        "calculado": Valor(calc, u, VERIFICADO, "results/etapa1.2/verificacao_burke2010.yaml"),
                        "dif_rel": (calc - pub) / pub})
    j = ler("results/etapa1.2/verificacao_jpl8243.yaml")
    for x in j["linhas"]:
        pub, calc = float(x["jpl"]["valor"]), float(x["nas_datas_jpl"]["valor"])
        u = "km²/s²" if x["grandeza"] == "c3" else "km/s"
        out.append({"fonte": f"{j['fonte']}, p. {x['jpl']['pagina']}", "janela": x["janela"], "tipo": x["tipo"],
                    "grandeza": "C3L" if x["grandeza"] == "c3" else "VHP", "datas": f"{x['jpl']['partida']} → {x['jpl']['chegada']}",
                    "publicado": Valor(pub, u, "dado publicado", j["fonte"]),
                    "calculado": Valor(calc, u, VERIFICADO, "results/etapa1.2/verificacao_jpl8243.yaml"),
                    "dif_rel": (calc - pub) / pub})
    return out


# ---------------------------------------------------------------- arquitetura

_PREMISSA_DO_ITEM = (("Plataforma (P-016", "P-016"), ("Plataforma de superfície L3", "P-017"),
                     ("Braço de coleta", "P-034"), ("Helicópteros", "P-038"))


def _rotular_item(x: dict, origem: str) -> dict:
    """Item da composição de um veículo: massa da plataforma = premissa; o resto é calculado."""
    pid = next((p for pref, p in _PREMISSA_DO_ITEM if x["item"].startswith(pref)), None)
    out = {"item": x["item"]}
    for k, nome in (("propelente_kg", "propelente"), ("inerte_kg", "inerte"), ("massa_kg", "massa")):
        if k in x:
            if pid and k == "massa_kg":
                out[nome] = Valor(float(x[k]), "kg", rotulo_premissa(pid), origem, (pid,))
            else:
                out[nome] = Valor(float(x[k]), "kg", CALCULADO, origem, premissas_citadas(x["item"]))
    return out


def arquitetura() -> dict:
    """Composição dos veículos, lançadores e margens e número de lançamentos (results/etapa2.5/arquitetura.yaml)."""
    o = "results/etapa2.5/arquitetura.yaml"
    a = ler(o)
    calc = lambda x, u: Valor(float(x), u, CALCULADO, o)  # noqa: E731
    return {
        "missao_referencia": a["missao_referencia"],
        "orbita_encontro_km": [calc(x, "km") for x in a["orbita_encontro_km"]],
        "envelope": calc(a["envelope_dv_km_s"], "km/s"),
        "orbitador": {"composicao": [_rotular_item(x, o) for x in a["orbitador"]["composicao"]],
                      "injetado": calc(a["orbitador"]["injetado_kg"], "kg")},
        "lander": {"composicao": [_rotular_item(x, o) for x in a["lander"]["composicao"]],
                   "injetado": calc(a["lander"]["injetado_kg"], "kg"),
                   "entrada": calc(a["lander"]["massa_entrada_kg"], "kg"),
                   "pousada": calc(a["lander"]["massa_pousada_kg"], "kg")},
        "margens": {veic: {n: calc(m, "") for n, m in d.items()} for veic, d in a["lancadores"]["margens_base"].items()},
        "lancamentos": calc(a["lancamentos"], ""),
        "cronograma": a["cronograma"],
    }


# ---------------------------------------------------------------- orçamento de massa com controles

ARMAZENAVEIS = ("insercao_marte", "retorno", "marte_unico")


def controles_base() -> dict:
    """Valores de base dos controles deslizantes, com rótulo e faixa (limites lidos de results/ e config/)."""
    d, s = ler("config/dimensionamento.yaml"), ler("config/superficie.yaml")
    pl = ler("results/etapa2.3/plataformas.yaml")
    st = d["estagios"]["insercao_marte"]
    return {
        "plataforma_lander_kg": {"base": valor_config(s["lander"]["plataforma_superficie_kg"], "kg", "config/superficie.yaml"),
                                 "faixa": (float(pl["lander"]["L1"]["prevista_kg"]["e1_medio"]),
                                           float(pl["lander"]["limite_superior_srl_2024_kg"])),
                                 "faixa_origem": "results/etapa2.3/plataformas.yaml: L1 (E1 médio) a SRL 2024 − MAV"},
        "margem_dv": {"base": valor_config(d["margem_dv"], "", "config/dimensionamento.yaml"),
                      "faixa": (min(d["sensibilidade"]["margem_dv"]), max(d["sensibilidade"]["margem_dv"])),
                      "faixa_origem": "config/dimensionamento.yaml: faixa de sensibilidade da Etapa 1.4"},
        "isp_armazenavel_s": {"base": valor_config(st["isp_s"], "s", "config/dimensionamento.yaml (MMH/MON)"),
                              "faixa": tuple(v(st["isp_s"]) * (1 + x) for x in d["sensibilidade"]["delta_isp_relativo"]),
                              "faixa_origem": "config/dimensionamento.yaml: faixa de sensibilidade da Etapa 1.4 (Isp × "
                                              + " a × ".join(f"{1 + x:g}" for x in d["sensibilidade"]["delta_isp_relativo"]) + ")"},
        "fracao_estrutural_armazenavel": {"base": valor_config(st["fracao_estrutural"], "", "config/dimensionamento.yaml (MMH/MON)"),
                                          "faixa": tuple(v(st["fracao_estrutural"]) * x for x in d["sensibilidade"]["fracao_estrutural_multiplicador"]),
                                          "faixa_origem": "config/dimensionamento.yaml: faixa de sensibilidade da Etapa 1.4 (× "
                                                          + " a × ".join(f"{x:g}" for x in d["sensibilidade"]["fracao_estrutural_multiplicador"]) + ")"},
    }


def orcamento(plataforma_lander_kg=None, margem_dv=None, isp_armazenavel_s=None, fracao_estrutural_armazenavel=None) -> dict:
    """Recalcula orbitador e lander com orbital.veiculos e as margens de injeção direta (ADR 0008) de cada lançador.

    Isp e fração estrutural valem para os estágios armazenáveis (MMH/MON): inserção em Marte, retorno e cruzeiro do
    lander. A órbita de encontro fica a de base (como na sensibilidade da Etapa 2.5). Sem argumentos, reproduz
    results/etapa2.5/arquitetura.yaml."""
    d, s, lcfg = ler("config/dimensionamento.yaml"), ler("config/superficie.yaml"), ler("config/lancadores.yaml")
    d, s = copy.deepcopy(d), copy.deepcopy(s)
    if margem_dv is not None:
        d["margem_dv"]["valor"] = float(margem_dv)
    for chave, valor in (("isp_s", isp_armazenavel_s), ("fracao_estrutural", fracao_estrutural_armazenavel)):
        if valor is None:
            continue
        for n in ARMAZENAVEIS:
            d["estagios"][n] = copy.deepcopy(d["estagios"][n])   # as âncoras YAML compartilham o mesmo dict
            d["estagios"][n][chave] = {**d["estagios"][n][chave], "valor": float(valor)}
        s["lancamento"]["cruzeiro_lander"][chave] = {**s["lancamento"]["cruzeiro_lander"][chave], "valor": float(valor)}
    try:
        vei, janelas, _ = veiculos(plataforma_lander_kg, d, s)
    except ValueError as e:   # Δv acima do que o estágio consegue com esse Isp e essa fração estrutural
        return {"viavel": False, "erro": str(e)}
    origem = "orbital.veiculos (recalculado no painel)"
    res = {"viavel": True, "veiculos": {}, "lancadores": []}
    for veic, chave in (("orbitador", "orbitador_regra_iii"), ("lander", "lander")):
        x = vei[chave]
        res["veiculos"][veic] = {"injetado": Valor(float(x["injetada_kg"]), "kg", CALCULADO, origem),
                                 "estagios": [{"nome": e["nome"], "propelente": Valor(float(e["propelente_kg"]), "kg", CALCULADO, origem),
                                               "inerte": Valor(float(e["inerte_kg"]), "kg", CALCULADO, origem)}
                                              for e in x["estagios"][1:]]}   # [0] é a saída da Terra, que não voa na forma (a)
        if veic == "lander":
            res["veiculos"][veic].update({k: Valor(float(x[c]), "kg", CALCULADO, origem) for k, c in
                                          (("entrada", "massa_entrada_kg"), ("pousada", "massa_pousada_kg"),
                                           ("mav", "mav_e_aquecimento_kg"), ("plataforma", "plataforma_kg"))})
        for nome, lan in lcfg["lancadores"].items():
            m, jan = pior_margem_a(nome, x["injetada_kg"], janelas, lcfg)
            res["lancadores"].append({"veiculo": veic, "lancador": nome, "categoria": lan["categoria"],
                                      "escolhido": nome in lcfg["escolha"][veic],
                                      "margem": None if m is None else Valor(float(m), "", CALCULADO, origem),
                                      "janela": jan, "serve": m is not None and m >= 0})
    return res


# ---------------------------------------------------------------- porkchops

def porkchops() -> dict:
    """Índice das grades exportadas por tools/exporta_painel.py (results/painel/porkchops.yaml)."""
    return ler("results/painel/porkchops.yaml")


def porkchop(sentido: str, janela: str) -> dict:
    """Grade de uma janela: datas TDB, C3, v∞ de chegada, tempo de voo, ângulo e (na ida) DLA."""
    arq = porkchops()["sentidos"][sentido]["janelas"][janela]["arquivo"]
    with np.load(RAIZ / "results" / "painel" / arq) as z:
        return {k: z[k] for k in z.files}


def minimos(sentido: str) -> dict:
    """Mínimos de C3 e de v∞ por tipo e janela (results/etapa1.2/minimos_<sentido>.yaml, tools/porkchop.py)."""
    return ler(f"results/etapa1.2/minimos_{sentido}.yaml")["janelas"]


def mascara_porkchop(g: dict, c3_max: float) -> np.ndarray:
    """Pontos escondidos no desenho, como em tools/porkchop.py: C3 acima do teto e ±P-006 em torno de 180°."""
    excl = float(premissa("P-006")["valor"])
    perto_180 = np.abs(np.nan_to_num(g["angulo_transf_graus"], nan=180.0) - 180.0) <= excl
    return perto_180 | ~(g["c3_km2_s2"] <= c3_max)


# ---------------------------------------------------------------- trajetória heliocêntrica

def kernels_presentes() -> bool:
    return all(p.exists() for p in eph.kernels_configurados())


def trajetoria(pontos_arco: int = 200, passo_planetas_dias: float = 2.0) -> dict:
    """Trajetória 2D (plano da eclíptica J2000, em UA) da missão de referência: Terra e Marte nas datas reais (DE440)
    e os arcos de Lambert da ida e da volta, propagados por Kepler. Precisa dos kernels (tools/fetch_kernels.py)."""
    eph.carregar_kernels()
    m = missao_referencia()
    datas = dict(m["eventos"])
    et = {k: eph.tdb_para_et(d) for k, d in datas.items()}
    t0, t1 = et["Partida da Terra"], et["Chegada à Terra"]
    ts = np.arange(t0, t1 + 1, passo_planetas_dias * pc.DIA)
    planeta = lambda corpo: np.array([pc.estado_corpo(corpo, t)[:3] for t in ts]) / UA_KM  # noqa: E731

    def arco(c1, c2, e1, e2):
        s1, s2 = pc.estado_corpo(c1, e1), pc.estado_corpo(c2, e2)
        sol = lambert.resolver(GM_SOL, s1[:3], s2[:3], e2 - e1)
        dts = np.linspace(0.0, e2 - e1, pontos_arco)
        r = np.array([s1[:3]] + [kepler.propagar(GM_SOL, s1[:3], sol.v1, dt)[0] for dt in dts[1:]])
        return r / UA_KM, s2[:3] / UA_KM

    ida, marte_cheg = arco(eph.TERRA, eph.BARICENTRO_MARTE, et["Partida da Terra"], et["Chegada a Marte"])
    volta, terra_cheg = arco(eph.BARICENTRO_MARTE, eph.TERRA, et["Partida de Marte"], et["Chegada à Terra"])
    eventos = []
    for nome, d in m["eventos"]:
        eventos.append({"evento": nome, "data_tdb": d,
                        "terra": pc.estado_corpo(eph.TERRA, et[nome])[:3] / UA_KM,
                        "marte": pc.estado_corpo(eph.BARICENTRO_MARTE, et[nome])[:3] / UA_KM})
    return {"terra": planeta(eph.TERRA), "marte": planeta(eph.BARICENTRO_MARTE),
            "datas_planetas": [eph.data_tdb(t) for t in ts], "ida": ida, "volta": volta, "eventos": eventos,
            "erro_chegada_ida_km": float(np.linalg.norm(ida[-1] - marte_cheg)) * UA_KM,
            "erro_chegada_volta_km": float(np.linalg.norm(volta[-1] - terra_cheg)) * UA_KM,
            "referencial": "ECLIPJ2000, centro no Sol (plano x–y da eclíptica)"}


def ler_texto(caminho: str) -> str:
    return (RAIZ / caminho).read_text(encoding="utf-8")


def existe(caminho: str) -> bool:
    return Path(RAIZ / caminho).exists()
