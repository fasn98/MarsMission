# Mapa de dependências da regeneração (gerado por tools/mapa_regeneracao.py)

Observação de ambiente (2026-11-14, x86_64): tempos desta máquina. Total em série 163 min; caminho crítico 110 min.

Caminho crítico: `tools/missoes.py` → `tools/varredura_encontro.py` → `tools/mav_propulsao.py` → `tools/redimensiona.py` → `tools/plataformas.py` → `tools/queima_finita.py` → `tools/bocais_estagio1.py` → `tools/rotas_mav.py` → `tools/missao_familia1.py` → `tools/mav_familia1.py` → `tools/ruido_subida.py` → `tools/inerte_solido.py` → `tools/opcoes_arquitetura.py`

| # | Ferramenta | Tempo (s) | Depende de (#) |
| -: | :- | -: | :- |
| 0 | `tools/baricentro_marte.py` | 2 | — |
| 1 | `tools/porkchop.py terra_marte` | 24 | — |
| 2 | `tools/porkchop.py marte_terra` | 43 | — |
| 3 | `tools/verifica_burke2010.py` | 25 | — |
| 4 | `tools/verifica_jpl8243.py` | 156 | — |
| 5 | `tools/efeito_efemeride.py` | 0 | — |
| 6 | `tools/missoes.py` | 114 | — |
| 7 | `tools/compara_dra5.py` | 0 | 6 |
| 8 | `tools/grafico_missoes.py` | 1 | 6 |
| 9 | `tools/lista_premissas.py` | 0 | — |
| 10 | `tools/dimensionamento.py` | 10 | 6 |
| 11 | `tools/compara_msr.py` | 1 | 10 |
| 12 | `tools/superficie.py` | 2 | 6 |
| 13 | `tools/varredura_encontro.py` | 34 | 6 |
| 14 | `tools/isru.py` | 0 | 6, 13 |
| 15 | `tools/mav_propulsao.py` | 17 | 6, 13 |
| 16 | `tools/redimensiona.py` | 1095 | 6, 15 |
| 17 | `tools/plataformas.py` | 247 | 6, 15, 16 |
| 18 | `tools/lancamento.py` | 33 | 6, 15, 16, 17 |
| 19 | `tools/coleta.py` | 7 | 6, 15, 16, 17 |
| 20 | `tools/arquitetura.py` | 12 | 6, 15, 16, 17 |
| 21 | `tools/confere_2033.py` | 52 | 12, 13, 14, 15 |
| 22 | `tools/exporta_painel.py` | 45 | — |
| 23 | `tools/queima_finita.py` | 170 | 6, 15, 16, 17 |
| 24 | `tools/baixo_empuxo.py` | 35 | 17 |
| 25 | `tools/geometria_marte.py` | 0 | 6 |
| 26 | `tools/orbitador_eletrico.py` | 116 | 6, 15, 16, 17, 20 |
| 27 | `tools/energia.py` | 55 | 6, 15, 16, 17 |
| 28 | `tools/termico.py` | 0 | 6, 15, 27 |
| 29 | `tools/comunicacao.py` | 8 | 6, 15, 16, 17, 27 |
| 30 | `tools/operacao_superficie.py` | 2 | 6, 15, 16, 17, 27, 29 |
| 31 | `tools/lista_massas_lander.py` | 9 | 6, 15, 16, 17, 20, 27, 28, 29 |
| 32 | `tools/fase4.py` | 1 | 6, 15, 16, 17, 20, 27, 28, 29, 30, 31 |
| 33 | `tools/envelope_arranjo.py` | 3 | 20, 27 |
| 34 | `tools/cad_parametros.py` | 2 | 20, 33 |
| 35 | `tools/encaixe_coifas.py` | 7 | 20, 33, 34 |
| 36 | `tools/mav_arranjo.py` | 1 | 20 |
| 37 | `tools/conferencia_onshape.py` | 1 | 34 |
| 38 | `tools/cg_lateral.py` | 1 | 34 |
| 39 | `tools/portao_7_2.py` | 1 | 20, 33, 34, 36 |
| 40 | `tools/bocais_estagio1.py` | 1 | 20, 23, 36, 39 |
| 41 | `tools/comprimento_mav.py` | 57 | 6, 15, 16, 17, 20, 23, 36 |
| 42 | `tools/rotas_mav.py` | 14 | 6, 15, 16, 17, 20, 23, 26, 29, 30, 34, 36, 40 |
| 43 | `tools/isp_44_bocal.py` | 1 | — |
| 44 | `tools/rota_a_dimensiona.py` | 137 | 6, 15, 16, 17, 20, 23, 33, 34, 36, 42, 43 |
| 45 | `tools/subida_mav.py` | 1302 | 6, 15, 16, 17, 20, 33, 34, 36, 43 |
| 46 | `tools/comprimento_solido.py` | 2 | — |
| 47 | `tools/mav_solido.py` | 4 | 6, 15, 16, 17, 20, 33, 34, 36, 46 |
| 48 | `tools/missao_familia1.py` | 5 | 2, 42 |
| 49 | `tools/mav_familia1.py` | 1387 | 6, 15, 16, 17, 20, 33, 34, 36, 46, 48 |
| 50 | `tools/ruido_subida.py` | 1541 | 49 |
| 51 | `tools/familia1_465.py` | 1016 | 6, 15, 16, 17, 20, 33, 34, 36, 42, 46, 49 |
| 52 | `tools/inerte_solido.py` | 1957 | 42, 46, 49, 50, 51 |
| 53 | `tools/opcoes_arquitetura.py` | 3 | 20, 35, 40, 42, 44, 45, 47, 52 |
