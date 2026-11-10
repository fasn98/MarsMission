# Lei de massa inerte do MAV sólido (gerado por tools/inerte_solido.py)

**NÃO VALIDADO.** Premissas P-014, P-019, P-108, P-110, P-111 e P-113 (nova, para aprovação).

## Motores do catálogo [F270] (inerte total impresso, salvo o Orion 38)

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

- **Escala.** A P-019 (k = 0,401 nos dois estágios) e a P-111 (k = 0,299 e 0,791) são proporcionais: o inerte cresce como o propelente (b = 1). O catálogo dá b = 0,70, e b = 1 fica fora de ±2 erros-padrão: **os dados não sustentam a escala proporcional de nenhuma das duas**. Ao crescer, a fração inerte cai.
- **Nível.** No tamanho do MSR, o motor do catálogo é mais leve que o motor do MSR [F269] (tabela acima); a P-111 reproduz o estágio do MSR por construção (verificação da P-110), e a P-019 dá outra divisão entre os estágios. Nenhuma das duas separa o inerte não propulsivo (aviônica, RCS, estrutura da carga), que o [F269] dá à parte e que não precisa crescer com o motor.
- **Proposta (P-113, NÃO VALIDADA, para aprovação):** inerte do estágio = N + c · P^b, com b do catálogo e N, o não propulsivo do [F269], fixo. Duas variantes do nível c: A, pelo motor do MSR [F269]; B, pela divisão que a verificação da P-110 escolheu. A escolha é do Fabio.

## Subida com cada variante (modelo de subida do sólido; tolerância 1e-06, passo da varredura 0,05, os da P-110)

### Lei A (nível do motor pelo [F269])

- N = 14 e 34 kg; c = 1,063 e 0,855; b = 0,701.
- Verificação com o MAV do MSR (órbita publicada de 350 km): inertes 60,0 e 48,1 kg; órbita 318 × 344 km; costa 468 s (publicada 446 s); **não chega à órbita publicada** (resíduo 5,2e+00).

| Caso, 380 km | Escala | Capacidade (m/s) | GLOM (kg) | Propelente (kg) | Inertes (kg) | Órbita simulada (km) | Chega? | Comprimento (m) | 4,65 m com deck | 4,65 m sem deck | 4,5 m com deck |
| :- | -: | -: | -: | -: | -: | :- | :- | -: | -: | -: | -: |
| sem margem (o menor que chega) | 1,075 | 4 110 | 418,0 | 232,3 + 58,5 | 62,4 + 48,8 | 380 × 380 | sim | 2,79 a 2,90 | +0,192 a +0,248 | +0,346 a +0,402 | −0,080 a −0,023 |
| com a margem da P-014 na capacidade | 1,345 | 4 521 | 501,6 | 290,5 + 73,2 | 70,6 + 51,3 | 432 × 693 | não | 3,11 a 3,63 | −0,172 a +0,087 | −0,018 a +0,241 | −0,443 a −0,185 |

### Lei B (nível pela divisão verificada da P-110)

- N = 14 e 34 kg; c = 1,169 e 0,549; b = 0,701.
- Verificação com o MAV do MSR (órbita publicada de 350 km): inertes 64,6 e 43,0 kg; órbita 350 × 350 km; costa 481 s (publicada 446 s); **chega à órbita publicada**.

| Caso, 380 km | Escala | Capacidade (m/s) | GLOM (kg) | Propelente (kg) | Inertes (kg) | Órbita simulada (km) | Chega? | Comprimento (m) | 4,65 m com deck | 4,65 m sem deck | 4,5 m com deck |
| :- | -: | -: | -: | -: | -: | :- | :- | -: | -: | -: | -: |
| sem margem (o menor que chega) | 0,994 | 4 078 | 392,2 | 214,7 + 54,1 | 64,4 + 43,0 | 380 × 380 | sim | 2,68 a 2,69 | +0,297 a +0,302 | +0,451 a +0,455 | +0,026 a +0,030 |
| com a margem da P-014 na capacidade | 1,227 | 4 486 | 464,5 | 265,0 + 66,7 | 72,3 + 44,4 | 422 × 635 | não | 2,97 a 3,31 | −0,012 a +0,158 | +0,141 a +0,311 | −0,284 a −0,114 |

Alvo de folga: +0,05 m. O caso com a margem foi simulado com o mesmo guiamento (subida vertical, tangente linear, costa e queima do estágio 2 antes do apoapse): o sólido não regula o empuxo, então a capacidade a mais só chega à órbita de 380 km se o guiamento conseguir gastá-la; "não" na coluna "Chega?" quer dizer que ele passa da órbita com esse guiamento, não que falta Δv.
