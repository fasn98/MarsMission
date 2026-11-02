# ADR 0022 — Arranjo dos veículos: aeroshell de 4,65 m (condicional), MAV de Ø 0,57 m e dois pares de tanques no orbitador

Status: Aceito (Fabio, 2026-11-02, portão da Etapa 7.1)
Data: 2026-11-02

## Contexto
A Etapa 7.1 (`docs/etapa7.1_envelope.md`, `results/etapa7.1/envelope.md`) derivou o envelope e o arranjo dos veículos:
- duas opções de aeroshell: 4,5 m (Mars 2020) e 4,65 m (SRL de lançamento duplo [F202]);
- duas opções de diâmetro do MAV: 0,50 m (limite do MSR [F35]) e 0,57 m (restrição de 2019 [F216]);
- dois arranjos de tanques no orbitador: dois pares ou um par por estágio.

## Decisão
1. **Aeroshell de 4,65 m**, porque a massa por área do lander (261 kg/m²) fica abaixo da classe do SRL.
   - **Condição:** a Etapa 7.2 confere a folga radial no Vulcan com a geometria real do conjunto, sem a altura escalada
     da P-083.
   - Se a folga não se confirmar, volta para 4,5 m, e a massa por área de 279 kg/m² fica registrada como risco de EDL.
2. **MAV de Ø 0,57 m** (3,56 m de comprimento).
   - O limite de 3 m do MSR fica como referência, não como restrição do estudo.
   - A Etapa 7.2 confere obrigatoriamente o MAV deitado contra o estreitamento da casca traseira.
3. **Orbitador com dois pares de tanques por estágio.**
4. **P-078 a P-088:** aprovadas, NÃO VALIDADAS. Procurar fonte para a densidade da hidrazina (P-079).

Registrado em `config/cad.yaml` (`escolha`).

## Consequências
- O FeatureScript da Etapa 7.2 usa essas escolhas, e os parâmetros são gerados por `tools/` a partir de `results/`.
- As duas conferências condicionais (folga no Vulcan e MAV na casca traseira) são resultado da Etapa 7.2 e voltam ao
  portão dela.
