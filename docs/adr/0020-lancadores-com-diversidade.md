# ADR 0020 — Lançadores de base com diversidade: lander no Vulcan VC4, orbitador no Falcon Heavy descartável

Status: Accepted (Fabio, 2026-11-01, portão da Etapa 4.5)
Data: 2026-11-01

## Contexto
- **Margem do lander:** com a P-017 no caso B (ADR 0019), a margem do lander fica pequena no Falcon Heavy com recuperação e
  negativa no Vulcan VC2 (`results/etapa4.5/lista_massas.md`).
- **Mitigações do risco do MAV apresentadas** (`docs/etapa4.5_massas.md`, seção 5):
  - (a) margem de lançador: sem número de política com fonte;
  - (b) lançador maior para o lander;
  - (c) Isp maior.
- **Orbitador:** já depende do Falcon Heavy descartável (ADR 0008; o Vulcan VC6 tem margem pequena).

## Decisão
1. **Mitigação (b), lançador maior para o lander, com diversidade de veículo:**
   - lander no **Vulcan VC4**, com o **Vulcan VC6** de reserva;
   - orbitador no **Falcon Heavy descartável**;
   - registrado em `config/lancadores.yaml` (`base`).
2. **Motivo da diversidade:** evitar que as duas metades da missão dependam do mesmo veículo. Com o lander também no Falcon
   Heavy descartável, uma indisponibilidade desse lançador pararia as duas.
3. **(c) descartada:** o ganho é pequeno e reabriria o ADR 0011 (troca de combustível com os LEROS).
4. **Custo dos lançadores:** fica para a Fase 6.

## Consequências
- **Margens:** as margens do lander no VC4 e no VC6, na base e nas sensibilidades, estão em
  `results/etapa2.5/arquitetura.md`.
- **Lista de lançadores que servem:** continua em `config/lancadores.yaml` (`escolha`). A base só indica o veículo adotado.
- **ADR 0008:** continua valendo para a forma de lançamento (injeção direta, lançamentos separados). Este ADR fixa os
  veículos de base.
