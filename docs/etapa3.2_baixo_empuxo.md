# Etapa 3.2: modelo de baixo empuxo, verificado

Fase 3, propulsão. Os números deste documento vêm de `results/etapa3.2/baixo_empuxo.md` e `.yaml`, gerados por
`tools/baixo_empuxo.py` a partir de `config/baixo_empuxo.yaml` e do módulo `src/orbital/baixo_empuxo.py`.

## 1. Pergunta
A Etapa 3.3 vai comparar o orbitador químico com um elétrico e um híbrido, em que a descida até uma órbita mais baixa e
a subida de volta são espirais de baixo empuxo. Antes disso, é preciso um modelo de espiral em que se possa confiar:
- uma solução analítica (Edelbaum);
- uma integração numérica com empuxo contínuo;
- as duas conferidas uma contra a outra e verificadas contra um caso publicado.

## 2. Modelo (`src/orbital/baixo_empuxo.py`)
- **Numérico:** movimento plano de dois corpos, corpo central como massa pontual, empuxo sempre tangente à velocidade
  (a favor para subir, contra para descer). Aceleração constante ou empuxo constante com massa variável (vazão
  T / (Isp · g0)). A espiral para quando a energia osculadora chega à da órbita circular-alvo. Integrador DOP853, com
  tolerâncias na P-046.
- **Analítico (quase circular, coplanar):** Δv = |√(μ/r0) − √(μ/r1)|. É derivado no módulo da taxa de energia
  dh/dt = a_T · v, que é a eq. (1) de Schwenzfeger [F113, p. 3], h' = ε|v|, em tempo físico. Coincide com a fórmula de
  Edelbaum sem mudança de plano.
- **Limitações:**
  - A fórmula de Edelbaum com mudança de plano não foi implementada. O artigo original (Edelbaum 1961, ARS Journal) é
    pago e não pôde ser citado literalmente (regra 1).
  - O empuxo tangencial não é o direcionamento ótimo. A fonte diz que ele é muito próximo do ótimo na parte de muitas
    voltas da espiral e se afasta perto do escape [F113, p. 1].
  - Sem J2, sem sombra (painéis solares), sem terceiro corpo.
  - A espiral parte e chega em órbitas circulares. A partida de uma órbita elíptica (a de captura ou a de encontro) é
    integrável, mas não tem solução analítica nem caso de verificação nesta etapa.

## 3. Verificação contra caso publicado (Schwenzfeger, NASA TM X-64836, 1973) [F113]
- **Caso:** subida com aceleração tangencial constante ε = 0,01 (adimensional com a órbita inicial) a partir de órbita
  circular. A fonte integrou numericamente com Runge-Kutta-Fehlberg de 7ª ordem (p. 25) e listou o estado (r, φ, u, v,
  h, t) em sete pontos até o escape (p. 31; imagem conferida e transcrita em `config/baixo_empuxo.yaml`).
- **Critério declarado** (P-046): diferença relativa ≤ 1e-4 em cada componente, que é a precisão relevante do estudo.

| t | Dif. r | Dif. φ | Dif. u | Dif. v | Dif. h | Vetor posição | Vetor velocidade |
| -: | -: | -: | -: | -: | -: | -: | -: |
| 0,1500 | +4,6e−08 | −2,6e−08 | +5,5e−09 | +8,4e−09 | −1,0e−08 | 4,6e−08 | 8,4e−09 |
| 2,5789 | −3,5e−08 | +3,9e−08 | +1,3e−06 | −2,2e−08 | −8,9e−09 | 1,1e−07 | 5,3e−08 |
| 9,8502 | +5,6e−08 | −3,1e−06 | **−3,2e−04** | +2,2e−07 | −4,3e−07 | 2,7e−05 | 1,3e−05 |
| 18,5400 | +1,1e−05 | −2,0e−06 | **−3,1e−04** | +3,0e−07 | −7,0e−07 | 3,0e−05 | 1,3e−05 |
| 35,0757 | +3,6e−06 | −1,5e−06 | **−1,4e−04** | +7,2e−07 | −1,8e−06 | 3,1e−05 | 1,5e−05 |
| 70,1725 | +9,5e−06 | +5,9e−08 | +1,5e−05 | −3,5e−07 | +3,8e−06 | 9,6e−06 | 8,0e−06 |
| 85,6922 | +6,9e−06 | −3,1e−07 | +5,4e−06 | +1,7e−07 | −3,7e−06 | 1,1e−05 | 4,2e−06 |

**Resultado: pelo critério declarado, NÃO verificado.** r, φ, v e h ficam dentro de 1e-4 em todos os pontos. A
componente u = r·ṙ fica fora em três pontos, com até 3,2e-4.

**Investigação da diferença em u:**
- **O integrador deste estudo está convergido.** DOP853 e Radau, com tolerâncias de 1e-9 a 1e-13, dão o mesmo u em 9
  dígitos (conferência feita na sessão, não gravada em `results/`).
- **A diferença não vem de comparar pelo tempo.** Integrando o sistema da fonte na variável dela (s, com dt/ds = r) e
  comparando nos valores redondos de s, a diferença em u é a mesma.
- **A diferença absoluta em u é pequena.** É de cerca de 1,4e-5, num estado em que |v| é cerca de 1,1. u é a parte
  radial, pequena e oscilante, da velocidade, e um erro absoluto pequeno vira um erro relativo grande. O erro do vetor
  velocidade fica abaixo de 1,5e-5, e o do vetor posição abaixo de 3,1e-5.
- **Conclusão provável:** a diferença está na integração publicada de 1973, cuja precisão a fonte não declara.
- **Ressalva na listagem da fonte:** o s impresso na última linha (34,488779) não fecha com o t e o estado impressos.
  Por isso a comparação é feita pelo t, e por ele a última linha fecha em 1e-5.

**Decisão do Fabio no portão:** ver a seção 6, item 1.

## 4. Conferência: espiral numérica × solução analítica
As duas soluções são deste estudo, então isto é conferência, não verificação. O problema adimensional só depende de
ε = aceleração / (μ/r0²) e da razão r1/r0.

| Caso | r1/r0 | Δv analítico | ε = 1e-2 | ε = 1e-3 | ε = 1e-4 |
| :- | -: | -: | -: | -: | -: |
| Marte: descida da circular de mesma energia que a órbita de encontro (16.042 km) até 300 km (3.696 km) | 0,2304 | 1,770 km/s | +2,8e−04 | +3,3e−06 | +2,9e−08 |
| Heliocêntrico: da órbita da Terra (1 UA) à de Marte | 1,5237 | 5,655 km/s | −3,1e−03 | −3,9e−05 | −4,6e−07 |

As células dos ε dão a diferença relativa do Δv numérico contra o analítico.
- A diferença cai com ε², como esperado. Em Marte, com ε = 1e-4, a descida leva 7.097 voltas.
- Com ε = 1e-2, a órbita termina com excentricidade de 0,04 (Marte) e 0,05 (heliocêntrico). Nesse caso a hipótese de
  órbita quase circular já não vale bem.

## 5. Trecho heliocêntrico: calculado, NÃO verificado
- **Busca de caso de referência publicado:**
  - Strack, NASA TN D-4559 [F114]: transferências Terra–Marte com empuxo **ótimo** e desligamentos, em três corpos.
  - Moeckel, NASA TR R-79 [F115]: uma família de trajetórias **indiretas** entre órbitas circulares.
- **Nenhum dos dois serve.** Ambos usam leis de empuxo diferentes da tangencial, e uma comparação exigiria implementar o
  controle ótimo ou a família de Moeckel.
- **Rótulo:** o trecho heliocêntrico (conferido só contra a solução analítica) fica como **calculado, não verificado**.

## 6. Para decidir no portão
1. **Critério da verificação contra [F113].** Pelo critério declarado (1e-4 por componente), a verificação **não passa**
   em u, que chega a 3,2e-4. Opções:
   - **(A)** Medir o erro pelo vetor velocidade e pelo vetor posição, relativo ao módulo de cada um. Passa, com até
     3,1e-5. É a medida usual de erro de estado e não exagera o erro da componente pequena.
   - **(B)** Manter 1e-4 por componente e registrar a etapa como "verificado em r, φ, v e h; u fora (até 3,2e-4),
     atribuído à integração publicada".
   - **(C)** Procurar um segundo caso publicado com listagem numérica (outro ε, ou uma missão real de espiral) antes de
     fechar.
2. **Edelbaum com mudança de plano.** Se a Etapa 3.3 precisar de mudança de plano na espiral, é preciso o artigo
   original [Edelbaum 1961], de acesso pago. Sem ele, a 3.3 fica restrita a espirais coplanares.
3. **Trecho heliocêntrico.** Opções:
   - aceitar o rótulo "calculado, não verificado";
   - implementar o controle ótimo para comparar com Strack [F114]. É bem mais trabalho.

## 7. Premissas
- **P-046 (nova, NÃO VALIDADA):**
  - tolerâncias do integrador;
  - tolerância da verificação (1e-4);
  - faixa de ε da conferência;
  - órbita da Terra circular de 1 UA;
  - arredondamento dos campos sensíveis ao ruído entre CPUs.
- **Total:** 46 premissas, todas NÃO VALIDADAS (`results/fase2/premissas_nao_validadas.md`).
