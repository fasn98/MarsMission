# MarsMission: regras de trabalho do projeto

Estudo conceitual (Pré-Fase A) de uma missão robótica Terra–Marte–Terra. Autor e decisor: Fabio Nogueira (@fasn98).
Estas regras valem para qualquer agente ou pessoa que trabalhe neste repositório. Elas têm precedência sobre regras
genéricas.

## Ciência e dados
1. **Só física e fontes verificáveis.** Toda constante tem fonte primária citada no código e em `docs/fontes.md`
   (`[Fnn]`), com a citação literal e a página quando houver. Fonte secundária ou de terceiros não basta.
2. **Valor sem fonte é premissa.** Entra em `config/premissas.yaml` com status **NÃO VALIDADA**. Só o Fabio muda esse
   status. Tolerância de teste, faixa de busca e fator de escala sem fonte também são premissas.
   - Mudança de valor-base de premissa só com aprovação prévia do Fabio; quando não der para esperar, pare e pergunte.
3. **"Verificado" ≠ "validado".** "Verificado" só quando o resultado é comparado com dados publicados. Este estudo
   nunca afirma "validado".
4. **Configuração em `config/`, resultados em `results/`.**
   - `results/` só é escrito por scripts em `tools/`, nunca à mão.
   - Formato novo de resultado: um script novo em `tools/`.
   - Todo número em relatório, ADR, PR ou painel vem de `results/` (ou de `src/` chamado sobre `config/`), nunca
     digitado.
   - A regra de números só de `results/` vale para resultados científicos; observações de ambiente são permitidas
     com data e máquina.
5. **Erratas são acrescentadas.** Nunca apagar o texto original de relatórios e ADRs: acrescentar uma seção
   "Errata" ou "Nota", com data, que diga o que muda e quais números estão vigentes.
6. **Reprodutibilidade.**
   - Todo `results/` versionado precisa sair do código e do `config/` atuais.
   - `tools/confere_regeneracao.py` regenera tudo numa cópia e compara com o versionado.
   - O CI roda essa verificação (`.github/workflows/regeneracao.yml`).
   - **"Idêntico" significa dentro das tolerâncias declaradas.**
     - Números (YAML, Markdown, NPZ): a (versionado) e b (regenerado) passam se |a − b| ≤ max(1e-9 · |b|, 1e-10) (P-039).
     - PNG: até 0,1 % dos pixels diferentes (P-040).
     - As duas são premissas NÃO VALIDADAS, decididas pelo Fabio.
     - O limite numérico vem da precisão relevante do estudo (~1e-4 relativo), com 5 ordens de folga para o ruído entre
       CPUs amplificado por cálculos mal condicionados (giro de plano, equação do foguete). Não deriva do ruído
       observado.
   - **Diferença acima do limite é problema a investigar**, nunca motivo para alargar a tolerância sem decisão do Fabio.
   - Texto, estrutura, forma e NaN nunca são tolerados.
   - A verificação é bloqueante, e cada relatório lista as diferenças abaixo do limite, com o tamanho.
   - Quando uma mudança altera um resultado de etapa anterior, regenerar e registrar errata no mesmo PR.

## Fluxo
7. **Portões.** O trabalho é dividido em fases, etapas e portões.
   - Em cada portão: parar e mostrar os números antes e depois.
   - Nenhuma escolha de arquitetura é do agente: apresentar as opções lado a lado, com prós, contras e fontes, e o
     Fabio decide. A decisão vira ADR em `docs/adr/` (uma por arquivo).
8. **Branches pequenos e PR.**
   - Um branch por etapa ou correção; push e PR só quando o Fabio autorizar.
   - Merge só com o CI verde. Quem faz o merge é o Fabio.
9. **Hook de pre-commit com pytest.**
   - Ativar com `git config core.hooksPath .githooks`; o hook usa `$MARSMISSION_PYTHON` ou o `python` do ambiente.
   - Nunca usar `git commit --no-verify`. Se o hook falhar, corrigir a causa.
10. **Revisão independente antes de todo push.**
    - Um revisor separado, somente leitura, que não escreveu o código.
    - Se houver achado bloqueante, corrigir e fazer **segunda revisão**, limitada às correções, antes do push.
    - O revisor pode concluir "nada bloqueante".
11. **Execuções longas em worktree.**
    - Regenerações e conferências longas (`tools/confere_regeneracao.py`, `tools/confere_2033.py`) rodam num
      `git worktree add <dir> <commit>`, fixo no commit conferido.
    - Assim, trocar de branch no diretório principal não afeta a execução.
    - Remover o worktree ao terminar (`git worktree remove`).
12. **Relato honesto.** Teste não rodado não é teste passando. Etapa pulada ou não conferida é dita explicitamente.
    Afirmação sobre ferramenta ou serviço externo (ex.: Replit) que não foi conferida em fonte oficial vai marcada
    "não conferido".

## Restrições
- `fasn98/DroneSimulator`: só leitura. Reaproveita-se o método, nunca os números. Citar só como "método reaproveitado
  de projeto anterior".
- Desenvolvimento permitido em qualquer ambiente (notebook, Claude Code na web, Claude Code no Replit), sempre com
  branch, hook, revisão independente e PR. Proibido: Replit Agent e commits diretos na main.
- Dependências Python: só no `pyproject.toml` (ADR 0010). `environment.yml` e o Replit instalam o pacote.

## Comandos
```bash
conda env create -f environment.yml && conda activate marsmission
git config core.hooksPath .githooks
python tools/fetch_kernels.py                      # kernels SPICE, com conferência do MD5
python -m pytest                                   # suíte
python tools/confere_regeneracao.py <rótulo> --ci  # regenera results/ e compara (rodar num worktree)
python -m streamlit run src/painel/app.py          # painel
```
