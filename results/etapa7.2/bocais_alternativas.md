# Portão da 7.2: alternativas para os bocais do estágio 1 do MAV (gerado por tools/bocais_estagio1.py)

Esta página não escolhe, e nenhuma premissa muda. Nada foi redimensionado: as massas são as atuais. A decisão é do Fabio.

**Decisões do Fabio (2026-11-04):**
- **C: DESCARTADA.** Empuxo/peso de 0,68, abaixo de 1 em Marte.
- **F: REFERÊNCIA APENAS.** R-40B fora de produção: [F228] PDF p. 30: "Not in Production; Requires component obsolescence update"; [F106] p. 3: "NIP=Not In Production".

## 1. Cabe, e sobe?

Saídas em círculo mínimo, sem folga entre elas. "Com parede" desconta 0,01 m de cada lado (P-085). Empuxo/peso em Marte com 386,8 kg e g = 3,713 m/s². Δv: efeito só do Isp no estágio 1 (2 777 m/s a 310 s), com as mesmas massas.

| Opção | Variante | Saída (m) | Círculo mínimo (m) | Cabe em Ø 0,57 m? | Empuxo/peso | Isp do catálogo (s) | Variação do Δv (m/s) | Motor (m) | Além da P-086 (m) |
| :- | :- | -: | -: | :- | -: | -: | -: | -: | -: |
| A: 4 × R-4D-11 164:1, Ø maior (a combinação atual) | 164:1 | 0,279 | 0,675 | não | 1,36 | 310 | +0 | 0,554 | 0,000 |
| B: 4 × R-4D-11 44:1 | 44:1 | 0,153 | 0,369 | sim | 1,36 | não dado | não calculável | 0,317 | 0,000 |
| C (DESCARTADA): 2 × R-4D-11 164:1 | 164:1 | 0,279 | 0,559 | só sem parede | 0,68 | 310 | +0 | 0,554 | 0,000 |
| D: 3 × R-4D-11 164:1 | 164:1 | 0,279 | 0,602 | não | 1,02 | 310 | +0 | 0,554 | 0,000 |
| E: 2 × R-42 (M1) | 160:1 | 0,390 | 0,779 | não | 1,24 | 305 | −45 | 0,787 | 0,187 |
| F (REFERÊNCIA APENAS): 1 × R-40B (M3) | 60:1 | 0,401 | 0,401 | sim | 2,79 | 296 | −125 | 0,711 | 0,111 |

## 2. Folga do MAV deitado, com a base no ombro

Mesma conta de results/etapa7.2/portao_decisao.md, menos a metade do que o motor passa da P-086. Folga em m; positivo = cabe.

| Opção | Ø (m) | Comprimento (m) | Tanques, variação de massa (kg) | Aeroshell 4,5 m | Aeroshell 4,65 m |
| :- | -: | -: | -: | -: | -: |
| A | 0,69 | 3,477 | −0,1 | −0,234 | −0,002 |
| A | 0,72 | 3,477 | −0,1 | −0,256 | −0,018 |
| B | 0,57 | 3,561 | +0,0 | −0,188 | +0,017 |
| C (DESCARTADA) | 0,57 | 3,561 | +0,0 | −0,188 | +0,017 |
| C (DESCARTADA) | 0,60 | 3,491 | −0,1 | −0,176 | +0,037 |
| D | 0,63 | 3,477 | −0,1 | −0,190 | +0,029 |
| E | fora da varredura (até 0,75 m) | — | — | — | — |
| F (REFERÊNCIA APENAS) | 0,57 | 3,672 | +0,0 | −0,244 | −0,039 |

## 3. Prós e contras

| Opção | Prós | Contras |
| :- | :- | :- |
| A | mantém o motor, o Isp e o histórico do Orion | muda o Ø do ADR 0022: 0,69 m sem parede, 0,72 m com parede |
| B | cabe em Ø 0,57 m, e o motor é 0,283 m mais curto que a P-086 | [F228] não dá Isp nem massa do 44:1, então a perda não é calculável (na folha, o Isp sobe do 164:1 para o 300:1); o empuxo/peso supõe o mesmo empuxo das outras variantes (não conferido) |
| C (DESCARTADA) | cabe em Ø 0,57 m, por 0,011 m, só sem parede | **empuxo/peso de 0,68, abaixo de 1: não decola na vertical** |
| D | empuxo/peso de 1,02 | não cabe; o empuxo quase não vence o peso; Ø de 0,63 m pela varredura |
| E | em produção, combinação já no catálogo | pior no diâmetro: pede 0,779 m, além da varredura; motor 0,187 m além da P-086 |
| F (REFERÊNCIA APENAS) | cabe em Ø 0,57 m com sobra de 0,169 m; maior empuxo/peso, 2,79 | fora de produção; −125 m/s pelo Isp; motor 0,111 m além da P-086; um só motor, sem redundância e com controle de atitude a definir |

## 4. Diferenças entre fontes (nada foi trocado)

| Motor | Massa no catálogo [F106] (kg) | Massa em [F228] (kg) | Isp no catálogo (s) | Isp em [F228] (s) | Situação em [F228] |
| :- | -: | -: | -: | -: | :- |
| R-42 | 6,58 | 4,53 | 305 | 305 | em produção |
| R-40B | 15,88 | 10,50 | 296 | 293 | fora de produção; pede atualização |

## 5. Não calculado

- **Redimensionamento:** nenhuma opção fechou de novo a massa. O Δv acima é só o efeito do Isp, e os motores de outra massa não entraram.
- **Saídas escalonadas no eixo ou bocais além do corpo:** o contorno dos bocais não é publicado com cotas suficientes.
- **Base alargada só na região dos motores:** muda a folga no aeroshell de um jeito que esta conta não representa.
- **Controle de atitude:** não está modelado em nenhuma opção. No estudo de Bowles, um só motor usa "a single gimbaled engine with pneumatic thrust vectoring control" ([F46] PDF p. 30).
- **Estágio 2:** não entra aqui; a questão do comprimento dele está na seção 7 de portao_decisao.md.

## 6. Fontes da geometria

- R-4D-11 164:1: [F228] PDF p. 22: "164:1 = 19.32"; "164:1 = 11.0"; "164:1 = 311 sec"; "164:1 = 3.76 kg (8.3 lbm)"
- R-4D-11 44:1: [F228] PDF p. 22, desenho: "44:1 = 9.97"; "44:1 = 6.01" (sem Isp nem massa na folha)
- R-42 160:1: [F228] PDF p. 25, desenho: "15.34", "6.0", "25.00", "Dimensions are in inches"; "Expansion Ratio 160:1"; "305 sec"; "4.53 kg (10.0 lbm)"; "Currently in Production"
- R-40B 60:1: [F228] PDF p. 30, desenho: "(15.8")", "(5.7")", "(22.3")" (os rótulos em mm do desenho estão inconsistentes com as polegadas, "40 mm" e "56.6 mm"; usadas as polegadas); "Expansion Ratio 60:1"; "293 sec"; "10.5 kg (23.0 lbm)"; "Not in Production; Requires component obsolescence update"
