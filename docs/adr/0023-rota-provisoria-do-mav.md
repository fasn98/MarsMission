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
  esboço, a massa dos tanques não acoplada ao GLOM e o Isp mínimo como piso, acima da faixa dos análogos.
- Risco aberto para a Etapa 7.3: a massa por área de 276 a 283 kg/m², contra 211 do Mars 2020. Nenhuma rota resolve isso
  (`docs/etapa7.3_portao_perguntas.md`).
