# Portão da Etapa 7.3: pergunta sobre o CG lateral da entrada

Esta é uma pergunta para o portão da 7.3, não uma conclusão. A decisão é do Fabio. O que não tem fonte está marcado como
NÃO VALIDADO. Nenhuma peça foi movida, e nenhuma premissa mudou.

## A pergunta
"O deslocamento lateral do CG da entrada deve ser intencional, com valor e direção escolhidos, para permitir entrada guiada
com sustentação e reduzir a elipse de pouso (relação com o risco principal do ADR 0018 e a P-075)? Ou deve ser anulado pelo
arranjo?"

## O que o estudo calcula (`results/etapa7.2/cg_lateral.md`)
- **Entrada, sem o estágio de cruzeiro:** deslocamento radial de 0,0306 m, ou 0,0065 do diâmetro da cápsula, num azimute de
  −65° que não foi escolhido. Ele sai do braço e do MAV.
- **MSL, para comparação:** zcg/d de −0,0215 [F226], intencional. O nosso é 30 % desse valor, com diâmetros de referência
  diferentes.
- **Não calculado:** o ângulo de trimagem e o L/D do lander, porque a aerodinâmica não está modelada (NÃO VALIDADO).

## Entrada guiada e elipse: o que as fontes dizem
| Item | O que a fonte diz | Fonte |
| :- | :- | :- |
| Por que a guiagem reduz a elipse | "Adding an autonomous guidance capability to a lifting entry provides active control of the range flown, significantly reducing the landing footprint ellipse" | [F227] PDF p. 3 |
| Como comanda | "provides bank angle commands"; "will command a bank reversal whenever the crossrange crosses a deadband threshold" | [F227] PDF p. 3; [F232] PDF p. 3 |
| De onde vem a sustentação no MSL | "the capsule used a radial cg offset to fly at an angle of attack (approximately −16◦ at hypersonic conditions)"; L/D de projeto de 0,24 | [F226] PDF p. 2; [F227] PDF p. 5 |
| Efeito da guiagem no MSL (simulação pré-voo) | "the entry guidance was able to reduce a 40 km 3σ miss error from all dispersions applied down to just over 10 km" | [F232] PDF p. 19 |
| Requisito de elipse | MSL: "25 x 20 km"; Mars 2020: "10 km x 10 km" | [F232] PDF p. 2; [F190] p. 2 |
| Elipse voada | MSL: "19.1 km x 6.9 km"; Mars 2020: "7.5 x 5.2 km" | [F190] p. 1 |
| Limites da guiagem | "the deploy ellipse would be no smaller than that of the position uncertainty of the onboard navigation system"; "initialization error is the primary driver in ellipse size for a guided entry" | [F232] PDF p. 2 e p. 20 |
| Entrada balística, sem guiagem (outro veículo, Phoenix) | de "approximately 250 km" (com sustentação) a "approximately 100 km" (balística) | [F233] PDF p. 4 |

Essas grandezas não são comparáveis entre si: há requisitos, simulações, elipses voadas e veículos diferentes.

**Não achado nas fontes consultadas (não conferido):**
- a elipse balística, com L/D zero, do MSL ou do Mars 2020;
- uma relação funcional entre o valor do L/D e o tamanho da elipse;
- a sensibilidade da trimagem ao deslocamento do CG, em graus por centímetro;
- os valores de CG do Mars 2020.

## Relação com o risco principal do ADR 0018 e a P-075
- **O que a Fase 4 já usa:** o plano de superfície parte da precisão voada de cerca de 1,7 km [F190] e do pouso de precisão
  previsto. A P-075 (200 m do depósito) é crítica.
- **O que decorre (NÃO VALIDADO, inferência do agente, sem fonte para o nosso veículo):**
  - os valores de elipse e de erro de entrega que a Fase 4 usa vêm de entradas guiadas, com sustentação;
  - anular o deslocamento do CG tiraria a sustentação na fase guiada, e esses valores deixariam de valer como referência;
  - um deslocamento intencional pediria massas de balanço ou um arranjo pensado para isso, e a massa delas não está
    identificada no orçamento. No MSL eram "145 kg of cruise balance masses; 168 kg of entry balance masses" [F234] PDF p. 3.

## Consumo dos propelentes de cruzeiro no CG
Tanques de MON-3 e de MMH em lados opostos, a 1,50 m do eixo (P-095), com massas diferentes.

| Propelente de cruzeiro restante | CG x (m) | Deslocamento radial (m) |
| -: | -: | -: |
| 100 % | 0,0256 | 0,0367 |
| 50 % | 0,0194 | 0,0330 |
| 0 % | 0,0129 | 0,0301 |

Valores de `results/etapa7.2/cg_lateral.md`, com a tabela completa.

- **NÃO VALIDADO:** o cálculo supõe razão de mistura constante (P-080) e as posições atuais dos tanques. Não há lei de
  consumo nem controle de CG modelados.
- **O que as fontes dizem do MSL no cruzeiro:**
  - "MSL was spin stabilized with a spin rate of about 2 rpm" [F234] PDF p. 3;
  - as massas de balanço mantinham o CG no eixo de rotação: "During the cruise and approach phases, the center of mass is on
    the axis of the spacecraft's stabilizing spin" [F214] PDF p. 27;
  - "Due to mass imbalances, the center of mass was slightly offset from the –Z axis, resulting in a small wobble as the
    spacecraft spun" [F235] PDF p. 24;
  - "the need to direct the thrust vector through the estimated spacecraft center of mass" [F111] p. 4.
- **Não conferido:** o efeito do consumo de propelente no CG ou no balanceamento de rotação do MSL. As fontes consultadas não
  o descrevem, e o MSL usava hidrazina em tanques iguais ("Each tank contained 36kg of hydrazine at launch" [F234] PDF p. 5), sem a
  diferença de massa entre oxidante e combustível do nosso arranjo.
- **Fora do nosso modelo:** o estudo não definiu se o cruzeiro do lander é estabilizado por rotação (NÃO VALIDADO).

## Opções a comparar no portão (sem escolha aqui)
| Opção | O que resolve | O que falta saber |
| :- | :- | :- |
| (a) deslocamento intencional, com valor e direção escolhidos | permitiria entrada guiada com sustentação, como no MSL (NÃO VALIDADO para o nosso veículo) | valor pedido para o nosso L/D, massas de balanço, arranjo; aerodinâmica não modelada |
| (b) anular pelo arranjo | CG no eixo, sem assimetria acidental | sem sustentação, os valores de elipse e de erro de entrega da Fase 4 ficam sem referência (NÃO VALIDADO) |

## Risco aberto (registrado pelo Fabio em 2026-11-06): massa por área na entrada
- **O risco:** a massa por área do lander no aeroshell de 4,5 m fica em 276 a 283 kg/m² na rota A, contra 211 kg/m² do Mars 2020
  (`results/etapa7.2/rotas_mav.md`).
- **Efeito a estudar:** entrada, descida e pouso, em particular a altitude de abertura do paraquedas e a margem de tempo.
- **Situação:** nenhuma rota resolve isso, e o efeito não foi calculado (NÃO VALIDADO). A aerodinâmica e a trajetória de entrada não
  estão modeladas.

## Nota (2026-11-07): massa por área com o Isp calculado do 44:1
A faixa de 276 a 283 kg/m² do risco aberto vem dos Isp dos análogos, rejeitados pelo Fabio. Com o Isp calculado, os valores estão em
`results/etapa7.2/rota_a.md`, seção 0.
