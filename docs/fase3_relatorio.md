# Fase 3: propulsão (relatório)

Estudo conceitual (Pré-Fase A) MarsMission. Autor e decisor: Fabio Nogueira. Os números vêm de `results/`, gerados
por `tools/` a partir de `config/`, e de lá são citados com o arquivo. Nada aqui é "validado". "Verificado" só quando
há comparação com dado publicado.

## 1. Resultado em uma página
- **Motores químicos com voo** (Etapa 3.1, ADR 0011):
  - captura C2 (8 × R-4D-11) e retorno R3 (4 × R-4D-11);
  - MAV M2/N2 (R-4D-11) e cruzeiro do lander Z1 (4 × 10N);
  - Isp de voo de 310 s e de 292 s.
- **Perdas de queima finita calculadas** (várias queimas no periapse): captura de 72,6 m/s e saída de Marte de
  56,4 m/s, contra 18 e 11 m/s do DRA (P-015) (`results/etapa3.1/perdas_calculadas.md`).
- **MAV:** fração estrutural do MAV hipergólico pressurizado, ε = 0,230 [F46] (ADR 0007, nota de 2026-10-28).
- **Modelo de baixo empuxo** (Etapa 3.2, ADR 0012):
  - espiral numérica e solução analítica quase circular, conferidas uma contra a outra;
  - verificação contra Schwenzfeger (NASA TM X-64836): concorda em r, φ, v e h e nos vetores; a componente u fica fora;
  - trecho heliocêntrico: calculado, não verificado.
- **Propulsão do orbitador** (Etapa 3.3, ADR 0013): **química**. "Na missão de referência (414 dias em Marte) e com as
  leis de guiagem verificadas, nenhuma opção elétrica fecha massa e tempo. Uma missão de estada longa, como a do ERO,
  poderia mudar isso, mas exigiria outra missão de referência e uma guiagem otimizada, não estudadas."
- **Arquitetura vigente** (`results/etapa2.5/arquitetura.md`, `results/etapa2.3/plataformas.md`):

| Item | Fim da Fase 2 (errata de 2026-10-27 do relatório da Fase 2, "Antes") | Fim da Fase 3 |
| :- | -: | -: |
| Orbitador injetado (regra iii) | 6.310 kg | **7.205 kg** |
| Lander injetado | 3.740 kg | **3.996 kg** |
| MAV + energia do aquecimento | 282 kg | **403 kg** |
| Total na órbita baixa da Terra, regra (iii) | 30.509 kg | **34.003 kg** |
| Órbita de encontro | 300 × 24.992 km | 300 × 24.992 km |

**Margens dos lançadores escolhidos** (pior janela, injeção direta; `results/etapa2.5/arquitetura.md`):
- orbitador: Falcon Heavy descartável +56 %, Vulcan VC6 +15 %;
- lander: Falcon Heavy com recuperação +17 %, Vulcan VC2 +8 %.

## 2. Método
**Etapa 3.1: motores e queima finita** (`docs/etapa3.1_motores.md`, `results/etapa3.1/`)
- **Catálogo:** motores com voo e fonte primária (F28, F105 a F112).
- **Queima finita:** integração plana de dois corpos com empuxo tangencial e massa variável (`orbital.queima_finita`),
  em uma e em várias queimas no periapse (`orbital.queima_multipla`, P-042).
- **Redimensionamento:** ponto fixo entre perdas, massas e órbita de encontro (`tools/redimensiona.py`, P-044). As
  Etapas 1.4, 2.1 e 2.2 ficam como registro da época ("antes_etapa_3_1").

**Etapa 3.2: modelo de baixo empuxo** (`docs/etapa3.2_baixo_empuxo.md`, `results/etapa3.2/`)
- **Espiral tangencial numérica:** DOP853, com aceleração constante ou empuxo constante.
- **Solução analítica quase circular:** Δv = |√(μ/r0) − √(μ/r1)|, derivada da taxa de energia. A atribuição a
  Edelbaum (1961) não foi conferida no original.

**Etapa 3.3: orbitador químico × elétrico × híbrido** (`docs/etapa3.3_orbitador.md`, `results/etapa3.3/`)
- **Geometria:** declinação das assíntotas no equador de Marte (`orbital.geometria`).
- **Catálogo elétrico:** só NSTAR e XIPS-25 (`config/eletrica.yaml`).
- **Híbrido:**
  - (c2) captura circular e espiral verificada (`orbital.hibrido`), com varredura da órbita de encontro, regra dos 5 %,
    MAV, massas (iii) e margens;
  - (c1) descida em arcos em torno do periapse (`orbital.baixo_empuxo.apoapse_por_arcos`).
- **Elétrico (b):** ordem de grandeza do trecho heliocêntrico.

## 3. Verificações
- **Espiral numérica contra Schwenzfeger, NASA TM X-64836 (1973), p. 31** [F113], ε = 0,01
  (`results/etapa3.2/baixo_empuxo.md`):
  - critério declarado (P-046): 1e-4 por componente;
  - r, φ, v e h ficam dentro em todos os pontos;
  - u = r·ṙ fica fora em três pontos, com até 3,2e-4;
  - erro dos vetores (métrica adicional): até 3,1e-5 na posição e 1,7e-5 na velocidade.
  - Decisão (ADR 0012, critério B): a diferença em u é atribuída, provavelmente, à precisão da integração publicada.
    Isso não foi confirmado.
- **Conferências (não são verificação; as duas soluções são deste estudo):**
  - analítico × numérico: a diferença relativa de Δv cai como ε², para 2,9e-8 (Marte) e 4,6e-7 em módulo (heliocêntrico) com
    ε = 1e-4;
  - espiral quase circular × numérica nos pontos do c2 (`results/etapa3.3/orbitador_eletrico.md`).
- **Sem verificação contra caso publicado:**
  - as perdas de queima finita da 3.1 (calculadas);
  - o trecho heliocêntrico elétrico;
  - a descida em arcos do c1.
- **Reprodutibilidade:** `tools/confere_regeneracao.py` regenera todo o `results/` em cada PR, no CI e num worktree
  local fixo no commit, dentro das tolerâncias P-039 e P-040.

## 4. Decisões (ADRs da Fase 3)
- **ADR 0011:** motores químicos C2, R3, M2, N2 e Z1; Isp de voo; perdas calculadas no lugar da P-015.
- **ADR 0007, notas de 2026-10-28:**
  - ε do MAV de 0,230;
  - risco da assíntota da equação do foguete;
  - a mitigação pela órbita mais baixa não se confirmou.
- **ADR 0012:** critério B da verificação; espirais coplanares se a geometria permitir; rótulo do trecho heliocêntrico.
- **ADR 0013:** orbitador químico; (B) estudo de estada longa fica para o futuro; catálogo NSTAR e XIPS-25.
- **ADR da propulsão nuclear térmica:** em PR à parte (fora do escopo, pelo prompt da Fase 3).

## 5. Limitações
- **Perdas de queima finita:** empuxo tangencial, que não é o direcionamento ótimo; Marte como massa pontual; sem J2.
- **MAV:** ε de um MAV de um estágio [F46] aplicado aos dois estágios. É hipótese, sem fonte, que seja otimista para o
  2º estágio.
- **Edelbaum:** a forma com mudança de plano não foi implementada (artigo pago). A Etapa 3.3 mostrou que ela não é
  necessária: o maior excesso de declinação é de 0,05° (`results/etapa3.3/geometria_planos.md`).
- **Híbrido:**
  - só duas concepções foram avaliadas, e não há guiagem otimizada;
  - perdas químicas iguais às da 3.1 (P-048);
  - fase de RAAN de 24 d [F121] não incluída, o que só piora o elétrico;
  - orientação do nodo na partida não tratada.
- **Opção (b):** só ordem de grandeza, sem dimensionamento.

## 6. Riscos
- **MAV perto da assíntota da equação do foguete** (ADR 0007): Isp de 310 s e Δv de subida de 5,764 km/s com margem.
  Com ε = 0,300 (P-045), o lander perde os dois lançadores escolhidos.
  - A mitigação por orbitador elétrico não se confirmou (ADR 0013).
  - Mitigações a avaliar: margem de lançador; lançador maior para o lander; MAV com Isp maior, se houver motor com voo.
- **Margens da sensibilidade** (`results/etapa2.5/arquitetura.md`):
  - com margem de Δv de 20 %, o orbitador perde o VC6 (−6 %) e o lander perde o VC2 (−3 %);
  - com o MGA do GSFC, o lander perde o VC2 (−3 %).

## 7. Premissas NÃO VALIDADAS
`results/fase3/premissas_nao_validadas.md` (gerado por `tools/lista_premissas.py`): 49 premissas, todas NÃO
VALIDADAS, 9 criadas na Fase 3:

| Id | Assunto |
| :- | :- |
| P-041 | Parâmetros numéricos da queima finita |
| P-042 | Várias queimas no periapse e fração do raio de Hill |
| P-043 | Conferência com o ERO |
| P-044 | Ponto fixo das perdas e massas |
| P-045 | Ilustração do risco do ε do MAV |
| P-046 | Espiral de baixo empuxo |
| P-047 | Operação do sistema elétrico |
| P-048 | Perdas químicas do híbrido |
| P-049 | Varredura e parâmetros do orbitador elétrico |
