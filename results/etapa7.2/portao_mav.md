# Portão do MAV: conclusão de sistema (gerado por tools/opcoes_arquitetura.py)

Decisão do Fabio (2026-11-07), registrada também no ADR 0023. Números de results/; nada novo calculado aqui.

> A arquitetura de referência da Fase 2 (dois lançamentos, orbitador químico, encontro em 300 × 25.952 km, MAV deitado em aeroshell de 4,5 m) não fecha a embalagem do MAV em nenhuma das rotas calculadas (A com e sem deck, B, sólido). Causa comum: o Δv do MAV até a órbita de encontro (5.772 m/s).

Conclusão parcial do portão da família 1 (decisão do Fabio, 2026-11-10; a linha não foi decidida):

> Com aeroshell de 4,5 m e deck (P-094), nenhum MAV calculado fecha o alvo de +0,05 m com a margem da P-014, em nenhuma das arquiteturas testadas.

A família 1 com o aeroshell de 4,65 m está em results/familia1/aeroshell_465.md.

Resultado parcial da família 1 com o aeroshell de 4,65 m (decisão do Fabio, 2026-11-12; **NÃO VALIDADO**):

> Família 1 com aeroshell de 4,65 m no Vulcan de coifa longa: o MAV sólido com a margem da P-014, massa pela P-113 e comprimento pela P-108 revista, fecha o alvo com deck (488 kg, folga +0,126 m). Pendências: verificação do orbitador só elétrico e tratamento da energia que sobra na subida.

Números de results/familia1/inerte_solido.md (variante A da P-113, com a margem da P-014, 380 km): GLOM de 488,1 kg, comprimento de 3,04 m, folga com deck de +0,126 m no aeroshell de 4,65 m, contra o alvo de +0,05 m.

Δv do MAV com margem, no vigente: 5,772 km/s (results/etapa2.5/arquitetura.yaml); órbita de encontro 300 × 25 952 km.

| Rota | Resultado | Fonte |
| :- | :- | :- |
| A com deck | Isp calculado de 298,2 s: folga com deck de −0,118 a −0,097 m nas quatro geometrias, contra o alvo de +0,05 m | results/etapa7.2/rota_a.md, seção 0 |
| A sem deck | não converge: com o empuxo/peso real, o Δv pedido passa do usado em toda a varredura (de +171 a +417 m/s), até o MAV não decolar | results/etapa7.2/subida_mav.md |
| B (orbitador elétrico, encontro em órbita baixa) | MAV com folga sem deck de +0,032 m (380 km) e +0,000 m (814 km), abaixo do alvo, e com deck negativa; orbitador híbrido com margem no Falcon Heavy de −83,0 a −77,1 %; o só elétrico (calculado, não verificado) fecha massa (+18,7 a +40,7 %) e estada, mas fica pronto em 2030-07-02 e 2030-07-18, depois do último lançamento do MAV (2030-03-06) | results/etapa7.2/rotas_mav.md; ADR 0013, adendo |
| Sólido | GLOM de 553 a 1 645 kg; melhor folga sem deck +0,018 m, no limite do Δv ideal | results/etapa7.2/mav_solido.md |

**Nota (2026-11-12):** a linha do sólido segue a P-108 revista (comprimento pelos motores do catálogo [F270] mais um resto fixo); a folga sem deck mudou com ela. Os valores anteriores estão na errata de results/etapa7.2/mav_solido.md.

## Achado: GLOM da base com o empuxo/peso real (não aplicado)

Com a subida simulada no empuxo/peso real (1,48), a base com o 164:1 converge em GLOM de 355,7 kg, contra 386,8 kg vigentes, com Δv de 100 × 100 km de 3 933,3 m/s contra 4 027,9 m/s de [F37] (results/etapa7.2/subida_mav.md). A folga sem deck da base segue negativa (−0,171 m). **Decisão do Fabio: não substituir o vigente agora; decidir junto com a arquitetura.**

As famílias de arquitetura para a próxima decisão estão em results/etapa7.2/opcoes_arquitetura.md.
