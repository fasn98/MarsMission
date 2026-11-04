# Roteiro no Onshape: veículos dentro das coifas (gerado por tools/encaixe_coifas.py)

**VERIFICAÇÃO geométrica do modelo, não validação.** O envelope do Vulcan é leitura de figura do guia, e o do Falcon é o STEP do fabricante amostrado.

**Não conferido:** os arquivos não foram compilados aqui, e as páginas de ajuda do Onshape não abriram na consulta. Os nomes de comandos (Commit, Mass Properties, Insert, Group, Measure e os da Assembly) vêm de memória e podem variar. Se algo não bater, anote o que apareceu.

## A. Colar os Feature Studios

1. Abra o documento "MarsMission Fase 7", ou crie um documento novo só para esta etapa.
2. Crie um Feature Studio chamado `envelope_vulcan`.
3. Apague o conteúdo que ele já traz.
4. Cole o conteúdo de `results/etapa7.2b/envelope_vulcan.fs`.
5. Clique em Commit e confira se não há erro.
6. Crie um Feature Studio chamado `envelope_falcon_heavy`.
7. Apague o conteúdo que ele já traz.
8. Cole o conteúdo de `results/etapa7.2b/envelope_falcon_heavy.fs`.
9. Clique em Commit e confira se não há erro.
10. Crie um Feature Studio chamado `lander_4_65`.
11. Apague o conteúdo que ele já traz.
12. Cole o conteúdo de `results/etapa7.2b/lander_4_65.fs`.
13. Clique em Commit e confira se não há erro.
14. Crie um Feature Studio chamado `lander_4_5`.
15. Apague o conteúdo que ele já traz.
16. Cole o conteúdo de `results/etapa7.2b/lander_4_5.fs`.
17. Clique em Commit e confira se não há erro.
18. Crie um Feature Studio chamado `orbitador`.
19. Apague o conteúdo que ele já traz.
20. Cole o conteúdo de `results/etapa7.2b/orbitador.fs`.
21. Clique em Commit e confira se não há erro.

## B. Criar os Part Studios

22. Crie um Part Studio chamado `Vulcan leitura 1`.
23. Adicione a feature "MarsMission envelope Vulcan".
24. Em "Leitura do envelope", escolha "Contorno reto entre as cotas".
25. Crie um Part Studio chamado `Vulcan leitura 2`.
26. Adicione a feature "MarsMission envelope Vulcan".
27. Em "Leitura do envelope", escolha "Diametro menor desde o plano da interface".
28. Crie um Part Studio chamado `Falcon Heavy`.
29. Adicione a feature "MarsMission envelope Falcon Heavy".
30. Crie um Part Studio chamado `Lander 4,65`.
31. Adicione a feature "MarsMission lander_4_65".
32. Marque "Assign materials".
33. Crie um Part Studio chamado `Lander 4,5`.
34. Adicione a feature "MarsMission lander_4_5".
35. Marque "Assign materials".
36. Crie um Part Studio chamado `Orbitador`.
37. Adicione a feature "MarsMission orbitador".
38. Marque "Assign materials".
39. Abra `Lander 4,65`.
40. Selecione todas as peças.
41. Abra Mass Properties. Esperado: 3 190,4 kg e CG em 0,026, −0,026, 3,003 m.
42. Abra `Lander 4,5`.
43. Selecione todas as peças.
44. Abra Mass Properties. Esperado: 3 154,7 kg e CG em 0,026, −0,027, 2,099 m.
45. Abra `Orbitador`.
46. Selecione todas as peças.
47. Abra Mass Properties. Esperado: 6 506,2 kg e CG em 0,000, 0,000, 1,393 m.
48. Confira se cada envelope aparece transparente. Se não aparecer, ajuste a aparência à mão; isso não muda nenhum número.

## C. Montar uma Assembly para cada configuração

| Assembly | Veículo | Envelope |
| :- | :- | :- |
| A1 | Lander 4,5 | Vulcan leitura 1 |
| A2 | Lander 4,5 | Vulcan leitura 2 |
| A3 | Lander 4,65 | Vulcan leitura 1 |
| A4 | Lander 4,65 | Vulcan leitura 2 |
| A5 | Orbitador | Falcon Heavy |

49. Crie uma Assembly para cada linha da tabela (A1, A2, A3, A4, A5). Repita os passos abaixo em cada uma.
50. Clique em Insert e insira o Part Studio do envelope.
51. Clique com o botão direito no envelope e escolha Fix.
52. Insira o Part Studio do veículo, inteiro.
53. Arraste uma peça do veículo.
54. Se ela sair sozinha, selecione todas as peças do veículo e crie um Group, para que andem juntas.
55. Escolha o mate Fastened.
56. Clique no mate connector do envelope, no plano da interface.
57. Clique no mate connector do veículo, no plano da interface.
58. Confirme. O veículo deve ficar dentro do envelope, com o topo para cima.
59. Se o veículo ficar de cabeça para baixo, use a opção de inverter o eixo no diálogo do mate.

## D. Medir as folgas (ferramenta Measure)

Selecione as duas entidades da tabela e leia a distância mínima. A leitura deve bater com o valor esperado na terceira casa.

**Cuidado:** o envelope é uma casca de 0,01 m, e a medida vale na face INTERNA, que fica atrás da externa. Use uma vista em corte (Section view) para selecionar. Medir na externa soma cerca de 0,01 m na leitura. As faces do topo são pequenas: aproxime bem a vista.

| Assembly | Medida | Selecione no veículo | Selecione no envelope | Esperado (m) | Folga com sinal (m) |
| :- | :- | :- | :- | -: | -: |
| A1 | radial | a aresta circular de `Escudo termico (PICA)`, em z = 2,150 m e raio 2,260 m | a face interna na mesma altura | 0,141 | +0,141 |
| A1 | axial | o topo de `Nariz do escudo (PICA)`, em z = 3,000 m | a face interna plana do topo, em z = 12,802 m | 9,802 | +9,802 |
| A2 | radial | a aresta circular de `Escudo termico (PICA)`, em z = 2,150 m e raio 2,260 m | a face interna na mesma altura | 0,064 | +0,064 |
| A2 | axial | o topo de `Nariz do escudo (PICA)`, em z = 3,000 m | a face interna plana do topo, em z = 12,802 m | 9,802 | +9,802 |
| A3 | radial | a aresta circular de `Escudo termico (PICA)`, em z = 3,120 m e raio 2,340 m | a face interna na mesma altura | 0,044 | +0,044 |
| A3 | axial | o topo de `Nariz do escudo (PICA)`, em z = 3,970 m | a face interna plana do topo, em z = 12,802 m | 8,832 | +8,832 |
| A4 | radial | a aresta circular de `Escudo termico (PICA)`, em z = 3,120 m e raio 2,340 m | a face interna na mesma altura | 0,016 | −0,016 |
| A4 | axial | o topo de `Nariz do escudo (PICA)`, em z = 3,970 m | a face interna plana do topo, em z = 12,802 m | 8,832 | +8,832 |
| A5 | radial | a face da peça, perto do ponto mais próximo de `Tanque insercao MON-3 1`, em z = 0,564 m e raio 1,959 m | a face interna na mesma altura | 0,361 | +0,361 |
| A5 | axial | o topo de `EES com o conteiner de amostras`, em z = 5,116 m | a face interna plana do topo, em z = 11,348 m | 6,232 | +6,232 |

O valor esperado é a menor distância entre as superfícies, um pouco menor que a folga horizontal onde o envelope é inclinado. O Measure não mostra o sinal (não conferido): uma folga negativa aparece como valor positivo, e quem diz que há interferência é a seção E.

## E. Rodar Check interference

60. Em cada Assembly, use o comando de interferência (Check interference ou o nome equivalente no menu).
61. Só importam os pares que incluem a peça Envelope. Pares entre peças do próprio veículo vão aparecer, como helicópteros e tanques de descida (folgas.md), e não têm valor esperado aqui (P-095).

| Assembly | Esperado com a peça Envelope |
| :- | :- |
| A1 | nenhuma |
| A2 | nenhuma |
| A3 | nenhuma |
| A4 | interferência com `Escudo termico (PICA)` e `Casca traseira 1 (SLA-561V)`, no ombro |
| A5 | nenhuma |

## F. Anotar

62. Para cada Assembly, anote o valor lido no Measure e o resultado do Check interference.
63. Mande os valores para registro. O estudo compara cada um com o esperado desta página.
