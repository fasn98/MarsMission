# ADR 0005 — Arquitetura de superfície e órbita de encontro

Status: Accepted (Fabio, 2026-10-27, portões da Etapa 2.1); **apoapse atualizado** no portão da propulsão do MAV (ADR 0007) e no portão da Etapa 2.3 (plataformas)
Data: 2026-10-27

## Contexto
A Etapa 2.1 comparou quatro arquiteturas de superfície (S1–S4) e fez uma varredura da órbita de
encontro (`docs/etapa2.1_superficie.md`). Com o orbitador químico da Fase 1, descer até uma órbita
baixa custa ~1,2 km/s, e partir de lá para a Terra custa outros ~1,2 km/s.

## Decisão
1. **Arquitetura: família S2.** O lander faz entrada direta a partir da trajetória hiperbólica, e o
   encontro acontece em órbita elíptica, com **orbitador químico**. S1, S3 e S4 ficam descartadas com
   propulsão química. **Encontro em órbita baixa exige propulsão elétrica no orbitador**, a ser avaliada
   na Fase 3.
2. **Periapse da órbita de encontro: 300 km.** É o requisito de vida orbital do contêiner de amostras
   do MSR: "Its periapsis should be above 300 km" (Martin-Mur et al., ISSFD 2024, p. 4 [F32]).
3. **Regra de escolha do apoapse:** o **menor apoapse** cuja massa total na órbita baixa da Terra
   (orbitador + lander, lançamentos separados) pela regra (iii) fique **até 5 % acima do mínimo** da
   varredura.
4. **Resultado:** apoapse de **18.483 km**, ou seja, órbita de encontro de 300 × 18.483 km.
   - Total pela regra (iii): 41.168 kg, 4,5 % acima do mínimo de 39.398 kg, que fica no extremo da
     varredura (apoapse de 33.793 km).
   - Total na missão A: 29.709 kg.
   - MAV: 1404 kg na decolagem, com Δv de subida de 5,17 km/s sem margem.
   - Fonte: `results/etapa2.1/varredura_encontro_rp300.yaml`, gerado por `tools/varredura_encontro.py`.
   - A varredura usa 120 pontos geométricos entre 380 e 33.793 km. Entre pontos vizinhos, o apoapse
     muda ~3,8 %; o valor escolhido tem essa resolução.

## Atualização (ADR 0007, MAV hipergólico)
Com o MAV hipergólico (O4, com aquecimento na superfície), a mesma regra dos 5 % aplicada à varredura
com periapse de 300 km escolhe **apoapse de 26.950 km**. A órbita de encontro passa a ser **300 × 26.950 km**.
- Total pela regra (iii): 31.233 kg, contra o mínimo de 29.948 kg no extremo da varredura.
- Total na missão A: 21.298 kg.
- MAV: 286 kg.
- Fonte: `results/etapa2.2/mav_propulsao.yaml` e `results/etapa2.1/varredura_encontro_rp300_O4.yaml`,
  gerados por `tools/mav_propulsao.py`.

O valor de 18.483 km dos itens 4 e seguintes vale para o MAV sólido e fica como histórico.

## Atualização (Etapa 2.3, plataformas)
Com as plataformas escolhidas pelo Fabio no portão da Etapa 2.3, a mesma regra dos 5 % escolhe
**apoapse de 24.992 km**. A órbita de encontro passa a ser **300 × 24.992 km**.
- Plataformas: orbitador de 442,3 kg (lista por subsistema, P-016) e lander de 1558,5 kg (L3 + amostras
  provisórias, P-017), no lugar dos 850 kg de cada.
- A bateria do orbitador depende do eclipse e, portanto, do apoapse. Plataforma e apoapse foram
  iterados até o apoapse não mudar (duas iterações).
- Total pela regra (iii): 29.607 kg, 4,6 % acima do mínimo de 28.309 kg no extremo da varredura.
- Total na missão A: 22.083 kg.
- MAV: 282,5 kg.
- Fonte: `results/etapa2.3/plataformas.yaml`, gerado por `tools/plataformas.py`.
- No primeiro portão da Etapa 2.3, com o lander sem o item de amostras (1470 kg), o apoapse também
  era 24.992 km, com 29.063 kg (iii) e 21.539 kg (A).

Os valores de 26.950 km acima ficam como histórico.

## Hipóteses mantidas
- Orbitador e lander em lançamentos separados, como no MSR, os dois na janela da missão A (2028).
- O orbitador chega à órbita de 1 sol (ADR 0003) e desce até a órbita de encontro com propulsão
  química: baixa o apoapse no periapse e sobe o periapse de 250 para 300 km no apoapse. Para a injeção
  trans-Terra, usa o mais barato entre partir da órbita de encontro ou voltar à de 1 sol.

## Riscos registrados (não modelados)
- **Encontro em órbita elíptica** (período de ~12,2 h a 300 × 18.483 km): detecção e rastreio do
  contêiner, navegação relativa, fases e velocidades altas perto do periapse. O MSR fazia o encontro
  numa órbita baixa quase circular.
- **Aerofrenagem:** fica só como referência (P-020), sem uso na arquitetura escolhida.
- **O mínimo pela regra (iii) está no extremo da varredura**, o apoapse da órbita de 1 sol. Apoapses
  maiores não foram explorados.

## Consequências
- O MAV cresce de ~340 kg (encontro em órbita baixa) para ~1,4 t. Esse é o ponto de partida da Etapa
  2.2 (ISRU).
- Se a Fase 3 adotar propulsão elétrica no orbitador, esta decisão deve ser revista.

## Nota (2026-10-27): redimensionamento da Etapa 3.1 (ADR 0011)
- Com os motores escolhidos e as perdas de queima finita calculadas, a regra dos 5 % foi reaplicada
  (`results/etapa2.3/plataformas.md`). O apoapse continua **24.992 km**: a órbita de encontro segue em 300 × 24.992 km.
- As massas mudaram (ver a errata em `docs/fase2_relatorio.md`).

## Nota (2026-10-28): orbitador elétrico avaliado na Fase 3 (ADR 0013)
O item 1 deixou o encontro em órbita baixa com orbitador elétrico para a Fase 3. A Etapa 3.3 avaliou a opção e ela não
foi adotada (ADR 0013): na missão de referência, nenhuma opção elétrica fecha massa e tempo. A família S2 e a órbita de
encontro de 300 × 24.992 km continuam.
