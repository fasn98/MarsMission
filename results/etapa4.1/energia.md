# Energia (gerado por tools/energia.py)

## Lander em Jezero

Estada 2029-09-20 a 2030-11-08 (Ls 190° a 58°), latitude 18,85°. Insolação diária no topo da atmosfera entre 3 627 e 4 672 Wh/m² por sol. Painel horizontal calibrado no 1º sol do InSight (Ls 296°, superfície 3 622 Wh/m², albedo 0,1): η = 0,247. Poeira acumulada no fim da estada, sem limpeza: fator 0,324.

Demanda: plataforma 3 500 Wh/sol (P-032) + aquecimento do MAV 48,0 W (1 185 Wh/sol) = 4 685 Wh/sol.

### Solar (τ constante na estada, como envoltória; bateria para a noite; com margens de crescimento)

O modelo de insolação vale até τ = 6; acima disso usa-se esse limite, e o resultado fica otimista.

| Cenário | τ | τ usado | Carga | Demanda (Wh/sol) | Área (m²) | Painel (kg) | Bateria (kg) | Total (kg) | Pior sol (Ls) |
| :- | -: | -: | :- | -: | -: | -: | -: | -: | -: |
| claro_jezero | 0,4 | 0,4 | operação normal | 4 685 | 16,0 | 84 | 96 | 180 | 58° |
| regional_jezero | 2,0 | 2,0 | operação normal | 4 685 | 25,5 | 134 | 96 | 230 | 58° |
| global_2018 | 8,5 | 6,0 | operação normal | 4 685 | 68,2 | 358 | 96 | 454 | 58° |
| global_2018 | 8,5 | 6,0 | só o aquecimento do MAV (sobrevivência) | 1 185 | 17,2 | 91 | 24 | 115 | 58° |
| claro_jezero | 0,4 | 0,4 | operação normal, sem poeira acumulada (sensibilidade) | 4 685 | 6,3 | 33 | 96 | 129 | 276° |

### MMRTG

2 unidade(s): 99,9 W cada no fim da estada (1,95 anos depois do lançamento), para 190,0 W médios; 90 kg; 3 950 W térmicos.

### Verificação da insolação diária contra a tabela do VL1 (22,3° N) [F56]

| Ls | τ | Publicado (Wh/m², horas terrestres) | Calculado (Wh/m²) | Diferença |
| -: | -: | -: | -: | -: |
| 69 | 0,65 | 3 430 | 3 443 | 0,4 % |
| 120 | 0,40 | 3 965 | 3 960 | −0,1 % |
| 153 | 0,50 | 3 987 | 3 976 | −0,3 % |
| 249 | 1,40 | 1 951 | 1 931 | −1,1 % |
| 299 | 3,25 | 1 052 | 1 070 | 1,8 % |

Maior diferença: 1,8 %.

## Orbitador

Distância máxima ao Sol por fase (janelas do envelope e referência): ida 1,507 UA, marte 1,666 UA, volta 1,665 UA; afélio de Marte 1,666 UA. Eclipse máximo: encontro 3,24 h, captura_1sol 4,19 h.

| Modo (proposta P-053) | Carga (W) | Distância (UA) | Eclipse (h) | Painel a 1 UA equivalente (W) | Painel sem margem (kg) | Energia no eclipse (Wh) |
| :- | -: | -: | -: | -: | -: | -: |
| cruzeiro | 745 | 1,507 | 0,00 | 745 | 27,3 | 0 |
| captura | 310 | 1,666 | 4,19 | 390 | 17,5 | 1 300 |
| encontro | 1 022 | 1,666 | 3,24 | 1 319 | 59,1 | 3 306 |
| retorno | 945 | 1,666 | 3,24 | 1 220 | 54,7 | 3 057 |

Modo dominante: encontro.

| | Carga (W) | Plataforma (kg) | Painel no afélio (W) | Bateria (Wh) | Orbitador injetado (kg) | Na órbita baixa (kg) |
| :- | -: | -: | -: | -: | -: | -: |
| Atual (P-028) | 510 | 496,5 | 658 | 5 500 | 7 205 | 21 872 |
| Proposta (P-053) | 1 022 | 609,8 | 1 319 | 11 021 | 7 882 | 23 928 |

Margens dos lançadores escolhidos para o orbitador (injeção direta, pior janela; órbita de encontro fixa): Falcon Heavy (descartável) +56 % → +42 %; Vulcan VC6 +15 % → +5 %.

Sensibilidade da bateria com a profundidade de descarga do MRO (40 %, [F139]): 4 125 Wh (atual) e 8 266 Wh (proposta), contra 5 500 e 11 021 Wh com 30 % (config).
