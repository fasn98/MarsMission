# Etapa 4.2: controle térmico

Fase 4, subsistemas. Os números vêm de `results/etapa4.2/termico.md` e `.yaml`, gerados por `tools/termico.py` a partir
de `config/termico.yaml`, de `config/mav_propulsao.yaml` e de `results/etapa4.1/energia.yaml`.

## 1. Pergunta
- Faixas de temperatura de cada item crítico (propelentes, MAV, baterias, amostras), com fonte.
- Potência de aquecimento por modo e o efeito no orçamento de energia.
- Pendência do 2º portão da 4.1 (ADR 0015): o calor das RHUs no cruzeiro, dentro do aeroshell.

## 2. Faixas (`results/etapa4.2/termico.md`)
| Item | Limite | Fonte |
| :- | :- | :- |
| MMH | fusão a −52,4 °C | [F157] |
| NTO / MON-3 | fusão a −11,2 °C | [F158] |
| Sistemas MMH/NTO em operação | nominal de 15 a 27 °C | [F159] |
| Tanques de propelente (cruzeiro do MER) | AFT de 17 a 28 °C | [F160] |
| Linhas de propelente | AFT de 17 a 50 °C (MER); típica de 15 a 50 °C | [F160, F161] |
| Propulsão líquida (hidrazina) do MAV do SRL | AFT de 14 a 50 °C | [F164] |
| Bateria Li-ion | operação de −20 a 30 °C (Perseverance); de 0 a 30 °C no cruzeiro do SRL | [F162, F165] |
| Amostras (RSTA) | AFT abaixo de −20 °C; +30 °C só em transientes operacionais inevitáveis | [F167] |
| MAV do estudo (O4, MMH/NTO) | aquecido a −1 °C (P-027: fusão do NTO + 10 K) | config/mav_propulsao.yaml |

Ambiente: o modelo de aquecimento do MAV usa −62,5 °C, o ambiente do igloo do SRL [F57]. A mínima noturna do solo em
Jezero é de cerca de −93 °C, ou 180 K [F172].

**Duas fontes divergem para o MAV sólido do SRL:** o [F57] dá AFT de −25 a −15 °C e o [F164] dá de −25 a 0 °C em operação.
Isso não afeta o MAV do estudo, que é líquido.

## 3. Aquecimento por modo e efeito no orçamento de energia
**Lander na superfície (linha de base C + RHU, ADR 0015).** A tabela abaixo mostra o alvo do MAV, que é o termo que muda.
Os aquecedores e as RHUs do lander seguem a P-056.

| Alvo do MAV | Potência | Sobrevivência | Demanda em operação | Área da opção | Massa da opção |
| :- | -: | -: | -: | -: | -: |
| −1 °C (atual, P-027) | 48,3 W | 1.694 Wh/sol | 4.691 Wh/sol | 27,7 m² | 245 kg |
| 15 °C (nominal MMH/NTO [F159]) | 60,8 W | 2.004 Wh/sol | 5.000 Wh/sol | 32,8 m² | 278 kg |
| 17 °C (AFT dos tanques do MER [F160]) | 62,4 W | 2.042 Wh/sol | 5.039 Wh/sol | 33,4 m² | 282 kg |

A área e a bateria da operação normal também são recalculadas com a demanda nova; a área continua sendo a da
sobrevivência.

- **O alvo de −1 °C da P-027 fica abaixo da prática de sistemas MMH/NTO.** A faixa nominal começa em 15 °C [F159]; a AFT
  dos tanques do MER começa em 17 °C [F160]; a da propulsão líquida do MAV do SRL, em 14 °C [F164].
  - Com 15 °C, a sobrevivência sobe para 2.004 Wh/sol, e a opção vai a 32,8 m² e 278 kg.
  - A P-027 só leva em conta o congelamento do NTO, e não a faixa em que o motor opera nem o limite das linhas.
- **Comparação com o projeto publicado do SRL** (análise, não medida; o SRL é outro veículo, no pior caso frio, Ls 72°):
  - aquecedores do LAMP e da bateria: 1.540 Wh/sol [F166];
  - aqui, aquecedores do lander 363 Wh/sol mais 34,6 W de RHUs (853 Wh/sol), total de 1.217 Wh/sol, ou 79 % do SRL;
  - não é verificação: o valor menor pode indicar que o análogo escalado do Spirit (P-056) não superestima, ou que
    subestima; e os ambientes diferem, porque o caso frio do SRL não é a tempestade global;
  - MAV do SRL: cerca de 30 W para a sobrevivência de toda a MAS, a maior parte gasta no RCS líquido a +14 °C [F164];
    um conceito anterior de MAV sólido pedia de 60 a 70 W para operar a −20 °C [F170]. O MAV líquido do estudo usa
    48,3 W.
- **Orbitador:**
  - os aquecedores estão dentro da potência da plataforma por modo (P-053, análogo do Mars Express [F68]): cruzeiro
    745 W, captura 310 W, encontro 1.022 W, retorno 945 W;
  - não há fonte que separe os aquecedores por modo; o MRO usa até 300 W em aquecedores [F171], numa página de
    divulgação;
  - o orçamento do orbitador não muda nesta etapa.

## 4. Amostras e MAV aquecido
- **Requisito:** a AFT das amostras é de −20 °C, exceto em transientes operacionais inevitáveis, em que vai a +30 °C. Pedidos
  acima de +30 °C passam por análise antes de waiver [F167, p. 6].
- **O MAV do estudo** é aquecido a −1 °C, 19 K acima dos −20 °C. Com 15 °C, seriam 35 K acima
  (`results/etapa4.2/termico.md`). O aquecimento é contínuo na estada, não um transiente.
- **Contexto que as fontes dão:**
  - a mesma fonte estima, no pior caso, máximas de +5 a +53 °C para as amostras no depósito, por anos; de +30 a +53 °C na
    transferência para o contêiner, por meses; e de +30 °C no lançamento do MAV, por minutos;
  - essas excursões são "very transient", e a média diária fica poucos graus acima da superfície. A origem é uma comunicação
    pessoal (D. Beaty) [F167, p. 5, Tab. 1];
  - os tubos no depósito podem ser aquecidos repetidamente a até 300 K por anos [F172].
- **O MAV do SRL não era todo frio:** os estágios sólidos ficavam entre −40 e −20 °C, mas o RCS líquido ficava a +14 °C
  ou mais, e era ali que ia a maior parte da potência de sobrevivência [F164]. A posição do contêiner em relação a partes
  aquecidas não foi estudada aqui.
- **É uma escolha de arquitetura, do Fabio** (seção 7). Os prós e contras de cada opção estão lá.

## 5. Cruzeiro: calor das RHUs dentro do aeroshell
As 35 RHUs dão 35,0 W. Isso é:
- 18 % da perda passiva máxima do LAMP do SRL, 200 W com a tampa de 2,5 m² [F165];
- 28 % dos 125 W que o MER teve de rejeitar por um sistema ativo (HRS) [F168];
- 9 % dos 400 W da MMRTG que o projeto do MSL dissipava parasitamente no backshell e no escudo [F169].

A dissipação das aviônicas do lander no cruzeiro não está no estudo. No SRL, a dissipação máxima do LAMP no cruzeiro era
de 322 W, acima dos 200 W da perda passiva, e o projeto foi para um HRS ativo [F165]. **O calor das RHUs sozinho é pequeno diante dos três análogos; a
decisão entre rejeição passiva e HRS depende da dissipação das aviônicas** e fica para a lista de massas (Etapa 4.5).

## 6. Limitações
- O aquecimento do MAV escala com a diferença de temperatura e com a massa^(2/3) (P-027), a partir de um único ponto de
  referência [F57], num ambiente de igloo, e não do solo de Jezero.
- As faixas de baterias e de propelentes vêm de outras missões, não de um projeto deste lander.
- **Os pontos de fusão do MMH e do NTO** vêm de handbooks da USAF numa hospedagem que não foi conferida contra o DTIC
  [F157, F158]. O [F159], da NASA, confirma os mesmos valores arredondados: "the freezing temperature of NTO is -11oC
  [12oF] while the one of MMH is around -52oC [-62oF]".
- A comparação com o SRL é contra uma análise publicada, não contra medida.
- **Lacunas declaradas:**
  - o aquecimento do MAV e dos propelentes do lander no cruzeiro não foi calculado;
  - os aquecedores do lander em operação normal estão dentro da plataforma da P-032 (análogo do Phoenix), não
    separados;
  - do lander, só há os modos de sobrevivência e de operação; o orbitador não tem divisão dos aquecedores por modo.

## 7. Para decidir (Fabio)
1. **Alvo de temperatura do MAV (P-027, mudança de valor-base):**
   - (a) manter −1 °C;
   - (b) 15 °C, a faixa nominal de sistemas MMH/NTO [F159]: sobrevivência de 2.004 Wh/sol, área de 32,8 m²;
   - (c) 17 °C, a AFT dos tanques do MER [F160]: 2.042 Wh/sol, 33,4 m².
2. **Amostras contra o MAV aquecido** (opções sem avaliação de massa; contexto na seção 4):
   - (a) isolar termicamente o contêiner das amostras dentro do MAV, longe das partes aquecidas.
     - Pró: mantém o MAV líquido.
     - Contra: não avaliado, e não há análogo publicado.
   - (b) só pôr as amostras no MAV pouco antes do lançamento e tratar esse período como transiente (+30 °C [F167]).
     - Pró: usa a exceção do próprio requisito.
     - Contra: exige que a transferência fique no fim da estada, e a fonte estima de +30 a +53 °C nessa fase.
   - (c) rever a escolha do MAV líquido (ADR 0007).
     - Contra: o MAV do SRL também tinha uma parte líquida a +14 °C [F164], e a troca refaz a Fase 2.
   - (d) registrar o desvio e levá-lo à análise prevista pela fonte para exceções.
     - Pró: as amostras já passam por estimativas de pior caso acima de −20 °C [F167, F172].
     - Contra: o requisito vigente não é atendido.
3. **Calor no cruzeiro:** registrar que a escolha entre rejeição passiva e HRS fica para a Etapa 4.5, com a dissipação das
   aviônicas do lander.
