# Etapa 7.1: envelope e arranjo

Fase 7, CAD paramétrico no Onshape. A ordem das fases foi decidida no ADR 0021: a Fase 7 vem antes das Fases 5 e 6.
- **Números:** `results/etapa7.1/envelope.md` e `.yaml`, gerados por `tools/envelope_arranjo.py`.
- **Entradas:**
  - `config/cad.yaml`: fontes F211 a F218, mais as citações acrescentadas a F26, F35, F40, F46, F80, F82, F107 e F202;
  - premissas P-078 a P-088;
  - `results/etapa2.5/arquitetura.yaml` e `results/etapa4.1/energia.yaml`.
- **Vistas 2D** (esquemas, não desenho de projeto), em `results/etapa7.1/`:
  - `orbitador_na_coifa.png`;
  - `lander_na_coifa.png`;
  - `lander_superficie.png`;
  - `mav.png`.

## 1. Pergunta
- Dimensões principais derivadas:
  - volumes de tanque a partir das massas de propelente;
  - diâmetro do aeroshell;
  - dimensões do MAV;
  - painéis do lander.
- Encaixe nas coifas: orbitador no Falcon Heavy, lander no Vulcan (ADR 0020).
- Esquema do arranjo de cada veículo e tabela de dimensões.

## 2. Coifas (envelope publicado)
- **Falcon, coifa padrão** (orbitador):
  - o guia [F82] não imprime o volume útil e remete a um arquivo STEP do fabricante (volume útil com mantas, PAF de
    1575 mm);
  - o perfil (altura, raio) foi lido desse arquivo com OpenCascade e está em `config/cad.yaml`;
  - leitura feita numa instalação à parte, que não é dependência do projeto. A origem do arquivo foi tomada como o
    plano do PAF (não conferido);
  - a coifa estendida só tem envelope "upon request" [F82].
- **Vulcan, coifa de 15,5 m** (lander):
  - envelope estático lido da Fig. 4.3.1-1 do guia [F80]: Ø 4.877 mm no plano do PAF de 1575 mm, estreitando até o
    topo;
  - o envelope já inclui a folga dinâmica de 25,4 mm [F80];
  - não foi achada restrição de comprimento de coifa para o VC4 (não conferido).

## 3. Resultados (`results/etapa7.1/envelope.md`)
- **Orbitador:**
  - tanques esféricos de 1,12 m (inserção) e 0,91 m (retorno), com dois pares por estágio;
  - o conjunto empilhado tem 4,23 m e cabe no Falcon com folga radial mínima de 0,36 m;
  - painéis de 14,3 m².
- **Lander no Vulcan:**
  - com aeroshell de 4,5 m, a folga radial é de 0,136 m;
  - com 4,65 m, é de 0,060 m. Essa folga depende da P-083 (altura escalada do MSL, diâmetro máximo no topo do conjunto).
- **Massa por área de referência:** o lander tem 279 kg/m² com 4,5 m (Mars 2020: 211 kg/m²) e 261 kg/m² com 4,65 m (SRL de
  lançamento duplo: acima de 294 kg/m²).
- **Descida:** 544 kg de hidrazina em 3 esferas de 0,71 m (P-084).
- **Painéis:** 32,8 m² em duas asas circulares de 4,57 m abertas (P-088), muito maiores que as do Phoenix (envergadura de
  5,52 m no total).
- **MAV:**
  - 3,56 m com Ø 0,57 m e 3,79 m com Ø 0,50 m, nos dois casos acima do limite do MAV do MSR (2,99 m × 0,50 m [F35]) e
    da restrição de 2019 (3 m × 0,57 m [F216]);
  - o MAV hipergólico de Bowles com 312,5 kg tem 2,19 m × 0,52 m [F46], mas é de um estágio e tem turbobomba;
  - a fonte de 2019 registra que o conceito líquido teve dificuldade com volume e massa [F216];
  - deitado, o MAV cabe no diâmetro útil interno dos dois aeroshells.

## 4. Para decidir (Fabio)
| Decisão | Opções | Prós | Contras |
| :- | :- | :- | :- |
| Diâmetro do aeroshell | (a) 4,5 m (MSL e Mars 2020) | herança de voo; folga radial maior no Vulcan | massa por área de 279 kg/m², contra 211 kg/m² do Mars 2020 (`results/etapa7.1/envelope.md`) |
| | (b) 4,65 m (SRL de lançamento duplo) | da classe de massa do SRL; massa por área menor | não voou; folga radial de 0,060 m no Vulcan, sensível à P-083; [F202]: "> 4.65-m may lead to a new launch vehicle fairing" |
| Diâmetro do MAV | (a) 0,50 m (limite do MSR) | encaixa no padrão do MSR | 3,79 m de comprimento |
| | (b) 0,57 m (restrição de 2019) | 3,56 m, mais curto | também acima do limite de 3 m |
| Arranjo dos tanques do orbitador | (a) dois pares por estágio (base) | conjunto mais baixo | mais tanques e linhas |
| | (b) um par por estágio | menos tanques (esferas de 1,41 e 1,14 m) | conjunto mais alto; com o cilindro central, folga radial de 0,06 m no estágio de inserção (0,88 m sem o cilindro) |

**Proposta do agente (o Fabio decide):**
- **Aeroshell:** (b), 4,65 m, porque a massa de entrada do lander está mais perto da classe do SRL. A folga radial no Vulcan
  precisa ser conferida com a geometria real do conjunto na 7.2.
- **MAV:** (b), 0,57 m, o mais curto. O comprimento acima de 3 m fica registrado como risco. Ele depende da P-086
  (comprimentos fora dos tanques, sem fonte), e só a 7.2 mede o empacotamento real.
- **Orbitador:** (a), dois pares.

## 5. Premissas novas (NÃO VALIDADAS)
| Premissa | O que define |
| :- | :- |
| P-078 | Densidade do MON-3 igual à do N2O4 |
| P-079 | Densidade da hidrazina |
| P-080 | Razão de mistura do cruzeiro do lander |
| P-081 | Fração de ullage |
| P-082 | Arranjo dos tanques |
| P-083 | Altura do conjunto de cruzeiro e aeroshell |
| P-084 | Propelente de descida escalado do MSL |
| P-085 | Geometria dos tanques do MAV |
| P-086 | Comprimento do MAV fora dos tanques |
| P-087 | Folgas de arranjo |
| P-088 | Painéis em duas asas |

## 6. Limitações
- **Volumes não dimensionados nesta etapa:** a plataforma do orbitador, o deck e as pernas do lander, o sistema de
  lançamento do MAV e o empacotamento dos painéis dobrados.
- **Dimensões sem fonte:** as do R-4D-11 e do contêiner de amostras não foram encontradas (P-086).
- **Densidades:** a do MON-3 e a da hidrazina são premissas (P-078, P-079).
- **Coifas:** o perfil do Falcon foi lido de um arquivo CAD, e o do Vulcan, de uma figura. Nenhum dos dois é texto citado.
  Os passos da leitura do STEP estão na fonte do perfil em `config/cad.yaml`.
- **MAV deitado no aeroshell:** a conferência usa o diâmetro útil interno, sem o estreitamento da casca traseira
  (afterbody triconic [F215]).
- **EES no CCRS:** o encaixe do EES (Ø 1,273 m) no CCRS (3,4 × 0,5 × 2 m) não foi conferido.
- **Padrão do drone:** o repositório fasn98/AeroDesignFlow não estava acessível com o token desta sessão (ADR 0021). Ele
  é necessário para a 7.2.

## 7. Nota (correção das listas de premissas)
As listas `results/fase2/` e `results/fase3/premissas_nao_validadas.md` vinham acumulando as premissas das fases seguintes,
e a da Fase 3 marcava como "criadas na Fase 3" também as da Fase 4. `tools/lista_premissas.py` foi corrigido: cada lista traz
só as premissas que existiam ao fim da fase. Com isso, as listas voltam a bater com os relatórios das Fases 2, 3 e 4. A
lista completa continua em `results/fase1/premissas.md`.
- **Fase 2:** a lista tem 40 premissas, como na §9 do relatório da Fase 2 depois da nota de 2026-10-27. As notas
  seguintes do relatório da Fase 2, que contavam a lista acumulada, receberam uma nota (2026-11-02).
- **Fase 3:** a lista tem 49 premissas, 9 delas criadas na Fase 3, como na §7 do relatório da Fase 3 (nota no relatório).
