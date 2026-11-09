# ADR 0023: rota provisória do MAV e alvo com deck

Status: Aceito como PROVISÓRIO (Fabio, 2026-11-06, portão do comprimento do MAV)
Data: 2026-11-06

## Contexto
A Etapa 7.2 mostrou que o MAV de Ø 0,57 m não cabe deitado no aeroshell de 4,5 m nem contém as saídas dos bocais
(`results/etapa7.2/rotas_mav.md`). O alvo de 4,5 m vem da folga confirmada na coifa do Vulcan.

## Decisão
1. **Rota A (R-4D-11 44:1 e tanques aninhados): PROVISÓRIA**, condicionada a:
   - Isp, massa e empuxo do 44:1 com fonte;
   - dimensionamento dos tanques aninhados.
2. **A rota A não é aplicada** ao CAD nem às premissas enquanto as condições não forem cumpridas.
3. **Alvo de projeto: com deck.** MAV deitado com, no máximo, 2,74 m em Ø 0,57 m, ajustado ao Ø que contenha as saídas com
   parede. O limite sem deck, 3,18 m, fica registrado como limite otimista.
4. **Rota B (orbitador elétrico):** trade feito e rejeitado; ver o adendo do ADR 0013.

## Consequências
- O arranjo do CAD atual e a P-086 continuam como estão até o portão seguinte.
- O ADR 0022 segue em vigor no CAD.
- A condição (ii) ainda não foi cumprida: `results/etapa7.2/rota_a.md` traz o primeiro dimensionamento, com o estágio 2 só em
  esboço, com a geometria ainda a decidir, a massa dos tanques não acoplada ao GLOM e o Isp mínimo dependente dessa geometria.
- Risco aberto para a Etapa 7.3: a massa por área de 276 a 283 kg/m², contra 211 do Mars 2020. Nenhuma rota resolve isso
  (`docs/etapa7.3_portao_perguntas.md`).

## Nota (2026-11-07): Isp calculado do 44:1
O Fabio rejeitou a faixa dos análogos como Isp do R-4D-11: é o mesmo motor com bocal menor, então o Isp fica abaixo do 164:1. O
cálculo está em [`results/etapa7.2/isp_44.md`](../../results/etapa7.2/isp_44.md), NÃO VALIDADO, e a consequência para a rota A, em
[`results/etapa7.2/rota_a.md`](../../results/etapa7.2/rota_a.md), seção 0. A geometria do estágio 2 segue não decidida. Alvo mantido:
folga de +0,05 m com deck.

## Nota (2026-11-07): rota A com deck não fecha (decisão do Fabio)
Com o Isp calculado do 44:1 (NÃO VALIDADO), a rota A **com deck não fecha** no alvo de +0,05 m, em nenhuma das quatro
geometrias do estágio 2 ([`results/etapa7.2/rota_a.md`](../../results/etapa7.2/rota_a.md), seção 0). A rota A **sem deck** fica
pendente da perda gravitacional na subida com o empuxo/peso real e da viabilidade do arranjo sem deck, com fonte. A P-094 e a
P-092 seguem como estão. O texto acima não muda.

## Nota (2026-11-07): conclusão de sistema (decisão do Fabio, portão do PR #55)
"A arquitetura de referência da Fase 2 (dois lançamentos, orbitador químico, encontro em 300 × 25.952 km, MAV deitado em
aeroshell de 4,5 m) não fecha a embalagem do MAV em nenhuma das rotas calculadas (A com e sem deck, B, sólido). Causa comum: o
Δv do MAV até a órbita de encontro (5.772 m/s)."

Resultados de cada rota, com os números em [`results/etapa7.2/portao_mav.md`](../../results/etapa7.2/portao_mav.md):
- **A com deck:** `results/etapa7.2/rota_a.md`, seção 0;
- **A sem deck:** `results/etapa7.2/subida_mav.md`, sem ponto fixo com o empuxo/peso real;
- **B:** `results/etapa7.2/rotas_mav.md` e o adendo do ADR 0013;
- **sólido:** `results/etapa7.2/mav_solido.md`.

As famílias de arquitetura para a próxima decisão estão em [`results/etapa7.2/opcoes_arquitetura.md`](../../results/etapa7.2/opcoes_arquitetura.md).
O GLOM da base com o empuxo/peso real fica como achado, sem substituir o vigente (decisão do Fabio). O texto acima não muda.

