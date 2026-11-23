# Mapa de dependências da regeneração (gerado por tools/mapa_regeneracao.py)

Observação de ambiente (2026-11-23, x86_64): tempos desta máquina. Total em série 1090 min; caminho crítico 353 min.

Caminho crítico: `tools/missoes.py` → `tools/varredura_encontro.py` → `tools/mav_propulsao.py` → `tools/redimensiona.py` → `tools/plataformas.py` → `tools/queima_finita.py` → `tools/bocais_estagio1.py` → `tools/rotas_mav.py` → `tools/missao_familia1.py` → `tools/orbitador_so_eletrico.py --bloco XIPS-25 (87 kg) 380 12-7` → `tools/orbitador_so_eletrico.py --bloco XIPS-25 (87 kg) 380 6-1` → `tools/orbitador_so_eletrico.py --junta`

| # | Ferramenta | Tempo (s) | Depende de (#) |
| -: | :- | -: | :- |
| 0 | `tools/baricentro_marte.py` | 0 | — |
| 1 | `tools/porkchop.py terra_marte` | 18 | — |
| 2 | `tools/porkchop.py marte_terra` | 40 | — |
| 3 | `tools/verifica_burke2010.py` | 23 | — |
| 4 | `tools/verifica_jpl8243.py` | 146 | — |
| 5 | `tools/efeito_efemeride.py` | 0 | — |
| 6 | `tools/missoes.py` | 105 | — |
| 7 | `tools/compara_dra5.py` | 0 | 6 |
| 8 | `tools/grafico_missoes.py` | 1 | 6 |
| 9 | `tools/lista_premissas.py` | 0 | — |
| 10 | `tools/dimensionamento.py` | 9 | 6 |
| 11 | `tools/compara_msr.py` | 0 | 10 |
| 12 | `tools/superficie.py` | 1 | 6 |
| 13 | `tools/varredura_encontro.py` | 32 | 6 |
| 14 | `tools/isru.py` | 0 | 6, 13 |
| 15 | `tools/mav_propulsao.py` | 17 | 6, 13 |
| 16 | `tools/redimensiona.py` | 1169 | 6, 15 |
| 17 | `tools/plataformas.py` | 252 | 6, 15, 16 |
| 18 | `tools/lancamento.py` | 31 | 6, 15, 16, 17 |
| 19 | `tools/coleta.py` | 5 | 6, 15, 16, 17 |
| 20 | `tools/arquitetura.py` | 11 | 6, 15, 16, 17 |
| 21 | `tools/confere_2033.py` | 52 | 12, 13, 14, 15 |
| 22 | `tools/exporta_painel.py` | 42 | — |
| 23 | `tools/queima_finita.py` | 176 | 6, 15, 16, 17 |
| 24 | `tools/baixo_empuxo.py` | 34 | 17 |
| 25 | `tools/geometria_marte.py` | 0 | 6 |
| 26 | `tools/orbitador_eletrico.py` | 121 | 6, 15, 16, 17, 20 |
| 27 | `tools/energia.py` | 55 | 6, 15, 16, 17 |
| 28 | `tools/termico.py` | 0 | 6, 15, 27 |
| 29 | `tools/comunicacao.py` | 8 | 6, 15, 16, 17, 27 |
| 30 | `tools/operacao_superficie.py` | 2 | 6, 15, 16, 17, 27, 29 |
| 31 | `tools/lista_massas_lander.py` | 8 | 6, 15, 16, 17, 20, 27, 28, 29 |
| 32 | `tools/fase4.py` | 1 | 6, 15, 16, 17, 20, 27, 28, 29, 30, 31 |
| 33 | `tools/envelope_arranjo.py` | 1 | 20, 27 |
| 34 | `tools/cad_parametros.py` | 1 | 20, 33 |
| 35 | `tools/encaixe_coifas.py` | 6 | 20, 33, 34 |
| 36 | `tools/mav_arranjo.py` | 1 | 20 |
| 37 | `tools/conferencia_onshape.py` | 1 | 34 |
| 38 | `tools/cg_lateral.py` | 1 | 34 |
| 39 | `tools/portao_7_2.py` | 1 | 20, 33, 34, 36 |
| 40 | `tools/bocais_estagio1.py` | 1 | 20, 23, 36, 39 |
| 41 | `tools/comprimento_mav.py` | 58 | 6, 15, 16, 17, 20, 23, 36 |
| 42 | `tools/rotas_mav.py` | 14 | 6, 15, 16, 17, 20, 23, 26, 29, 30, 34, 36, 40 |
| 43 | `tools/isp_44_bocal.py` | 1 | — |
| 44 | `tools/rota_a_dimensiona.py` | 143 | 6, 15, 16, 17, 20, 23, 33, 34, 36, 42, 43 |
| 45 | `tools/subida_mav.py` | 1547 | 6, 15, 16, 17, 20, 33, 34, 36, 43 |
| 46 | `tools/comprimento_solido.py` | 0 | — |
| 47 | `tools/mav_solido.py` | 2 | 6, 15, 16, 17, 20, 33, 34, 36, 46 |
| 48 | `tools/missao_familia1.py` | 6 | 2, 42 |
| 49 | `tools/mav_familia1.py` | 1645 | 6, 15, 16, 17, 20, 33, 34, 36, 46, 48 |
| 50 | `tools/ruido_subida.py` | 1327 | 49 |
| 51 | `tools/familia1_465.py` | 1023 | 6, 15, 16, 17, 20, 33, 34, 36, 42, 46, 49 |
| 52 | `tools/inerte_solido.py` | 2047 | 42, 46, 49, 50, 51 |
| 53 | `tools/orbitador_so_eletrico.py --caso-publicado` | 1121 | — |
| 54 | `tools/orbitador_so_eletrico.py --bloco XIPS-25 380 12-7` | 4068 | 6, 16, 23, 42, 48 |
| 55 | `tools/orbitador_so_eletrico.py --bloco XIPS-25 380 6-1` | 5668 | 6, 16, 23, 42, 48, 54 |
| 56 | `tools/orbitador_so_eletrico.py --bloco XIPS-25 (87 kg) 380 12-7` | 12087 | 6, 16, 23, 42, 48 |
| 57 | `tools/orbitador_so_eletrico.py --bloco XIPS-25 (87 kg) 380 6-1` | 7323 | 6, 16, 23, 42, 48, 56 |
| 58 | `tools/orbitador_so_eletrico.py --bloco NEXT-C 380 7-1` | 4363 | 6, 16, 23, 42, 48 |
| 59 | `tools/orbitador_so_eletrico.py --bloco XIPS-25 814 12-7` | 4516 | 6, 16, 23, 42, 48 |
| 60 | `tools/orbitador_so_eletrico.py --bloco XIPS-25 814 6-1` | 2656 | 6, 16, 23, 42, 48, 59 |
| 61 | `tools/orbitador_so_eletrico.py --bloco XIPS-25 (87 kg) 814 12-7` | 3068 | 6, 16, 23, 42, 48 |
| 62 | `tools/orbitador_so_eletrico.py --bloco XIPS-25 (87 kg) 814 6-1` | 3580 | 6, 16, 23, 42, 48, 61 |
| 63 | `tools/orbitador_so_eletrico.py --bloco NEXT-C 814 7-1` | 6710 | 6, 16, 23, 42, 48 |
| 64 | `tools/orbitador_so_eletrico.py --junta` | 25 | 42, 48, 49, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63 |
| 65 | `tools/opcoes_arquitetura.py` | 0 | 20, 35, 40, 42, 44, 45, 47, 52 |
