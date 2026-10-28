# ADR 0013 — Propulsão do orbitador: química (elétrica e híbrida avaliadas e não adotadas)

Status: Accepted (Fabio, 2026-10-28, portão da Etapa 3.3)
Data: 2026-10-28

## Contexto
A Etapa 3.3 comparou três opções de propulsão para o orbitador (`docs/etapa3.3_orbitador.md`,
`results/etapa3.3/orbitador_eletrico.md`):
- (a) químico atual;
- (b) elétrico, no cruzeiro e na espiral;
- (c) híbrido: captura química e espiral elétrica até a órbita baixa.

O híbrido foi avaliado em duas concepções:
- **(c2):** captura em órbita circular e espiral tangencial verificada. Cabe no tempo, mas não cabe em massa.
- **(c1):** captura na elipse e descida em arcos em torno do periapse. Não cabe no tempo da estada.

A opção (b) foi estimada só em ordem de grandeza, com o rótulo "calculado, não verificado".

## Decisão
1. **Propulsão do orbitador: (A), química** (a atual: ADR 0011, órbita de encontro do ADR 0005).
2. **Conclusão registrada:** "Na missão de referência (414 dias em Marte) e com as leis de guiagem verificadas, nenhuma
   opção elétrica fecha massa e tempo. Uma missão de estada longa, como a do ERO, poderia mudar isso, mas exigiria outra
   missão de referência e uma guiagem otimizada, não estudadas."
3. **Estudo futuro (B):** missão de estada longa, como a do ERO, com outra missão de referência (ADR 0003) e uma guiagem
   otimizada da descida, verificada.
4. **Catálogo de propulsores elétricos:** só NSTAR e XIPS-25 (`config/eletrica.yaml`).
5. **Premissas P-047 a P-049:** aprovadas, NÃO VALIDADAS.
6. **Limitação registrada como está:** o tempo de encontro (22 d [F121]) não inclui a fase de RAAN de 24 d da mesma
   fonte. Ela só piora o elétrico: as folgas do c2 com 1 e com 2 NSTAR (13 e 21 d, `results/etapa3.3/orbitador_eletrico.md`)
   são menores que os 24 d.

## Consequências
- A arquitetura não muda:
  - orbitador de 7.205 kg e lander de 3.996 kg;
  - total (iii) de 34.003 kg;
  - órbita de encontro de 300 × 24.992 km.
  - Fonte: `results/etapa2.5/arquitetura.md`.
- A mitigação do risco do MAV por órbita de encontro mais baixa com orbitador elétrico **não se confirmou**. Ver a nota de
  2026-10-28 no ADR 0007.
