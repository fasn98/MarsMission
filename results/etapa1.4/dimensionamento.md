# Dimensionamento por estágios (gerado por tools/dimensionamento.py)

Carga útil CU-2, margem de Δv 10 %, acréscimo na cápsula 0 %. Massas em kg. Só trechos no espaço (descida, pouso e subida: Fase 2).

## missao_A: missão A em todos os estágios

| Estágio | Propelente | Inerte | Massa inicial (com o que carrega) |
| :- | -: | -: | -: |
| saida_terra | 3 741 | 403 | 6 180 |
| insercao_marte | 670 | 212 | 2 036 |
| retorno | 338 | 107 | 1 154 |
| **Massa na órbita baixa da Terra** | | | **6 180** |

## i_sistema_unico: (i) saída da Terra com estágio próprio + um só estágio para captura e retorno; cada janela com a sua missão, projeto pela pior janela (janela que define: 2033)

| Estágio | Propelente | Inerte | Massa inicial (com o que carrega) |
| :- | -: | -: | -: |
| saida_terra | 6 268 | 675 | 10 352 |
| marte_unico | 2 052 | 648 | 3 409 |
| **Massa na órbita baixa da Terra** | | | **10 352** |

## ii_estagios_pior_trecho: (ii) cada estágio pelo pior caso do seu trecho

| Estágio | Propelente | Inerte | Massa inicial (com o que carrega) |
| :- | -: | -: | -: |
| saida_terra | 6 508 | 701 | 10 629 |
| insercao_marte | 1 343 | 424 | 3 420 |
| retorno | 717 | 226 | 1 653 |
| **Massa na órbita baixa da Terra** | | | **10 629** |

## iii_marte_pior_terra_ref: (iii) estágios de Marte pelo pior caso; saída da Terra pela janela de referência (A)

| Estágio | Propelente | Inerte | Massa inicial (com o que carrega) |
| :- | -: | -: | -: |
| saida_terra | 6 285 | 677 | 10 381 |
| insercao_marte | 1 343 | 424 | 3 420 |
| retorno | 717 | 226 | 1 653 |
| **Massa na órbita baixa da Terra** | | | **10 381** |

## Sensibilidade da massa na órbita baixa (kg)

Cada linha muda um parâmetro e mantém os demais no caso base.

| Parâmetro | Valor | missao_A | i_sistema_unico | ii_estagios_pior_trecho | iii_marte_pior_terra_ref |
| :- | :- | -: | -: | -: | -: |
| Carga útil | CU-1 | 6 292 | 10 258 | 10 264 | 10 025 |
| Carga útil | CU-2 | 6 180 | 10 352 | 10 629 | 10 381 |
| Carga útil | CU-2b | 5 396 | 9 038 | 9 280 | 9 064 |
| Carga útil | CU-3 | 799 | 1 332 | 1 368 | 1 336 |
| Margem de Δv | 0 % | 4 990 | 7 596 | 8 070 | 7 904 |
| Margem de Δv | 5 % | 5 550 | 8 839 | 9 252 | 9 049 |
| Margem de Δv | 10 % | 6 180 | 10 352 | 10 629 | 10 381 |
| Margem de Δv | 20 % | 7 692 | 14 541 | 14 124 | 13 755 |
| Acréscimo na massa da cápsula | 0 % | 6 180 | 10 352 | 10 629 | 10 381 |
| Acréscimo na massa da cápsula | 15 % | 6 296 | 10 546 | 10 828 | 10 576 |
| Acréscimo na massa da cápsula | 30 % | 6 413 | 10 740 | 11 028 | 10 771 |
| Acréscimo na massa da cápsula | 50 % | 6 568 | 10 999 | 11 293 | 11 030 |
| Isp de todos os estágios | -5 % | 7 010 | 12 548 | 12 516 | 12 204 |
| Isp de todos os estágios | +5 % | 5 521 | 8 774 | 9 191 | 8 990 |
| Frações estruturais × fator | 0,50 | 4 671 | 6 171 | 7 089 | 6 947 |
| Frações estruturais × fator | 1,50 | 9 243 | 41 008 | 20 129 | 19 569 |
