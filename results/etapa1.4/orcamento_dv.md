# Orçamento de Δv por trecho (gerado por tools/dimensionamento.py)

Δv em km/s: ideal (Etapa 1.3) + perdas gravitacionais + parcelas fixas. Margem de 10 % aplicada a todos os trechos (P-014, NÃO VALIDADA). Colunas: missão A e o mínimo admissível de cada janela (ADR 0004). Penúltima coluna: pior caso de cada trecho entre as janelas. Última: Δv de projeto pela regra `iii_marte_pior_terra_ref` (ADR 0004).

| Trecho | A | jan. 2028 | jan. 2031 | jan. 2033 | jan. 2035 | Pior caso do trecho | Projeto (regra de projeto) |
| :- | -: | -: | -: | -: | -: | -: | -: |
| saida_terra | 3,735 | 3,735 | 3,806 | 3,735 | 3,794 | 3,806 | 3,735 |
| correcoes_ida | 0,065 | 0,065 | 0,065 | 0,065 | 0,065 | 0,065 | 0,065 |
| captura_marte | 1,077 | 1,077 | 1,362 | 1,266 | 0,904 | 1,362 | 1,362 |
| encontro_e_manutencao_marte | 0,145 | 0,145 | 0,145 | 0,145 | 0,145 | 0,145 | 0,145 |
| saida_marte | 0,764 | 0,764 | 0,790 | 1,065 | 1,389 | 1,389 | 1,389 |
| correcoes_volta | 0,065 | 0,065 | 0,065 | 0,065 | 0,065 | 0,065 | 0,065 |
| desvio_orbitador | 0,019 | 0,019 | 0,024 | 0,031 | 0,027 | 0,031 | 0,031 |
| **Total sem margem** | **5,869** | **5,869** | **6,257** | **6,372** | **6,389** | **6,862** | **6,791** |
| **Total com margem** | **6,456** | **6,456** | **6,882** | **7,009** | **7,028** | **7,549** | **7,471** |
