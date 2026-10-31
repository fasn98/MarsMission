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

| Alvo do MAV | Potência | Sobrevivência | Área da opção | Demanda em operação |
| :- | -: | -: | -: | -: |
| −1 °C (atual, P-027) | 48,3 W | 1.694 Wh/sol | 27,7 m² | 4.691 Wh/sol |
| 15 °C (nominal MMH/NTO [F159]) | 60,8 W | 2.004 Wh/sol | 32,8 m² | 5.000 Wh/sol |
| 17 °C (AFT dos tanques do MER [F160]) | 62,4 W | 2.042 Wh/sol | 33,4 m² | 5.039 Wh/sol |

- **O alvo de −1 °C da P-027 fica abaixo da prática de sistemas MMH/NTO.** A faixa nominal começa em 15 °C [F159]; a AFT
  dos tanques do MER começa em 17 °C [F160]; a da propulsão líquida do MAV do SRL, em 14 °C [F164].
  - Com 15 °C, a sobrevivência sobe para 2.004 Wh/sol e a área da opção para 32,8 m².
  - A P-027 só leva em conta o congelamento do NTO, e não a faixa em que o motor opera nem o limite das linhas.
- **Comparação com o projeto publicado do SRL** (análise, não medida; o SRL é outro veículo, no pior caso frio, Ls 72°):
  - aquecedores do LAMP e da bateria: 1.540 Wh/sol [F166];
  - aqui, aquecedores do lander 363 Wh/sol mais 34,6 W de RHUs (853 Wh/sol), total de 1.217 Wh/sol, ou 79 % do SRL;
  - não é verificação, mas indica que o análogo escalado do Spirit (P-056) não superestima;
  - MAV sólido do SRL: cerca de 30 W para sobreviver a −40 °C [F164] e de 60 a 70 W para operar a −20 °C [F170]. O MAV
    líquido do estudo usa 48,3 W.
- **Orbitador:**
  - os aquecedores estão dentro da potência da plataforma por modo (P-053, análogo do Mars Express [F68]): cruzeiro
    745 W, captura 310 W, encontro 1.022 W, retorno 945 W;
  - não há fonte que separe os aquecedores por modo; o MRO usa até 300 W em aquecedores [F171], numa página de
    divulgação;
  - o orçamento do orbitador não muda nesta etapa.

## 4. Amostras e MAV aquecido
A AFT das amostras é de −20 °C, fora dos transientes [F167]. O MAV do estudo é aquecido a −1 °C, 19 K acima disso; com
15 °C, seriam 35 K acima.
- **Se o contêiner de amostras viajar no MAV aquecido, o requisito das amostras não é atendido.**
- No SRL, o MAV era sólido e ficava frio: sobrevivência a −40 °C, operação a −20 °C [F164, F170].
- **Esta é uma escolha de arquitetura, para o Fabio** (seção 7).

## 5. Cruzeiro: calor das RHUs dentro do aeroshell
As 35 RHUs dão 35,0 W. Isso é:
- 18 % da perda passiva máxima do LAMP do SRL, 200 W com a tampa de 2,5 m² [F165];
- 28 % dos 125 W que o MER teve de rejeitar por um sistema ativo (HRS) [F168];
- 9 % dos 400 W da MMRTG que o MSL dissipou parasitamente no backshell e no escudo [F169].

Não falta só um número: a dissipação das aviônicas do lander no cruzeiro não está no estudo, e no SRL ela é o termo
dominante (o projeto chegou a um HRS ativo [F165]). **O calor das RHUs sozinho é pequeno diante dos três análogos; a
decisão entre rejeição passiva e HRS depende da dissipação das aviônicas** e fica para a lista de massas (Etapa 4.5).

## 6. Limitações
- O aquecimento do MAV escala com a diferença de temperatura e com a massa^(2/3) (P-027), a partir de um único ponto de
  referência [F57], num ambiente de igloo, e não do solo de Jezero.
- As faixas de baterias e de propelentes vêm de outras missões, não de um projeto deste lander.
- **Os pontos de fusão do MMH e do NTO** vêm de handbooks da USAF numa hospedagem que não foi conferida contra o DTIC
  [F157, F158]. O [F159], da NASA, confirma os mesmos valores arredondados: "the freezing temperature of NTO is -11oC
  [12oF] while the one of MMH is around -52oC [-62oF]".
- A comparação com o SRL é contra uma análise publicada, não contra medida.

## 7. Para decidir (Fabio)
1. **Alvo de temperatura do MAV (P-027, mudança de valor-base):**
   - (a) manter −1 °C;
   - (b) 15 °C, a faixa nominal de sistemas MMH/NTO [F159]: sobrevivência de 2.004 Wh/sol, área de 32,8 m²;
   - (c) 17 °C, a AFT dos tanques do MER [F160]: 2.042 Wh/sol, 33,4 m².
2. **Amostras contra o MAV aquecido** (opções sem avaliação de massa):
   - (a) isolar termicamente o contêiner das amostras dentro do MAV (não avaliado; sem análogo publicado de contêiner
     frio em MAV aquecido);
   - (b) só pôr as amostras no MAV pouco antes do lançamento e tratar esse período como transiente (+30 °C [F167]);
   - (c) rever a escolha do MAV líquido (ADR 0007).
3. **Calor no cruzeiro:** registrar que a escolha entre rejeição passiva e HRS fica para a Etapa 4.5, com a dissipação das
   aviônicas do lander.
