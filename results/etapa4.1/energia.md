# Energia (gerado por tools/energia.py)

## Lander em Jezero

Estada 2029-09-20 a 2030-11-08 (Ls 190° a 58°), latitude 18,85°. Insolação diária no topo da atmosfera entre 3 627 e 4 672 Wh/m² por sol. Painel horizontal calibrado no 1º sol do InSight (Ls 296°, superfície 3 622 Wh/m², albedo 0,1): η = 0,247. Poeira acumulada no fim da estada, sem limpeza: fator 0,324.

Demanda: plataforma 3 500 Wh/sol (P-032) + aquecimento do MAV 48,3 W (1 191 Wh/sol) = 4 691 Wh/sol.

### Solar (τ constante na estada, como envoltória; bateria para a noite; com margens de crescimento)

A energia da noite passa pela bateria (eficiência de recarga da P-029): a produção necessária é 1,125 × a demanda.

O modelo de insolação vale até τ = 6; acima disso usa-se esse limite, e o resultado fica otimista.

| Cenário | τ | τ usado | Carga | Demanda (Wh/sol) | Área (m²) | Painel (kg) | Bateria (kg) | Total (kg) | Pior sol (Ls) |
| :- | -: | -: | :- | -: | -: | -: | -: | -: | -: |
| claro_jezero | 0,4 | 0,4 | operação normal | 4 691 | 18,0 | 95 | 99 | 194 | 58° |
| regional_jezero | 2,0 | 2,0 | operação normal | 4 691 | 28,7 | 151 | 99 | 250 | 58° |
| global_2018 | 8,5 | 6,0 | operação normal | 4 691 | 76,8 | 404 | 99 | 502 | 58° |
| global_2018 | 8,5 | 6,0 | sobrevivência: MAV + aquecedores e eletrônica do lander (P-056) | 1 694 | 27,7 | 146 | 35 | 180 | 58° |
| claro_jezero | 0,4 | 0,4 | operação normal, sem poeira acumulada (sensibilidade) | 4 691 | 7,1 | 38 | 99 | 136 | 276° |
| global_2018 | 8,5 | 6,0 | sobrevivência, aquecedores com escala linear na massa (sensibilidade da P-056) | 2 086 | 34,1 | 180 | 43 | 222 | 58° |

### Opção C: solar com sobrevivência (linha de base)

Carga de sobrevivência na tempestade global (P-056): MAV 1 191 Wh/sol + aquecedores do lander 363 Wh/sol (84 Wh/sol do Spirit × (1 565 kg / 174 kg)^0,67) + eletrônica mínima 140 Wh/sol = 1 694 Wh/sol. Com escala linear na massa (sensibilidade): 2 086 Wh/sol.

Painel e bateria para os dois casos (a maior área e a maior bateria; a área sai da sobrevivência): 27,7 m², painel 146 kg, bateria 99 kg, total 245 kg. Sensibilidade com escala linear: 34,1 m², total 278 kg (área da sobrevivência).

Comparação do modelo com o Opportunity na tempestade de 2018 [F140] (razão de energia contra o sol de τ = 0,64; latitude do sítio, painel horizontal, poeira constante):

| Sol | Data | τ | Razão medida | Razão do modelo | Diferença |
| -: | :- | -: | -: | -: | -: |
| 5106 | 2018-06-04 | 2,1 | 0,529 | 0,666 | 25,8 % |
| 5111 | 2018-06-10 | 10,8 | 0,034 | fora do modelo (τ > 6) | — |

Acima de τ = 6 (P-057): com τ = 10,8 o Opportunity produziu 3,4 % da energia de τ = 0,64. Aplicada ao painel da opção C no pior sol da estada: 254 Wh/sol contra 1 906 Wh/sol necessários (13 %); a sobrevivência nessa condição exigiria 208 m². Sensibilidade (escala linear): 13 %, 256 m². A duração da fase com τ > 6 e a ponte pela bateria não foram avaliadas.

Desfecho do único dado de voo acima de τ = 6: [F140] sóis 5292–5299 (13–20/12/2018): "No signal from Opportunity has been heard since Sol 5111 (June 10, 2018). Opportunity likely experienced a low-power fault, a mission clock fault and an up-loss timer fault".

Picos por sol (na bateria das duas opções): braco 20,0 Wh, recarga_helicopteros 17,5 Wh, transmissoes_uhf 34,5 Wh; total 72,0 Wh.

### Alternativa A: MMRTG (condicionada à disponibilidade de Pu-238)

2 unidade(s): 99,9 W cada no fim da estada (1,95 anos depois do lançamento, 90,8 % da inicial), para 190,2 W médios (sobra de 237 Wh/sol); 90 kg sem margem + margem de 27,5 % + bateria dos picos 2,9 kg = 118 kg; 3 950 W térmicos; 6 956 g de Pu-238. Sensibilidade com o abastecimento 1 ano antes do lançamento: 95,1 W cada, 2 unidade(s).

Atividade do Pu-238: 4 408 TBq = 4,41 × 10⁶ A2 (44,1 vezes o limite do Tier I do NSPM-20, 100 mil A2): acima do Tier I: Tier II, ou Tier III se a análise de segurança der probabilidade ≥ 1e-6 de exposição acima de 25 rem (não avaliada).

Disponibilidade de Pu-238:

- [F143] p. 27 do PDF: "although DOE planned to produce a total of 1.5 kg from 2018 through 2021, they produced only 0.77 kg"
- [F143] p. 28 do PDF: "the Dragonfly rotorcraft is being designed with one MMRTG requiring 32 fueled clads"; "DOE can only produce about 187 fueled clads over that time period—101 fewer than needed"
- [F143] p. 13 do PDF: "a fueled clad containing 150 grams of Pu-238"
- [F144] p. PS-104: "DoE continues to increase annual production, producing approximately 700 grams per year"
- [F145] p. 32 do PDF: "In July 2025, DOE informed NASA that DOE did not have sufficient thermal inventory to provide an in-spec multi-mission radioisotope thermoelectric generator for a baselined mission"
- [F146] p. PS-56: "The budget assumes a pause in the development of additional units after completion of the MMRTG for the Dragonfly mission"

### Comparação com bases iguais (margens de crescimento e bateria dos picos nas duas fontes)

| Opção | Massa (kg) | Área (m²) | Pu-238 | Tempestade global (inclusive τ > 6) | Degradação na estada |
| :- | -: | -: | :- | :- | :- |
| **C. Solar com sobrevivência (linha de base)** | 245 | 27,7 | — | sobrevive (MAV + lander, P-056) até τ = 6; com τ = 10,8, 13 % da energia de sobrevivência (P-057) | poeira: fator 0,324 no fim, sem limpeza |
| A. MMRTG × 2 (alternativa condicionada) | 118 | — | 6 956 g; condicionada à disponibilidade (fatos acima); acima do Tier I do NSPM-20 | não depende de τ | potência no fim 90,8 % da inicial |
| B. Solar, céu claro | 194 | 18,0 | — | não atravessa: com τ = 6 a energia cai a 23,5 % da de céu claro | poeira: fator 0,324 |
| D. Solar operando na tempestade | 502 | 76,8 | — | opera até τ = 6; acima, ver a razão do Opportunity | poeira: fator 0,324 |

### Verificação da insolação diária contra a tabela do VL1 (22,3° N) [F56]

A tabela é cálculo publicado (modelo de Appelbaum & Flood), não medida: a comparação verifica a implementação.

| Ls | τ | Publicado (Wh/m², horas terrestres) | Calculado (Wh/m²) | Diferença |
| -: | -: | -: | -: | -: |
| 69 | 0,65 | 3 430 | 3 443 | 0,4 % |
| 120 | 0,40 | 3 965 | 3 960 | −0,1 % |
| 153 | 0,50 | 3 987 | 3 976 | −0,3 % |
| 249 | 1,40 | 1 951 | 1 931 | −1,1 % |
| 299 | 3,25 | 1 052 | 1 070 | 1,8 % |

Maior diferença: 1,8 %.

## Orbitador

Distância máxima ao Sol por fase (janelas do envelope e referência): ida 1,507 UA, marte 1,666 UA, volta 1,665 UA; afélio de Marte 1,666 UA. Eclipse máximo: encontro 3,34 h, captura_1sol 4,19 h.

| Modo (P-053) | Carga (W) | Distância (UA) | Eclipse (h) | Potência do painel na distância (W) | Painel sem margem (kg) | Energia no eclipse (Wh) |
| :- | -: | -: | -: | -: | -: | -: |
| cruzeiro | 745 | 1,507 | 0,00 | 745 | 27,3 | 0 |
| captura | 310 | 1,666 | 4,19 | 390 | 17,5 | 1 300 |
| encontro | 1 022 | 1,666 | 3,34 | 1 314 | 58,9 | 3 410 |
| retorno | 945 | 1,666 | 3,34 | 1 215 | 54,5 | 3 153 |

Modo dominante: encontro.

| | Carga (W) | Plataforma (kg) | Painel no afélio (W) | Bateria (Wh) | Orbitador injetado (kg) | Na órbita baixa (kg) |
| :- | -: | -: | -: | -: | -: | -: |
| Anterior (510 W) | 510 | 498,7 | 656 | 5 672 | 7 117 | 21 603 |
| Adotada (P-028 = modo dominante da P-053) | 1 022 | 614,0 | 1 314 | 11 367 | 7 796 | 23 667 |

A linha anterior usa as perdas e o apoapse atuais (sensibilidade, não o resultado da Etapa 3.4).

Margens dos lançadores escolhidos para o orbitador (injeção direta, pior janela; órbita de encontro fixa), anterior → adotada: Falcon Heavy (descartável) +58 % → +44 %; Vulcan VC6 +17 % → +6 %.

Sensibilidade da bateria com a profundidade de descarga do MRO (40 %, [F139]): 4 254 Wh (anterior) e 8 525 Wh (adotada), contra 5 672 e 11 367 Wh com 30 % (config).
