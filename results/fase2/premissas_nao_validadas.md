# Premissas NÃO VALIDADAS ao fim da Fase 2 (gerado por tools/lista_premissas.py)

Só o Fabio altera o status. Justificativas completas em config/premissas.yaml.

| Id | Nome | Valor | Unidade | Uso |
| :- | :- | :- | :- | :- |
| P-001 | tolerancia_efemeride_vs_horizons_km | 1.0 | km | tests/test_ephemeris.py — tolerância de posição entre DE440 (local) e Horizons (DE441) |
| P-002 | tolerancia_velocidade_vs_horizons_km_s | 1e-06 | km/s | tests/test_ephemeris.py — tolerância de velocidade entre DE440 (local) e Horizons (DE441) |
| P-003 | tolerancia_lambert_vs_kepler_rel | 1e-10 | adimensional (erro relativo de posição e velocidade) | tests/test_lambert.py — solução de Lambert propagada por Kepler analítico (variável universal) |
| P-004 | tolerancia_kepler_vs_integrador_rel | 1e-08 | adimensional (erro relativo de posição) | tests/test_kepler.py — propagação analítica comparada com integração numérica (DOP853, rtol 1e-13) |
| P-005 | tolerancia_lambert_vs_referencia_km_s | 1e-08 | km/s (maior diferença por componente) | tests/test_lambert.py — comparação com os testes oficiais do valladopy |
| P-006 | exclusao_angulo_180_graus | 1.0 | graus | tools/porkchop.py e tools/verifica_burke2010.py — busca do mínimo de C3 por tipo |
| P-007 | tolerancia_burke2010_rel | 0.002 | adimensional (erro relativo de C3 e de v∞ de chegada) | tests/test_porkchop.py — C3 e v∞ nas datas impressas em NASA/TM-2010-216764, janelas 2028–2033 |
| P-008 | tolerancia_jpl8243_rel | 0.002 | adimensional (erro relativo de C3L e de VHP) | tests/test_retorno.py — C3L e VHP nas datas impressas no JPL 82-43 Parte 5, 1992–2007 |
| P-009 | conjuncao_permanencia_busca_dias | [400, 700] | dias | config/missoes.yaml, classes conjuncao e conjuncao_transito_curto (faixa de busca) |
| P-010 | aerocaptura_periapse_altitude_km | 50 | km | config/parametros_orbitais.yaml — periapse da passagem atmosférica em Marte |
| P-011 | reentrada_max_km_s | 12.9 | km/s (velocidade inercial na interface de reentrada) | config/parametros_orbitais.yaml — limite na busca de missões (tools/missoes.py) |
| P-012 | acrescimo_massa_capsula_faixa | [0.0, 0.15, 0.3, 0.5] | fração da massa da cápsula com amostras (89,9 kg na CU-2) | config/dimensionamento.yaml — sensibilidade da massa na órbita baixa |
| P-013 | desvio_orbitador_parametros | periapse_seguro_alt_km: 300; antecedencia_dias: 1 | km; dias | config/dimensionamento.yaml — Δv de desvio do orbitador após soltar a cápsula (plano B) |
| P-014 | margem_dv | 0.1 | fração, aplicada a todos os trechos | config/dimensionamento.yaml |
| P-015 | perdas_gravitacionais_do_dra | saida_terra: 0.148; captura_marte: 0.018; saida_marte: 0.011 | km/s | config/dimensionamento.yaml |
| P-016 | plataforma_orbitador_kg | 496.5 | kg (massa seca prevista da plataforma, sem módulos propulsivos e sem carga útil) | config/dimensionamento.yaml |
| P-017 | plataforma_superficie_kg | 1564.875 | kg (massa pousada sem o MAV e sem o bloco de aquecimento do MAV) | config/superficie.yaml — massa pousada = MAV + plataforma de superfície |
| P-018 | razao_massa_pousada_entrada | entrada_direta: 0.509; a_partir_de_orbita: 0.624 | adimensional (massa pousada / massa de entrada) | config/superficie.yaml — massa do sistema de entrada, descida e pouso |
| P-019 | mav_estagios | fracao_estrutural: 0.286; fracao_dv_estagio_1: 0.481 | adimensional | config/superficie.yaml — dimensionamento do MAV sólido de dois estágios |
| P-020 | aerofrenagem_orbitador | dv_saida_km_s: 0.09; duracao_dias: 205 | km/s; dias | config/superficie.yaml — arquitetura S4 |
| P-021 | mav_loxch4_fracao_estrutural | 0.295 | adimensional (por estágio, MAV de dois estágios) | config/mav_propulsao.yaml (O2) e config/isru.yaml (Etapa 2.2) |
| P-022 | escala_planta_moxie | expoente_massa: 1.0; expoente_potencia: 1.0 | adimensional | config/isru.yaml — planta de O2 da opção O3 |
| P-023 | escala_liquefacao_o2 | 1.0 | adimensional | config/isru.yaml — liquefação de O2 (O3) |
| P-024 | escala_armazenamento_zbo | 0.6667 | adimensional (expoente sobre a massa armazenada) | config/isru.yaml — armazenamento sem evaporação na superfície (O2 e O3) |
| P-025 | escala_energia_solar | 1.0 | adimensional | config/isru.yaml — massa de painéis solares |
| P-026 | armazenamento_cruzeiro | referencia_kg: 6567; expoente: 0.6667 | kg; adimensional | config/mav_propulsao.yaml — armazenamento sem evaporação de LOX e CH4 no cruzeiro (O2) |
| P-027 | aquecimento_mav_superficie | expoente_area: 0.6667; margem_congelamento_k: 10 | adimensional; K | config/mav_propulsao.yaml — aquecimento do MAV sólido (O1) e hipergólico (O4) durante a estada |
| P-028 | carga_eletrica_orbitador_w | 510 | W (mesma carga no sol e no eclipse) | config/plataformas.yaml — painel e bateria do orbitador |
| P-029 | eficiencia_recarga_bateria | 0.8 | adimensional (energia devolvida / energia de recarga) | config/plataformas.yaml — potência do painel do orbitador |
| P-030 | fator_perdas_painel_orbitador | 0.774 | adimensional (multiplica a potência específica a 1 UA escalada por 1/d²) | config/plataformas.yaml — massa do painel do orbitador |
| P-031 | base_do_cabeamento_orbitador | plataforma | — | config/plataformas.yaml — cabeamento = 5 % da massa seca nominal [F71] |
| P-032 | energia_lander | energia_por_sol_wh: 3500; fracao_noite: 0.5 | Wh/sol; adimensional | config/plataformas.yaml — painel e bateria do lander |
| P-033 | margem_crescimento_e1_ponto_medio | ponto médio da faixa E1 do AIAA S-120A | — | config/plataformas.yaml — margem por subsistema |
| P-034 | sistema_de_amostras_lander | 59 | kg | config/plataformas.yaml — coleta e transferência de amostras na base do lander (L3 + amostras, alocação provisória) e nos limites L1/L2. Atualização (Etapa 2.5, ADR 0009): deixa de ser provisória; é o braço de coleta de reserva (regolito do sítio) |
| P-035 | escala_nucleo_lander | limite_inferior: L1; limite_superior: SRL 2024 − MAV; referencia: L2; base: L3 + braço + helicópteros (Etapa 2.5) | — | config/plataformas.yaml — estrutura, pernas, térmico, comando e dados, GNC, propulsão de descida seca e cabeamento do lander |
| P-036 | multiplicador_dla | dla_graus: [28.5, 40, 50, 60]; fator: [1.0, 0.95, 0.9, 0.65] | adimensional (multiplica a massa entregue pelo lançador na injeção direta) | config/lancadores.yaml — injeção direta com |DLA| > 28,5° a partir do Cabo |
| P-037 | saida_propria_fora_do_plano | orbita_baixa_km: 407; inclinacoes_com_dado_graus: [28.5, 51.6] | km; graus | tools/lancamento.py — opção (b), órbita baixa + estágio criogênico próprio |
| P-038 | categoria_de_margem_dos_helicopteros | eletronica_0_5kg | categoria do AIAA S-120A (E1; 20–35 %, ponto médio 27,5 %) | config/plataformas.yaml — helicópteros de recuperação no lander (ADR 0009) |
| P-039 | tolerancia_regeneracao_numerica | relativa: 1e-09; piso_absoluto: 1e-10 | adimensional (passa se |a − b| ≤ max(relativa · |b|, piso_absoluto); a = versionado, b = regenerado) | tools/confere_regeneracao.py — números em YAML, Markdown e NPZ de results/ regenerados contra os versionados |
| P-040 | tolerancia_regeneracao_png | 0.001 | fração de pixels diferentes por figura | tools/confere_regeneracao.py — figuras PNG de results/ regeneradas contra as versionadas |

Total: 40 de 40 premissas com status NÃO VALIDADA.
