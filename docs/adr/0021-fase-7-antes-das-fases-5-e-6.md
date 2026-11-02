# ADR 0021 — Fase 7 (CAD paramétrico no Onshape) antes das Fases 5 e 6

Status: Aceito (Fabio, 2026-11-01)
Data: 2026-11-01

## Contexto
- **Estado:** a Fase 4 (subsistemas) terminou com a arquitetura vigente (`docs/fase4_relatorio.md`, `results/fase4/resumo.md`).
- **Ordem prevista:** as Fases 5 e 6 viriam antes do CAD. Hoje elas aparecem citadas só como destino de itens adiados (por
  exemplo, o custo dos lançadores fica para a Fase 6, ADR 0020).
- **Pedido do Fabio:** começar a Fase 7, o CAD paramétrico no Onshape, com FeatureScript, no padrão já usado no projeto do
  drone (repositório fasn98/AeroDesignFlow).

## Decisão
1. **A Fase 7 é feita antes das Fases 5 e 6** (decisão do Fabio, 2026-11-01).
2. **Etapas:**
   - 7.1: envelope e arranjo;
   - 7.2: FeatureScript paramétrico;
   - 7.3: propriedades de massa;
   - 7.4: integração.
   Cada etapa tem portão.
3. **Regras próprias do CAD:**
   - toda dimensão vem de `results/` ou `config/` por script, ou de fonte publicada; dimensão sem fonte é premissa NÃO
     VALIDADA, e nenhuma é digitada direto no FeatureScript;
   - a massa do CAD não é ajustada para bater com o orçamento: a diferença fica explícita.

## Consequências
- **Arquitetura:** o CAD parte da arquitetura do fim da Fase 4. O que as Fases 5 e 6 mudarem depois volta para o CAD pelos
  scripts, regenerando os parâmetros.
- **Twin e entrada atmosférica:** o CG e as inércias da Etapa 7.3 alimentam o Twin (Fase 8) e a entrada atmosférica
  (deslocamento do CG).
- **Padrão do drone:** o repositório fasn98/AeroDesignFlow não estava acessível com o token desta sessão (não aparece
  na lista de repositórios nem na busca). Antes da Etapa 7.2 é preciso dar acesso de leitura ou indicar outro meio de
  consultar o padrão. Não conferido.
