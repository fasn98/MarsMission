# Comparação de ordem de grandeza com o MSR (gerado por tools/compara_msr.py)

**Comparação de ordem de grandeza, não verificação.** O ERO volta com propulsão elétrica (Isp 4000 s) e tem plataforma completa (energia, aviônica, comunicação, térmica). Este estudo usa propulsão química e **não modela a plataforma do orbitador**: a carga útil é só captura + cápsula (CU-2) e a fração estrutural cobre só os módulos propulsivos. Massas em kg.

| Grandeza | ERO (MSR) | missao_A | i_sistema_unico | ii_estagios_pior_trecho | iii_marte_pior_terra_ref |
| :- | -: | -: | -: | -: | -: |
| Massa a caminho de Marte (ERO: massa úmida no lançamento; aqui: depois da injeção trans-Marte) | 6 500 | 2 036 | 3 409 | 3 420 | 3 420 |
| Módulo de inserção em Marte (seco + propelente) | 2 500 | 882 | — | 1 767 | 1 767 |
| Massa na órbita baixa da Terra (inclui o estágio de saída da Terra; o ERO seria lançado num Ariane 64 [F32], sem esse estágio) | — | 6 180 | 10 352 | 10 629 | 10 381 |
