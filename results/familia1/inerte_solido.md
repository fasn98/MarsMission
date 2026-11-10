# Lei de massa inerte do MAV sólido (gerado por tools/inerte_solido.py)

**NÃO VALIDADO.** Premissas P-014, P-019, P-108, P-110, P-111 e P-113 (nova, para aprovação).

## Motores do catálogo [F270] (inerte total impresso, salvo o Orion 38)

Critério: motores do catálogo [F270] com folha de dados de massa e propelente entre 12 e 1.300 kg, reunidos na busca de 2026-11-10 (não se afirma que a lista é exaustiva) (estágio superior e de chute, do tamanho do MAV ao do MAV escalado); fora: STAR 3 a 6B (TIRS, retro e spin, menos de 12 kg de propelente) e a série STAR 48 (acima de 2.000 kg)

| Motor | Envelope | Propelente (kg) | Inerte (kg) | Inerte/propelente | Fator do resíduo | PDF p. |
| :- | :- | -: | -: | -: | -: | -: |
| STAR 8 | titânio | 12,3 | 5,1 | 0,417 | 1,50 | 78 |
| STAR 9 | grafite-epóxi | 14,4 | 4,2 | 0,289 | 1,09 | 79 |
| STAR 12GV | grafite-epóxi | 32,9 | 9,0 | 0,273 | 1,31 | 80 |
| STAR 13B | titânio | 41,2 | 5,8 | 0,141 | 0,73 | 81 |
| STAR 15G | grafite-epóxi | 79,6 | 14,0 | 0,176 | 1,10 | 82 |
| STAR 17 | titânio | 69,6 | 9,4 | 0,136 | 0,82 | 83 |
| STAR 17A | titânio | 112,3 | 13,4 | 0,119 | 0,83 | 84 |
| STAR 20 | fibra de vidro-epóxi | 272,9 | 27,5 | 0,101 | 0,91 | 85 |
| STAR 24 | titânio | 199,9 | 18,3 | 0,092 | 0,76 | 86 |
| STAR 24C | titânio | 219,5 | 19,7 | 0,090 | 0,76 | 87 |
| STAR 26 | aço D6AC | 230,7 | 38,8 | 0,168 | 1,45 | 88 |
| STAR 26B | titânio | 237,7 | 23,4 | 0,098 | 0,86 | 89 |
| STAR 26C | titânio | 232,0 | 30,7 | 0,132 | 1,14 | 90 |
| STAR 27 | titânio | 333,7 | 27,5 | 0,082 | 0,79 | 91 |
| STAR 27H | titânio | 337,8 | 30,0 | 0,089 | 0,86 | 92 |
| STAR 30BP | titânio | 505,1 | 37,7 | 0,075 | 0,81 | 94 |
| STAR 30C | titânio | 590,8 | 38,5 | 0,065 | 0,74 | 95 |
| STAR 30C/BP | titânio | 590,8 | 41,1 | 0,070 | 0,79 | 96 |
| STAR 30E | titânio | 631,4 | 42,5 | 0,067 | 0,78 | 97 |
| STAR 31 | kevlar-epóxi | 1 285,9 | 107,5 | 0,084 | 1,20 | 99 |
| STAR 37FM | titânio | 1 066,0 | 81,7 | 0,077 | 1,04 | 100 |
| STAR 37FMV | titânio | 1 063,8 | 107,4 | 0,101 | 1,37 | 101 |
| STAR 37XFP | titânio | 883,7 | 72,4 | 0,082 | 1,06 | 102 |
| STAR 37GV | grafite-epóxi | 974,3 | 110,2 | 0,113 | 1,50 | 103 |
| Orion 38 | não declarado | 770,2 | 102,5 | 0,133 | 1,65 | 16 |

Massas do catálogo em lbm; 1 lb = 0,4535924 kg ([F112] p. 65 do PDF).

## Ajuste

- Forma: potência, inerte = a · propelente^b, mínimos quadrados em ln, 25 motores de 12,3 a 1 286 kg de propelente.
- a = 0,591, b = 0,701 (erro-padrão 0,041; ±2 erros-padrão: 0,619 a 0,783).
- Erro do ajuste: fator rms 1,31 (resíduo rms em ln 0,267); maior desvio, fator 1,65.
- Proporcional (b = 1, a forma da P-019 e da P-111): k = 0,115, fator rms 1,61, maior desvio 3,63.

## Comparação no tamanho do MSR (kg)

| Estágio | Propelente | Motor pelo catálogo | Motor do MSR [F269] | Não propulsivo do MSR | Estágio do MSR | P-019 | P-111 | Lei A | Lei B |
| :- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| estágio 1 | 216,0 | 25,6 | 46 | 14 | 60 | 86,5 | 64,6 | 60,0 | 64,6 |
| estágio 2 | 54,4 | 9,7 | 14 | 34 | 48 | 21,8 | 43,0 | 48,1 | 43,0 |

## O que os dados sustentam

- **Escala.** A P-019 (k = 0,401 nos dois estágios) e a P-111 (k = 0,299 e 0,791) são proporcionais: o inerte cresce como o propelente (b = 1). O catálogo dá b = 0,70, e b = 1 fica fora de ±2 erros-padrão: **para o motor, os dados não sustentam a escala proporcional de nenhuma das duas**; ao crescer, a fração inerte do motor cai. Para o estágio inteiro, isso depende também de como cresce o inerte não propulsivo, que não tem fonte (a P-113 o fixa). O catálogo junta projetos diferentes: a dispersão entre eles não é a escala de um único projeto.
- **Erro-padrão.** Supõe resíduos independentes; há variantes do mesmo motor (STAR 26/26B/26C, 30BP/30C/30C-BP/30E, 37FM/37FMV), então o erro-padrão está subestimado. A distância de b a 1 é de 7,3 erros-padrão.
- **Nível.** No tamanho do MSR, o motor do catálogo é mais leve que o motor do MSR [F269] (tabela acima). A verificação da P-110 reproduz o inerte total do MSR e a órbita publicada, não a divisão por estágio: a P-111 dá 64,6 e 43,0 kg, contra 60 e 48 kg do [F269]. A P-019 dá outra divisão. Nenhuma das duas separa o inerte não propulsivo (aviônica, RCS, estrutura da carga), que o [F269] dá à parte.
- **Conflito com a P-110 (não resolvido aqui).** A justificativa da P-110 diz que a divisão do inerte por estágio não tem fonte; o [F269] publica uma (fração do estágio 2 = 0,444, contra 0,40 escolhida pela verificação da P-110). Com o modelo de subida e o guiamento atuais, a divisão do [F269] não chega à órbita publicada (variante A, abaixo). A P-110 não foi mudada; a decisão é do Fabio.
- **Proposta (P-113, NÃO VALIDADA, para aprovação):** inerte do estágio = N + c · P^b, com b do catálogo e N, o não propulsivo do [F269], fixo. Duas variantes do nível c: A, pelo motor do MSR [F269]; B, pela divisão que a verificação da P-110 escolheu. A escolha é do Fabio.

## Subida com cada variante (modelo de subida do sólido; tolerância 1e-06, passo da varredura 0,05, os da P-110)

### Lei A (nível do motor pelo [F269]): nominal

- N = 14 e 34 kg; c = 1,063 e 0,855; b = 0,701. O c da variante A é calibrado no propelente do [F269] (216 e 54 kg) e aplicado ao do MSR usado no estudo (216 e 54,4 kg, config/cad.yaml), daí o estágio 2 com um pouco mais que 48 kg.
- Verificação com o MAV do MSR (órbita publicada de 350 km): inertes 60,0 e 48,1 kg; órbita 318 × 344 km; costa 468 s (publicada 446 s); **não chega à órbita publicada** (resíduo 5,2e+00).

| Caso, 380 km | Escala | Capacidade (m/s) | GLOM (kg) | Propelente (kg) | Inertes (kg) | Órbita simulada (km) | Chega? | Comprimento, P-108 (m) | 4,65 m com deck, P-108 | Comprimento, P-108 revista (m) | 4,65 m com deck, revista | 4,65 m sem deck, revista | 4,5 m com deck, revista |
| :- | -: | -: | -: | -: | -: | :- | :- | -: | -: | -: | -: | -: | -: |
| sem margem (o menor que chega) | 1,075 | 4 110 | 418,0 | 232,3 + 58,5 | 62,4 + 48,8 | 380 × 380 | sim | 2,79 a 2,90 | +0,192 a +0,248 | 2,79 | +0,251 | +0,405 | −0,021 |
| com a margem da P-014 na capacidade | 1,345 | 4 521 | 501,6 | 290,5 + 73,2 | 70,6 + 51,3 | 432 × 693 | não | 3,11 a 3,63 | −0,172 a +0,087 | 3,08 | +0,102 | +0,256 | −0,169 |

### Lei B (nível pela divisão verificada da P-110): sensibilidade

- N = 14 e 34 kg; c = 1,169 e 0,549; b = 0,701.
- Verificação com o MAV do MSR (órbita publicada de 350 km): inertes 64,6 e 43,0 kg; órbita 350 × 350 km; costa 481 s (publicada 446 s); **chega à órbita publicada**.

| Caso, 380 km | Escala | Capacidade (m/s) | GLOM (kg) | Propelente (kg) | Inertes (kg) | Órbita simulada (km) | Chega? | Comprimento, P-108 (m) | 4,65 m com deck, P-108 | Comprimento, P-108 revista (m) | 4,65 m com deck, revista | 4,65 m sem deck, revista | 4,5 m com deck, revista |
| :- | -: | -: | -: | -: | -: | :- | :- | -: | -: | -: | -: | -: | -: |
| sem margem (o menor que chega) | 0,994 | 4 078 | 392,2 | 214,7 + 54,1 | 64,4 + 43,0 | 380 × 380 | sim | 2,68 a 2,69 | +0,297 a +0,302 | 2,69 | +0,297 | +0,451 | +0,025 |
| com a margem da P-014 na capacidade | 1,227 | 4 486 | 464,5 | 265,0 + 66,7 | 72,3 + 44,4 | 422 × 635 | não | 2,97 a 3,31 | −0,012 a +0,158 | 2,95 | +0,166 | +0,320 | −0,105 |

As duas variantes fecham a 380 km com o passo e a tolerância da P-110: não foi preciso refiná-los.

Alvo de folga: +0,05 m. O caso com a margem foi simulado com o mesmo guiamento (subida vertical, tangente linear, costa e queima do estágio 2 antes do apoapse): o sólido não regula o empuxo, então a capacidade a mais só chega à órbita de 380 km se o guiamento conseguir gastá-la; "não" na coluna "Chega?" quer dizer que ele passa da órbita com esse guiamento, não que falta Δv. O gasto por guinada está na seção da energia que sobra.

## Viés do modelo de subida do sólido (P-114, NÃO VALIDADO)

Fator comum no Isp dos dois estágios que leva o MAV do MSR na variante A à órbita publicada: **1,0083**, ou **33 m/s** de capacidade ideal (órbita 350 × 350 km). É a incerteza do modelo de subida do sólido; a P-110 não foi ajustada.

### Variante nominal corrigida pelo viés (Isp × fator nos dois estágios)

| Caso, 380 km | Escala | Capacidade (m/s) | GLOM (kg) | Propelente (kg) | Inertes (kg) | Órbita simulada (km) | Chega? | Comprimento, P-108 (m) | 4,65 m com deck, P-108 | Comprimento, P-108 revista (m) | 4,65 m com deck, revista | 4,65 m sem deck, revista | 4,5 m com deck, revista |
| :- | -: | -: | -: | -: | -: | :- | :- | -: | -: | -: | -: | -: | -: |
| sem margem (o menor que chega) | 1,023 | 4 053 | 401,7 | 221,0 + 55,7 | 60,7 + 48,3 | 380 × 380 | sim | 2,73 a 2,76 | +0,262 a +0,280 | 2,73 | +0,280 | +0,434 | +0,009 |
| com a margem da P-014 na capacidade | 1,275 | 4 459 | 480,0 | 275,4 + 69,4 | 68,5 + 50,7 | 429 × 632 | não | 3,03 a 3,44 | −0,078 a +0,129 | 3,01 | +0,140 | +0,294 | −0,132 |

## Comprimento do motor (P-108 revista, proposta)

- Os 25 motores do catálogo publicam diâmetro e comprimento ("Motor length"; no Orion 38, "Overall motor length (including nozzle)"); nenhum tem bocal extensível.
- Forma: L = a · P^b · D^c, mínimos quadrados em ln: a = 0,0070, b = 0,780 (erro-padrão 0,059), c = −1,529 (erro-padrão 0,181); erro: fator rms 1,09, maior desvio fator 1,23.
- Só com o propelente (L = a · P^b): b = 0,294, fator rms 1,20, maior desvio 1,55. O diâmetro entra porque o do MAV é fixo e menor que o da maioria dos motores.
- No Ø 0,57 m do MAV e no propelente do MSR: motores de 1,10 e 0,37 m. O resto até os 2,7 m do MSR ([F247]), 1,23 m, é interestágio, carga, aviônica e adaptadores: continua sem fonte e fica fixo na escala.
- **Proposta (para aprovação do Fabio): P-108 revista** = comprimento = motor do estágio 1 + motor do estágio 2 (pelo ajuste) + o resto fixo acima. Hoje a P-108 escala o comprimento não fixo na proporção do propelente, com a parte fixa de 0 a 1,5 m. A P-108 atual não foi mudada; as tabelas mostram as duas.

## Energia que sobra no sólido com margem (variante nominal)

- **(a1) Ignição antecipada do estágio 2, o método do MSR** ([F230] PDF p. 9: "This second stage burn is performed slightly before predicted apoapsis, expending excess energy by lowering apoapsis while at the same time raising periapsis"; [F271] PDF p. 3: "The solid motors are sized so as to nominally impart more delta-v than required to meet the target orbit"), com a antecedência até o limite da P-115: não chega a 380 km (melhor órbita 432 × 693 km, antecedência 16 s). No modelo, o estágio 2 empurra na horizontal local e o excesso vem do estágio 1 (guiamento no limite c₁ = 0,050 1/s da P-110); o MSR apontava o estágio 2 com guiamento próprio ([F230] PDF p. 9), o que o modelo não tem.
- **(a2) Guinada alternada do estágio 2 (P-115, sem fonte para o MAV; o mais próximo é o GEM, pilotagem fora do ótimo, [F272] PDF p. 4):** melhor órbita 379,97 × 380,04 km com guinada de 42,1° (resíduo 1,4e-05, tolerância 1e-06: **fora** da tolerância da P-110). Custo para a missão: nenhuma massa a mais (a margem já está no MAV); o que se perde é a energia da margem quando ela não é usada.
- **(b) Aceitar a órbita do sólido (432 × 693 km) e levar o orbitador até ela** (orbitador só elétrico, XIPS-25 × 10, **calculado, não verificado**; massa de 9 420 kg, a injetada, como limite superior: o tempo sai maior que o real):
  - subir a circular de 380 km até o periapse: 23 m/s, 3,9 dias; essa parte se recupera na espiral de saída (Edelbaum coplanar: o Δv entre circulares soma);
  - subir o apoapse em arcos em torno do periapse (P-049): 56 m/s, 22,8 dias (fim em 438 × 693 km);
  - semieixo dessa órbita a 563 km de altitude (no raio do estudo), acima do limite de 500 km do MSR ([F273] PDF p. 1, sobre o raio equatorial): no MSR, essa órbita estaria fora da faixa aceita;
  - total antes do encontro: 26,7 dias a mais entre o lançamento do MAV e a partida, que atrasam a partida de Marte. Não inclui a fase (RAAN e anomalia) nem o crédito da saída a partir da elipse.
- **Qual afeta menos a missão:** pelos critérios da P-110, só (b) fecha. Se a órbita de (a2), a 0,04 km da circular de 380 km, for aceita, (a) afeta menos (nem massa nem datas), contra os 26,7 dias e o xenônio de (b). A guinada de (a2) não tem fonte para o MAV; o método com fonte do MSR é (a1), que o modelo não reproduz. Decisão do Fabio.

## Proposta de errata da P-110 (para aprovação do Fabio; o valor antigo fica)

- Decisão do Fabio (2026-11-10): a divisão do inerte do [F269] (fração do estágio 2 = 0,444) prevalece como entrada.
- Errata proposta: a P-110 passa a usar a divisão do [F269] na verificação e na escala, no lugar da varredura que escolheu 0,40. O valor antigo, 0,40, fica registrado na errata. Consequência: a verificação deixa de chegar à órbita publicada, e a diferença passa a ser o viés da P-114 (acima).
- Nada foi mudado em config/premissas.yaml para a P-110 nem em results/familia1/mavs.yaml.

