# Premissas NÃO VALIDADAS ao fim da Fase 3 (gerado por tools/lista_premissas.py)

Só o Fabio altera o status. Justificativas completas em config/premissas.yaml. "Fase 3" marca as criadas nela.

| Id | Nome | Valor | Unidade | Uso | Fase 3 |
| :- | :- | :- | :- | :- | :- |
| P-001 | tolerancia_efemeride_vs_horizons_km | 1.0 | km | tests/test_ephemeris.py — tolerância de posição entre DE440 (local) e Horizons (DE441) |  |
| P-002 | tolerancia_velocidade_vs_horizons_km_s | 1e-06 | km/s | tests/test_ephemeris.py — tolerância de velocidade entre DE440 (local) e Horizons (DE441) |  |
| P-003 | tolerancia_lambert_vs_kepler_rel | 1e-10 | adimensional (erro relativo de posição e velocidade) | tests/test_lambert.py — solução de Lambert propagada por Kepler analítico (variável universal) |  |
| P-004 | tolerancia_kepler_vs_integrador_rel | 1e-08 | adimensional (erro relativo de posição) | tests/test_kepler.py — propagação analítica comparada com integração numérica (DOP853, rtol 1e-13) |  |
| P-005 | tolerancia_lambert_vs_referencia_km_s | 1e-08 | km/s (maior diferença por componente) | tests/test_lambert.py — comparação com os testes oficiais do valladopy |  |
| P-006 | exclusao_angulo_180_graus | 1.0 | graus | tools/porkchop.py e tools/verifica_burke2010.py — busca do mínimo de C3 por tipo |  |
| P-007 | tolerancia_burke2010_rel | 0.002 | adimensional (erro relativo de C3 e de v∞ de chegada) | tests/test_porkchop.py — C3 e v∞ nas datas impressas em NASA/TM-2010-216764, janelas 2028–2033 |  |
| P-008 | tolerancia_jpl8243_rel | 0.002 | adimensional (erro relativo de C3L e de VHP) | tests/test_retorno.py — C3L e VHP nas datas impressas no JPL 82-43 Parte 5, 1992–2007 |  |
| P-009 | conjuncao_permanencia_busca_dias | [400, 700] | dias | config/missoes.yaml, classes conjuncao e conjuncao_transito_curto (faixa de busca) |  |
| P-010 | aerocaptura_periapse_altitude_km | 50 | km | config/parametros_orbitais.yaml — periapse da passagem atmosférica em Marte |  |
| P-011 | reentrada_max_km_s | 12.9 | km/s (velocidade inercial na interface de reentrada) | config/parametros_orbitais.yaml — limite na busca de missões (tools/missoes.py) |  |
| P-012 | acrescimo_massa_capsula_faixa | [0.0, 0.15, 0.3, 0.5] | fração da massa da cápsula com amostras (89,9 kg na CU-2) | config/dimensionamento.yaml — sensibilidade da massa na órbita baixa |  |
| P-013 | desvio_orbitador_parametros | periapse_seguro_alt_km: 300; antecedencia_dias: 1 | km; dias | config/dimensionamento.yaml — Δv de desvio do orbitador após soltar a cápsula (plano B) |  |
| P-014 | margem_dv | 0.1 | fração, aplicada a todos os trechos | config/dimensionamento.yaml |  |
| P-015 | perdas_gravitacionais_do_dra | saida_terra: 0.148; captura_marte: 0.018; saida_marte: 0.011 | km/s | config/dimensionamento.yaml |  |
| P-016 | plataforma_orbitador_kg | 614.0 | kg (massa seca prevista da plataforma, sem módulos propulsivos e sem carga útil) | config/dimensionamento.yaml |  |
| P-017 | plataforma_superficie_kg | 1564.875 | kg (massa pousada sem o MAV e sem o bloco de aquecimento do MAV) | config/superficie.yaml — massa pousada = MAV + plataforma de superfície |  |
| P-018 | razao_massa_pousada_entrada | entrada_direta: 0.509; a_partir_de_orbita: 0.624 | adimensional (massa pousada / massa de entrada) | config/superficie.yaml — massa do sistema de entrada, descida e pouso |  |
| P-019 | mav_estagios | fracao_estrutural: 0.286; fracao_dv_estagio_1: 0.481 | adimensional | config/superficie.yaml — dimensionamento do MAV sólido de dois estágios |  |
| P-020 | aerofrenagem_orbitador | dv_saida_km_s: 0.09; duracao_dias: 205 | km/s; dias | config/superficie.yaml — arquitetura S4 |  |
| P-021 | mav_loxch4_fracao_estrutural | 0.295 | adimensional (por estágio, MAV de dois estágios) | config/mav_propulsao.yaml (O2) e config/isru.yaml (Etapa 2.2) |  |
| P-022 | escala_planta_moxie | expoente_massa: 1.0; expoente_potencia: 1.0 | adimensional | config/isru.yaml — planta de O2 da opção O3 |  |
| P-023 | escala_liquefacao_o2 | 1.0 | adimensional | config/isru.yaml — liquefação de O2 (O3) |  |
| P-024 | escala_armazenamento_zbo | 0.6667 | adimensional (expoente sobre a massa armazenada) | config/isru.yaml — armazenamento sem evaporação na superfície (O2 e O3) |  |
| P-025 | escala_energia_solar | 1.0 | adimensional | config/isru.yaml — massa de painéis solares |  |
| P-026 | armazenamento_cruzeiro | referencia_kg: 6567; expoente: 0.6667 | kg; adimensional | config/mav_propulsao.yaml — armazenamento sem evaporação de LOX e CH4 no cruzeiro (O2) |  |
| P-027 | aquecimento_mav_superficie | expoente_area: 0.6667; alvo_o4_c: 15 | adimensional; °C | config/mav_propulsao.yaml — aquecimento do MAV sólido (O1) e hipergólico (O4) durante a estada |  |
| P-028 | carga_eletrica_orbitador_w | 1022 | W (mesma carga no sol e no eclipse) | config/plataformas.yaml — painel e bateria do orbitador |  |
| P-029 | eficiencia_recarga_bateria | 0.8 | adimensional (energia devolvida / energia de recarga) | config/plataformas.yaml — potência do painel do orbitador |  |
| P-030 | fator_perdas_painel_orbitador | 0.774 | adimensional (multiplica a potência específica a 1 UA escalada por 1/d²) | config/plataformas.yaml — massa do painel do orbitador |  |
| P-031 | base_do_cabeamento_orbitador | plataforma | — | config/plataformas.yaml — cabeamento = 5 % da massa seca nominal [F71] |  |
| P-032 | energia_lander | energia_por_sol_wh: 3500; fracao_noite: 0.5 | Wh/sol; adimensional | config/plataformas.yaml — painel e bateria do lander |  |
| P-033 | margem_crescimento_e1_ponto_medio | ponto médio da faixa E1 do AIAA S-120A | — | config/plataformas.yaml — margem por subsistema |  |
| P-034 | sistema_de_amostras_lander | 59 | kg | config/plataformas.yaml — coleta e transferência de amostras na base do lander (L3 + amostras, alocação provisória) e nos limites L1/L2. Atualização (Etapa 2.5, ADR 0009): deixa de ser provisória; é o braço de coleta de reserva (regolito do sítio) |  |
| P-035 | escala_nucleo_lander | limite_inferior: L1; limite_superior: SRL 2024 − MAV; referencia: L2; base: L3 + braço + helicópteros (Etapa 2.5) | — | config/plataformas.yaml — estrutura, pernas, térmico, comando e dados, GNC, propulsão de descida seca e cabeamento do lander |  |
| P-036 | multiplicador_dla | dla_graus: [28.5, 40, 50, 60]; fator: [1.0, 0.95, 0.9, 0.65] | adimensional (multiplica a massa entregue pelo lançador na injeção direta) | config/lancadores.yaml — injeção direta com |DLA| > 28,5° a partir do Cabo |  |
| P-037 | saida_propria_fora_do_plano | orbita_baixa_km: 407; inclinacoes_com_dado_graus: [28.5, 51.6] | km; graus | tools/lancamento.py — opção (b), órbita baixa + estágio criogênico próprio |  |
| P-038 | categoria_de_margem_dos_helicopteros | eletronica_0_5kg | categoria do AIAA S-120A (E1; 20–35 %, ponto médio 27,5 %) | config/plataformas.yaml — helicópteros de recuperação no lander (ADR 0009) |  |
| P-039 | tolerancia_regeneracao_numerica | relativa: 1e-09; piso_absoluto: 1e-10 | adimensional (passa se |a − b| ≤ max(relativa · |b|, piso_absoluto); a = versionado, b = regenerado) | tools/confere_regeneracao.py — números em YAML, Markdown e NPZ de results/ regenerados contra os versionados |  |
| P-040 | tolerancia_regeneracao_png | 0.001 | fração de pixels diferentes por figura | tools/confere_regeneracao.py — figuras PNG de results/ regeneradas contra as versionadas |  |
| P-041 | parametros_numericos_queima_finita | rtol: 1e-11; atol_km: 1e-09; tolerancia_alvo: 1e-06; passo_continuacao: 2.0; duracao_inicial_continuacao_s: 60; demais: ver config/queima_finita.yaml | adimensional; km e km/s; s | config/queima_finita.yaml (orbital.queima_finita e tools/queima_finita.py, Etapa 3.1) | sim |
| P-042 | divisao_captura_saida_varias_queimas | numero_de_queimas: 1, 2, 3, 4; fracao_raio_hill: 0.1; sensibilidade: 0,05 e 1/3 | adimensional | config/queima_finita.yaml (orbital.queima_multipla, Etapa 3.1) | sim |
| P-043 | hipoteses_conferencia_ero | massa_na_captura: 6500 kg [F22] ou 7200 kg [F29]; propelente_da_captura: todo o do OIM, 1900 kg [F22]; motor: 2 x 400 N [F29] como 2 x S400-15; periapse: o da órbita de 1 sol; orbita_alvo: 1 sol ou órbita alta (P-042); vinf_km_s: 2,0 a 2,75 e o da missão de referência | kg; km/s | config/queima_finita.yaml (verificacao_ero; tools/queima_finita.py) | sim |
| P-044 | ponto_fixo_perdas_e_massas | tolerancia_km_s: 1e-06; max_iteracoes: 10 | km/s; adimensional | config/queima_finita.yaml (tools/redimensiona.py, Etapa 3.1) | sim |
| P-045 | mav_fracao_estrutural_ilustracao_de_risco | 0.3 | adimensional (por estágio, MAV de dois estágios) | config/mav_propulsao.yaml (O4, sensibilidade) e tools/arquitetura.py (Etapa 2.5) | sim |
| P-046 | espiral_baixo_empuxo_parametros | rtol: 1e-11; atol_relativo: 1e-12; tolerancia_verificacao_relativa: 0.0001; convergencia: ['DOP853 1e-9', 'DOP853 1e-13', 'Radau 1e-11']; eps_conferencia: [0.01, 0.001, 0.0001]; raio_terra_ua: 1.0; arredondamento: {'raio_e_excentricidade': 1e-06, 'voltas': 0.001} | adimensional; UA | config/baixo_empuxo.yaml (orbital.baixo_empuxo, tools/baixo_empuxo.py, Etapa 3.2) | sim |
| P-047 | operacao_propulsao_eletrica | reservas: 1; desligado_no_eclipse: True; alimentacao_xips_kg: 11.4 | propulsores; kg | config/eletrica.yaml (orbital.hibrido, tools/orbitador_eletrico.py, Etapa 3.3) | sim |
| P-048 | perdas_quimicas_do_hibrido | captura_marte: Etapa 3.1; saida_marte: Etapa 3.1 | km/s | tools/orbitador_eletrico.py (Etapa 3.3) | sim |
| P-049 | varredura_orbitador_eletrico | encontro_alt_km: [300, 20000, 40]; captura_alt_km: [1000, 40000, 40]; n_ativos_max: 12; c1_meio_arco_graus: 30; n_ativos_ordem_de_grandeza: [1, 4, 12]; c1_folga_apoapse: 0.01; demonstracao_tangencial_empuxo_n: 1.0; convergencia_massas_kg: 1e-09; arredondamento: {'voltas': 0.1, 'excentricidade': 0.0001, 'altitude_km': 0.1} | km; propulsores | config/eletrica.yaml (tools/orbitador_eletrico.py, Etapa 3.3) | sim |
| P-050 | modelo_energia_solar_lander | albedo: 0.1; data_primeiro_sol_insight: 2018-11-27T12:00:00; painel: horizontal; tau_constante_na_estada: True; mmrtg_anos_antes_do_lancamento_sensibilidade: 1.0; tolerancia_teste_fluxo: 0.007; tolerancia_teste_vl1: 0.07 | adimensional; data TDB | config/energia.yaml (orbital.energia, tools/energia.py, Etapa 4.1) | sim |
| P-051 | sem_limpeza_dos_paineis | False | — | config/energia.yaml (lander.limpeza) | sim |
| P-052 | helicopteros_com_energia_propria | True | — | config/energia.yaml (lander.helicopteros_energia_propria) | sim |
| P-053 | carga_do_orbitador_por_modo | cruzeiro: [445, 300, 0]; captura: [310, 0, 0]; encontro: [445, 500, 77]; retorno: [445, 500, 0] | W (plataforma, CCRS, outros) | config/energia.yaml (orbitador.modos) — PROPOSTA lado a lado com a P-028, que continua o valor-base | sim |
| P-054 | cargas_de_pico_e_base_do_mmrtg | braco_horas_por_sol: 2.0; voos_de_helicoptero_por_sol: 2; margem_do_mmrtg: painel_solar | h/sol; voos/sol; categoria E1 | config/energia.yaml (lander.picos, lander.mmrtg_margem_categoria) | sim |
| P-055 | arranjo_simetrico_de_mais_r4d11 | C4: 10; C5: 12 | motores R-4D-11 | config/motores.yaml (combinações de captura C4 e C5) | sim |
| P-056 | sobrevivencia_do_lander_pelo_spirit | expoente_escala: 0.6667; expoente_sensibilidade: 1.0 | adimensional | tools/energia.py (opção C, carga de sobrevivência na tempestade) | sim |
| P-057 | razao_de_energia_do_opportunity_em_2018 | tau_alto: 10.8; tau_referencia: 0.64 | adimensional | tools/energia.py (sobrevivência da opção C acima de τ = 6) | sim |
| P-058 | atividade_do_pu238 | massa_molar_g_mol: 238; dias_por_ano: 365.25 | g/mol; dias | tools/energia.py (atividade e enquadramento no NSPM-20 da alternativa A) | sim |
| P-059 | fator_do_opportunity_nas_tempestades | aplicado_a: cenários de tempestade (τ ≥ 2) e sobrevivência; tau_da_comparacao: 2.1 | adimensional | tools/energia.py (sensibilidade das áreas de painel) | sim |
| P-060 | tolerancia_potencia_especifica_pu238 | 0.01 | fração | tests/test_energia.py (potência específica do Pu-238 pela física contra a da MMRTG [F135]) | sim |
| P-061 | probabilidade_de_tempestade_global_na_estada | probabilidade_por_ano_marciano: 0.25 | fração | tools/energia.py (probabilidade do risco acima de τ = 6) | sim |
| P-062 | data_do_deposito_de_three_forks | 2023-02-15 | data | config/termico.yaml (tempo das amostras no depósito até a chegada) | sim |
| P-063 | demanda_de_dados_do_lander | 250 | Mbit por sol | config/comunicacao.yaml (demanda do lander contra o enlace direto e o relé) | sim |
| P-064 | escala_da_taxa_do_orbitador_com_a_distancia | expoente: 2 | adimensional | tools/comunicacao.py (taxa em banda X do orbitador) | sim |
| P-065 | passe_dte_do_lander | 8 | horas por sol | config/comunicacao.yaml (volume do enlace direto do lander) | sim |
| P-066 | enlace_uhf_do_rele_proprio | potencia_tx_w: 5; ganhos_antenas_dbi: 0; margem_db: 3 | W; dBi; dB | config/comunicacao.yaml (taxa do relé UHF lander–orbitador) | sim |
| P-067 | geometria_dos_passes_de_rele | inclinacao_graus: 30; sois_simulados: 60; passo_s: 30 | graus; sóis; s | tools/comunicacao.py (simulação dos passes do orbitador sobre Jezero) | sim |
| P-068 | volume_de_dados_dos_helicopteros | imagens_por_voo: 200; compressao: nenhuma | imagens; — | tools/comunicacao.py (demanda de dados dos helicópteros) | sim |
| P-069 | escala_do_enlace_direto_maior | ganho: ∝ D²; taxa: ∝ potência de RF; massa_refletor: densidade de área do MRO; gimbal: ∝ D² a partir do MRO | — | tools/comunicacao.py (opção (b), enlace direto maior) | sim |
| P-070 | enlace_direto_minimo_critico | horas_por_sol: 1; categoria_mga: eletronica_0_5kg; receptor: ligado o sol inteiro | h; —; — | config/comunicacao.yaml (reserva própria do lander, decisão do Fabio no portão da 4.3) | sim |
| P-071 | capacidade_do_tgo_por_passe | mbit_por_passe_min: 30; mbit_por_passe_max: 1000; passes_por_sol: 2 | Mbit; passes por sol | config/comunicacao.yaml (capacidade do caminho primário) | sim |
| P-072 | media_de_imagens_do_ingenuity_por_voo | navcam_por_voo: 13959/72; rte_por_voo: 602/72; compressao: nenhuma | imagens por voo | tools/comunicacao.py (volume dos helicópteros pela média do Ingenuity) | sim |

Total: 72 de 72 premissas com status NÃO VALIDADA; 32 criadas na Fase 3.
