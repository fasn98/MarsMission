# Dimensionamento por estágios (gerado por tools/dimensionamento.py)

Carga útil CU-2, margem de Δv 10 %, acréscimo na cápsula 0 %, plataforma do orbitador 850 kg (P-016). Massas em kg. Só trechos no espaço (descida, pouso e subida: Fase 2). Regra de projeto (ADR 0004): `iii_marte_pior_terra_ref`.

## missao_A: missão A em todos os estágios

| Estágio | Propelente | Inerte | Massa inicial (com o que carrega) |
| :- | -: | -: | -: |
| saida_terra | 8 226 | 886 | 13 587 |
| insercao_marte | 1 473 | 465 | 4 476 |
| retorno | 743 | 235 | 2 537 |
| **Massa na órbita baixa da Terra** | | | **13 587** |

## i_sistema_unico: (i) saída da Terra com estágio próprio + um só estágio para captura e retorno; cada janela com a sua missão, projeto pela pior janela (janela que define: 2033)

| Estágio | Propelente | Inerte | Massa inicial (com o que carrega) |
| :- | -: | -: | -: |
| saida_terra | 13 946 | 1 501 | 22 953 |
| marte_unico | 4 519 | 1 427 | 7 506 |
| **Massa na órbita baixa da Terra** | | | **22 953** |

## ii_estagios_pior_trecho: (ii) cada estágio pelo pior caso do seu trecho

| Estágio | Propelente | Inerte | Massa inicial (com o que carrega) |
| :- | -: | -: | -: |
| saida_terra | 14 315 | 1 541 | 23 378 |
| insercao_marte | 2 953 | 933 | 7 522 |
| retorno | 1 578 | 498 | 3 636 |
| **Massa na órbita baixa da Terra** | | | **23 378** |

## iii_marte_pior_terra_ref: (iii) estágios de Marte pelo pior caso; saída da Terra pela janela de referência (A)

| Estágio | Propelente | Inerte | Massa inicial (com o que carrega) |
| :- | -: | -: | -: |
| saida_terra | 13 823 | 1 488 | 22 833 |
| insercao_marte | 2 953 | 933 | 7 522 |
| retorno | 1 578 | 498 | 3 636 |
| **Massa na órbita baixa da Terra** | | | **22 833** |

## Sensibilidade da massa na órbita baixa (kg)

Cada linha muda um parâmetro e mantém os demais no caso base.

| Parâmetro | Valor | missao_A | i_sistema_unico | ii_estagios_pior_trecho | iii_marte_pior_terra_ref |
| :- | :- | -: | -: | -: | -: |
| Carga útil | CU-1 | 13 699 | 22 858 | 23 013 | 22 477 |
| Carga útil | CU-2 | 13 587 | 22 953 | 23 378 | 22 833 |
| Carga útil | CU-2b | 12 804 | 21 629 | 22 029 | 21 516 |
| Carga útil | CU-3 | 8 206 | 13 860 | 14 117 | 13 788 |
| Margem de Δv | 0 % | 10 970 | 16 825 | 17 749 | 17 383 |
| Margem de Δv | 5 % | 12 201 | 19 588 | 20 348 | 19 902 |
| Margem de Δv | 10 % | 13 587 | 22 953 | 23 378 | 22 833 |
| Margem de Δv | 20 % | 16 913 | 32 282 | 31 069 | 30 257 |
| Acréscimo na massa da cápsula | 0 % | 13 587 | 22 953 | 23 378 | 22 833 |
| Acréscimo na massa da cápsula | 15 % | 13 704 | 23 149 | 23 577 | 23 028 |
| Acréscimo na massa da cápsula | 30 % | 13 820 | 23 345 | 23 777 | 23 223 |
| Acréscimo na massa da cápsula | 50 % | 13 975 | 23 606 | 24 042 | 23 483 |
| Isp de todos os estágios | -5 % | 15 413 | 27 841 | 27 530 | 26 845 |
| Isp de todos os estágios | +5 % | 12 140 | 19 444 | 20 216 | 19 773 |
| Frações estruturais × fator | 0,50 | 10 268 | 13 663 | 15 589 | 15 277 |
| Frações estruturais × fator | 1,50 | 20 326 | 91 351 | 44 282 | 43 049 |
| Plataforma do orbitador | 331,8 kg | 9 071 | 15 322 | 15 605 | 15 242 |
| Plataforma do orbitador | 850,0 kg | 13 587 | 22 953 | 23 378 | 22 833 |
| Plataforma do orbitador | 2 200,0 kg | 25 352 | 42 834 | 43 626 | 42 611 |
