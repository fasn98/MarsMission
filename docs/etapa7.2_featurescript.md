# Etapa 7.2: FeatureScript paramétrico

Fase 7, CAD no Onshape. Os números deste documento vêm de `results/etapa7.2/conferencias.md` e `parametros.yaml`, gerados
por `tools/cad_parametros.py`.

**Entradas da ferramenta:**
- `results/etapa7.1/envelope.yaml` e `results/etapa2.5/arquitetura.yaml`;
- `config/cad.yaml`, com as escolhas do ADR 0022;
- fontes novas: F219 a F225, mais as citações acrescentadas a F41 e F215;
- premissas novas: P-089 a P-095.

## 1. Como o CAD é gerado
- **Ferramenta:** `tools/cad_parametros.py` monta cada veículo como uma lista de corpos primitivos, com posição, dimensões e
  material:
  - cilindro e tubo;
  - esfera e esfera oca;
  - tronco de cone, maciço ou oco;
  - caixa.
- **Modelo:** `cad/featurescript/modelo.fs` não tem nenhuma dimensão; ele só constrói a lista. O teste
  `tests/test_cad.py` confere isso: fora do cabeçalho, o modelo só tem os índices 0 a 2 e o expoente da unidade de
  densidade.
- **Arquivos gerados:** um por veículo, em `results/etapa7.2/` (`orbitador.fs`, `lander.fs` e `mav.fs`). Cada um é o modelo
  mais o bloco de dados do veículo. Todo valor do bloco sai de `results/` ou de `config/`.
- **Padrão de construção:** reaproveita o método de projeto anterior (fasn98/AeroDesignFlow, só leitura):
  - uma feature por veículo;
  - corpos ocos por subtração;
  - nome, aparência e material em cada corpo, para as Mass Properties do Onshape;
  - nomes em ASCII.
- **Materiais com fonte:**
  - Ti-6Al-4V [F219], Al 2219 [F220], Al 7075 [F221], CFRP IM7/8552 [F222] e PICA [F223];
  - MMH [F211] e MON-3 (P-078);
  - hidrazina (P-079) e SLA-561V (P-090).
- **Peças com geometria e material:** tanques, propelente, cilindro central do orbitador, escudo térmico (PICA, espessura
  de [F215]) e casca traseira (SLA-561V, espessura de [F225]).
- **Peças sem geometria própria** (P-094), com densidade equivalente = massa do orçamento / volume:
  - plataforma do orbitador, CCRS e EES;
  - núcleo do lander, braço e helicópteros;
  - motores e carga do MAV.

  Para essas peças, a massa do CAD é a do orçamento por construção. O que o CAD acrescenta é o CG e as inércias.

## 2. Conferências pedidas no portão da 7.1 (ADR 0022)

### 2.1 Folga radial do lander no Vulcan com a geometria real (sem a P-083)
- **Perfis:** as cápsulas foram lidas da Fig. 2 de [F41] (MSL/M2020, SRL-A e SRL-C).
  - A cápsula do SRL não é o MSL escalado: a frente é a mesma, e a casca traseira é maior.
  - A leitura do MSL dá raio máximo de 2,26 m, contra 2,25 m publicados; o erro de leitura é da ordem de 0,01 m.
- **Montagem:** frente para cima (P-091, lado seguro), com o estágio de cruzeiro 0,12 m além da cápsula.

| Forma | Raio máximo (m) | Comprimento (m) | Menor folga radial no Vulcan (m) |
| :- | -: | -: | -: |
| MSL/M2020 (Ø 4,5 m) | 2,26 | 2,88 | 0,143 |
| SRL-A (forma do CAD) | 2,34 | 3,85 | 0,047 |
| SRL-C | 2,36 | 3,55 | 0,032 |

- **Resultado:** a folga se confirma positiva com 4,65 m, nas duas formas do SRL. Ela é pequena (3 a 5 cm), mas maior que o
  erro de leitura.
- **Dependências:**
  - a orientação na coifa (P-091);
  - o perfil da SRL-A, que é de 2024 e ainda está mudando [F41].

### 2.2 MAV deitado contra o estreitamento da casca traseira
- **MAV:** Ø 0,57 m, 3,56 m de comprimento.
- **Folga interna:** 0,25 m (P-087).
- **Como foi conferido:** o comprimento máximo vem do raio interno no topo do MAV, com a base em cada estação (distância ao
  nariz).

| Estação da base (m) | MSL/M2020 | SRL-A | SRL-C |
| -: | -: | -: | -: |
| 0,85 (plano do ombro, P-092) | 3,18 (não cabe) | 3,60 (cabe) | 3,62 (cabe) |
| 0,95 | 3,04 (não cabe) | 3,49 (não cabe) | 3,51 (não cabe) |
| 1,05 | 2,89 (não cabe) | 3,39 (não cabe) | 3,40 (não cabe) |

(Tabela completa em `results/etapa7.2/conferencias.md`; vista em `results/etapa7.2/capsula_mav.png`.)

- **SRL:** o MAV deitado só cabe com a base no plano do ombro, com folga de 2 a 3 cm de cada lado. Essa posição é otimista,
  porque a estrutura de descida e o deck ocupam parte desse espaço. Com a base 10 cm mais para trás, ele já não cabe.
- **MSL (4,5 m):** não cabe em nenhuma estação.
- **Consequência para a alternativa de 4,5 m:** ela também deixaria de acomodar o MAV deitado.

### 2.3 Orbitador no Falcon (arranjo do CAD)
- **Arranjo:** a plataforma (0,30 m, P-094) e o EES sobre o CCRS entram no empilhamento.
- **Resultado:** o conjunto vai a 5,12 m e cabe, com folga radial mínima de 0,36 m (tanques de inserção).

## 3. Massa e CG esperados do CAD
Os valores vêm dos volumes dos primitivos. Eles servem para conferir o que o Onshape construir. Não são a comparação com o
orçamento, que fica para a Etapa 7.3.

| Veículo | Massa do CAD (kg) | Com geometria | Propelente | Densidade equivalente | CG z (m) | Orçamento (kg) |
| :- | -: | -: | -: | -: | -: | -: |
| Orbitador | 6.506,3 | 263,3 | 4.919,1 | 1.323,9 | 1,393 | 7.796 |
| Lander (lançamento) | 3.045,1 | 184,8 | 943,5 | 1.916,9 | 2,983 | 4.615 |
| MAV | 348,1 | 25,1 | 285,5 | 37,5 | 1,540 | 386,8 |

A diferença para o orçamento não é ajustada. São as peças que ainda não têm geometria:
- **Orbitador:** estrutura e motores dos estágios.
- **Lander:** estrutura do aeroshell, paraquedas e motores de descida.
- **MAV:** a estrutura fora dos tanques.

## 4. Instruções para gerar no Onshape (Fabio)
1. Crie um documento no Onshape e, nele, um **Feature Studio** para cada veículo: orbitador, lander e MAV.
2. Em cada Feature Studio, mantenha as duas primeiras linhas que o Onshape cria (versão da linguagem e da biblioteca
   padrão).
   - Cole o conteúdo do arquivo do veículo (`results/etapa7.2/<veiculo>.fs`) a partir da linha 3.
   - As duas primeiras linhas do arquivo usam a versão 2737, a do projeto anterior, e devem ser trocadas pelas da conta.
3. Clique em *Commit*. Num **Part Studio**, adicione a feature (MarsMission orbitador, lander ou mav) e marque
   *Assign materials*.
4. Selecione todas as peças e abra **Mass properties**. Envie:
   - capturas da geometria (lateral e isométrica);
   - massa total, CG (x, y, z) e momentos de inércia em torno do CG;
   - a massa de algumas peças por nome, para conferir contra `results/etapa7.2/parametros.yaml`.
5. Se houver erro de compilação, envie a mensagem do Onshape. O FeatureScript **não foi compilado** aqui (não conferido),
   porque não há conta Onshape neste ambiente.

**Integração por API:** não faz parte desta etapa. Se for feita depois, as chaves do Onshape ficam só em Secrets (por
exemplo, `ONSHAPE_ACCESS_KEY` e `ONSHAPE_SECRET_KEY` no Replit), nunca no repositório.

## 5. Para decidir (Fabio)
1. **Aeroshell de 4,65 m:** a condição se confirmou, com folga positiva no Vulcan (seção 2.1). A proposta é manter.
2. **MAV deitado:** cabe só com a base no plano do ombro, com 2 a 3 cm de folga de cada lado (seção 2.2). As opções:

   | Opção | Prós | Contras |
   | :- | :- | :- |
   | (a) manter deitado no plano do ombro (P-092) | não muda o arranjo | otimista: o deck e a descida ocupam esse espaço |
   | (b) reduzir a folga interna da P-087 (0,25 m, sem fonte) | ganha comprimento | a folga cobre estrutura, TPS e espaço livre, também sem fonte |
   | (c) MAV em pé, no eixo da cápsula (como o "central internal volume" de 1,2 m × 4+ m de [F46]) | usa o comprimento da cápsula | muda o arranjo e o sistema de ereção; não calculado |
   | (d) MAV mais largo e mais curto | menor comprimento | muda o ADR 0022 (diâmetro); não calculado |

   A proposta do agente é manter (a) no CAD da 7.3 e registrar o risco. As opções (c) e (d) seriam calculadas se você
   pedir.
3. **P-079, densidade da hidrazina:** achei fonte, a densidade relativa de 1,01 a 15 °C [F224].
   - Proposta: mudar o valor-base de 1.004 para cerca de 1.009 kg/m³ (1,01 × a densidade da água a 15 °C, que precisaria
     de fonte própria). Não mudei: valor-base só com a sua aprovação.
4. **Premissas novas (NÃO VALIDADAS):**

   | Premissa | O que define |
   | :- | :- |
   | P-089 | Forma da cápsula por opção (SRL-A para 4,65 m) |
   | P-090 | Densidade do SLA-561V |
   | P-091 | Orientação na coifa e estágio de cruzeiro |
   | P-092 | Estação da base do MAV |
   | P-093 | Materiais e espessuras |
   | P-094 | Peças com densidade equivalente |
   | P-095 | Arranjo interno do lander |

## 6. Limitações
- **Perfis das cápsulas:** são leitura de figura, e o SRL ainda está em projeto [F41].
- **Geometria simplificada:** os primitivos não dimensionam estrutura nem pressão, as espessuras são de ordem de grandeza
  (P-093) e o CAD não confere interferência entre peças.
- **Compilação:** o FeatureScript não foi compilado aqui (não conferido). A biblioteca padrão foi conferida na documentação
  oficial do FeatureScript: `fCylinder`, `fCone`, `fCuboid`, `opSphere`, `opBoolean` e `setProperty`.
- **Configuração:** o lander está em configuração de lançamento. A configuração de entrada (sem o estágio de cruzeiro), que
  dá o deslocamento do CG, fica para a 7.3.
